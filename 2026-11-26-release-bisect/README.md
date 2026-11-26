# Benchmark 2026-11-26: which release made the batches stop earlier

- **Question:** v1.20.1 and v1.21.0 make about 8 to 10 turns per batch call, against about 14 on
  v1.4.0, with the same model, effort, turn limit and batch cap
  ([results](../results.md#replay-of-v1201-and-v1210-against-v140-2026-11-25-kaipu-record-five-prs)).
  They also post fewer findings. Which release did that?
- **Method:** run releases in between on the two pull requests where v1.21.0 and v1.4.0 differ most,
  kaipu-record #465 (14 files, 2 batches) and #467 (47 files, 6 batches), three runs each. Then
  run the release where the turns dropped again with the other credential.
- **Runs:** W19–W21 = v1.5.0, bench #62–#67; W22–W24 = v1.9.0, bench #68–#73; W25–W27 =
  v1.15.0 on a subscription token, bench #74–#79; W28–W30 = v1.15.0 on an API key, bench
  #80–#85, in [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on
  2026-11-26.
- **Per-PR analysis:** [`prs/`](prs/). Raw reviews and comments: [`raw/`](raw/). Rows: `run_label`
  W19–W30 in `dataset/`.

## Result

**No release up to v1.15.0 cut the turns. The credential did.** The same v1.15.0, at the same SHA with the same
inputs, makes about 15 turns per batch call on an API key and about 9 on a Claude subscription
token. Every set at about 15 turns ran on an API key, and every set at about 9 on the token.

| #465 and #467, 3 runs each | v1.4.0, Nov 2 (W4–W6) | v1.4.0, Nov 25 (W16–W18) | v1.5.0 (W19–W21) | v1.9.0 (W22–W24) | **v1.15.0, key (W28–W30)** | **v1.15.0, token (W25–W27)** | v1.20.1 (W7–W9) | v1.21.0, $10 (W13–W15) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Credential | API key | API key | API key | API key | **API key** | **subscription token** | subscription token | subscription token |
| Batches at once | 1 | 1 | 1 | 1 | 1 | 1 | 4 | 4 |
| Turns per batch call, #465 | 14.7 | 13.7 | 14.2 | 15.8 | **14.3** | **9.3** | 7.7 | 8.5 |
| Turns per batch call, #467 | 14.6 | 15.1 | 15.8 | 14.9 | **15.2** | **9.7** | 7.0 | 10.3 |
| Review time, #467 | not recorded | 361–384 s | 393–423 s | 353–401 s | 349–437 s | 268–302 s | 266–287 s | 270–280 s |
| Findings posted, #465 | 12 | 10 | 15 | 11 | 15 | 9 | 10 | 11 |
| Findings posted, #467 | 28 | 34 | 39 | 27 | 32 | 25 | 17 | 22 |
| Known bugs, #465 (of 9) | 7 | 5 | 7 | 6 | 6 | 4 | 6 | 8 |
| Known bugs, #467 (of 30) | 11, plus 2 in part | 12, plus 3 | 14, plus 3 | 11, plus 4 | 12, plus 4 | 10, plus 4 | 7, plus 1 | 10, plus 2 |
| Distinct known bugs, #467 (of 10) | 6 | 5 | 7 | 5 | 6 | 6 | 4 | 6 |
| Reviews left partial | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| #467 cost per review | $2.82–$2.98 | $2.81–$2.91 | $2.82–$3.10 | $2.78–$3.07 | $2.81–$3.20 | $2.86–$2.91 | $2.75–$3.15 | $2.94–$3.03 |

- **The engine is cleared from v1.9.0 to v1.15.0.** On the key, v1.15.0's turns and known bugs
  sit inside the range of v1.4.0, v1.5.0 and v1.9.0, and its review time is close to it (349–437 s
  on #467, against 353–423 s). Parallel batches (v1.16.0) were
  already cleared: v1.15.0 on the token is low while reviewing one batch at a time.
- **On the token, a call stops earlier; each turn is the same.** From the v1.15.0 run logs
  (`wachiman-cost` lines, 2 and 6 batch calls per review):

  | v1.15.0 batch calls | Turns per call | Output tokens per call | Output tokens per turn | Seconds per turn |
  | --- | --- | --- | --- | --- |
  | API key, #465 / #467 | 14.3 / 15.2 | 9,195 / 7,034 | 642 / 462 | 6.0 / 4.2 |
  | Subscription token, #465 / #467 | 9.3 / 9.7 | 5,432 / 4,686 | 582 / 482 | 5.8 / 4.9 |

  The model does about as much per turn and ends the call about 5 turns sooner, so it reads less
  and writes less per batch: 41% less output on #465, 33% less on #467.
- **Where the difference comes from is not measured here.** The engine passes the token to Claude
  Code in place of the key and changes nothing else in a batch (`buildChildEnv` and
  `resolveClaudeAuth` in `src/providers/claude-code.ts`); it only changes the footer, which calls
  the cost an estimate. Claude Code is the same version (2.1.304) in every set. So the change is
  in what Claude Code or the service does with a subscription token: a request setting, a
  default, or the model's behaviour on that path. Comparing the requests Claude Code sends on
  each credential, for the same batch, would say which.
- **Cost does not show it.** Every set spends about $3 on #467. On the token the figure is Claude
  Code's API-price estimate, not a bill, and it stays at about $3 although the calls write less.
- **Fewer bugs on the token, within the spread.** v1.15.0 found 6 of 9 and 12 of 30 (plus 4 in
  part) on the key, against 4 of 9 and 10 of 30 (plus 4) on the token. Three runs per set cannot
  separate that from the spread between runs, but it points the same way as the turns.
- **New findings:** across both PRs, the v1.5.0 runs posted 8 that matched no known or
  earlier bug (#465 N7 and #467 N23–N29: 5 valid, 3 partly valid). The v1.9.0 runs posted 2 more
  (#465 N8 and #467 N30, both valid) and re-posted v1.5.0's #467 N24. The v1.15.0 token runs
  posted 3 more on #467 (N31 and N33 valid, N32 partly valid) and re-posted N24. The v1.15.0 key
  runs posted 2 more (#465 N9 and #467 N34, both valid) and re-posted N23, N24, N26 and N28.
  Verdicts are in the per-PR docs.

## What this changes

- **The v1.21.0 against v1.4.0 comparison mixed credentials.** v1.4.0 ran on the key and v1.21.0
  on the token, so its turns gap and part of its gap in findings most likely measure the
  credential, not the release (v1.21.0 was not run on the key) ([results](../results.md#replay-of-v1201-and-v1210-against-v140-2026-11-25-kaipu-record-five-prs)).
- **A benchmark compares releases on one credential.** The report names it.
- **The next question is about Claude Code, not Wachiman's engine:** why a batch call on a
  subscription token ends after about 9 turns where the same call on a key takes about 15.

## Conditions

| Condition | W19–W21 (v1.5.0) | W22–W24 (v1.9.0) | W25–W27 (v1.15.0, token) | W28–W30 (v1.15.0, key) |
| --- | --- | --- | --- | --- |
| Pull requests | kaipu-record #465 and #467 at the manifest heads, [`replay/manifest-2026-11-26-bisect.tsv`](../replay/manifest-2026-11-26-bisect.tsv) | same | same | same |
| Base commit | manifest base (`BENCH_FOCUS=as-is`) | same | manifest base plus the focus commit (`BENCH_FOCUS=rename`) | same as W25–W27 |
| Review focus file | `.github/agent-review.md`, read | same file, read (with a notice: v1.9.0 prefers `.github/wachiman.md`) | `.github/wachiman.md` (a copy of `.github/agent-review.md`), read | same as W25–W27 |
| Engine | v1.5.0 by SHA, `31f422b` | v1.9.0 by SHA, `b3f60be` | v1.15.0 by SHA, `6b99963` | same as W25–W27 |
| Caller | [`replay/wachi-workflow-v1.5.0.yml`](../replay/wachi-workflow-v1.5.0.yml): W4–W6's inputs (Opus 5.5, effort `high`) plus `budget_usd: 10` | [`replay/wachi-workflow-v1.9.0.yml`](../replay/wachi-workflow-v1.9.0.yml): the same inputs | [`replay/wachi-workflow-v1.15.0.yml`](../replay/wachi-workflow-v1.15.0.yml): the same inputs plus `verify: false` | [`replay/wachi-workflow-v1.15.0-api-key.yml`](../replay/wachi-workflow-v1.15.0-api-key.yml): the same inputs as W25–W27 |
| Batches | one at a time | one at a time | one at a time | one at a time |
| Credential | `ANTHROPIC_API_KEY`: billed. Neither release accepts a subscription token | same | `CLAUDE_CODE_OAUTH_TOKEN` only: the cost is an estimate | `ANTHROPIC_API_KEY` only: billed |
| Runs | 3 per PR, `/wachi review` | same | same | same |

Model, effort (`high`), turn limit (40) and batch cap ($0.75) are the same in every set of the table
above. Every review records the model and the effort (`reviews.csv`). One run log of W13–W15 and
one of W16–W18 were read to confirm the inputs the engine received. The turn limit and the batch cap
are the callers' defaults, which are 40 and $0.75 in v1.9.0's and v1.15.0's `review.yml` too.

## Method

- **Setup:** [`replay/bench.sh`](../replay/bench.sh) with `BENCH_BRANCH_PREFIX=replay-v150` (then
  `replay-v190`), `BENCH_FOCUS=as-is` and `BENCH_MANIFEST=replay/manifest-2026-11-26-bisect.tsv`:
  `push`, `open`, `rounds 2 3`, `collect`. v1.15.0 used `replay-v1150` (token) and `replay-v1150k`
  (key) with `BENCH_FOCUS=rename`, because v1.14.0 stopped reading `.github/agent-review.md`. Each
  workflow was put on the repository's `main` through the contents API (commits `c684024`,
  `74e01b8`, `7f34ca8` and `ce2c3e0`) before its round 1.
- **Credential:** read from each review footer: `Cost` on a key, `Cost (estimate)` on a token. Across
  the raw reviews of every report in this repository, the 51 that say `Cost (estimate)` are
  exactly W7–W15 and W25–W27; the other 93, W28–W30 included, say `Cost`.
- **Labels:** a Claude Sonnet 5.5 subagent per set matched each finding against the known-bug
  lists and extras of the [v1.4.0 re-run docs](../2026-11-25-v1.4.0-rerun/prs/), reading the head
  code. Judgement calls are in each doc. Counts come from `dataset/labelled-runs.csv`; turns from
  `run-logs.csv`, joined through `reviews.csv` `run_id`; tokens from the `wachiman-cost` lines of
  the run logs in `dataset/raw/`.

## Limits

- **Two pull requests, three runs each.** Enough to see a 15-against-9 gap in turns, not to rank
  sets by known bugs.
- **One release on both credentials.** The token was tested on v1.15.0, v1.20.1 and v1.21.0, the
  key on v1.15.0 and older. That v1.20.1 and v1.21.0 would also go back to about 15 turns on the
  key is expected from the result, not measured.
- **Labelled by other subagents than the earlier sets.** The docs share IDs and the "Label when
  found" rules, but a borderline "partial" can be called differently.
