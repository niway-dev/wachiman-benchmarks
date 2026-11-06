#!/bin/zsh
# Daily field run: review new kaipu-record PRs locally with Haiku, filter, verify with Opus and
# Sonnet, save CodeRabbit's comments next to them, and push the results to the draft PR.
#
#   field-run.sh            every PR opened since FIELD_SINCE that has no run yet
#   field-run.sh 541 543    only these PRs (re-runs them if a run exists)
#
# Runs on the claude.ai subscription: refuses to start with ANTHROPIC_API_KEY set. Nothing is
# posted to kaipu-record. State lives in ~/.wachiman-field (see the README next to this script).
set -u
setopt null_glob

FIELD_HOME=${FIELD_HOME:-$HOME/.wachiman-field}
FIELD_SINCE=${FIELD_SINCE:-2026-11-06}
REPO=niway-dev/kaipu-record
ENGINE=$FIELD_HOME/engine
KAIPU=$FIELD_HOME/kaipu-record
BENCH=$FIELD_HOME/benchmarks
FIELD=$BENCH/2026-11-field-kaipu
HARNESS=$FIELD/harness
VERIFIERS=(claude-opus-5-5 claude-sonnet-5-5)

# launchd starts with a bare environment: give `claude` the personal login and the tools a PATH.
export USER=${USER:-$(id -un)}
export CLAUDE_CONFIG_DIR=${FIELD_CLAUDE_CONFIG_DIR:-$HOME/.claude-personal}
export PATH=$HOME/.local/bin:$HOME/.bun/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin
export GIT_SSH_COMMAND="ssh -o BatchMode=yes"
unset ANTHROPIC_API_KEY

