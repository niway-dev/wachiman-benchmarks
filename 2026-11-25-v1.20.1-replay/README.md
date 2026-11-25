# Benchmark 2026-11-25: Wachiman v1.20.1 on the v1.4.0 replay

- **Question:** what today's release costs, how long it takes and what it finds, on the same five
  pull requests that measured v1.4.0. Everything in [`dataset/`](../dataset/) before this run was
  v1.4.0 or older.
- **Runs:** W7 = #2–#6, W8 = #7–#11, W9 = #12–#16 in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3), on 2026-11-25.
- **Compared with:** [W4–W6](../2026-11-02/README.md), Wachiman v1.4.0, 2026-11-02.
- **Per-PR analysis:** [`prs/`](prs/). Raw reviews and comments: [`raw/`](raw/). Rows:
  `run_label` W7–W9 in `dataset/runs.csv`, `reviews.csv`, `run-logs.csv`, `findings.csv`,
  `labels.csv` and `labelled-runs.csv`.

## Result

**v1.20.1 costs about the same per review as v1.4.0, runs faster, and posts fewer findings. It
catches slightly fewer known bugs: 30 of 81 chances against 35.** So each known bug caught costs
more: $0.71 against $0.60. The gap is under two known bugs per run (W4–W6: 11–12 per run, W7–W9:
9–11). Three runs per version cannot tell a small regression from run-to-run variation. These runs did
not read the repository's review focus file (see Method); the
[follow-up run with it](../2026-11-25-v1.21.0-focus-replay/README.md) found no more.

| Per review (15 reviews each) | v1.4.0 (W4–W6) | v1.20.1 (W7–W9) |
| --- | --- | --- |
| Median cost | $1.00 | $1.09 |
| Cost range | $0.82–$2.98 | $0.90–$3.15 |
| Total, 15 reviews | $20.87 | $21.45 |
| Median model time (sum of batch calls) | 158 s | 138 s |
| Longest model time | 413 s | 287 s |
| Median wall time of the Actions run | not measured | 97 s |
| Findings posted | 80 (5.3 per review) | 61 (4.1 per review) |
| Cost per finding | $0.26 | $0.35 |
| Known bugs caught (of 81: 27 bugs × 3 runs) | 35, plus 4 in part | 30, plus 2 in part |
| Per run | W4 12, W5 11, W6 12 | W7 10, W8 9, W9 11 |
| Distinct known bugs caught by any of the 3 runs (of 27) | 19 | 16 |
| Cost per known bug caught | $0.60 | $0.71 |
| Partial reviews | 0 | 2 (#6: 8 of 47 files left, #11: 11) |

What the matched findings were (`labels.csv`, `label_kind`): v1.4.0 34 expected, 17 additional,
16 new. v1.20.1 33 expected, 11 additional, 16 new. The new v1.20.1 findings cover 16 distinct
defects. The analyst judged 14 valid, 1 partly valid and 1 unverified; none invalid
([`prs/`](prs/), "New findings").

## Where they differ

Known bugs caught by at least one of the three runs:

| PR | v1.4.0 (W4–W6) | v1.20.1 (W7–W9) |
| --- | --- | --- |
| #463 | E1 E2 E3 E4 E6 | E1 E2 E4 |
| #464 | E1 E2 E3 | E1 E2 E3 |
| #465 | E1 E2 E3 | E1 E2 E3 |
| #466 | E1 E3 | E1 E2 E3 |
| #467 | E3 E6 E7 E8 E9 E10 | E6 E7 E9 E10 |

- **Lost:** #463 E6 (a queued camera turn-on with no off check, High) and E3. #467 E3 and E8. No
  v1.20.1 run posted them.
- **Gained:** #466 E2, which all three v1.20.1 runs caught.
- **#467 is the biggest pull request.** v1.20.1 splits it into 6 batches. In two of the three runs,
  batches ran out of budget and left 8 and 11 files unreviewed. The known bugs missed there may sit
  in those files; the per-PR doc does not settle it.

## Method

Same setup as W4–W6, except for the engine version, the credential and the review focus file.

- **Review focus file: not read.** Every base commit has kaipu-record's review focus at
  `.github/agent-review.md`. v1.4.0 read it. v1.20.1 did not, because v1.14.0 stopped reading that
  name, so these runs were reviewed without the repository's rules. The
  [follow-up run](../2026-11-25-v1.21.0-focus-replay/README.md) restored the file on v1.21.0 and
  caught 27 known bugs, not more, so the missing file does not explain the gap above.

- **Pull requests:** the five pull requests in
  [`replay/manifest-2026-10-31.tsv`](../replay/manifest-2026-10-31.tsv) (kaipu-record #463–#467),
  at the same commits.
- **Runs:** three runs, started with `/wachi review` by
  [`replay/bench.sh`](../replay/bench.sh) (`create`, `open`, `rounds 2 3`, `collect`). To reproduce them with today's `bench.sh`, set `BENCH_FOCUS=as-is` (the default now stops on
  these bases) and use the workflow at the commit linked below.
- **Settings:** Claude Opus 5.5, effort `high`, `verify: false`, engine pinned to v1.20.1
  (`793a64d`) in [`replay/wachi-workflow.yml` as of these runs](https://github.com/niway-dev/wachiman-benchmarks/blob/55dea9c/replay/wachi-workflow.yml).
- **Credential:** the review ran on a Claude subscription token (`CLAUDE_CODE_OAUTH_TOKEN`), not an
  API key. **Every v1.20.1 cost here is the engine's API-equivalent estimate, not a bill.** It uses
  the same per-token computation the API runs of W4–W6 reported, so the two columns compare. Nothing
  was billed per token.
- **Durations:** "model time" is `log_duration_ms`, the sum of the batch calls' durations in the
  run log, the same measure as W4–W6. v1.20.1 runs its batches in parallel, so its Actions run ends
  sooner than that sum: 97 s median wall time, from run start to end. W4–W6 have no wall time in the
  dataset.
- **Labels:** each finding was matched to the known-bug list (E1…) and the baseline extras (A1…) of
  [the v1.4.0 analysis](../2026-11-02/prs/) by a Claude Sonnet 5.5 subagent. It read the head code
  in a kaipu-record clone, the same kind of check W4–W6 had. A consistency check between each row's
  cells and its "Label when found" column found one wrong cell (#463 E1, W8), which was fixed. The
  other judgement calls are listed in each doc. `scripts/labels.ts` then joined 60 of the 61
  findings to those rows. One, #464 W7 `en.json:1413` (the doc says A4), scored below the threshold
  and is in `dataset/ambiguous.md`.
- **Labelled, caught none:** every run × PR here has a row in `dataset/labelled-runs.csv`, including
  runs that caught nothing. See the dataset README.

## Limits

- **Three runs per version is a small sample.** Five known bugs over 81 chances is the whole gap; no
  significance test was run.
- **The known-bug list was built from earlier versions' runs and the authors' fixes.** A bug only
  v1.20.1 sees is counted as "new", not "known", so this table cannot reward it.
- **The cost is an estimate.** Nobody checked a bill. The stop rule set before spending (stop after
  round 1 if its median review cost more than $2.00, twice the W4–W6 median) did not trip: round 1's
  median was $1.08. Single reviews of #467 did cost more than $2.00 ($2.75–$3.15), as #467 did on
  v1.4.0 ($2.82–$2.98).
