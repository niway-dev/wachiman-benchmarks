#!/usr/bin/env bash
# run-v14.sh <events.tsv> <out-dir> [ids...]: replay Wachiman v1.4.0 per review event, offline.
# v1.4.0 has no `local` command: it reviews a GitHub PR. This runs `review <pr>` in dry-run with the
# `gh` and `claude` wrappers of this directory first on PATH. `gh` answers the engine's reads from the
# local clone at the event's base..head and refuses every write; nothing reaches GitHub.
# env: AO_CLONE (full clone), WACHIMAN_V14 (engine checkout at v1.4.0, deps installed),
#      REAL_CLAUDE (claude binary), PR_META_DIR (pr-<n>.json with title, body, author per PR)
set -u
EV=$1; OUT=$2; shift 2; ONLY=" $* "
CLONE=${AO_CLONE:?}; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
tail -n +2 "$EV" | while IFS=$'\t' read -r id pr review base head rest; do
  [ "$ONLY" != "  " ] && [[ "$ONLY" != *" $id "* ]] && continue
  [ -s "$OUT/$id.log" ] && grep -q "^--- review at" "$OUT/$id.log" && { echo "kept $id"; continue; }
  wt=${TMPDIR:-/tmp}/ao-v14-$id
  git -C "$CLONE" worktree remove --force "$wt" >/dev/null 2>&1
  git -C "$CLONE" worktree add --quiet -B "ao-v14/$id" "$wt" "$head" || { echo "FAILED worktree $id"; continue; }
  start=$(date +%s)
  env -u ANTHROPIC_API_KEY -u GITHUB_TOKEN PATH="$HERE:$PATH" GH_TOKEN=offline-shim \
    GITHUB_REPOSITORY=OrchestratorInc/agent-orchestrator AGENT_REVIEW_DRY_RUN=1 \
    AGENT_REVIEW_MODEL=claude-sonnet-5-5 AGENT_REVIEW_EFFORT=high \
    CLAUDE_CONFIG_DIR="$HOME/.wachiman/claude-personal" WACHIMAN_DIR="${WACHIMAN_V14:?}" \
    SHIM_CLONE="$CLONE" SHIM_BASE="$base" SHIM_HEAD="$head" SHIM_PR="$pr" \
    SHIM_META="${PR_META_DIR:?}/pr-$pr.json" SHIM_LOG="$OUT/$id.gh.log" \
    wachiman review "$pr" --repo-dir "$wt" >"$OUT/$id.log" 2>&1
  echo "$id exit $? $(( $(date +%s) - start ))s $(grep -c '^--- ' "$OUT/$id.log") blocks"
  git -C "$CLONE" worktree remove --force "$wt" >/dev/null 2>&1
  git -C "$CLONE" branch -D "ao-v14/$id" >/dev/null 2>&1
done
