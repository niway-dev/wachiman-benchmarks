# Variance experiment: Wachiman 1.12.0 on the t3code#30579 replay

Question: why did the first run miss T3, T4, T5 and T8? Is it run-to-run variance, or does Wachiman never probe the edge cases of new data-transforming functions?

**Answer: mostly variance.** Over three identical runs, Wachiman found 5 of the 6 reachable defects at least once, but never all of them in the same run. T4 (the empty-body case) showed up in 2 of 3 runs, and T8 in 1. T3 and T5 never showed up. Even T1, a serious bug, was missed in run 3. The edge-case instruction pass (step 2) was not run, because its precondition failed: T4 appeared in runs 2 and 3.

## Setup

- Wachiman 1.12.0 (`WACHIMAN_DIR=…/wachiman/.claude/worktrees/main-1-12`), product defaults (verify off, 1 batch, history off), Claude Opus 5.5, managed profile `isolated:personal`.
- Command, unchanged for every run: `env -u ANTHROPIC_API_KEY WACHIMAN_DIR=… wachiman local --repo-dir /tmp/t3bench-30579 --commit HEAD --profile isolated:personal --format json --output <file>`.
- Clone `/tmp/t3bench-30579` at replay head `dcb86358`, clean. No other reviewer was run, and nothing was posted.
- Run 2 started at load 5.3. Run 3 waited until the 5-minute load average was below 8 (it was 7.4). Neither run hit `spawnSync … ETIMEDOUT`.

## Results

✓ = found, matching the bot thread. — = not found. Time is the review call (`wachiman-cost.duration_ms`); end-to-end time is in brackets. Cost is Wachiman's API-price estimate, not a bill.

| Run | T1 | T2/T6 | T3 | T4 | T5 | T8 | Other findings | Turns | Time | Cost | Output tokens |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run 1 ([`../wachiman.json`](../wachiman.json)) | ✓ fix | ✓ medium | — | — | — | — | none | 9 | 57.1 s (136.9 s) | $0.568 | 5,331 |
| run 2 ([`run2.json`](run2.json)) | ✓ fix | ✓ consider | — | ✓ consider | — | — | N1: Resolve button loses `ml-auto` when Add to chat is wired but hidden | 13 | 83.2 s (187 s) | $0.570 | 7,271 |
| run 3 ([`run3.json`](run3.json)) | — | ✓ fix | — | ✓ consider | — | ✓ (same finding as T2) | N2: Summary-tab Add to chat sends only the first page of a thread's replies | 10 | 73.6 s (156 s) | $0.570 | 6,271 |
| run-edge | not run | | | | | | | | | | |

Union of the three runs: T1, T2, T4, T8 and two new findings. Never found: T3 and T5.

## Judgments

- **T4 in runs 2 and 3: checked.** Both findings point at `pullRequestDetail.logic.ts` (`:709` and `:669`) and say that a body that is only an unclosed `<!--` returns `""` instead of `null`. That is T4's claim and fix.
- **T8 in run 3: checked.** The run 3 finding at `PullRequestDetailPanel.tsx:1077` names a second problem besides the number-only match: the hand-off chip `pull-request-context:N` satisfies `hasPullRequest`, and the next hand-off sweeps it away, so the remark chips are left with no PR reference. That is T8.
- **T1 missing in run 3: checked.** Run 3 has no finding in `PullRequestTimelineTab.tsx`, and its summary does not mention the Timeline tab lookup.
- **T3 never found: checked; why it was missed is inferred.** Runs 2 and 3 did try the unclosed-`<!--` input, but they reported only the empty-return consequence (T4). They did not report the other consequence: real text after the opener is dropped. My reading is that the model treated "truncate at an unclosed opener" as the intended behaviour, not as a bug. So it does probe this odd input, but it does not question the design choice behind it.
- **T5 never found: checked.** No run mentions the `pr-comment:${thread.id}` id format or its scope.
- **N1 is a real cosmetic bug: checked.** At head `PullRequestReviewAnnotation.tsx:255`, Add to chat renders only when a comment has a visible body. Resolve's class at `:270` tests only `onFix || onAddToChat`. With no fix action and all-bookkeeping comments, Resolve loses `ml-auto`. No bot thread covers it.
- **N2 is plausible: inferred, not verified.** `chatSubject` in `PullRequestSummaryTab.tsx:215-223` passes the thread as it is, while the Code tab passes the loaded comments. I did not check whether the Summary tab ever holds extra loaded replies that would be left out.

## What the variance shows

- **The first run's misses are not a fixed blind spot (inferred from 3 runs).** T4 and T8 were reachable and were found in later identical runs. Coverage of the reachable defects was 2, 3 and 3 of 6 per run, and 4 of 6 for the union.
- **The hypothesis "it never attacks the new parser" is partly wrong (checked).** Two of three runs fed `readableBody` an unclosed comment. What was missing in run 1 looks like depth per run (9 turns, 5.3k output tokens) more than a habit of trusting the tests. Runs 2 and 3 used more turns and output tokens, and found more.
- **Severity labels and findings move between runs (checked).** T2 went from `medium`, to `consider`, to `fix`. T1 went from `fix` to absent. Any single run is therefore a sample, not a verdict on a PR. Three runs cost about $1.71, against $0.57 for one.
- **T3 and T5 stay missed in all three runs (checked).** They may need a different prompt, or more runs, to show up. Three runs cannot separate "rare" from "never".

## Edge-case instruction (step 2)

Skipped, because its precondition failed: T4 appeared in runs 2 and 3.

A supported mechanism does exist, so the pass could be run later. Checked in `docs/review-policy.md` and `docs/local-review.md` of the 1.12.0 worktree: Wachiman reads `.github/wachiman.md` (the focus file), then the root `CLAUDE.md` and `AGENTS.md`, from the start of the range. With `--commit`, that is the commit's parent. The replay base `91dc71f7` already has a root `CLAUDE.md` and `AGENTS.md`, but no `.github/wachiman.md`. The way to test it without changing the reviewed diff:

1. Rebuild the base with a `.github/wachiman.md` that holds the instruction.
2. Commit the same head tree, plus that file, on top of the new base.

The diff of `HEAD^..HEAD` is then unchanged.

Since T3 and T5 were never found, this pass is the natural next test for them specifically. It costs about $0.57 per run, and one run would not settle it either.

## Limits

- Three runs is a small sample. The frequencies above (2/3, 1/3) are rough.
- Bot verdicts come from [`../bot-threads.md`](../bot-threads.md) and were not re-judged. The match verdicts and the N1/N2 checks were made by Claude Opus 5.5.
