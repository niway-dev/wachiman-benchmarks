# Wachiman review of branch `bench/pr-467` of pr-467 against origin/replay/pr-467/base (merge-base 13b7ff5), at b12d760

All 47 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

10 finding(s): 2 to fix, 8 to consider

## Findings

### 🟡📝 **Consider · docs: `DestinationSizes.sizeText` says it returns "up to ~570 MB", but the row is never given that text (confidence high)**

`apps/kaipu-record/src/renderer/src/pages/export/destination-row.tsx:13`

The interface comment lists "~570 MB", "up to ~570 MB", or "Full size". The only caller passes `sizeText: estimateText` (export-page.tsx:337), and `estimateText` (export-page.tsx:241-244) only returns "about" or "full". The "up to" wording comes from the separate `sizeText` that goes to the stage (export-page.tsx:245-248). So the cards always show "~X", even for a preset whose size is only an upper bound. If the cards are meant to be short, change the comment to say so. If they should say "up to", pass `sizeText` instead.

### 🟡🐛 **Consider · bug: Enter still exports while focus is inside a dialog; the arrow keys already stop there (confidence medium)**

`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375`

`destinationStep` ignores events from inside `[role='dialog']` (line 364), but `isPrimaryEnter` has no such check. It only skips fields, buttons and links. The listener is on `document` (line 299), so pressing Enter on any focusable element inside a dialog that is not a button, link or field starts an encode behind that dialog. The VideoPicker panel is a `role="dialog"` (video-picker.tsx:71), and other dialogs can open over this screen. Adding the same `closest("[role='dialog']")` check here would make the two keys behave the same.

### 🟠🐛 **Fix · bug: Library no longer intercepts file drops, so a file dropped on it navigates the app window to that file (confidence medium)**

`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`

The Library used to call `useFileDrop`, which listens for `dragover`/`drop` on the window and calls `preventDefault`. The hook's own comment says why: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-11`, `:29-47`). This PR removes that call and keeps no other listener on the page. The only remaining caller is `usePrepareImport`, and only the Export page uses it (`use-prepare-import.ts:55`, `export-page.tsx:85`). I found no `will-navigate` guard in the main process; a search of `src/` turns up only `setWindowOpenHandler` (`main/index.ts:400`), which covers `window.open`, not navigation. So dragging a video onto the Library, which used to import it, now replaces the renderer with the file and drops the app's UI and state. The user gets no explanation.

Suggested fix: keep a window-level drop guard on the Library. The simplest version calls `preventDefault` on `dragover`/`drop` and shows a toast pointing to Export, or sends the dropped files to Export. A better fix is a guard at the shell or main-process level (`will-navigate` → `preventDefault`), so every screen is covered, not only the Library.

### 🟡🧪 **Consider · tests: Wrapping `covered` in a Set stops the test catching a preset shared by mistake (confidence high)**

`apps/kaipu-record/src/renderer/src/features/prepare/destinations.test.ts:45`

Before this change, `covered` was a plain array, so the sorted-equality check failed whenever two destinations listed the same preset. Wrapping it in a `Set` was needed so email can share `balanced` with chat (`destinations.ts:71`). It also means the test no longer notices any other duplicate. The reverse-mapping loop does not fill the gap either, because it skips only `email` and checks `destinationOfPreset(p) === d`. So a future destination that reuses, say, `light` would pass that loop only if it came first in `DESTINATION_IDS`. Consider keeping the array and allowing exactly the one known overlap, for example by asserting that the array minus email's presets has no duplicates.

### 🟠🐛 **Fix · bug: The new Library drop test checks for no import, but a file dropped on Library now opens in the window (confidence medium)**

`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`

Before this PR, Library mounted the window-wide drop handler. `useFileDrop` is now mounted only through `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which only Export uses. The hook's own doc comment explains why it exists: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`). A search of `apps/kaipu-record/src` found no `will-navigate` guard in main and no other window `drop`/`dragover` listener.

So after this change, dropping a video on Library no longer imports it; it replaces the app's page with the file. That used to be the documented way to bring a video in. This test checks that `importVideoFiles` is not called, and it also passes while the default navigation still happens. Compare `dropFiles` in `export-page.test.tsx:414-416`, which asserts `!fireEvent.drop(...)` for exactly this reason.

Suggested fix: keep a default-preventing window guard mounted outside Export (for example a no-op `useFileDrop` in the shell, or `will-navigate` prevention in main). Then make this test assert that `fireEvent.drop` returns false. Also, the test checks `importVideoFiles` synchronously, so an async handler would still pass it.

