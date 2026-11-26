# kaipu-bench-wachi-v3#63 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T01:37:16Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

10 finding(s): 3 to fix, 7 to consider; 10 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 6.** Part 1 has one likely bug. `ExportPage` returns a bare \"Loading…\" whenever `useLocalLibrary.isLoading` is true, and that flag goes true on every re-list, including the ones main triggers with `libraryChanged`. Each re-list therefore unmounts the Export screen and resets the picked destination, the YouTube preset and Fill/Fit. Medium confidence: I did not trace everything that sends the broadcast. The minor issues: picking a card never writes `?to=`, so Back loses the pick; the unreadable-file redirect drops the destination picked on screen; and the `destinationStep` comment claims it ignores a held key, but the code never checks for one. The Email destination, the `preparePath` aliases, the legacy redirects and the router changes are consistent with the PR's documented decisions. Outside this part: the Library page no longer catches window drops, and the renderer has no other drop guard, so a file dropped there falls to Electron's default handling.

**Batch 2 of 6.** I reviewed part 2 of 6: `export-stage.tsx`, `recent-exports.tsx`, `video-picker.tsx`, `library-page.tsx` and the deleted `destination-detail.tsx`. I found one bug (fix, medium confidence) and one design point (consider).

- **Finished exports don't show up while you stay on Export (fix).** The page keeps the library list it loaded on mount. Two things that would refresh it are missing:
  - Finishing an export (the `recordingFinalize` call in `recording-hub.ts`) doesn't send the "library changed" signal.
  - The Export page passes no `onSaved` callback when it starts a copy.

  Prepare got away with this because it left the screen after starting a copy; Export stays. So the copy you just made drops out of "Recent exports" when it finishes. Its destination card also never turns "Ready", and pressing Enter again encodes a second copy instead of opening the first. Confidence is medium because I didn't check the finished-copy tracker in `ready-copies` for another refresh path. Suggested fix: call `refresh()` from `onSaved` in `startCopy`.
- **Fill / Fit has lost its visual preview (consider).** The old screen showed the recording's thumbnail on the vertical or square canvas; now the only explanation is a hover tooltip. Fill cuts off most of a 16:9 screen recording, and nothing on screen shows that before you export.

The video picker and the `library-page.tsx` cleanup look correct.

**Batch 3 of 6.** I found nothing to flag in part 3. I read all seven files in full, plus the code they call into: ready-copies.ts, the export runner, use-file-drop.ts, destinations.ts, routes.ts and the i18n messages.

- **Sidebar badge (sidebar.tsx):** the new `useExportBadge` keeps the old hook's logic: it still clears a copy when its page is opened, and still leaves out the copy whose ready card is on screen. It adds the running export to the count without double-counting it, because the runner clears `ready` when an export starts. The `export.railBadge` message exists in both English and Spanish.
- **Deleted Prepare page:** nothing in the source tree still imports the removed files. `isPrimaryEnter` and the drop import now live in the Export page.
- **Destination tests:** the updated tests match `destinations.ts`. Email shares chat's `balanced` preset, so the test that maps each preset back to its destination skips email and checks that a `balanced` file still reads as chat.
- **Drop-hook test:** the new `useFileDrop` test keeps the behavioural cases of the deleted drop-zone test. The two cases it drops tested the removed `ImportDropZone` component itself.

**Batch 4 of 6.** I reviewed the three test files in part 4. The Export page tests match `export-page.tsx`: the destination row, keyboard handling, the redirect from old Prepare URLs, and drop-to-import. In `library-detail-page.test.tsx` the changes only rename the route from `/prepare` to `/export`.

One fix: the new Library test (`library-page.test.tsx:80`) makes Library's lack of a drop handler the expected behaviour. Library used to catch file drops and stop Electron's default action; it no longer does. `useFileDrop` is now mounted only on Export, and the main process has no `will-navigate` guard. A video dropped on the Library, which used to import it, would now load the raw file in the main window in place of the app. Confidence is medium: that Electron behaviour comes from the hook's own comment, not from code I could read in the repository.

**Batch 5 of 6.** I found no defects in this part, only two optional test gaps, both in `sidebar.test.tsx`.

