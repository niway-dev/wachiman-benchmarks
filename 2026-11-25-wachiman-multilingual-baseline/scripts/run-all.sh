#!/bin/zsh
# usage: run-all.sh <engine checkout> <clone root> : runs run.ts over every case in cases.tsv, one at a time
# (timings are not run in parallel), one raw/<corpus>.jsonl per corpus.
engine=$1; root=$2
here=${0:A:h}; raw=$here/../raw; mkdir -p $raw; rm -f $raw/*.jsonl
cd $engine
while IFS=$'\t' read id corpus url base head label; do
  echo "== $id" >&2
  bun --no-env-file --config=bunfig.toml $here/run.ts --src $engine/src --repo $root/$id --id $id --runs 5 >> $raw/$corpus.jsonl || echo "FAILED $id" >&2
done < $here/cases.tsv
