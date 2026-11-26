#!/usr/bin/env bash
# Replay local Wachiman over agent-orchestrator/replays/manifest.tsv, one PR at a time. No scoring.
#
# usage: run-set.sh [-n|--dry-run] <clone-dir> <out-dir> [-- <extra wachiman local args>...]
#   clone-dir  a FULL clone of OrchestratorInc/agent-orchestrator (or a fork) that holds the
#              reviewed heads; fetch them first with `fetch-heads.sh <clone-dir>`
#   out-dir    one <pr>.json and <pr>.log per row (an existing, non-empty json is kept)
#   -n         print the commands, run nothing
#   --         everything after it goes to `wachiman local` unchanged
# env:
#   WACHIMAN_DIR   the Wachiman checkout to run (required; pins the engine version)
#
# Each row is reviewed as base..head, the exact range CodeRabbit first reviewed: a worktree on a
# throwaway branch ao-replay/<pr> (the engine refuses a detached HEAD) is added at head under
# $TMPDIR, `wachiman local --base <base>` runs in it, then the worktree and branch are removed. The clone's own checkout is never touched. Rows run strictly one after the
# other (the mac is shared); a failed row does not stop the rest. ANTHROPIC_API_KEY is never passed
# on, so the run uses the signed-in Claude subscription (isolated:personal).
set -u
usage() { sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-2}"; }
DRY=0
case "${1:-}" in -n|--dry-run) DRY=1; shift ;; -h|--help) usage 0 ;; esac
[ "$#" -ge 2 ] || usage
CLONE=$1; OUT=$2; shift 2
EXTRA=()
if [ "${1:-}" = "--" ]; then shift; EXTRA=("$@"); elif [ "$#" -gt 0 ]; then usage; fi
HERE=$(cd "$(dirname "$0")" && pwd)
MANIFEST=$HERE/../replays/manifest.tsv
unset ANTHROPIC_API_KEY
[ -f "$MANIFEST" ] || { echo "run-set: $MANIFEST not found" >&2; exit 2; }
[ -n "${WACHIMAN_DIR:-}" ] || { echo "run-set: set WACHIMAN_DIR to the engine checkout" >&2; exit 2; }
if [ "$DRY" -eq 0 ]; then
  git -C "$CLONE" rev-parse --git-dir >/dev/null 2>&1 || { echo "run-set: '$CLONE' is not a git clone" >&2; exit 2; }
  [ "$(git -C "$CLONE" rev-parse --is-shallow-repository)" = "false" ] \
    || { echo "run-set: '$CLONE' is a shallow clone; use a full one" >&2; exit 2; }
  mkdir -p "$OUT"; OUT=$(cd "$OUT" && pwd)
fi
# Columns are found by header name. US (0x1f) keeps empty fields through `read`.
LIST=$(awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) col[$i] = i; next }
  { printf "%s\037%s\037%s\n", $col["pr"], $col["base"], $col["head"] }' "$MANIFEST")
TOTAL=$(printf '%s\n' "$LIST" | wc -l | tr -d ' ')
FAILED=(); N=0
while IFS=$'\037' read -r pr base head; do
  N=$((N + 1))
  out=$OUT/$pr.json; log=$OUT/$pr.log
  wt=${TMPDIR:-/tmp}/ao-replay-$pr
  echo "==> [$N/$TOTAL] $pr  $base..$head"
  cmd=(env -u ANTHROPIC_API_KEY "WACHIMAN_DIR=$WACHIMAN_DIR" wachiman local
       --repo-dir "$wt" --base "$base" --profile isolated:personal
       --format json --output "$out" ${EXTRA[@]+"${EXTRA[@]}"})
  if [ "$DRY" -eq 1 ]; then printf '%q ' "${cmd[@]}"; echo; continue; fi
  if [ -s "$out" ]; then echo "    kept: $out already exists"; continue; fi
  for sha in "$base" "$head"; do
    git -C "$CLONE" cat-file -e "$sha^{commit}" 2>/dev/null \
      || { echo "    FAILED: $sha is not in $CLONE" >&2; FAILED+=("$pr (missing $sha)"); continue 2; }
  done
  git -C "$CLONE" merge-base --is-ancestor "$base" "$head" \
    || { echo "    FAILED: base is not an ancestor of head" >&2; FAILED+=("$pr (base not ancestor)"); continue; }
  git -C "$CLONE" worktree remove --force "$wt" >/dev/null 2>&1
  git -C "$CLONE" worktree add --quiet -B "ao-replay/$pr" "$wt" "$head" \
    || { echo "    FAILED: worktree add" >&2; FAILED+=("$pr (worktree)"); continue; }
  echo "    diff: $(git -C "$wt" diff --shortstat "$base" HEAD)"
  start=$(date +%s)
  if "${cmd[@]}" >"$log" 2>&1; then echo "    ok, $(( $(date +%s) - start )) s"
  else rc=$?; echo "    FAILED: exit $rc after $(( $(date +%s) - start )) s (see $log)" >&2
       FAILED+=("$pr (exit $rc)"); rm -f "$out"; fi
  git -C "$CLONE" worktree remove --force "$wt" >/dev/null 2>&1
  git -C "$CLONE" branch -D "ao-replay/$pr" >/dev/null 2>&1
done <<EOF
$LIST
EOF
[ "$DRY" -eq 1 ] && { echo "dry run: $TOTAL row(s), nothing ran"; exit 0; }
echo "done: $((TOTAL - ${#FAILED[@]})) of $TOTAL ran or were kept"
if [ "${#FAILED[@]}" -gt 0 ]; then
  echo "failures:" >&2; printf '  %s\n' "${FAILED[@]}" >&2; exit 1
fi
