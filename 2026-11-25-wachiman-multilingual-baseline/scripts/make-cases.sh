#!/bin/zsh
# Writes cases.tsv: id, corpus, remote-url, base, head, label. Martian rows come from the worklist; for
# the "-flat" rows the worklist's head is a local-only commit, so the real PR head is read from the fork's PR #1.
here=${0:A:h}
out=$here/cases.tsv
: > $out
tail -n +2 $here/martian-worklist.tsv | while IFS=$'\t' read repo url n base head fork; do
  num=${url##*/}
  real=$(gh api repos/code-review-benchmark/$fork/pulls/1 --jq .head.sha) || { echo "FAILED $fork" >&2; continue; }
  printf "martian-%s-%s\tmartian\thttps://github.com/code-review-benchmark/%s\t%s\t%s\t%s\n" "$repo" "$num" "$fork" "$base" "$real" "$repo" >> $out
done
# merged PRs measured against the merge commit's first parent (head and base resolved after the fetch)
printf "t3code-39445\tt3code\thttps://github.com/pingdotgg/t3code\t-\tccabed086ad47294173769c77d2d44e55bb8bd0d\tt3code\n" >> $out
printf "t3code-40132\tt3code\thttps://github.com/pingdotgg/t3code\t-\te97290a064dac58dcd425752695bae8743a4dc9a\tt3code\n" >> $out
for p in 8961:65dfabd449b9f736701914a44ab60a06c6b7f003 8893:716af8d46c61ff607ede09661eca65cc9e3bf0eb 8678:4fff577f7fb0be96ff27240cc66a4aee584654b0 9005:feac004ab9c37cb1090f4cfecadaa329be119f7f 8895:657cf5e8001918c24595dfa22d39acfa7ad3eb02; do
  printf "orchestrator-%s\torchestrator\thttps://github.com/OrchestratorInc/agent-orchestrator\t-\t%s\torchestrator\n" ${p%%:*} ${p#*:} >> $out
done
wc -l $out
