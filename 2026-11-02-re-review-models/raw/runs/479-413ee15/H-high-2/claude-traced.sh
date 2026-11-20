#!/bin/bash
export USER="${USER:-$(id -un)}"
if [ "$1" = "--version" ]; then exec "/Users/cristiansotomayor-m5-pro/.local/bin/claude" --version; fi
dir="/tmp/wb-rr/2026-11-02-re-review-models/raw/runs/479-413ee15/H-high-2"
n=1; while [ -e "$dir/call-$n.jsonl" ]; do n=$((n+1)); done
args=(); prev=""
for a in "$@"; do
  if [ "$prev" = "--output-format" ] && [ "$a" = "json" ]; then args+=("stream-json" "--verbose"); else args+=("$a"); fi
  prev="$a"
done
printf '%s\n' "${args[@]}" | grep -v '^{' > "$dir/call-$n.args"
tee "$dir/call-$n.prompt.txt" | "/Users/cristiansotomayor-m5-pro/.local/bin/claude" "${args[@]}" > "$dir/call-$n.jsonl"
status=$?
grep '"type":"result"' "$dir/call-$n.jsonl" | tail -n 1
exit $status
