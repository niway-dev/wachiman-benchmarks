# Benchmark 2026-11-26: which release made the batches stop earlier

- **Question:** v1.20.1 and v1.21.0 make about 8 to 10 turns per batch call, against about 14 on
  v1.4.0, with the same model, effort, turn limit and batch cap
  ([results](../results.md#replay-of-v1201-and-v1210-against-v140-2026-11-25-kaipu-record-five-prs)).
  They also post fewer findings. Which release did that?
- **Method:** run releases in between on the two pull requests where v1.21.0 and v1.4.0 differ most,
  kaipu-record #465 (14 files, 2 batches) and #467 (47 files, 6 batches), three runs each.
- **Runs:** W19–W21 = v1.5.0, bench #62–#67; W22–W24 = v1.9.0, bench #68–#73; W25–W27 =
  v1.15.0, bench #74–#79, in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-26.
- **Per-PR analysis:** [`prs/`](prs/). Raw reviews and comments: [`raw/`](raw/). Rows: `run_label`
  W19–W27 in `dataset/`.

## Result

**v1.5.0 and v1.9.0 work like v1.4.0: about 15 turns per call. v1.15.0 is already down to about 9,
like v1.20.1 and v1.21.0. But the credential changes at the same place:** every set at about 15
turns ran on an API key, and every set at about 9 ran on a Claude subscription token. These runs
cannot tell the engine from the credential.

| #465 and #467, 3 runs each | v1.4.0, Nov 2 (W4–W6) | v1.4.0, Nov 25 (W16–W18) | **v1.5.0 (W19–W21)** | **v1.9.0 (W22–W24)** | **v1.15.0 (W25–W27)** | v1.20.1 (W7–W9) | v1.21.0, $10 (W13–W15) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Credential | API key | API key | API key | API key | subscription token | subscription token | subscription token |
| Batches at once | 1 | 1 | 1 | 1 | 1 | 4 | 4 |
| Turns per batch call, #465 | 14.7 | 13.7 | 14.2 | 15.8 | 9.3 | 7.7 | 8.5 |
| Turns per batch call, #467 | 14.6 | 15.1 | 15.8 | 14.9 | 9.7 | 7.0 | 10.3 |
| Review time, #467 | not recorded | 361–384 s | 393–423 s | 353–401 s | 268–302 s | 266–287 s | 270–280 s |
| Findings posted, #465 | 12 | 10 | 15 | 11 | 9 | 10 | 11 |
| Findings posted, #467 | 28 | 34 | 39 | 27 | 25 | 17 | 22 |
| Known bugs, #465 (of 9) | 7 | 5 | 7 | 6 | 4 | 6 | 8 |
| Known bugs, #467 (of 30) | 11, plus 2 in part | 12, plus 3 | 14, plus 3 | 11, plus 4 | 10, plus 4 | 7, plus 1 | 10, plus 2 |
| Distinct known bugs, #467 (of 10) | 6 | 5 | 7 | 5 | 6 | 4 | 6 |
| Reviews left partial | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| #467 cost per review | $2.82–$2.98 | $2.81–$2.91 | $2.82–$3.10 | $2.78–$3.07 | $2.86–$2.91 | $2.75–$3.15 | $2.94–$3.03 |

- **Parallel batches are not the cause.** v1.15.0 reviews one batch at a time, like v1.4.0, and
  still makes about 9 turns per call.
- **The credential is the other suspect.** The engine passes the token to Claude Code in place of
  the key and changes nothing else in a batch (`buildChildEnv` and `resolveClaudeAuth` in
  `src/providers/claude-code.ts`); it does change the footer, which says the cost is an estimate.
  Review time follows the credential too: about 380 s for #467 on the key, about 280 s on the
  token, whether the batches run one at a time (v1.15.0) or four at once (v1.20.1). Why a
  subscription call would take fewer turns is not measured here.
- **Cost does not move with the turns.** Every set spends about $3 on #467. On the token the
  figure is Claude Code's API-price estimate, not a bill.
- **v1.15.0 caught fewer known bugs on #465** (4 of 9, the lowest of any set) and as many as
  v1.9.0 on #467. Three runs per set cannot separate that from the spread between runs.
- **New findings:** across both PRs, the v1.5.0 runs posted 8 that matched no known or
  earlier bug (#465 N7 and #467 N23–N29: 5 valid, 3 partly valid). The v1.9.0 runs posted 2 more
  (#465 N8 and #467 N30, both valid) and re-posted v1.5.0's #467 N24. The v1.15.0 runs posted 3
  more on #467 (N31 and N33 valid, N32 partly valid) and re-posted N24. Verdicts are in the
  per-PR docs.

## Where to look next

**Next run: v1.15.0 again, on the API key only.** Same SHA and inputs, without the token secret.
If its turns go back to about 15, the credential explains the drop, and the engine releases
between v1.9.0 and v1.15.0 are cleared. If they stay near 9, the cause is in those releases, and
the engine commits that change the batch prompt are the place to look:

| Release | Change |
| --- | --- |
| v1.10.0 | The verifier is on by default. The bench callers set `verify: false` from v1.15.0 on, so it is not a cause in these runs |
| v1.13.0 | Fidelity: a claims call, and claims assigned to each batch, which changes the batch prompt |

v1.16.0 (four batches at once) and v1.17.0 (inline findings as a table, rules read from the base
commit) are cleared by v1.15.0's turns. The focus file is not the cause: v1.20.1 ran without it
and v1.15.0 and v1.21.0 with it, and all three are low.

## Conditions

| Condition | W19–W21 (v1.5.0) | W22–W24 (v1.9.0) | W25–W27 (v1.15.0) |
| --- | --- | --- | --- |
| Pull requests | kaipu-record #465 and #467 at the manifest heads, [`replay/manifest-2026-11-26-bisect.tsv`](../replay/manifest-2026-11-26-bisect.tsv) | same | same |
| Base commit | manifest base (`BENCH_FOCUS=as-is`) | same | manifest base plus the focus commit (`BENCH_FOCUS=rename`) |
| Review focus file | `.github/agent-review.md`, read | same file, read (with a notice: v1.9.0 prefers `.github/wachiman.md`) | `.github/wachiman.md` (a copy of `.github/agent-review.md`), read |
| Engine | v1.5.0 by SHA, `31f422b` | v1.9.0 by SHA, `b3f60be` | v1.15.0 by SHA, `6b99963` |
| Caller | [`replay/wachi-workflow-v1.5.0.yml`](../replay/wachi-workflow-v1.5.0.yml): W4–W6's inputs (Opus 5.5, effort `high`) plus `budget_usd: 10` | [`replay/wachi-workflow-v1.9.0.yml`](../replay/wachi-workflow-v1.9.0.yml): the same inputs | [`replay/wachi-workflow-v1.15.0.yml`](../replay/wachi-workflow-v1.15.0.yml): the same inputs plus `verify: false` |
| Batches | one at a time | one at a time | one at a time |
| Credential | `ANTHROPIC_API_KEY`: billed. Neither release accepts a subscription token | same | `CLAUDE_CODE_OAUTH_TOKEN` only: the cost is an estimate |
| Runs | 3 per PR, `/wachi review` | same | same |

Model, effort (`high`), turn limit (40) and batch cap ($0.75) are the same in every set of the table
above: every review records them (`reviews.csv`), and one run log of W13–W15 and one of W16–W18
were read to confirm the inputs the engine received.

## Method

- **Setup:** [`replay/bench.sh`](../replay/bench.sh) with `BENCH_BRANCH_PREFIX=replay-v150` (then
  `replay-v190`), `BENCH_FOCUS=as-is` and `BENCH_MANIFEST=replay/manifest-2026-11-26-bisect.tsv`:
  `push`, `open`, `rounds 2 3`, `collect`. v1.15.0 used `replay-v1150` and `BENCH_FOCUS=rename`,
  because v1.14.0 stopped reading `.github/agent-review.md`. Each workflow was put on the
  repository's `main` through the contents API (commits `c684024`, `74e01b8` and `7f34ca8`) before
  its round 1.
- **Labels:** a Claude Sonnet 5.5 subagent per release matched each finding against the known-bug
  lists and extras of the [v1.4.0 re-run docs](../2026-11-25-v1.4.0-rerun/prs/), reading the head
  code. Judgement calls are in each doc. Counts come from `dataset/labelled-runs.csv`; turns from
  `run-logs.csv`, joined through `reviews.csv` `run_id`.

## Limits

- **Two pull requests, three runs each.** Enough to see a 15-against-8 gap in turns, not to rank
  releases by known bugs.
- **The credential and the engine change together.** Every API-key set is v1.9.0 or older and
  every token set is v1.15.0 or newer, so these runs leave both explanations open.
- **Labelled by other subagents than the earlier sets.** The docs share IDs and the "Label when
  found" rules, but a borderline "partial" can be called differently.
