# Benchmark 2026-11-26: Wachiman v1.21.0 on Sonnet 5.5, the release baseline

- **Question:** what the current release finds, costs and how many turns it takes on its default
  model, so the next release can be compared against a measured number instead of a memory.
- **Why it exists:** the drop that the [release bisect](../2026-11-26-release-bisect/README.md)
  traced to the credential (fewer turns on a subscription token under the per-batch cap, see the
  [credential probe](../2026-11-26-credential-probe/README.md)) only shows when the model runs.
  No test or type check sees it. A fixed set run on every release is the detector.
- **Runs:** W31 = #92–#96 (round 1), W32 and W33 (rounds 2 and 3) in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-26.
- **Compared with:** W13–W15 ([v1.21.0 on Opus 5.5, $10, token](../2026-11-25-v1.21.0-budget-replay/README.md)),
  the same release, budget and credential on the other model.

## Setup

- **Engine:** Wachiman v1.21.0 (`621aa39`), `claude-sonnet-5-5`, effort `high`, verifier off,
  `budget_usd: 10` (as W13–W15, so no review ends partial for lack of room).
- **Credential:** `CLAUDE_CODE_OAUTH_TOKEN` only. The caller,
  [`replay/wachi-workflow-sonnet.yml`](../replay/wachi-workflow-sonnet.yml), does not pass
  `ANTHROPIC_API_KEY`, so no run can fall back to it. It was put on the repository's `main` through
  the contents API (commit `0b6c83e`) before round 1, and replaced by `wachi-workflow.yml` again after round 3 (commit `f15a3f4`).
- **Pull requests:** the five kaipu-record PRs of the v1.4.0 replay (#463–#467), with the review
  focus file ([`replay/bench.sh`](../replay/bench.sh), `BENCH_BRANCH_PREFIX=replay-sonnet`,
  `BENCH_FOCUS=rename`: `push`, `open`, `rounds 2 3`, `collect`).

## Next release

Run the same set on the next release with only the pin in `wachi-workflow-sonnet.yml` changed, a
new `BENCH_BRANCH_PREFIX`, and label it against the same known-bug list. Report per run: known bugs
found, turns per batch, cost, and how each batch ended. A difference smaller than the spread of
W31–W33 is not a change.

## Result

**The baseline: on the same five pull requests, v1.21.0 on Sonnet 5.5 caught 16, 14 and 12 of the
27 known bugs per run, at $5.69 to $5.88 a run.** Opus 5.5 on the same release, budget and
credential caught 12, 11 and 9 at about $7.42 a run.

| Per run (5 reviews each) | v1.4.0, Opus, key (W4–W6) | v1.21.0, Opus, token, $10 (W13–W15) | **v1.21.0, Sonnet, token, $10 (W31–W33)** |
| --- | --- | --- | --- |
| Known bugs caught (of 27) | 12, 11, 12 | 12, 11, 9 | **16, 14, 12** |
| … plus caught in part | 0, 2, 2 | 0, 1, 1 | 2, 2, 1 |
| … on #463–#466 (of 17) | 9, 7, 8 | 9, 8, 5 | 12, 10, 9 |
| … on #467 (of 10) | 3, 4, 4 | 3, 3, 4 | 4, 4, 3 |
| Distinct known bugs caught by any run (of 27) | 19 | 18 | 20 |
| Reviews left partial | 0 | 0 | 0 |
| Findings posted, all 15 reviews | 80 | 71 | 110 |
| Invalid findings | — | — | 1 |
| Turns per batch call | 13.7 | 10.1 | **19.3** (42 calls, 11 to 31) |
| Cost per run (API-equivalent on the token) | $6.96 | $7.42 | **$5.74, $5.69, $5.88** |
| #467 cost per review | $2.82–$2.98 | $2.94–$3.03 | $2.14–$2.28 |
| Cost per known bug caught | $0.60 | $0.70 | **$0.41** |

Per pull request and per run, with every label and its evidence: [`prs/`](prs/). Raw reviews and
comments: [`raw/`](raw/). Every batch call's `wachiman-cost` line: [`batch-calls.jsonl`](batch-calls.jsonl).

- **No call ended on its cap.** All 42 batch calls ended `success`. The costliest cost $0.73
  of the $0.75 cap (#463); the mean was $0.41.
- **Sonnet makes about twice the turns of Opus on the token** (19.3 against 10.1). A Sonnet turn costs
  less, so the spend shown against the $0.75 cap grows more slowly; that this is why it keeps going
  is inferred, as in the [credential probe](../2026-11-26-credential-probe/README.md).
- **The first run of a set is not special:** W31 is the highest, W33 the lowest; the spread of
  16 to 12 is the noise this set has to beat.

## What a next release has to show

Run the same set, three runs, and compare with W31–W33. Known bugs per run inside 12 to 16 is no
measured change; so is a cost per run inside $5.69 to $5.88 plus or minus the run-to-run spread.
Only a release whose three runs all fall outside the range has changed something.

## Limits

- **Labels are one Sonnet 5.5 pass per pull request, not blind.** Each labeller saw which run it
  was labelling and the earlier columns. Its judgement calls are written in each `prs/` file.
  W4–W15 were labelled by earlier passes with the same rules, not re-labelled here.
- **Three runs per set.** A difference of two known bugs per run is inside the spread.
- **The known-bug list was built from earlier versions' runs.** A bug only a newer version finds
  appears as a new finding, not in the count of 27.
- **Opus W13–W15 ran on 2026-11-25, Sonnet on 2026-11-26.** The engine, Claude Code version
  (2.1.304) and inputs are the same; the model's service is not controlled.
