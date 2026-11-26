# kaipu-bench-wachi-v3#67 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:353 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡📝 **Consider · docs: destinationStep's doc says a held key is ignored, but the code never checks `event.repeat` (confidence high)**

The docstring says an arrow is not for the row when it comes from "a held key". The guards at lines 357-365 check modifiers, `defaultPrevented`, `isComposing`, fields, other radiogroups and dialogs, but not `event.repeat`. Holding ArrowRight therefore keeps stepping along the row. `isPrimaryEnter` does check `event.repeat` (line 376). Either add `event.repeat` to the guard at line 358, or drop "a held key" from the comment if auto-repeat is meant to work.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:40 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: "Pick from Library" stays enabled during an import, so a running import can take the user to a different video (confidence medium)**

"Browse files" is disabled while `importing` (line 51), but the VideoPicker trigger is not. If the user picks a Library video while an import is running, `openVideo` navigates to `/export/<picked>`. When the import finishes, `usePrepareImport`'s `onImported` runs `refresh().then(() => navigate(preparePath(first.assetId, to)))` (use-prepare-import.ts:48) and replaces the screen with the imported video. The video the user picked disappears with no explanation. Disabling the trigger while `importing` would match the Browse button. Passing `disabled={importing}` through the trigger props is enough.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:212 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: A destination picked on the screen is lost after "Open" and then Back (confidence medium)**

`selected` is component state that starts from `?to=` (line 212), and `chosen` is a ref (line 77). Neither is written back to the URL. When a destination already has a copy, the primary action navigates to `/library/<existing>` (line 162). Router Back then remounts ExportPage under the original history entry, so the screen shows the URL's destination, or "Where is it going?", instead of the card the user picked. The fix is to write the selection to `?to=` with `setSearchParams(..., { replace: true })` when a card is picked. That also lets `chosen` go.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A file dropped on the Library now navigates the whole window to the file instead of doing nothing (confidence medium)**

This change removes `useFileDrop` from the Library, so nothing on that screen calls `preventDefault` on `dragover`/`drop` any more. The hook's own doc explains why it listened on the whole window: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-12`). Nothing else catches it. No other renderer code adds a `dragover`/`drop` listener (the only matches are in `use-file-drop.ts`), and the main process has no `will-navigate` guard, only `setWindowOpenHandler` (`src/main/index.ts:400-403`), which does not cover in-window navigation.

The PR says "dropping a file there does nothing". What actually happens: dropping an MP4 on the Library replaces the app's renderer with Chromium's file viewer, and the user has to reload. Before this PR the drop imported the video.

Suggested fix: keep a window-level `dragover`/`drop` `preventDefault` while the Library is mounted (or `useFileDrop(() => {})`). The more durable option is an app-wide guard in the shell, or `will-navigate` → `preventDefault` in `main/index.ts`. Other screens without a drop handler already had this gap, so an app-wide guard also covers them.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: An Email export changes its name in Recent exports when it finishes (confidence high)**

While an export runs, its row takes its logo from `running.destination` (line 50). So an Email copy shows the Email logo while it exports. Once it finishes, the row is rebuilt from `destinationOfPreset(copy.export!.preset)`, and that returns `chat` for `balanced` (`features/prepare/destinations.ts:69-71,102-107`). The same row then switches to the Slack · Discord logo and name. The PR covers `destinationOfPreset("balanced")` for the Ready cards but not this list. If the finished copy can't record its destination, consider showing a neutral name for Balanced copies, or keeping the destination on the export metadata, so the row doesn't change identity when it completes.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Badge is cleared on /export/:assetId, where nothing shows the finished copies (confidence medium)**

`onExport` matches with `end: false`, so `/export/:assetId` counts as "opening Export" too. The Library check just below it uses `end: true`, so that `/library/:assetId` does not count. Only the no-video screen (`/export`) renders `RecentExports` (`pages/export/export-page.tsx:101-113`). The per-recording `ExportScreen` lists none of the other finished copies.

