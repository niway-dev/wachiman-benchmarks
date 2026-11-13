# Opus 5.5 high vs Sonnet 5.5 high on pingdotgg/t3code#30556

**One minute.** Same version (1.12.0), same commit, same flags; only the model changed. Both runs made 2 findings, both "consider". Both found the branch-cleanup defect (T1 and T4, the two real bugs) with the same fix. They differ on the other two useful threads. Opus named the two cases behind T2 (single-commit fast-forward) and T5 (unmerged MR) as a partial match, in finding W2. Sonnet did not raise them as a finding: it noted the unmerged-MR case only in its `contracts` block ("would get the 'landed as several commits' message, which would be misleading, but the UI gates this"), and never mentioned fast-forward. Sonnet's second finding is a test-coverage gap, which no bot raised; it is accurate (checked in code) and minor. Neither run flagged T3 (wrong) or T6 (nit), so neither missed anything worth fixing. Cost: Sonnet $0.354 and 86 s in the model, Opus $0.71 and 79 s.

Summary: Opus found T1, T4 and partly T2, T5. Sonnet found T1, T4 only.

## Reference threads (real-bug or real-minor)

All four were catchable at the head per `report.md` (T5 and T6 were raised on later commits, but the defect is already at the head).

| T# | Verdict | Opus | Sonnet |
| --- | --- | --- | --- |
| T1 | real-bug | found (W1, matched) | found (S1, matched) |
| T2 | real-minor | partial (W2: truthful message, not the revert) | missed |
| T4 | real-bug | found (W1, matched) | found (S1, matched) |
| T5 | real-minor | partial (W2: names the unmerged case, asks only for a message) | missed as a finding; mentioned only in `contracts.failure_mode`, which is not a posted finding |

Not useful: T3 (wrong) and T6 (nit) were missed by both runs.

## Sonnet findings

| S# | Severity | path:line | Claim | Match / verdict | Basis |
| --- | --- | --- | --- | --- | --- |
| S1 | consider | `GitLabPullRequestCli.ts:983` | The `revert-<sha8>` name is fixed and only the `/revert` call cleans up; if the `merge_requests` POST fails, the branch stays and every retry fails at branch creation. Fix: delete the branch on failure, or reuse or suffix the name. | matched T1 and T4. Equals Opus W1 | checked in code (lines 970-991) and against report.md |
| S2 | consider | `GitLabPullRequestCli.test.ts:519` | The tests cover the happy path and a failing `/revert`, but not the `GitLabRevertUnavailableError` path or a failing `merge_requests` POST. | Sonnet-only; real-minor (test gap, no behaviour bug) | checked in code: the head tests are only "reverts a merged merge request..." (469) and "deletes the revert branch when GitLab cannot revert cleanly" (519); neither exercises the null-commit path or a failing final POST |

## Opus-only (not found by Sonnet)

- W2 (partial T2 and T5): the "landed as several commits" error also covers a single-commit fast-forward merge and a never-merged MR, and the server does not check the state. Sonnet did not raise it as a finding. Its `contracts` block names the unmerged case only (basis: from `wachiman.json`).
- Sub-claim inside W1: a revert MR that is closed without merging keeps its branch, so the next revert fails at branch creation. Real-minor per report.md. S1 says "reverting twice in a row hits the same error", but does not name the closed-MR cause. Treat as not found.

## Sonnet-only

- S2: test-coverage gap, real-minor (checked in code). It is not an Opus finding, and it is not tied to any bot thread.

## Wrong findings

None from either run. Opus: none per report.md. Sonnet: S1 and S2 both checked and accurate.

## Limits

- One run per model. The model is not deterministic, so another run could differ, especially on the two partial matches.
- Judged by a Claude Sonnet 5.5 subagent reading the code at the head (`/tmp/t3bench-30556`, HEAD `6fc8da0c`). No test was run, and wachiman was not rerun.
- Opus verdicts, the T3 and T6 verdicts, and the "closed MR keeps branch" claim come from `report.md` and were not rechecked. The latter rests on GitLab API behaviour that was not tested.
- Cost and time figures are from each run's `wachiman.json`/`report.md`, at API prices, not bills.
