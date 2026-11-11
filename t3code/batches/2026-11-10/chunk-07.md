# Chunk 07: PRs #31535..#31262 (2026-11-10)

## 1. Header

- PRs covered: 25 (#31535 .. #31262). All are `fix(web)` PRs by one author (flamboh, AI-assisted) and all merged into **stack branches of the unmerged "redesign" stack**, not into `main`: #31535 into the layer-1/2 branches, the other 24 into `maria/redesign/6-workspace-panes` (layer 6, PR #28845, still open, labelled "DO NOT MERGE", +42060/-11038). 12 PRs have no bot thread.
- Bot threads: 28 total, all Macroscope. CodeRabbit left nothing on these PRs.
- Verdicts: real-bug 3, real-minor 20, nit 2, unclear 3, wrong 0.
- Outcomes: fixed-before-merge 14, fixed-elsewhere 1 (#31462 T2, fixed by #31406), ignored/no reply or "comes from the base branch" 13, disputed 0.
- Code checked at the merge commit: #31469 T2 (layoutDrag.ts:300 still has the buggy filter), #31485 T3 (SurfaceHost.tsx 1060-1082). Everything else is judged from thread text and replies (unverified).
- Track B: 25 fix PRs; 22 traced with SZZ (3 skipped as trivial: #31395, #31387, #31384; #31514 returned "pure addition"). Time about 30 minutes.
- Caveat 1: SZZ shows `?fcdbd455` for most layer-6 fixes. That is commit `fcdbd4550fe6749a4e20ce350e0a7bec6d5b91ac` "feat(web): add workspace panes and transitions" (2026-10-31), the first commit of PR #28845. Same for `?e9a083d8` (#28840 layer 2) and `?47b6fa97` (#28839 layer 1). These commits have no `(#N)` in their subject, so I mapped them by title (confirmed by `gh pr view`).
- Caveat 2: Macroscope threads end with "Sorry, I'm unable to act on this request because you do not have permissions" on every thread; ignore that line as noise.
- Caveat 3: the fix PRs repair a feature that never reached `main`; severity is "user-visible bug in an unreleased redesign".

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31535 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 4 | data integrity | yes | In queue mode the "draft changed during attachment upload" check was skipped, so edits typed while uploads ran were cleared without being sent. Reply: fixed in 06cef8f3b2 (check now runs for every send). Outdated+resolved. |
| 31535 | 2 | MS | High | real-minor | ignored | 2 | 4 | state machine | no | Switching thread A to B while A's upload is pending cancels A's send because shared composer refs now describe B. Unresolved, no reply (unverified). |
| 31529 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | UI state | no | Settled menu snapshot stale when thread suggestions arrive late; next keystroke drops them. Fixed in f51e81f with browser regression. |
| 31485 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Hint placement captured composer as null before the deferred chat mounted. Reply: reproduced in Chromium, fixed b4b2d74544. |
| 31485 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Clearance measured through the stage zoom (132px instead of 252px for a 240px composer at 0.5 scale). Reply: reproduced, fixed 5628442775. |
| 31485 | 3 | MS | Critical | unclear | ignored | 1 | 3 | state machine | no | Claims `seen.placed !== slotByTabId` loops forever because `slotByTabId` is a fresh Map each render. I read the merged file: the Map is built by an inline IIFE at line 460 and compared at line 1071, so it is a new Map each render and the claim is plausible by reading. But the whole redesign shipped to testers with panes displaying and the author says it is old base code, so something else (compiler memoization, or a different guard) probably prevents it. Not resolved either way. Repeated as #31390 T1. |
| 31482 | 1 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Test already passes on base; remove. Done in e7193b69c4. |
| 31482 | 2 | MS | Medium | real-minor | ignored | 2 | 3 | cross-file contract | no | Unnamed workspace gets generic "Workspace" label when the pane's active tab is not a chat. Author: base-branch code, left. Repeated as #31390 T2; code still there at 66bca5ddfb (selectLayoutWorkspaceLeadTab) but #31262 later changed it. |
| 31469 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | `commitLayoutDrop` returns true for a no-op drop so the drop flag stays armed and spoils the next split animation. Fixed 94359fce48. |
| 31469 | 2 | MS | Medium | real-minor | ignored | 2 | 3 | data integrity | yes | Dragging an already-open thread between tabs lands at the wrong index ([B,C,A] instead of [B,A,C]). Verified: merge 0159f98f6f layoutDrag.ts:300 still filters only `source.kind === "tab"`. Author: base code, left. |
| 31469 | 3 | MS | Medium | real-minor | ignored | 2 | 4 | state machine | no | `key === null` early return leaves running slides animating with old offsets. Base code, left (unverified). |
| 31469 | 4 | MS | High | unclear | ignored | 2 | 5 | state machine | no | Dropped tab that reuses an element with a running slide keeps the old translation. Unresolved, no reply (unverified). |
| 31462 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Close confirmation labels every shell "Terminal" instead of the command. Fixed ec16dca335. |
| 31462 | 2 | MS | Medium | real-bug | fixed-elsewhere | 3 | 4 | cross-file contract | yes | In `always-shrink` mode a divider drag does not land at the pointer (0.6 share + untouched neighbour renormalizes to ~545px instead of 600px). Author: fixed in #31406, not this PR. Same bug as #31424 T1. |
| 31435 | 1 | MS | Medium | real-minor | ignored | 2 | 4 | state machine | no | `key` becoming null during a resize drag leaves slides running. Base code (unverified). Same as #31469 T3. |
| 31435 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Tab switched mid-slide jumps to destination; reply "Real", fixed 0c81eb7237. |
| 31435 | 3 | MS | High | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | `wasOf` rereads mutable `slides` map so a later tab inherits the wrong offset. Reply "Real", fixed ff01963fef (snapshot first). |
| 31425 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Pending pane placement not consumed when opening an existing singleton surface, so the next new surface lands in the wrong pane. Fixed 8f339df770 with test. |
| 31425 | 2 | MS | Medium | real-minor | ignored | 2 | 3 | error handling | no | Browser open failures other than settings-read give no tab and no toast. Base code, left (unverified). |
| 31424 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Always-shrink drag from 600px to 720px renders at 655px (shares renormalized). Fixed 21f3952124 (take width from the right neighbour) with test. Strong example: needs the `selectLayoutPaneSlots` renormalization in view. |
| 31390 | 1 | MS | High | unclear | ignored | 1 | 3 | state machine | no | Same "too many re-renders" claim as #31485 T3. See that row. |
| 31390 | 2 | MS | Medium | real-minor | ignored | 2 | 3 | cross-file contract | no | Same as #31482 T2 (lead tab label). Left to base. |
| 31390 | 3 | MS | Medium | real-minor | ignored | 2 | 2 | UI state | no | Wheel events pan the overview stage while the command palette is open (no `isCommandPaletteOpen()` check). Base code, left (unverified). |
| 31268 | 1 | MS | Medium | real-minor | ignored | 2 | 3 | cross-file contract | no | Live-render width in overview divided by `window.innerWidth`, so wide panes stay thumbnails with sidebar open. Base code, left (unverified). |
| 31265 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | UI state | no | `pointer-events: none` on sidebar is undone by a child with `pointer-events-auto`, so the Woke dismiss button is clickable under the overview. Fixed b5437f38ba with `inert`. |
| 31265 | 2 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Style rule: move sidebar CSS into Tailwind in the component. Done in 9cbce75. |
| 31262 | 1 | MS | High | real-minor | fixed-before-merge | 2 | 4 | data integrity | no | Empty focused workspace in the middle is appended last, highlighting the wrong pill ([A,C,B] instead of [A,B,C]). Fixed f26db5f572 with test. |
| 31262 | 2 | MS | Medium | real-minor | ignored | 2 | 4 | state machine | no | Background insertion normalizes layout before restoring focus, which can delete the user's focused empty workspace. Base code, left (unverified). |

## 3. Track B (escaped bugs)

Skipped as trivial: #31395 (one-line list alignment), #31387 (gap colour), #31384 (removes snap ticks, -18 lines). #31514 is a pure addition (no SZZ target).

Bots at intro: **#28845 (layer 6) was never reviewed by Macroscope** ("skipped: per-review cost limit exceeded, estimate $34.23 vs $15.00 limit") and CodeRabbit left only a summary comment. So for every layer-6 row the answer is bots-did-not-run. #28840 (layer 2) was reviewed (CodeRabbit 24 + Macroscope 8 inline threads, none on the composer menu, modifier or timeline code touched by these fixes).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 31535 | Choosing Queue while an approval was pending declined that approval first; a second send while the first was saving failed silently | none clear. SZZ #23062 (refactor, 37 lines) and `approvalRedirectNotice` came from #22734 / #23095 refactors; behaviour traces to the pre-refactor ChatView send path | low | n/a (origin is refactors of old code) | 3 | 4 | Behaviour predates the refactors; no feature PR identified. |
| 31529 | @ menu dropped file results while each search ran, collapsing the menu and moving highlight | #28840 "feat(web): redesign composer and conversation timeline" (e9a083d8; 6 lines; #1905 has 15 lines but is an old skill-discovery PR whose lines were reworked) | medium | missed (bots reviewed #28840, 32 inline threads, none on menu loading state) | 2 | 3 | Fix replaces list logic wholesale. |
| 31524 | Holding a modifier shifted the composer (layout jump) | #28840 (e9a083d8, 5 lines) | medium | missed | 1 | 2 | CSS/UI behaviour. |
| 31518 | Tasks tray flashed the previous turn's plan on send | commit 53eedd98 "fix(chat): settle completed tasks and cap the prompt at eight lines" (2 lines; no PR resolved) | low | unknown | 2 | 3 | |
| 31516 | Steered turns lost the cut-off attempt and showed two timers | #28840 (e9a083d8, 3 lines; rest are old refactor lines) | low | missed (no thread on session-logic/timer) | 2 | 4 | |
| 31514 | Sending a workspace's only pane away flashed the launcher | no SZZ target (pure addition) | n/a | n/a | 1 | 3 | |
| 31485 | Workspace pill lagged behind its pane (React state), landed in wrong place, hidden by composer | #28845 (fcdbd455, 60 of 68 blamed lines) | high | did not run (Macroscope skipped, cost limit) | 2 | 4 | Four visual cases. |
| 31482 | "Move tab to workspace above" did nothing in the top workspace | #28845 (4 of 4 lines) | high | did not run | 2 | 2 | Easy once you compare with the symmetric bottom case. |
| 31475 | Leaving a terminal for an empty workspace jumped focus back | #28845 (2 of 2) | high | did not run | 2 | 4 | |
| 31469 | Dropped pane slid in from where its tab used to be | #28845 (8 of 9) | high | did not run | 2 | 3 | |
| 31462 | Pane chrome differed by how it was opened (keyboard resize band, labels, etc.) | #28845 (131 lines; also older #7318, #3093 lines reworked) | high | did not run | 2 | 3 | Collection of 13 small fixes. |
| 31450 | Streaming chat at the end lost end-position in the frame its pane shrinks | #3587 / #9146 (old timeline code, 3 lines each), not the redesign | low | unknown (old PRs) | 2 | 5 | Timing-dependent; low confidence. |
| 31435 | Panes moving aside for a new left column jumped instead of sliding | #28845 / #30002 (4 lines; #30002 is a stacked PR) | medium | did not run for #28845 | 2 | 4 | |
| 31433 | Switching tabs reset a chat's scroll position | #31585 (1 line), then #28845 | low | n/a | 2 | 3 | |
| 31425 | "+" menu opened new tabs in a different pane | #28845 (12 of 12) | high | did not run | 2 | 3 | |
| 31424 | Shrinking a column while scrolled right ran away to minimum width | #28845 (23 of 23) | high | did not run | 3 | 4 | Scroll change read as pointer movement. |
| 31397 | One click did not work anywhere in an unfocused pane | #28845 (27 of 27) | high | did not run | 2 | 3 | |
| 31390 | Top-left tab jumped when overview zoomed in | #28845 (34 of 34) | high | did not run | 2 | 4 | |
| 31389 | Overview did not fade out sidebar toggle; Cmd+B not ignored | #3497 / #4130 (old sidebar lines, 10 and 6) with the redesign wrapper | low | unknown | 1 | 2 | |
| 31268 | Holding the workspace key showed black frames and restarted the slide | #28845 (8 of 8) | high | did not run | 2 | 4 | |
| 31265 | Sidebar behind the zooming overview (z-index order) | #28839 (47b6fa97, 14 lines) and #28845 (10 lines) | medium | #28839 reviewed (Macroscope 7+, CodeRabbit 1); none on z-order (unverified) | 1 | 2 | Visual only. |
| 31262 | Workspace pill misnamed workspaces and capped bars at 5 | #28845 (28 of 28) | high | did not run | 2 | 3 | |

## 4. Catalogue candidates (severity >= 3)

All three are Track A (fixed before merge); head is the commit the bot commented on, base is its first parent. No Track B row reaches severity 3 with a clean introducing PR.

- `composer-queue-send-drops-edits-during-upload` (PR #31535, caught by Macroscope, High). Golden: with Queue mode the draft-changed-during-upload check is skipped, so text or attachments added while uploads run are cleared without being sent. base `0f9e14ac67aa5651507a247b8c56078faa8ad399`, head `46dc91738f16068be10d426a1ea3e3bd571749ed`.
- `column-resize-always-shrink-drag-misplaces-divider` (PRs #31424 T1 and #31462 T2, caught by Macroscope). Golden: in always-shrink mode the dragged column's share is set directly while all shares are renormalized, so the divider ends near 655px when released at 720px; the neighbour must give up the width. base `81f2ca8faee5c46aabeba23d078ea38097b8c690`, head `8240b6351c9041ce4a8c06f65d31ca4475dc1bb3` (alternate for #31462: base `ac324f907ed490c624cae43156c42ef58400466b`, head `a4f65c63ce3993b8914948b3cce20837cd12bc40`).
- `surface-host-render-loop-claim` is NOT a candidate (unclear, probably wrong).

## 5. Observations

- Macroscope is the only reviewer on these PRs. It finds real, concrete bugs in fix PRs (3 real-bug, 20 real-minor of 28), and the author replied "Real" or fixed with a regression in 14 cases, often with a test that fails before the fix.
- Macroscope refused to review the 42k-line layer-6 PR (#28845), where most of this chunk's bugs were introduced. It then reviewed each small fix PR and found base-branch bugs there; the author answered 8 of those with "comes from the base branch, leaving it". Those bugs shipped as unreviewed code. A bot that skips large PRs reviews them later by accident, only if a fix touches the file.
- Repeats: the same base-branch issue (SurfaceHost "too many renders", lead-tab label, `key === null` slides) was flagged on 2-3 consecutive PRs, because it stays unfixed in the base. No dedup across PRs.
- Severity labels are loose: one "Critical" (render loop) that the app evidently survives, while the "High" real bug (#31535 T1) is a quiet data-loss case.
- Macroscope also posts rule-style comments with no severity (test rules, "Tailwind in the owning component"), which authors act on (#31482 T1, #31265 T2).
