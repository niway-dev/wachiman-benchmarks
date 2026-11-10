#!/usr/bin/env python3
"""Quality and product-cost metrics for one Wachiman run on Martian's bench.

Quality, from step3 evaluations (Martian's counting):
  - "All" profile: precision, recall, F1, High+Critical found (as step3 prints it).
  - "Core" profile, F2: the metric Martian's site ranks by (analysis/benchmark_dashboard.py,
    default profile core, beta 2). A match on a non-Core golden is "matched-excluded": neither a
    hit nor a false positive. This reproduces analysis/score_profiles.py.
Product cost, from the review JSONs (`execution.costUsdEstimate`, the CLI's API-list-price
estimate): total, per PR (mean, median, p90, max), per 1,000 changed lines, per golden found,
per High/Critical golden found, and review minutes.
Judge cost, from judge_shim JSONL logs if given: kept apart, because it is a cost of measuring,
not of using the product.

Golden text is never printed. Usage:
  python3 -I metrics.py --reviews <reviews-dir> --evals <wachiman-evaluations.json> \
      [--tool wachiman] [--judge-log <calls.jsonl> ...] [--json out.json] [--row]
"""
import argparse
import glob
import json
import os
import statistics

CORE = {"bug", "security", "concurrency", "data", "api", "perf", "test_gap", "doc_defect"}
HC = {"high", "critical"}


def fbeta(p, r, b):
    return (1 + b * b) * p * r / (b * b * p + r) if p + r else 0.0


def quality(evals, tool):
    a = {"tp": 0, "fp": 0, "fn": 0, "hc": 0, "hc_total": 0, "prs": 0, "judge_errors": 0}
    c = {"tp": 0, "fp": 0, "fn": 0}
    for _url, tools in evals.items():
        r = tools.get(tool)
        if not r or r.get("skipped"):
            continue
        a["prs"] += 1
        a["tp"] += r["tp"]; a["fp"] += r["fp"]; a["fn"] += r["fn"]
        a["judge_errors"] += r.get("errors_count", 0)
        tps, fns = r.get("true_positives", []), r.get("false_negatives", [])
        hc_found = sum(1 for g in tps if str(g.get("severity", "")).lower() in HC)
        hc_missed = sum(1 for g in fns if str(g.get("severity", "")).lower() in HC)
        a["hc"] += hc_found; a["hc_total"] += hc_found + hc_missed
        c["tp"] += sum(1 for g in tps if g.get("category") in CORE)
        c["fn"] += sum(1 for g in fns if g.get("category") in CORE)
        c["fp"] += r["fp"]
    out = {}
    for name, m in (("all", a), ("core", c)):
        p = m["tp"] / (m["tp"] + m["fp"]) if m["tp"] + m["fp"] else 0.0
        rc = m["tp"] / (m["tp"] + m["fn"]) if m["tp"] + m["fn"] else 0.0
        out[name] = {**{k: m[k] for k in ("tp", "fp", "fn")}, "precision": p, "recall": rc,
                     "f1": fbeta(p, rc, 1), "f2": fbeta(p, rc, 2)}
    out["all"].update({k: a[k] for k in ("hc", "hc_total", "prs", "judge_errors")})
    return out


def pct(v, q):
    v = sorted(v)
    return v[min(len(v) - 1, int(round(q * (len(v) - 1))))]


def product_cost(reviews_dir):
    costs, minutes, lines, findings, partial, calls = [], [], 0, 0, 0, 0
    for f in sorted(glob.glob(os.path.join(reviews_dir, "**", "*.json"), recursive=True)):
        d = json.load(open(f))
        if "execution" not in d:
            continue
        e = d["execution"]
        costs.append(e["costUsdEstimate"])
        minutes.append(e["durationMs"] / 60000)
        calls += e["calls"]
        lines += sum(b.get("lines", 0) for b in d.get("batches", []))
        findings += len(d.get("findings", []))
        partial += 1 if d["coverage"]["partial"] else 0
    total = sum(costs)
    out = {"reviews": len(costs), "partial_reviews": partial, "calls": calls, "findings": findings,
            "changed_lines": lines, "total_usd": total,
            "per_pr_mean_usd": total / len(costs), "per_pr_median_usd": statistics.median(costs),
            "per_pr_p90_usd": pct(costs, 0.9), "per_pr_max_usd": max(costs),
            "per_1k_lines_usd": total / lines * 1000 if lines else None,
            "minutes_median": statistics.median(minutes), "minutes_max": max(minutes)}
    out["verifier"] = verifier_stats(reviews_dir)
    return out


def verifier_stats(reviews_dir):
    """What the verifier (result /2, v1.10.0 on) did and cost; None for older results."""
    usd, statuses, outcomes, tiers, seen = 0.0, {}, {}, {}, 0
    for f in sorted(glob.glob(os.path.join(reviews_dir, "**", "*.json"), recursive=True)):
        d = json.load(open(f))
        v = d.get("verification")
        if not v:
            continue
        seen += 1
        usd += v.get("costUsd") or 0
        statuses[v["status"]] = statuses.get(v["status"], 0) + 1
        for e in v.get("entries", []):
            outcomes[e["outcome"]] = outcomes.get(e["outcome"], 0) + 1
        for x in d.get("findings", []):
            tiers[x["tier"]] = tiers.get(x["tier"], 0) + 1
    if not seen:
        return None
    return {"reviews": seen, "total_usd": usd, "run_status": statuses, "entry_outcomes": outcomes,
            "posted_tiers": tiers}


def judge_cost(logs):
    n, usd = 0, 0.0
    for p in logs:
        for line in open(p):
            x = json.loads(line)
            if "error" not in x:
                n += 1
                usd += x.get("cost_usd") or 0
    return {"calls": n, "usd": usd}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reviews", required=True)
    ap.add_argument("--evals", required=True)
    ap.add_argument("--tool", default="wachiman")
    ap.add_argument("--judge-log", nargs="*", default=[])
    ap.add_argument("--json")
    ap.add_argument("--row", action="store_true", help="print a history.md table row")
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    q = quality(json.load(open(a.evals)), a.tool)
    pc = product_cost(a.reviews)
    pc["per_golden_found_usd"] = pc["total_usd"] / q["all"]["tp"] if q["all"]["tp"] else None
    pc["per_hc_found_usd"] = pc["total_usd"] / q["all"]["hc"] if q["all"]["hc"] else None
    out = {"quality": q, "product_cost": pc}
    if a.judge_log:
        out["judge_cost"] = judge_cost(a.judge_log)
    if a.json:
        json.dump(out, open(a.json, "w"), indent=2)
    if a.row:
        al, co = q["all"], q["core"]
        print(f"| {a.label} | {al['prs']} | {al['hc']}/{al['hc_total']} | {al['recall']:.1%} | {al['precision']:.1%} "
              f"| {al['f1']:.1%} | {co['f2']:.1%} | {al['fp']} | ${pc['total_usd']:.2f} | ${pc['per_pr_median_usd']:.2f} "
              f"| ${pc['per_pr_p90_usd']:.2f} | ${pc['per_1k_lines_usd']:.2f} | ${pc['per_golden_found_usd']:.2f} "
              f"| ${pc['per_hc_found_usd']:.2f} | {pc['partial_reviews']} |")
    else:
        print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
