#!/usr/bin/env bash
# One run of one case with one engine: run.sh <case-id> <label> [--dry-run]
# Env: ENGINE (wachiman checkout, default /tmp/rrc/engine-base), KAIPU_CLONE, HEADS (worktrees
# kaipu-<sha7> at each head), FIELD_RAW (wachiman-benchmarks 2026-11-02-field/raw), STATE (meta
# and threads-now dumps), WACHI_X_* (experiment switches read by a prototype engine).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
id="$1"; label="$2"; shift 2
ENGINE="${ENGINE:-/tmp/rrc/engine-base}"
KAIPU_CLONE="${KAIPU_CLONE:-$HOME/Documents/Workspace/Personal/kaipu-record-monorepo}"
HEADS="${HEADS:-/tmp/rrc/heads}"
FIELD_RAW="${FIELD_RAW:-$HOME/Documents/Workspace/Personal/wachiman-benchmarks/2026-11-02-field/raw}"
STATE="${STATE:-$here/../raw/state}"
OUT="${OUT:-$here/../raw/runs}"
line="$(grep -v '^#' "$here/cases.tsv" | awk -F'\t' -v id="$id" '$1==id')"
[ -n "$line" ] || { echo "unknown case $id" >&2; exit 2; }
IFS=$'\t' read -r _ pr head since at basetip _ _ _ <<<"$line"
exec bun "$here/rereview.ts" --engine "$ENGINE" --clone "$KAIPU_CLONE" --repo-dir "$HEADS/kaipu-${head:0:7}" \
  --pr "$pr" --head "$head" --at "$at" --raw "$FIELD_RAW" --threads-now "$STATE/threads-now-pr-$pr.json" \
  --meta "$STATE/meta-pr-$pr.json" --base-tip "$basetip" --out "$OUT/$id/$label" "$@"
