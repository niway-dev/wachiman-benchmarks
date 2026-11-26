# kaipu-bench-wachi-v3#71 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Any library re-list unmounts the Export screen and resets the picked destination (confidence medium)**

`useLocalLibrary().refresh` sets `isLoading` to true on every call, not only the first (`use-local-library.ts:41-42`). It runs again whenever main broadcasts `library:changed` (`use-local-library.ts:133`). That happens when the mount-time `refreshCloudCatalog()` succeeds for a signed-in user (`use-local-library.ts:130`, `main/library/index.ts:73-76`), on account changes and on tag edits (`main/library/index.ts:85-88`, `108-112`). Each time, line 117 swaps the whole page for "Loading…", and `ExportScreen` remounts. On remount, `selected` is re-initialised from `initialDestination` (the URL's `?to=`). The YouTube 1440p/4K choice and the Fill/Fit framings go back to their defaults (lines 212-221).

What the user sees:
- They open Export with no `?to=` and pick GitHub. About a second later the cloud refresh lands and the stage snaps back to "Where is it going?".
- They open Export at `?to=youtube`, pick Email, and the screen silently re-selects YouTube. Pressing Enter then exports a YouTube copy, not the one they chose.

The page's `chosen` ref is not reset, because `assetId` did not change. It still holds Email, so a later drop or Change video carries a destination the screen no longer shows.

Possible fix: only show the loading state before the first list, e.g. `if (isLoading && !video)`. That keeps `ExportScreen` mounted across re-lists. I could not read the deleted `prepare-page.tsx` to tell whether Prepare had the same gate. Either way, this screen now holds much more local state that the remount throws away.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A file dropped on the Library now sends the whole window to that file (confidence medium)**

This change removes `useFileDrop` from the Library. After that, the only window-level drag/drop handler left in the renderer is the one under Export (`use-prepare-import.ts:55`). The hook's own docstring (`use-file-drop.ts:9-11`) explains why it exists: "a file dropped where nothing handles it makes Electron navigate the window to that file". The main process does not guard against this. It sets only `setWindowOpenHandler` (`main/index.ts:400-403`), and there is no `will-navigate` handler anywhere in `src/`.

So when a user drags an MP4 onto the Library, as they could until this PR, the app is not left doing "nothing" as the PR body says. The renderer navigates away to `file://…mp4` and the app's UI is gone. Any renderer-held state goes with it, including an export the runner is encoding in this renderer.

The Library is the screen where users have learned to drop files, so this is the likeliest place for it to happen. Two fixes would work:
- keep a window-level `dragover`/`drop` `preventDefault` mounted for the whole app shell (for example a no-op `useFileDrop` in the shell), or
- add a `will-navigate` guard in `main/index.ts` that blocks navigation away from the app URL.

The second also covers the other screens that never handled drops.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:201 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: The 1440p/4K and Fill/Fit radiogroups ignore the arrow keys (confidence medium)**

These segmented controls declare `role="radiogroup"` and `role="radio"`, but they have no `onKeyDown` and no roving `tabindex`. `destinationStep` deliberately returns null inside any radiogroup that is not the destination row (`export-page.tsx:363`), with a comment saying such a group "answers its own arrows" (`export-page.tsx:352-354`). Nothing here does that. With focus on 1440p/4K or Fill/Fit, ←/→ do nothing, and every option is a separate Tab stop, unlike the radio pattern the roles announce. The Fill/Fit group at line 233 has the same gap. Add arrow handling (and roving tabindex) to these groups, or let the row's arrows through when focus is in them.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: The Export badge clears on /export/:assetId, a screen that doesn't show the finished copies (confidence high)**

`onExport` matches with `end: false`, so `/export/:assetId` also calls `announceReadyCopies()`. The doc comment justifies this because Export "points at the copies", but only the no-video branch renders `RecentExports` (`pages/export/export-page.tsx:101-113`). With a recording open, the Export screen shows no finished copies, and the Library is still the only page that outlines them (`unseenCopyIds` is used only in `library-page.tsx:62`). So a copy that finishes while its ready card is hidden loses its badge when the user goes to Export on any recording, and they never see where that copy is. Even on `/export`, the strip lists only the three newest copies (`recent-exports.tsx:12`), so a fourth unseen copy is announced without being shown. Consider announcing only on `ROUTES.exportNew` with `end: true`, which matches how the Library is handled one line below.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Library no longer intercepts file drops, and this test locks that in: a dropped file navigates the window away from the app (confidence medium)**

Before this PR, the Library mounted `ImportDropZone` and so `useFileDrop`, which called `preventDefault` on `dragover` and `drop` for the whole window. The hook explains why it does that: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-11`). After this PR the only caller of `useFileDrop` is `usePrepareImport`, and only `ExportPage` uses that (`features/prepare/use-prepare-import.ts:55`, `pages/export/export-page.tsx:85`). The main process has no `will-navigate` guard either: grepping `src/` finds only `setWindowOpenHandler` at `main/index.ts:400`.

So if someone drops a video on the Library, which was the import target until now, Chromium's default runs. The renderer navigates to `file:///…/clip.mp4`, the app UI is replaced, and a background export running in the renderer goes with it. Nothing warns the user first.

This test, titled "does not take a video dropped on the window", only checks that `importVideoFiles` was not called. It ignores what `fireEvent.drop` returns, which is the default-prevented signal that `dropFiles` in `export-page.test.tsx:414-416` checks. So it passes while that navigation happens.

Suggested fix: keep a window-level guard that calls `preventDefault` on file `dragover`/`drop` outside Export. Either the app shell or the Library page could install it, or main could handle `will-navigate`. Then assert here that `fireEvent.drop(...)` returns `false`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only checks the URL that has a video (confidence high)**

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. Bare `/export` (`ROUTES.exportNew`, the link's own `to`) is never checked for `aria-current`. Note that `isActive` in `sidebar.tsx:68-69` uses `matchPath` with `end: false`, so `/export/asset-1` would light up even if the prefix rule changed. Add `renderAt(ROUTES.exportNew)` with the same assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:48 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The "in progress" part of the Export badge is never tested (confidence high)**

`useExportBadge` (`sidebar.tsx:121-122`) now adds 1 while `useExportRunner().status === "exporting"`, and the accessible name is now "copy in progress or ready". Every test here drives only `noteFinishedCopy`, so nothing covers the running export being counted, or the badge staying while you sit on Export during a run. That second case is easy to get wrong because `announceReadyCopies` only clears finished copies. A test that mocks or starts a running export would pin the new behaviour the label describes.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/export-screen.md:50 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Dropping a file on the Library now replaces the whole app (confidence medium)**

The PR removes the Library's window drop handling ("it no longer takes window drops"), and nothing else catches a dropped file there. The only window-level `drop`/`dragover` handlers in `src` are in `useFileDrop` (`features/library/hooks/use-file-drop.ts:48-51`). That hook's own comment (`use-file-drop.ts:10-11`) says "a file dropped where nothing handles it makes Electron navigate the window to that file". The main process sets only `setWindowOpenHandler` (`main/index.ts:400-403`) and has no `will-navigate` guard. So a user who drops a video on the Library, the screen that used to import it, now gets the video file loaded in place of the app UI, with no message. To stop that, catch the drop on the Library: either keep a `preventDefault`-only `useFileDrop`, or send the drop to Export. Alternatively, block file navigation in main with `will-navigate`, which also covers Record and the Editor.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T01:48:08Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment for the removed drop strip (confidence high)**

`.importZone` was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip…") stayed. It now sits directly above the `.stickyBar` comment and describes a rule that no longer exists. Remove it.

<!-- wachi:finding -->
