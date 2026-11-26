# kaipu-bench-wachi-v3#56 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:337 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Row cards drop "up to" for YouTube / Vertical / Square, unlike the stage (confidence high)**

The row gets `sizeText: estimateText`, and `estimateText` (lines 241-244) never says "up to": for a fixed-canvas preset (`sizeKindOf` returns "up-to", `export-size.ts:34-37`) the card shows `~X MB` (`sizeAbout` = "~{size}"). The stage, using `sizeText` (lines 245-248), shows "up to ~X MB" for the same plan. The two numbers match, but the card presents a ceiling as a typical size. Also, the `DestinationSizes.sizeText` doc in `destination-row.tsx:13` still lists "up to ~570 MB" as a possible value. If the cards are short on purpose, update that doc. If they are not, pass `sizeText`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:279 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Enter on a focused card with nothing selected does nothing (confidence medium)**

When `selected` is null, the first card has the tab stop (`destination-row.tsx:73`). If a keyboard user tabs to it and presses Enter, `isPrimaryEnter` returns true because a `role='radio'` button is not excluded (line 384). The handler then calls `preventDefault()`, which cancels the button's own click, and `primary()` returns early because `plan` is null (line 263). So nothing is selected and nothing is exported, and the screen gives no feedback. One fix is to let Enter fall through to the card's click when nothing is selected. Another is to make the first Enter select the focused card.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A file dropped on the Library now replaces the app window with the file (confidence high)**

This change removes `useFileDrop` from the Library. That hook was the only thing on this screen calling `preventDefault` on window `dragover`/`drop` (`features/library/hooks/use-file-drop.ts:29-47`). The hook's own docstring says why that matters: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`use-file-drop.ts:9-11`). The main process does not guard against this: it sets `setWindowOpenHandler`, but nothing listens for `will-navigate` (`main/index.ts:400-403`).

So a user who drops an MP4 on the Library, which until this PR was where you dropped videos, gets the main window navigated to `file:///…/video.mp4`. The renderer is unloaded and the app UI and its state are gone until a reload. The PR body says "dropping a file there does nothing", but that is not what happens.

Suggested fix: keep a window-level guard that calls `preventDefault` on file `dragover`/`drop` everywhere outside Export. This could live in the shell, or be a `will-navigate` handler in main that blocks `file:` URLs. Alternatively, leave the Library's drop handler in place and have it route the files to Export. The same default already applies on every other screen except Export, so a shell-level guard covers all of them.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: An Email export changes its name to "Slack · Discord" once it finishes (confidence high)**

The in-progress row takes its logo from `running.destination` (line 50), which can be `email`. The finished row takes it from `destinationOfPreset(copy.export!.preset)`, and for `balanced` that always returns `chat` (`features/prepare/destinations.ts:102-107`). So the strip shows an Email export as Email while it runs, then relabels it as Slack · Discord when it is done. The PR body acknowledges the `destinationOfPreset` mapping, but this strip makes the change visible. If the job's destination isn't persisted on the copy, a neutral name for `balanced` copies here would avoid the switch.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The new "copy in progress" part of the Export badge has no test (confidence high)**

`useExportBadge` now adds 1 while `status === "exporting"`, and the label `export.railBadge` says "in progress or ready". `sidebar.test.tsx` only drives `noteFinishedCopy`. It never puts the export runner into `exporting`, so nothing checks the running half of the count. That includes the hand-off when the export finishes: the count goes from 1 (running) to 0, because `ready` is set and that copy's ready card is on screen (`export-runner.ts:462`, `ready-copies.ts:74`). It could just as well go to 1, if the copy is counted as unannounced. Consider adding a test that starts an export (or mocks `useExportRunner`) and checks the badge while it runs and after it finishes.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟠🧪 **Fix · tests: The new test treats an unhandled drop as correct, but in the real app that drop replaces the Library window with the file (confidence medium)**

This test checks that a file dropped on Library is not imported. It does not check what happens to the drop instead. Only the Export screen (through `usePrepareImport`) now mounts `useFileDrop`. Nothing in `src/renderer/src/app` handles drag or drop, and `main/index.ts` has no `will-navigate` guard. `use-file-drop.ts:10-11` says why that matters: "a file dropped where nothing handles it makes Electron navigate the window to that file". So a video dropped on Library, which Library used to import, now navigates the main window to the `.mp4` and the app UI disappears.

The test also passes for a second reason. It checks `importVideoFiles` right after the drop, with nothing awaited and no `pathForFile` stub. A handler that called it after one microtask would still pass.

Suggested change: on Library, keep the window drop guard (call `preventDefault` on dragover and drop) even without importing, or redirect drops to Export. Then have this test check `fireEvent.drop(...)` returns false, as `dropFiles` does at `export-page.test.tsx:416`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:285 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The "Enter exports, from the page or a card" test only presses Enter on a card (confidence high)**

The test fires only `keyDown(card(/^YouTube/), Enter)`. The page-level path, where the target is `document.body` and `isPrimaryEnter` gets no closest match, is never exercised with a destination selected. Line 165 presses Enter on the body only with nothing picked. Add a `fireEvent.keyDown(document.body, { key: "Enter" })` case, or rename the test. Likewise, the test at line 251 says "the cards say where it went" but only checks the start arguments.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only checks the URL with a video (confidence high)**

The test name promises that the Export link is active on both `/export` and `/export/:assetId`, but it only renders `/export/asset-1`. The bare `/export` case is the one that depends on `isActive` using `end: false` against `ROUTES.exportNew` (`sidebar.tsx:68-69`, `:53`). Add a second `renderAt(ROUTES.exportNew)` check, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The badge's new "in progress" count has no test (confidence medium)**

`useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (`sidebar.tsx:121-122`), and the label reads "N copies in progress or ready". Every test here drives only `noteFinishedCopy`, so the running count, and how it combines with a finished copy, is never exercised in this file. Consider a test that mocks the runner's `status` as `"exporting"` and checks the badge shows 1, then 2 once a finished copy is noted.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.module.css:4 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡📝 **Consider · docs: The header comment gives the minimum window size as the size the app opens at (confidence high)**

This header was partly rewritten in this PR. It still says the layout is sized for "the window the app opens at (900 × 670)", but the main window opens at 1040 × 760, and 900 × 670 is its `minWidth`/`minHeight` (`src/shared/window-size.ts:50`). Since the stage and row rely on fitting that space, say "the smallest window (900 × 670 minimum)" instead.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T00:11:39Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment for the removed import drop strip (confidence high)**

The `.importZone` rule was deleted, but its comment ("NIW2-579: the \"Drop a video here\" strip, between the header and the toolbar.") still sits right above the `.stickyBar` comment. It now describes something that isn't there and reads as if it belongs to `.stickyBar`. Remove the line.

<!-- wachi:finding -->
