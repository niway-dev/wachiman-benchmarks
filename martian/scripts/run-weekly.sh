#!/bin/zsh
# One Wachiman run on Martian's 50 PRs, gentle on a single laptop. See ../README.md#weekly-run.
#
# usage: run-weekly.sh <label> [model] [effort]
#   label   e.g. 2026-11-14-v1.10.0-opus-5-5 (becomes martian/runs/<label>/)
# env:
#   MARTIAN_WORK   cache with repos/, martian-upstream/, venv/ (default ~/.cache/wachiman-martian)
#   QUEUES         review queues in parallel (default 2: two Opus sessions at a time)
#   JUDGE_BATCH    judge calls in flight (default 8)
#   EXTRA_ENV      extra settings for the reviews, e.g. "AGENT_REVIEW_X=1" (an arm)
#   WACHIMAN_ARGS  extra `wachiman local` flags, e.g. "--result-version 2" (v1.10.0 on: keeps the verifier's verdicts)
#   RAM_GB         RAM disk size for snapshots (default 6; two Discourse snapshots need about 4)
# Needs: the installed `wachiman`, ~/.wachiman/claude-personal signed in, ANTHROPIC_API_KEY unset.
set -u
LABEL=$1; MODEL=${2:-claude-opus-5-5}; EFFORT=${3:-high}
HERE=${0:A:h:h}                                   # martian/
W=${MARTIAN_WORK:-$HOME/.cache/wachiman-martian}
QUEUES=${QUEUES:-2}; JUDGE_BATCH=${JUDGE_BATCH:-8}; EXTRA_ENV=${EXTRA_ENV:-}; WACHIMAN_ARGS=${WACHIMAN_ARGS:-}
JM=anthropic/claude-opus-4-5-20251101; JD=anthropic_claude-opus-4-5-20251101
PROFILE=$HOME/.wachiman/claude-personal
RUN=$W/runs/$LABEL; DEST=$HERE/runs/$LABEL
log() { echo "$(date +%H:%M:%S) $*" | tee -a $RUN/run.log; }

[ -n "${ANTHROPIC_API_KEY:-}" ] && { echo "unset ANTHROPIC_API_KEY first"; exit 2; }
[ -d $W/repos ] && [ -d $W/martian-upstream ] && [ -x $W/venv/bin/python ] || { echo "cache missing: see README bootstrap"; exit 2; }
mkdir -p $RUN/reviews $RUN/wt
log "run $LABEL: wachiman $(wachiman --version), model $MODEL, effort $EFFORT, queues $QUEUES ${EXTRA_ENV:+extra: $EXTRA_ENV} ${WACHIMAN_ARGS:+args: $WACHIMAN_ARGS}"

