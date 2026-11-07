#!/bin/zsh
# usage: flatten.sh <repo-dir-name>
# For each PR whose review failed with "no common ancestor": ask GitHub for the true merge base,
# fetch it, and make one commit with the head's exact tree on top of it (message: PR title).
# The diff merge-base -> commit is the pull request's diff; commit messages are lost.
name=$1
cd /tmp/martian-run/repos/$name
: > /tmp/martian-run/$name.flat.shas
while IFS=$'\t' read url n base head commits fork; do
  grep -q "no common ancestor" /tmp/martian-run/reviews/$name/$n.stderr 2>/dev/null || continue
  mb=$(gh api repos/code-review-benchmark/$fork/compare/$base...$head --jq .merge_base_commit.sha) || { echo "FAILED compare $n"; continue; }
  git cat-file -e $mb 2>/dev/null || git fetch -q --depth=1 https://github.com/code-review-benchmark/$fork $mb || { echo "FAILED fetch $n"; continue; }
  title=$(python3 -I -c "import json,sys;print(json.load(open('/tmp/martian-run/bench/results/benchmark_data.json'))[sys.argv[1]]['pr_title'])" "$url")
  flat=$(git commit-tree "$head^{tree}" -p $mb -m "$title")
  git branch -f pr-$n-flat $flat
  rm -f /tmp/martian-run/reviews/$name/$n.json /tmp/martian-run/reviews/$name/$n.stderr
  rm -rf /tmp/martian-run/wt/$name/$n; git worktree prune
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$url" "$n-flat" "$mb" "$flat" 1 "$fork" >> /tmp/martian-run/$name.flat.shas
  echo "flattened $name #$n on $mb"
done < /tmp/martian-run/$name.shas
echo DONE
