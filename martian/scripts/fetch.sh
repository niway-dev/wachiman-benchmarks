#!/bin/zsh
# usage: fetch.sh <repo-dir-name> <list-file: golden_url source fork1,fork2,...>
name=$1; list=$2
mkdir -p /tmp/martian-run/repos/$name && cd /tmp/martian-run/repos/$name
[ -d .git ] || git init -q
while read url src forks; do
  n=${url##*/}
  grep -q "^$url	" /tmp/martian-run/$name.shas 2>/dev/null && { echo "skip $n"; continue; }
  ok=0
  for fork in ${(s:,:)forks}; do
    meta=$(gh api repos/code-review-benchmark/$fork/pulls/1 --jq '[.base.sha,.head.sha,.commits]|@tsv' 2>/dev/null) || continue
    read base head commits <<<"$meta"
    git fetch -q --depth=$((commits+5)) https://github.com/code-review-benchmark/$fork $head 2>/dev/null || continue
    git branch -f pr-$n $head
    git cat-file -e $base 2>/dev/null || git fetch -q --depth=1 https://github.com/code-review-benchmark/$fork $base || continue
    printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$url" "$n" "$base" "$head" "$commits" "$fork" >> /tmp/martian-run/$name.shas
    echo "fetched $name #$n via $fork"; ok=1; break
  done
  [ $ok = 1 ] || echo "FAILED $name #$n"
done < $list
echo DONE
