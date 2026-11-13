#!/usr/bin/env python3
"""Aggregate the judge experiment: cost, time, hits and new alarms per config.

Reads runs/, the score files and the alarm files; prints Markdown tables.
Hits and alarm classes come from the label files (worker-labelled, spot-checked);
this script only counts.
"""

from __future__ import annotations

import csv
import glob
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIGS = ["opus-high", "opus-medium", "sonnet-high", "sonnet-medium", "haiku-high"]
PER_BATCH_USD = {"sonnet": 0.32, "opus": 0.5, "haiku": 0.28}  # wachiman src/estimate.ts, origin/main
KNOWN_VALID = {"22107", "19355", "18505", "33632", "19432"}
# Spot-check overrides of worker labels: (phase, case, config, verdict_index) -> label
OVERRIDES = {("p3", "ssh-prompt-queue-never-settles-25239", "sonnet-high", "0"): "partial"}


def tsv(name):
    p = HERE / name
    return list(csv.DictReader(open(p), delimiter="\t")) if p.exists() else []


def judge_runs(phase_dir):
    out = []
    for f in sorted(glob.glob(str(HERE / "runs" / phase_dir / "*.json"))):
        d = json.load(open(f))
        d["_stem"] = Path(f).stem.split("__")[0]
        out.append(d)
    return out


def money(x):
    return f"${x:.2f}"


