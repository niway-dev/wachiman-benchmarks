# Wachiman on the replay of pingdotgg/t3code#30556

**One minute.** Wachiman 1.12.0 ran locally on the replay head (one commit, 6 files, +202 lines) and made 2 findings, both "consider". W1 matches the PR's two real bugs (Macroscope T1 and CodeRabbit T4 describe the same defect: a failed merge-request creation leaves the `revert-<sha8>` branch behind and blocks every retry). The merged PR fixed it with a comment that says nearly what W1 says. W2 partly matches two real-minor threads: it names the two cases the revert path gets wrong, a single-commit fast-forward merge (T2) and a merge request that was never merged (T5), but it only asks for a more accurate message, where the bots asked for a behaviour change. The merged PR changed the behaviour in both cases. Wachiman missed T3 (our verdict: wrong) and T6 (our verdict: nit), so it missed nothing worth fixing. No finding is Wachiman-only. W1 adds one point no bot raised: a revert merge request closed without merging keeps its branch too. That point is real but minor and is still in t3code `main`.

Basis: a local rerun at the replay head (`basis: rerun` in the `wachiman-audit` sense), compared with the bot threads in [`bot-threads.md`](bot-threads.md). The bots reviewed the original PR on GitHub. No other reviewer was run for this report.

## Run facts

| | |
| --- | --- |
| Command | `env -u ANTHROPIC_API_KEY WACHIMAN_DIR=<wachiman main-1-12 worktree> wachiman local --repo-dir /tmp/t3bench-30556 --commit HEAD --profile isolated:personal --format json --output wachiman.json` |
| Wachiman version | 1.12.0 (`engine.version` in `wachiman.json`; `wachiman --version` with that `WACHIMAN_DIR` printed 1.12.0) |
| Model | Claude Opus 5.5 via Claude Code 2.1.321, effort high, isolated profile `personal` |
| Range | one commit: `6fc8da0` (replay head = t3code `5586c4ca`) against its parent `87668c5` (replay base = t3code `a185dd92`) |
| Coverage | 6 of 6 files reviewed, 0 skipped, not partial, 1 batch, verify off. The snapshot lacked 2 submodule paths under `.repos/alchemy-effect/submodules/`, outside the diff |
| Wall time | 147 s for the whole command; the review batch itself took 79.0 s and 11 turns |
| Cost | $0.71 estimated at API prices (not a bill: the run used the subscription). Tokens: 12 input, 6,742 output, 212,441 cache read, 65,979 cache write |
| Outputs | [`wachiman.json`](wachiman.json); [`wachiman.md`](wachiman.md) is rendered from that JSON with `jq`, because `wachiman local` has no option to re-render a saved result |

Failed attempts, discarded: two runs failed before reaching the model, both with `git add -A -f failed in .../wachiman-snapshot-*: spawnSync git ETIMEDOUT`.

1. 23:11:44 (-05:00), started at load ~2.2. It failed after 99 s, and load had risen to ~9.5.
2. 23:14:14, started at load ~5.6. It failed after 94 s, at load ~10.

During the second failure, `ps` showed the #33758 thread's Wachiman run in its own snapshot step (`tar -xf .../wachiman-snapshot-*.tar` and `git add -A -f`), with the Avira scan service at ~107% CPU. Two snapshots of a ~557 MB, ~31,800-file tree at once, each scanned file by file, did not fit in the snapshot step's fixed 60 s timeout. The third run was started at 23:19:29, once no other snapshot process was running and load was ~7, and it succeeded. Neither failed run wrote any output or posted anything.

## Posted review

One review with 2 inline comments on the head commit `6fc8da0`. Both lines are in the diff, so the review body holds no finding: https://github.com/niway-dev/t3code-bench-wachi/pull/5#pullrequestreview-5869093539

| W# | path:line | comment |
| --- | --- | --- |
| W1 | `packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:983` | https://github.com/niway-dev/t3code-bench-wachi/pull/5#discussion_r4546281509 |
| W2 | `packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:129` | https://github.com/niway-dev/t3code-bench-wachi/pull/5#discussion_r4546281517 |

## Match table

T# refers to the rows of [`bot-threads.md`](bot-threads.md): T1 Macroscope High, T2 CodeRabbit Major, T3 CodeRabbit Minor, T4 CodeRabbit Major, T5 CodeRabbit Minor, T6 CodeRabbit Major.

| Wachiman finding | severity | bot thread | verdict | judgment basis |
| --- | --- | --- | --- | --- |
| W1: the `revert-<sha8>` name is the same on every attempt, and only a failed revert commit deletes the branch. If opening the merge request fails, or an earlier revert MR was closed without merging, every retry fails at branch creation (`GitLabPullRequestCli.ts:983`) | consider | T1, T4 | **matched** (same defect, same lines 983/989, same fix: delete the branch when creating the merge request fails) | checked in the code at the head and in the merged commit `362ef9a8` |
| W2: the "landed as several commits" error is raised whenever both `merge_commit_sha` and `squash_commit_sha` are empty, which also covers a single-commit fast-forward merge and a merge request that was never merged; the server does not check the state (`GitLabPullRequestCli.ts:129`) | consider | T2, T5 | **partial** (same two cases, but W2 asks for a truthful message; T2 asks to revert the fast-forward commit, T5 asks to block unmerged MRs) | checked in the code at the head and in `362ef9a8` |
| none | | T3: keep GitLab's reason for a failed revert | **bot-only** (our verdict: wrong, disputed) | from the chunk verdict, not rechecked |
| none | | T6: gate revert on creation permission, not `can_merge` | **bot-only** (our verdict: nit, disputed) | checked in the code: the gate is at the head |

