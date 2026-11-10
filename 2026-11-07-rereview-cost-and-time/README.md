# Re-review cost and time: Wachiman vs Pullfrog on kaipu-record PR #546

**Status:** measurements and a plan. The reproduction test below has not been run.
**Date of measurements:** 2026-11-07. Revised the same day after an independent review that re-checked the numbers against the Actions logs (section 9 lists what changed).
**Costs** are what each tool reports (Wachiman review footer, Pullfrog run log). They are not reconciled with the billing account.

## 1. Summary

- **Problem.** The owner finds Wachiman's cost close to Pullfrog's and wants it lower. Per review run Wachiman costs about half of Pullfrog; reading the PR's changes once each, the costs per line reviewed are similar.
- **Time is mostly a deliberate wait, not review speed.** Every Wachiman run after the first waits 180 s ("Wait for further pushes", a debounce) before it starts. The review step itself took 58 s, 109 s, 111 s and 42 s. Pullfrog's whole job took 157 s and 207 s. On model time Wachiman's re-reviews are about as fast as Pullfrog or faster. The wait is a product choice and can be reported separately.
- **Cost falls with the size of the change, down to a floor near $0.27.** Re-reviews cost $0.57 (676 lines), $0.55 (417), $0.28 (61) and $0.27 (9). The earlier reading that cost does not shrink with the diff holds only between 417 and 802 lines. What the $0.27 floor consists of is the open question.
- **The #546 runs used Wachiman v1.8.0** (verified in the run logs), before the cost fixes of 1.9.0.
- **What the test will decide.** (a) Where the cost floor is and what is in it. (b) Whether 1.9.0 lowers it. (c) How Wachiman and Pullfrog compare on cost per line and on step time, under a clean method.
- **Needed from the owner.** Spend approval and a decision on Pullfrog effort (section 8).

## 2. The data

### 2.1 Wachiman on niway-dev/kaipu-record PR #546

Source: review footers, and the job steps of the GitHub Actions runs of `wachiman-review.yml` (`gh api .../actions/runs/<id>/jobs`), read 2026-11-07. Claude Opus 5.5, effort high, engine `review.yml@v1.8.0` for every row. Run wall time is workflow start to end, so it includes queue, setup and the wait.

| Reviewed commit | Kind | Files / lines | Cost | Turns | Tokens: in / out / cache read / cache write | Run wall | Wait step | Review step |
|---|---|---|---|---|---|---|---|---|
| 55ae970 | first review, whole PR | 20 / 802 | $0.47 | 9 | 14 / 5.5k / 343k / 58k | 69 s | none | 58 s |
| 1cc738a | rebase, "no content" | n/a | no cost line | n/a | n/a | 3 m 20 s | 180 s | 4 s |
| 93a721a | re-review | 9 / 676 | $0.57 | 12 | 18 / 9.5k / 425k / 58k | 5 m 05 s | 180 s | 109 s |
| 6d2bf6a | re-review | 2 / 417 | $0.55 | 10 | 12 / 11k / 237k / 59k | 5 m 06 s | 180 s | 111 s |
| 9c07227 | re-review | 4 / 61 | $0.28 | 9 | 10 / 3.7k / 127k / 36k | 3 m 56 s | 180 s | 42 s |
| 177ecc1 | re-review | 1 / 9 | $0.27 | 9 | 10 / 2.7k / 108k / 40k | not read | not read | not read |

Findings: 55ae970 one consider-level (webcam seek lead, fixed in 9c07227); 93a721a one fix-level (cut hand-off seeks the video at every contiguous boundary, fixed in d222c3b); 6d2bf6a, 9c07227 zero. 177ecc1 not read.

Arithmetic on these rows:

- The three costs used in the first draft: $0.47 + $0.57 + $0.55 = $1.59. With the two later re-reviews: $2.14 for five costed runs.
- Cost up to 93a721a: $0.47 + $0.57 = $1.04 (1cc738a has no cost line, and its review step lasted 4 s, so the model call was most likely skipped).
- Run wall time from the start of 55ae970 to the end of 93a721a: 69 s + 200 s + 305 s = 574 s. Of that, 360 s is two waits of 180 s; the review steps add up to 58 + 4 + 109 = 171 s.
- Cache read per turn is about 38k, 35k, 24k, 14k and 12k tokens across the five costed runs (derived). Cache write: 58k, 58k, 59k, 36k, 40k.

### 2.2 Pullfrog on the same code

