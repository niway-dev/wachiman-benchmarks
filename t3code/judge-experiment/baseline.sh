#!/usr/bin/env bash
# Baseline review per new case: local Wachiman at the engine worktree, product defaults.
# Resumable: skips cases whose output exists. Usage: ./baseline.sh (reads cases-new.tsv)
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
export WACHIMAN_DIR="${WACHIMAN_DIR:-/tmp/wachiman-judge-exp}"
tail -n +2 "$here/cases-new.tsv" | while IFS=$'\t' read -r set id class intro reviewed rest; do
  sha="${reviewed##*/}"
  out="$here/runs/baseline/$id.json"
  [[ -s "$out" ]] && { echo "skip $id"; continue; }
  start=$(date +%s)
  if env -u ANTHROPIC_API_KEY wachiman local --repo-dir /tmp/t3code-fork --commit "$sha" \
      --profile isolated:personal --format json --output "$out" > "$here/runs/baseline/$id.log" 2>&1; then
    echo "$(date +%T) ok $id $(( $(date +%s) - start ))s"
  else
    echo "$(date +%T) FAIL $id $(( $(date +%s) - start ))s"; rm -f "$out"
  fi
  echo "$id $(( $(date +%s) - start ))" >> "$here/runs/baseline/wall-seconds.txt"
done
