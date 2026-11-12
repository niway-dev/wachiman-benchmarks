# Reference bot threads: pingdotgg/t3code#30556

Original PR: https://github.com/pingdotgg/t3code/pull/30556 (feat(gitlab): revert a merged merge request), merged 2026-11-11.

Replay: base `a185dd924889cd7f925760431a9f29b973a35e2f`, head `5586c4cad0af8abf92eb792e9ce01fe022af39df`.

These are the CodeRabbit (`coderabbitai`) and Macroscope (`macroscopeapp`) threads raised on the replay head or on a later commit of the PR: 6 of the PR's 6 threads. They are the reference that Wachiman's findings on the replay are compared with. "Claim" is the thread's own headline. "Our verdict" comes from [`batches/2026-11-11/chunk-03.md`](../../batches/2026-11-11/chunk-03.md) (Track A, row T#), as verdict (outcome). The chunk row says whether that verdict was checked in code or judged from the thread text.

| T# | bot | bot severity | path:line | commit | claim | our verdict | url |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | macroscopeapp | High | `packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:983` | 5586c4ca | When the final `write("merge_requests", ...)` fails, `revertMergeRequest` leaves the `revert-${target.commitSha.slice(0, 8)}` branch behind. | real-bug (fixed-before-merge) | [thread](https://github.com/pingdotgg/t3code/pull/30556#discussion_r4462816788) |
| 2 | coderabbitai | Major | `packages/source-control-gitlab/src/server/gitLabMergeRequestJson.ts:897` | 5586c4ca | Support single-commit fast-forward merges. | real-minor (fixed-before-merge) | [thread](https://github.com/pingdotgg/t3code/pull/30556#discussion_r4462848873) |
| 3 | coderabbitai | Minor | `packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:982` | 5586c4ca | Keep GitLab's reason for a failed revert. | wrong (disputed) | [thread](https://github.com/pingdotgg/t3code/pull/30556#discussion_r4462848876) |
| 4 | coderabbitai | Major | `packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:989` | 5586c4ca | Clean up the branch if merge-request creation fails. | real-bug (fixed-before-merge) | [thread](https://github.com/pingdotgg/t3code/pull/30556#discussion_r4462848881) |
| 5 | coderabbitai | Minor | `packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:1437` | c5a9985d | Block revert for merge requests that are not merged. | real-minor (fixed-before-merge) | [thread](https://github.com/pingdotgg/t3code/pull/30556#discussion_r4463215390) |
| 6 | coderabbitai | Major | `packages/source-control-gitlab/src/shared/definition.ts:63` | 9c4033c0 | Gate revert on creation permissions, not merge permission. | nit (disputed) | [thread](https://github.com/pingdotgg/t3code/pull/30556#discussion_r4534509855) |
