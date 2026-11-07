#!/usr/bin/env python3
"""Compare two step3 evaluation files for one tool, PR by PR.

Used to calibrate the judge route: Martian's stored Opus 4.5 evaluation of a tool against the same
tool re-judged through judge_shim.py. Prints per-PR TP/FP/FN for both and the totals, and lists
golden comments whose matched/unmatched status differs (by index, not text, so this script never
prints golden contents).

Usage: python3 -I compare_judges.py <stored-evaluations.json> <new-evaluations.json> <tool>
"""
import json
import sys


def golden_key(item):
    # true_positives / false_negatives entries carry the golden comment; identify it by its text hash
    if isinstance(item, dict):
        g = item.get("golden_comment") or item.get("golden") or item.get("comment") or json.dumps(item, sort_keys=True)
    else:
        g = item
    return hash(g if isinstance(g, str) else json.dumps(g, sort_keys=True))


def main():
    stored = json.load(open(sys.argv[1]))
    new = json.load(open(sys.argv[2]))
    tool = sys.argv[3]
    tot = {"stored": [0, 0, 0], "new": [0, 0, 0]}
    flips = 0
    goldens = 0
    print(f"{'PR':<45} {'stored tp/fp/fn':>16} {'new tp/fp/fn':>14}")
    for url in sorted(new):
        n = new[url].get(tool)
        s = stored.get(url, {}).get(tool)
        if not n or not s or n.get("skipped") or s.get("skipped"):
            continue
        for k, r in (("stored", s), ("new", n)):
            tot[k][0] += r["tp"]
            tot[k][1] += r["fp"]
            tot[k][2] += r["fn"]
        # A golden is unmatched when it is in false_negatives; compare those sets.
        st = {golden_key(x) for x in s.get("false_negatives", [])}
        nt = {golden_key(x) for x in n.get("false_negatives", [])}
        goldens += s["total_golden"]
        flips += len(st ^ nt)
        print(f"{url:<45} {s['tp']:>4}/{s['fp']:>3}/{s['fn']:>3}      {n['tp']:>4}/{n['fp']:>3}/{n['fn']:>3}")
    for k, (tp, fp, fn) in tot.items():
        p = tp / (tp + fp) if tp + fp else 0
        r = tp / (tp + fn) if tp + fn else 0
        f1 = 2 * p * r / (p + r) if p + r else 0
        print(f"{k:>6}: tp {tp} fp {fp} fn {fn}  precision {p:.1%} recall {r:.1%} F1 {f1:.1%}")
    print(f"golden comments whose matched status differs: {flips} of {goldens}")


if __name__ == "__main__":
    main()