### Threads raised after the head

T5 (commit `c5a9985d`) and T6 (`9c4033c0`) were raised on later commits of the PR, on lines that do not exist at the head. In both cases the defect they name is already at the head, so both could have been caught there:

- **T5:** at the head, `revertMergeRequest` never checks that the merge request is merged. It only checks for a commit sha (`GitLabPullRequestCli.ts:963`). W2 says exactly this ("the server does not check the state, only the UI does").
- **T6:** at the head, `revert` is in `MERGE_ACTIONS`, so `viewerCanMerge` gates it (`GitLabPullRequestProvider.ts:55-71`). Wachiman's summary describes the gate ("Permission is gated by GitLab's `can_merge`") but does not flag it. The PR author added a comment defending the choice ("Reverting pushes a branch to the target project, which the same permission covers"), and our chunk verdict is nit (disputed).

No bot thread was raised on code that does not exist at the head in some form.

## Bot findings Wachiman missed

- **T3 (CodeRabbit, Minor): keep GitLab's reason for a failed revert.** Our chunk verdict is wrong (disputed), so missing it costs nothing.
- **T6 (CodeRabbit, Major): gate revert on creation permission, not merge permission.** Our chunk verdict is nit (disputed), and the merged PR keeps `revert` behind `can_merge`. Wachiman saw the gate and treated it as a design choice, which is how the maintainers treated it.

## Partial match, in detail

**W2 against T2 and T5 (checked in the code).** At the head, `decodeRevertTargetJson` sets `commitSha` to `merge_commit_sha ?? squash_commit_sha` (`gitLabMergeRequestJson.ts`), and `revertMergeRequest` raises `GitLabRevertUnavailableError` when it is null (`GitLabPullRequestCli.ts:963-969`). That error's text is "This merge request landed as several commits". Wachiman found the two other cases that reach this error: a fast-forward merge of one commit (T2) and an unmerged merge request (T5). It proposed rewording the message so it is true in every case. The bots proposed fixing the behaviour, and the merged commit `362ef9a8` did:

- it adds `soleCommitSha`, which reads the MR's commits and reverts the only one when there is exactly one (T2);
- it adds `if (!target.merged)` with a new `reason: "not-merged"` and the message "Only a merged merge request can be reverted." (T5).

So Wachiman saw both defects but undersold them: as a fix it would have produced an accurate error, not a working revert of a fast-forward MR. During local development that is still useful, because the developer would have read the two cases and could have chosen the bigger fix. It counts as partial, not matched.

## Wachiman-only findings

No finding is Wachiman-only. W1 contains one sub-claim that no bot raised:

- **A revert MR closed without merging keeps its branch, so the next revert attempt fails at branch creation. Real but minor (checked in the code; GitLab behaviour from its API semantics, not tested).** `remove_source_branch: true` only deletes the source branch when the merge request is merged. If someone closes the revert MR instead, `revert-<sha8>` stays, and a second revert of the same MR posts `repository/branches` with the same name and gets GitLab's "already exists" error. The merged commit `362ef9a8` still builds the name as `` `revert-${commitSha.slice(0, 8)}` `` (line 1446) and does not handle a branch that already exists. t3code `main` at `836b86a5` (2026-11-11) is unchanged on this line; the one later commit to the file (`f3da8ff6`, #30575) is about overview threads. The user can delete the branch in GitLab and retry, so it is a rough edge, not a blocker.

Wrong findings: none found.

## Counts

| | count |
| --- | --- |
| Wachiman findings | 2 (2 consider) |
| Bot reference threads | 6 (5 distinct defects: T1 and T4 are the same defect) |
| Matched | 1 Wachiman finding (W1) ↔ 2 bot threads (T1, T4), both real-bug |
| Partial | 1 Wachiman finding (W2) ↔ 2 bot threads (T2, T5), both real-minor |
| Bot-only | 2 (T3 wrong, T6 nit); both catchable at the head, neither worth fixing |
| Wachiman-only | 0 findings; 1 extra real-but-minor point inside W1, not fixed upstream |

Of the 4 useful bot threads (3 distinct defects), Wachiman matched the real bug and partly matched the other two. It missed only the threads we judged wrong or a nit.

## How it would have helped before the PR

Run on the laptop before pushing, this review takes about 2.5 minutes and $0.71 at API prices. It would have pointed the author at the branch cleanup gap that both bots flagged as High/Major, and at the two cases the merged PR later handled (fast-forward single commit, unmerged MR), although it framed those as a wording problem. Its severities are lower than the bots': W1 is "consider" where Macroscope said High and CodeRabbit said Major, so a developer reading only severities could skip it.

## Limits

- One PR, one local rerun, one Wachiman run (the model is not deterministic; another run could differ).
- The bots reviewed GitHub's PR state; Wachiman reviewed the same tree as a single commit on a laptop. Same code, different setting.
- Judged by Claude Opus 5.5 (`claude-opus-5-5`) in the main session, reading the code at the replay head and the merged commit `362ef9a88a18`. No test was run. T3's verdict and the "fixed before merge" outcomes come from the chunk verdicts in `bot-threads.md`, not rechecked here.
- No verdicts were recorded in Wachiman's history: the run did not use `--history`.