log() { print -r -- "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

mkdir -p $FIELD/runs $FIELD_HOME/logs
# One run at a time: a second start while one is running exits.
if ! mkdir $FIELD_HOME/.lock 2>/dev/null; then log "another run is in progress"; exit 0; fi
trap 'rmdir $FIELD_HOME/.lock' EXIT

git -C $KAIPU fetch -q origin '+refs/heads/*:refs/remotes/origin/*' '+refs/pull/*/head:refs/remotes/pr/*' || { log "fetch failed"; exit 1; }
git -C $BENCH pull -q --rebase origin field/2026-11-kaipu 2>/dev/null

if (( $# )); then
  prs=($@)
else
  prs=(${(f)"$(gh pr list --repo $REPO --state all --limit 100 --search "created:>=$FIELD_SINCE" --json number --jq '.[].number' | sort -n)"})
fi

ran=0
for pr in $prs; do
  run=$FIELD/runs/pr-$pr
  if (( ! $# )) && [[ -f $run/summary.json ]]; then continue; fi

  info=$(gh pr view $pr --repo $REPO --json title,headRefOid,baseRefName,isDraft,createdAt)
  title=$(print -r -- $info | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["title"])')
  head=$(print -r -- $info | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["headRefOid"])')
  baseRef=$(print -r -- $info | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["baseRefName"])')

  # The commit CodeRabbit reviewed first, so both reviewers read the same code. Until CodeRabbit
  # reviews, wait one day; after that, review the current head and say so.
  crSha=$(gh api "repos/$REPO/pulls/$pr/reviews" --paginate --jq '[.[] | select(.user.login=="coderabbitai[bot]")] | sort_by(.submitted_at) | .[0].commit_id // empty')
  if [[ -n $crSha ]]; then
    sha=$crSha; reason="the first commit CodeRabbit reviewed"
  else
    created=$(print -r -- $info | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["createdAt"])')
    age=$(python3 -I -c "import datetime as d,sys; print(int((d.datetime.now(d.timezone.utc)-d.datetime.fromisoformat(sys.argv[1].replace('Z','+00:00'))).total_seconds()//3600))" $created)
    if (( age < 24 && ! $# )); then log "#$pr: no CodeRabbit review yet, opened ${age} h ago; next run"; continue; fi
    sha=$head; reason="the head at run time (CodeRabbit had not reviewed it)"
  fi
  git -C $KAIPU cat-file -e "$sha^{commit}" 2>/dev/null || git -C $KAIPU fetch -q origin $sha

  base=$(git -C $KAIPU merge-base origin/$baseRef $sha 2>/dev/null)
  if [[ -z $base ]]; then log "#$pr: no merge-base with origin/$baseRef; skipped"; continue; fi
  log "#$pr: reviewing ${sha:0:8} ($reason), base ${base:0:8}"

  wt=$FIELD_HOME/wt/pr-$pr
  git -C $KAIPU worktree remove --force $wt 2>/dev/null
  git -C $KAIPU branch -D field/pr-$pr 2>/dev/null >/dev/null
  git -C $KAIPU worktree add -q -b field/pr-$pr $wt $sha || { log "#$pr: worktree failed"; continue; }

  rm -rf $run; mkdir -p $run
  stat=$(git -C $wt diff --shortstat $base...HEAD)
  files=$(print -r -- $stat | grep -oE '[0-9]+ file' | grep -oE '[0-9]+'); added=$(print -r -- $stat | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+'); removed=$(print -r -- $stat | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+')
  engineVer=$(git -C $ENGINE describe --tags --always)
  python3 -I -c 'import json,sys; a=sys.argv; json.dump({"pr":int(a[1]),"title":a[2],"sha":a[3],"base":a[4],"commitReason":a[5],"files":int(a[6] or 0),"added":int(a[7] or 0),"removed":int(a[8] or 0),"engine":a[9],"ranAt":a[10]},open(a[11],"w"),indent=2)' \
    $pr "$title" $sha $base "$reason" "$files" "$added" "$removed" "$engineVer" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" $run/meta.json

  # 1. Propose: Haiku high, the engine unchanged.
  AGENT_REVIEW_MODEL=claude-haiku-5-5 AGENT_REVIEW_EFFORT=high AGENT_REVIEW_BUDGET_USD=4 \
    bun --no-env-file --config=$ENGINE/bunfig.toml $ENGINE/src/cli.ts local \
    --repo-dir $wt --base $base --max-depth 500 --format json --output $run/haiku.json > $run/haiku.log 2>&1
  code=$?
  if (( code != 0 )) || [[ ! -s $run/haiku.json ]]; then log "#$pr: Haiku review failed (exit $code); see $run/haiku.log"; continue; fi

  # 2. Filter with code, then 3. one verifier call per model.
  python3 -I $HARNESS/verify.py $run $wt $base $VERIFIERS > $run/verify.log 2>&1
  log "#$pr: $(tr '\n' ' ' < $run/verify.log)"

  # 4. CodeRabbit's comments on this PR so far, for the month-end comparison.
  gh api "repos/$REPO/pulls/$pr/comments" --paginate --jq '[.[] | select(.user.login=="coderabbitai[bot]") | {id, path, line, original_line, commit_id, original_commit_id, created_at, body}]' > $run/cr-comments.json
  gh api "repos/$REPO/pulls/$pr/reviews" --paginate --jq '[.[] | select(.user.login=="coderabbitai[bot]") | {id, commit_id, submitted_at, state, body}]' > $run/cr-reviews.json
  python3 -I -c 'import json,sys; c=json.load(open(sys.argv[1])); r=json.load(open(sys.argv[2])); json.dump({"atCommit":sum(1 for x in c if x.get("original_commit_id")==sys.argv[3]),"comments":c,"reviews":r},open(sys.argv[4],"w"),indent=2)' \
    $run/cr-comments.json $run/cr-reviews.json $sha $run/coderabbit.json && rm -f $run/cr-comments.json $run/cr-reviews.json

  python3 -I $HARNESS/report.py $FIELD $pr
  git -C $KAIPU worktree remove --force $wt 2>/dev/null
  ran=$((ran + 1))
done

if (( ran )); then
  git -C $BENCH add 2026-11-field-kaipu
  git -C $BENCH commit -q -m "field: $ran kaipu-record PR(s) reviewed on $(date +%Y-%m-%d)" \
    && git -C $BENCH push -q origin field/2026-11-kaipu \
    && log "pushed $ran run(s)"
else
  log "nothing new"
fi
