# Benchmark 2026-11-26: Wachiman v1.22.0 on Sonnet 5.5, same set as the v1.21.0 baseline

- **Question:** whether v1.22.0 changes what the release baseline measures (known bugs found, cost,
  turns per batch) on the same five pull requests, model, credential and budget as the
  [v1.21.0 Sonnet baseline](../2026-11-26-v1.21.0-sonnet-baseline/README.md).
- **Runs:** R1 = #107–#111, R2 = #112–#116, R3 = #117–#121 in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-26. R1–R3
  are labels for this set only; they are not W-numbers.
- **Compared with:** the v1.21.0 Sonnet baseline (W31–W33, #92–#106), same inputs except the engine pin.
- **Known bugs caught:** TODO (labelling is a separate pass; nothing in this file is labelled).

## Setup

- **Engine:** Wachiman v1.22.0 (`79ce0f0`), `claude-sonnet-5-5`, effort `high`, verifier off,
  `budget_usd: 10`. The only change from the baseline caller is the `uses:` pin
  (`621aa39 # v1.21.0` to `79ce0f0 # v1.22.0`) in
  [`replay/wachi-workflow-sonnet.yml`](../replay/wachi-workflow-sonnet.yml). v1.22.0's
  `review.yml` still accepts every input and secret the caller passes (`operator`, `model`,
  `effort`, `verify`, `budget_usd`, `CLAUDE_CODE_OAUTH_TOKEN`); its diff from v1.21.0 only
  deprecates `size_gate_usd` and adds `approve_max_usd` (default 20).
- **Credential:** `CLAUDE_CODE_OAUTH_TOKEN` only; `ANTHROPIC_API_KEY` is not passed. Every batch
  call reports `auth: oauth-token`. Costs are API-equivalent estimates, not a bill.
- **Caller on `main`:** installed through the contents API as `.github/workflows/wachi-bench.yml`
  (commit `972ac73`) before round 1, and replaced by `replay/wachi-workflow.yml` after round 3
  (commit `dfcb6ed`).
- **Pull requests:** the five kaipu-record PRs of the v1.4.0 replay (#463–#467), with the review
  focus file: `BENCH_BRANCH_PREFIX=replay-v1220s`, `BENCH_FOCUS=rename`, `KAIPU_CLONE=/tmp/kaipu-mine/repo`;
  `./bench.sh push`, `open`, `rounds 2 3`, `collect ... v1220s`, as in the baseline.
- **Infrastructure failures:** none. All 15 workflow runs ended `success`; none was rerun.

## Runs

| Run | Replay PRs (kaipu-record #463 to #467) |
| --- | --- |
| R1 | #107, #108, #109, #110, #111 |
| R2 | #112, #113, #114, #115, #116 |
| R3 | #117, #118, #119, #120, #121 |

Raw reviews and comments: [`raw/`](raw/). Every batch call's `wachiman-cost` line:
[`batch-calls.jsonl`](batch-calls.jsonl) (42 calls, taken from the 15 workflow run logs).

## Cost and turns, side by side

Cost per review is the last `<sub>` footer of each posted review; cost per run is the sum of its five
reviews; cost per review in the table is the run's cost / 5. Findings posted is the number of
finding rows in the reviews' tables (fix, consider and for-your-information rows; questions for
the author are not rows). It gives 95 for the baseline; the baseline report's "110" was counted
another way that this pass could not reproduce.

| Per run (5 reviews each) | v1.21.0 baseline (W31, W32, W33) | v1.22.0 (R1, R2, R3) |
| --- | --- | --- |
| Cost per run (API-equivalent) | $5.74, $5.69, $5.88 (mean $5.77) | $4.30, $4.60, $4.80 (mean $4.57) |
| Cost per review (run / 5) | $1.15, $1.14, $1.18 (mean $1.15) | $0.86, $0.92, $0.96 (mean $0.91) |
| #467 cost per review | $2.14 to $2.28 | $1.59 to $1.90 |
| Batch calls | 14, 14, 14 (42) | 14, 14, 14 (42) |
| Turns per batch call, mean | 19.6, 18.9, 19.5 (all 19.3) | 18.0, 20.2, 21.4 (all 19.9) |
| Turns per batch call, min to max | 14 to 31, 11 to 27, 14 to 28 (all 11 to 31) | 11 to 25, 14 to 31, 13 to 32 (all 11 to 32) |
| Cost per batch call, mean (max) | $0.41 ($0.73) | $0.33 ($0.71) |
| Terminal reasons of batch calls | `success` 42 | `success` 42 |
| Reviews left partial | 0, 0, 0 | 0, 0, 0 (every review: whole pull request) |
| Findings posted | 35, 29, 31 (95) | 29, 33, 30 (92) |

Per review cost, v1.22.0 (R1 / R2 / R3): #463 $1.00 / $1.19 / $1.12, #464 $0.45 / $0.57 / $0.59,
#465 $0.64 / $0.62 / $0.66, #466 $0.62 / $0.51 / $0.53, #467 $1.59 / $1.71 / $1.90.

## Limits

- Three runs per set; the baseline's own spread was $5.69 to $5.88 per run.
- Same date and model service as the baseline, not controlled beyond that.
- No label in this file. Known-bug counts: TODO.
