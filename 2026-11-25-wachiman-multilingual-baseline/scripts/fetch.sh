#!/bin/zsh
# usage: fetch.sh <root> <case-id> : blobless, depth-limited fetch of one case into <root>/<case-id>.
# Blobs for the changed files are fetched on demand later (run.ts warms them up before timing).
root=$1; id=$2
here=${0:A:h}
IFS=$'\t' read cid corpus url base head label < <(grep "^$id	" $here/cases.tsv)
d=$root/$id; mkdir -p $d; cd $d
[ -d .git ] || { git init -q; git remote add origin $url; git config remote.origin.promisor true; git config remote.origin.partialclonefilter blob:none; }
if [ "$base" != "-" ]; then
  git fetch -q --depth=1 --filter=blob:none origin $head $base || { echo "FAILED $id"; exit 1; }
else
  git fetch -q --depth=2 --filter=blob:none origin $head || { echo "FAILED $id"; exit 1; }
  base=$(git rev-parse $head^)
fi
echo "$base" > $d/.base; echo "$head" > $d/.head
echo "ok $id"
