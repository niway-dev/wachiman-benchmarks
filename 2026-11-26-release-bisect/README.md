# Benchmark 2026-11-26: which release made the batches stop earlier

- **Question:** v1.20.1 and v1.21.0 make about 8 to 10 turns per batch call, against about 14 on
  v1.4.0, with the same model, effort, turn limit and batch cap
  ([results](../results.md#replay-of-v1201-and-v1210-against-v140-2026-11-25-kaipu-record-five-prs)).
  They also post fewer findings. Which release did that?
- **Method:** run releases in between on the two pull requests where v1.21.0 and v1.4.0 differ most,
  kaipu-record #465 (14 files, 2 batches) and #467 (47 files, 6 batches), three runs each.
- **Runs:** W19–W21 = v1.5.0, bench #62–#67; W22–W24 = v1.9.0, bench #68–#73, in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-26.
- **Per-PR analysis:** [`prs/`](prs/). Raw reviews and comments: [`raw/`](raw/). Rows: `run_label`
  W19–W24 in `dataset/`.

## Result

**v1.5.0 and v1.9.0 work like v1.4.0: about 15 turns per call. The drop happened after v1.9.0 and
by v1.20.1.** Neither release lost known bugs against v1.4.0.

| #465 and #467, 3 runs each | v1.4.0, Nov 2 (W4–W6) | v1.4.0, Nov 25 (W16–W18) | **v1.5.0 (W19–W21)** | **v1.9.0 (W22–W24)** | v1.20.1 (W7–W9) | v1.21.0, $10 (W13–W15) |
| --- | --- | --- | --- | --- | --- | --- |
| Turns per batch call, #465 | 14.7 | 13.7 | 14.2 | 15.8 | 7.7 | 8.5 |
| Turns per batch call, #467 | 14.6 | 15.1 | 15.8 | 14.9 | 7.0 | 10.3 |
| Findings posted, #465 | 12 | 10 | 15 | 11 | 10 | 11 |
| Findings posted, #467 | 28 | 34 | 39 | 27 | 17 | 22 |
| Known bugs, #465 (of 9) | 7 | 5 | 7 | 6 | 6 | 8 |
| Known bugs, #467 (of 30) | 11, plus 2 in part | 12, plus 3 | 14, plus 3 | 11, plus 4 | 7, plus 1 | 10, plus 2 |
| Distinct known bugs, #467 (of 10) | 6 | 5 | 7 | 5 | 4 | 6 |
| Reviews left partial | 0 | 0 | 0 | 0 | 2 | 0 |
| #467 cost per review | $2.82–$2.98 | $2.81–$2.91 | $2.82–$3.10 | $2.78–$3.07 | $2.75–$3.15 | $2.94–$3.03 |

- **Cost does not move with the turns.** Every release spends about $3 on #467. v1.20.1 and v1.21.0
  spend it in fewer turns. Why is not measured here; one possibility is more context per turn.
- **v1.5.0 caught the most on #467** (14 of 30). Three runs per set cannot separate that from the
  9-to-14 spread between runs of one release, so it says "no loss", not "better".
- **New findings:** across both PRs, the v1.5.0 runs posted 8 that matched no known or
  earlier bug (#465 N7 and #467 N23–N29: 5 valid, 3 partly valid). The v1.9.0 runs posted 2 more
  (#465 N8 and #467 N30, both valid) and re-posted v1.5.0's #467 N24.
  Verdicts are in the per-PR docs.

## Where to look next

The engine commits between v1.9.0 and v1.20.1 that change how a batch works:

| Release | Change |
| --- | --- |
| v1.10.0 | The verifier is on by default. The bench callers set `verify: false` from v1.20.1 on, so it is not a cause in these runs |
| v1.13.0 | Fidelity: a claims call, and claims assigned to each batch, which changes the batch prompt |
| v1.16.0 | Up to 4 batches at once (`perf(engine): review up to 4 batches at once`) |
| v1.17.0 | Inline findings as a table, repository rules and dangerous paths read from the base commit |

The focus file is not the cause: v1.20.1 ran without it and v1.21.0 with it, and both are low.
**Next run: v1.15.0**, between v1.13.0 and v1.16.0. If its turns drop, the cause is in v1.10–v1.15
(v1.13.0 first). If they stay near 15, it is v1.16.0 or v1.17.0. It needs `verify: false` and
`BENCH_FOCUS=rename`, because v1.14.0 stopped reading `.github/agent-review.md`.

## Conditions

| Condition | W19–W21 (v1.5.0) | W22–W24 (v1.9.0) |
| --- | --- | --- |
| Pull requests | kaipu-record #465 and #467 at the manifest heads, [`replay/manifest-2026-11-26-bisect.tsv`](../replay/manifest-2026-11-26-bisect.tsv) | same |
| Base commit | manifest base (`BENCH_FOCUS=as-is`) | same |
| Review focus file | `.github/agent-review.md`, read | same file, read (with a notice: v1.9.0 prefers `.github/wachiman.md`) |
| Engine | v1.5.0 by SHA, `31f422b` | v1.9.0 by SHA, `b3f60be` |
| Caller | [`replay/wachi-workflow-v1.5.0.yml`](../replay/wachi-workflow-v1.5.0.yml): W4–W6's inputs (Opus 5.5, effort `high`) plus `budget_usd: 10` | [`replay/wachi-workflow-v1.9.0.yml`](../replay/wachi-workflow-v1.9.0.yml): the same inputs |
| Batches | one at a time | one at a time |
| Credential | `ANTHROPIC_API_KEY`: billed. Neither release accepts a subscription token | same |
| Runs | 3 per PR, `/wachi review` | same |

Model, effort (`high`), turn limit (40) and batch cap ($0.75) are the same in every set of the table
above: every review records them (`reviews.csv`), and one run log of W13–W15 and one of W16–W18
were read to confirm the inputs the engine received.

## Method

- **Setup:** [`replay/bench.sh`](../replay/bench.sh) with `BENCH_BRANCH_PREFIX=replay-v150` (then
  `replay-v190`), `BENCH_FOCUS=as-is` and `BENCH_MANIFEST=replay/manifest-2026-11-26-bisect.tsv`:
  `push`, `open`, `rounds 2 3`, `collect`. Each workflow was put on the repository's `main` through
  the contents API (commits `c684024` and `74e01b8`) before its round 1.
- **Labels:** a Claude Sonnet 5.5 subagent per release matched each finding against the known-bug
  lists and extras of the [v1.4.0 re-run docs](../2026-11-25-v1.4.0-rerun/prs/), reading the head
  code. Judgement calls are in each doc. Counts come from `dataset/labelled-runs.csv`; turns from
  `run-logs.csv`, joined through `reviews.csv` `run_id`.

## Limits

- **Two pull requests, three runs each.** Enough to see a 15-against-8 gap in turns, not to rank
  releases by known bugs.
- **Labelled by other subagents than the earlier sets.** The docs share IDs and the "Label when
  found" rules, but a borderline "partial" can be called differently.
