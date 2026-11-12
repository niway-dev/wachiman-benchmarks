# Which model and effort reviews best: Opus, Sonnet and Haiku on Martian

- **Last updated:** 2026-11-12
- **Scope:** Wachiman v1.9.0, no verifier, the same 50 PRs (173 goldens, 66 High or Critical), one run
  per row, every row judged by the same route ([reference/](reference/README.md)).
- **This is the page to read first.** It joins the five model arms, the audit of what the judge calls
  false positives, the scorer experiment and the comparison with other tools. Each claim links to the
  report that holds its data.

## Answer

| Model | Effort to use | Why |
| --- | --- | --- |
| Opus 5.5 | **medium** | Finds the same as high (114 vs 117 goldens, 50 vs 51 High+Critical) with 39 fewer unlisted comments and about 20% less cost. High effort bought nothing measurable |
| Sonnet 5.5 | **high** | Finds the most of all five arms (122 goldens, 52 High+Critical). Medium is half the price but drops to 44 High+Critical |
| Haiku 5.5 | **high** (the only effort measured) | Finds as much as Opus (119 goldens, 52 High+Critical) at $0.19 per PR, with about twice the unlisted comments |

For the main reviewer two arms remain: **Sonnet high** (most found, $0.36 per PR) and **Opus medium**
(fewer minor comments, $0.39 per PR). The recommendation written on 2026-11-12 is Sonnet high, because
the plan is to order and section minor findings with a score, not to reduce them
([scorer](analysis/2026-11-11-scorer/README.md)). **Decided 2026-11-12:** the owner chose Sonnet high; it is
the product default since [wachiman#192](https://github.com/niway-dev/wachiman/pull/192). Two repeat runs
of Sonnet high are measuring run-to-run variance.

## The five arms

| Reviewer | Goldens found (of 173) | High+Critical (of 66) | Judge false positives | Recall | Precision | F1 (All) | F2 (Core) | Findings | $/PR mean | $/PR median | Reviews total | Minutes/review median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Opus 5.5 high ¹ | 117 | 51 | 177 | 67.6% | 39.8% | 50.1% | 58.4% | n/a ² | about $0.50 | $0.48 | about $26 ³ | 1.4 |
| Opus 5.5 medium | 114 | 50 | 138 | 65.9% | 45.2% | 53.6% | 61.0% | 248 | $0.39 | $0.36 | $19.62 | 1.0 |
| Sonnet 5.5 high | 122 | 52 | 190 | 70.5% | 39.1% | 50.3% | 60.4% | 304 | $0.36 | $0.30 | $17.94 | 1.4 |
| Sonnet 5.5 medium | 103 | 44 | 107 | 59.5% | 49.0% | 53.8% | 57.5% | 201 | $0.17 | $0.12 | $8.31 | 0.5 |
| Haiku 5.5 high ¹ | 119 | 52 | 331 | 68.8% | 26.4% | 38.2% | 51.3% | n/a ² | $0.19 | $0.10 | $9.64 | 3.6 |

¹ Totals with the two Keycloak PRs re-run on the right commits
([Opus](runs/2026-11-11-keycloak-range-fix/README.md),
[Haiku](analysis/2026-11-11-scorer/haiku-keycloak-rerun/)). The rows of these two runs in
[history.md](history.md) are the stored originals, before that fix: 110 and 111 goldens, 47 of 66.
The three runs of 2026-11-11 used the corrected worklist from the start.
² Not recomputed for the corrected total. The original runs had 273 (Opus) and 421 (Haiku).
³ $25.01 for the original 50 reviews; the two corrected Keycloak reviews cost $1.47.

Raw data: [Opus high](runs/2026-11-07-v1.9.0-opus-5-5/README.md),
[Opus medium](runs/2026-11-11-v1.9.0-opus-5-5-medium/),
[Sonnet high](runs/2026-11-11-v1.9.0-sonnet-5-5-high/),
[Sonnet medium](runs/2026-11-11-v1.9.0-sonnet-5-5-medium/),
[Haiku high](runs/2026-11-07-v1.9.0-haiku-5-5-high/README.md).

## What effort buys

- **Opus, high to medium:** 3 fewer goldens, 1 fewer High+Critical, 39 fewer judge false positives,
  22% lower mean cost. The quality difference is inside one run's variance.
- **Sonnet, high to medium:** 19 fewer goldens, 8 fewer High+Critical, 83 fewer judge false positives,
  54% lower mean cost. Its higher F1 comes from commenting less, not from finding more.
- **Haiku:** only high was run. Medium and low are not measured.

## What the judge's false positives are

A finding matched to no golden counts as a false positive, and Martian's methodology says the golden
set may be incomplete. GPT-6.1 Sol audited them against the code, one pass, no human check:

| Audited set | Real defect missing from the goldens | True but minor | Wrong | Unverifiable |
| --- | --- | --- | --- | --- |
| Opus high, 85 of its 177 (Cal.com, Sentry) | 34 | 47 | 2 | 2 |
| Haiku high, 67 on Cal.com | 27 | 37 | 1 | 2 |
| Sonnet high, 97 of its 190 (Cal.com, Sentry) | 30 | 60 | 2 | 5 |

So the reviewer almost never invents. Martian precision is a floor, and the gap to the top tools is
the volume of minor comments. Reports: [Opus audit](analysis/2026-11-11-scorer/audit/README.md),
[Haiku audit](analysis/2026-11-11-scorer/audit/haiku/README.md),
[Sonnet audit](analysis/2026-11-11-scorer/audit/sonnet/README.md).

On the same 20 PRs Sonnet high and Opus high are each wrong twice. Sonnet writes more minor comments (60
against 47) and labels severity less sharply: 12 of its 30 unlisted real defects are under `consider`,
against 7 of 34 for Opus.

**Not audited:** the false positives of Opus medium and Sonnet medium; Discourse, Grafana and Keycloak
for any model; Haiku on Sentry. Whether their unlisted comments are the same "true but
minor" kind is unknown.

## Telling serious from minor

Measured on 134 Opus high findings, where serious means matched a golden or audited as a real defect
(83 serious, 51 not):

| Signal | AUC |
| --- | --- |
| 0-10 score by Opus | 0.832 |
| 0-10 score by Haiku (about $0.009 per PR) | 0.825 |
| Wachiman's own severity | 0.784 |
| A Haiku review raised something within 10 lines | 0.634 |

The Haiku scorer does the job of the Opus scorer. It has been measured on Opus findings only.
Report: [scorer experiment](analysis/2026-11-11-scorer/README.md).

## Against other tools

- Of our 34 unlisted real defects, 25 were also raised by at least one of ten other tools, and 15 by
  three or more. Of our 47 minor findings, 24 were raised by another tool.
- The top-ranked tools post far fewer unlisted comments: qodo-extended-v2 106 goldens and 50 false
  positives, augment 108 and 70, cubic-v2 108 and 65 (Martian's published totals, their judge route).
- Report: [other tools](analysis/2026-11-11-scorer/audit/others/README.md). Same-judge reference
  scores: [reference/](reference/README.md#same-judge-scores).

## Limits

- One run per arm. A difference of 1 to 3 High+Critical goldens is inside one run's variance, so the
  table does not rank arms that sit close.
- The Sonnet medium judge step ran twice: its first pass failed on every call because the working
  directory was removed mid-run. The reviews are from the first pass and were not repeated.
- Opus medium was judged with 8 calls in flight, the other two runs of 2026-11-11 with 2. Batch size
  does not change what the judge is asked.
- Cost is at API list prices for the reviews only. The judge's cost is in each `metrics.json`.
- v1.9.0 has no verifier. The v1.10.0 default (Haiku high + Opus verifier) scored below Opus alone:
  [history.md](history.md).
