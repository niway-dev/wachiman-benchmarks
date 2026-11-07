#!/bin/zsh
# usage: seq.sh <log> <repo>:<shasfile> ... : strictly one review at a time, up to 3 attempts each
log=$1; shift
for spec in "$@"; do
  r=${spec%%:*}; f=/tmp/martian-run/${spec#*:}; out=/tmp/martian-run/reviews/$r
  while IFS=$'\t' read url n base head commits fork; do
    for attempt in 1 2 3; do
      [ -s $out/$n.json ] && break
      wt=/tmp/martian-run/wt/$r/$n
      [ -d $wt ] || git -C /tmp/martian-run/repos/$r worktree add -q $wt pr-$n
      s=$(date +%s)
      env -u ANTHROPIC_API_KEY TMPDIR=/Volumes/martianram/tmp AGENT_REVIEW_MODEL=claude-opus-5-5 AGENT_REVIEW_EFFORT=high AGENT_REVIEW_BUDGET_USD=10 \
        wachiman local --repo-dir $wt --base $base --format json --profile isolated:personal --max-depth 1000 \
        --output $out/$n.json 2> $out/$n.stderr
      echo "$r $n attempt $attempt exit $? $(( $(date +%s) - s ))s" >> /tmp/martian-run/$log
    done
  done < $f
done
echo "$(date +%H:%M) $log done" >> /tmp/martian-run/orch.log
