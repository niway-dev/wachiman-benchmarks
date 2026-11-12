#!/usr/bin/env python3
"""Recompute a run's totals with some PRs' judgments replaced by a re-run's (counts only, no golden text).

usage: replace_rows.py <original-evals.json> <rerun-evals.json> <rerun-reviews-dir> <original-reviews-dir> \
           [--tool wachiman] [--json out.json]
Metrics are Martian's counting (see metrics.py): All profile P, R, F1, High+Critical found of total.
"""
import argparse, glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from metrics import quality, product_cost

ap = argparse.ArgumentParser()
ap.add_argument("orig"); ap.add_argument("rerun"); ap.add_argument("rerun_reviews"); ap.add_argument("orig_reviews")
ap.add_argument("--tool", default="wachiman"); ap.add_argument("--json")
a = ap.parse_args()
orig, new = json.load(open(a.orig)), json.load(open(a.rerun))
merged = {u: dict(t) for u, t in orig.items()}
per_pr = {}
for u, t in new.items():
    merged[u][a.tool] = t[a.tool]
    for label, ev in (("original", orig[u][a.tool]), ("rerun", t[a.tool])):
        tps, fns = ev.get("true_positives", []), ev.get("false_negatives", [])
        hc = lambda gs: sum(1 for g in gs if str(g.get("severity", "")).lower() in {"high", "critical"})
        per_pr.setdefault(u, {})[label] = {"tp": ev["tp"], "fp": ev["fp"], "fn": ev["fn"],
            "goldens": ev["tp"] + ev["fn"], "hc_found": hc(tps), "hc_total": hc(tps) + hc(fns),
            "errors": ev.get("errors_count", 0)}
out = {"per_pr": per_pr, "original": quality(orig, a.tool), "replaced": quality(merged, a.tool)}
# product cost: original reviews, minus the replaced PRs' files, plus the re-run's
if a.json:
    json.dump(out, open(a.json, "w"), indent=2)
for u, v in per_pr.items():
    print(u, json.dumps(v))
for k in ("original", "replaced"):
    q = out[k]["all"]; c = out[k]["core"]
    print(f"{k}: PRs {q['prs']} R {q['recall']:.1%} P {q['precision']:.1%} F1 {q['f1']:.1%} H+C {q['hc']}/{q['hc_total']} "
          f"TP {q['tp']} FP {q['fp']} FN {q['fn']} | core F2 {c['f2']:.1%} errors {q['judge_errors']}")
