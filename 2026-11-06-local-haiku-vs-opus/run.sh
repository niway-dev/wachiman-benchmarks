#!/bin/zsh
# usage: run.sh <pr> <model> <label>
n=$1; model=$2; label=$3
unset ANTHROPIC_API_KEY
cd /tmp/wachi-local/pr-$n || exit 1
AGENT_REVIEW_MODEL=$model AGENT_REVIEW_EFFORT=high AGENT_REVIEW_BUDGET_USD=3 \
  bun --no-env-file --config=/tmp/wachi-local/engine/bunfig.toml /tmp/wachi-local/engine/src/cli.ts local \
  --repo-dir /tmp/wachi-local/pr-$n --base origin/replay/pr-$n/base --format markdown \
  --output /tmp/wachi-local/out/pr$n-$label.md > /tmp/wachi-local/out/pr$n-$label.log 2>&1
echo "pr$n $label exit=$?"
