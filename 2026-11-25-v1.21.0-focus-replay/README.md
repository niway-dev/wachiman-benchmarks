# Benchmark 2026-11-25: Wachiman v1.21.0 with the review focus file

- **Question:** v1.20.1 found fewer known bugs than v1.4.0 on the same five pull requests
  ([report](../2026-11-25-v1.20.1-replay/README.md)). It also reviewed them without kaipu-record's
  review focus file, which v1.4.0 had. Does the missing file explain the gap?
- **Runs:** W10 = #17–#21, W11 = #22–#26, W12 = #27–#31 in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-25.
- **Compared with:** [W4–W6](../2026-11-02/README.md) (v1.4.0) and
  [W7–W9](../2026-11-25-v1.20.1-replay/README.md) (v1.20.1).
- **Per-PR analysis:** [`prs/`](prs/). Raw reviews and comments: [`raw/`](raw/). Rows: `run_label`
  W10–W12 in `dataset/`.

## Result

**No. With the focus file restored, v1.21.0 catches 27 of 81 known-bug chances, against 30 for
v1.20.1 without it and 35 for v1.4.0. Most of the gap is in one pull request, #467, the biggest,
where the newer engines leave files unreviewed.** On the four smaller pull requests the three
versions catch about as many: 24, 23 and 23 of 51 chances. There, though, the catches spread over
fewer distinct bugs (13, 12 and 10): #463 E1 and #464 E1, which v1.20.1 caught, no v1.21.0 run
did.

