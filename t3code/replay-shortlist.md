# Replay shortlist: 10 t3code cases for a Wachiman run

Purpose: pick 10 catalogued defects from `catalogue.md` that are worth replaying into a test repository, so Wachiman reviews the same diff the t3code bots saw and we can check whether it states the golden defect. Six cases are escaped bugs (no bot commented; we replay the introducing PR at its last commit) and four are bot-caught (a bot flagged the defect before merge; we replay the PR at the commit the bot commented on). Every PR merged into `main`, has at most 40 files and 3000 added lines, and the buggy lines were checked at the replay head in the local clone (`/tmp/t3code-mine/repo`). Severity for bot-caught rows is our own rating (the catalogue has none for them); the bot's own label is in the section.

Shas are full 40-char. `base` is the parent of the PR's first commit, which equals `baseRefOid` except where noted. All checks were `gh` reads and `git` read commands.

| # | id | kind | PR to replay | base | head | files/+lines | sev | class | caught by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | checkpoint-ignore-check-drops-untracked | escaped | #21315 | 220eb73524ca7882d53b6a12c824ccbcd97ad279 | 10ca8a6c7aba11bf932cb55e3aab0005c10a52e8 | 2 / +169 | 4 | data integrity (git) | none |
| 2 | git-timeout-no-force-kill-permit-leak | escaped | #22107 | 3117be980bebd268b9cc6dc8b8609547f7ae3a15 | 8481fae25c8c6463e5044dc8fe6f493cef0afdee | 3 / +638 | 4 | resource leak, race (server/git) | none |
| 3 | detach-session-strands-pending-approval | escaped | #19355 | adb04202b25c1c45255e76be9f03f0b346b9c5c4 | f2248534a197b12d1aa1485c9d49a333abe3215c | 7 / +448 | 4 | state machine (providers) | none |
| 4 | provider-env-duplicate-row-deletes-stored-secret | escaped | #18505 | e688034b5f5505f92fcf1d78ba853c9c0107f9f1 (catalogue sha was wrong) | 1e110495aff3abc8e31156988bc7cca27091ed04 | 15 / +658 | 4 | data integrity (settings, web+server) | none |
| 5 | mcp-csrf-bound-to-session-id-breaks-hosted-approval | escaped | #33632 | bbdc7dca320ee4fbc7131498aaffef2fa1eb3d41 | a8edf4951b29c9353b5ee0abe637e215d4995869 | 24 / +666 | 4 | security, cross-file contract (auth) | none |
| 6 | ssh-stale-pid-wrong-process | escaped | #19432 | 8414d168191599dec08588080d0b77506c849424 | 4572c6bec9b7a12a518d1361b1474a7539ab6b3b | 2 / +488 | 4 | race/ordering, process identity (desktop ssh) | none |
| 7 | gitlab-revert-branch-left-behind | bot-caught | #30556 | a185dd924889cd7f925760431a9f29b973a35e2f (catalogue sha was wrong) | 5586c4cad0af8abf92eb792e9ce01fe022af39df (catalogue head was the final commit, bug already fixed) | 6 / +202 | 3 | error handling, cleanup (forge) | Macroscope (High) and CodeRabbit |
| 8 | mobile-preview-fork-trusted-script-overwritable | bot-caught | #33618 | bbdc7dca320ee4fbc7131498aaffef2fa1eb3d41 | 19e8c6c80e7de66a2935e7b20b2367331916173d (catalogue head was the last commit; bug is in both) | 5 / +747 | 4 | security (mobile CI) | Macroscope (Critical), ignored at merge |
| 9 | thread-cache-save-resurrects-removed-thread | bot-caught | #33503 | dc7270581800518b9d7d4db6c8e13852067c8c2d (catalogue sha was wrong) | 4ec957c8ab22fb43451d24e0b29cecb728c523ba | 6 / +338 | 3 | race/ordering (web cache) | Macroscope (High), fixed in 0b7b2995 |
| 10 | codex-notification-drops-read-reset | bot-caught | #27791 | 935818e422f9b58c46e14d70f4ef386fa3575105 (catalogue sha was wrong) | ff265e82d4cab6d511585b1f8ee2334b8545ebf0 | 6 / +655 | 4 | state machine, ordering (providers) | Macroscope (High), fixed later in the PR |

