# kaipu-bench-wachi-v3#83 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:30:33Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

9 finding(s): 3 to fix, 6 to consider; 8 on their lines. Reply in a comment's thread to answer it.

### Risk map

**Low.**

**Needs a person:**

- `apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:72` (`direction`) — Only Export accepts dropped files now. Someone has to decide whether the other screens should refuse drops cleanly or send the user to Export, instead of falling through to Electron's navigate-to-file default.

**Read first:** `apps/kaipu-record/src/renderer/src/pages/prepare/destination-detail.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx`, `apps/kaipu-record/src/renderer/src/pages/prepare/destination-list.tsx`.

### Outside the diff

- Nit · 🟡📝 **Consider · docs: Crop section comment says YouTube only, but every upload destination shows it (confidence high)** (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:156`): The comment says `YouTube: an illustrated before / after of small text.` But `UploadSizeCard` renders `.crops` for every `send-more` destination, including TikTok · Reels and LinkedIn · Feeds (export-stage.tsx:93-104 and 252-257). The backlog doc says the same. Reword it to "Upload destinations: …".

### Summary

**Batch 1 of 6.** This part covers the Export page, its header, destination row and drop zone, the new Email destination, the path helpers and the router. Email is threaded through correctly: every exhaustive record gained an entry, and `usePrepareCopy` takes an explicit destination. The legacy `/prepare` redirect keeps the query.\n\nThere is one bug, at `export-page.tsx:117`. The `isLoading` gate runs again on every Library re-list, because `refresh` sets loading to true each time. That unmounts `ExportScreen`, and the user's destination, YouTube resolution and Fill/Fit choices are lost. Re-lists happen on broadcasts that are common while the screen is open, including the one that follows the user's own export finishing. The PR now keeps the user on Export after an export starts, which makes this easy to hit.

**Batch 2 of 6.** Part 2 has two findings, one to fix and one to consider. The fix: the Library no longer handles window drops, and nothing else guards them. useFileDrop's own comment says Electron then navigates the window to the dropped file, and main sets no will-navigate guard, so a drop on the Library replaces the app UI. That contradicts the PR's claim that such a drop "does nothing". To consider: the new 1440p/4K and Fill/Fit radio groups ignore the arrow keys, while the page's arrow handler assumes they handle them themselves. In the rest of the part, export-stage, recent-exports and video-picker match the runner and planCopy as read.

**Batch 3 of 6.** Part 3 reviewed: the Prepare page deletions, the sidebar badge move and the test changes. Nothing in these files needs changing.

**Sidebar badge** (`sidebar.tsx`): the badge now sits on the Export item and counts the running export plus finished copies the user hasn't been shown. Opening `/export` or `/library` clears the finished copies, and the Spanish and English badge labels match the new meaning. Nothing in the code contradicts the PR body here.

**Test changes:**
- `use-file-drop.test.tsx` keeps the `useFileDrop` checks that were in the deleted ImportDropZone test.
- `destinations.test.ts` is updated correctly for Email reusing the Balanced preset.

**Issue in another part's file:** the PR says dropping a file on the Library "does nothing". But `use-file-drop.ts:8-12` says a file dropped where nothing handles it makes Electron load that file in place of the app. `main/index.ts` has no guard against that, only `setWindowOpenHandler`. So a video dropped on the Library may now replace the app with the video file. I logged this as an open contract rather than a finding because the fix belongs in `library-page.tsx` or `main/index.ts`, which this part doesn't cover. It was not run in Electron.

**Batch 4 of 6.** I reviewed the new Export page tests, the switch from /prepare to /export in the Library detail tests, and the trimmed Library page tests.

The Export tests match the code in export-page.tsx, prepare-path.ts and use-prepare-import.ts.

The Library has a problem. Its rewritten test confirms that the page no longer imports a dropped video, but nothing on the page now handles the drop at all. In Electron, an unhandled file drop navigates the window to that file. The repository's own comment in use-file-drop.ts says so, and the main process has no `will-navigate` guard. The test also cannot fail: the shared setup stubs `pathForFile` to return an empty string, so `importVideoFiles` would never be called even if a drop handler were still mounted.

**Batch 5 of 6.** I found no defects in part 5 (8 files). There are two optional test suggestions on `sidebar.test.tsx`; neither blocks the merge:

- **Active-state test checks only one URL.** The test named "is active on Export with and without a video" only renders `/export/asset-1`. The bare `/export` URL is never checked.
- **Running exports are untested in the badge.** The Export badge now adds 1 while an export is running. Every test only uses finished copies, so that part of the count has no coverage.

What I checked:
- **Stylesheets.** Every CSS variable the new styles use is defined in `packages/tokens/css/tokens.css` or `base.css`. Every class is referenced by its component. The `data-group` and `data-tone` values match what `groupOf` and `destination-row.tsx` emit.
- **Deleted Prepare tests.** The scenarios they covered now have equivalents in `export-page.test.tsx`.

**Batch 6 of 6.** Part 6 covers routes, the window-size test, the Export stylesheets, the removed Prepare and Library CSS, the backlog doc and the i18n messages. I found no defects, only two optional "consider" notes:

- **Leftover comment:** an orphaned NIW2-579 comment at `library-page.module.css:108` now sits above the sticky-bar rule, where it reads as if it described it.
- **Stale comment:** the crop-section comment at `export-stage.module.css:156` says YouTube only, but the before/after crops show on every upload destination.

What I checked:
- **Routes:** `shared/routes.ts` adds only string literals, with no value imports from workspace packages. The legacy `/prepare` redirect keeps the query string and replaces the history entry.
- **Stylesheets:** every class the export components use exists in their CSS modules, including the new `data-tone` values `fits` and `over`.
- **Messages:** no code still uses the removed `library` or `prepare` i18n keys. The new `export` and email keys are used, and `en.json` and `es.json` have the same keys.
- **Backlog doc:** its claims hold where I checked them: the badge is cleared on Export or the Library, the stage scrolls on its own, and the legacy URLs redirect.

<details><summary>What the change connects to (15 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Deleting ImportDropZone takes away the Library's window-wide file drop. The PR says 'dropping a file there does nothing'. (`apps/kaipu-record/src/renderer/src/features/library/components/import-drop-zone.test.tsx:1`) — Does anything else in the renderer or main stop the default file-drop navigation on the Library page now that useFileDrop is gone? The Record and Editor pages already had this gap before the PR. Files that would answer it: `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`, `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/app/router.tsx`.

**Closed, with the lines they rest on**
- Library re-list while the Export screen is open (export finished, import, screenshot, cloud refresh) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117`) — The screen flashes to Loading; the destination, YouTube resolution and framing go back to their URL or default values. If it fails: The user's choices are lost silently on every broadcast, including the one that follows their own export finishing. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:41-48`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:133`, `apps/kaipu-record/src/main/library/index.ts:25-29`, `apps/kaipu-record/src/main/library/index.ts:185`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:212`.
- Enter starts an export (or opens an existing copy) from a document-wide keydown listener (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277-301`) — The progress card appears, with the destination passed explicitly (Email falls back to "your export" because the ICU select has no email branch, as the PR states). If it fails: Pressing Enter while another export runs shows a toast; held keys are ignored by the event.repeat check. The VideoPicker items are buttons, so Enter inside the picker is excluded. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-131`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:82-90`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-57`.
- File dropped on the window while Export is open: imported, then Export opens on it with the current destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — Export opens on the new video. If it fails: Import errors come from useImportVideos. With no destination row on /export, current() is only urlDestination. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-47`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`.
- Legacy /prepare URLs redirect to /export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`) — The Export screen opens with ?to= preselecting the destination. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- Library stops handling window-level file drops and loses its import buttons (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Dropping a file on the Library makes Electron navigate the window to the file, and the app UI is replaced. If it fails: The user loses the app view until a reload; nothing tells them why. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:9-11`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:400-403`.
- RecentExports reads the export runner snapshot to show the copy being exported now (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34`) — The running row shows its percentage; finished rows come from the library list newest-first, limited to three in total. If it fails: On error the status is 'error', so the running row disappears and only finished copies show. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:59`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:321`.
- SizeBarCard draws GitHub's bar against the 10 MB free limit (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:296`) — The bar fill and tag show fits/over or lighter/not-lighter. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:202-203`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:262-268`.
- The rail badge moves from Library to the new Export item and now counts a running export plus finished copies nobody has been shown yet. Opening /export or /li… (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The badge appears on the Export item with the label export.railBadge ('# copy in progress or ready'). The Library item has no badge now. If it fails: The ready-copies store lives in memory, so a relaunch clears it, as before. The running count comes straight from the runner's status, so it can't drift. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-75`, `apps/kaipu-record/src/shared/routes.ts:20`, `packages/i18n/messages/en.json:946`.
- A video dropped anywhere on the Export window is imported and Export opens on it, keeping the selected destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:485`) — The drop zone lights up while a file is dragged, then the route changes to /export/<new>?to=<dest>. A toast names any extra videos, and another toast lists files that were skipped. If it fails: If the import fails, useImportVideos shows the error through reportError (use-import-videos.ts:84-85). Files that are not videos are skipped with a toast. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:21-58`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:96-115`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:75-88`.
- A file dropped on the Library page is no longer handled (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Electron's default behaviour applies, and the window navigates to the dropped file. If it fails: The app UI is replaced by the file without any message. The main process has no will-navigate guard to stop it. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-15`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:400-403`.
- Old /prepare URLs redirect to /export and keep the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — The Export screen opens for the same recording with the same destination. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`.
- Sidebar Export badge: counts a running export plus unannounced finished copies, and clears when either Export or the Library opens (`apps/kaipu-record/src/shell/sidebar.test.tsx:44`) — The Rail item for Export shows the count and the accessible label export.railBadge ("N copy/copies in progress or ready"). Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `packages/i18n/messages/en.json:946`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.
- Coverage of the deleted PreparePage tests moves to ExportPage tests (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:132`) — The scenarios that matter have equivalents in export-page.test.tsx: busy, unreadable file, screenshots, existing copy reused, unexported edits, dropping files (video, several videos, non-video), and the drop zone lighting up. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:319-368`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:460-511`.
- Legacy /prepare/:assetId and /prepare URLs redirect to /export/:assetId and /export, keeping the query string (`apps/kaipu-record/src/shared/routes.ts:21`) — The user lands on Export with the same destination preselected. Because the redirect uses replace, Back skips the legacy URL. If it fails: This is synchronous client routing with no async work. A missing assetId falls back to /export. Evidence: `apps/kaipu-record/src/renderer/src/app/router.tsx:69-74`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`.
- The rail badge's finished copies are cleared when the user opens Export, as the backlog doc claims (`apps/documentation/src/content/docs/backlog/export-screen.md:28`) — The Export rail badge drops the finished copies when the user opens Export or the Library. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:104-119`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 19 | $0.62 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 13 | $0.49 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 11 | $0.34 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 16 | $0.49 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 14 | $0.39 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 17 | $0.48 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 114 in / 39k out / 2.5M cache read / 306k cache write · $2.81</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=794fb4a6-8e8a-4f4b-a516-636fedca0664 -->
