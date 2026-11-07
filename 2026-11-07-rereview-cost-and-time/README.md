# Re-review cost and time: Wachiman vs Pullfrog on kaipu-record PR #546

**Status:** measurements and a plan. The reproduction test below has not been run.
**Date of measurements:** 2026-11-07.
**Costs** are what each tool reports (Wachiman review footer, Pullfrog run log). They are not reconciled with the billing account.

## 1. Summary

- **Problem.** The owner finds Wachiman's cost close to Pullfrog's, and wants it lower. Per review run, Wachiman costs about half of Pullfrog. To reach the same commit, the totals are about equal, and Wachiman takes several times longer in wall time.
- **Measured per run.** Wachiman $0.47 to $0.57. Pullfrog run 1 $1.00, Pullfrog run 2 $1.47.
- **Measured to reach commit 93a721a.** Wachiman $1.04 across two costed runs, plus one run with no cost line (so $1.04 is a floor). Pullfrog run 1 $1.00 in one run.
- **Measured wall time.** Wachiman 9 min 34 s across three runs; Pullfrog run 1 about 2 min. Each Wachiman re-review took about 5 min.
- **Unknown.** Why a re-review of 417 changed lines cost about as much as the first review of 802 lines. Four hypotheses are listed in section 4; none is tested. Also unknown: whether the #546 runs used Wachiman 1.8.0 or 1.9.0.
- **What the test will decide.** (a) Whether re-review cost depends on the size of the change. (b) Whether release 1.9.0 changes that. (c) How Wachiman and Pullfrog compare on cost and time for the same commits.
- **Needed from the owner.** Approval of the spend (planned $32 to $40, cap $45) and a decision on whether the replay repositories may be public (section 8).

## 2. The data

### 2.1 Wachiman on niway-dev/kaipu-record PR #546

Source: review footers and GitHub Actions run metadata, workflow `wachiman-review.yml`, read 2026-11-07. Wachiman runs with Claude Opus 5.5, effort high. Wall time is the workflow run start to end, so it includes queue and setup, not only model time.

| Reviewed commit | What it reviewed | Files / lines | Footer cost | Turns | Tokens: in / out / cache read / cache write | Wall time | Findings |
|---|---|---|---|---|---|---|---|
| 55ae970 | whole PR, first review | 20 / 802 | $0.47 | 9 | 14 / 5.5k / 343k / 58k | 69 s | 1, consider level (webcam seek lead) |
| 1cc738a | rebase onto 1e7cf17, "no new changes since 55ae970" | n/a | no cost line | n/a | n/a | 3 m 20 s | unknown |
| 93a721a | re-review of changes since 1cc738a | 9 / 676 | $0.57 | 12 | 18 / 9.5k / 425k / 58k | 5 m 05 s | 1, fix level (cut hand-off seeks video at every boundary) |
| 6d2bf6a | re-review of changes since 93a721a | 2 / 417 | $0.55 | 10 | 12 / 11k / 237k / 59k | 5 m 06 s | 0 |
| 9c07227 | last fix commit | unknown | unknown | unknown | unknown | 3 m 56 s | unknown (review text not read) |

Arithmetic on these rows:

- Sum of the three costed runs: $1.59.
- Cost up to 93a721a: $0.47 + $0.57 = $1.04 (1cc738a is uncosted).
- Wall time from the start of 55ae970 to the end of 93a721a: 69 s + 3 m 20 s + 5 m 05 s = 574 s, which is 9 min 34 s.
- Derived, not measured directly: cache read per turn is about 38k, 35k and 24k for the three costed runs. Output tokens per run went from 5.5k to 11k, so the cost is not strictly fixed.

### 2.2 Pullfrog on the same code

