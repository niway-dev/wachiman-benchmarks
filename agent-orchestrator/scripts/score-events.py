#!/usr/bin/env python3
"""Unblind the judged review events and print each tool's real defects.

Usage: python3 -I scripts/score-events.py replays/judging-2026-11-26
Reads judge-key.tsv (item -> tool) and out-*.tsv (blind verdicts).
Items in one event that the judge marked `same_as` count as one defect.
"""
import collections
import csv
import glob
import sys

d = sys.argv[1]
key = {r["item"]: r["tool"] for r in csv.DictReader(open(f"{d}/judge-key.tsv"), delimiter="\t")}
judged = {}
for f in sorted(glob.glob(f"{d}/out-*.tsv")):
    for r in csv.DictReader(open(f), delimiter="\t"):
        judged[r["item"]] = r
assert set(judged) == set(key), "every keyed item must be judged once"

print("tool\treal\tstyle\tfalse\tunsure\treal_fixed_later")
for tool in ("coderabbit", "wachiman"):
    rows = [r for i, r in judged.items() if key[i] == tool]
    n = collections.Counter(r["verdict"] for r in rows)
    fixed = sum(1 for r in rows if r["verdict"] == "real" and r["fixed_sha"] not in ("", "-"))
    print(f"{tool}\t{n['real']}\t{n['style']}\t{n['false']}\t{n['unsure']}\t{fixed}")

parent = {i: i for i in judged}
def root(x):
    while parent[x] != x:
        x = parent[x]
    return x
for i, r in judged.items():
    for other in r["same_as"].split(","):
        if other.strip() in judged:
            parent[root(i)] = root(other.strip())
groups = collections.defaultdict(set)
for i, r in judged.items():
    if r["verdict"] == "real":
        groups[root(i)].add(i)

rank = {"low": 0, "medium": 1, "high": 2}
total = collections.Counter()
per_event = collections.defaultdict(collections.Counter)
for members in groups.values():
    tools = {key[i] for i in members}
    side = "both" if len(tools) == 2 else f"{tools.pop()}_only"
    sev = max((judged[i]["severity"] for i in members), key=lambda s: rank.get(s, -1))
    total[(side, sev)] += 1
    per_event[next(iter(members)).rsplit("-i", 1)[0]][side] += 1

print("\ndefects\tlow\tmedium\thigh")
for side in ("both", "coderabbit_only", "wachiman_only"):
    print(side + "\t" + "\t".join(str(total[(side, s)]) for s in ("low", "medium", "high")))
print("\nevent\tboth\tcoderabbit_only\twachiman_only")
for e in sorted(per_event):
    c = per_event[e]
    print(f"{e}\t{c['both']}\t{c['coderabbit_only']}\t{c['wachiman_only']}")
