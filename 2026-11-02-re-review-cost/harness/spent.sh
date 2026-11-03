#!/usr/bin/env bash
# Total reported cost of every traced call under raw/runs (the spend cap is tracked from this).
here="$(cd "$(dirname "$0")" && pwd)"
find "$here/../raw/runs" -name 'call-*.jsonl' -print0 | xargs -0 -I{} sh -c "grep '\"type\":\"result\"' '{}' | tail -n 1" | jq -s '[.[].total_cost_usd] | {calls: length, total_usd: (add // 0)}'
