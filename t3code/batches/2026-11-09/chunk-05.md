# Chunk 05: PRs #29018..#19064 (2026-11-09)

## 1. Header

- PRs covered: 23 (#29018 .. #19064). 6 have no bot thread (#29018, #28667, #28638, #28524, #28125, #19064). All 23 merged into `main` (checked with `gh pr view ... baseRefName` for the fix PRs and the PRs SZZ blamed); none is a stack-branch PR, so no SZZ result lands on unmerged stack commits.
- Bot threads: 60. CodeRabbit 46, Macroscope 14.
- Verdicts: real-bug 10, real-minor 28, nit 11, wrong 11, unclear 0.
- Outcomes: fixed-before-merge 44, disputed 12 (author explained, bot withdrew or accepted), ignored 2, unknown 2.
- Code checked: #28814 (merge diff vs T1), #27748 (T5 text at f218ec0), #24079 (T8 code at b406b70), #21163 (T6 code at 9a71d10). Everything else is judged from thread text, replies and outdated/resolved flags: "(unverified)" where it matters.
- Track B: 20 `fix` PRs; 2 trivial or non-source (#29018 CSS, #28524 vendored tarball bump); SZZ run on 18 (the 18th, #19064, returned "pure addition" with 4 others). 5 pure additions, 3 with no usable target, 10 traced to a PR; no escaped bug is severity >= 3.
- Note on numbering: PR numbers are not merge order in this repo (for example #30257 and #30561 merged before #27748 and #24079). SZZ results with a higher number than the fix are normal.

## 2. Track A (bot threads)

Outcome evidence: "reply" = author reply says fixed; "outdated+resolved" = flags; "withdrawn" = bot accepted the author's rebuttal.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | one-line finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 28814 | 1 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | Swallowing every `ERR_ABORTED` from `loadURL` also hides a blocked unload, so navigation reports success while the old page stays. Merged diff has `unloadPrevented` via `will-prevent-unload` (code read). |
| 28814 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Same-URL self-reload aborts the first load with the same URL; comparing URLs misses it. Addressed in 015a6eb. |
| 28571 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | Perf test should wait per update; author waits for the final status instead, bot agreed. Test-only. |
| 28047 | 1 | CR | Major | wrong | disputed | 1 | 3 | state machine | no | Existing Claude sessions keep old flag. Labs row says "Applies to new sessions"; bot withdrew. |
| 28047 | 2 | CR | Minor | wrong | disputed | 1 | 3 | resource leak | no | Unbounded `thread/sample`; Codex has a 30 s server timeout. Withdrawn. |
| 28047 | 3 | CR | Minor | wrong | disputed | 1 | 3 | state machine | no | Sample while descendants run; UI only shows suggestion for a completed run. Withdrawn. |
| 28047 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | security | maybe | Cached suggestion served for a deleted thread id. Fixed in 11fd8e9 (null for missing thread), test added. |
| 28047 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI state | no | Tab-only hint shown on touch-only mobile web. Fixed in 11fd8e9. |
| 28047 | 6 | CR | Minor | nit | ignored | 1 | 2 | UI state | no | Long suggestion can spill over controls; author declines, bot accepts. |
| 28047 | 7 | CR | Minor | wrong | disputed | 1 | 2 | security | no | `prompt_suggestion` frame lands in opt-in native log; log already holds full prompts. Withdrawn. |
| 28047 | 8 | CR | Minor | wrong | disputed | 1 | 3 | state machine | no | Sample while background command runs; earlier review removed that guard on purpose. Withdrawn. |
| 28047 | 9 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | resource leak | maybe | Interrupted settings read after `prepareMcpSession` leaves the MCP credential reservation held. Fixed in be059be (read moved before). Claim not traced in code; could be sev 3. |
| 28047 | 10 | CR | Major | wrong | disputed | 1 | 1 | other | no | Asks for a subscription test; test already added in 11fd8e9. Bot "Major" for a test request. |
| 28047 | 11 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI state | no | Tab traps keyboard users when a suggestion shows; Escape dismiss added in be059be. |
| 28047 | 12 | CR | Minor | wrong | disputed | 1 | 4 | race/ordering | no | Late older-run sample overwrites newer; Codex fails stale samples via `history_version()`. Withdrawn. |
| 27753 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Legacy child tasks use latest run for model while result is stored from an earlier run. Addressed 3aacf80. (unverified) |
| 27753 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | data integrity | no | Provider notices not limited to the active attempt. Addressed 3aacf80. (unverified) |
| 27753 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Alias vs catalog slug makes a false "substituted model" note. Addressed b229bfc..bd5c9d9. (unverified) |
| 27753 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | `executedModel` undefined when the latest turn has no model frame. Thread resolved+outdated, no reply seen (outcome inferred, unverified). |
| 27748 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Test checks a keyword not the prohibition. Addressed 8ac3a29. |
| 27748 | 2 | CR | Major | real-minor | unknown | 2 | 4 | security | maybe | File-backed stdin for `sudo -S` breaks piped commands and `sudo cat /dev/stdin` could echo the password. Outdated, no reply; later text still says "the password takes stdin" (unverified whether judged). |
| 27748 | 3 | CR | Major | nit | unknown | 1 | 1 | other | no | CI wants `agent-context-increase` label; author says it is a maintainer decision. Process, not code. |
| 27748 | 4 | CR | Major | nit | disputed | 1 | 3 | other | no | `-y` auto-approves confirmations. Author: needed because stdin is the password file; bot conceded it overstated. |
| 27748 | 5 | MS | High | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | `sudo -n <cmd>` still runs the command under cached or NOPASSWD sudo, so a nonzero exit triggers the documented `sudo -S` retry and the command runs twice. Instruction text at f218ec0 reads "once `sudo -n <cmd>` fails, run `sudo -S ...`" (code read). Fixed c45eb6c (retry only when a password is required). |
| 27748 | 6 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | Same defect as T5 (duplicate execution after partial change). Fixed c45eb6c. |
| 27748 | 7 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | other | no | Eval cases pass on `test -e` and miss `--stdin`; graders tightened over three rounds. |
| 27748 | 8 | MS | - | nit | fixed-before-merge | 1 | 1 | other | no | Test pins instruction copy; removed in c45eb6c. |
| 27576 | 1 | CR | Minor | wrong | disputed | 1 | 2 | other | no | Lower nav-bar guard to API 26. Author: API 26-28 paints an opaque bar, flipping icons would hurt contrast. Withdrawn. |
| 27353 | 1 | CR | Major | nit | ignored | 1 | 1 | other | no | Wrap browser test assertions in `vi.waitFor`. Unresolved, merged. |
| 27046 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | maybe | Page `[popover]:popover-open` animation can move the cursor; author reproduced in Chromium. Fixed 306ea0f. |
| 25835 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | maybe | macOS: `isFullScreen()` stays true until `leave-full-screen`, so a re-entry request is dropped. Fixed b153abf. |
| 25828 | 1 | CR | Minor | wrong | disputed | 1 | 3 | other | no | Paste item missing when input is not first responder; author checked on simulator, UIKit supplies it. Withdrawn. |
| 25828 | 2 | MS | High | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Toolbar Paste skipped `resetInput()`, so Korean recomposition emits DELs into pasted text. Fixed 4402bee. |
| 25828 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Same as T2, found by CodeRabbit. Fixed 4402bee. |
| 25532 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Provider-based image paste bypasses both handlers; author reproduced with a native test. Fixed 67ec555. |
| 24933 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 2 | error handling | no | A rejected alert-channel read aborts device registration. Fixed e4be495. (unverified) |
| 24933 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | API 36 ongoing Done card cannot be dismissed when locked; Dismiss action added. |
| 24933 | 3 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Doc wording. |
| 24933 | 4 | MS | - | nit | fixed-before-merge | 1 | 1 | other | no | Duplicate test; folded in bdc043a. |
| 24482 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | A paste-sized commit starting with the composing word escapes the 32 KiB fold threshold. Fixed 2be4466. (unverified) |
| 24079 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 4 | state machine | yes | Parent keeps publishing `waiting_for_approval` after a child request resolves or the child is deleted, when publishing was disabled in between. Fixed (re-read cached children on publish). |
| 24079 | 2 | MS | High | real-bug | fixed-before-merge | 3 | 4 | race/ordering | yes | Child-triggered parent publishes bypass `cancelPublishRetry`, so a transient failure reuses an exhausted retry budget and never retries (approval push lost). Fixed (same entry point as event publishes). |
| 24079 | 3 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | state machine | yes | Child request first appearing while publishing is off or relay unlinked never enters `subagentRequests`; parent never reports the wait. Fixed (`trackSubagentWhilePaused`). |
| 24079 | 4 | MS | High | real-minor | fixed-before-merge | 2 | 3 | race/ordering | no | Replacement approval from a child keeps the old request timestamp. Author first declined, then fixed in e98fac6 by tracking request id. |
| 24079 | 5 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Empty startup snapshot does not turn on paused tracking. Fixed b48f1c9. |
| 24079 | 6 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | state machine | yes | When child A is waiting and B starts waiting later, parent still selects A so the publish identity is unchanged and B's approval push is skipped. Fixed 34bfc4a. |
| 24079 | 7 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Equal-millisecond requests keep the first; added change-order tie-break (2e78c26). |
| 24079 | 8 | MS | High | real-bug | fixed-before-merge | 3 | 5 | race/ordering | yes | After a clear publish the next child wait reuses the same `updatedAt` and `alert_id`, so Android treats the second approval as already seen. Pre-fix logic present at b406b70 (code read: `previousPublication.updatedAt` + 1 ms only when a wait is active). Fixed fb50dd3. |
| 24079 | 9 | CR | Minor | wrong | disputed | 1 | 4 | race/ordering | no | Clear publish with older `updatedAt` is rejected by Android. Author: ordering uses FCM `updated_at` set by relay send time. Bot withdrew. |
| 24079 | 10 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Comment for `Effect.fnUntraced`. |
| 21687 | 1 | CR | Major | nit | fixed-before-merge | 1 | 1 | other | no | detekt complexity 17 > 15 (CI). Fixed bee6dac. |
| 21687 | 2 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | maybe | IME key event with device id 0 and no soft flag is treated as hardware Return and sends. Author first declined, then fixed a68cd86 (requires resolved alphabetic keyboard). |
| 21652 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Horizontal swipe loses ownership once vertical drift exceeds horizontal. Author first rejected, then restored the gesture latch in d3999d2 after manual testing. |
| 21163 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | race/ordering | no | Existing Live Activities waited up to 10 s on the widget snapshot read. Fixed 25247c6. |
| 21163 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | race/ordering | maybe | Older widget snapshot can overwrite newer one; reads numbered (f7773cf). |
| 21163 | 3 | MS | High | real-bug | fixed-before-merge | 3 | 3 | state machine | yes | Sign-out during `loadPreferences()` still primes a Live Activity with the signed-out account's thread data. Fixed 1ba2c18 (recheck identity). (unverified in code) |
| 21163 | 4 | MS | High | wrong | disputed | 1 | 2 | cross-file contract | no | Widget deep link hard-codes `t3code://`. Author: widget URL always opens the containing app, all three schemes are registered. Acknowledged. |
| 21163 | 5 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | state machine | no | After cold start a failed snapshot read leaves stale signed-out content. Fixed 9a71d10 (tri-state). |
| 21163 | 6 | MS | Critical | real-bug | fixed-before-merge | 3 | 4 | data integrity | yes | After the auth bridge releases account A, A's cached thread/project titles stay visible under B's session if B's snapshot fails (`widgetShows` stays "account-rows"). Code at 9a71d10 shows the fix gating on identity change (read, partial). Fixed 49a8baa (`rowsOf: identity`). |
| 21163 | 7 | MS | High | real-minor | fixed-before-merge | 2 | 4 | race/ordering | maybe | Obsolete refresh for A bumps the shared read counter and discards B's snapshot, leaving B on Loading. Fixed 49a8baa. |

## 3. Track B (escaped bugs)

Skipped as trivial or non-source: #29018 (CSS hover radius), #28524 (vendored markdown tarball bump, no source), #19064 (pure addition, Expo plugin for Android window metrics, no SZZ target).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 28814 | A page redirect during `loadURL` showed a `navigate.loadURL` error although the redirect succeeded | #3244 "[codex] structure desktop preview failures" (+1189/-415, 2026-06-20), 2 of 2 lines | low | no bot comments on that PR | 2 | 3 | #3244 wrapped `loadURL` in the error reporter; the underlying loadURL call is older. Needs Electron `ERR_ABORTED` knowledge. |
| 28667 | Opening a citation comment put the caret at the start, not the end | #9146 "feat(web): cite assistant responses with inline citations" (+5986/-328, 2026-09-02), 1 of 1 | high | missed (13 inline comments on that PR, none on focus or caret) | 1 | 1 | Cosmetic. |
| 28638 | A window saved 1px past a display edge was judged off-screen and reopened at the default position | #3851 "fix(desktop): preserve main window bounds" (+917/-16, 2026-07-20), 4 of 4 | high | missed (Macroscope: minimized-quit bounds at DesktopWindow.ts:386; CR none on the containment test) | 2 | 3 | Strict containment check with no tolerance; visible in one hunk if you know OS rounding. |
| 27753 | Delegated Claude tasks named the requested model, not the one that ran (org allows only Sonnet) | no clear SZZ target: blamed lines are #2829 (noise) and 1-line hits in #27039, #16595, #16719 | n/a | n/a | 2 | 3 | Feature gap (new `executedModel` field) rather than a defect in older code. |
| 27748 | Agents never called `request_secret` for a sudo password; they told the user to run it themselves | #30257 "feat(server): agents ask for secrets through request_secret instead of chat" (+437/-36, 2026-11-04), 1 of 1 line | medium | missed (CR commented on SecretRequests.ts and the contract, none on the instruction text; Macroscope no inline hit found) | 2 | 3 | Prompt-behaviour gap found by running 5 real agent runs (author measured 0 of 5 called the tool); not visible in a diff. |
| 27576 | Android navigation-bar style ignored the app theme | #15502 "fix(mobile): keep dictation running across navigation behind an edge pill" (+1306/-305, 2026-10-04), 1 of 1 line in `App.tsx` | low | no bot comments on that PR | 1 | 3 | The real origin is the one-time edge-to-edge default (framework), not this PR. |
| 27353 | Markdown task checkboxes stayed checked after the source row was removed (stale DOM state) | no SZZ target (pure addition) | n/a | n/a | 2 | 3 | React key or state reuse in `ChatMarkdown.tsx`; origin not found. |
| 27046 | Recording cursor hidden behind a native `showModal()` dialog | #12779 "fix(desktop): align preview recording cursors and show input feedback" (+1398/-107, 2026-09-20), 1 of 1 line | medium | missed (Macroscope: one comment on PreviewView.tsx recording tab id, unrelated) | 2 | 3 | Top-layer stacking knowledge needed. |
| 25835 | Chat video fullscreen only filled the app window (taskbar stayed visible on Windows) | PR body names #16961 "browser tab fixes for fullscreen, shortcuts, links, reload and hidden tabs" (+1069/-152, 2026-10-08); SZZ: pure addition | high (from fix body) | missed (Macroscope High on #16961 was about OAuth popup shortcuts; none about fullscreen sizing) | 2 | 4 | Setting `disableHtmlFullscreenWindowResize` had a product side effect only visible at runtime. |
| 25828 | iOS terminal: no copy of output, no long-press Paste, multi-line paste joined, freeze, off-screen toolbar Paste | no single target (mixed: #2013 WIP mobile megapatch, #11265, #9199) | low | not checked | 2 | 4 | Several unrelated gaps in the native terminal; not a regression from one PR. |
| 25532 | Dropping an image onto the iOS message input added no attachment (`canPaste` rejected image providers) | no SZZ target (pure addition) | n/a | n/a | 2 | 3 | Missing capability more than a regression. |
| 24933 | Android completion posted a separate Done alert and the finished live activity lost its Live Update promotion; muting alerts also dropped the activity | #10416 "feat(mobile): add Android agent notifications and ongoing activity" (+5761/-142, 2026-09-09; 8 lines) and #11645 (redesign, 6 lines) | medium | partly: Macroscope High on #10416 `FcmDeliveries.ts:225` ("notification-only environments lose alerts when another live activity exists") is the same alert/activity coupling; whether it was fixed there is unverified | 2 | 3 | Adjacent catch, not the exact symptom. |
| 24482 | Android keyboard clipboard paste (committed text) stayed inline instead of folding into an attachment | #11442 "feat(composer): fold large pastes into text attachments" (+3275/-462, 2026-09-13), 6 of 6 | high | missed (many paste comments on web and mobile, none on IME `commitText` path) | 2 | 4 | Needs knowledge that keyboard clipboard goes through `commitText`, not the paste menu. |
| 24079 | Phone got no "Approval needed" push when a delegated subagent waited | #2837 "feat(relay): Add managed relay tunnels and APN service" (+48977/-2064, 2026-06-05), 9 of 16 lines; also #30561 (2 lines) | low | bots too diluted to judge (50 inline comments, none on subagents; unverified) | 3 | 4 | Feature gap: relay only published top-level threads. Not catalogued as an escape, since the sev-3 defects were in the fix PR and caught before merge (see Track A). |
| 21687 | Android hardware keyboard Return always inserted a newline, no send key | no SZZ target (pure addition) | n/a | n/a | 1 | 2 | New setting; not a regression. |
| 21652 | Diagonal sideways swipe across an HTML block started scrolling the conversation | #17211 "fix(mobile): HTML pages in a thread no longer trap scrolling on Android" (+138/-70, 2026-10-08), 13 of 14 | high | missed (one CR review with no inline comments) | 2 | 4 | Fix of a fix: #17211 itself changed touch interception; needs Android gesture knowledge. |
| 21163 | iOS Agent Activity widget stayed blank | #3685 "Improve live activity routing and diagnostics" (+5735/-812, 2026-07-07), 4 of 6 lines | low | not checked (37 inline comments, several on remoteRegistration.ts, none on widget) | 2 | 3 | Mostly an unbuilt feature (no widget layout), not a regression. |

Bot coverage on the traced bugs: caught 0 exactly, partly 1 (#24933), missed 8 (28667, 28638, 27748, 27046, 25835, 24482, 21652, 24079 diluted), no bot comments or not checked 4 (28814, 27576, 25828, 21163). All sev <= 3 and the sev 3 one (#24079) is a feature gap.

## 4. Catalogue candidates (real bugs, severity >= 3)

All are Track A, fixed before merge, so the head is the commit the bot commented on (not the PR's last commit).

| id | PR(s) | golden description | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| desktop-loadurl-swallows-blocked-unload | #28814 | Treating every `ERR_ABORTED` from `loadURL` as a superseded navigation also swallows the rejection caused by a page that blocks unload, so navigation reports success while the old page stays. | 3fd2b855c5c6b9169cdfe3733b34011c1c5ed4b7 | a926a8a5c804c74a39b110e704c1cb559caa03d3 | CodeRabbit |
| sudo-retry-reruns-command-after-nonzero-exit | #27748 | The instruction retries with `sudo -S` whenever `sudo -n <cmd>` exits nonzero, but `sudo -n` still runs the command under cached or NOPASSWD sudo, so a command that ran and failed (or partly changed state) is executed twice. | d0f1f7200dce1229f75314b3d9eb1d7ac3abb607 | f218ec0d94eddf6f88a7b548a8263c2c34baff3f | Macroscope + CodeRabbit |
| relay-child-wait-lost-while-publishing-paused | #24079 | A subagent approval request that first appears while publishing is disabled or the relay is unlinked is never tracked, so after publishing resumes the parent does not report `waiting_for_approval`. | 8f144827f680f4064cb3951b4b60d4e24043748d | e17084bce7f4fa20bbaf31e8df6b7bcb3bd13df3 | CodeRabbit |
| relay-child-publish-bypasses-retry-reset | #24079 | Parent publishes triggered by child request changes skip `cancelPublishRetry`, so a transient failure reuses an exhausted retry budget, no retry is scheduled, and the approval push is never sent. | 8f144827f680f4064cb3951b4b60d4e24043748d | e17084bce7f4fa20bbaf31e8df6b7bcb3bd13df3 | Macroscope |
| relay-second-child-approval-not-selected | #24079 | With child A waiting and child B starting to wait later, the parent still selects A's request, so the publish identity is unchanged and B's approval push is skipped. | 8f144827f680f4064cb3951b4b60d4e24043748d | e98fac6f7dcf4cc09a9a6af37dcfc36bf3cf8ef6 | CodeRabbit |
| relay-reused-alert-id-suppresses-second-approval | #24079 | After a child wait clears, the next wait reuses the same `updatedAt` and `alert_id` (the clear publication used the older running timestamp), so Android treats the second approval notification as already seen. | 8f144827f680f4064cb3951b4b60d4e24043748d | b406b70d1bf54fa57237aa05f56563a5e4ac89d7 | Macroscope + CodeRabbit (T9 related, rebutted) |
| widget-shows-previous-account-rows-after-switch | #21163 | After account A's token provider is released, the widget keeps A's cached thread and project titles (`widgetShows` stays "account-rows") and shows them under account B if B's snapshot read fails. | 25bf84ab07f53f141c20239c63e383823a9d5ea0 | 9a71d1093083e4246a5d3a146b798e181f1aeb66 | Macroscope |
| widget-primes-live-activity-after-sign-out | #21163 | A sign-out during `loadPreferences()` still lets the refresh prime a Live Activity with the pre-sign-out snapshot, recreating a card with the signed-out account's data. | 25bf84ab07f53f141c20239c63e383823a9d5ea0 | f3ddbac193af819286b299fb46857a6d49e222ef | Macroscope |

Borderline, not promoted: #28047 T9 (MCP credential reservation held after an interrupted settings read, sev 2-3, claim not traced); #24079 T1 (stale `waiting_for_approval` after child resolves with publishing off, sev 3, close cousin of the first relay entry).

## 5. Observations

- Macroscope found most of the severe defects in this chunk (6 of 10 real-bug threads: #27748 T5, #24079 T1/T2/T8, #21163 T3/T6), mostly state and ordering bugs in relay and account-switch code. CodeRabbit found 4 real-bug threads. Both bots reported the same sudo-retry defect on #27748.
- CodeRabbit severity labels are inflated again: Major on a CI label request (#27748 T3), a test request (#28047 T10) and a lint complexity count (#21687 T1). 11 of 60 threads were wrong and 9 of those 11 were withdrawn by the bot after the author explained a constraint the bot did not know (Codex server timeout, Labs "new sessions" contract, FCM `updated_at`).
- Many in-PR bot findings were on PRs authored with an AI loop that replies to every thread (#28047, #24079, #21163, #27748): 44 of 60 threads fixed before merge, 2 ignored, 2 unknown. Two threads were first declined and later fixed by the author (#24079 T4, #21687 T2), so a decline reply is not a final answer.
- Escaped bugs from this day are low severity (max 2, except the feature-gap #24079): mobile and desktop platform behaviour (IME paths, OS rounding, Electron `ERR_ABORTED`, Android gestures). Neither bot commented on any of these at introduction, and these cases need platform knowledge, not diff reading. Several "fixes" are really missing capabilities (5 pure additions).
- Macroscope sometimes lags: on #27748 T5 it replied that the fix "isn't in the current PR branch" while CodeRabbit said the same about an unpushed commit, so both bots' re-checks were stale for a while (unverified how long).
