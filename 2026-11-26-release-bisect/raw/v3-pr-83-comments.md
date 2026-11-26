# kaipu-bench-wachi-v3#83 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117 · github-actions[bot] · 2026-11-26T06:30:33Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: Every Library re-list unmounts the Export screen and drops the user's choices (confidence high)**

`useLocalLibrary().refresh` sets `isLoading` to true at the start of every re-list, not only the first one (`features/library/hooks/use-local-library.ts:42`). It runs on every `libraryChanged` broadcast (`use-local-library.ts:133`). Main sends that broadcast on imports, screenshot saves, cloud-catalog refreshes and new library items (`main/library/index.ts:87,185`, `main/screenshots/screenshot-save.ts:48`). Here `if (isLoading) return …loading` comes before `<ExportScreen>`, so each re-list replaces the screen with "Loading…" and then mounts `ExportScreen` again from scratch.

The remount loses `selected`, the YouTube 1440p/4K choice and the Fill/Fit framings. `initialDestination` falls back to `urlDestination`, so a card picked on screen (which is never written to `?to=`) goes back to "Where is it going?".

This PR keeps the user on Export after an export starts. When the copy lands in the Library, that broadcast resets the stage the user is still looking at, and nothing tells them why. A screenshot taken from the hotkey, or the cloud-catalog refresh that runs on mount (`use-local-library.ts:130`), does the same while they are choosing.

Fix: show the loading state only while there is no list yet. For example, `if (isLoading && !video) …`, or track a first-load flag. This keeps `ExportScreen` mounted while the list is re-read.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T06:30:33Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: A file dropped on the Library now navigates the Electron window to that file (confidence high)**

This change removes the Library's `useFileDrop` call. After this, the only caller of `useFileDrop` is `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which only the Export screen mounts. The hook's own comment says why it listens on the whole window: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:9-11`). The main process does not stop that navigation: `main/index.ts:400-403` sets only a window-open handler, and there is no `will-navigate` handler anywhere in `src`.

So a user who drags an MP4 onto the Library, which the previous build invited them to do, now sees the app replaced by the raw file. They have to reload or restart to get it back. The PR's test step 12 ("dropping a file there does nothing") does not describe what actually happens.

The fix: if the Library should ignore drops, mount a window-level guard that calls `preventDefault` on `dragover`/`drop` without importing. A better place for it is the app shell, so every non-Export screen is covered, or a `will-navigate` deny in main. Another option is to send the dropped files to Export.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:201 · github-actions[bot] · 2026-11-26T06:30:33Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: The 1440p/4K and Fill/Fit radio groups do not respond to the arrow keys (confidence medium)**

These segmented controls declare `role="radiogroup"`/`role="radio"` but have no key handling. Meanwhile `destinationStep` (`export-page.tsx:353-363`) deliberately ignores arrow keys inside any other radiogroup, on the grounds that such a group "answers its own arrows". So with focus on 1440p, ←/→ does nothing at all: it neither moves within the group, as the radio role promises screen-reader users, nor moves the destination row. The same applies to the Fill/Fit group at line 233. Either add roving arrow handling to these groups or use plain toggle buttons (`aria-pressed`). The deleted `destination-detail.tsx` had the same gap, but the new page-level handler now assumes it is closed.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T06:30:33Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: The Library now leaves file drops to the browser default, which navigates the window away from the app (confidence medium)**

This test now expects the Library to ignore a dropped video. It does not check what happens to the drop afterwards. After this PR, `useFileDrop` is mounted only through `usePrepareImport`, which only Export uses (`features/prepare/use-prepare-import.ts:55`); nothing else calls `preventDefault` on `dragover` or `drop`. The hook's own comment states the result: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`). The main process has no `will-navigate` guard, only `setWindowOpenHandler` (`main/index.ts:400`).

So a user who drops a video on the Library, where drops used to be accepted, gets the main window replaced by the raw file. The renderer state is gone, including a background export running in the renderer, and no message says what happened.

Suggested fix: keep a window-level handler on the Library that calls `preventDefault` on file drags, for example by routing the drop to Export, or add a `will-navigate` guard in main. Then make this test assert that the drop was prevented, the way `export-page.test.tsx:416` does with `!fireEvent.drop(...)`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:86 · github-actions[bot] · 2026-11-26T06:30:33Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: This assertion would pass even if the Library still had its drop handler (confidence high)**

The test does not override `pathForFile`. The shared setup stubs it as `() => ""` (`test/setup.ts:156`). `importDropped` puts any file with an empty path on the skipped list and returns before calling `importVideoFiles` (`features/library/hooks/use-import-videos.ts:102-111`). So `importVideoFiles` is never called whether or not a drop listener is mounted, and the test cannot fail. The removed test set `pathForFile` for exactly this reason. Either set `pathForFile` the way `export-page.test.tsx:421` does, or assert on the return value of `fireEvent.drop`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T06:30:33Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "Active with and without a video" only checks the with-video URL (confidence high)**

The test name says the Export link is active on `/export` and on `/export/:assetId`, but it only renders `/export/asset-1` (line 40). The bare `/export` route (`ROUTES.exportNew`, the NavLink's own `to` at `sidebar.tsx:53`) never gets an `aria-current` check. Either add a second `renderAt(ROUTES.exportNew)` assertion or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T06:30:33Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: Running exports now count toward the badge, but no test covers it (confidence high)**

`useExportBadge` adds 1 while `useExportRunner().status === "exporting"` (`sidebar.tsx:121-122`), and the label changed to "in progress or ready". Every test here only drives `noteFinishedCopy`, so the new in-progress part of the count goes untested, including that it doesn't clear when Export opens. A test that mocks the runner status as exporting would pin that down.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T06:30:33Z

👮 **Wachiman** · Nit · 🟡🧹 **Consider · cleanup: Orphaned comment for the removed import strip (confidence high)**

The `.importZone` rule was deleted, but its comment (`NIW2-579: the "Drop a video here" strip, between the header and the toolbar.`) is still here. It now sits directly above the `.stickyBar` comment, so it reads as if it described the sticky bar. Delete line 108.

<!-- wachi:finding -->
