#!/usr/bin/env bash
# Compares git grep (one call per name, today's engine) with ripgrep (per name, and all names in one call).
# Usage: rg-vs-grep.sh <checkoutDir> <namesFile>   (SKIP_GIT=1 skips the slow git grep rows)
set -u
dir=$1; names=$2
EXT=(ts tsx js jsx mjs cjs go py rs java kt swift vue svelte)
GG=(); RG=(--hidden --no-ignore -g '!.git/')
for e in "${EXT[@]}"; do GG+=("*.$e"); RG+=(-g "*.$e"); done
for x in node_modules dist build .next vendor; do GG+=(":(exclude)$x/*" ":(exclude)*/$x/*"); RG+=(-g "!$x/"); done
GG+=(":(exclude)*.min.js" ":(exclude)*.d.ts"); RG+=(-g '!*.min.js' -g '!*.d.ts')
N=(); while IFS= read -r l; do [ -n "$l" ] && N+=("$l"); done < "$names"
E=(); for n in "${N[@]}"; do E+=(-e "$n"); done
now() { perl -MTime::HiRes=time -e 'printf "%.0f\n", time*1000'; }
cd "$dir"
echo "names=${#N[@]}"
git grep -q -w -F -e warmup -- "${GG[@]}"; rg -q -w -F -e warmup "${RG[@]}" .
if [ "${SKIP_GIT:-0}" != 1 ]; then
  t=$(now); for n in "${N[@]}"; do git grep -n -I -w -F --no-color -e "$n" -- "${GG[@]}" >/dev/null; done; echo "git_grep_per_name_ms=$(( $(now)-t ))"
fi
t=$(now); for n in "${N[@]}"; do rg -n -w -F -e "$n" "${RG[@]}" . >/dev/null; done; echo "rg_per_name_ms=$(( $(now)-t ))"
t=$(now); c=$(rg -n -w -F "${E[@]}" "${RG[@]}" . | wc -l); echo "rg_one_call_ms=$(( $(now)-t )) lines=$c"
t=$(now); c=$(rg -n -w -F "${E[@]}" "${RG[@]}" -g '!.repos/' . | wc -l); echo "rg_one_call_skip_repos_ms=$(( $(now)-t )) lines=$c"
c=$(git grep -n -I -w -F --no-color "${E[@]}" -- "${GG[@]}" | wc -l); echo "git_grep_one_call_lines=$c (reference count, not timed)"
