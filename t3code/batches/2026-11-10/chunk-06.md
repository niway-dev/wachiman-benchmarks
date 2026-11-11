# Chunk 06: PRs #31823..#31537 (2026-11-10)

## 1. Header

- PRs covered: 25 (#31823 .. #31537), all by flamboh, all 2026-11-10 03:54-04:49 UTC. 19 have no bot thread. All are `fix`/`perf` PRs inside the unmerged "redesign" stack (bases are other stack PRs' merge commits, not main). Bodies note "GPT-6.1 Sol / Claude Opus 5.5 on behalf of Oliver".
- Bot threads: 10 total. CodeRabbit 0, Macroscope 10 (#31598 x6, #31595 x1, #31594 x2, #31573 x1). CodeRabbit left nothing here.
- Verdicts: real-bug 1, real-minor 2, nit 7 (six style threads on #31598 plus #31595 T1), unclear 0, wrong 0.
- Outcomes: fixed-before-merge 4 (#31594 x2, #31573 T1, #31595 T1 restyled), unknown/stale 6 (#31598; author reply: lines now belong to the base layer), ignored 0, disputed 0.
- Code checked: #31594 T1 (menu.tsx at 2538cb92), #31594 T2 (focus-return.ts at dde82a1a), #31573 T1 (KeybindingsSettings.tsx at d71128e5). Everything else is from thread text (unverified).
- Track B: 24 fix PRs, 9 non-trivial with SZZ run (1 pure addition: #31553). Big caveat: the redesign was developed on stack branches whose intermediate commits (marked `?sha`) were never squash-merged to main, so SZZ shows `?` commits that belong to open stack PRs #28839-#28845 (all still OPEN on 2026-11-11, bases `maria/redesign/N-*`). "Introducing PR" below means the stack layer, which has no merge date.
- Replay caveat: `base` in raw.jsonl is the stack parent commit, so replays need that parent present (it is in the clone, unverified for replay).

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31598 | 1 | MS | none | nit | unknown (stale) | 1 | 1 | other | no | Test Signal: remove bar-position visual test. Author reply: flagged before rebase, lines now come from the base layer (unverified). |
| 31598 | 2 | MS | none | nit | unknown (stale) | 1 | 1 | other | no | Remove static error-banner copy test. Same stale reply. |
| 31598 | 3 | MS | none | nit | unknown (stale) | 1 | 1 | other | no | Remove clerk theme styling test. Same stale reply. |
| 31598 | 4 | MS | none | nit | unknown (stale) | 1 | 1 | other | no | Remove composer rim geometry test. Same stale reply. |
| 31598 | 5 | MS | none | nit | unknown (stale) | 1 | 1 | other | no | Remove copy-text test. Same stale reply. |
| 31598 | 6 | MS | none | nit | unknown (stale) | 1 | 1 | other | no | UI Consistency: move min-width calc to a Tailwind class. Same stale reply. |
| 31595 | 1 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Move static slide-frame styles from index.css to component classes. Outdated, "no longer relevant as of 9fe1d96e" (unverified). |
| 31594 | 1 | MS | Medium | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | `tooltipSafeFinalFocus(props.finalFocus)` makes an omitted `finalFocus` an explicit callback, so Base UI skips its outside-focus check and focus is stolen back to the trigger after a menu closes on an outside input. Verified at 2538cb92 (menu.tsx:85 wraps unconditionally). Fixed in dde82a1a with regression test. |
| 31594 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | maybe | Focus guard uses `popup.contains(activeElement)`, which is false for a separately portaled submenu, so focus is not returned to the root trigger when a submenu item closes the tree. Guard at dde82a1a matches the description (focus-return.ts:26 `!popup?.contains`). Fixed in bb2df5f0. |
| 31573 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | race/ordering | yes | Escape in the new-binding recorder calls `onCancel()` without the `isSaving` guard that the row and the Cancel button have, so a pending save's success handler can discard a newly opened draft. Verified at d71128e5 (captureKeybinding Escape branch calls onCancel unconditionally, while other paths check isSaving). Fixed in 3ef358c9. |

## 3. Track B (escaped bugs)

Skipped as trivial or non-source: #31768 (removes launch toasts, behavior change), #31603/#31596/#31588/#31583/#31581/#31576/#31569/#31563/#31558/#31552/#31550/#31547/#31537 (CSS, layout, copy, hover/focus polish, one-line fixes; no SZZ), #31600 and #31598 (breadcrumb layout), #31595 (perf, not a fix).
Bot check: Macroscope/CodeRabbit comments on the introducing stack PR were listed filtered by the file names in question (only exact files), so "missed" means no bot comment on those files (unverified for the exact lines).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 31823 | Sidebar highlighted every thread visible in any pane as selected, not only the focused pane's thread | stack layer #28845 "feat(web): add workspace panes and transitions" (OPEN; commit fcdbd455, 6 of 6 lines) | high | missed (no bot comment on SidebarThreadRow/SurfaceHost) | 1 | 2 | Looks like a design reversal (comment "pen r45lm" removed), not a defect. |
| 31625 | "Working" indicator vanished between sending a message and the turn starting | #9293 "feat(providers): add context compaction command" and #26238 "chore: delete 18k lines of code" (1 line each) | low | missed on ChatView (bots on #9293 flagged other ChatView lines) | 2 | 4 | SZZ lands on unrelated lines; real origin is the send-to-start phase logic (unverified). |
| 31603 | Sidebar hover cards appeared while scrolling | #20448 "rc/01 tooltips", #89 (noise), #15455 "dismiss hovered timeline tooltips on scroll" | low | not checked | 1 | 2 | Behavior polish; no clear introducing line. |
| 31587 | Sidebar did not keep the open thread in view when a new thread sends and shelves open | #9731 "feat(web): drag threads across sections with consistent motion" (8 of ~25 lines; also #13926, #2829 noise) | low | not checked | 2 | 3 | Sidebar.tsx rewritten over many PRs; no single origin. |
| 31553 | Timeline position was restored after paint, causing a visible jump on open/send | no SZZ target (pure addition) | n/a | n/a | 2 | 3 | Needs layout-effect ordering knowledge (unverified). |
| 31573 | Settings showed the new page title over the previous page's content while the route loaded; Escape in a new shortcut recorder left its draft; sheet close lost focus | spread over `?03828335` (stack layer #28842 "redesign settings and setup surfaces", OPEN) and older #24847, #2533, #27151 | low | missed (CodeRabbit rate-limited on #28842's KeybindingsSettings; Macroscope only asked to delete a copy test) | 2 | 3 | Three separate small defects in one PR. |
| 31594 | Returning focus after a dialog/context menu reopened its trigger's tooltip away from the pointer; nested dialogs not opaque | #20448 "rc/01 tooltips" (2 lines), #21960 "dialogs keep their content while they close" (1 line), #89 noise | low | not checked | 2 | 4 | Tooltip focus handling is cross-library behavior (Base UI). Fix itself introduced two regressions that Macroscope caught. |
| 31605 | Layout introduction and tour could not be used from the keyboard | `?8f6727d7` (12 lines), `?fcdbd455` (7) = stack layer #28845 "workspace tabs with a guided tour" (OPEN) | medium | missed (no bot comment on LayoutOnboarding/pageNavigation/Overview) | 2 | 3 | Accessibility gap in a new feature. |
| 31624 | File approval and superseded-attempt rows were unclear in the timeline/composer | `?374a0e96` etc. = stack layer #28840 "redesign composer and conversation timeline" (OPEN) | low | partial (CodeRabbit left 3 approval-panel comments on #28840, all fixed; none on the unclear labeling) | 1 | 2 | UX copy/clarity. |

Bot coverage on SZZ-traced bugs: caught 0, missed 6, not checked 3 (#31603, #31587, #31594).

## 4. Catalogue candidates (real bugs, severity >= 3)

| id | PR(s) | golden description | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| menu-final-focus-wrap-steals-outside-focus | #31594 | Wrapping `props.finalFocus` unconditionally (`tooltipSafeFinalFocus(props.finalFocus)`) turns an omitted finalFocus into an explicit callback, so Base UI skips its outside-focus check and a closing menu steals focus back from an outside input; only wrap when finalFocus was supplied. | f0ffe9abfed52d93e0c82747805979163d824243 | 2538cb92060543f91fdc3df17bdffbaf82381e4d | Macroscope (fixed before merge in dde82a1a) |

Borderline (sev 2, not promoted): #31594 T2 (submenu portal focus), #31573 T1 (Escape during pending save drops a draft).

## 5. Observations

- Macroscope found the only real defects (all 3 of its non-style threads), all on author-owned PRs where the author answered each one and added a failing-first regression test. Its "reply" requests return "no permissions" (same as other chunks).
- 7 of 10 threads are Macroscope style rules ("Test Signal": delete the test; "Tailwind in the owning component"). On #31598 all six were stale after a stack rebase and dismissed with one templated reply, so the rule-based noise costs a reply, not a fix.
- CodeRabbit was silent on all 25 PRs (unverified why; it was rate-limited on the parent layer #28842).
- Stack-development hides history: SZZ resolves to unmerged intermediate commits, so introducing-PR attribution is a stack layer with no merge date, and bots reviewed those layer PRs (15k+ lines, 100s of files), where per-file bot coverage is thin.
- Bugs here are small UI-state defects; the one fix PR whose own fix needed two bot rounds (#31594) shows fix-the-fix regressions are where the bot paid off.
