# Benchmark 2026-11-25: Wachiman v1.21.0 with a $10 budget per review

- **Question:** v1.21.0 left 11 to 19 of #467's 47 files unread in every run, because the batches
  started last ran out of the $3 review budget ([focus-file run](../2026-11-25-v1.21.0-focus-replay/README.md)).
  With enough budget to read every file, does it catch what v1.4.0 caught?
- **Runs:** W13 = #32–#36, W14 = #37–#41, W15 = #42–#46 in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-25.
- **Compared with:** W4–W6 ([v1.4.0, 2026-11-02](../2026-11-02/README.md)), W7–W9
  ([v1.20.1](../2026-11-25-v1.20.1-replay/README.md)), W10–W12 (v1.21.0 at $3, focus-file run) and
  W16–W18 ([v1.4.0 again, same day](../2026-11-25-v1.4.0-rerun/README.md)).
- **Per-PR analysis:** [`prs/`](prs/). Raw reviews and comments: [`raw/`](raw/). Rows: `run_label`
  W13–W15 in `dataset/`.

## Result

**Yes, mostly. With $10, every review read every file, and v1.21.0 caught 32 of 81 known-bug
chances, against 27 at $3. v1.4.0, re-run the same day, caught 34.** The budget was the main
cause of the gap: on #467 the catches went from 4 to 10 of 30 (v1.4.0: 12). On the four smaller
pull requests nothing changed (22 or 23 of 51 in every set), because their batches never ran out.

| Per review (15 reviews each) | v1.4.0 (W4–W6) | v1.20.1 (W7–W9) | v1.21.0, $3 (W10–W12) | **v1.21.0, $10 (W13–W15)** | v1.4.0 again (W16–W18) |
| --- | --- | --- | --- | --- | --- |
| Date | 2026-11-02 | 2026-11-25 | 2026-11-25 | 2026-11-25 | 2026-11-25 |
| Review budget (`budget_usd`) | $3 | $3 | $3 | **$10** | $3 |
| Focus file read | yes | no | yes | yes | yes |
| Reviews left partial | 0 | 2 | 3 | **0** | 0 |
| Known bugs caught (of 81) | 35, plus 4 in part | 30, plus 2 | 27, plus 3 | **32, plus 2** | 34, plus 5 |
| … on #463–#466 (of 51) | 24 | 23 | 23 | 22 | 22 |
| … on #467 (of 30) | 11 | 7 | 4 | **10** | 12 |
| Per run | 12, 11, 12 | 10, 9, 11 | 9, 8, 10 | 12, 11, 9 | 9, 11, 14 |
| Distinct known bugs caught by any run (of 27) | 19 | 16 | 13 | 18 | 17 |
| Median cost | $1.00 | $1.09 | $1.12 | $1.14 | $1.12 |
| Total, 15 reviews | $20.87 | $21.45 | $22.04 | $22.25 | $21.47 |
| #467 cost per review | $2.82–$2.98 | $2.75–$3.15 | $2.89–$3.15 | $2.94–$3.03 | $2.81–$2.91 |
| Cost per known bug caught | $0.60 | $0.71 | $0.82 | $0.70 | $0.63 |
| Findings posted | 80 | 61 | 65 | 71 | 78 |
| Turns per batch call | 13.7 | 8.2 | 8.5 | 10.1 | 14.1 |
| Median model time (sum of batch calls) | 158 s | 138 s | 119 s | 121 s | 158 s |
| Median wall time of the Actions run | not measured | 97 s | 86 s | 87 s | 180 s |

## What it means

- **The $3 default is too small for a large pull request on v1.21.0.** #467 costs about $3 to read
  in full on either engine ($2.94–$3.03 here, $2.81–$2.91 on v1.4.0). v1.4.0 runs its batches one
  after another, so it can spend all of the $3. v1.21.0 runs up to 4 at once, and each running
  batch reserves its full $0.75 cap first. The batches that start last find too little left, end on
  `budget`, and leave their files unread. With $10 nothing is reserved away. The review costs the
  same, but every file is read. This is what the
  [budget gate design](https://github.com/niway-dev/wachiman/blob/main/docs/specs/2026-11-21-budget-gate-design.md)
  in the engine repository addresses. Raising `budget_usd` is the workaround until it ships.
- **Speed is kept.** The parallel batches still finish in about half of v1.4.0's wall time (87 s
  against 180 s, both measured today).
- **What is left of the gap is small.** 32 against 34 known bugs, 18 against 17 distinct. That is
  within the spread between runs of one version (v1.4.0 today: 9, 11 and 14 per run).
- **Still different, not yet explained: fewer turns per call** (10.1 against 14.1) **and fewer
  findings** (71 against 78). It does not come from the budget: on the four smaller pull requests
  the turns were 9.9 at $10 and 9.5 at $3. In this sample it did not cost known bugs.
- **Precision.** 11 findings matched no known or earlier bug. The analyst judged 4 valid, 4 partly
  valid, 1 unverified and 2 invalid (#467 N13 and N15, questions the head code answers). The
  v1.4.0 re-run's 11 were 10 valid and 1 partly valid ([its report](../2026-11-25-v1.4.0-rerun/README.md)).

## Conditions

Same as W10–W12 ([conditions table](../2026-11-25-v1.21.0-focus-replay/README.md#conditions))
except for one input:

| Condition | W10–W12 | W13–W15 |
| --- | --- | --- |
| `budget_usd` | 3 (default) | **10** |
| Every other input | Opus 5.5, effort `high`, `verify: false`, engine defaults | same |
| Engine | v1.21.0, `621aa39` | same |
| Base commit | manifest base plus the focus commit (`6e7521b` for #463, `3feb5b1` for the others) | same commits |
| Credential | `CLAUDE_CODE_OAUTH_TOKEN`: cost is an API-equivalent estimate, not a bill | same. The repository also had `ANTHROPIC_API_KEY` from round 2 on; with both set, v1.21.0 uses the token, and every review footer says "Claude subscription" |

## Method

- **Workflow:** [`replay/wachi-workflow-budget-10.yml`](../replay/wachi-workflow-budget-10.yml), which is
  `wachi-workflow.yml` plus `budget_usd: 10`, put on the repository's `main` through the contents API
  (commit `40ff287`) before round 1. Every W13–W15 run used it. `main` went back to
  `wachi-workflow.yml` after the runs.
- **Setup:** [`replay/bench.sh`](../replay/bench.sh) with `BENCH_BRANCH_PREFIX=replay-budget` and
  `BENCH_FOCUS=rename`: `push`, `open`, `rounds 2 3`, `collect`. The stop rule (stop after round 1
  if its median cost is above $2.00) did not trip: round 1's median was $1.14.
- **Labels:** a Claude Sonnet 5.5 subagent matched each finding to the known-bug list and the
  earlier extras, reading the head code in a kaipu-record clone, as for W7–W12. It checked every
  Expected row's cells against its "Label when found" column. Its judgement calls are in each doc.
  The counts above come from `dataset/labelled-runs.csv`.
- **Turns and durations** come from each review's own run (`reviews.csv` `run_id`, joined to
  `run-logs.csv`). Wall time is the Actions run's start to end.

## Limits

- **Three runs per set.** 32 against 34 is not a difference these runs can resolve.
- **The known-bug list was built from earlier versions' runs.** A bug only a newer version sees
  counts as new, not known.
- **One more variable than the budget.** W13–W15 ran after W10–W12 on the same day; nothing else
  in the setup changed.