- **Stylesheets:** every class and `data-*` selector in the new and changed files is used by its component (`destination-row.tsx`, `export-header.tsx`, `export-drop-zone.tsx`, `export-page.tsx`). The `send-more` and `keep-light` values match `groupOf`, and the email logo colour matches the new `email` destination. Every CSS variable referenced (`--tone-heavy`, `--tone-saving`, `--accent-primary-ring`, `--border-light`, `--bg-app`, `--bg-card-hover`) is also used in existing stylesheets.
- **Deleted `prepare-page.test.tsx`:** every behaviour it covered has a matching test in `export-page.test.tsx`.
- **Sidebar tests (`sidebar.test.tsx`):**
  - The test named "with and without a video" only checks the with-video URL (`/export/asset-1`), not the bare `/export` route.
  - Nothing tests the new "in progress" part of the Export badge, which adds 1 while an export is running.

**Batch 6 of 6.** Part 6 (routes, the window-size test, stylesheets, docs and messages) has one small finding: a stale comment in library-page.module.css, at "consider" severity. Everything else checks out:
- **Routes:** the new `/export` routes are wired up, and the legacy `/prepare` URLs redirect there keeping the query.
- **Window size:** Export gets the `main` preset, the same as Prepare did.
- **Stylesheets:** every class in export-stage, recent-exports and video-picker is used by its component, and the new `data-tone` values match what export-stage.tsx sets.
- **Messages:** every new `export.*` key is used, and en.json and es.json have the same keys. Nothing still references the removed `library.import*` or `prepare.prepareAVideo` keys.
- **Docs:** the backlog page matches the code where I checked: the GitHub 10 MB limit, the redirect, and when the rail badge clears.

One question is still open, about code outside this part. With the Library's drop handling gone and no `will-navigate` guard in main, a video dropped on the Library may make the window navigate to the file's URL. The PR's test plan says that drop "does nothing". I left it as an open question for the part that owns library-page.tsx.