### 🟡🧪 **Consider · tests: "an unknown ?to= picks nothing" never checks that the cards are unselected (confidence high)**

`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:368`

The test only waits for the "Where is it going?" heading. In `export-page.tsx:74`, `isDestinationId(to)` sends an unknown value to null, which is what produces that heading. But the test never checks that every card in the radiogroup has `aria-checked="false"`, which the test at line 161 does. Adding that line would pin "picks nothing" itself, not just the heading.

### 🟡🧪 **Consider · tests: "with and without a video" only checks the with-a-video URL (confidence high)**

`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39`

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. The case without a video, `ROUTES.exportNew` (`/export`), is the link's own `to`, and it never gets an `aria-current` check. Add a second `renderAt(ROUTES.exportNew)` with the same assertion, or rename the test.

### 🟡🧪 **Consider · tests: No test covers the running export in the badge count (confidence high)**

`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44`

`useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (sidebar.tsx:121-122), and it excludes the copy whose ready card is showing (`ready?.recording.assetId`). The new label reads "copy in progress or ready", yet every test here only goes through `noteFinishedCopy`. Neither the in-progress count nor the exclusion of the ready card's copy is tested.

### 🟡🐛 **Consider · bug: Export with no video has no scroll container, so a short window clips it (confidence medium)**

`apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:10`

`.wrap` is deliberately not a scroll box. In the no-video branch, `ExportHeaderEmpty`, `ExportDropZone` and `RecentExports` sit directly in `.screen`, which has `overflow: hidden` (export-page.tsx:101-113, export-page.module.css:9-16). Unlike the with-video layout, they are not inside `.stage` (`overflow-y: auto`). When the header, the zone (36px padding plus title, body and actions) and the recent exports are together taller than the page, the bottom is cut off and cannot be reached, including the last recent exports. One fix: put the drop zone and the recents in a scrolling middle region, and let the Library picker escape that region (portal or fixed position) instead of relying on there being no scroll box.

### 🟡🧹 **Consider · cleanup: Orphaned comment for the removed `.importZone` rule (confidence high)**

`apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108`

The `.importZone` rule is gone, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits right on top of the `.stickyBar` comment, so it reads as if it describes the sticky toolbar. Delete line 108.

## Summary

**Batch 1 of 6.** Part 1 has nothing that blocks the merge or needs a fix. I reviewed all 13 files, read the unchanged code they call (use-prepare-import, video-picker, useSourceProbe, destinations) and checked that the new Email keys exist in en.json.

Two "consider" findings:
- **`destination-row.tsx:13`:** the `sizeText` comment promises an "up to ~570 MB" form that the row is never given. The page passes the shorter "about" text, so the cards always show "~X".
- **`export-page.tsx:375`:** Enter still starts an export when focus is inside a dialog. The arrow keys already ignore dialogs; Enter should do the same.

Checked and fine:
- **Email destination:** Email reuses chat's preset. Existing files still read as chat, and new copies are named Email on the progress and ready cards.
- **Old Prepare links:** the `/prepare` URLs redirect to Export and keep `?to=`.
- **Dropped files:** a file dropped on the window is imported and opened on Export with the chosen destination.

One question stays open: a probe that never resolves leaves "Reading…" on screen with nothing bounding the wait. The old Prepare screen behaved the same way, and I did not read `probeSource`, so I can't say whether it can hang.

**Batch 2 of 6.** I found one issue in this part. Removing the Library's import surface also removed its window-level file-drop guard (`useFileDrop`). The hook's own comment says that without that guard, Electron navigates the window to a dropped file, and I found no `will-navigate` guard in the main process. So dropping a video on the Library now replaces the app UI instead of importing the video. The new `export-stage`, `recent-exports` and `video-picker` files read correctly against the plan types, the CSS tones and the Export page's key handling. I left one contract open: whether the Library list refreshes when an export finishes, so the new copy replaces the progress row in Recent exports. `destination-detail.tsx` is only deleted, and Export takes over its role.

**Batch 3 of 6.** Part 3 has no defects. The new Export rail item highlights on both /export and /export/:assetId. Its badge reuses the earlier Library-badge logic, adds Export as a second page that clears the count, and counts a running export as one. Nothing in the app still imports the deleted Prepare components, and the new use-file-drop test keeps the drop-handling coverage the deleted test gave. One test note (consider): wrapping `covered` in a Set in destinations.test.ts means the test no longer catches presets that two destinations share by mistake.

**Batch 4 of 6.** I reviewed the three test files in this part; I read the code only and ran nothing. The new Export page tests line up with what `export-page.tsx` does: the Enter and arrow-key handling, the copy that already exists ("Ready"), the toast when a file can't be read, and the redirect from old `/prepare` URLs. The Library detail tests only swap `/prepare` for `/export`. One real problem, likely but not fully confirmed: Library no longer has a handler for files dropped on the window. The hook's own comment says Electron then opens the dropped file in the window, and a search of `apps/kaipu-record/src` found no other guard (no `will-navigate`, no other drop listener). The new Library test checks only that no import happens, so it passes while the app page is replaced by the file. Also suggested: the unknown `?to=` test should check that no card is selected.

**Batch 5 of 6.** Part 5 holds the sidebar test, the Export stylesheets and the deleted Prepare test and import-drop-zone CSS. Nothing in this part is wrong enough to need a fix in this pull request. Every new CSS variable resolves in packages/tokens or base.css. The cases the deleted prepare-page.test covered reappear in export-page.test.tsx: drop and import, one export at a time, the Ready copy, an unreadable file and screenshots. There are three "consider" items. A sidebar test is named for two cases but checks only one. No test covers the running export in the badge count. With no video, the Export page has no scroll container, so a short window clips the bottom.

**Batch 6 of 6.** I read all 11 files in part 6 and found one minor issue: a leftover comment in `library-page.module.css` (line 108). It belonged to the removed `.importZone` strip and now reads as if it describes the sticky toolbar.

Other checks, which found nothing wrong:
- **`routes.ts`:** it has no value imports from workspace packages, so the preload rule holds.
- **Stylesheet classes and `data-tone` values:** every class `export-stage.tsx` uses exists in the stylesheet. The bar's tone values (`fits`, `over`, `lighter`, `not-lighter`) match the `data-tone` selectors.
- **Removed `library.*` import strings:** no code uses them anymore. The `import*` names a search still finds are the IPC calls `importVideos` / `importVideoFiles`, not the deleted translation keys.
- **New strings:** the new `prepare.*Email` and `export.*` keys exist in both `en.json` and `es.json`.
- **Docs:** the backlog page has its status banner and its row in `backlog/index.mdx`.

One contract is still open. I didn't confirm that the redirect from the old `/prepare` URLs to `/export` keeps `?to=`. That code is in `router.tsx`, which another part of this review covers.

<details><summary>What the change connects to (14 closed, 3 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- The source is probed on Export; on a probe error the page shows a toast and navigates to the empty Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — Can probeSource reject or hang? I did not read its implementation. Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.
- RecentExports reads the background export runner and shows the running job's progress, plus the newest finished copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — When a job finishes, does the Library list (useLocalLibrary) refresh, so the new copy replaces the progress row? Or does the strip lose the row until the next refresh? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts`.
- New routes `/export/:assetId` and `/export`; the `/prepare` routes stay only as legacy redirects (`apps/kaipu-record/src/shared/routes.ts:17-24`) — Does router.tsx really redirect `/prepare/:assetId` to `/export/:assetId` and keep `?to=`? That redirect is in another part of this review. Files that would answer it: `apps/kaipu-record/src/renderer/src/app/router.tsx`, `apps/kaipu-record/src/shared/window-size.ts`.

