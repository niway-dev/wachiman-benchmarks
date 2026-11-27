# Reconciling two results: Wachiman beats CodeRabbit on the replay set, CodeRabbit beats Wachiman on another repository

Status: **draft protocol**. Nothing in this document is measured yet. The branch that
holds the second repository's data validates it, then fills the blanks marked `TBD`.

## The two results

| | Replay set (kaipu) | Second repository |
|---|---|---|
| Source | `dataset/runs.csv`, `dataset/labels.csv`, `dataset/labelled-runs.csv` | `TBD` (repository, PR list, date range) |
| PRs | 5 PRs that carry a known-bug list (26 known bugs) | `TBD` |
| Metric | Known bugs caught per run ÷ list size, averaged per PR, then across PRs | `TBD`: findings posted per PR (count) |
| Wachiman | 45–47% (v1.4.0 Opus 45%, v1.20.1 47%, v1.21.0 45%) | `TBD` |
| CodeRabbit | 11% | `TBD` |
| Pullfrog | 12% | `TBD` |

The replay figure is a **recall on known bugs**. The observation on the second repository is a
**count of findings**. They are different quantities, so both can be true. This document makes
them comparable instead of arguing from the difference.

## Why both can be true (hypotheses, not findings)

1. **Volume is not recall.** CodeRabbit posts many comments per PR (style, docs, nitpicks). A count
   favours it. Recall on a fixed list of real bugs does not reward volume.
2. **Sample size.** The replay result rests on 5 PRs and 26 bugs. A second repository can
   legitimately contradict it.
3. **Different kinds of PR.** The replay PRs were chosen for having known bugs. The second
   repository may hold PRs where the defects are mostly small ones CodeRabbit is tuned to report.
4. **Judging.** Replay findings were labelled against the known-bug list plus a "real issue, not on
   the list" outcome. If the second repository has no list, "real" is the only outcome and the
   labeller decides alone.
5. **Budget.** Newer Wachiman releases miss bugs mostly because of `budget_usd`, not the engine
   (see the v1.21.0 budget replay). A cap that is fine on the replay set may truncate a review on a
   larger PR, so a low count could be the cap and not the detection.

Each hypothesis predicts something different in the data. The protocol separates them.

## Protocol

Use the same definitions on both repositories so the table above is filled with one metric.

1. **Pin the sample.** List the PRs, the commit SHA of each, and whether CodeRabbit, Pullfrog and
   Wachiman each posted. A PR where a tool did not run is excluded for that tool, never counted as
   zero (same rule as `labelled-runs.csv`).
2. **Run Wachiman on every PR it has not reviewed**, with the release, model and `budget_usd`
   recorded in `dataset/runs.csv`, and the cost in `cost_usd`.
3. **Collect every finding of every tool** into `dataset/findings.csv` with the tool, severity (or
   native severity) and the file and line.
4. **Label each finding with one rubric**, the replay one: *real issue*, *partly right*, *could not
   confirm*, *wrong*, with a short reason. A second labeller (human or a different model) labels a
   sample of at least 30 findings to measure agreement.
5. **Report, per tool and per PR:** findings posted, findings that are real, real findings per PR,
   real findings per dollar, and the share of Wachiman's real findings no other tool found.
6. **Report the budget effect:** list every Wachiman review that hit `budget_usd`, and rerun a
   small subset with a higher cap to see whether the count moves.

## What would change our conclusion

- If CodeRabbit's **real** findings per PR exceed Wachiman's on the second repository with the cap
  not binding, the replay result does not generalise, and the site and README must say so.
- If CodeRabbit leads on **count** but not on **real** findings, the two results agree and the
  report states the difference between volume and precision.
- If Wachiman's low count disappears with a higher cap, the cause is the budget default, and the
  fix is in the engine, not in the benchmark.

## Out of scope

- Changing any published figure before the second repository is labelled.
- Deciding which tool is better overall. The report compares what each tool finds on each
  repository, with the sample size next to every number.

## Blanks for the validating branch

- [ ] Repository, PR list and SHAs.
- [ ] Per-tool findings count and real count.
- [ ] Agreement between the two labellers.
- [ ] Which hypotheses the data supports.
