# v1.5.0: predictions

- **Registered:** 2026-11-03, before the release PR
  ([wachiman#84](https://github.com/niway-dev/wachiman/pull/84)) merged.
- **Previous version:** v1.4.0. **Changes:**
  [v1.4.0...v1.5.0](https://github.com/niway-dev/wachiman/compare/v1.4.0...main) (9 `feat` and 2
  `fix` commits: #74, #88, #89).
- **Rolled out to:** niway-dev/kaipu-record. The pin moves from `@v1.4.0` to `@v1.5.0`. The model
  is `claude-opus-5-5`. Triggers are `pull_request` (opened, ready_for_review, synchronize) and
  `issue_comment`. There is **no `pull_request_review_comment`**, so thread-reply runs do not run
  there.
- **Evaluation point:** after 5 kaipu-record pull requests that change main-process data code
  (`apps/kaipu-record/src/main/**`), or on 2026-11-17, whichever comes first. The result goes in
  `RESULTS.md` next to this file.

## In one minute

v1.5.0 should find more of the data-path bugs Wachiman missed in the
[field run](../../2026-11-02-field/README.md), with no new invalid findings and no rise in cost per
batch. **The number that matters most is the share of real Medium+ bugs Wachiman finds on
data-path PRs**: 4 of 14 (29 %) in the field run, 7 of 10 in the
[A/B](../../2026-11-03-data-path-questions-ab/README.md). The A/B was in-sample, so new code should
land between those two numbers. v1.5.0 also stops re-reviewing code merged in from `main`. It does
**not** make a normal re-review cheaper: that cost follows turns, and nothing here changes them.

## Predictions, one per change

| # | Change | What it should improve | Metric | Baseline (source) | Predicted | Where to read it | Falsified if |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Data-path questions (#88, ADR 0016) | Recall on data-path bugs | Share of the real Medium+ bugs on the evaluated PRs that Wachiman posts | 4 of 14, 29 % (field run) | **40–60 %** | Audit of the evaluated PRs: bugs found by any bot, the owner or a later fix | ≤ 29 %: no better than the field run |
| P2 | Same | No new noise | Invalid findings among all Wachiman findings, audited | 0 of 76 (field run), 0 of 39 with questions (A/B) | ≤ 1 in 20 | Same audit | > 1 in 20 |
| P3 | Same | Questions only where the pattern is | Share of files that fire any question | 9 % on kaipu data PRs, 2 % on UI, docs or CI PRs (`scripts/questions-firing.ts`, #88) | 5–15 % on data PRs, ≤ 5 % elsewhere | `Data-path questions for part …` log lines | ≥ 20 % on non-data PRs |
| P4 | Same | No cost penalty | Cost per batch that fired, against batches that did not, same size class | A/B: $0.52 with questions against $0.59 without | Fired batches ≤ 25 % above unfired | `cost_usd` per batch in the `review / Agent review` log | > 25 % above, with no confirmed finding from a question (ADR 0016's reopen condition) |
| P5 | Merge into a re-reviewed file sends only the author's rows (#89, ADR 0011 amendment) | No review of code from `main` | (a) model cost of a push that only merges `main`; (b) findings on lines the author did not write | (a) charged as a normal re-review; (b) 3 of 3 v1.4.0 merge re-reviews in the field run, with HTTP 422 refusals | (a) **$0**, with the "Brought up to date" review; (b) **0** | Review bodies and footers; the engine log; refused-inline lists | Any merge-only push that calls the model, or a finding on a merged-in line |
| P6 | Automatic ceiling, default $6 per PR (#74, ADR 0012) | Bound the spend per PR | Automatic spend per PR; ceiling notices | Max $3.49 per PR in the field run (#483, mostly v1.3.0, uncapped) | No PR above $6 automatic. At most 1 in 5 data PRs reaches the ceiling | Signed footers, ceiling notice | A PR above $6, or a ceiling hit before a push that held a real bug |
| P7 | Thread replies answered without a push (#74) | — | — | — | **Does not run on kaipu-record**: the caller has no `pull_request_review_comment` trigger | — | — |

## Known not fixed

| Problem | Current number (source) | Expected in this release |
| --- | --- | --- |
| A normal re-review's cost (turns, not diff size) | $0.57 per v1.4.0 re-review, median turns 7 → 14 from v1.3.0 to v1.4.0 (field run; #89) | unchanged ± 20 % |
| Re-reviews' share of the bill | 49 % ($7.23 of $14.66, field run) | unchanged ± 10 points |
| Bugs no question targets: a pending id adopted without rebinding the gate (#482) | missed in every A/B run | still missed |
| `copyToAll` from an unreadable source (#482) | missed by both A/B arms | still missed |
| Trigger limits written in each question module (e.g. `read-error-as-empty` needs the write in the same added lines) | ADR 0016 | unchanged |
| CSS cascade and layout-shift bugs | 2 shipped, 0 caught by any bot (field run) | still not caught |
| Local runs need a wrapper that restores `USER` | A/B harness | unchanged |

## Risks to watch, and when to roll back

| Risk | Signal | Roll the pin back to `@v1.4.0` if |
| --- | --- | --- |
| Questions add noise | Invalid findings in the audit | 2 or more invalid findings in the evaluated set |
| Questions add cost | Cost per 1,000 changed lines of a first review | Above $0.95 on 3 PRs (1.5 times the v1.4.0 replay's $0.63) |
| The ceiling hides a needed review | Ceiling notice, then a later real bug in an unreviewed push | Once on a data PR |
| The merge fix drops the author's own lines | A re-review after a merge skips a line the author wrote | Once, confirmed in the patch |

## How the results will be scored

- **Cost, firing, ceiling and merge pushes** come from the Actions logs (`gh run view --log`) and
  the signed footers, as in the field run.
- **P1 and P2** need an audit. Every Wachiman finding on the evaluated PRs gets a verdict from
  reading the code at the head and the fix commit, done by subagents running locally on the Claude
  Code subscription. The real Medium+ list comes from all sources: Wachiman, CodeRabbit when it
  ran, the owner's tests and later fix commits.
- P1 is scored only on PRs that fired at least one question. PRs that fired none are counted
  separately.

## Amendments

None.