**Closed, with the lines they rest on**
- Email destination added: its own card and its own copy, over chat's `balanced` preset (`apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:71`) — The Email card shows 'Ready' whenever a balanced copy exists, including one made for chat. Its primary action then opens that file. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:251`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:338`.
- The URL builders now point at /export; the old /prepare URLs redirect, keeping the query (`apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:13`) — Old links land on Export with `?to=` preserved. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- A file dropped on the window, or picked with Browse, is imported, then Export opens on it with the chosen destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — After `refresh()` the page navigates to /export/:new?to=… If it fails: usePrepareImport calls `relist().then(navigate)` with no catch, so if the relist rejects the page never navigates. That code is outside this part. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`.
- Document-level keyboard handler: Enter exports, the left/right arrows step through the destinations (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — Enter on a focused card starts the copy, or opens the copy that already exists. If it fails: Enter is not filtered for dialogs, while the arrows are (reported as a finding). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-101`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:71`.
- Library page stops importing outside videos (header buttons, drop zone, window drop removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — A file dropped on the Library is no longer imported. Electron's default navigates the window to the file. If it fails: The renderer is replaced by the dropped file and the app UI is lost, silently. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-47`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`.
- VideoPicker opens a list and closes it on Escape or an outside mousedown, through document listeners (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`) — The list closes and the screen moves to the picked video. ExportPage's arrow handler ignores keys inside [role='dialog'], and its Enter handler ignores buttons. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:86-89`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:384`.
- Rail gains an Export item (ROUTES.exportNew) that is lit on /export and /export/:assetId (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:53`) — The Export rail item is highlighted on both Export screens. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:47-58`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:68-69`, `apps/kaipu-record/src/shared/routes.ts:17-24`.
- Rail badge moves from Library to Export: it counts the running export plus unannounced finished copies, and visiting Export or the Library announces the copies (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`) — The Export rail item shows a count with the label export.railBadge ('# copy in progress or ready'). The Library item no longer shows a badge. If it fails: On an export error the status becomes 'error' and the running count drops to 0. No copy is noted, so the badge simply disappears and the error card reports the failure. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:337`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462`, `packages/i18n/messages/en.json:946`.
- Prepare page, destination list, drop zone and the import-drop-zone test are removed (`apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx:1`) — A search under apps/kaipu-record/src finds no remaining import of pages/prepare, import-drop-zone, prepare-drop-zone, destination-list or useLibraryBadge. The useFileDrop behaviour the deleted test covered is kept in use-file-drop.test.tsx, minus the zone's own click and disable… Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:20-73`.
- A file dropped on the Library window (no drop handler there any more) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Electron navigates the window to the dropped file, as the hook's comment describes; no import happens. If it fails: The app's page is replaced by the file. The test asserts only that no import happened, so this goes unnoticed. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:414-416`.
- Probe of the recording fails, so Export toasts and replaces the route with /export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329`) — A toast appears and the screen shows Export with no video, keeping ?to=. If it fails: Covered by the test: the toast appears, the route ends at /export, and start is not called. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`.
- Enter on the page runs the primary action of the picked destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:285`) — The export starts, or the existing copy opens in Library. If it fails: Ignored in fields, with a modifier, and on non-radio buttons, as the test asserts. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:262-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`.
- The Export rail entry carries a badge (running export plus unseen finished copies) and clears it on Export or Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — A badge number and the accessible label `export.railBadge` on the Export link; the Library link no longer has a badge (sidebar.test.tsx:44-57). Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:72-82`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`, `apps/kaipu-record/src/shared/routes.ts:18-20`.
- Export with no video renders the header, the drop zone and the recent exports directly in the non-scrolling screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:101`) — Content that does not fit is clipped by `.screen`'s `overflow: hidden`. If it fails: In a short window the bottom of the zone and the recents cannot be reached. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:101-113`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.module.css:9-24`, `apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:2-11`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 10 | $0.59 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 10 | $0.51 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 10 | $0.42 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 7 | $0.43 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 13 | $0.52 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 10 | $0.44 |

