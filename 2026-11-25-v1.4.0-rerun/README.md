# Benchmark 2026-11-25: Wachiman v1.4.0 again, three weeks later

- **Question:** v1.4.0 caught 35 of 81 known-bug chances on 2026-11-02 (W4–W6); today's engines
  caught fewer. Does v1.4.0 itself still catch 35 today, on the same model? If not, part of the gap
  would come from the model or the day, not the engine.
- **Runs:** W16 = #47–#51, W17 = #52–#56, W18 = #57–#61 in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-25.
- **Compared with:** W4–W6 ([2026-11-02](../2026-11-02/README.md)). The comparison with v1.21.0 at
  $3 and at $10 is in the [budget report](../2026-11-25-v1.21.0-budget-replay/README.md).
- **Per-PR analysis:** [`prs/`](prs/). Raw reviews and comments: [`raw/`](raw/). Rows: `run_label`
  W16–W18 in `dataset/`.

## Result

**Yes. v1.4.0 catches about what it caught three weeks ago: 34 of 81, against 35.** So the
model and the setup have not drifted, and the lower counts of v1.20.1 and v1.21.0 at $3 come from
the engine. Most of that is the budget. With $10, v1.21.0 caught 32
([budget report](../2026-11-25-v1.21.0-budget-replay/README.md)).

| Per review (15 reviews each) | v1.4.0, 2026-11-02 (W4–W6) | v1.4.0, 2026-11-25 (W16–W18) |
| --- | --- | --- |
| Known bugs caught (of 81) | 35, plus 4 in part | 34, plus 5 in part |
| … on #463–#466 (of 51) | 24 | 22 |
| … on #467 (of 30) | 11 | 12 |
| Per run | 12, 11, 12 | 9, 11, 14 |
| Distinct known bugs caught by any run (of 27) | 19 | 17 |
| Reviews left partial | 0 | 0 (#467: 47 of 47 files in every run) |
| Median cost | $1.00 | $1.12 |
| Total, 15 reviews | $20.87 | $21.47 |
| Cost per known bug caught | $0.60 | $0.63 |
| Findings posted | 80 | 78 |
| Turns per batch call | 13.7 | 14.1 |
| Median model time (sum of batch calls) | 158 s | 158 s |

- **Run-to-run spread is wide:** 9 to 14 known bugs per run on the same engine, the same model and
  the same commits. Differences of two or three between sets of three runs are within it.
- **New finds:** W17 caught #463 E5, the fingerprint bug no earlier run had posted. 11 findings
  matched no known or earlier bug. The analyst judged 10 valid and 1 partly valid; none invalid.
- **Caught on 2026-11-02 but by no run today:** #463 E1 and E3, #464 E2, #467 E3. Caught today but
  not then: #463 E5, #466 E2, #467 E2. #467 E6 was caught in full then and only in part today
  (from the per-PR docs).

## Conditions

| Condition | W4–W6 | W16–W18 |
| --- | --- | --- |
| Pull requests and commits | kaipu-record #463–#467 at the manifest heads, [`replay/manifest-2026-10-31.tsv`](../replay/manifest-2026-10-31.tsv) | same |
| Base commit | manifest base | manifest base (`BENCH_FOCUS=as-is`) |
| Review focus file | `.github/agent-review.md`, read | same file, read: v1.4.0 reads that name |
| Engine | v1.4.0, by tag | v1.4.0 by SHA, `e09fc2d` (the tag's commit) |
| Caller workflow | kaipu-bench-wachi `efaae4a`: Opus 5.5, effort `high`, `ANTHROPIC_API_KEY` | the same inputs: [`replay/wachi-workflow-v1.4.0.yml`](../replay/wachi-workflow-v1.4.0.yml) |
| Budgets | engine defaults ($3 a review, $0.75 a batch) | same |
| Batches | one at a time | same |
| Credential | API key: billed | API key: billed. v1.4.0 cannot use a subscription token |
| Claude Code | 2.1.304 | 2.1.304 |
| Repository | kaipu-bench-wachi | kaipu-bench-wachi-v3 (`replay-v140/` branches) |
| Runs | 3 per PR, `/wachi review` | same |

## Method

- **Setup:** [`replay/bench.sh`](../replay/bench.sh) with `BENCH_BRANCH_PREFIX=replay-v140` and
  `BENCH_FOCUS=as-is`: `push`, `open`, `rounds 2 3`, `collect`. The workflow above was put on
  `main` through the contents API (commit `4669ee2`) before round 1. `main` went back to
  `wachi-workflow.yml` after the runs. The stop rule (stop after round 1 if its median cost is
  above $2.00) did not trip: round 1's median was $1.15.
- **Labels:** a Claude Sonnet 5.5 subagent matched each finding against the known-bug list and every
  earlier extra, reading the head code, and read the 2026-11-02 docs so it labels v1.4.0's
  phrasing the way W4–W6 were labelled. Its judgement calls are in each doc. Counts come from
  `dataset/labelled-runs.csv`.

## Limits

- **Three runs per date.** 34 against 35 says "the same", not "exactly equal".
- **The 2026-11-02 runs were labelled by other subagents.** The docs share IDs and the "Label when
  found" rules, but two analysts can call a borderline "partial" differently.
