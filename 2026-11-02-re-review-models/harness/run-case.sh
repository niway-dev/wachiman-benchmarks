#!/usr/bin/env bash
# run-case.sh <case-id> <arm> [<arm> ...]: runs the arms of one case in the given order.
# Env: CAP (default 8.00), STOP_AT (default 6.50): no run starts once the reported total is above it.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
. "$here/arms.sh"
OLD="$here/../../2026-11-02-re-review-cost/harness"
export KAIPU_CLONE="${KAIPU_CLONE:-/tmp/rrc2/kaipu}" HEADS="${HEADS:-/tmp/rrc2/heads}"
export FIELD_RAW="${FIELD_RAW:-$here/../../2026-11-02-field/raw}" STATE="$OLD/../raw/state"
export OUT="${OUT:-$here/../raw/runs}"
STOP_AT="${STOP_AT:-6.50}"
case_id="$1"; shift
for a in "$@"; do
  total="$("$here/spent.sh" | jq -r .total_usd)"
  if awk -v t="$total" -v s="$STOP_AT" 'BEGIN{exit !(t>s)}'; then echo "STOP $case_id $a: spent $total > $STOP_AT" | tee -a "$here/../raw/driver.log"; exit 3; fi
  read -r eng model effort <<<"$(arm "$a")"
  echo "$(date -u +%FT%TZ) start $case_id $a ($model $effort $eng) spent=$total" >> "$here/../raw/driver.log"
  ENGINE="/tmp/rrc2/engine-$eng" AGENT_REVIEW_MODEL="$model" AGENT_REVIEW_EFFORT="$effort" \
    "$OLD/run.sh" "$case_id" "$a" > "$OUT/$case_id.$a.stdout" 2> "$OUT/$case_id.$a.stderr"
  echo "$(date -u +%FT%TZ) done  $case_id $a exit=$?" >> "$here/../raw/driver.log"
done