Cost: $2.91, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 6 call(s), 60 turn(s), 6 min 16 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of b12d760 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/renderer/src/pages/export/destination-row.tsx:13 · 🟡📝 Consider · docs: `DestinationSizes.sizeText` says it returns "up to ~570 MB", but the row is never given that text (confidence high)
   The interface comment lists "~570 MB", "up to ~570 MB", or "Full size". The only caller passes `sizeText: estimateText` (export-page.tsx:337), and `estimateText` (export-page.tsx:241-244) only returns "about" or "full". The "up to" wording comes from the separate `sizeText` that goes to the stage (export-page.tsx:245-248). So the cards always show "~X", even for a preset whose size is only an upper bound. If the cards are meant to be short, change the comment to say so. If they should say "up to", pass `sizeText` instead.
2. apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · 🟡🐛 Consider · bug: Enter still exports while focus is inside a dialog; the arrow keys already stop there (confidence medium)
   `destinationStep` ignores events from inside `[role='dialog']` (line 364), but `isPrimaryEnter` has no such check. It only skips fields, buttons and links. The listener is on `document` (line 299), so pressing Enter on any focusable element inside a dialog that is not a button, link or field starts an encode behind that dialog. The VideoPicker panel is a `role="dialog"` (video-picker.tsx:71), and other dialogs can open over this screen. Adding the same `closest("[role='dialog']")` check here would make the two keys behave the same.
3. apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · 🟠🐛 Fix · bug: Library no longer intercepts file drops, so a file dropped on it navigates the app window to that file (confidence medium)
   The Library used to call `useFileDrop`, which listens for `dragover`/`drop` on the window and calls `preventDefault`. The hook's own comment says why: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-11`, `:29-47`). This PR removes that call and keeps no other listener on the page. The only remaining caller is `usePrepareImport`, and only the Export page uses it (`use-prepare-import.ts:55`, `export-page.tsx:85`). I found no `will-navigate` guard in the main process; a search of `src/` turns up only `setWindowOpenHandler` (`main/index.ts:400`), which covers `window.open`, not navigation. So dragging a video onto the Library, which used to import it, now replaces the renderer with the file and drops the app's UI and state. The user gets no explanation.

   Suggested fix: keep a window-level drop guard on the Library. The simplest version calls `preventDefault` on `dragover`/`drop` and shows a toast pointing to Export, or sends the dropped files to Export. A better fix is a guard at the shell or main-process level (`will-navigate` → `preventDefault`), so every screen is covered, not only the Library.
