#!/usr/bin/env bash
# Fetch every manifest PR's head from upstream into <clone-dir> as refs/ao-pr/<pr>, so the
# reviewed commits exist locally. Fetch only: no checkout, no branch change.
# usage: fetch-heads.sh <clone-dir>
set -eu
[ "$#" -eq 1 ] || { sed -n '2,4p' "$0"; exit 2; }
CLONE=$1
URL=https://github.com/OrchestratorInc/agent-orchestrator.git
MANIFEST=$(cd "$(dirname "$0")" && pwd)/../replays/manifest.tsv
refs=$(awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) col[$i] = i; next }
  { printf "refs/pull/%s/head:refs/ao-pr/%s ", $col["pr"], $col["pr"] }' "$MANIFEST")
# shellcheck disable=SC2086
git -C "$CLONE" fetch --quiet "$URL" $refs
echo "fetched: $refs"
