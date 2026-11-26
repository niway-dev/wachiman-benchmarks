# kaipu-bench-wachi-v3#51 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Enter-to-export does not skip open dialogs, but the arrow handler does (confidence medium)**

`destinationStep` returns null inside `[role='dialog']` (line 364). `isPrimaryEnter` has no matching check. The document-level listener (lines 277-301) therefore runs `primary()` for any Enter whose target is not a field, button or link. The VideoPicker panel is a `role="dialog"` (`video-picker.tsx:69-74`). If the user clicks the panel's padding or the "pickerEmpty" text, focus moves to `<body>`. Pressing Enter then starts an encode, or opens the existing copy, while the Change-video list is still open. The same applies to any other dialog mounted over the screen. Adding `if (target.closest("[role='dialog']")) return false;` would match the arrow handler.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-copy.ts:29 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: EXPORT_ORDER repeats DESTINATION_IDS and nothing checks that the two match (confidence high)**

`EXPORT_ORDER` has the same seven ids in the same order as `DESTINATION_IDS` (`features/prepare/destinations.ts:37-45`). Its type is only `readonly DestinationId[]`, so the compiler will not catch a destination added to one list but not the other. A destination added later would type-check (`EXPORT_NAME` would fail, which helps) but never appear in the row or in arrow navigation. Either derive the order from `DESTINATION_GROUPS.flatMap(g => g.destinations)`, which is the documented order (bigger, light, keep), or pin the two lists together with a test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Library no longer intercepts window file drops, so a dropped file navigates the app window away (confidence high)**

The Library dropped its `useFileDrop` call, so nothing on this screen calls `preventDefault` on `dragover`/`drop` any more. `use-file-drop.ts:8-11` gives the reason the hook covers the whole window: "a file dropped where nothing handles it makes Electron navigate the window to that file." The main process has no `will-navigate` guard. A search of `src/main` finds only `setWindowOpenHandler` at `index.ts:400`, and no other renderer code handles `drop`.

So on the Library, dragging an MP4 from Finder no longer "does nothing" as the PR's test step 12 claims. It replaces the app's UI with the file. Before this PR the Library imported the file. The user loses the app UI and any renderer state until they reload.

Fix: keep the window-wide guard on the Library without importing. Call `useFileDrop` with a no-op, or with a handler that sends the files to Export. A one-line `dragover`/`drop` `preventDefault` in the app shell would protect every screen.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:111 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Archive line always says "sound as recorded", even for a recording without audio (confidence medium)**

`keepPicture` renders "{width} × {height} · sound as recorded · {size}" (en.json:927) whatever the recording is. `planCopy` sets `sound: "none"` when `!source.hasAudio` (`destinations.ts:209-210`). The removed Prepare detail used `plan.sound` and said "no sound" in that case.

For a silent recording the Archive card now states something false. Consider picking the sound phrase from `plan.sound`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Badge is cleared on /export/:assetId, a screen that doesn't show the finished copies (confidence medium)**

`onExport` uses `end: false`, so `announceReadyCopies()` runs on `/export/<anyAssetId>` as well as on `/export`. The doc comment (lines 107-108) justifies the clearing with "both point at the copies". Only the no-video screen shows them, though: `RecentExports` is rendered only in the `!assetId` branch (`pages/export/export-page.tsx:101-112`). The per-recording screen has no list of finished copies.

The effect also re-runs on every `copies` change (line 120). Under this PR, Export stays on screen after an export starts. Two things follow:
- Any copy that finishes while the user is still on `/export/:assetId` is announced as soon as `noteFinishedCopy` fires (`export-runner.ts:462-463`). Once its ready card is closed, the rail shows 0 instead of 1. Before this PR, that copy kept a Library badge after its card was closed (`libraryBadgeCount` only excludes the on-screen ready card, `ready-copies.ts:70-75`).
- Opening Export for any recording (for example from a recording page's "Prepare for…" chip) silently clears the badge for unrelated copies that finished in the background. Nothing on that screen shows them.

`sidebar.test.tsx` only covers `ROUTES.exportNew` for the clearing, so `/export/:assetId` is untested. Fix: match `{ path: ROUTES.exportNew, end: true }` for the announce. The nav item's own `isActive` can stay `end: false`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Library no longer intercepts file drops, so a dropped file can navigate the whole window to that file. The test locks this in (confidence medium)**

Before this PR, Library mounted the window-wide drop hook. The removed test "imports a video dropped anywhere on the window" covered it. After this PR, only Export mounts `useFileDrop` (via `usePrepareImport`, `export-page.tsx:85`; `use-prepare-import.ts:55`). The hook's own comment says what happens without it: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`use-file-drop.ts:8-11`, also `use-prepare-import.ts:32-34`). The main process has no `will-navigate` guard. It only sets `setWindowOpenHandler` (`main/index.ts:400-403`).

So if a user drags a video onto the Library, the app most likely does not ignore it. The main window loads the file instead of the app UI. This new test only checks that `importVideoFiles` is not called. It never checks the drop's default. Compare `dropFiles` in `export-page.test.tsx:416`, which asserts `!fireEvent.drop(...)`. The test passes while the window is replaced.

Suggested fix: keep a window-level guard that calls `preventDefault` on `dragover`/`drop` for file drags outside Export. That could be a no-op `useFileDrop` in the shell or Library, or a `will-navigate` block in main. Then assert here that `fireEvent.drop` returns `false`. Also, the assertion runs synchronously right after the drop. An import started after an `await` would not have happened yet, so `not.toHaveBeenCalled()` would pass whatever the page does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The test says "with and without a video" but only checks /export/asset-1 (confidence high)**

The test only renders `/export/asset-1`. The no-video route `ROUTES.exportNew` (`/export`), which the NavLink actually points at (`sidebar.tsx:53`), is never checked for `aria-current`. Add a second render at `/export`, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: No test covers the badge's new in-progress count (confidence high)**

`useExportBadge` now adds 1 while the runner's status is `exporting` (`sidebar.tsx:121-122`), and the badge label reads "N copies in progress or ready". Every test here drives only finished copies through `noteFinishedCopy`. No test checks that a running export shows "1", or that the count falls back to the unannounced copies once it finishes.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T00:03:49Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment left for the removed drop strip (confidence high)**

This change deletes the `.importZone` rule, but its comment `/* NIW2-579: the "Drop a video here" strip, between the header and the toolbar. */` is still there. It now sits right above the `.stickyBar` comment, so it reads as if it describes the sticky toolbar. Nothing in `src/` uses `importZone` anymore. Delete the line.

<!-- wachi:finding -->
