# New cases: notes

One section per admitted case. Reviewed commit is the squash commit of the introducing PR on main; line numbers are in that commit.

## checkpoint-ignore-probe-drops-untracked-14892

- Intro PR: https://github.com/pingdotgg/t3code/pull/14892 (squash 6d266ea683ecc46c17aed5d68a093221be093862, 4 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/32374
- Class: cross-file contract (git check-ignore semantics vs capture staging mode)
- Location: apps/server/src/vcs/GitVcsDriver.ts:969; other side: apps/server/src/vcs/GitVcsDriver.ts:1038 (consumer `workspaceIgnored ? "-u" : "-A"`; probe helper filterIgnoredPaths at :700-712 runs `check-ignore --no-index`)
- Added-line evidence: added apps/server/src/vcs/GitVcsDriver.ts:969: const workspaceIgnored = (yield* filterIgnoredPaths(input.cwd, ["."])).length === 0; and added :1038: workspaceIgnored ? "-u" : "-A", (the check-ignore helper itself at :708 is pre-existing; this PR adds the "." probe and its consumer). Candidate re-check: PASSES (4 files). Bots on intro: summary comments only.
- Fix summary: Fix replaces the `.` probe with a probe of the workspace's directory name (`../<dir>`) obtained from `rev-parse --show-prefix`, and treats the working-tree root as never ignored. Only GitVcsDriver.ts source changed (+ tests).

## delegated-followup-self-queued-run-17696

