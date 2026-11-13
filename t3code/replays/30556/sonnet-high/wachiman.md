# Wachiman 1.12.0 local review (Sonnet 5.5 high): replay of pingdotgg/t3code#30556

> Rendered from `wachiman.json` with `jq` (a copy of its fields, no new review). `wachiman local` has no option to re-render a saved result.

- Change: commit 6fc8da0 of t3bench-30556 against its parent (87668c5)
- Engine: Wachiman 1.12.0; provider: Claude Sonnet 5.5 via Claude Code 2.1.321, model claude-sonnet-5-5, effort high, profile isolated
- Coverage: 6 of 6 files reviewed, partial: false
- Execution: 18 turns, 86.117 s in the model, $0.354 estimated at API prices (not a bill)

## Summary

The GitLab revert is a sound four-step REST flow. It is gated on merge permission and on merged state in both clients, and it cleans up the branch when the revert itself fails. One gap: if opening the revert MR fails, the fixed-name branch is left behind and blocks every retry. The new tests also skip the null-commit error path and the failing MR creation.

## Findings

### W1. [consider] Failed MR creation leaves the revert branch behind, and the fixed branch name blocks every retry

`packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:983` · topic bug · confidence high

The branch is named `revert-<first 8 of sha>` (line 970), so it is the same on every attempt. Only the `/revert` call has cleanup (lines 972-982). If the revert commit is pushed and the `merge_requests` POST at line 983 then fails (permissions, an MR already open for that source branch, a network error, a timeout), the branch with the revert commit stays on the project. The next click then fails at line 971 because the branch already exists, with no hint why. The user has to delete the branch by hand. Reverting twice in a row hits the same error. Either also delete the branch when the MR creation fails, or reuse or suffix the branch name so a retry can proceed. The cleanup comment at line 973 already treats an orphan branch as unwanted.

### W2. [consider] The no-commit error path and a failing MR creation are not covered

`packages/source-control-gitlab/src/server/GitLabPullRequestCli.test.ts:519` · topic tests · confidence medium

The two new tests cover the happy path and a failing `/revert` call. The `GitLabRevertUnavailableError` path (`merge_commit_sha` and `squash_commit_sha` both null, GitLabPullRequestCli.ts:963) has no test, and neither does a failure at the final `merge_requests` POST. The first of these is a new user-visible error and the second is where the orphan-branch behavior comes from. A row in the existing revert test, or a short second case, would settle both.