4. apps/kaipu-record/src/renderer/src/features/prepare/destinations.test.ts:45 · 🟡🧪 Consider · tests: Wrapping `covered` in a Set stops the test catching a preset shared by mistake (confidence high)
   Before this change, `covered` was a plain array, so the sorted-equality check failed whenever two destinations listed the same preset. Wrapping it in a `Set` was needed so email can share `balanced` with chat (`destinations.ts:71`). It also means the test no longer notices any other duplicate. The reverse-mapping loop does not fill the gap either, because it skips only `email` and checks `destinationOfPreset(p) === d`. So a future destination that reuses, say, `light` would pass that loop only if it came first in `DESTINATION_IDS`. Consider keeping the array and allowing exactly the one known overlap, for example by asserting that the array minus email's presets has no duplicates.
5. apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · 🟠🐛 Fix · bug: The new Library drop test checks for no import, but a file dropped on Library now opens in the window (confidence medium)
   Before this PR, Library mounted the window-wide drop handler. `useFileDrop` is now mounted only through `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which only Export uses. The hook's own doc comment explains why it exists: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`). A search of `apps/kaipu-record/src` found no `will-navigate` guard in main and no other window `drop`/`dragover` listener.

   So after this change, dropping a video on Library no longer imports it; it replaces the app's page with the file. That used to be the documented way to bring a video in. This test checks that `importVideoFiles` is not called, and it also passes while the default navigation still happens. Compare `dropFiles` in `export-page.test.tsx:414-416`, which asserts `!fireEvent.drop(...)` for exactly this reason.

   Suggested fix: keep a default-preventing window guard mounted outside Export (for example a no-op `useFileDrop` in the shell, or `will-navigate` prevention in main). Then make this test assert that `fireEvent.drop` returns false. Also, the test checks `importVideoFiles` synchronously, so an async handler would still pass it.
6. apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:368 · 🟡🧪 Consider · tests: "an unknown ?to= picks nothing" never checks that the cards are unselected (confidence high)
   The test only waits for the "Where is it going?" heading. In `export-page.tsx:74`, `isDestinationId(to)` sends an unknown value to null, which is what produces that heading. But the test never checks that every card in the radiogroup has `aria-checked="false"`, which the test at line 161 does. Adding that line would pin "picks nothing" itself, not just the heading.
7. apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · 🟡🧪 Consider · tests: "with and without a video" only checks the with-a-video URL (confidence high)
   The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. The case without a video, `ROUTES.exportNew` (`/export`), is the link's own `to`, and it never gets an `aria-current` check. Add a second `renderAt(ROUTES.exportNew)` with the same assertion, or rename the test.
8. apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · 🟡🧪 Consider · tests: No test covers the running export in the badge count (confidence high)
   `useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (sidebar.tsx:121-122), and it excludes the copy whose ready card is showing (`ready?.recording.assetId`). The new label reads "copy in progress or ready", yet every test here only goes through `noteFinishedCopy`. Neither the in-progress count nor the exclusion of the ready card's copy is tested.
9. apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:10 · 🟡🐛 Consider · bug: Export with no video has no scroll container, so a short window clips it (confidence medium)
   `.wrap` is deliberately not a scroll box. In the no-video branch, `ExportHeaderEmpty`, `ExportDropZone` and `RecentExports` sit directly in `.screen`, which has `overflow: hidden` (export-page.tsx:101-113, export-page.module.css:9-16). Unlike the with-video layout, they are not inside `.stage` (`overflow-y: auto`). When the header, the zone (36px padding plus title, body and actions) and the recent exports are together taller than the page, the bottom is cut off and cannot be reached, including the last recent exports. One fix: put the drop zone and the recents in a scrolling middle region, and let the Library picker escape that region (portal or fixed position) instead of relying on there being no scroll box.
10. apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · 🟡🧹 Consider · cleanup: Orphaned comment for the removed `.importZone` rule (confidence high)
   The `.importZone` rule is gone, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits right on top of the `.stickyBar` comment, so it reads as if it describes the sticky toolbar. Delete line 108.
```