- Intro PR: https://github.com/pingdotgg/t3code/pull/17696 (squash c572cb71d2711d8cdb4ff7e0ba88af5e9a23aa81, 14 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/32504
- Class: state machine (delegated task linkage)
- Location: apps/server/src/orchestration-v2/Orchestrator.ts:4567; other side: apps/server/src/mcp/OrchestratorMcpService.ts:1282 (task result run chosen by `run.delegatedTaskId === task.id`)
- Added-line evidence: added Orchestrator.ts:4567-4568: const continuedTaskId = projection.runs.find( (run) => run.id === command.restartContinuationOfRunId, ... omission: no branch for a self-queued run (senderThreadId === threadId). Adjacent bot comments exist on this PR (Macroscope High at Orchestrator.ts:10066 about per-task finalization with another follow-up active, CodeRabbit on client relationship edges) but not on the self-queued linkage.
- Fix summary: Fix links a self-queued run (`command.senderThreadId === command.threadId && isActiveRun(run)`) to the active run's task, and adds `delegatedTaskResultRun` so result selection skips queued/held runs the task no longer waits on.

## local-refresh-writes-null-remote-21046

- Intro PR: https://github.com/pingdotgg/t3code/pull/21046 (squash e677e9799df44fd33d96890cb80dc0ee64d1221d, 4 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/33263
- Class: state machine (cache part semantics)
- Location: apps/server/src/vcs/VcsStatusBroadcaster.ts:497; other side: apps/server/src/vcs/VcsStatusBroadcaster.ts:346 (reader `mergeGitStatusParts(cached.local.value, cached.remote.value)`) and :533
- Added-line evidence: added VcsStatusBroadcaster.ts:497: { branch: local.refName, fingerprint: fingerprintStatusPart(null), value: null }, inside the localOnly branch (:487-497). Bots on intro: Macroscope/CodeRabbit comments on other defects (tag/branch name, discarded cache, mixed cache snapshot).
- Fix summary: Fix drops the null-remote write and the remote invalidation from the localOnly path; it only refreshes local status and merges existing cached parts.

## usage-resume-agent-cancelled-on-restart-29838

- Intro PR: https://github.com/pingdotgg/t3code/pull/29838 (squash 90f0158e60b08946bcaae1df07109a893e7c36af, 4 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/31292
- Class: cross-file contract (message origin vs startup recovery filter)
- Location: apps/server/src/orchestration-v2/UsageLimitRecoveryWorker.ts:76; other side: apps/server/src/orchestration-v2/ProviderRuntimeRecoveryService.ts:369 (`message.createdBy === "user"` retryable filter)
- Added-line evidence: added UsageLimitRecoveryWorker.ts:76: createdBy: "agent", (changed from "user"). Fix PR #31292 body names this PR as the regression source. Bots on intro: summary/approval only.
- Fix summary: Fix tags the resume run with `usageLimitContinuationOfRunId`, and startup recovery re-arms the thread's limitRecovery with a fresh requestId when it cancels a never-started tagged resume, hiding its duplicate prompt.

## compaction-steer-client-server-split-15631

- Intro PR: https://github.com/pingdotgg/t3code/pull/15631 (squash fc21184afbb85604660f459ca43bbbe55ad020e4, 6 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/24138
- Class: cross-file contract (client steering gate vs server steer refusal)
- Location: apps/web/src/components/ChatView.tsx:2526 (also apps/mobile/src/state/use-thread-composer-state.ts:340); other side: apps/server/src/orchestration-v2/Orchestrator.ts:3941 (server refuses steering only for `/compact` text)
- Added-line evidence: added ChatView.tsx:2526: const compactionRunning = serverVisibleTurnItems.some( ... item.type === "compaction" ... item.status === "running" and added use-thread-composer-state.ts:340: item.runId === activeRunId && item.type === "compaction" && item.status === "running", (returns isCompacting true). Bots on intro: summary/approval only.
- Fix summary: Fix adds a provider capability `activeSteeringDuringCompaction` (Codex true) and a shared `compactionBlocksSteering` helper so clients block steering only for explicit /compact or providers that cannot steer through compaction.

## settle-after-run-dropped-by-new-run-17145

- Intro PR: https://github.com/pingdotgg/t3code/pull/17145 (squash 37eaf5d293ef83ce86d2ce9a1583792696c82bbc, 7 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/31815
- Class: race (settle once vs later run)
- Location: apps/server/src/orchestration-v2/ThreadManagementService.ts:761; other side: apps/server/src/orchestration-v2/Orchestrator.ts:2568 (thread.settle handler refusing when a run is active or queued)
- Added-line evidence: added ThreadManagementService.ts:761: type: "thread.settle", inside new settleAfterRun (dispatch at :760-763 with no retry or follow-up wait). Bots on intro: CodeRabbit Major on handler structure only (fixed).
- Fix summary: Fix makes settleAfterRun wait for automatic follow-up runs (notification/delegated completion), retry the settle after them, give up when a user turn arrives, and adds `expectedLatestRunId` so the server refuses a stale settle.

## live-buffer-charged-before-coalescing-9715

- Intro PR: https://github.com/pingdotgg/t3code/pull/9715 (squash 108f295cc3672716c3cb8291ce487846df5ce098, 6 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/16317
- Class: ordering (budget charge vs coalesce)
- Location: apps/server/src/orchestration/ThreadLiveEventCoalescer.ts:170; other side: apps/server/src/orchestration/ThreadLiveEventCoalescer.ts:129 (flush coalesces via budget.replace after all were retained)
- Added-line evidence: added ThreadLiveEventCoalescer.ts:170: yield* budget.retain(input.event).pipe( followed by :171 Effect.tap((item) => Effect.sync(() => pendingUpdates.push(item))). Bots on intro: Macroscope approvability summary only; author note comment (Claude on behalf of Theo) reviewing the limits.
- Fix summary: Fix replaces the previously retained update for the same key via `budget.replace` at insertion time (latestUpdates map), so superseded updates never accumulate against the budget.

## goal-command-notice-not-steered-29909

- Intro PR: https://github.com/pingdotgg/t3code/pull/29909 (squash e2bb9e63e129001aa37fa1f9f51cb334d1a3db42, 4 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/33268
- Class: state machine (notification routing into active run)
- Location: apps/server/src/orchestration-v2/Orchestrator.ts:5745; other side: n/a (single-file routing condition)
- Added-line evidence: added Orchestrator.ts:5745: : command.notification?.source.kind === "delegated_task" (omission: no handling of source.kind === "command"). Weaker case: could be read as a feature gap rather than a regression. CodeRabbit comment on intro concerns attachment-bearing notices, not this.
- Fix summary: Fix adds `commandNotice` (server-created command notification) to the steering condition, only when the Codex goal is active.

## auto-resume-arms-archived-parent-subagents-27951

- Intro PR: https://github.com/pingdotgg/t3code/pull/27951 (squash 95414cf1ad5af17ddb6e710218579a23ceee4bfa, 2 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/30363
- Class: state machine (thread lifecycle)
- Location: apps/server/src/orchestration-v2/ProjectionStore.ts:3982; other side: n/a (single SQL predicate)
- Added-line evidence: added ProjectionStore.ts:3982: AND json_extract(parent.payload_json, '$.settledOverride') = 'settled' (omission: no `$.archivedAt IS NOT NULL` or `parent.deleted_at IS NOT NULL`). No bot comments at all on this PR.
- Fix summary: Fix extends the same NOT EXISTS predicate with archivedAt IS NOT NULL OR parent.deleted_at IS NOT NULL.

## ssh-prompt-queue-never-settles-25239

- Intro PR: https://github.com/pingdotgg/t3code/pull/25239 (squash 02f4ba75a20f28a5383bdb95a1c250e6892556e9, 17 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/34192
- Class: cross-file contract (desktop main process vs renderer prompt lifetime)
- Location: apps/web/src/components/desktop/SshPasswordPromptDialog.tsx:52; other side: apps/desktop/src/ssh/DesktopSshPasswordPrompts.ts:426 (main process sends the prompt, owns its lifetime, sends no settled event)
- Added-line evidence: added SshPasswordPromptDialog.tsx:52: setPromptQueue([...promptQueue, request]); inside new startSshPasswordPromptQueue (queue has no removal path for main-side expiry). CodeRabbit comment on intro concerns a U+00A0 in useLiveRegion.ts.
- Fix summary: Fix adds a `desktop:ssh-password-prompt-settled` IPC channel (main, preload, contract) fired when the request ends however it ends, and the renderer removes that request from its queue.

## notification-key-ignores-new-request-24760

- Intro PR: https://github.com/pingdotgg/t3code/pull/24760 (squash 242d00cd34534e7a93cb6f6b02cf4652bdd1210e, 14 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/32719
- Class: state machine (notification dedupe key)
- Location: apps/web/src/components/ThreadNotificationCoordinator.logic.ts:46; other side: apps/web/src/components/ThreadNotificationCoordinator.tsx:256 (key built as `${runId}:${status}`; this line pre-exists, only the logic.ts file is new)
- Added-line evidence: added ThreadNotificationCoordinator.logic.ts:46: if (next.attention && next.attention !== prior.attention) { (new file in this PR). Bots on intro: CodeRabbit on PullRequestSyncReactor/ThreadSettlementService only.
- Fix summary: Fix adds the pending request's id to the observation and tracks seen attention keys per thread (`attend`), so a new request id inside the same run notifies.

## restart-send-to-ended-run-errors-16926

- Intro PR: https://github.com/pingdotgg/t3code/pull/16926 (squash 10f7db7e38ea353c5b2b6c324c155cb6a6bedf72, 2 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/32899
- Class: state machine (dispatch mode vs run state)
- Location: apps/server/src/orchestration-v2/Orchestrator.ts:4816; other side: n/a (single-file dispatch logic)
- Added-line evidence: added Orchestrator.ts:4816-4826: comment at :4819 "an explicit steer or restart still fails below." and the guard `command.deliveryIntent === "auto" && (dispatchMode.type === "steer_active" || dispatchMode.type === "restart_active")`. Weak case: the added comment states the behaviour as intended, so a reviewer may see a design choice. Bots on intro: approval summaries only.
- Fix summary: Fix widens the stale-target check to restart_active (non-active target) and turns an explicit restart that Stop reached into start_immediately.

## model-refresh-keeps-latest-version-cache-33511

- Intro PR: https://github.com/pingdotgg/t3code/pull/33511 (squash d0f7a509cc9143bf7511800d2f28b7d87e6ef1ec, 15 files, single parent)
- Fix PR: https://github.com/pingdotgg/t3code/pull/33515
- Class: cross-file contract (cache coherence between model manifest and CLI latest-version cache)
- Location: apps/server/src/provider/ProviderRegistry.ts:1091; other side: packages/provider-core/src/server/ProviderLatestVersions.ts:11 (FOUND_TTL one hour, no invalidateAll)
- Added-line evidence: added ProviderRegistry.ts:1090-1091 (refreshModelCatalog: if probedManifestUpdatedAt === updatedAt return; yield* refreshAll();) with the omission of any latest-version invalidation. Weakest case: closer to a missing step than a regression. Macroscope High on this PR is at ProviderRegistry.ts:1082 about probedManifestUpdatedAt advancing on a failed refresh, a different defect.
- Fix summary: Fix adds `invalidateAll` to ProviderLatestVersions and calls it before refreshAll when the manifest changed.

## Checked candidates: results

- #14892: admitted (above). 4 files, adds the `"."` probe call and the `-u`/`-A` consumer.
- #19291: REJECTED, criterion 2 (46 changed files, over the 40 limit). Not recorded in the TSV (valid=no rows are listed only here). Its `DEFAULT_BACKEND_TERMINATE_GRACE` change was not examined further.

## Rejected candidates

- #22790 (fix #22425, held queue after other provider): criterion 4. The defective `usageLimitHoldsQueue` lines are not in its diff; they were added by #21314, which has a Macroscope inline comment on the same guard (criterion 3).
- #21314 (same defect, fix #22425 / #33591): criterion 3 (Macroscope High on `usageLimitHoldsQueue`) and, for #33591, criterion 4 (the `command.modelSelection ?? projection.thread.modelSelection` line is pre-existing).
- #29450 (fix #27953, closed PR watch): criterion 3. CodeRabbit commented on PullRequestWatchReactor.ts:498-499 about the activity/detail read handling.
- #30308 (fix #30139, iOS nativeEventCount): criterion 3. CodeRabbit confirmed a bug at T3ComposerEditorView.swift:671 on the same reset/event-count logic.
- #21460 (fix #32434, form.created session): criterion 4. `sessionOfEvent` is pre-existing; the diff only adds a call.
- #19340 (fix #23356, login shell probe retry): criterion 4. The 5 s timeout and missing retry are pre-existing; the diff adds `__MISE_DIFF` handling.
- #8228 (fix #33695, push default branch): criterion 4. The default-branch detection (origin/HEAD symref) is not in the diff.
- #13450 (fix #33440, citation send): criterion 3. CodeRabbit Major on `finalFocus` restore in AssistantCitationChip.tsx:185, the same restore-focus mechanism.
- #16002 (fix #21676, cancelled background task): criterion 3 (many Macroscope/CodeRabbit High/Major threads on the cancel and stop paths); defect line unclear.
- #15323 (fix #33469), #25426 (fix #32902), #24972 (fix #29601), #13689 (fix #29688): criterion 3 or 4 unclear. Heavy bot comments in the same area, or the defective line is pre-existing or moved (#24972: `editChanged` expression only moved; #13689: CodeRabbit comment on the publish flow at ws.ts:3046).
- #17129/#16695 (migrations, fix #26834), #25524 (fix #30115), #14290, #16102, #28047, #6466, #10101, #9293: criterion 3 (many bot comments) or 2 (over 40 files: #17129 62, #14290 120, #9293 53, #6466 41, #10101 50).
- #28845, #28840, #2829, #2837, #2679, #5362, #10677, #16719, #12598, #11436, #17082, #27197, #30623, #4860, #21362, #15328, #24276, #18124: criterion 2 (over 40 files or open PR).
- Already-used intro PRs excluded: 21315, 22107, 19355, 18505, 33632, 19432, 7599.

## Unverified

- Criterion 3 (no bot comment on the defect) was checked by reading inline review comments (first 170-500 characters each) for the intro PRs, plus the catalogue's `caught by none`; issue comments and review bodies were skimmed only for summaries. Overlap judgments between a bot comment and the golden are mine.
- Cases 16926, 33511 and 29909 are weaker (feature-gap flavour). Case 14892 class is closest to cross-file contract through external git semantics.
