# Wachiman 1.12.0 local review: replay of pingdotgg/t3code#30556

> Rendered from `wachiman.json` with `jq` (a copy of its fields, no new review). `wachiman local` has no option to re-render a saved result, and a second run would cost another review and could differ.

- Change: commit 6fc8da0 of t3bench-30556 against its parent (87668c5)
- Engine: Wachiman 1.12.0; provider: Claude Opus 5.5 via Claude Code 2.1.321, effort high, profile isolated
- Coverage: 6 of 6 files reviewed, partial: false

## Summary

This adds a GitLab revert action. It reads the merge request, takes the merge commit (or the squash commit as a fallback), creates a `revert-<sha8>` branch from the target branch, reverts the commit onto it, and opens a merge request. If the revert commit fails, the new branch is deleted. Permission is gated by GitLab's `can_merge`. The wiring follows the existing `disable-auto-merge` path, and errors reach the client through the provider's error mapping. Two "consider" notes: the branch name is the same on every attempt, so a failure while opening the merge request (or an earlier revert merge request closed without merging) leaves a branch that makes every retry fail; and the "landed as several commits" message is also shown in cases where it is false.

## Findings

### W1. [consider] A failed revert can block every retry

`packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:983` · topic bug · confidence medium

The branch name `revert-<sha8>` is the same on every attempt (line 970). The cleanup at 974 only deletes the branch when the revert commit fails. If opening the merge request at 983 fails, the branch is left behind with the revert commit on it. The same happens when an earlier revert merge request was closed without merging, because `remove_source_branch` only removes the branch on merge. In both cases the next attempt fails at branch creation (971) with GitLab's "already exists" error, and the app gives no way to clear it. Fix: also delete the branch when opening the merge request fails, or add a suffix to the name when it is already taken.

### W2. [consider] Revert-unavailable message can be wrong

`packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:129` · topic bug · confidence medium

This error is raised whenever both `merge_commit_sha` and `squash_commit_sha` are empty (gitLabMergeRequestJson.ts:609). That also covers a fast-forward merge of a single commit, and a merge request that was never merged: the server does not check the state, only the UI does (PullRequestActionsMenu.tsx:442). In those cases "landed as several commits" is false. Something like "GitLab recorded no single commit for this merge request" would be accurate in every case.