<details><summary>What the change connects to (18 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- The Library no longer registers window-wide file drop handling (documented in export-screen.md:50-51) (`apps/documentation/src/content/docs/backlog/export-screen.md:50`) — Does anything else (a webPreferences flag or a main-process `will-navigate` handler outside main/index.ts) stop the default file-drop navigation on pages without `useFileDrop`? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

**Closed, with the lines they rest on**
- Starting a copy from Export (Enter or the Export button) passes an explicit destination to usePrepareCopy (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252`) — Progress and ready status cards; Email shows its Mail logo but the 'your export' wording (the ICU select has no email branch, as the PR documents). If it fails: A second Enter while an export runs shows the busy toast. startExport is fire-and-forget (void) inside the unchanged runner. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-131`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-57`.
- Window-wide file drop on Export imports the video and opens Export on it (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — The drop zone lights up while dragging; Export opens on the new video. If it fails: Import errors are handled by useImportVideos (unchanged). The Library page no longer calls useFileDrop and no renderer-wide dragover/drop guard exists (only use-file-drop.ts listens), so a file dropp… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:36-57`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`.
- The probe of the selected recording gates the Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — 'Reading…' until the probe is ready. If it fails: probeSource has no timeout. If it never settles, the screen stays on 'Reading…' indefinitely (the user can still leave via the rail). Nothing bounds the wait beyond the probe promise itself. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-45`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`.
- Screen state (selected destination, YouTube preset, framings) across library re-lists and remounts (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117`) — ExportScreen is swapped for 'Loading…' and remounts with the URL's destination. If it fails: The user's pick is reset while the chosen ref keeps the old value; on router Back, the selection is lost because it is never written to the URL. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:41-66`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:124-134`, `apps/kaipu-record/src/main/library/index.ts:27`.
- Legacy /prepare URLs redirect to /export keeping the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — Old links land on Export with ?to= preserved. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- Recent exports strip: shows the running export, then the newest finished copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — The running row disappears when the export finishes, and the new copy does not appear until remount. If it fails: Silent: the strip looks as if the export produced nothing. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:124-134`, `apps/kaipu-record/src/main/recording/recording-hub.ts:390-396`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:254-259`.
- VideoPicker list: pick an original to export from; closes on outside mousedown or Escape (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`) — Picking calls onPick → navigate(exportPath(id, current destination)). Evidence: `apps/kaipu-record/src/renderer/src/features/library/tags/tag-chip.tsx:44`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`.
- DestinationStage: upload hint, YouTube preset radio, Fill/Fit radio, size bar against GitHub limit (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:59-144`) — The stage text and bar render from planCopy output. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:183-217`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:230-258`.
- The rail's badge moves from Library to the new Export item. It counts the running export (status "exporting") plus finished copies not yet announced. Opening /… (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export rail item shows a count, labelled through export.railBadge, which exists in both en.json and es.json (line 946). The Library item no longer shows a badge. If it fails: When an export fails (status "error"), the running count drops to 0. The error is still shown by ExportStatusCards, which brings back the progress card on error. The counts live in memory, so a relau… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:321-326`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462`, `apps/kaipu-record/src/shared/routes.ts:17-20`, `packages/i18n/messages/en.json:946`, `packages/i18n/messages/es.json:946`.
- Removed PreparePage, DestinationList and PrepareDropZone; isPrimaryEnter and usePrepareImport move to the Export page. (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — /prepare routes redirect to /export according to the legacy comments in routes.ts. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:279`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:36`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/shared/routes.ts:21-24`.
- A file from the OS is dropped on the Library page, which no longer mounts a drop handler (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Electron's default for an unhandled file drop navigates the BrowserWindow to the file, replacing the app UI; main has no will-navigate guard. If it fails: The window shows the raw video instead of the app, and work in that renderer (such as a running export) is abandoned. Nothing tells the user why. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-12`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`, `apps/kaipu-record/src/main/index.ts:400-411`.
- Export tests drive ExportPage/LegacyPrepareRedirect through a memory router, with mocks for useVideoExport, probeSource and isVideoExportBusy (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:97`) — The assertions match the page: the probe error navigates to exportNewPath, Enter is handled at document level via isPrimaryEnter/destinationStep, and the legacy redirect keeps the search string. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`.
- The Export rail item now carries the badge the Library item used to carry: finished copies the user hasn't seen, plus 1 while an export is running. Opening Exp… (`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44`) — The rail's Export item shows the count, and its accessible name comes from export.railBadge ("N copy/copies in progress or ready"). The Library item no longer shows a badge. If it fails: The ready-copies store is module state, so a remount or router Back re-runs the effect on the current pathname and clears again. Nothing here is async, so nothing can fail silently. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:72-82`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/shared/routes.ts:18-20`, `packages/i18n/messages/en.json:946`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.
- prepare-page.test.tsx is deleted; its behaviour moves to export-page.test.tsx (`apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.test.tsx:1`) — Every behaviour the deleted suite covered has a matching test in the Export suite: the default and per-destination presets, 4K, Fill/Fit, Enter-to-export and its exclusions, one export at a time, unreadable file, screenshots, Ready copy, unexported edits, unknown ?to=, drop impo… Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:169-372`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374-382`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:419-511`.
- Legacy `/prepare/:assetId` and `/prepare` URLs redirect to `/export/:assetId` and `/export`, keeping the query string (`apps/kaipu-record/src/shared/routes.ts:21-24`) — The user lands on Export with `?to=` still preselecting the destination. Evidence: `apps/kaipu-record/src/renderer/src/app/router.tsx:69-74`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`.
- New `/export/:assetId` and `/export` routes, and the window-size preset they get (`apps/kaipu-record/src/shared/window-size.test.ts:21-22`) — The window does not resize when the user navigates to Export. Evidence: `apps/kaipu-record/src/shared/window-size.ts:82-88`.
- New `export` i18n namespace and `prepare.*Email` keys; removed `library.import*` and `prepare.prepareAVideo` keys (`packages/i18n/messages/en.json:881-946`) — Export screen labels in English and Spanish. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-copy.ts:11-26`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:188`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-80`, `apps/kaipu-record/src/renderer/src/features/prepare/destination-copy.ts:17`.
- Size-bar tone moves from `data-direction` to `data-tone` (adds fits/over for GitHub) (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:262-290`) — GitHub's bar is teal when the copy fits the 10 MB limit and amber when it is over. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:299-330`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:203`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 19 | $0.68 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 18 | $0.64 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 14 | $0.40 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 10 | $0.37 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 12 | $0.39 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 23 | $0.62 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 6 batches · $3.10</sub>

<!-- wachi:review -->

<!-- agent-review sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=53d8a40f-2b0a-4556-b76a-4c0d361c5949 -->
