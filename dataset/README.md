# Review dataset: every Wachiman, Pullfrog and CodeRabbit review already posted on GitHub

One structured copy of the reviews the three tools posted on the benchmark replays and on
kaipu-record, so past results can be queried (`duckdb`, `jq`, a spreadsheet) instead of re-read as
markdown. Everything comes from the GitHub API through `gh`. No model ran to build it.

- **Built:** 2026-11-02. **Extended:** 2026-11-25 with `kaipu-bench-wachi-v3`: Wachiman v1.20.1, runs W7–W9
  ([report](../2026-11-25-v1.20.1-replay/README.md)), Wachiman v1.21.0 with the review focus file, runs W10–W12
  ([report](../2026-11-25-v1.21.0-focus-replay/README.md)), v1.21.0 with `budget_usd: 10`, runs W13–W15
  ([report](../2026-11-25-v1.21.0-budget-replay/README.md)), and v1.4.0 again, runs W16–W18
  ([report](../2026-11-25-v1.4.0-rerun/README.md)). **Extended again:** 2026-11-26 with the release bisect
  (W19–W30, bench #62–#85), the Sonnet 5.5 baseline of v1.21.0, runs W31–W33, bench #92–#106
  ([report](../2026-11-26-v1.21.0-sonnet-baseline/README.md)), and the 5-minute prompt-cache check, runs W34–W36,
  bench #86–#91 ([report](../2026-11-26-prompt-cache-5m/README.md)).
- **Scope:** the seven `niway-dev/kaipu-bench-*` repositories (all pull requests, any state) and every
  `niway-dev/kaipu-record` pull request that has a Wachiman review (112 of 467), which includes the
  field-run PRs #439 #449 #478 #479 #482 #483 #484.
- **Private repositories** that run Wachiman were read too. Their data is **not** in this
  repository; only counts are (see [Privacy](#privacy)).

## Files

| File | One row per | What it holds |
| --- | --- | --- |
| [`findings.csv`](findings.csv) / [`findings.jsonl`](findings.jsonl) | posted finding | tool, source repo, bench PR, original kaipu-record PR, round, run label, model, version, run id, review id, comment id, `placement` (`inline` or `body`), path, line, commit, severity, topic, confidence, the tool's own labels, title, replies, date, URL. The JSONL also has the comment `body`. |
| [`contracts.jsonl`](contracts.jsonl) | contract entry | The "What the change connects to" entries parsed from Wachiman review bodies. |
| [`reviews.csv`](reviews.csv) | Wachiman review | Model, effort, version, batches, cost from the review footer and from the log, finding and contract counts, the `Confidence rule` line of the log. |
| [`run-logs.csv`](run-logs.csv) | Actions run with a saved log | Workflow ref, version, model, effort, `credential`, calls, turns, cost and duration summed from the per-batch result lines. A run started by a comment is listed under the PR whose review it produced: replays of one original share a title, and comment runs are matched to PRs by title. |
| [`runs.csv`](runs.csv) | bench PR (bench repos) or bot review (kaipu-record) | **The run map for the owner to review.** Tool, model, version, `credential` (see [Credential](#credential)), round tag, the label the analysis docs use (W-R1, W4, S7, PF-v1, CR-v2…), original PR, date, `confidence`, `basis`. |
| [`labels.csv`](labels.csv) | finding that matched a verdict | The owner's verdict ID from the analysis docs (E/A/N/X/SN/NS for the replays, F for the field run), the verdict text, the match score and why. |
| [`labelled-runs.csv`](labelled-runs.csv) | run × replayed PR that an analysis doc labelled | The run's column in the doc's Expected issues table: how many known bugs (E) the doc lists, how many the run caught or caught in part, and their IDs. See [Labelled, caught none](#labelled-caught-none). |
| [`known-bugs.csv`](known-bugs.csv) | known bug (E row) per replayed PR | `original_pr,id,severity,title,doc`. The Expected issues rows (E1…En) of the primary per-PR doc for that PR: the newest doc whose Expected table has a Severity column. `severity` is High, Medium, Low or Info. `doc` is that doc's directory. The ids are the ones `labelled-runs.csv` lists in `expected_caught_ids` (except S7–S9 on #464, whose doc counts its A rows in the table). Written by `scripts/known-bugs.ts`; a severity that differs between docs is printed as a warning and the primary doc wins. |
| [`annotations.csv`](annotations.csv) | note, hand-written | `target_kind,target,text,link`. A short explanation a reader needs next to a number. `target_kind` is `version`, `variant`, `view`, `pr` or `bug`; `target` is the value it explains (for example `v1.3.0`, a variant such as `v1.21.0+cache-5m`, a PR number, or a bug as `<pr>:<id>`); `text` is the note; `link` is a path in this repository, with an optional `#anchor`. RFC 4180 quoting. Not generated: edit it by hand. |
| [`ambiguous.md`](ambiguous.md) | — | Findings in an analysed set that could not be matched with enough evidence, with their best candidates. |
| [`raw/`](raw) | pull request | The API snapshots: `pr.json`, `review-comments.json`, `reviews.json`, `issue-comments.json`, `runs.json`, `meta.json` and `logs/run-<id>.log.gz`. Per repository, `_index.json` and `_runs.json`. |
| `normalize-report.json` | — | Header lines that did not parse (none), counts seen per tool, and per-repository aggregates. |

### Columns of `findings.csv`

- `tool`: `wachiman`, `pullfrog` or `coderabbit`. Wachiman is recognised by its brand
  (`👮 **Wachiman** ·`) or, for engines before v1.3, by its bare label posted by `github-actions[bot]`.
- `severity`, `topic`, `confidence`: **Wachiman only**, from its exact header
  `👮 **Wachiman** · 🟠🐛 **Fix · bug: <title> (confidence medium)**`. Severity is
  `blocker|fix|consider|info`. Confidence is empty before v1.4.0.
- `native_severity`, `native_category`, `native_tags`: **the other tools' own words, kept raw**, with no
  mapping to Wachiman's scale. CodeRabbit: `Minor` / `Functional Correctness` / `Quick win`. Pullfrog posts
  no labels, so they are empty (a leading `Nit:` or `Correction:` is kept). The v1.0.x Wachiman posted
  `**Note (correctness): …**`; that is stored here as `Note` / `correctness`, with `severity` and `topic` empty.
- `placement`: `inline` is a review comment on a line. `body` is a finding that only lives in a review body:
  Wachiman's "Outside the diff" and "For your information" lists (and the "GitHub refused them inline" list),
  and CodeRabbit's "Outside diff range comments". `body_section` names the section.
- `original_pr`: the kaipu-record PR a replay copies, from the head ref `replay/pr-463/head-r4`; for
  kaipu-record rows, the PR itself. `round`: `r2`…`r9` from the title (`[replay]` is `r1`).
- `run_label`: from [`runs.csv`](runs.csv). `version`: from the run log (`Uses: …review.yml@refs/tags/v1.4.0`),
  else from the doc. `model`: from the log (`AGENT_REVIEW_MODEL`), else the review footer.
- `line` is the line on the head the comment was posted on; `original_line` is the line GitHub recorded when
  it was posted (they differ after a push). Whole-file findings have no line.
- A thread reply is not a finding. `replies` counts the replies in the finding's thread.

## Re-run

```sh
gh auth switch --hostname github.com --user csdev19

# 1. Snapshot. Idempotent: a PR whose updated_at did not change is skipped; --refresh forces a re-fetch.
bun scripts/fetch.ts --out dataset/raw --logs \
  --repos niway-dev/kaipu-bench-wachi,niway-dev/kaipu-bench-wachi-v2,niway-dev/kaipu-bench-wachi-v3,niway-dev/kaipu-bench-pullfrog,niway-dev/kaipu-bench-pullfrog-v2,niway-dev/kaipu-bench-coderabbit,niway-dev/kaipu-bench-coderabbit-v2
bun scripts/fetch.ts --out dataset/raw --logs --only-wachiman \
  --workflows "Agent review,Pullfrog" --repos niway-dev/kaipu-record \
  --keep niway-dev/kaipu-record#439,niway-dev/kaipu-record#449,niway-dev/kaipu-record#478,niway-dev/kaipu-record#479,niway-dev/kaipu-record#482,niway-dev/kaipu-record#483,niway-dev/kaipu-record#484

# 2. Tables, in this order (normalize reads runs.csv; labels reads findings.jsonl and runs.csv).
bun scripts/runs.ts      --raw dataset/raw --out dataset/runs.csv
bun scripts/normalize.ts --raw dataset/raw --out dataset
bun scripts/labels.ts    --dataset dataset
bun scripts/known-bugs.ts --dataset dataset   # reads the per-PR docs; writes known-bugs.csv

bun test scripts
```

`fetch.ts` waits out the GitHub rate limit by itself (the first full pass of kaipu-record spent it).
`labels.ts` reads the analysis docs (`<date>/prs/pr-<n>.md`) from the working tree. `--docs-ref <ref>`
reads them from a git ref instead.

## Row counts

### Public repositories

| Repository | PRs snapshotted | Wachiman | Pullfrog | CodeRabbit |
| --- | --- | --- | --- | --- |
| kaipu-bench-wachi | 60 | 282 (258 inline, 24 body) | — | — |
| kaipu-bench-wachi-v2 | 5 | 0 (see below) | — | — |
| kaipu-bench-wachi-v3 | 106 | 573 (551 inline, 22 body) | — | — |
| kaipu-bench-pullfrog | 5 | — | 7 | — |
| kaipu-bench-pullfrog-v2 | 6 | — | 9 | — |
| kaipu-bench-coderabbit | 10 | — | — | 15 |
| kaipu-bench-coderabbit-v2 | 6 | — | — | 6 |
| kaipu-record | 112 of 467 | 278 (266 inline, 12 body) | 34 | 27 (20 inline, 7 body) |
| **Total** | 310 | **1133** | **50** | **48** |

**1231 findings** in total. Also: **1357 contract entries**, **311 Wachiman reviews**,
**328 run logs** with parsed cost/model/version, **417 rows in `runs.csv`**.

Wachiman reviews by version: the 60 kaipu-bench-wachi reviews are v1.3.0 (15) and v1.4.0 (45); the 105
kaipu-bench-wachi-v3 reviews are v1.20.1 (15, bench #2–#16), v1.21.0 (45: #17–#31 at the default budget, #32–#46
with `budget_usd: 10`, #92–#106 on Sonnet 5.5), v1.4.0 (15, bench #47–#61), v1.5.0 (6, #62–#67), v1.9.0 (6, #68–#73),
v1.15.0 (12: #74–#79 on a subscription token, #80–#85 on an API key; all on #465 and #467 only) and
`v1.21.0+cache-5m` (6, #86–#91, on #465 and #467 only; see [Run map](#run-map)).
kaipu-record has 16 reviews on v1.4.0, 21 on v1.3.0, 70 on v1.2.x, 23 on the floating `v1` tag and 16 whose
version is unknown (no log).

### Verdict join

`labels.csv` has **769** rows. Of the 1231 findings, 314 are outside the analysed sets (see
[What is missing](#what-is-missing)), and 917 are in them: **769 matched, 148 are in
[`ambiguous.md`](ambiguous.md)**.

| `label_kind` | Rows |
| --- | --- |
| `expected` (E) | 381 |
| `additional` (A) | 167 |
| `new` (N, X, SN, NS, NF) | 129 |
| `field` (F) | 91 |
| `false-positive` | 1 (#466 N5 in the v1.21.0 analysis, marked invalid) |

### Private adoption repositories (counts only)

Wachiman is wired into these repositories. The data is in `~/Documents/Workspace/Personal/wachiman-data/`, outside
any git repository. Only the counts below are public. Findings are Wachiman's own; "Note" is the v1.0.x label with
no severity.

| Repository | PRs with a Wachiman review | Reviews | Findings | Findings by severity | Logs saved (expired) | Cost on the footers |
| --- | --- | --- | --- | --- | --- | --- |
| niway-dev/gymtrack-monorepo | 7 of 73 | 7 | 9 | note 9 | 7 | $0.19 |
| csdev19/csdev-monorepo | 4 of 42 | 4 | 4 | consider 3, fix 1 | 4 | $0.40 |
| csdev19/invisible-assistant | 62 of 309 | 66 | 56 | note 51, info 3, consider 1, fix 1 | 119 saved, 39 expired (all repos) | $1.24 |
| niway-dev/fidelity-card | 0 of 14 | 0 | 0 | — | — | — |

By topic: gymtrack-monorepo correctness 3, security 2, other 4; csdev-monorepo docs 2, security 1, question 1;
invisible-assistant correctness 11, other 19, adr 13, rules 7, security 4, docs 2.

Repositories whose workflow references Wachiman (found by reading `.github/workflows/` of every repository in
`gh repo list niway-dev` and `gh repo list csdev19`, default branches): kaipu-record, kaipu-bench-wachi,
kaipu-bench-wachi-v2, gymtrack-monorepo, csdev-monorepo, invisible-assistant, fidelity-card. fidelity-card has
the workflow and no review yet. Other branches were not scanned.

## Privacy

`niway-dev/wachiman` is public. **Nothing from a private repository is committed here**: no code, comment
bodies, titles, paths or PR titles. `fetch.ts`, `runs.ts` and `normalize.ts` write wherever `--out` points, so
the private pass uses an `--out` outside the repository, and only the per-repository figures from its
`normalize-report.json` (`aggregate`) were copied into this README. Check `git status` before adding anything from
a private run.

kaipu-record, kaipu-bench-* are public, so their raw snapshots are committed.

### Labelled, caught none

`labels.csv` has a row only for a finding that matched a verdict, so a run that caught no known bug
looks the same there as a run nobody labelled. `labelled-runs.csv` tells them apart: it has one row per
run and replayed PR whose own analysis doc (the run label's primary doc in `scripts/labels.ts`) has a
column for it in the Expected issues table, even when every cell says `no`.

- **Labelled, caught none:** a row with `expected_caught` 0 and `expected_partial` 0 (for example CR-v1
  on #463).
- **Not labelled:** no row. That covers every finding outside the analysed sets.
- `findings_labelled` counts that run's `labels.csv` rows on that PR (E, A and N), so 0 with a row
  means the run posted nothing an analyst matched.

170 rows: W-R1…R3, PF-v1/v2 and CR-v1/v2 (2026-11-01), W4–W6 (2026-11-02), S7–S9 (2026-11-02-e1-sonnet),
W7–W9 (2026-11-25-v1.20.1-replay), W10–W12 (2026-11-25-v1.21.0-focus-replay), W13–W15
(2026-11-25-v1.21.0-budget-replay) and W16–W18 (2026-11-25-v1.4.0-rerun), each on #463–#467, and W19–W30
(2026-11-26-release-bisect) on #465 and #467, W31–W33 (2026-11-26-v1.21.0-sonnet-baseline) on #463–#467, and
W34–W36 (2026-11-26-prompt-cache-5m) on #465 and #467. A later doc that copies an earlier run's
column for comparison does not label it again.

### Wachiman v1.20.1 formats

v1.20 changed what the engine posts, and `scripts/parse.ts` reads both forms:

- An inline comment opens with a table: `| 👮 **Wachiman** | <title> |`, then Severity, Area and
  Confidence rows. The Priority row (`Should`, `Could`) is not stored.
- The review body indexes every finding in To fix / To consider tables. Only the rows under
  `<details><summary>For your information` (and Outside the diff) are body-only findings.
- Counts and the partial status come from the `<!-- wachi:state … -->` marker; the cost from the last
  `<sub>` footer. On a Claude subscription token that cost is an API-equivalent estimate, not a bill.
- The log names the engine by the commit SHA the workflow pins; `PINNED_SHAS` maps it to its tag.
- `log_duration_ms` sums the batch calls. v1.20.1 runs batches in parallel, so the run's wall time is
  shorter than that sum; W4–W6 are compared on the same sum.

## Contracts

Recoverable, with one loss. The block `What the change connects to (N closed, M open)` in a Wachiman review
body (v1.4.0 and later; 45 of 45 bench reviews and 14 of 16 kaipu-record v1.4.0 reviews have one) is parsed back
into `action`, `location`, `failure_mode`, `status`, `evidence[]`, `open_question`, `candidates[]` and
`evidence_checked` (false when the review printed "A citation did not resolve in the head").

The review prints only one of `visible_effect`, `before_after` and `equivalent_path` per entry (the first that
exists), so they cannot be told apart: `contracts.jsonl` has a single `effect` field. The action is cut at 160
characters and each sentence at 280 when rendered. No review had its contracts cut for size (`contracts_hidden`
is 0 everywhere). v1.3.0 and earlier reviews have no contracts.

## Run map

`runs.csv` is derived, and the owner should check it. `confidence` says how:

- `derived`: tool, model, version and date come from the snapshots and the run logs; the label comes from a doc that
  names it (`basis` gives the doc). 354 rows.
- `guessed`: 63 rows. Labels that no doc gives (`W-set2-R1…R3` and `CR-set2` for the five bug-catalogue PRs #402
  #255 #276 #269 #184, replayed in bench PRs #46–#60 and coderabbit #6–#10; `W-v2` for the failed wachi-v2 repo),
  Pullfrog and CodeRabbit round numbers on kaipu-record (`PF-1`, `CR-2`: the field docs name rounds by commit, I
  numbered them in order), and 16 kaipu-record Wachiman reviews whose version is unknown.
- Labels follow each doc generation: baseline `W-R1…R3`, `PF-v1/v2`, `CR-v1/v2` (2026-11-01); `W4…W6` (2026-11-02);
  `S7…S9` (2026-11-02-e1-sonnet). The field run uses its docs' own names (`Full`, `Inc-4`, `W-i1`, `R0`…`R5`),
  keyed by commit in `FIELD_ROUNDS` in `scripts/runs.ts`, each with the doc line it comes from.
- The version read from a log agreed with the doc in every case that had both.
- **Two sets share a base version.** W31–W33 (Sonnet 5.5, bench #92–#106) and W13–W15 are plain `v1.21.0`, the
  release tag. W34–W36 (bench #86–#91) are pinned by the SHA `8a9a6d782aa1f6c9ef88f1430e8f5cd789f2c8ce`, which is
  v1.21.0 plus the 5-minute prompt-cache fix and is not a release. Its `version` is **`v1.21.0+cache-5m`** so that it
  cannot be confused with plain `v1.21.0` when grouping by version. The SHA-to-version table is `PINNED_SHAS` in
  `scripts/parse.ts` (it holds the other pins too, which are all release tags), and the label rules are in
  `benchLabel` in `scripts/runs.ts`.
- The prompt-cache set was first published as W31–W33 and renamed W34–W36, because the Sonnet baseline uses W31–W33.

### Credential

`runs.csv` and `run-logs.csv` have a `credential` column: what the run authenticated with.

- `oauth-token`: a Claude subscription token. `api-key`: an Anthropic API key. It is read from the `auth` field of the
  first `wachiman-cost` line of the run's log, so it is data, not a doc's claim.
- **Empty means unknown, not "key".** Logs of the older engines (v1.2.x to v1.9.0, so every row of
  kaipu-bench-wachi, W16–W24 and all of kaipu-record) print no `auth`. The reports of W16–W24 say they ran on an API key, but the
  dataset does not turn that into a value. Pullfrog and CodeRabbit rows are empty too.
- v1.15.0 shows both: W25–W27 `oauth-token`, W28–W30 `api-key`. W7–W15 and W31–W36 are all `oauth-token`; W16–W24
  (v1.4.0, v1.5.0, v1.9.0) are empty. The cost
  of an `oauth-token` run is an API-equivalent estimate, not a bill, so compare cost only inside one credential.

## How the join works (and why 148 are left)

For a replay finding, the candidates are the verdicts whose run column in the primary doc for that run says the
run found it. For a field finding they are the verdicts of the same bot on the same PR. A candidate scores a path
match (+3), a line within 8 of a line the verdict names (+4), word overlap with the title and the start of the
text, and a round or commit match for the field docs. A match needs a score of 5.5, wording that agrees with the
location (a path-and-line hit alone is not enough: the same line can host several findings) and a lead of 1.5 over
the runner-up, or a lead of 3. Anything else goes to `ambiguous.md`. The F12a/b/c claims are one Pullfrog comment
in the doc and are labelled together (`F12a|F12b|F12c`).

`shares_verdict_with` lists other findings of the same run matched to the same verdict: the same defect posted
twice. No label says `duplicate` because the docs' duplicate prose is not machine-readable.

## What is missing

- **314 findings are outside the analysed sets**: all kaipu-record PRs other than the seven field PRs, and the
  bench replays of #402 #255 #276 #269 #184 (no analysis doc). They have no `labels.csv` row and are not in
  `ambiguous.md`.
- **kaipu-bench-wachi-v2**: all five runs failed before posting (`agent-review.yml` failed, no job logs).
  Its PRs are in `raw/` and have no findings. Also without any comment: coderabbit #1 #3 #5 (v1) and #1 #4 #5 (v2)
  (CodeRabbit posted a walkthrough only), pullfrog-v2 #1 (setup PR), and 30 of the 112 kaipu-record PRs have a
  Wachiman review with no finding.
- **Logs**: no public log is expired. 17 runs have none because they never started a job (`not-found`), 53 were
  skipped by their `if:`. 39 private-repository logs are past the 90-day retention. All public logs are kept in
  full (1.7 MB gzipped), so nothing was reduced to extracted lines.
- **Runs**: `gh run list` returns at most 1000 runs; kaipu-record is listed per workflow (`Agent review`,
  `Pullfrog`) to get past that, so its CI runs are not in `_runs.json`. Cost and duration come from the logs when
  one exists and from the review footer otherwise.
- **Pullfrog and CodeRabbit in kaipu-record** are only snapshotted on PRs that also have a Wachiman review.
  Pullfrog's "Technical details" blocks inside a comment are not split into findings. CodeRabbit findings raised
  in thread replies or in "Follow-up comments" are not captured (field doc: #482 F17, #483 F19). CodeRabbit's
  walkthrough issue comments are in `raw/` only.
- **Pullfrog cost, model and version** are not parsed: its logs are saved in `raw/` but the log reader looks for
  Wachiman's lines only, and a search of one Pullfrog log found no model or cost line. The `model` for Pullfrog
  rows comes from the doc (`derived` from the doc, not from data).
- **Wachiman's `thread_replies`** ("Looks addressed") are not findings and are not extracted.
- The verdict docs are the owner's reading of the code; this dataset does not re-check any verdict.
