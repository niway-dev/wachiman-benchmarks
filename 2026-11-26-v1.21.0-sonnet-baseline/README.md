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
  the contents API (commit `0b6c83e`) before round 1.
- **Pull requests:** the five kaipu-record PRs of the v1.4.0 replay (#463–#467), with the review
  focus file ([`replay/bench.sh`](../replay/bench.sh), `BENCH_BRANCH_PREFIX=replay-sonnet`,
  `BENCH_FOCUS=rename`: `push`, `open`, `rounds 2 3`, `collect`).

## Next release

Run the same set on the next release with only the pin in `wachi-workflow-sonnet.yml` changed, a
new `BENCH_BRANCH_PREFIX`, and label it against the same known-bug list. Report per run: known bugs
found, turns per batch, cost, and how each batch ended. A difference smaller than the spread of
W31–W33 is not a change.

## Result

Pending: the runs are in progress.
