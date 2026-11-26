# kaipu-bench-wachi-v3#75 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-26T06:03:21Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Enter starts an export behind an open "Change video" list (confidence medium)**

`destinationStep` ignores keys inside `[role='dialog']` (line 364), but `isPrimaryEnter` has no such check. `VideoPicker` renders its list as `role="dialog"` (`pages/export/video-picker.tsx:71`) and closes only on Escape or an outside mousedown. While the list is open, focus can leave the trigger button, for example after a click on the panel's padding or its empty text. If the user then presses Enter, the event target is `body` or a non-button node inside the dialog, so `isPrimaryEnter` returns true (line 381). The document listener then calls `primary()` and starts encoding the selected destination while the list is still open. Fix: add the same `target.closest("[role='dialog']")` guard here, or skip Enter while a picker is open.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:40 · github-actions[bot] · 2026-11-26T06:03:21Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: "Pick from Library" stays enabled during an import (confidence medium)**

"Browse files…" is disabled while `importing` (line 51), but the `VideoPicker` trigger is not. If the user picks a Library video while a dropped file is still importing, Export opens on the picked video. When the import finishes, `usePrepareImport` navigates to the imported file (`features/prepare/use-prepare-import.ts:48`), so the screen switches to another video without the user asking. Fix: disable the trigger while `importing`, as the other button is.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T06:03:21Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: A file dropped on the Library now opens that file in the app window, replacing the app (confidence medium)**

The Library no longer calls `useFileDrop`. That hook's own comment says it exists because "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-11`). The only other caller is `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which is mounted only on Export. Main has no `will-navigate` guard: `main/index.ts` only sets `setWindowOpenHandler` (line 400), and nothing in `src/` intercepts `drop` or `dragover` apart from this hook.

So dragging an MP4 from Finder onto the Library no longer "does nothing", as the PR says (test step 12). Chromium's default runs: the window navigates to `file://…/video.mp4`, the renderer UI is gone, and no error is shown. Before this change the Library caught the drop and imported the file.

Fix: keep a window-level guard while the Library is mounted, or better app-wide in the shell, that calls `preventDefault` on `dragover`/`drop` for file drags. Add `will-navigate` prevention in main as a backstop. Confidence is medium because I could not run Electron to watch the navigation happen.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:201 · github-actions[bot] · 2026-11-26T06:03:21Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: The 1440p / 4K and Fill / Fit radio groups do nothing on arrow keys (confidence high)**

`destinationStep` ignores arrows inside any other `[role='radiogroup']` because, its comment says, that group "answers its own arrows" (`pages/export/export-page.tsx:351-363`). Neither radiogroup here (lines 201 and 233) has an `onKeyDown`, and every radio is a separate tab stop. With focus on one of these radios, ←/→ do nothing: they don't switch the option, and they don't move the destination either. Either add roving arrow handling (as the ARIA radiogroup pattern expects) or let the screen's arrows through here.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121 · github-actions[bot] · 2026-11-26T06:03:21Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: The running export is counted even while its progress card is on screen (confidence medium)**

`libraryBadgeCount` leaves out the copy whose ready card is on screen, because that card already says it (`ready-copies.ts:66-75`). The new `running` term adds 1 whenever `status === "exporting"`, even when the progress card is visible (`progressHidden` is false, `export-runner.ts:107`). The rail therefore shows a badge for the same export the progress card shows. The runner is also the editor's export pipeline, so an editor export lights the EXPORT badge and its label says "copy in progress". If the badge is meant to follow the same rule as the ready card, use `status === "exporting" && progressHidden ? 1 : 0`. Otherwise, a comment saying the running count is deliberate would help.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T06:03:21Z

👮 **Wachiman** · Important · 🟠🧪 **Fix · tests: "Does not take a dropped video" passes while the drop navigates the Electron window to the file (confidence medium)**

This test only checks that `importVideoFiles` is never called. It never checks whether the drop's default action was prevented. With this PR the Library no longer mounts `usePrepareImport`/`useFileDrop`, and `usePrepareImport` is the only caller of `useFileDrop` (`features/prepare/use-prepare-import.ts:55`). So nothing on the Library calls `preventDefault` on `dragover`/`drop`.

The hook explains why that matters: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`). Main has no `will-navigate` guard either: only `setWindowOpenHandler` is set (`main/index.ts:400-403`). So a video dropped on the Library replaces the app with the file. The PR's step 12 says "dropping a file there does nothing", and this test is meant to pin that, but it cannot catch the navigation.

The Export test already checks this through the return value of `fireEvent.drop` (`export-page.test.tsx:414-416`). Do the same check here, `expect(fireEvent.drop(...)).toBe(false)`, and it will fail. The real fix belongs in the Library page or the shell: a window-wide guard that only prevents the default drop, or a `will-navigate` block in main.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T06:03:21Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "active with and without a video" only checks the case with a video (confidence high)**

The test name says the Export link is active on `/export` and on `/export/:assetId`, but it only renders `/export/asset-1`. The case without a video (`ROUTES.exportNew`) is the one where the link's own `to` matches exactly, so neither path's `aria-current` is checked there. Adding `renderAt(ROUTES.exportNew)` with the same assertion, or renaming the test, would make it match its name.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T06:03:21Z

👮 **Wachiman** · Nit · 🟡🧹 **Consider · cleanup: Stale comment for the removed import drop strip (confidence high)**

The `.importZone` rule was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still here. It now sits right above the `.stickyBar` comment, so it reads as if it describes the sticky bar. Delete line 108.

<!-- wachi:finding -->