The focus file was a real difference between the runs, and it is now fixed in kaipu-record
([kaipu-record#728](https://github.com/niway-dev/kaipu-record/pull/728)), but it is not what made
the newer engine find less: restoring it did not bring the catches back. On #467 it may even have
cost some, by leaving less budget for the last batches (see below).

| Per review (15 reviews each) | v1.4.0 (W4–W6) | v1.20.1 (W7–W9) | v1.21.0 + focus file (W10–W12) |
| --- | --- | --- | --- |
| Focus file read | yes (`.github/agent-review.md`) | **no** | yes (`.github/wachiman.md`) |
| Median cost | $1.00 | $1.09 | $1.12 |
| Total, 15 reviews | $20.87 | $21.45 | $22.04 |
| Median model time (sum of batch calls) | 158 s | 138 s | 119 s |
| Median wall time of the Actions run | not measured | 97 s | 86 s |
| Findings posted | 80 | 61 | 65 |
| Turns per batch call | 13.7 | 8.2 | 8.5 |
| Known bugs caught (of 81: 27 bugs × 3 runs) | 35, plus 4 in part | 30, plus 2 in part | 27, plus 3 in part |
| … on #463–#466 (of 51) | 24, plus 2 in part | 23, plus 1 in part | 23 |
| … on #467 (of 30) | 11, plus 2 in part | 7, plus 1 in part | 4, plus 3 in part |
| Per run | W4 12, W5 11, W6 12 | W7 10, W8 9, W9 11 | W10 9, W11 8, W12 10 |
| Distinct known bugs caught by any run (of 27) | 19 | 16 | 13 |
| Cost per known bug caught | $0.60 | $0.71 | $0.82 |
| #467 reviews left partial | 0 of 3 | 2 of 3 (8 and 11 of 47 files unread) | 3 of 3 (19, 19 and 11 of 47 files unread) |

Known bugs caught by at least one of the three runs:

| PR | v1.4.0 | v1.20.1 | v1.21.0 + focus file |
| --- | --- | --- | --- |
| #463 | E1 E2 E3 E4 E6 | E1 E2 E4 | E2 E4 |
| #464 | E1 E2 E3 | E1 E2 E3 | E2 E3 |
| #465 | E1 E2 E3 | E1 E2 E3 | E1 E2 E3 |
| #466 | E1 E3 | E1 E2 E3 | E1 E2 E3 |
| #467 | E3 E6 E7 E8 E9 E10 | E6 E7 E9 E10 | E2 E7 E10 |

## What the gap comes from

- **#467, the 47-file pull request: files left unreviewed, from the budget.** Since v1.16.0 the
  engine runs up to 4 batches at once, and each running batch reserves its full cap ($0.75) from
  the review's budget before it starts. The batches started last get little or none, end on
  `budget`, and leave their files unread. v1.4.0 ran batches one after another, charged each its
  real cost, and read all 47 files in every run. Here every v1.21.0 run of #467 was partial: E9's
  file (`library-page.module.css`) went unread in all three, and E7's (`sidebar.test.tsx`) in two.
  That is where the known bugs were lost.
- **More files went unread with the focus file than without it:** 19, 19 and 11, against 8, 11 and
  none. Why is not established. The focus file adds about 1.5 KB to every batch prompt, which makes
  each batch cost a little more and leaves less for the last ones; run-to-run variation is the other
  candidate (W12 and W8 both left 11). Either way, the cause underneath is the budget reservation.
- **The four smaller pull requests: about the same count, fewer distinct bugs.** Every batch there
  ended on `success`, so the budget did not cut them. The newer engine takes fewer turns per call
  (8.5 against 13.7) and posts fewer findings, and catches nearly as many (23 against 24 of 51),
  but repeats the same bugs more across runs: 10 distinct against 13. Three runs cannot say whether
  that is a loss or variation. Why it takes fewer turns is not identified. One candidate
  is the risk paragraph that v1.12.0 adds to every batch prompt; it is untested.
- **Not the cause:** the optional settings. `verify`, `pr_confidence` and `memory_proposals` are off
  in every run here. The review rules and flow questions in the prompt, the tools, `max_turns` and
  the per-batch cap are the same as in v1.4.0.

## Conditions

Everything below is the same in the three sets of runs unless the row says otherwise.

| Condition | v1.4.0 (W4–W6) | v1.20.1 (W7–W9) | v1.21.0 (W10–W12) |
| --- | --- | --- | --- |
| Pull requests | kaipu-record #463–#467 from [`replay/manifest-2026-10-31.tsv`](../replay/manifest-2026-10-31.tsv) | same | same |
| Head commits, and so the reviewed diff | manifest heads | same | same; the diff is byte-identical (#467: 47 files, +2676 −2177 in each) |
| Base commit of the pull request | manifest base | manifest base | manifest base plus one commit that copies `.github/agent-review.md` to `.github/wachiman.md` (`6e7521b` for #463, `3feb5b1` for the others) |
| Review focus file the engine read | `.github/agent-review.md` | none: v1.14.0 dropped that name | `.github/wachiman.md`, same content (20 lines) |
| `CLAUDE.md` | read | read | read |
| Engine | v1.4.0 | v1.20.1, `793a64d` | v1.21.0, `621aa39`. v1.21.0 differs from v1.20.1 only in telemetry settings (its changelog) |
| Model, effort, verify | Claude Opus 5.5, `high`, off | same | same |
| Budgets | engine defaults (not set in the workflow) | same | same |
| Batches | one at a time | up to 4 at once | up to 4 at once |
| Credential | API key: billed cost | Claude subscription token: API-equivalent estimate | same as v1.20.1 |
| Claude Code | 2.1.304 | 2.1.304 | 2.1.304 |
| Runs | 3 per PR, started with `/wachi review` | same | same |

## Method

- **Setup:** [`replay/bench.sh`](../replay/bench.sh) with `BENCH_BRANCH_PREFIX=replay-focus` and
  `BENCH_FOCUS=rename`: `push`, `open`, `rounds 2 3`, `collect`. The prefix keeps these branches
  apart from W7–W9's in the same repository. The rename mode builds the extra base commit with a
  fixed author and date, so it is reproducible, and the round-1 pull request body names it. `main`'s
  workflow was updated to the v1.21.0 pin through the contents API before round 1 (`push` does not
  touch `main`). The
  [replay README](../replay/README.md#review-focus-file) explains the modes. Without a mode,
  `bench.sh` now stops when a base has the focus file only under a name Wachiman ignores, so a run
  cannot lose it silently again.
- **Checking the focus file was read:** the engine reads its focus file from the pull request's
  base commit (`instructionsFrom` in v1.21.0's `src/engine.ts`). Each of the 15 pull requests has
  the focus commit as its `base.sha`, and that commit has `.github/wachiman.md`. The run log does
  not list the files it read, so this is checked from the code and the commits, not from the log.
- **Labels:** a Claude Sonnet 5.5 subagent matched each finding to the known-bug list (E1…) and the
  earlier extras (A1…, N1…), reading the head code in a kaipu-record clone, as for W7–W9. Its
  judgement calls are listed in each doc. It checked each Expected row's cells against its "Label
  when found" column. The bug counts above come from those doc cells (`dataset/labelled-runs.csv`).
- **Joining findings to labels:** `scripts/labels.ts` joined 51 of the 65 findings to a doc row.
  The other 14 scored below its threshold and are in `dataset/ambiguous.md`. They change
  `labels.csv`, not the bug counts.

## Limits

- **Three runs per version is a small sample.** The small pull requests' 24, 23 and 23 are the
  same within run-to-run variation; their distinct bugs (13, 12, 10) may not be. #467's 11, 7 and 4 follow the number of files left unread,
  which is the signal worth acting on.
- **The known-bug list was built from earlier versions' runs.** A bug only a newer version sees
  counts as "new", not "known", so this table cannot reward it. 8 findings were new here.
- **The cost is an estimate:** subscription token, API prices, no bill. The stop rule (stop after
  round 1 if its median review cost more than $2.00) did not trip: round 1's median was $1.12.