Source: Pullfrog run logs and job spans on niway-dev/kaipu-bench-pullfrog-v3 (PRs #2 and #3). Replay head 93a721a, base 1e7cf17. Pullfrog keeps notes per repository between runs, so run 2 was contaminated by notes from run 1.

| Run | PR | Description | Effort (from log) | Repo notes seeded | Findings | Cost | Job time | Agent time |
|---|---|---|---|---|---|---|---|---|
| 1 | #2 | original final description (names later fixes) | medium (the default, not set explicitly) | no | 2 | $1.00 | 157 s | 119 s (self-reported) |
| 2 | #3 | minimal | high | yes | 0 | $1.47 | 207 s | not read |

Pullfrog run 1 findings: the split between source-contiguous clips seeks the video at every cut (same defect Wachiman reported at 93a721a); Play at the end of the layout does nothing (not reported by Wachiman at 93a721a; fixed by the owner in e2ebac2, which lands before 6d2bf6a; whether it is a real defect is not independently verified). It did not report the webcam seek-lead defect. Neither Pullfrog run is clean, so nothing is scored.

## 3. The owner's claim: "Wachiman charges half but takes twice as long to find the same thing"

**What is right.**

- Per review run, Wachiman costs about half of Pullfrog run 1 ($0.47 and $0.57 against $1.00).
- Wall time from push to posted review is longer for Wachiman: about 5 minutes per re-review against about 2 to 3.5 minutes for Pullfrog.

**What is imprecise.**

- **The time gap is the 180 s wait.** Without it Wachiman's re-review steps (109 s, 111 s, 42 s) are at or below Pullfrog's job time (157 s, 207 s). So the time cost is a choice (wait for further pushes before starting, which also avoids paying for a review of a head that is about to change) and not review speed. Whether the wait is worth its delay is a separate question.
- **Cost to the same commit is not a like-for-like comparison.** Wachiman paid $1.04 for two incremental runs covering 802 + 676 lines. Pullfrog paid $1.00 for one read of the final diff (about 1,400 lines). The statement supported by the data is that the cost per line reviewed is similar. Which tool is cheaper on a live PR with many pushes is what arm C of the test answers; Pullfrog on the live PR would also have run more than once.
- **"The same thing" is not the same result set.** Both found the split-seek defect. Wachiman alone reported the webcam seek lead; Pullfrog run 1 alone reported Play at the end of the layout.
- **Effort differs.** Wachiman runs at high. Pullfrog run 1 ran at its default medium. The one high-effort Pullfrog run was contaminated.

## 4. What is explained and what is not

**Observation (measured).** Re-review cost by size of the change: $0.57 (676 lines), $0.55 (417), $0.28 (61), $0.27 (9). The first review of 802 lines cost $0.47. So cost does fall with the diff, to a floor near $0.27, with a flat part between roughly 400 and 800 lines. Turns are 9 to 12 in every run. Cache write fell from 58k to 36k to 40k tokens at the small sizes.

**Open question.** What the floor of about $0.27 and about 9 turns consists of, and why a 417-line and a 676-line re-review cost the same. A first review (no open threads) cost less than the two large re-reviews.

**Hypotheses (not tested).**

- **H1.** A fixed amount of context is rebuilt in every run (instructions, repository map, open threads). Partly weakened by the cache write falling to 36k to 40k at small diffs.
- **H2.** The number of model turns drives cost more than the diff. Turns barely vary (9 to 12), so with this data it cannot be separated from the others.
- **H3.** Re-review repeats a fixed amount of work (checking open threads, the "what the change connects to" questions). Not measured; the run logs may show which stages ran.
- **H4.** The engine version changes the per-run work (section 5).

## 5. Version

- Verified: the run logs show `review.yml@refs/tags/v1.8.0` for the #546 runs, so they did not include the fixes of the 2026-11-06 cost audit (PR #133: binaries by script, `pendingThreads` on push, cost on every run).
- Verified: tag v1.9.0 exists (release commit b3f60be, merge of PR #128, 2026-11-07 00:34 -0500).
- The 1cc738a run's log says it rebased with no content and its review step took 4 s, so the missing cost line there reflects a skipped model call, not only a missing print.
- kaipu-record's workflow on origin/main pins v1.8.0. Moving it to v1.9.0 is the first thing to try.

## 6. Notes for the analyzer and the refuter

Owner direction: Wachiman's analyzer (the stage that proposes findings) and refuter (the stage that tries to falsify them) have a lot of room to improve.

Observations on PR #546, not causes:

- **Split-seek defect.** Introduced by commit 0c88e06; found only at the re-review after it landed (93a721a), not at the first review.
- **Play at end of layout.** Pullfrog reported it on the same code; Wachiman did not at 93a721a. Whether it is real is not independently verified.
- **Webcam seek lead.** Wachiman reported it at consider level at 55ae970; Pullfrog run 1 did not. Fixed in 9c07227.
- **Zero findings at 6d2bf6a and 9c07227.** Not checked against the code.

One PR is not enough to say more. Questions before changing either stage: (1) was the Play-at-end handler in the analyzer's input at 93a721a; (2) did the refuter reject any finding at 93a721a or 6d2bf6a, and why; (3) is the zero-finding result at 6d2bf6a right (needs a code read).

## 7. The reproduction test (plan, not run)

### 7.1 Questions

- (a) Where is the re-review cost floor, and what is in it?
- (b) Does v1.9.0 change it?
- (c) How do Wachiman and Pullfrog compare on cost per line reviewed and on review-step time, under a clean method?

### 7.2 Arms

| Arm | Reviewer | Setting | Note |
|---|---|---|---|
| A | Wachiman, pinned v1.8.0 | pin in the workflow file the replay repo carries | effort high, as in the real runs |
| B | Wachiman, pinned v1.9.0 | same, different tag | tag exists (section 5) |
| C | Pullfrog, Opus 5.5 | effort high, checked in the run log | run 1 used the default (medium); the mechanism to set it explicitly must be confirmed (the dashboard setting the owner changed on 2026-11-07) |

### 7.3 Method

0. **No-spend step (done in this revision).** Pinned ref read from the logs (v1.8.0), the 1cc738a and 9c07227 runs read, step times read. What remains to read: the 177ecc1 run.
1. **Fresh replay repositories.** `replay/bench.sh create wachi <name>` for Wachiman arms. **Set the pin yourself:** `replay/wachi-workflow.yml` currently pins v1.3.0, so an unedited copy would silently run the wrong arm. Check the resolved ref in each run log. The Pullfrog arm needs a fresh repository for each repeat of the push sequence (its notes carry across pushes inside one repository, which is part of how it behaves), a minimal PR description, and a log check for `learnings seeded ... existing=no` and the intended `effort:`.
2. **Replay as one pull request advanced by real pushes.** There is no `bench.sh` command for this: `create` opens one PR at the final head with the original description, and `rounds` is Wachiman-only and pushes the same SHA to new branches (to dodge the engine's "already reviewed this head" check), which does not exercise re-review. The sequence is manual git: push the PR branch at each of 55ae970, 1cc738a, 93a721a, 6d2bf6a, 9c07227 and 177ecc1 (or their equivalents), one after another, and wait for each review to finish before the next push. Notes: 1cc738a is a rebase, so the **base branch also moves** (from a35cc89 to 1e7cf17); 55ae970 is still fetchable (its parent is 9899eee). Check each push's diff size against the table in 2.1.
3. **Controls.** (i) One full review of the final head in a separate fresh repository per arm, to price a full read. (ii) Three repeats of the full push sequence per arm, each in a new repository.
4. **Measure per run.** Footer cost (Wachiman) or `Cost ($)` row (Pullfrog), turns, tokens (in, out, cache read, cache write), and from the Actions API the job time and the time of each step, reporting the review step apart from the wait, queue and setup. Findings and the commit each was posted on.
5. **Decide with the rules in 7.4, then report with the limits in 7.6.**

### 7.4 Decision rules (proposed; fixed before the first run and changed only by the owner)

- **R1, size effect.** Compare re-reviews of different sizes only (about 676, 417, 61 and 9 lines), so mode is not confounded with size. Report cost against changed lines per arm. The floor is the median cost of the two smallest pushes. Cost is independent of size above the floor if the 676-line and 417-line medians differ by 20% or less.
- **R2, incremental vs full.** Compare cost per changed line, and compare the two tools' incremental sequence totals with each other. Do not compare the incremental sum with one full read of the final head: the sum of several runs will always exceed one read, so that rule cannot fail. The full-review control (i) still gives the price of one full read per tool.
- **R3, v1.9.0.** 1.9.0 helps if its median sequence cost is lower than 1.8.0's by more than the 1.8.0 spread (max minus min over its three repeats). Findings are nondeterministic, so "same defects" means a defect reported at a commit by a majority of the repeats of that arm; a cheaper arm that loses a majority-reported defect is not counted as a saving.
- **R4, Wachiman vs Pullfrog.** Medians per sequence for cost, cost per changed line and review-step time, side by side, with both findings lists per commit. No winner on cost alone: a winner needs the findings checked against the code at each commit.

### 7.5 Budget and time

The per-run figures are planning numbers from measured runs. Wachiman: $0.55 for pushes of 400 to 700 lines, $0.27 to $0.28 for small ones, so about $0.45 average over six pushes. Pullfrog: $1.00 to $1.47 per full read; small pushes will probably cost less and Pullfrog may not run on a no-diff rebase push, so the range is an upper bound.

| Item | Runs | Planning cost per run | Subtotal |
|---|---|---|---|
| Arm A, Wachiman 1.8.0 (3 repeats x 6 pushes) | 18 | about $0.45 | about $8 |
| Arm B, Wachiman 1.9.0 (3 repeats x 6 pushes) | 18 | about $0.45 | about $8 |
| Arm C, Pullfrog (3 repeats x 5 to 6 pushes) | 15 to 18 | up to $1.00 to $1.47 | up to about $15 to $26 |
| Controls, one full review each (A, B, C) | 3 | $0.5, $0.5, $1.0 to $1.47 | about $2 to $2.5 |
| **Total** | | | **about $33 to $45, upper bound** |

Suggested cap: $45, to be confirmed by the owner before launch. Retries and failed runs are not included.

Time, one arm after another: the wait dominates. A Wachiman sequence of six pushes takes about 6 x 3 min of waiting plus about 6 x 1.5 min of review, so about 25 to 30 minutes; six sequences are about 2.5 to 3 hours of wall time, mostly the debounce, and sequences of different arms can run at the same time because they are on GitHub-hosted workflows in separate repositories. If any arm runs locally, one heavy process at a time.

### 7.6 Limits

- One pull request, one repository.
- Wall time includes queue and setup; report step times next to it.
- Costs are self-reported by each tool, not reconciled with billing.
- Replayed commits may get new SHAs; check the diff sizes at each push.
- Pullfrog keeps notes per repository; a fresh repository and the `existing=no` check are the only control.
- Findings are nondeterministic; verdicts need the code at each commit to be read.

## 8. Open questions for the owner

1. **Spend.** Approve the budget (about $33 to $45 upper bound, cap $45) and the order of work.
2. **Visibility.** niway-dev/kaipu-record is public (checked 2026-11-07), as are the existing replay repositories, so public replay repositories are consistent with earlier rounds. Confirm.
3. **Pullfrog effort.** High (matches Wachiman, recommended) or medium (Pullfrog's default, matches run 1; cheaper).
4. **The 180 s wait.** Keep, shorten or make it configurable? It accounts for most of Wachiman's longer wall time, and it avoids paying for a review of a head that is about to change.
5. **Repeats and thresholds.** Three repeats per arm; the 20% rule (R1) and the spread rule (R3).
6. **Play at end of layout.** Is it a real defect? A code read at 93a721a is needed; who does it?
7. **Analyzer and refuter.** Answer section 6 questions 1 and 2 before changing either stage?

## 9. What changed after the independent review

A fresh reviewer (Fable, low effort, read-only) re-checked the first version against the Actions logs and the PRs. Verified and applied:

- The time comparison was wrong: the 180 s wait step accounts for most of the gap; review steps are 58, 109, 111, 42 s.
- The 9c07227 row was marked unknown but exists ($0.28, 4 files / 61 lines), and so does 177ecc1 ($0.27, 1 file / 9 lines); cost does fall with size.
- "About equal cost to the same commit" compared incremental runs with a one-shot read.
- Pullfrog times: job spans are 157 s and 207 s; 119 s was the agent's self-reported time.
- Decision rules R1 (mode confounded with size), R2 (could not fail) and R3 (assumed deterministic findings) were rewritten.
- Feasibility: no `bench.sh` command for sequential pushes; the base branch moves for the rebase step; the replay workflow template pins v1.3.0.
- The version and tag questions are answered.

## Links

- Source PR: https://github.com/niway-dev/kaipu-record/pull/546
- Pullfrog replay, run 1: https://github.com/niway-dev/kaipu-bench-pullfrog-v3/pull/2
- Pullfrog replay, run 2: https://github.com/niway-dev/kaipu-bench-pullfrog-v3/pull/3
- Sibling snapshot folder: `../2026-11-07-kaipu-record-546-snapshot/` (added by https://github.com/niway-dev/wachiman-benchmarks/pull/17, so it appears here only once that PR merges)