Area mix: server/git (1, 2), providers (3, 10), settings (4), auth security (5), desktop ssh (6), forge (7), mobile CI (8), web (9). The catalogue has no sev >= 4 escaped bug with a small PR in mobile or web UI, so those two areas are covered only by bot-caught rows.

## 1. checkpoint-ignore-check-drops-untracked (escaped, PR #21315)

- Golden: Checkpoint capture decides "the workspace is ignored" by running `git check-ignore --no-index` on `.` and treating an empty result as ignored; a blank CRLF or spaces-only line in any ignore source makes a normal workspace look ignored, so capture stages with `git add -u`, leaves untracked files out, and a later restore deletes them.
- Where: `apps/server/src/vcs/GitVcsDriver.ts:1012` (`workspaceIgnored = (yield* filterIgnoredPaths(input.cwd, ["."])).length === 0`), consumed at `:1081` (`workspaceIgnored ? "-u" : "-A"`); the probe itself is at `:706`.
- Fix PR: #32374 (replaces the probe with `rev-parse --show-prefix` and drops `check-ignore`).
- Why valuable: silent data loss on restore from a 169-line perf PR whose title ("8 git processes instead of 10") hides the behavior change. Needs git semantics knowledge, not just reading the hunk.
- Verified: base is an ancestor of head; `git diff base head` = 2 files, +169 -9; the lines above exist at head; the fix diff removes exactly this probe.

## 2. git-timeout-no-force-kill-permit-leak (escaped, PR #22107)

- Golden: Git commands run with a timeout but the driver passes `forceKillAfter: input.forceKillAfterMs`, which is undefined for almost every caller, so a git process that ignores SIGTERM is never killed, keeps one of the 8 shared process permits, and eventually queues every later git call.
- Where: `apps/server/src/vcs/GitVcsDriverCore.ts:969` (`forceKillAfter: input.forceKillAfterMs`), option declared at `:176`; only one call site sets it (`:1292`).
- Fix PR: #26601 (hard-codes `forceKillAfter: "1 second"` and removes the option).
- Why valuable: resource leak that only shows under a hung git (lock contention, network); a 638-line PR where most lines are tests, so the one-line gap is easy to miss.
- Verified: base is an ancestor of head; 3 files, +638 -48; line 969 present at head; fix diff changes exactly that line.

## 3. detach-session-strands-pending-approval (escaped, PR #19355)

- Golden: When a one-thread provider session is detached (branch switch, restart, disconnect) while an approval is pending, the detached thread is removed from `attachedThreadIds` before release, so the release loop skips it and its pending runtime request is never cancelled; Approve, Decline and Settle then all fail until the thread is archived.
- Where: `apps/server/src/orchestration-v2/ProviderSessionManager.ts:687` (`for (const threadId of input.entry.attachedThreadIds)` in `writeReleasedRuntimeRequestEvents`); the correct pattern already exists at `:800`, which adds `detachedThreadId` to the set.
- Fix PR: #33535 (shared `releasedThreadIds` helper used by both loops).
- Why valuable: a state-machine miss with a visible sibling that handles the case correctly; a reviewer that compares the two loops finds it.
- Verified: base equals the first commit's parent; 7 files, +448 -7; lines 687 and 800 present at head; fix diff matches.

## 4. provider-env-duplicate-row-deletes-stored-secret (escaped, PR #18505)

