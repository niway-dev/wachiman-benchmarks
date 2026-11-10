# v1.10.0 as released: Haiku 5.5 high reviewer + Opus 5.5 verifier

**Verdict: a clear failure.** The verifier, on by default in v1.10.0, removed 14 of 415 findings,
left precision where Haiku alone had it (26%), lost 2 High/Critical goldens (noise range), and
tripled the cost of the review it was checking. Haiku + Opus verifier is worse than Opus alone
on every quality number and costs more.

- **Date:** 2026-11-10, 00:13 to 03:38 local (3 h 25 min).
- **What ran:** Wachiman v1.10.0 as released: reviewer `claude-haiku-5-5` effort `high`, verifier
  `claude-opus-5-5` effort `high` (the defaults), `wachiman local --result-version 2`, one run over
  Martian's 50 PRs with [`run-weekly.sh`](../../scripts/run-weekly.sh). Judge route as the
  [baseline](../2026-11-07-v1.9.0-opus-5-5/README.md).
- **What counts:** every finding the review posts, including `Pre-existing` and `Nit` tiers, because
  that is what a user sees on the PR. Findings the verifier dropped were judged separately (below).
- **Data:** [metrics.json](metrics.json), [metrics-dropped.json](metrics-dropped.json), [data/](data/), [run.log](run.log).

## Result next to the earlier runs

| | Opus 5.5 high (baseline) | Haiku 5.5 high (arm 1) | **v1.10.0: Haiku + Opus verifier** |
| --- | --- | --- | --- |
| High+Critical found | 47/66 | 47/66 | **45/66** |
| Goldens found (recall, All) | 110 (63.6%) | 111 (64.2%) | 106 (61.3%) |
| Findings posted | 273 | 421 | 406 |
| False positives | 174 | 314 | **302** |
| Precision (All) | 38.7% | 26.1% | **26.0%** |
| F1 (All) | 48.1% | 37.1% | **36.5%** |
| F2 (Core, the site's metric) | 55.7% | 49.1% | **47.0%** |
| Reviews, total (API list price) | $25.01 | $8.98 | **$28.62** (reviewer $7.52 + verifier $21.10) |
| $/PR median · p90 · max | $0.48 · $0.61 · $2.31 | $0.10 · $0.35 · $1.90 | **$0.55** · $0.91 · $2.86 |
| $/golden found · $/High+Critical found | $0.23 · $0.53 | $0.08 · $0.19 | **$0.27 · $0.64** |
| Minutes per PR, median · max | 1.4 · 4.4 | 3.6 · 26.5 | 4.8 · 25.7 |
| Partial reviews | 0 | 0 | 0 |

## What the verifier did with Haiku's 415 findings

| Outcome | Findings | Judged |
| --- | --- | --- |
| Kept as is | 339 | |
| Moved one severity down | 51 | |
| Confidence lowered | 11 | |
| **Dropped** | **14 (3.4%)** | 13 false positives, 1 real bug (not High/Critical) |
| Marked pre-existing (posted in its own tier) | 12 | |

Verifier run status: 49 `verified`, 1 `nothing` (a review with no finding above `info`).
Verifier cost: $21.10, 74% of the run; 2.8 times the reviewer it checked.

## Reading

- **The verifier is safe but idle.** When it drops, it is right 13 times of 14. But it drops
  once every 30 findings, and 314 of them were false positives. The rule that a finding is removed
  only on a checkable disproof (a path and a line) is too conservative for Haiku's noise: most false
  positives are not disprovable by one line, they are unsupported claims. The verifier sees them,
  doubts, lowers severity or confidence, and the finding is posted anyway. Those 62 severity and
  confidence moves change nothing in this judge, which ignores both.
- **Cost inverts the premise.** Arm 3 was worth running only if the falsifier cost less than the
  $16 Haiku saves against Opus. It cost $21. Haiku + verifier ($0.55/PR) is above Opus alone
  ($0.48/PR) with 11.6 fewer F1 points.
- **Recall moved within noise** (45 against 47 High/Critical; the rule is 3 or fewer is noise).
  The one dropped real bug does not explain it; Haiku's own run-to-run variance does.
- **Same lesson as crysk's:** detection, not filtering, is the bottleneck, and a refuter that keeps
  everything it cannot disprove does not change precision.

## What this says about v1.10.0's default

Haiku + verifier should not be the default in this form. Two directions worth a measured arm, in
this order:

1. **Opus 5.5 as reviewer with the verifier on** (one variable against the baseline): does the
   verifier cut Opus's 174 false positives, where disproofs may be more common?
2. **Let the verifier drop on "no supporting evidence"** for `consider` and `info` findings, not
   only on a counterexample, and measure how many of the 302 go and how many real bugs with them.

## Cost of the measurement

Judge: 1,746 calls for the run (about $35 at API list price) plus 14 for the dropped findings,
all on the owner's subscription.
