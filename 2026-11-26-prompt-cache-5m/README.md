# Prompt-cache check (2026-11-26): does a 5-minute cache bring Wachiman on a subscription token back to the key's depth?

- **Question:** the [credential probe](../2026-11-26-credential-probe/README.md) found that a plain
  `claude -p` call on a Claude subscription token makes fewer turns at Wachiman's $0.75 batch cap
  because Claude Code writes the prompt cache for 1 hour there, and that forcing 5 minutes brings
  the turns back. Does the same hold for Wachiman itself?
- **Change under test:** Wachiman v1.21.0 plus one key in the adapter's settings file,
  `"promptCacheTtl": "5m"` ([niway-dev/wachiman#324](https://github.com/niway-dev/wachiman/pull/324)),
  pinned by SHA `8a9a6d7` in [`replay/wachi-workflow-cache-5m.yml`](../replay/wachi-workflow-cache-5m.yml).
- **Runs:** W34–W36, kaipu-record #465 and #467, three runs each, in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3) (bench #86–#91),
  `CLAUDE_CODE_OAUTH_TOKEN` only (no API key passed), Claude Opus 5.5, effort `high`,
  `budget_usd: 10`, verify off, the same inputs as W13–W15. Raw reviews in [`raw/`](raw/), labels in
  [`prs/`](prs/). The set was first published as W31–W33 and renamed W34–W36 because the
  [Sonnet baseline](../2026-11-26-v1.21.0-sonnet-baseline/README.md) uses those labels.

## Result

**The 5-minute cache took effect on every call and raised the turns per batch call by 2 to 3, to
between the old token runs and the key. The known bugs found did not rise.**

| #465 and #467, 3 runs each | v1.21.0, token, 1-hour cache (W13–W15) | v1.15.0, token, 1-hour cache (W25–W27) | **v1.21.0 + 5m, token (W34–W36)** | v1.15.0, key (W28–W30) |
| --- | --- | --- | --- | --- |
| Cache write price per MTok (lifetime) | $8 (1 hour) | $8 (1 hour) | **$5 (5 minutes)** | $5 (5 minutes) |
| Batches at once | 4 | 1 | 4 | 1 |
| Turns per batch call, #465 | 8.5 | 9.3 | **11.5** | 14.3 |
| Turns per batch call, #467 | 10.3 | 9.7 | **12.9** | 15.2 |
| Findings posted, #465 | 11 | 9 | **13** | 15 |
| Findings posted, #467 | 22 | 25 | **26** | 32 |
| Known bugs, #465 (of 9) | 8 | 4 | **7** | 6 |
| Known bugs, #467 (of 30) | 10, plus 2 in part | 10, plus 4 | **8, plus 4** | 12, plus 4 |
| Distinct known bugs, #467 (of 10) | 6 | 6 | **3** | 6 |
| #467 cost per review | $2.94–$3.03 | $2.86–$2.91 | **$2.45–$2.68** | $2.81–$3.20 |

- **The cache lifetime is confirmed by price, not by a `cache_creation` record.** Wachiman's run log
  keeps only the total cache write (`cache_write_tokens` in each `wachiman-cost` line), not
  `usage.cache_creation`. The probe's 12 `result` records, which do hold `ephemeral_5m` and
  `ephemeral_1h`, fit Claude Code's cost exactly (largest error 0.002%) at $20 per MTok output,
  $0.20 cache read, **$5 per 5-minute write and $8 per 1-hour write**. Solving each batch call's
  cost for its write price gives $5.00 on all 24 calls of W34–W36, $8.00 on all 48 of W13–W15 and
  W25–W27, and $5.00 on all 24 of W28–W30. Every W34–W36 line says `auth: "oauth-token"`.
- **Turns rose but stayed below the key.** #465 went from 8.5 (same release, 1-hour) to 11.5, #467
  from 10.3 to 12.9; the key made 14.3 and 15.2 on v1.15.0. The probe saw the same shape on a plain
  call (10–12, then 13–14, against 15–17).
- **Known bugs did not follow.** On #465 the set found 7 of 9 (W13–W15: 8). On #467 it found 8 plus
  4 in part of 30 (W13–W15: 10 plus 2) and only 3 distinct of 10, the lowest of these sets: E7, E8
  and E9 in every run, E6 in part in every run, nothing of E1–E5. Three runs per set put a
  difference of one or two bugs inside the spread, so this is not a measured loss, but it is not
  the gain the turns suggested either.
- **Cheaper per review.** #467 cost $2.45–$2.68 (API-price estimate) against $2.94–$3.03 on the same
  release with the 1-hour cache, because each write is priced lower.

## What it means

- **Measured:** the setting reaches Claude Code on the token, every call writes the 5-minute cache,
  each batch call makes more turns, and the review costs less.
- **Not shown:** that the extra turns find more known bugs. On #467 the set found fewer distinct
  ones than any earlier set. Whether that is spread or a real effect of the 4-batch engine needs
  more runs; the key has not been run on v1.21.0, so the cleanest "full depth" reference for this
  release does not exist yet.

## Limits

- **Two pull requests, three runs each.** Enough to see turns move by 2 to 3 per call with little
  overlap, not to rank sets by known bugs.
- **Different engines across columns.** W25–W30 are v1.15.0 with one batch at a time; W13–W15 and
  W34–W36 are v1.21.0 with four at once. W13–W15 is the like-for-like baseline.
- **One labeller, one pass, not blind.** Claude Sonnet 5.5 (effort high) applied the
  [release bisect](../2026-11-26-release-bisect/prs/)'s rows and rules; its judgement calls are in
  each doc. E10 on W36 (partial) would make #467 9 plus 3 and 4 distinct if counted as found.
- **Not in `dataset/` yet.** These runs are not added to `runs.csv` or `labelled-runs.csv`.