# 1. RAM disk for wachiman's snapshots (the laptop disk is too slow: see the 2026-11-07 report)
RAM=/Volumes/martianram
if [ ! -d $RAM ]; then
  D=$(hdiutil attach -nomount ram://$(( ${RAM_GB:-6} * 2097152 )) | awk '{print $1}')
  diskutil erasevolume APFS martianram $D >/dev/null
fi
mkdir -p $RAM/tmp

# 2. Reviews: QUEUES strictly sequential queues, up to 3 attempts per PR
review_queue() {
  while IFS=$'\t' read repo url n base head fork; do
    out=$RUN/reviews/$repo; mkdir -p $out
    for attempt in 1 2 3; do
      [ -s $out/$n.json ] && break
      wt=$RUN/wt/$repo-$n
      git -C $W/repos/$repo worktree prune
      [ -d $wt ] || git -C $W/repos/$repo worktree add -q $wt pr-$n
      s=$(date +%s)
      env -u ANTHROPIC_API_KEY TMPDIR=$RAM/tmp AGENT_REVIEW_MODEL=$MODEL AGENT_REVIEW_EFFORT=$EFFORT \
        AGENT_REVIEW_BUDGET_USD=10 ${=EXTRA_ENV} \
        wachiman local --repo-dir $wt --base $base --format json --profile isolated:personal \
        --max-depth 1000 ${=WACHIMAN_ARGS} --output $out/$n.json 2> $out/$n.stderr
      log "review $repo $n attempt $attempt exit $? $(( $(date +%s) - s ))s"
    done
    git -C $W/repos/$repo worktree remove --force $RUN/wt/$repo-$n 2>/dev/null
  done < $1
}
tail -n +2 $HERE/worklist.tsv > $RUN/worklist.tsv
for q in $(seq 1 $QUEUES); do awk -v q=$q -v Q=$QUEUES 'NR%Q==q%Q' $RUN/worklist.tsv > $RUN/queue-$q.tsv; done
for q in $(seq 1 $QUEUES); do review_queue $RUN/queue-$q.tsv & done
wait
done_n=$(find $RUN/reviews -name '*.json' -size +0 | wc -l | tr -d ' ')
log "reviews done: $done_n of 50"

# 3. A fresh copy of Martian's offline bench, with Wachiman's findings added
rm -rf $RUN/bench; cp -R $W/martian-upstream/offline $RUN/bench
for repo in $(cut -f1 $RUN/worklist.tsv | sort -u); do
  awk -F'\t' -v r=$repo '$1==r {print $2"\t"$3"\t"$4"\t"$5"\t1\t"$6}' $RUN/worklist.tsv > $RUN/$repo.shas
  python3 -I $HERE/scripts/to_martian.py $RUN/bench $JD $RUN/$repo.shas $RUN/reviews/$repo | tee -a $RUN/run.log
done

# 4. Dedup and judge through the shim, JUDGE_BATCH calls in flight; step3 twice so failed calls retry
env -u ANTHROPIC_API_KEY CLAUDE_CONFIG_DIR=$PROFILE python3 -I $HERE/scripts/judge_shim.py --port 8797 \
  --log $RUN/judge-calls.jsonl --concurrency $JUDGE_BATCH > $RUN/shim.log 2>&1 &
SHIM=$!; trap "kill $SHIM 2>/dev/null" EXIT; sleep 2
step() { (cd $RUN/bench && env -u ANTHROPIC_API_KEY MARTIAN_API_KEY=local-shim MARTIAN_BASE_URL=http://127.0.0.1:8797/v1 \
  MARTIAN_MODEL=$JM $W/venv/bin/python $HERE/scripts/martian_step.py "$@" >> $RUN/judge.log 2>&1) }
step step2_5_dedup_candidates --batch $JUDGE_BATCH -- --tool wachiman
for i in 1 2; do step step3_judge_comments --batch $JUDGE_BATCH -- --tool wachiman --evaluations-file results/$JD/wachiman-evaluations.json; done
log "judging done"

# 5. Metrics and the history row
python3 -I $HERE/scripts/metrics.py --reviews $RUN/reviews --evals $RUN/bench/results/$JD/wachiman-evaluations.json \
  --judge-log $RUN/judge-calls.jsonl --json $RUN/metrics.json
ROW=$(python3 -I $HERE/scripts/metrics.py --reviews $RUN/reviews --evals $RUN/bench/results/$JD/wachiman-evaluations.json --row --label "$LABEL")

# 6. Copy the raw data into the repository
mkdir -p $DEST/data/evaluations $DEST/data/judge-calls
(cd $RUN && find reviews -name '*.json' -size +0 | while read f; do mkdir -p $DEST/data/${f:h}; cp $f $DEST/data/$f; done)   # not .stderr: it holds local paths
cp $RUN/bench/results/$JD/wachiman-evaluations.json $DEST/data/evaluations/wachiman.json
cp $RUN/judge-calls.jsonl $DEST/data/judge-calls/
cp $RUN/metrics.json $RUN/run.log $DEST/
python3 -I -c "
import json,sys
c=json.load(open(sys.argv[1])); g=json.load(open(sys.argv[2]))
json.dump({u:{'wachiman':v['wachiman']} for u,v in c.items() if 'wachiman' in v},open(sys.argv[3],'w'),indent=1)
json.dump({u:{'wachiman':v['wachiman']} for u,v in g.items() if 'wachiman' in v},open(sys.argv[4],'w'),indent=1)
" $RUN/bench/results/$JD/candidates.json $RUN/bench/results/$JD/dedup_groups.json $DEST/data/candidates-wachiman.json $DEST/data/dedup-groups-wachiman.json
log "copied to $DEST"
echo; echo "history.md row:"; echo "$ROW"