def main():
    p1, p3 = judge_runs("v2-phase1"), judge_runs("v2-phase3")
    base = {Path(f).stem: json.load(open(f)) for f in glob.glob(str(HERE / "runs/baseline/*.json"))}
    wall = {}
    for line in open(HERE / "runs/baseline/wall-seconds.txt"):
        k, v = line.split()
        wall[k] = int(v)

    # labels
    s1 = tsv("scores-phase1-preliminary.tsv")
    s3 = tsv("scores-phase3-preliminary.tsv")
    for r in s3:
        key = ("p3", r["case_id"], r["config"], r["verdict_index"])
        if key in OVERRIDES:
            r["label"] = OVERRIDES[key]
    a1 = {(r["arm"], r["pr"], r["config"], r["verdict_index"]): r for r in tsv("alarms-phase1.tsv")}
    a3 = {(r["case_id"], r["config"], r["verdict_index"]): r for r in tsv("alarms-phase3.tsv")}

    # hits per config
    hits_known = defaultdict(lambda: {"A": set(), "C": set(), "Apart": set(), "Cpart": set()})
    for r in s1:
        if r["pr"] not in KNOWN_VALID:
            continue
        if r["label"] == "hit":
            hits_known[r["config"]][r["arm"]].add(r["pr"])
        elif r["label"] == "partial":
            hits_known[r["config"]][r["arm"] + "part"].add(r["pr"])
    base_scores = {r["id"]: r["score"] for r in tsv("baseline-scores.tsv")}
    hits_new = defaultdict(set)
    part_new = defaultdict(set)
    for r in s3:
        if r["label"] == "hit":
            hits_new[r["config"]].add(r["case_id"])
        elif r["label"] == "partial":
            part_new[r["config"]].add(r["case_id"])

    # alarms per config (rows labelled other, or partial rows classified as another bug)
    def alarm_counts(rows_by_key, phase):
        per = defaultdict(lambda: defaultdict(int))
        for k, r in rows_by_key.items():
            cfg = k[2] if phase == 1 else k[1]
            if phase == 3 and r.get("label") == "hit":
                continue
            if phase == 3 and r.get("label") == "partial":
                continue  # partials count as near-hits, not alarms
            per[cfg][r["class"]] += 1
            per[cfg]["total"] += 1
        return per

    al1, al3 = alarm_counts(a1, 1), alarm_counts(a3, 3)

    def cost_time(runs):
        c, t, n = defaultdict(float), defaultdict(float), defaultdict(int)
        for d in runs:
            c[d["config"]] += float(d.get("cost_usd") or 0)
            t[d["config"]] += float(d.get("wall_ms") or 0) / 1000
            n[d["config"]] += 1
        return c, t, n

    c1, t1, n1 = cost_time(p1)
    c3, t3, n3 = cost_time(p3)
    n_new = len(base)
    base_cost = sum(b["execution"]["costUsdEstimate"] for b in base.values())
    base_batches = sum(len(b.get("batches", [])) for b in base.values())
    base_wall = sum(wall.values())

    print(f"New cases: {n_new}; baseline caught {sum(1 for v in base_scores.values() if v=='caught')}, "
          f"partial {sum(1 for v in base_scores.values() if v=='partial')}, "
          f"noted-not-reported {sum(1 for v in base_scores.values() if v=='noted-not-reported')}")
    print(f"Baseline: {money(base_cost)} total, {money(base_cost/n_new)} per review, {base_batches} batches, "
          f"{base_wall/n_new:.0f} s per review\n")

    print("| config | phase-3 calls | hits on new cases (of 13) | partial on new | hits known A (of 5) | hits known C (of 5) | "
          "new alarms per review (p3) | wrong (p3) | new alarms per review (p1) | wrong (p1) | cost per review (p3) | time per review (p3) |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for cfg in CONFIGS:
        hk = hits_known[cfg]
        nn = max(n3[cfg], 1)
        print(f"| {cfg} | {n3[cfg]} | {len(hits_new[cfg])} ({', '.join(sorted(x.rsplit('-',1)[1] for x in hits_new[cfg])) or '-'}) | "
              f"{len(part_new[cfg])} | {len(hk['A'])} (+{len(hk['Apart'])}p) | {len(hk['C'])} (+{len(hk['Cpart'])}p) | "
              f"{al3[cfg]['total']/nn:.2f} | {al3[cfg]['wrong']} of {al3[cfg]['total']} | "
              f"{al1[cfg]['total']/14:.2f} | {al1[cfg]['wrong']} of {al1[cfg]['total']} | "
              f"{money(c3[cfg]/nn)} | {t3[cfg]/nn:.0f} s |")
    print()
    print("Alarm classes per config (phase 3 | phase 1):")
    for cfg in CONFIGS:
        print(f"- {cfg}: p3 {dict(al3[cfg])} | p1 {dict(al1[cfg])}")
    print()
    print("Cost per judge call, phase 1 (14 inputs) and phase 3:")
    for cfg in CONFIGS:
        print(f"- {cfg}: p1 {money(c1[cfg])} total / {money(c1[cfg]/max(n1[cfg],1))} per call, {t1[cfg]/max(n1[cfg],1):.0f} s; "
              f"p3 {money(c3[cfg])} / {money(c3[cfg]/max(n3[cfg],1))}, {t3[cfg]/max(n3[cfg],1):.0f} s")
    print()
    opus_est = base_batches * PER_BATCH_USD["opus"] / n_new
    sonnet_est = base_batches * PER_BATCH_USD["sonnet"] / n_new
    print(f"Pair cost per review (new cases): Sonnet-high reviewer measured {money(base_cost/n_new)} "
          f"(estimate.ts: {money(sonnet_est)}); Opus-high reviewer alone, estimate.ts: {money(opus_est)} "
          f"(= measured Sonnet x {PER_BATCH_USD['opus']/PER_BATCH_USD['sonnet']:.2f}: {money(base_cost/n_new*PER_BATCH_USD['opus']/PER_BATCH_USD['sonnet'])})")
    for cfg in CONFIGS:
        nn = max(n3[cfg], 1)
        pair = base_cost / n_new + c3[cfg] / nn
        print(f"- Sonnet high + {cfg}: {money(pair)} per review")
    total = sum(float(json.load(open(f)).get("cost_usd") or 0) for f in glob.glob(str(HERE / "runs/**/*.json"), recursive=True)
                if "cost_usd" in json.load(open(f)))
    print(f"\nRunning total (judge calls incl. v1 and failed calls, plus baselines): {money(total + base_cost)}")


if __name__ == "__main__":
    main()
