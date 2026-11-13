#!/usr/bin/env bash
# Run local Wachiman over one set of t3code/cases.tsv, one case at a time. No scoring.
#
# usage: run-set.sh [-n|--dry-run] <clone-dir> <set> <out-dir> [-- <extra wachiman local args>...]
#   clone-dir  a FULL clone (not shallow) that holds the reviewed commits:
#                set escaped: niway-dev/t3code (the fork of pingdotgg/t3code)
#                set replay:  niway-dev/t3code-bench-wachi (the replay commits exist only there)
#   set        escaped | replay
#   out-dir    one <run-id>.json per case is written here (an existing, non-empty file is kept)
#   -n         print the commands, run nothing, check no path
#   --         everything after it goes to `wachiman local` unchanged
# env:
#   WACHIMAN_DIR   the Wachiman checkout to run (required; pins the engine version)
#
# The mac is shared: cases run strictly one after the other, and a case that fails does not stop
# the rest. An API key is never passed on: ANTHROPIC_API_KEY is unset here and again with
# `env -u` in each command, so the run uses the signed-in Claude subscription (isolated:personal).
# Replay rows are one per bot defect; they share one reviewed commit, so a commit runs once.
# Run id = the row's id without a trailing -T<n> (t3code-30579-T1 -> t3code-30579).
# Rows with valid=no are skipped.
set -u

usage() { sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-2}"; }

DRY=0
case "${1:-}" in -n|--dry-run) DRY=1; shift ;; -h|--help) usage 0 ;; esac
[ "$#" -ge 3 ] || usage
CLONE=$1; SET=$2; OUT=$3; shift 3
EXTRA=()
if [ "${1:-}" = "--" ]; then shift; EXTRA=("$@"); elif [ "$#" -gt 0 ]; then usage; fi

HERE=$(cd "$(dirname "$0")" && pwd)
CASES=$HERE/../cases.tsv
unset ANTHROPIC_API_KEY

[ -f "$CASES" ] || { echo "run-set: $CASES not found" >&2; exit 2; }
case "$SET" in escaped|replay) ;; *) echo "run-set: set must be escaped or replay, got '$SET'" >&2; exit 2 ;; esac
[ -n "${WACHIMAN_DIR:-}" ] || { echo "run-set: set WACHIMAN_DIR to the engine checkout" >&2; exit 2; }
if [ "$DRY" -eq 0 ]; then
  [ -d "$WACHIMAN_DIR" ] || { echo "run-set: WACHIMAN_DIR '$WACHIMAN_DIR' is not a directory" >&2; exit 2; }
  git -C "$CLONE" rev-parse --git-dir >/dev/null 2>&1 || { echo "run-set: '$CLONE' is not a git clone" >&2; exit 2; }
  [ "$(git -C "$CLONE" rev-parse --is-shallow-repository)" = "false" ] \
    || { echo "run-set: '$CLONE' is a shallow clone; use a full one" >&2; exit 2; }
  mkdir -p "$OUT"
fi

# One line per case to run: <run-id> US <sha>. Columns are found by header name, so a column
# added to cases.tsv does not break this. US (0x1f) is not whitespace, so empty fields survive read.
LIST=$(awk -F'\t' -v set="$SET" '
  NR == 1 { for (i = 1; i <= NF; i++) col[$i] = i; next }
  $col["set"] == set && $col["valid"] == "yes" {
    id = $col["id"]; sub(/-T[0-9]+$/, "", id)
    sha = $col["reviewed_commit_url"]; sub(/.*\/commit\//, "", sha)
    if (!(sha in seen)) { seen[sha] = 1; printf "%s\037%s\n", id, sha }
  }' "$CASES")
[ -n "$LIST" ] || { echo "run-set: no valid rows for set '$SET' in $CASES" >&2; exit 2; }
TOTAL=$(printf '%s\n' "$LIST" | wc -l | tr -d ' ')

FAILED=(); N=0
while IFS=$'\037' read -r id sha; do
  N=$((N + 1))
  out=$OUT/$id.json
  echo "==> [$N/$TOTAL] $id  $sha"
  cmd=(env -u ANTHROPIC_API_KEY "WACHIMAN_DIR=$WACHIMAN_DIR" wachiman local
       --repo-dir "$CLONE" --commit "$sha" --profile isolated:personal
       --format json --output "$out" ${EXTRA[@]+"${EXTRA[@]}"})
  if [ "$DRY" -eq 1 ]; then printf '%q ' "${cmd[@]}"; echo; continue; fi
  if [ -s "$out" ]; then echo "    kept: $out already exists"; continue; fi
  if ! git -C "$CLONE" cat-file -e "$sha^{commit}" 2>/dev/null; then
    echo "    FAILED: commit $sha is not in $CLONE" >&2; FAILED+=("$id (commit not in clone)"); continue
  fi
  start=$(date +%s)
  if "${cmd[@]}"; then echo "    ok, $(( $(date +%s) - start )) s"
  else rc=$?; echo "    FAILED: exit $rc after $(( $(date +%s) - start )) s" >&2; FAILED+=("$id (exit $rc)"); rm -f "$out"; fi
done <<EOF
$LIST
EOF

[ "$DRY" -eq 1 ] && { echo "dry run: $TOTAL case(s), nothing ran"; exit 0; }
echo "done: $((TOTAL - ${#FAILED[@]})) of $TOTAL ran or were kept"
if [ "${#FAILED[@]}" -gt 0 ]; then
  echo "failures:" >&2; printf '  %s\n' "${FAILED[@]}" >&2; exit 1
fi