Export no longer navigates away when a copy starts: `startCopy` only calls `copy.start(...)` (`export-page.tsx:252-260`), so the user usually stays on `/export/:assetId` while the copy encodes. When it finishes, `noteFinishedCopy` (`export-runner.ts:463`) changes `copies`. The effect re-runs with `onExport` true and calls `announceReadyCopies()`, so the badge for that copy never appears. The same happens to a copy of recording A that finishes while the user is setting up `/export/B`.

If the user has closed the Ready card (`dismissReadyExport`), nothing in the rail says a copy finished, which contradicts the comment at lines 105-109 ("both point at the copies"). Suggest `end: true` here, like the Library check, or a test that pins the per-recording behaviour if it is intended. `sidebar.test.tsx` only covers clearing on `ROUTES.exportNew`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Test locks in a Library that leaves file drops unhandled, so Electron navigates the window to the file (confidence medium)**

This test checks only that `importVideoFiles` is not called. It never checks that the drop's default action is prevented, and at head nothing prevents it. `library-page.tsx` no longer mounts `useFileDrop`; its imports at lines 1-33 have no drop or import hook. `useFileDrop` is now mounted only by `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which only Export uses. The hook's own doc (`features/library/hooks/use-file-drop.ts:10-11`) says what happens next: "a file dropped where nothing handles it makes Electron navigate the window to that file." Main has no `will-navigate` guard (the only navigation hook in `src/main` is `setWindowOpenHandler` at `main/index.ts:400`).

Before this change, Library handled window drops: the removed test "imports a video dropped anywhere on the window" covered it. Now dropping a video on Library, or on any page other than Export, replaces the app UI with the file. That also unloads the renderer, which hosts the background export runner, so a running export is lost without warning.

Fix: keep a window-level drop guard while Library (or the app shell) is mounted. It should `preventDefault` on dragover/drop for files, or route the drop to Export. Then make this test assert it the way `export-page.test.tsx:416` does: `expect(fireEvent.drop(document.body, …)).toBe(false)`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only checks with a video (confidence high)**

The test only renders `/export/asset-1`. It never checks the bare `/export` (`ROUTES.exportNew`), even though line 20 registers that route for this purpose. The sidebar's `isActive` uses `end: false` on `ROUTES.exportNew` (sidebar.tsx:53, 68-69). If `end` were ever set to true, only the no-video URL would stay lit, and this test would still pass. Add a `renderAt(ROUTES.exportNew)` case, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The badge now counts the running export, but no test covers it (confidence high)**

`useExportBadge` adds 1 while `useExportRunner().status === "exporting"` (sidebar.tsx:121-122), and the label now reads "in progress or ready". Every test here only seeds finished copies with `noteFinishedCopy`, so the in-progress half of the count is never exercised. A search finds `useExportBadge` and this label only in sidebar.tsx and this test. A case that mocks the runner as exporting (count 1), then finishes it into `ready` (the ready copy is excluded by `libraryBadgeCount`), would pin the new behaviour and guard against counting it twice.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:10 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: With no video, nothing on the Export screen can scroll (confidence low)**

`.wrap` dropped `overflow-y: auto` on purpose, so the Library picker isn't clipped. In the no-video branch (export-page.tsx:101-114), `.screen` is `overflow: hidden` (export-page.module.css:15). The header and `RecentExports` are `flex-shrink: 0` (export-header.module.css:3, recent-exports.module.css:3). That leaves no scroll container anywhere. On a window shorter than the 670 px minimum, the drop zone's bottom (the Browse files / Pick from Library actions) gets clipped and can't be reached. That can happen because `fitWindowPreset` lowers `minHeight` to the screen height (window-size.ts:113). The picker could instead escape the clip as a portal or with `position: fixed`, which would let the wrap scroll again.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T01:38:06Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment for the removed `.importZone` rule (confidence high)**

The diff deletes `.importZone`, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits right above the `.stickyBar` comment, so it reads as if it describes the sticky toolbar. Delete line 108 too.

<!-- wachi:finding -->
