#!/usr/bin/env bash
# Total reported cost of every traced call of this study (the $8 cap is tracked from this).
# The token-count calls of the prompt comparison are in raw/token-counts/*.json and added by hand.
here="$(cd "$(dirname "$0")" && pwd)"
find "$here/../raw/runs" -name 'call-*.jsonl' -print0 | xargs -0 -I{} sh -c "grep '\"type\":\"result\"' '{}' | tail -n 1" | jq -s '[.[].total_cost_usd] | {calls: length, total_usd: (add // 0)}'
