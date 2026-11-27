#!/usr/bin/env python3
"""Unblind a judging pass with several tools and print each one's real defects.

Usage: python3 -I scripts/score-versions.py replays/judging-2026-11-26-versions
Items in one event that the judge links in `same_as` (any separator) count as one defect.
"""
import collections, csv, glob, re, sys

d = sys.argv[1]
key = {r["item"]: r["tool"] for r in csv.DictReader(open(f"{d}/judge-key.tsv"), delimiter="\t")}
judged = {}
for f in sorted(glob.glob(f"{d}/out-*.tsv")):
    for r in csv.DictReader(open(f), delimiter="\t"):
        judged[r["item"].strip()] = r
assert set(judged) == set(key), "every keyed item must be judged once"
tools = sorted(set(key.values()), key=lambda t: (t != "coderabbit", t))  # the reference first
event = lambda i: i.rsplit("-j", 1)[0]

print("tool\titems\treal\tstyle\tfalse\tunsure\treal_fixed_later")
for t in tools:
    rows = [r for i, r in judged.items() if key[i] == t]
    n = collections.Counter(r["verdict"].strip() for r in rows)
    fixed = sum(1 for r in rows if r["verdict"].strip() == "real" and r["fixed_sha"].strip() not in ("", "-"))
    print(t, len(rows), n["real"], n["style"], n["false"], n["unsure"], fixed, sep="\t")

parent = {i: i for i in judged}
def root(x):
    while parent[x] != x:
        x = parent[x]
    return x
for i, r in judged.items():
    for o in re.split(r"[;,\s]+", r["same_as"]):
        if o in judged and event(o) == event(i):
            parent[root(i)] = root(o)
groups = collections.defaultdict(set)
for i, r in judged.items():
    if r["verdict"].strip() == "real":
        groups[root(i)].add(i)
rank = {"low": 0, "medium": 1, "high": 2}
defects = [({key[i] for i in s}, max((judged[i]["severity"].strip() for i in s), key=lambda x: rank.get(x, -1)))
           for s in groups.values()]

print(f"\ndistinct real defects: {len(defects)}")
print("tool\tdefects\tmedium_or_high\thigh")
for t in tools:
    mine = [s for ts, s in defects if t in ts]
    print(t, len(mine), sum(s in ("medium", "high") for s in mine), sum(s == "high" for s in mine), sep="\t")
ref = tools[0]
print(f"\nagainst {ref}: both, only {ref}, only the other")
for t in tools[1:]:
    print(t, sum(t in ts and ref in ts for ts, _ in defects), sum(ref in ts and t not in ts for ts, _ in defects),
          sum(t in ts and ref not in ts for ts, _ in defects), sep="\t")
others = set(tools[1:])
union = [ts for ts, _ in defects if ts & others]
print(f"\nunion of {', '.join(tools[1:])}: {len(union)} defects, {sum(ref in ts for ts in union)} shared with {ref};"
      f" only {ref}: {sum(ts == {ref} for ts, _ in defects)}")
print(f"found by every one of them: {sum(others <= ts for ts, _ in defects)}; by exactly one: {sum(len(ts & others) == 1 for ts, _ in defects)}")