- Golden: Environment-variable rows with the same name share one secret slot, but the save logic queues `remove-secret` for any non-sensitive or empty row even when a redacted row of the same name still keeps that slot, so the stored secret is deleted and cannot be recovered.
- Where: `apps/server/src/serverSettings.ts:952-953` (non-sensitive row pushes `remove-secret` unconditionally) and `:964-966` (empty value pushes it again), at head `1e110495`.
- Fix PR: #31337 (tracks `keptSecretNames` and filters removals); three further duplicate-row defects in that PR were caught by CodeRabbit, so this is the root cause they came from.
- Why valuable: data integrity in a refactor PR (settings plus web inputs) where the rule is about row identity across the whole save; the later PR shows how many variants hide behind it.
- Verified: catalogue base `19bef8c1...` is NOT an ancestor of head (it is main at merge time); replaced with the parent of the first commit. With the new base: 15 files, +658 -460. Buggy lines present at head. Intro PR confidence: high (the catalogue lists #18505 without a caveat; Macroscope's flag at #10054 is a different PR).

## 5. mcp-csrf-bound-to-session-id-breaks-hosted-approval (escaped, PR #33632)

- Golden: The MCP approval CSRF token is derived from `session.sessionId`, but the hosted app.t3.codes client mints a fresh relay credential (a new session) per call, so the approval POST arrives under a different session id and is refused; DPoP sessions must be bound to the proof-key thumbprint instead.
- Where: `apps/server/src/auth/McpOAuth.ts:310` (`csrfToken = (sessionId, authorization)`) and `:416` (`csrfToken(session.sessionId, authorization)`); verification at `:474`.
- Fix PR: #33645 (human fix next day; uses `dpop:<thumbprint>` as the holder).
- Why valuable: security-adjacent cross-file contract (server token binding vs the client runtime in `packages/client-runtime/.../connectMcpApproval.ts`). A reviewer must reason about how the client authenticates, not only the server hunk.
- Verified: base is an ancestor of head and equals the first commit's parent; 24 files, +666 -707; lines present at head; fix diff changes exactly these call sites.

## 6. ssh-stale-pid-wrong-process (escaped, PR #19432)

- Golden: The remote launch and stop scripts trust `kill -0 "$REMOTE_PID"` on a saved pid file, so after pid reuse (or a zombie, or a thread id) reconnect waits 60 s on an unrelated process and disconnect sends SIGTERM to it; the script must check that the pid is the managed `serve --host 127.0.0.1 --port N` command.
- Where: `packages/ssh/src/tunnel.ts:679-680` (launch path) and `:780-781` (stop path); pid wait loop at `:618`.
- Fix PR: #26963 (adds `managed_server_running`, which checks `ps -o args=`).
- Why valuable: desktop remote-connection area; a shell script embedded in TypeScript, the kind of file reviewers skim. The test file in the PR even asserts the `kill -0` strings, which can mislead.
- Verified: base equals the first commit's parent and `baseRefOid`; 2 files, +488 -46; lines present at head. Intro PR confidence: medium (as in the catalogue); the lines were first added by #19432 as far as the fix's blame goes.

## 7. gitlab-revert-branch-left-behind (bot-caught, PR #30556)

- Golden: `revertMergeRequest` creates the `revert-<sha8>` branch, cleans it up only if the revert-commit write fails, and does not clean it up when the final `write("merge_requests", ...)` fails, so a retry fails creating the already-existing branch and the user cannot finish the revert.
- Where: `packages/source-control-gitlab/src/server/GitLabPullRequestCli.ts:983` (the unprotected merge request write; branch created at `:970`, cleanup only on the revert write at `:972-980`), at head `5586c4ca`.
- Fix PR: same PR; the last commit wraps both writes so the cleanup covers the merge request write (checked in the final file).
- Caught by: Macroscope (High, comment 4462816788 on `5586c4ca`, line 983) and CodeRabbit (same commit, lines 982 and 989).
- Why valuable: classic error-handling/cleanup defect with two bots agreeing, and a half-fixed version in the diff (cleanup exists for one step only), which tests whether a reviewer reads the whole sequence.
- Verified: bot commit is the PR's first commit; base is its parent. The catalogue's base `a03d9bce...` is not an ancestor and its head `2824155f...` is the final commit where the bug is already fixed, so both were replaced. Diff base..head = 6 files, +202.

## 8. mobile-preview-fork-trusted-script-overwritable (bot-caught, PR #33618)

- Golden: In the fork-preview workflow the comment script is checked out into `.trusted/` inside the same job workspace where fork code runs (`pnpm install`, Expo config, Gradle), so fork code can overwrite `.trusted/.github/scripts/mobile-preview-comment.cjs` before the Comment step runs it with `GH_TOKEN` and `pull-requests: write`; comment from a separate job that never runs fork code.
- Where: `.github/workflows/mobile-eas-preview-fork.yml:229` (`run: node .trusted/.github/scripts/mobile-preview-comment.cjs`), with the checkout at `:84-89`, at head `19e8c6c8`.
- Fix PR: none; the thread was unresolved at merge and line 229 is unchanged in the final commit `632bc2f2`.
- Caught by: Macroscope (Critical, comment 4520050593 on `19e8c6c8`); an earlier Critical on the same file at `0da5c399` line 89 is the install-step variant.
- Why valuable: CI security in a YAML workflow, rated Critical, never fixed; tests whether a reviewer treats workflows as code and understands `pull_request_target` trust boundaries.
- Verified: base is an ancestor of head; 5 files, +747 -7; line 229 present at head. Replay head differs from the catalogue's (last commit), which contains the same bug.

## 9. thread-cache-save-resurrects-removed-thread (bot-caught, PR #33503)

- Golden: `saveThread` encodes the snapshot (a step that yields) and then writes it, so a `removeThread` or environment clear that runs in between deletes the record and the resumed save writes the stale snapshot back, restoring a deleted thread's contents in the cache.
- Where: `apps/web/src/connection/storage.ts:955-963` (`encodeStoredThreadSnapshot` then `writeDatabaseValue(...)`); `removeThread` at `:1039`, at head `4ec957c8`.
- Fix PR: same PR, second commit `0b7b2995` (Macroscope marked the thread "no longer relevant as of" it).
- Caught by: Macroscope (High, comment 4516815976 on `4ec957c8`, line 963).
- Why valuable: web race/ordering bug that needs the yield point in `encode` to be noticed; fixed before merge, so it measures catching, not just reading.
- Verified: bot commit is the PR's first commit; catalogue base `6b02cbff...` is not an ancestor, replaced with its parent. Diff = 6 files, +338 -44. Lines present at head.

## 10. codex-notification-drops-read-reset (bot-caught, PR #27791)

- Golden: When a quota notification updates an exhausted window without `resetsAt` while the first `account/rateLimits/read` is pending, `laterReport` returns the notification because it requires `notified.resetsAt != null`, dropping the read's reset timestamp; `codexUsageLimitResetAt` then returns null and the terminal never auto-recovers.
- Where: `apps/server/src/provider/codexUsageLimits.ts:261-272` (`laterReport`, condition at `:268`), used at `:208-216`, at head `ff265e82`.
- Fix PR: same PR; the final head `bb863312` no longer contains `laterReport`.
- Caught by: Macroscope (High, comment on `ff265e82`, `codexUsageLimits.ts:266-273`); the same PR has two further Macroscope Highs (removed windows kept, wrong-plan reset).
- Why valuable: providers state machine where correctness depends on the order of a read and a notification; a nullable-field condition is easy to approve.
- Verified: catalogue base `41443e57...` is main at merge time (diff to head = 2111 files), so it was replaced by the parent of the first commit; base..head = 6 files, +655 -73 (2 commits). The line exists at head.

## Rejected near-misses

- git-push-default-branch-into-itself (#8228, 2 files, +154, sev 4): valid shas and strong, but it adds a third git/server case; first alternate if one case fails. Not re-checked at head.
- usage-scan-cache-single-string-oom (#15149, 9 files, +579, sev 4): valid shas, but the defect is a memory bound that needs a size measurement to prove, so a pass/fail golden is weak.
- managed-policy-observability-ignored (#27197): 193 files, +9048; too big.
- claude-query-exit-before-turn-attach (#12598): 56 files, +7214 and low-medium intro confidence; too big.
- effect-worker-title-generation-starvation and codex-compaction-reinject-loop (#2829): the introducing PR is a 1912-file rewrite; the catalogue already says no replay.
- composer-queue-send-drops-edits-during-upload (#31535): targets the stack branch `maria/redesign/6-workspace-panes`, not `main`.
- codex-stalled-retry-fails-recovered-turn (#33130, High): the bot's commit `1521afec` is not among the PR's commits and not an ancestor of its last commit (rewritten by a force push), and the catalogue base is not an ancestor of it, so the replay state cannot be rebuilt reliably.
- steer-restart-strands-delegated-wake (#15323): 29 files, +2494 fits the size limit, but intro confidence is low and the bug was not verified at head.
