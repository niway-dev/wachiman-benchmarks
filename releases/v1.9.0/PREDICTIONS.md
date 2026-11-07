# v1.9.0: predictions

- **Registered:** 2026-11-07, **after** the release PR
  ([wachiman#128](https://github.com/niway-dev/wachiman/pull/128)) merged at 05:34 UTC and the tag
  `v1.9.0` was published, but **before any consumer runs it**: the three pins below still read
  `v1.8.0`. This breaks the registering rule ("merge before the release PR merges"). The commit
  time of this file and the commit time of each consumer's pin bump show that no field data
  existed when it was written. See the first Amendment.
- **Previous version:** v1.8.0. **Changes:**
  [v1.8.0...v1.9.0](https://github.com/niway-dev/wachiman/compare/v1.8.0...v1.9.0) (5 `feat` and 4
  `fix` commits, plus the skills and docs: #131, #133 and the local-review commits).
- **Rolled out to** (pin `@v1.8.0` → `@v1.9.0`; each consumer is predicted as it is, no trigger or
  input is added by the bump):
  - niway-dev/kaipu-record: model `claude-opus-5-5`; `pull_request` (opened, ready_for_review,
    **synchronize**) and `issue_comment`. No `pull_request_review_comment`, so thread-reply runs
    do not run there.
  - csdev19/invisible-assistant: model `claude-opus-5-5`; `pull_request` (opened,
    ready_for_review) and `issue_comment`. **No `synchronize`**, so no push re-review runs.
  - niway-dev/wachiman: default model; `pull_request` (opened, ready_for_review) and
    `issue_comment`. No `synchronize`.
- **Evaluation point:** after 5 kaipu-record pull requests with two or more pushes each, or on
  2026-11-21, whichever comes first. The result goes in `RESULTS.md` next to this file.

## In one minute

v1.9.0 fixes the push re-review path that cost kaipu-record money on 2026-11-06 (three defects,
[wachiman#133](https://github.com/niway-dev/wachiman/pull/133)) and renames the surfaces people
type (#131, ADR 0023). **The number that matters most is the cost of a push re-review on a pull
request that holds a binary file**: three full reviews at $0.46, $0.50 and $0.36 on kaipu-record
PR 540, where the second and third should have cost about $0.12. Almost all of the fix runs only
on kaipu-record, because it is the only consumer that reviews pushes. v1.9.0 does **not** change
what happens when the provider refuses a call (no credit): that still blocks the marker. The local
review changes (global `wachiman` command, review one commit, history matching, two skills) run on
no consumer.

## Predictions, one per change

| # | Change | What it should improve | Metric | Baseline (source) | Predicted | Where to read it | Falsified if |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Binaries are classified by the engine; a binary never blocks the marker (#133, dc55910, 79eb122) | A push after a first review that skipped a binary is incremental | Share of pushes after the first review, on PRs holding a binary, that are re-reviews (not full reviews) | kaipu-record PR 540: 0 of 2 pushes were incremental (#133 body) | **All of them** (100 %) | Review footer reads `re-review · N commits`; `agent-review sha=` marker on the review | Any push after a complete first review that pays a full review because of a binary |
| P2 | Same | A push that changes only binaries costs nothing | Model cost of a binary-only push | Charged as a full review (PR 540) | **$0**, a one-line notice, the marker moves | The notice comment and the run log | A binary-only push that calls the model |
| P3 | Same | The cost of a push re-review follows the size of the push | Median cost of a push re-review on kaipu-record, v1.9.0 runs | #133 estimates about $0.12 for PR 540's pushes; v1.4.0 re-reviews cost $0.57 each in the [field run](../../2026-11-02-field/README.md), but that was before the marker fix | **≤ $0.25** | `· $N` at the end of the review footer | Median above $0.40 over 5 PRs |
| P4 | Same | A text file is not wrongly skipped as binary | Files marked `not reviewable: binary` that are text at the head | Not measured | **0** | The headline `all N files reviewed, not reviewable: …`; the file read at the head | Any text file listed as binary |
| P5 | The push re-review answers only pending threads (#133, dc55910) | No second "Looks addressed" on a thread Wachiman already answered | Replies by Wachiman on a thread where Wachiman wrote last, and threads with more than two Wachiman replies | kaipu-record PR 539: one thread got two "Looks addressed" replies (#133 body) | **0** and **0** | The PR threads, `wachi_replies` count | Either number above 0 |
| P6 | Same | A pending thread still gets its answer | Pending threads (owner wrote last, fewer than two Wachiman replies) left unanswered after a push that touched them | Not measured | **0** unanswered, on at least 3 pending threads | The PR threads | 1 or more pending thread skipped after a push that changed its lines |
| P7 | Every automatic run shows its cost and the PR's running total (#133, ADR 0008, 0011, 0012) | The price is visible without opening the log | Share of automatic runs and push-review replies that carry `this run $N · PR so far $M over K automatic runs` | Replies carried no cost; the cost sat only in the body footer (#133 body) | **100 %** of automatic runs on kaipu-record; the first review on invisible-assistant and wachiman shows the footer too | Review footers and reply lines | Any automatic run, or a push-review reply, without a cost line |
| P8 | The ceiling neither sums nor counts the unflagged reply line (#133) | No run is counted twice | Ceiling `spent` against the sum of signed footers on a PR | Not measured | Equal to the sum of the review footers, ±$0.01 | Footers against the ceiling notice, if any | A PR whose `PR so far` exceeds its signed footers |
| P9 | One name, Wachiman (#131, ADR 0023) | Old and new names both work | Runs started by `/wachiman review` and by `/wachi review` | `/wachi review` only, on the three consumers | **Both start a run**, the `/wachi` run unchanged | The `Wachiman on demand` job after each comment | Either comment starts no run |
| P10 | Same: focus file `.github/wachiman.md`, old `.github/agent-review.md` read with a notice | The consumers keep their focus without a rename in the bump | Reviews that apply the focus file, and the notice | Focus applied from `.github/agent-review.md` (both consumers hold it) | **Applied, plus a notice** that names the new path, on the three consumers | The run log; the review body | A run that ignores the old focus file |
| P11 | Same: caller file `wachiman-review.yml`, check names `Wachiman review …` | Nothing breaks | Required status checks that stop matching | None known; the review is advisory | **0** | Branch protection on the three repos; the check names on the first PR | A merge blocked on a check named `Agent review` |
| P12 | Thread-reply runs, `wachi_replies` in the review input (#89d6e97) | — | — | — | **Does not run on any consumer**: none has a `pull_request_review_comment` trigger. P5 and P6 cover only the push path | — | — |
| P13 | Local review: global command, one commit or from a commit, history matching by cited line, skills `wachiman-review` and `wachiman-audit` | — | — | — | **Does not run on any consumer**: these are laptop features. They are scored in their own audits, not here | — | — |

P1 to P8 run on kaipu-record only, because only its caller has `synchronize`. On invisible-assistant
and wachiman, P1 to P6 are "does not run here"; P7, P9, P10 and P11 do.

## Known not fixed

| Problem | Current number (source) | Expected in this release |
| --- | --- | --- |
| A provider refusal (no credit, rejected key) blocks the marker, so the next push pays a full review | Nov 4-5 runs on kaipu-record were all refused, $0.00 footers ([audit](https://github.com/niway-dev/wachiman/pull/133)) | unchanged: still blocks |
| Cancelled runs are not counted by the ceiling (ADR 0012 reopen condition) | Out of scope in #133 | unchanged |
| Threads are never resolved automatically | ADR 0008 non-goal | unchanged; a later opt-in |
| A normal re-review's cost follows turns, not diff size | $0.57 per v1.4.0 re-review, median turns 7 → 14 (field run; [v1.5.0 predictions](../v1.5.0/PREDICTIONS.md)) | P3 sets the new bar: ≤ $0.25 |
| The `+undefined` golden-prompt mocks | Follow-up named in #133 | unchanged |

## Risks to watch, and when to roll back

| Risk | Signal | Roll the pin back to `@v1.8.0` if |
| --- | --- | --- |
| A text change rides in with a binary push and is never reviewed | The marker moves past a push whose patch had a text hunk | Once, confirmed in the patch |
| The pending-thread filter hides a reply that is due | A thread where the owner wrote last gets no reply after a push | Twice |
| The renamed focus file is not found | Review without the focus the file asks for, or no notice | Once |
| The new cost line mis-states spend | `PR so far` differs from the footers (P8) | Twice, or once above $0.10 off |
| The binary check reads the file at the head and fails | A run that errors on a missing or large file | Once on a data PR |

## How the results will be scored

- **P1 to P4, P7, P8** come from the signed review footers and the Actions logs
  (`gh run view --log`) of the evaluated kaipu-record PRs, read the same way as the 2026-11-06
  audit. Binary-holding PRs are listed first, because they are the case the fix targets; if fewer
  than 2 such PRs occur by the evaluation point, P1 and P2 are scored "not measurable" and a
  one-off test PR with a PNG is the fallback, flagged as synthetic.
- **P4 and P6** need a read of the code at the head by the owner or a subagent; each verdict names
  the file or thread read.
- **P5 and P6** come from the PR threads: for each, who wrote last, and how many Wachiman replies.
- **P9 to P11** are checked once, on the first PR of each consumer after the bump.
- The first `v1.9.0` run of each consumer is recorded under Amendments as one run, not a result.

## Amendments

- **2026-11-07, at registration.** The "Registered" line says the rule was broken: the release PR
  merged at 05:34 UTC, before this file. Nothing else changes the predictions: no consumer had run
  v1.9.0 and the pins read `@v1.8.0`. Wachiman's own pin on its self-review caller (#123) is also
  `v1.8.0`, and moves only after this file merges.
- **Sources not re-read.** The baselines for PR 539 and PR 540 come from the body of wachiman#133,
  not from a fresh read of the kaipu-record logs.
