# kaipu-bench-wachi-v3#63 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117 · github-actions[bot] · 2026-11-26T01:37:16Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Any library re-list unmounts the Export screen and resets the picked destination, YouTube preset and framing (confidence medium)**

`refresh()` sets `isLoading` to true on every call, not only the first (`use-local-library.ts:42`). The hook also calls it again whenever main broadcasts `libraryChanged` (`use-local-library.ts:133`, sent from `main/library/index.ts:27`), for example after the cloud-catalog refresh it starts on mount (`use-local-library.ts:130`). During that re-list, line 117 returns the bare "Loading…" div, so `ExportScreen` unmounts. When it comes back, `selected` falls back to the URL's `?to=` (or to "Where is it going?"), the YouTube choice goes back to `defaultYoutubePreset`, and Fill/Fit goes back to the defaults. The `chosen` ref is kept, so a later drop or Change video still carries the old pick, which no longer matches what is on screen. The PR says "Export stays on screen after it starts", but a re-list after a copy lands would also flash the screen and drop the user's choice. A fix is to show Loading only while `videos` is still empty (the first load), so a re-list keeps the screen mounted.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:213 · github-actions[bot] · 2026-11-26T01:37:16Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Picking a card does not update the URL, so Back loses the selection (confidence high)**

`select` only sets component state and the `chosen` ref; it never writes `?to=`. If the user opens an existing copy (`onOpenExisting` → `/library/…`, line 162) and presses Back, the page remounts under the old history entry. `chosen` is reset (line 79) and `selected` starts from `initialDestination` again, so the destination they had picked is gone. Calling `setSearchParams({ to: d }, { replace: true })` in `select` would keep the selection in the history entry, and `chosen` would then no longer be needed.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:98 · github-actions[bot] · 2026-11-26T01:37:16Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Unreadable-file redirect drops the destination picked on screen (confidence high)**

The probe-error redirect uses `urlDestination`. The other two exits (`openVideo` line 87, and drop import through `current`) use `current()`, which prefers the card picked on this screen. If the user picks a card before the probe fails, the redirect to `/export` loses that pick. Using `current()` here would match the other exits.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:353 · github-actions[bot] · 2026-11-26T01:37:16Z

👮 **Wachiman** · 🟡📝 **Consider · docs: `destinationStep` doc says it ignores a held key, but it never checks `event.repeat` (confidence high)**

The comment lists "a held key" as a case that returns null. The function checks `defaultPrevented`, `isComposing` and the modifier keys, but not `event.repeat` (lines 357-359). `isPrimaryEnter` does check it (line 376). Holding → therefore steps through all seven cards. Either add the check or fix the comment.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:36 · github-actions[bot] · 2026-11-26T01:37:17Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A finished export disappears from Recent exports; the list is never refreshed (confidence medium)**

The running row shows only while `runner.status === "exporting"`. When the job finishes, the runner resets to IDLE (`export-runner.ts:462`) and the row goes away. The finished copy should take its place through `recentCopies(videos, …)`, but `videos` comes from `useLocalLibrary` in `ExportPage`. That hook re-lists only on mount and on `library:changed` (`use-local-library.ts:124-134`). The export lands through `recordingFinalize` (`recording-hub.ts:390-396`), which does not call `broadcastLibraryChanged()`. Only the library handlers and `screenshot-save.ts` call it.

The Export page also passes no `onSaved` to `copy.start` (`export-page.tsx:254-259`), so nothing triggers `refresh()` there either. Prepare got away with this because it navigated back to the recording after starting a copy. Export now stays on screen. As a result, the copy you just made vanishes from "Recent exports" until you leave and come back.

The same stale `videos` feeds `lineage.exportsOf` → `findReusableExports`, so the destination card does not flip to "Ready". Pressing Enter again starts a second encode instead of opening the existing file.

Suggested fix: refresh the library when the copy is saved, e.g. `onSaved: () => void refresh()` in `startCopy`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:228 · github-actions[bot] · 2026-11-26T01:37:17Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Fill / Fit no longer shows what gets cropped (confidence medium)**

The deleted `ShapeCard` showed a `FramingPreview` of the recording's thumbnail on the vertical/square canvas, with a hint line under the choice. Now the only explanation of Fill / Fit is a `title` tooltip on each segment. Fill crops most of a 16:9 screen recording into 9:16, and nothing visible shows that before exporting. Consider keeping the `FramingPreview` (the header already has the thumbnail) or showing the hint text inline.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T01:37:17Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Library no longer intercepts file drops, so a dropped video navigates the whole window to the file (confidence medium)**

The old Library tests show the page used to take window-level file drops (the removed test "imports a video dropped anywhere on the window"). That handler is gone, and this new test only checks that `importVideoFiles` is not called. It never checks that the drop was prevented. `useFileDrop` is now mounted only through `usePrepareImport` on Export (`features/prepare/use-prepare-import.ts:55`, `pages/export/export-page.tsx:85`), and it is the only `drop`/`dragover` listener in the renderer (`features/library/hooks/use-file-drop.ts:48-51`). The hook's own comment states the consequence: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`use-file-drop.ts:10-11`). `main/index.ts:400-411` sets a window-open handler but has no `will-navigate` guard. So when a user drops a video on the Library, which used to work as an import, the main window loads the raw file and the app UI is gone. That would also abandon a background export running in that renderer. The fix is to keep a window-level guard (`preventDefault` on `dragover`/`drop` for file drags) mounted app-wide, or at least on Library. A `will-navigate` handler in main that refuses `file:` URLs would also work. This test should then assert `fireEvent.drop(...)` returns false, as `dropFiles` does in `export-page.test.tsx:416`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T01:37:17Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only checks the with-video case (confidence high)**

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. The bare `/export` route (`ROUTES.exportNew`) is never checked for `aria-current="page"`. The Rail item's `to` is `ROUTES.exportNew` with `end` unset (`sidebar.tsx:53`, `isActive` at `sidebar.tsx:68-69`), so the case matters: if someone later sets `end: true` the way Record does, the `/export/:assetId` case breaks while `/export` still passes, and the reverse change would slip through too. A second `renderAt(ROUTES.exportNew)` assertion would make the test cover what its name says.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T01:37:17Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: No test for the in-progress part of the new Export badge (confidence high)**

`useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (`sidebar.tsx:121-122`), and the label changed to "copies in progress or ready". Every test here only drives `noteFinishedCopy`, so the running term is never tested: not counted alone, not shown while Export is open (where finished copies never badge), and not counted twice when a copy finishes and moves from running to `ready`. A test that mocks or drives the runner into `exporting` would pin down this new behaviour.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T01:37:17Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment for the deleted import drop strip (confidence high)**

The `.importZone` rule was removed, but its comment (`/* NIW2-579: the "Drop a video here" strip, between the header and the toolbar. */`) is still there. It now sits right above the comment for `.stickyBar` (lines 109-111), so it looks like it describes the sticky toolbar. Delete line 108 along with the rule.

<!-- wachi:finding -->
