#!/usr/bin/env python3
"""Score step3 evaluation files: precision, recall, F1 and High+Critical recall per tool.

Uses Martian's own counting (tp/fp/fn summed over PRs, the "All" profile, as step3 prints it) and
adds High+Critical recall from each golden's severity field. Golden text is never printed.
Optionally restricts to the PRs of one source repo and to the PRs a reference tool has reviewed, so
every row covers the same PRs.

Usage: python3 -I score.py <benchmark_data.json> <evaluations.json>... [--repo cal.com] [--same-as wachiman]
"""
import argparse
import json

HC = {"high", "critical"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("evals", nargs="+")
    ap.add_argument("--repo")
    ap.add_argument("--same-as")
    ap.add_argument("--tools", help="comma-separated tools to show")
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.data))
    merged = {}
    for p in a.evals:  # later files win for the same (pr, tool)
        for url, tools in json.load(open(p)).items():
            merged.setdefault(url, {}).update(tools)
    urls = [u for u in merged if u in data and (not a.repo or data[u]["source_repo"].startswith(a.repo))]
    if a.same_as:
        urls = [u for u in urls if a.same_as in merged[u] and not merged[u][a.same_as].get("skipped")]
    show = set(a.tools.split(",")) if a.tools else None
    rows = {}
    for u in urls:
        hc_total = sum(1 for g in data[u]["golden_comments"] if str(g.get("severity", "")).lower() in HC)
        for tool, r in merged[u].items():
            if r.get("skipped") or (show and tool not in show):
                continue
            m = rows.setdefault(tool, {"tp": 0, "fp": 0, "fn": 0, "hc": 0, "hc_total": 0, "prs": 0, "err": 0})
            m["tp"] += r["tp"]; m["fp"] += r["fp"]; m["fn"] += r["fn"]; m["prs"] += 1
            m["err"] += r.get("errors_count", 0)
            hc_missed = sum(1 for g in r.get("false_negatives", []) if str(g.get("severity", "")).lower() in HC)
            m["hc"] += hc_total - hc_missed; m["hc_total"] += hc_total
    out = []
    for tool, m in rows.items():
        p = m["tp"] / (m["tp"] + m["fp"]) if m["tp"] + m["fp"] else 0
        r = m["tp"] / (m["tp"] + m["fn"]) if m["tp"] + m["fn"] else 0
        f1 = 2 * p * r / (p + r) if p + r else 0
        out.append((f1, tool, m, p, r))
    out.sort(reverse=True)
    if a.markdown:
        print("| # | Tool | PRs | High+Critical found | Recall | Precision | F1 | TP | FP | Judge errors |")
        print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for i, (f1, tool, m, p, r) in enumerate(out, 1):
        hc = f"{m['hc']}/{m['hc_total']}"
        if a.markdown:
            name = f"**{tool}**" if tool == a.same_as else tool
            print(f"| {i} | {name} | {m['prs']} | {hc} | {r:.1%} | {p:.1%} | {f1:.1%} | {m['tp']} | {m['fp']} | {m['err']} |")
        else:
            print(f"{i:>2} {tool:<18} prs {m['prs']:>2}  H+C {hc:>6}  R {r:6.1%}  P {p:6.1%}  F1 {f1:6.1%}  tp {m['tp']:>3} fp {m['fp']:>3} err {m['err']}")


if __name__ == "__main__":
    main()
