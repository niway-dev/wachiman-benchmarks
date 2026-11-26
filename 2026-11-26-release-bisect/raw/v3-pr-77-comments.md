# kaipu-bench-wachi-v3#77 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T06:03:25Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: Library no longer intercepts window file drops, so Electron's default drop navigation may replace the app (confidence medium)**

Before this change, the Library mounted `useFileDrop`, which calls `preventDefault()` on `dragover` and `drop` for the whole window (`features/library/hooks/use-file-drop.ts:29-51`). This PR removes that hook, and I found no other guard: a search for `will-navigate` and for `dragover`/`drop` listeners in `apps/kaipu-record/src` matches only `use-file-drop.ts`.

In Chromium/Electron, when nothing cancels a file drop, the default is to navigate the window to `file:///…/video.mp4`. That would replace the renderer with the bare file and drop all app state. Step 12 of the PR's test plan says "dropping a file there does nothing", but nothing in the code makes that true.

Suggested fix: keep a window-level `dragover`/`drop` `preventDefault` on the Library that imports nothing (or add one at the shell level), or block `will-navigate` in the main process.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-26T06:03:25Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: An Email export shows as Email while running, then as Slack · Discord once finished (confidence high)**

The in-progress row uses `running.destination ?? destinationOfPreset(...)` (line 50), so an Email job shows the Email logo. A finished row uses only `destinationOfPreset(copy.export!.preset)`, which returns `chat` for `balanced` (`features/prepare/destinations.ts:102-107`). So the same copy changes from Email to Slack · Discord the moment it completes.

The PR body accepts `destinationOfPreset("balanced") === "chat"`, but this strip shows the change inside one session. If the export's destination is stored with the copy, use it here too.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121 · github-actions[bot] · 2026-11-26T06:03:25Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Running export counts on the badge even while its progress card is on screen (confidence medium)**

`libraryBadgeCount` leaves out the copy whose ready card is on screen, because "that card already says it" (`ready-copies.ts:66-75`). The new `running` term adds 1 whenever `status === "exporting"`, even when the progress card is visible (`progressHidden` false; see `export-status-cards.tsx:35-37`) and even when the user is already on `/export`. The finished-copy rule and the in-progress rule now disagree. If the badge is meant to point at work the user can't see, `status === "exporting" && progressHidden` would match the ready-card rule. If it is meant to always show a running export, the docstring at lines 105-109 could say so.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:85 · github-actions[bot] · 2026-11-26T06:03:25Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: A file dropped on the Library is no longer intercepted, and this test locks that in (confidence medium)**

Library used to mount the window-wide drop guard. `useFileDrop` is now mounted only by `usePrepareImport`, which only Export uses (`features/prepare/use-prepare-import.ts:55`). The hook's own comment says why the guard exists: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`). I searched `src/main` for a `will-navigate` handler and found none; only `setWindowOpenHandler` (`main/index.ts:400`), which does not cover a drop. So dropping a video on the Library, the screen people used to drop onto, should now replace the whole app UI with the file. This test only checks that `importVideoFiles` is not called. It never checks whether the drop's default was prevented, the way `dropFiles` does in export-page.test.tsx:416, so it passes in exactly that case. Two possible fixes: keep a window-level guard that prevents `dragover`/`drop` for files outside Export (at the app shell, or with `will-navigate` in main), or assert here that `fireEvent.drop(...)` returns false.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T06:03:25Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "with and without a video" only checks the with-a-video URL (confidence high)**

The test name says the Export link is active on Export with and without a video, but it only renders `/export/asset-1`. `/export` (ROUTES.exportNew), the URL with no video, is never checked for `aria-current="page"`. The sidebar matches that path with `end: false` (`sidebar.tsx:68-69`, `sidebar.tsx:53`), so it works today. Still, the name promises coverage the test doesn't have. Add `renderAt(ROUTES.exportNew)` with the same assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T06:03:25Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: The running-export part of the badge is not covered (confidence medium)**

`useExportBadge` now adds 1 while an export is running (`status === "exporting"`, `sidebar.tsx:121`). The badge label also changed to "in progress or ready". Every test here only drives `noteFinishedCopy`, so nothing checks that an export in flight shows on the rail, or that it is not counted twice once it finishes and becomes `ready`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T06:03:25Z

👮 **Wachiman** · Nit · 🟡🧹 **Consider · cleanup: Orphaned comment about the removed drop strip (confidence high)**

The `.importZone` rule was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits directly above the toolbar's own comment, so it reads as if it describes the sticky toolbar. Delete the line along with the rule.

<!-- wachi:finding -->
