# kaipu-bench-wachi-v3#69 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117 · github-actions[bot] · 2026-11-26T01:46:53Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Every Library re-list unmounts ExportScreen and throws away the user's destination, YouTube preset and framing (confidence medium)**

`if (isLoading) return …loading…` runs before the video checks. But `useLocalLibrary().refresh` sets `isLoading` back to true on every re-list (`use-local-library.ts:41-42`), not only on the first load. Re-lists are triggered from the hook itself. On mount it calls `refreshCloudCatalog()`, and when that succeeds main broadcasts `library:changed` (`main/library/index.ts:73-76`), which runs `refresh()` again (`use-local-library.ts:124-134`). Account changes, tag edits and imports broadcast the same event.

Each time this happens the page shows "Loading…" for a moment and `ExportScreen` unmounts. It comes back with `initialDestination={urlDestination}` (line 158). For a signed-in user, the card they picked a second after opening Export (and any 1440p/4K or Fill/Fit choice) can quietly reset to the `?to=` value or to "Where is it going?", with no error shown. The selection held in `chosen` (line 77) is never passed back in.

Fix: show the loading state only while there is nothing to render yet, e.g. `if (isLoading && !video)`. Or pass `current()` as `initialDestination` and keep the YouTube preset and framing in the page.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T01:46:53Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A file dropped on the Library now opens it in the main window and the app is gone (confidence high)**

The Library no longer calls `useFileDrop`. After this PR, Export (through `usePrepareImport`, `features/prepare/use-prepare-import.ts:55`) is the only caller in the renderer. No other code in the app calls `preventDefault` on `dragover` or `drop`. The main process has no `will-navigate` guard either: `main/index.ts:400-411` only sets `setWindowOpenHandler`.

The hook's own doc says what happens next (`features/library/hooks/use-file-drop.ts:10-11`): "a file dropped where nothing handles it makes Electron navigate the window to that file." So if a user drops an MP4 on the Library, which until now advertised that exact gesture, the main window loads `file://…/clip.mp4` and the React app disappears. Any export the renderer's runner is driving loses its UI. The user has to restart to get back.

The PR description says "dropping a file there does nothing". That is not what happens.

Suggested fix: keep a window-level guard that only cancels the drop (`preventDefault` on `dragover` and `drop`, no import) on screens that don't import, for example in the shell. Alternatively, add a `will-navigate` handler in main that blocks `file:` URLs.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:252 · github-actions[bot] · 2026-11-26T01:46:53Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: The before/after crop promises sharper text for LinkedIn · Feeds and TikTok · Reels, but those copies are not above 1080p (confidence high)**

The old `DestinationDetail` drew the text crops only for YouTube, whose 2560×1440 and 3840×2160 copies really are above 1080p. `UploadSizeCard` is now shown for every `send-more` destination, and `TextCrop` always pairs a blurred "Uploaded at 1080p" (`cropBefore`, en.json:917) with a sharp "Uploaded at {resolution}".

For `square` the canvas is 1080×1080 (`export-presets.ts:280`), so the sharp side reads "Uploaded at 1080 × 1080". That has fewer pixels than the blurred 1080p side. For `vertical` (1080×1920, `export-presets.ts:273`) it is the same density as 1080p. Either way the illustration shows the user an improvement the copy does not deliver, and nothing on screen says so.

Suggested fix: render the `crops` block only when the copy is actually larger than 1080p (YouTube, as before), or give the fixed-canvas destinations their own illustration.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:240 · github-actions[bot] · 2026-11-26T01:46:53Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Fill / Fit explanation is now only a hover tooltip, and the framing preview is gone (confidence medium)**

The old `ShapeCard` showed a `FramingPreview` of the thumbnail and printed `framingFitHint` / `framingFillHint` under the choice. Now the hint lives only in `title`, which keyboard users never see and screen readers announce inconsistently. Nothing else on the stage shows what Fill crops or what Fit pads. Consider bringing back a visible hint line under the radiogroup.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T01:46:53Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A file dropped on Library is now unhandled, so Electron opens it in place of the app; this test locks that in (confidence medium)**

The PR says "dropping a file there does nothing". This test only checks that `importVideoFiles` is not called. It never checks what the drop does by default, and jsdom never navigates, so the test passes either way. In Electron, nothing on the Library page or in the app shell intercepts the drop any more. The window-wide `useFileDrop` was the only drop listener in the renderer (`use-file-drop.ts:48-51`), and only `use-prepare-import.ts:55` mounts it now, i.e. only Export. The main process registers no `will-navigate` guard: `index.ts:400-403` only sets `setWindowOpenHandler`. The hook's own comment states what follows (`use-file-drop.ts:10-11`): "a file dropped where nothing handles it makes Electron navigate the window to that file."

So a user who drops an MP4 on Library, where drops used to work, has the main window replaced by the video file. The React app is unloaded, along with anything it was running, such as a background export. The PR notes the app was not run in Electron.

Suggested fix: keep a window-level drop guard while Library is mounted (preventDefault on dragover/drop for `Files`, with no import), or add an app-wide guard. Then assert it here the way `export-page.test.tsx:416` does: `expect(fireEvent.drop(document.body, …)).toBe(false)`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T01:46:53Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only checks the URL with a video (confidence high)**

The test renders only `/export/asset-1` and never `/export` (`ROUTES.exportNew`). The nav item points at `ROUTES.exportNew` and is matched with `end: false` (`sidebar.tsx:53`, `sidebar.tsx:68-69`), so if someone later sets `end: true` on it, the bare `/export` case would still pass here and the with-video case would break. Either render both paths, or rename the test to match what it checks.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:48 · github-actions[bot] · 2026-11-26T01:46:53Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The "in progress" half of the badge is not tested (confidence high)**

`useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (`sidebar.tsx:121-122`), and the label the tests assert reads "copy in progress or ready". Every test here only feeds finished copies through `noteFinishedCopy`, though. Nothing covers the running-export count, or the fact that it stays on the badge even while Export is open, where `announceReadyCopies` clears only the finished copies. A test that mocks the runner as exporting would pin both.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T01:46:53Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment about the removed "Drop a video here" strip (confidence high)**

The PR deletes `.importZone`, but the comment that described it ("NIW2-579: the \"Drop a video here\" strip, between the header and the toolbar.") is still there. It now sits right above the `.stickyBar` comment, so it reads as if it describes the sticky toolbar. The Library no longer has a drop strip. Delete line 108.

<!-- wachi:finding -->
