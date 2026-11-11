# Chunk 06: PRs #30078..#26452 (2026-11-06)

## 1. Header

- PRs covered: 25 (#30078 .. #26452). 11 have no bot thread at all (#29738, #29607, #29285, #29284, #28955, #28825, #28625, #27699, #27691, #27682, #27489).
- Bot threads: 54 total. CodeRabbit 43, Macroscope 11.
- Verdicts: real-bug 2, real-minor 38, nit 7, wrong 3, unclear 4. (Judged from thread text and replies; code read only where stated.)
- Outcomes: fixed-before-merge 37, ignored/no reply 6, disputed (author declined, bot withdrew or no reply) 11. Unresolved at merge: #29825 T1 (outdated), #29817 T1, #28487 T6/T7/T8, #27500 T1, #26452 T4.
- Code checked in the clone: #29817 (diff only: `limit: 100`, filter on `:`), #30078 diff. All other verdicts are "(unverified)" in code.
- Track B: 17 `fix` PRs touch non-trivial source. SZZ run on 17 (one "no changed lines", one pure addition). Roughly 20 minutes.
- Caveat: the Macroscope reply "unable to act on this request" appears on most Macroscope threads; it is a permissions notice, not a verdict.

## 2. Track A (bot threads)

"fixed-before-merge" = author reply names a fix commit or the thread is outdated+resolved. "disputed" = author declined with a reason, bot withdrew.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30078 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Family match must normalize both slugs (`openai.gpt-5.6-luna` vs `gpt-5.6-luna`). Fixed 0ee81012c7. (unverified) |
| 30078 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Fallback model keeps the requested model's reasoningEffort/serviceTier; `none` rejected by another model (HTTP 400). Fixed 0ee81012c7 with test. (unverified) |
| 30078 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Managed instances omit custom slugs from the snapshot, so new fallback would replace a custom model; custom check moved before family match. Fixed 11729c9. (unverified) |
| 30000 | 1 | CR | Minor | nit | disputed | 1 | 1 | other | no | Layout class on `SelectTrigger`; author explained `min-w-0` overrides trigger's `min-w-36`; bot withdrew. |
| 30000 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Citation to a hidden (non-final) assistant message never navigates in final-answers-only mode. Fixed 951f131454. (unverified) |
| 30000 | 3 | MS | High | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Revert targets computed from the filtered timeline: reverting user run 3 uses checkpoint 1 and undoes run 2's work. Fixed ba9fe499ae with test. (unverified in code; reply and outdated flag) |
| 30000 | 4 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Active provider-retry errors hidden in final-answers-only mode. Fixed ba9fe499ae. Same defect as T6. |
| 30000 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Provisional runless answer shown while work continues. Fixed 951f131. |
| 30000 | 6 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Duplicate of T4 (running retry errors dropped). Fixed 951f131..ba9fe49. |
| 30000 | 7 | MS | Medium | nit | fixed-before-merge | 1 | 1 | performance | no | Boundary rescanned per loop iteration (quadratic). Fixed c30ffbd728. |
| 30000 | 8 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Dropping wake-notification rows moves the Working row above the previous answer. Fixed 8a2fafd912 with test. (unverified) |
| 30000 | 9 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Follow-up sent while the previous run still finalizes loses its Working row. Fixed 8a2fafd912. |
| 30000 | 10 | CR | Minor | wrong | disputed | 1 | 2 | other | no | Wanted decided approvals/recovered retries shown; owner: intentionally hidden in Zen; bot withdrew (its premise about folds was wrong). |
| 30000 | 11 | MS | High | real-minor | fixed-before-merge | 2 | 4 | UI state | no | Zen hides a completed steer answer of the same active run. Fixed 1b3cbfe791 (mobile and web). |
| 30000 | 12 | MS | High | unclear | disputed | 2 | 4 | UI state | no | Reply before a steer is dropped. Author: checked 544 real steers, only 3 of 20 replies were full answers; left as is. Design choice, not verified. |
| 29825 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | platform API | no | Android 13 and earlier: hardware Enter (IME_NULL) does not submit. Fixed 1020e30ffb; author says not re-run on a device. Thread unresolved but outdated. |
| 29825 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | platform API | no | Same Enter issue; bot also withdrew its "drop key-down filter" suggestion after author's on-device double-submit result. |
| 29825 | 3 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | Accessibility label not forwarded to the native EditText. Fixed e7930c2461 (`inputLabel`). Not tested with TalkBack. |
| 29817 | 1 | CR | Major | real-minor | ignored | 2 | 3 | resource limits | no | Fetching up to 100 PRs (`limit: 100` confirmed in the merged diff) could exceed the 1,000,000-byte process output limit and fail JSON decoding. Byte limit not confirmed; unresolved at merge. |
| 29795 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | After the 4-pass clean cap, restore returned success with removable paths left. Fixed 6bd5263aa6 (dry run, error). |
| 29795 | 2 | MS | High | real-bug | fixed-before-merge | 3 | 3 | error handling | no | The new leftover check treated `Skipping repository` / `Would skip repository` lines as leftovers, so restore failed whenever a protected nested repo existed. Fixed by e7ac911 (outdated). A regression the PR itself created. (unverified) |
| 29795 | 3 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | state machine | yes | Failed cleanup path returned without `git reset`, leaving checkpoint changes staged. Fixed e7ac911 (`resetIndex`). (unverified in code) |
| 29762 | 1 | CR | Major | unclear | disputed | 2 | 5 | race/ordering | no | `session.error` before the interrupted tool update leaves tool items running. Author: same ordering on main, out of scope; bot withdrew. Not checked in code. |
| 29688 | 1 | MS | none | nit | disputed | 1 | 1 | convention | no | Asks to move publish-and-refresh into a service (Effect conventions). Author: main already does it in the handler. |
| 29292 | 1 | CR | Minor | wrong | disputed | 1 | 3 | UI state | no | Recovery banner for provider-native subagents; author showed the state is unreachable (runless roots); bot withdrew. |
| 29292 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Banner says "Resumes" at quota reset though snooze is later. Fixed a4fa5a41ef. |
| 29292 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Banner promised a resume for a settled thread. Fixed 61cbac0. |
| 29292 | 4 | CR | Minor | nit | fixed-before-merge | 1 | 2 | UI layout | no | Touch target clipped below 44px. Fixed 4aacf5d. |
| 29292 | 5 | CR | Minor | nit | fixed-before-merge | 1 | 2 | UI layout | no | Wrapped touch targets overlap. Fixed 4aacf5d. |
| 29292 | 6 | CR | Minor | wrong | disputed | 1 | 3 | cross-file contract | no | Older-server ChatGPT limit codes; author showed web gates on `usage_limit`, bot withdrew. |
| 29292 | 7 | CR | Minor | nit | disputed | 1 | 1 | other | no | `any-pointer-coarse` suggestion; declined, repo convention is `pointer-coarse`. |
| 29292 | 8 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Recovery actions shown while a question is pending; server rejects the update (`Orchestrator.ts:3593` per author). Fixed 09a32d1. |
| 29292 | 9 | CR | Minor | nit | disputed | 1 | 1 | test coverage | no | Test request declined: maintainer asked for no tests. |
| 29220 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Reused Claude query reports a window computed from a later turn's cwd. Fixed a7425964c3 with two-turn test. (unverified) |
| 28728 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Truncated `stages` connection could replace a failed "Pipeline" check. Fixed 3d4e04f. |
| 28728 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | GraphQL partial data (`errors` or null stage) could drop a failed stage. Fixed. |
| 28728 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Nameless stage skipped instead of treated as incomplete. Fixed 0048ed6. |
| 28728 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | data integrity | no | Null job node drops a failed job; author says current head keeps the stage (`listedWhole`). |
| 28487 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 5 | race/ordering | no | Buffered items from the old session tagged with the new omission key. Author first deferred ("exists on main"), then juliusmarminge fixed it in bb012ea8245 (`subscribeDynamicWithSession`). (unverified) |
| 28487 | 2 | CR | Major | wrong | disputed | 1 | 5 | data integrity | no | Replay not refreshing the older-settled boundary; author showed counts refresh client-side, bot withdrew. |
| 28487 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Failed cwd scan leaves empty provider catalogs; no fallback. Fixed 61981f67f3. |
| 28487 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Live socket replaced at 1.5 s after delivering a frame. Fixed 791c9f1332. |
| 28487 | 5 | CR | Minor | nit | disputed | 1 | 3 | other | no | Silence window for remote sockets; intentional trade-off, bot accepted. |
| 28487 | 6 | CR | Minor | unclear | ignored | 1 | 3 | performance | no | Provider without cwd scanning marked pending; mobile schedules two useless refreshes. Unresolved. (unverified) |
| 28487 | 7 | CR | Minor | unclear | ignored | 2 | 4 | cross-file contract | no | Omitted catalogs could project identically so a change is never signalled. Unresolved, outdated. (unverified) |
| 28487 | 8 | CR | Major | unclear | ignored | 3 | 5 | data integrity | maybe | Client resumes by omission key without checking event-store identity; a different DB at the same endpoint could be missed. Unresolved, outdated. Not traced (the bot rated it Major; plausible but rare). |
| 28223 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI layout | no | Modal overlaps native caption buttons at `sm` widths. Fixed ad42e64. |
| 28223 | 2 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | UI layout | no | Heading reads "server?" at short heights (specificity). Fixed ad42e64. |
| 27500 | 1 | CR | Minor | real-minor | ignored | 1 | 3 | edge case | no | `-2147483648` accepted though Git rejects it. Unresolved, merged. (unverified) |
| 26452 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 5 | race/ordering | yes | Flush compares `state.value` with `props.value`, so edits round-tripping to the same text stay unacknowledged and the draft reappears after send; may also consume an intercepted paste. Fixed a6b8cfc. (unverified) |
| 26452 | 2 | CR | Major | wrong | disputed | 1 | 4 | race/ordering | no | `readState` returns stale text; author: `emitTextChange` updates synchronously on main queue; bot withdrew. |
| 26452 | 3 | CR | Major | real-bug | fixed-before-merge | 3 | 5 | race/ordering | yes | Selection event clears `lastEventWasPaste`, so a flush can acknowledge past a pending paste and drop it. Fixed 6c45966 (`pasteEventCount`). Residual in-flight paste case left, same as main. |
| 26452 | 4 | CR | Minor | nit | ignored | 1 | 2 | other | no | Usage-limits command read before flush; needs a pending misspelling in a command. Declined. |
| 26452 | 5 | CR | Major | real-minor | fixed-before-merge | 2 | 5 | race/ordering | no | Flush skips paste state but resolves before the paste callback arrives; send snapshot can predate it. Confirmed addressed by author (follow-up work). (unverified) |

## 3. Track B (escaped bugs)

Skipped as trivial or not a bug fix: #29738 (status bar icon size), #28955 (SZZ ran: #24492, 1 line; iOS compose button growth, UI), #27489 and #29825 (pure additions: autofill opt-out, no SZZ target), #27691 (dnd-kit autoscroll tuning; SZZ only #2829), #27682 (rounding of width; SZZ #20812, 1 line, sev 1), #28825 (manifest orientation lock; SZZ #5613 "Allow Android tablets to rotate", sev 1, no bots), #29292 / #28728 / #28223 (feature-sized "fix" titles, UX consolidation or re-landing). #29284 and #30000 are perf and feat.

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 30078 | Text generation (titles, commits, PR text) sent the default `gpt-6-luna` to ChatGPT-login accounts that do not list it, so every call failed | #14290 "feat(codex): connect ChatGPT accounts with managed authentication" (+10061/-280, 2026-09-29); SZZ itself blames #9921 (4 lines, qualified-id selection) and #14290 (1) | low | missed (Macroscope: 18 comments, one High that a ChatGPT account is published with `models: []`, adjacent but not about the text-gen default) | 3 | 4 | The model-selection lines are #9921's; the failure only appears once managed ChatGPT accounts with narrower catalogs exist (#14290). |
| 29817 | Azure DevOps `az repos pr list --source-branch` matches a fork's same-named branch, hiding the branch's own PR | no SZZ target (pure addition of a `headBranchProbe`) | n/a | n/a | 2 | 3 | The provider had no probe hook; origin is the absence of a hook. |
| 29795 | Reverting files ran `git clean -fd` once, so files hidden by a new `.gitignore` from the turn were left behind | #2586 "Optimize VCS diff loading to be up to 98% faster" (+2123/-1074, 32 files, 2026-05-11); 5 of 10 blamed lines; `git log -S` agrees | medium | missed (Macroscope: 2 comments on stream collection and truncation marker, none on restore) | 3 | 4 | Design gap in original restore, not a regression. Other blamed PRs: #11338, #14874 (1-2 lines each). |
| 29762 | Stopped OpenCode tools showed as failed (diff text "Tool execution aborted") instead of interrupted | #2829 orchestrator import only (9 lines) | n/a | n/a (noise origin) | 2 | 3 | Origin predates the file move (#17345); no target. |
| 29688 | A publish whose first push fails did not refresh repository identity and Git status, so the UI still offered Publish | #13689 "perf(server): stop re-running git for every project each minute" (+100/-36, 2026-09-26); 2 blamed lines | medium | missed (CR and Macroscope commented on that exact handler: asked for a test, CR accepted a documented narrow stale-identity case; failure path never raised) | 2 | 3 | Refresh was added on success path only. |
| 29607 | Thread titles, branches and commit messages silently failed when the default provider (Codex) was not installed or signed out | #26164 "feat: fall back when the default provider is out of usage" (+763/-37, 2026-10-29); 6 of 6 blamed lines | medium | missed (Macroscope: 14 comments on this feature's fallback; one High about a logged-out saved fallback, adjacent) | 3 | 3 | The fallback only handled an exhausted usage window, not an unusable provider. Before #26164 there was no fallback at all. |
| 29285 | Remote subagents listed apart from "Previous agents"; running ones looked finished | #16719 "feat(server): delegate_task to a linked environment" (+5156/-322, 2026-10-27); 22 of 38 blamed lines (#2829 has 14, noise) | high | missed (Macroscope commented on the same component, provider-initials collision, not on the grouping) | 1 | 2 | UX inconsistency, no data impact. |
| 29220 | Claude compaction meter ignored `autoCompactWindow` set in Claude's own settings files | #22864 "fix(server): Claude --settings launch args merge with T3's settings" (+182/-36, 2026-10-27); 6 of 14 blamed lines (also #30051: 4, #24654: 3) | low | missed (CodeRabbit: 6 comments on settings logging and skillOverrides, none on compaction) | 2 | 4 | Missing feature rather than regression; low confidence. |
| 28625 | Android 15+ stayed "offline" after reopening because `expo-network` never reports the block lifting | no SZZ target (change adds `onBlockedStatusChanged` to a patch file) | n/a | n/a | 3 | 5 | Platform behaviour; patch file has no blamable removed lines. |
| 27699 | Android showed both an alert and a retained Done card for one completion | #10416 "feat(mobile): add Android agent notifications and ongoing activity" (+5761/-142, 58 files, 2026-09-09); 8 of 8 blamed lines | high | missed (CodeRabbit had a duplicate-alert thread on the alert history ordering, fixed; the alert plus card duplication was not raised) | 2 | 3 | Adjacent duplicate-alert finding, different mechanism. |
| 27500 | Numeric `core.bare` values (`2`, `-1`, `01`) were read as false, so onboarding omitted worktrees of a bare repo | #16688 "fix(server): onboarding offers worktrees of a bare repository" (+107/-8, 2026-10-20); 1 blamed line | high | missed (both bots reviewed `bare` parsing there: include.path, quoted `"true"`, same-line `[core] bare = true` all raised and fixed; numeric forms never) | 2 | 3 | Same parser, fourth variant of the same family. |
| 26452 | iOS: Send accepted a pending autocorrection after the draft was read; late event refilled the composer | #3101 "[codex] Add native mobile composer and markdown" (+8550/-715, 148 files, 2026-06-16); 11 of 19 blamed lines | medium | missed (Macroscope: 5 comments, none on the editor event ordering) | 3 | 5 | Cross-layer ordering between native events and JS; very hard from one diff. |
| 27682 | Android composer flickered at the wrap boundary (width rounded down) | #20812 "fix(mobile): the composer stays one row until the draft wraps" (+469/-201, 2026-10-20); 1 line | medium | missed (CodeRabbit raised a Major on ThreadComposer font scale, not width rounding) | 1 | 4 | Cosmetic. |
| 28955 | iOS compose button grew while a tab was pressed | #24492 "fix(mobile): the iPhone new-chat button sits beside the tab bar on iOS 26.6" (+7/-6); 1 line | medium | bots-did-not-run (no bot comments at all, unverified why) | 1 | 4 | Cosmetic. |
| 28825 | Android tablet cold launch used a portrait manifest lock before the runtime policy ran | #5613 "Allow Android tablets to rotate" (+81/-0, 2026-08-10); 16 of 16 blamed lines | medium | bots-did-not-run (no comments, unverified) | 1 | 3 | Cosmetic splash letterboxing. |
| 27691 | Sidebar drag scrolled to the bottom (dnd-kit default autoscroll) | #2829 only | n/a | n/a | 1 | 3 | Library default, no target. |
| 29738 | Alert and live card used different status bar icons | #10416 (8 lines blamed); trivial | medium | missed | 1 | 2 | Trivial, no analysis. |

## 4. Catalogue candidates (severity >= 3)

1. `gitclean-single-pass-leaves-ignored-files` (Track B, escaped). PR #29795, introduced by #2586. Golden: restore runs `git clean -fd` once, but the first pass deletes a `.gitignore` the turn created and, in the same scan, git had skipped the files it ignored, so those files survive the revert and later get staged; clean must repeat until nothing is left. Base `8fc317939f5c8bbef4afbe309ae897abbc221631`, head `427bc9ccc6862d76db100035f4daa01aea911534` (last commit of #2586). Caught by: none (Macroscope commented on #2586 elsewhere). Confidence in introducing PR: medium.
2. `autocorrect-flush-uncorrected-draft-after-send` (Track B, escaped). PR #26452, introduced by #3101. Golden: on iOS, tapping Send makes the native text view accept a pending autocorrection and emit a change event after JS has read and cleared the draft, so the late event refills the composer with the corrected draft. Base `708d5383a9c7415c3795890ca4f664c7b00f9a47`, head `3a4a8254987eddd542a456a660efb79d827834fc`. Caught by: none. Confidence: medium; PR is 148 files, replay is heavy.
3. `zen-rollback-targets-from-filtered-timeline` (Track A, fixed before merge). PR #30000. Golden: in final-answers-only mode rollback targets are derived from the timeline after notification-only wake runs were removed, so reverting a later user run restores the wrong checkpoint and also undoes the earlier run's changes. Base `7c22e24e3fa1a3bb3a95f27aea000067f198fe7f`, head `28e4da85045622d1edb3db12241399fb55a1b621` (Macroscope's comment commit). Caught by: Macroscope.
4. `restore-checkpoint-cleanup-failure-leaves-index-staged` (Track A, fixed before merge). PR #29795. Golden: the new "untracked files remain" error path in `restoreCheckpoint` returns without `git reset`, leaving the checkpoint's changes staged in the index. Base `0a86e157a0eaf80c34da089a29526c6201ac529a`, head `6bd5263aa644ffd9c00f6691f40f9c6a1b4ad644` (CodeRabbit's comment commit). Caught by: CodeRabbit.
5. `ios-flush-pending-input-paste-ack` (Track A, fixed before merge). PR #26452. Golden: `flushPendingInput` acknowledges the newest native event count, so an intercepted paste event whose JS callback has not run is rejected and dropped, and text edits that round-trip to the same text leave the draft to reappear. Base `bd7da7fa485d20d361e9c7146bfe29c0bcf82d5a`, head `342fd8632c903104d48b3ca6d711912a406b2f89` (Macroscope T1; CodeRabbit T3 commented on `e3b154aaa437cb991820f8bf788ac09c94f2da7c`). Caught by: Macroscope and CodeRabbit.

Considered and rejected: #28625 (sev 3, no introducing PR to replay), #28487 T8 (unverified, unresolved, plausible but not traced).

## 5. Observations

- Macroscope's High findings in this chunk (#30000 T3, #29795 T2, #26452 T1) were all real regressions created by the PR under review and all fixed before merge; CodeRabbit raised the sibling defects (#29795 T3, #26452 T3).
- Across 17 traced fixes, neither bot flagged the defect at the introducing PR in any case; where they reviewed the same code (#16688 bare parsing, #13689 publish handler, #26164 fallback, #10416 alert dedup) they found neighbouring variants, never the later bug.
- CodeRabbit withdrew 10 findings after the author supplied a reason (#30000 T1/T10, #29292 T1/T6/T7/T9, #28487 T2/T5, #26452 T2, #29762 T1); authors answer with code facts, and several withdrawn claims rested on a premise the bot had not checked (#30000 T10, #29292 T1, #28487 T2).
- Macroscope is told "unable to act on this request" when the author replies to it; the bot gives no ack, so Macroscope threads rely on outdated flags to show they were fixed.
- Unresolved Major CodeRabbit threads were merged without reply in #29817 T1 and #28487 T8; both are speculative resource or identity edge cases.
