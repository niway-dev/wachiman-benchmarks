# Benchmark 2026-11-26: Wachiman v1.22.0 on Sonnet 5.5, same set as the v1.21.0 baseline

- **Question:** whether v1.22.0 changes what the release baseline measures (known bugs found, cost,
  turns per batch) on the same five pull requests, model, credential and budget as the
  [v1.21.0 Sonnet baseline](../2026-11-26-v1.21.0-sonnet-baseline/README.md).
- **Runs:** R1 = #107–#111, R2 = #112–#116, R3 = #117–#121 in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-26. R1–R3
  are labels for this set only; they are not W-numbers.
- **Compared with:** the v1.21.0 Sonnet baseline (W31–W33, #92–#106), same inputs except the engine pin.
- **Answer:** v1.22.0 costs less, with no detectable change in known bugs found. It catches 13,
  14 and 12 of the 27 known bugs per run (baseline: 16, 14 and 12), at $4.30 to $4.80 a run
  (baseline: $5.69 to $5.88). Under the release rule below, cost changed and known bugs did not.

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
reviews; cost per review in the table is the run's cost / 5. Findings posted counts
every item the reviews posted: inline comments, findings listed with no thread, and questions
in the body, duplicates included. That is the baseline's method; the per-PR counts are in
[`prs/`](prs/). Counting only the rows of the reviews' finding tables instead gives 95 for the
baseline and 92 here.

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
| Findings posted (every item) | 110 in all | 34, 42, 36 (112) |
| Findings posted (table rows only) | 35, 29, 31 (95) | 29, 33, 30 (92) |
| Known bugs caught (of 27) | 16, 14, 12 (mean 14.0) | 13, 14, 12 (mean 13.0) |
| Cost per known bug caught (mean run / mean bugs) | $0.41 | $0.35 |

Per review cost, v1.22.0 (R1 / R2 / R3): #463 $1.00 / $1.19 / $1.12, #464 $0.45 / $0.57 / $0.59,
#465 $0.64 / $0.62 / $0.66, #466 $0.62 / $0.51 / $0.53, #467 $1.59 / $1.71 / $1.90.

## Known bugs per pull request

Labelled against the baseline's known-bug list, one file per pull request in [`prs/`](prs/). A
partial (the right place, not the right mechanism) is not counted.

| Kaipu PR (known bugs) | R1 | R2 | R3 |
| --- | --- | --- | --- |
| [#463](prs/pr-463.md) (6) | 2 | 3 | 3 |
| [#464](prs/pr-464.md) (4) | 3 | 2 | 2 |
| [#465](prs/pr-465.md) (3) | 3 | 1 | 1 |
| [#466](prs/pr-466.md) (4) | 2 | 4 | 3 |
| [#467](prs/pr-467.md) (10) | 3 | 4 | 3 |
| **Total (27)** | **13** | **14** | **12** |

#466's 4 in R2 includes a borderline E1 call (explained in its file); a strict reading gives 3,
and R2's total 13. #463's E1 in R3 is also borderline (a hedged question with no fix); a strict
reading gives 2 there, and R3's total 11. Even then, R1 and R2 stay inside 12 to 16, so the
verdict below holds. Caught in part (not counted): 2, 2 and 1 (baseline: 2, 2 and 1). Invalid findings: 0, 1 and 2
(one on #466 in R2, two on #467 in R3; baseline: 1 across its three runs).

The 27 include #464's E4, which is not present at that pull request's head, so no run can find it.
The baseline counts it the same way, so the comparison is fair, but 26 is the real ceiling.

## Verdict under the release rule

The baseline's rule: a measure changed only if all three runs fall outside the baseline's range.

- **Cost: changed.** All three runs ($4.30, $4.60, $4.80) are below the baseline's cheapest
  ($5.69). Cost per review falls from $1.15 to $0.91, about 21%.
- **Known bugs: no detectable change.** All three runs (13, 14, 12) are inside 12 to 16. The mean
  is one lower (13.0 against 14.0), which is inside the baseline's own spread.
- **Turns per batch call: no change.** Mean 19.9 against 19.3, same spread.

## Why it costs less: same tokens, cheaper cache writes

Summed over the 42 batch calls of each set (from each `batch-calls.jsonl`), v1.22.0 did the same
work as v1.21.0, or slightly more, and paid less for it:

| 42 batch calls | v1.21.0 | v1.22.0 |
| --- | --- | --- |
| Cache read tokens | 19.95 M | 21.66 M |
| Cache write tokens | 2.79 M | 2.83 M |
| Output tokens | 0.41 M | 0.44 M |
| Cost (API-equivalent) | $17.30 | $13.69 |

Fewer tokens did not lower the cost; a lower price per token did. The only change in v1.22.0
that moves a token price is the prompt cache lifetime: Claude Code on the subscription token
wrote a 1-hour cache, and v1.22.0 forces 5 minutes (`promptCacheTtl: "5m"`). A 1-hour write is
priced higher than a 5-minute write; the [5-minute cache experiment](../2026-11-26-prompt-cache-5m/README.md)
measured $8 against $5 per million written tokens on Opus 5.5, by fitting each call's cost.

- **Measured:** the token counts and costs above; every call ran on the token.
- **Measured: the write price fell, nothing else did.** Fitting each batch call's cost to its
  token counts (least squares, 42 calls per set, largest error under 0.01%) gives the same
  prices for reads ($0.10 per million) and output ($10) in both sets, and a cache write of $4.00
  per million in v1.21.0 against $2.50 in v1.22.0. Those are Sonnet 5.5's 1-hour and 5-minute
  write prices, the same 1.6 ratio as Opus's $8 and $5. At the old write price, v1.22.0's tokens
  would have cost $17.93. Writes saved $4.25, the extra reads, writes and output gave back $0.64, and
  the set cost $3.61 less.
- **Unlike the Opus experiment, turns did not rise** (19.9 against 19.3 per batch call). The
  saving here comes from price alone.
- **The start floor most likely did not act:** with a $10 budget, no batch ran short of money. A
  set at the default $3 budget would exercise it.

## Against v1.4.0, the release before the token

The same five pull requests, labelled against the same 27 known bugs. The v1.4.0 set ran on Opus
5.5 with an API key (W4 to W6, from the [v1.21.0 Sonnet baseline](../2026-11-26-v1.21.0-sonnet-baseline/README.md)):

| Per run | v1.4.0, Opus, API key (W4–W6) | v1.22.0, Sonnet, token (R1–R3) |
| --- | --- | --- |
| Known bugs caught (of 27) | 12, 11, 12 | 13, 14, 12 |
| Cost per run, mean (API-equivalent) | $6.96 | $4.57 |
| Cost per known bug caught | $0.60 | $0.35 |

v1.22.0 on Sonnet catches at least as many known bugs for about a third less per run. Under the
release rule it does not catch *more*: R3 (12) ties v1.4.0's best run. The two sets also differ in
model and credential, not only in release, so this compares what a user ran then with what a
user runs now; it does not isolate the engine. The W4 to W6 labels also come from earlier labelling passes (copied
into each `prs/` file), not from the pass that labelled R1 to R3.

## Limits

- Three runs per set; the baseline's own spread was $5.69 to $5.88 per run.
- Same date and model service as the baseline, not controlled beyond that.
- Labels are one Sonnet 5.5 pass per pull request, checked against the head code; borderline
  calls are explained in each `prs/` file.
