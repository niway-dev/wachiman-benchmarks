#!/usr/bin/env python3
"""Print a chunk of a day's raw.jsonl as compact text for a reviewer.

Usage: python3 -I show.py batches/<day>/raw.jsonl <chunk-number> [chunk-size=25]

Chunk 1 is the 25 highest PR numbers of the day. PRs with no bot thread are listed in one line
each (they still matter for Track B when they are fixes).
"""
import json, sys

rows = [json.loads(l) for l in open(sys.argv[1])]
k, size = int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 25
chunk = rows[(k - 1) * size: k * size]
print(f"chunk {k}: PRs #{chunk[0]['number']}..#{chunk[-1]['number']} ({len(chunk)} PRs)\n")
for r in chunk:
    print(f"=== #{r['number']} {r['title']}  [{r['author']}, +{r['additions']}/-{r['deletions']}, "
          f"{r['changedFiles']} files, merge {(r['mergeCommit'] or '')[:10]}]")
    if not r["threads"]:
        print("  (no bot threads)\n")
        continue
    print("  body: " + r["body"][:500].replace("\n", " ") + "\n")
    for i, t in enumerate(r["threads"], 1):
        sev = "/".join(x for x in (t.get("severity"), t.get("category")) if x)
        print(f"  -- T{i} {t['bot']} {sev} {t['path']}:{t['line']} resolved={t['resolved']} outdated={t['outdated']}")
        print("     " + t["body"].replace("\n", "\n     "))
        for rep in t["replies"]:
            print(f"     > [{rep['by']}] " + rep["body"].replace("\n", " "))
        print()
