#!/bin/bash
S=$1; W=$2; shift 2
for x in "$@"; do set -- $x; BENCH_LOG=1 bun $S/bench/bench.ts $W/src $S/repos/$1 $2 2>$S/bench/log-$1-${2:0:7}.txt >> $S/bench/results.jsonl || echo "fail $1 $2" >> $S/bench/results.jsonl; done