Source: Pullfrog run logs on the replay repository niway-dev/kaipu-bench-pullfrog-v3 (PRs #2 and #3). Replay head 93a721a, base 1e7cf17. Pullfrog keeps notes per repository between runs, so run 2 was contaminated by notes from run 1.

| Run | PR | Description | Effort (from log) | Repo notes seeded | Findings | Cost | Time |
|---|---|---|---|---|---|---|---|
| 1 | #2 | original final description (names later fixes) | medium | no | 2 | $1.00 | 119 s |
| 2 | #3 | minimal | high | yes | 0 | $1.47 | about 3 m 21 s (about 201 s) |

Pullfrog run 1 findings:

- The split between source-contiguous clips seeks the video at every cut. This is the same defect Wachiman reported at 93a721a.
- Play at the end of the layout does nothing. Wachiman did not report this at 93a721a. The owner fixed it later in e2ebac2. Whether it is a real defect is not verified.
- Pullfrog run 1 did not report the webcam seek-lead defect that Wachiman reported at 55ae970.

Neither Pullfrog run is clean, so nothing is scored.

## 3. The owner's claim: "Wachiman charges half but takes twice as long to find the same thing"

**What is right.**

- Per review run, Wachiman costs about half of Pullfrog run 1. $0.47 and $0.57 are 47% and 57% of $1.00.
- Against Pullfrog run 2 ($1.47, effort high), Wachiman is 32% to 39%. Run 2 was contaminated by notes, so this comparison is weaker.

**What is imprecise or wrong.**

- **Cost to the same commit is about equal, not half.** Wachiman needed $1.04 over two costed runs (plus an uncosted rebase run). Pullfrog run 1 needed $1.00 in one run.
- **Time is understated.** The Wachiman path to 93a721a took 574 s. Pullfrog run 1 took 119 s. That is 4.8x. Each Wachiman re-review (305 s and 306 s) is 2.6x Pullfrog run 1, and 1.5x Pullfrog run 2. "Twice as long" fits one re-review against run 2 only.
- **"The same thing" is not the same result set.** Both tools found the split-seek defect. Wachiman alone reported the webcam seek lead (at 55ae970). Pullfrog run 1 alone reported Play at the end of the layout (not reported by Wachiman at 93a721a).
- **The effort settings differ.** Wachiman runs at effort high. Pullfrog run 1 ran at medium. The only high-effort Pullfrog run was contaminated, so there is no clean like-for-like run yet.
- **The timing sources differ.** Wachiman's time includes queue and setup. Pullfrog's time comes from its own log, and the span it covers is not stated in the log extract used here.

## 4. The unexplained observation and the hypotheses

**Observation (measured).** The 417-line re-review (6d2bf6a, $0.55) cost about as much as the 802-line first review (55ae970, $0.47). Cache write was 58k, 58k and 59k tokens in the three costed runs.

**Pattern (n = 3, weak).** Cost rises with turns in these three runs: 9 turns $0.47, 10 turns $0.55, 12 turns $0.57. Output and cache reads also vary, so turns cannot be separated from them with this data.

**Hypotheses (not tested).**

- **H1.** Each run rebuilds the same large context (instructions, repository map, open threads), whatever the size of the diff. Consistent with the nearly constant cache write. Against it: cache read varies from 237k to 425k, so the loaded context may not be identical across runs.
- **H2.** The number of model turns (9 to 12) drives cost more than the size of the diff. Consistent with the ordering above, with n = 3.
- **H3.** Re-review repeats a fixed amount of work, such as checking open threads and the "what does this change connect to" questions. Not measured. The run logs may show which stages ran; this has not been checked.
- **H4.** The engine version changes per-run work (section 5). Not tested.

These hypotheses are not exclusive. The test in section 7 is built to separate H1 and H2 by comparing a large single review with several small pushes, and by keeping the push sequence fixed across arms.

## 5. Version question (not verified)

- Wachiman release 1.9.0 shipped 2026-11-07 00:34 -0500 (merge of PR #128). It includes fixes from the 2026-11-06 cost audit (PR #133): binaries by script, `pendingThreads` on push, and cost reported on every run.
- The kaipu-record workflow on origin/main pins `niway-dev/wachiman/.github/workflows/review.yml@v1.8.0`. So the #546 runs probably used 1.8.0, without those fixes.
- The review footer does not show the engine version. The PR branch could pin a different value.
- Hypothesis, not verified: the missing cost line on 1cc738a fits the absence of the "cost on every run" fix in 1.8.0.
- Check before the test: the Actions run log or the workflow file at each run's commit should show the pinned ref. This was not checked.

## 6. Notes for the analyzer and the refuter

Owner direction: Wachiman's analyzer (the stage that proposes findings) and refuter (the stage that tries to falsify them) have a lot of room to improve.

Observed evidence on PR #546. These are observations, not causes:

- **Split-seek defect.** Introduced by commit 0c88e06. It was found only at the re-review after that commit landed (93a721a), not at the first review.
- **Play at end of layout.** Pullfrog reported it on the same code. Wachiman did not report it at 93a721a. Whether it is real is not verified.
- **Webcam seek lead.** Wachiman reported it at consider level at 55ae970. Pullfrog run 1 did not report it. Fixed in 9c07227.
- **Zero findings at 6d2bf6a.** Whether that result is correct has not been checked against the code.

One PR is not enough to say more.

Questions to answer before changing either stage (no conclusions yet):

1. For Play at end of layout: was the handler in the analyzer's input at 93a721a?
2. Did the refuter reject any finding at 93a721a or 6d2bf6a? If so, with what reason?
3. Is the zero-finding result at 6d2bf6a right? This needs a code read.

## 7. The reproduction test (plan, not run)

### 7.1 Questions

- (a) Does re-review cost and time depend on the size of the change?
- (b) Does release 1.9.0 change that?
- (c) How do Wachiman and Pullfrog compare on cost and time for the same commits, under a clean method?

### 7.2 Arms

| Arm | Reviewer | Setting | Note |
|---|---|---|---|
| A | Wachiman, pinned v1.8.0 | pin in `replay/wachi-workflow.yml` | effort high, as in the real runs |
| B | Wachiman, pinned v1.9.0 | pin in `replay/wachi-workflow.yml` | confirm that tag v1.9.0 exists |
| C | Pullfrog, Opus 5.5 | effort set explicitly and checked in the log | recommend high, to match Wachiman (see section 8) |

The arms differ only in the reviewer, or in the Wachiman pin.

### 7.3 Method

0. **No-spend check first.** Read the Actions logs of the #546 runs (to see the pinned ref), the 1cc738a run log, and the 9c07227 review text. This fills the unknowns in section 2.
1. **Create fresh replay repositories.** One fresh repository per run sequence. For Wachiman, use `replay/bench.sh create wachi <name>` and set the pin in `replay/wachi-workflow.yml`. The Pullfrog arm also needs a fresh repository for each repeat of the push sequence (its notes carry across pushes inside one repository, which is part of how it behaves), a minimal PR description, and a check that the log shows `learnings seeded ... existing=no` and the intended `effort:`. The exact Pullfrog command is not in the notes used here; confirm it in `replay/bench.sh`.
2. **Replay the PR as one pull request, pushed in sequence.** Advance the head branch with five pushes, in this order:
   1. 55ae970-equivalent (first review of the whole PR);
   2. 1cc738a-equivalent (rebase onto the new base, no code change; the original run still took 3 m 20 s);
   3. 93a721a-equivalent;
   4. 6d2bf6a-equivalent;
   5. 9c07227-equivalent.
   Wait for each review to finish before the next push, so that each push is a real re-review of the changes since the previous one. Do not use `bench.sh rounds`: it pushes the same SHA to new branches to avoid the engine's "already reviewed this head" check, so it does not exercise re-review.
3. **Controls.**
   - (i) One full review of the final head, in a separate fresh repository, for each Wachiman version and for Pullfrog. This prices one full read against the incremental pushes.
   - (ii) Three repeats of the full push sequence per arm, each in a new repository. Three repeats are needed for the decision rule in 7.4.
4. **Measure per run.** Footer cost (Wachiman) or the `Cost ($)` row (Pullfrog). Turns. Tokens: input, output, cache read, cache write. Workflow wall time, and model time where available. Findings, and the commit each was posted on. For Pullfrog, also the run time from the log.
5. **Decide with the rules in 7.4.**
6. **Report** with the limits in 7.5.

### 7.4 Decision rules (proposed; to be fixed before the first run and adjusted only by the owner)

- **R1, diff size.** For each Wachiman arm, take the median cost of the 802-line-equivalent first push (step 1) and the median cost of the 417-line-equivalent push (step 4). Re-review cost is independent of diff size if the two medians differ by 20% or less.
- **R2, incremental vs full.** If the sum of the five incremental runs is more than the single full review of the final head (control i), then the incremental mode costs more than reading the PR once. Report this as a finding.
- **R3, release 1.9.0.** Release 1.9.0 helps if its median sequence cost is lower than 1.8.0's median by more than the 1.8.0 spread (maximum minus minimum across its three repeats). It must also report the same defects at the same commits. A cheaper run that drops a defect is not counted as a saving.
- **R4, Wachiman vs Pullfrog.** Report medians per sequence for cost and wall time, side by side, and both findings lists per commit. Do not declare a winner on cost alone. A winner needs the findings checked against the code at each commit (limit 7.5).

### 7.5 Cost and time budget

Planning figures. The per-run inputs are measured (Wachiman $0.47 to $0.57 on costed runs; Pullfrog $1.00 to $1.47 on two runs). The $0.50 Wachiman planning figure is an assumption for the uncosted pushes.

| Item | Runs | Planning cost per run | Subtotal |
|---|---|---|---|
| Arm A, Wachiman 1.8.0 (3 repeats x 5 pushes) | 15 | about $0.50 | about $7.50 |
| Arm B, Wachiman 1.9.0 (3 repeats x 5 pushes) | 15 | about $0.50 | about $7.50 |
| Arm C, Pullfrog (3 repeats x 5 pushes) | 15 | $1.00 to $1.47 | $15.00 to $22.05 |
| Control (i), Wachiman full review, one per version | 2 | about $0.50 | about $1.00 |
| Control (i), Pullfrog full review | 1 | $1.00 to $1.47 | $1.00 to $1.47 |
| **Total** | | | **$32.00 to $39.52** |

Suggested cap: $45. Retries and failed runs are not included. The owner must confirm the spend before launch.

Time, if run one after another. A Wachiman sequence took 18 min 36 s in the original run (69 s + 200 s + 305 s + 306 s + 236 s). Arms A and B: 6 sequences, about 112 min. Arm C: Pullfrog runs took 119 s to 201 s each; 3 sequences of 5 runs is about 30 to 50 min. Total about 2.5 to 3 hours. The Pullfrog range is an extrapolation from two runs.

All three arms run in GitHub-hosted workflows (the Wachiman workflow and the Pullfrog GitHub app), so the one-heavy-local-process rule does not apply. If any arm is run locally, run one at a time.

### 7.6 Limits

- One pull request, one repository.
- Wall time includes queue and setup. Pullfrog's time comes from its own log, and the span may differ.
- Costs are self-reported by each tool, not reconciled with billing.
- Replayed commits may get new SHAs and may not be byte-identical to the originals. Check the diff sizes at each push against the table in section 2.1 (2 files / 417 lines for the 6d2bf6a-equivalent push).
- Pullfrog keeps notes per repository. A fresh repository and the `existing=no` check are the only controls for this.
- Effort: Wachiman is high; the Pullfrog effort must be set and logged.
- Verdicts on findings are not verified until the code at each commit is read.

## 8. Open questions for the owner

1. **Spend.** Approve the budget (planned $32 to $40, cap $45) and the order of work: section 7.3 step 0 first (no spend), then the test.
2. **Visibility.** niway-dev/kaipu-record is public (checked 2026-11-07), and the existing replay repositories are public, so public replay repositories are consistent with the previous rounds. Confirm that this is still what you want before any repository is created.
3. **Pullfrog effort.** High (matches Wachiman, recommended) or medium (matches run 1)? Medium would be the cheaper arm.
4. **Repeats.** Three repeats per arm, as R1 requires. Confirm.
5. **Thresholds.** Confirm or change the 20% (R1), the "spread" rule (R3), and the 2 to 3 hour time estimate.
6. **Pinned version.** Confirm that tag v1.9.0 exists, and read the pinned ref of the #546 runs (section 5).
7. **Play at end of layout.** Is it a real defect? This needs a code read at 93a721a. Who does it?
8. **Analyzer and refuter.** Do section 6 questions 1 and 2 before any change to either stage?

## Links

- Source PR: https://github.com/niway-dev/kaipu-record/pull/546
- Pullfrog replay, run 1: https://github.com/niway-dev/kaipu-bench-pullfrog-v3/pull/2
- Pullfrog replay, run 2: https://github.com/niway-dev/kaipu-bench-pullfrog-v3/pull/3
- Sibling snapshot folder: `../2026-11-07-kaipu-record-546-snapshot/` (added by https://github.com/niway-dev/wachiman-benchmarks/pull/17, so it appears here only once that PR merges)
