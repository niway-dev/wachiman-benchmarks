# History: Wachiman on the t3code cases

One row per measured run set, newest first. A run set is one variant run over one set of
[`cases.tsv`](cases.tsv). "Caught" means the run states the same cause as the case's `golden_cause`,
not only the same file; "partial" and "noted, not reported" are defined in
[`README.md`](README.md#how-to-score). Cost is the engine's `costUsdEstimate`: an API-price estimate
for a run paid by the owner's Claude subscription, not a bill. Every count comes from the reports
linked in the last column; nothing here was re-judged.

Engines:

- **E1** = [wachiman `c3e46d5`](https://github.com/niway-dev/wachiman/commit/c3e46d598ca5842b0a6abb7230dd2188f6eee87d) (origin/main on 2026-11-12), with a local, uncommitted change: `TIMEOUT_MS` in `src/connectors/local-git.ts` raised from 60 s to 300 s. Arm C and C-Opus add a second local patch, [`engine-arm-c.diff`](contract-order-experiment/engine-arm-c.diff).
- **E2** = [wachiman `fd99401`](https://github.com/niway-dev/wachiman/commit/fd9940100be9287807480cec93ccba07b887131b) (main on 2026-11-11; the reports record no local change), with the 60 s snapshot timeout. The timeout later got a fix: [wachiman PR 195](https://github.com/niway-dev/wachiman/pull/195), merged as [`7b1b6c9`](https://github.com/niway-dev/wachiman/commit/7b1b6c9e5007496b263823b163e48be32553c34d).

- **E3** = [wachiman `aef4422`](https://github.com/niway-dev/wachiman/commit/aef442293e0c5c56366078dd236c001f3c2b4e68) (1.14.0, origin/main on 2026-11-13), with the same local `TIMEOUT_MS` change as E1.

## Runs

| Date | Engine | Reviewer | Variant | Set | Caught of valid | Partial | Noted, not reported | Est. cost | Run files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-13 | E3 | Sonnet 5.5, high | **run 2**, product defaults (control for the judge) | escaped, the 13 cases added 2026-11-13 | **1 of 13** ([#21046](https://github.com/pingdotgg/t3code/pull/21046)) | 1 (#17145) | 3 (#14892, #25239, #16926) | $6.15 | [`runs/baseline-run2/`](judge-experiment/runs/baseline-run2/) |
| 2026-11-13 | E3 | Sonnet 5.5, high | **run 1**, product defaults | escaped, the 13 cases added 2026-11-13 | **1 of 13** ([#21046](https://github.com/pingdotgg/t3code/pull/21046)) | 1 (#17145) | 3 (#14892, #25239, #16926) | $6.65 | [`runs/baseline/`](judge-experiment/runs/baseline/) |
| 2026-11-12 | E2 (wachiman 1.12.0) | Sonnet 5.5, high | first runs, product defaults (verify off, 1 batch); only the model changed | replay, all 5 PRs (21 reachable defects) | **4 PRs comparable with Opus: bugs 4 + 1 partial, minors 2** (Opus: bugs 5 + 1 partial, minors 2 partial); **#33758: 1 of 6** (T1) | see the comparison | unknown | $2.00 ($1.47 on the 4 comparable PRs + $0.53) | [`replays/sonnet-vs-opus.md`](replays/sonnet-vs-opus.md) and each `<pr>/sonnet-high/` |
| 2026-11-12 | E1 + arm C patch | Opus 5.5, high | **C-Opus**: the arm C boundary questions in the batch prompt, same command | escaped, 4 runs (3 valid + 1 invalid case; not run on 2 valid cases for the thread's $8 cap) | **1 of 5** ([#19432](https://github.com/pingdotgg/t3code/pull/19432); it ran on 3 of the 5 valid cases) | 0 | unknown | $2.29 | [`runs/C-opus-*.json`](contract-order-experiment/runs/) |
| 2026-11-12 | E1 + arm C patch | Sonnet 5.5, high | **C**: boundary questions in the batch prompt, asked of every batch | escaped, 7 runs | **0 of 5** | 0 | at least 2 ([#22107](https://github.com/pingdotgg/t3code/pull/22107), #33632); the others unknown | $4.11 | [`runs/C-*.json`](contract-order-experiment/runs/) |
| 2026-11-12 | E1 | Sonnet 5.5, high | **B**: focus file `.github/wachiman.md` asking for flow tracing | escaped, 7 runs | **1 of 5** (#19432) | 0 (the partial of A on [#33632](https://github.com/pingdotgg/t3code/pull/33632) was lost) | at least 2 ([#18505](https://github.com/pingdotgg/t3code/pull/18505), [#33632](https://github.com/pingdotgg/t3code/pull/33632): it cited the lines of the bug and reported nothing); the others unknown | $3.73 | [`runs/B-*.json`](contract-order-experiment/runs/) |
| 2026-11-12 | E1 | Sonnet 5.5, high | **A**: product defaults | escaped, 7 runs | **0 of 5** | 1 ([#33632](https://github.com/pingdotgg/t3code/pull/33632): right cause, wrong trigger) | unknown | $3.49 | [`runs/A-*.json`](contract-order-experiment/runs/) |
| unknown (committed 2026-11-12) | E2 | Opus 5.5, high | repeat runs, product defaults: run 3 of 3 | replay, [#30579](https://github.com/pingdotgg/t3code/pull/30579) only (6 reachable defects) | 3 of 6 (T2, T4, T8; T1 missed) | 0 | unknown | $0.570 | [`run3.json`](replays/30579/experiments/run3.json) |
| unknown (committed 2026-11-12) | E2 | Opus 5.5, high | repeat runs, product defaults: run 2 of 3 | replay, [#30579](https://github.com/pingdotgg/t3code/pull/30579) only (6 reachable defects) | 3 of 6 (T1, T2, T4) | 0 | unknown | $0.570 | [`run2.json`](replays/30579/experiments/run2.json) |
| 2026-11-11 | E2 | Opus 5.5, high | first runs, product defaults (verify off, 1 batch, history off) | replay, 4 of 5 PRs (15 reachable defects) | **5 of 15** | 3 | unknown | $2.53 | [`replays/RESULTS.md`](replays/RESULTS.md) and each `<pr>/wachiman.json` |
| 2026-11-11 and 2026-11-12 | E2 | Opus 5.5, high | first run of [#33758](https://github.com/pingdotgg/t3code/pull/33758): **no review**, 3 attempts failed in the snapshot step with `git add` over the 60 s timeout | replay, [#33758](https://github.com/pingdotgg/t3code/pull/33758) (6 reachable defects) | — | — | — | $0 (no model call) | [`replays/33758/report.md`](replays/33758/report.md) |

Totals of the escaped set: 25 runs, $13.62 (A 3.49 + B 3.73 + C 4.11 + C-Opus 2.29), from the run
files; counts on the 5 valid cases only, because [#21315](https://github.com/pingdotgg/t3code/pull/21315) and [#7599](https://github.com/pingdotgg/t3code/pull/7599) are `valid=no` in
[`cases.tsv`](cases.tsv) (their reviewed diff does not add the defect). Run 1 of the three
repeat runs on [#30579](https://github.com/pingdotgg/t3code/pull/30579) is the same run as that PR's row in the first runs, so it is not listed twice.

The date of the repeat runs is not in their report. The first-run date comes from the [#24079](https://github.com/pingdotgg/t3code/pull/24079) and
[#30556](https://github.com/pingdotgg/t3code/pull/30556) reports (23:34 UTC and 23:19 local on 2026-11-11); the [#30579](https://github.com/pingdotgg/t3code/pull/30579) and [#32830](https://github.com/pingdotgg/t3code/pull/32830) reports give none.
The reviewer on the replays is `claude-opus-5-5`, effort high, as recorded in each
`wachiman.json` (`provider`).

## Second pass over run 1: the hazard judge (2026-11-13)

A second model call that reads run 1's contract notes and the code, and must either build the failing scenario or cite the line that makes it safe. Not a product variant: **the owner decided not to change the product** ([decision](judge-experiment/README.md#decision-owner-2026-11-13)). Full report: [`judge-experiment/README.md`](judge-experiment/README.md).

| Judge | Extra bugs on the 13 new cases | With run 1's own catch | Alarms per review | Wrong alarms | Cost per review | Run files |
| --- | --- | --- | --- | --- | --- | --- |
| Opus 5.5, high | 2 (#14892, #29838) | 3 of 13 | 0.62 | 0 of 8 | $1.15 | [`runs/v2-phase3/`](judge-experiment/runs/v2-phase3/) |
| Opus 5.5, medium | 1 (#29838) | 2 of 13 | 0.23 | 0 of 3 | $0.53 | same |
| Sonnet 5.5, high | 2 (#25239, #29838) | 3 of 13 | 0.46 | 0 of 6 | $0.42 | same |
| Sonnet 5.5, medium | 0 | 1 of 13 | 0.00 | 0 of 0 | $0.09 | same |
| Haiku 5.5, high | 2 (#25239, #29838) | 3 of 13 | 1.23 | 0 of 16 | $0.20 | same |
| control: run 2 | 0 | 1 of 13 | 0.85 | 4 of 11 | $0.47 | [`runs/baseline-run2/`](judge-experiment/runs/baseline-run2/) |

On the first 7 escaped cases every judge caught only [#19432](https://github.com/pingdotgg/t3code/pull/19432), and on [#22107](https://github.com/pingdotgg/t3code/pull/22107) every judge read the spawner and still called it safe. One run per cell. Total spent on the experiment: $86.10 (API-price estimate on the subscription).

## Replay first runs, by case

Caught and partial are counted over the defects reachable at the replay head, one per row of
[`cases.tsv`](cases.tsv); "T" ids are the reference bot threads of each report.

| PR | Reachable defects | Caught | Partial | Missed | Wachiman findings | Est. cost |
| --- | --- | --- | --- | --- | --- | --- |
| [#30579](https://github.com/pingdotgg/t3code/pull/30579) ([report](replays/30579/report.md)) | 6 | 2: T1, T2 (T2 and T6 are one defect) | 0 | 4 real-minor: T3, T4, T5, T8 | 2 | $0.568 |
| [#32830](https://github.com/pingdotgg/t3code/pull/32830) ([report](replays/32830/report.md)) | 2 | 1: T1 (T1 and T3 are one defect) | 0 | 1 real-minor: T2 | 5 | $0.643 |
| [#24079](https://github.com/pingdotgg/t3code/pull/24079) ([report](replays/24079/report.md)) | 4 | 1: T1 | 1: T3 (same root cause, other direction) | 2 serious: T2, T6 | 1 | $0.614 |
| [#30556](https://github.com/pingdotgg/t3code/pull/30556) ([report](replays/30556/report.md)) | 3 | 1: T1 (T1 and T4 are one defect) | 2: T2 and T5 (it asked for a truer message, the bots for a different behavior) | 0 | 2 | $0.705 |
| [#33758](https://github.com/pingdotgg/t3code/pull/33758) ([report](replays/33758/report.md)) | 6 | no Opus run (Sonnet 5.5 high: 1, T1; [comparison](replays/33758/sonnet-high/comparison.md)) | — | — | — | $0 |
| **total, 4 PRs run** | **15** | **5** | **3** | 7 | 10 | **$2.53** |

Reading: the replay set is the bots' best cases (chosen because they got several useful bot
comments), so it measures recall of defects the bots also found, not what the bots missed. Wachiman
also made 4 findings on [#32830](https://github.com/pingdotgg/t3code/pull/32830) that no bot raised (3 real-minor, 1 real but unlikely to trigger).

## The three runs on [#30579](https://github.com/pingdotgg/t3code/pull/30579)

Same engine, model, commit and command; only the run differs. ✓ found, — not found.

| Run | T1 | T2 | T3 | T4 | T5 | T8 | Other findings | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 ([`wachiman.json`](replays/30579/wachiman.json)) | ✓ | ✓ | — | — | — | — | none | $0.568 |
| 2 ([`run2.json`](replays/30579/experiments/run2.json)) | ✓ | ✓ | — | ✓ | — | — | N1 (real cosmetic bug) | $0.570 |
| 3 ([`run3.json`](replays/30579/experiments/run3.json)) | — | ✓ | — | ✓ | — | ✓ | N2 (plausible, not verified) | $0.570 |

The union of the three runs is T1, T2, T4 and T8; T3 and T5 were never found. Even T1, a serious
bug, was missed once. One run is a sample, not a verdict on a PR. Source:
[`replays/30579/experiments/README.md`](replays/30579/experiments/README.md).

## How to add a row

Run [`scripts/run-set.sh`](scripts/run-set.sh), score each output file against `cases.tsv`
([how](README.md#how-to-score)), and add one row at the top: date, engine commit as a URL, model and
effort, what differs from the previous variant, set, counts, cost summed from the files
(`jq -s 'map(.execution.costUsdEstimate) | add'`), and the path of the run files.
