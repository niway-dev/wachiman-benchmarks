# kaipu-bench-wachi-v3#61 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T00:12:21Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

13 finding(s): 4 to fix, 9 to consider; 12 on their lines. Reply in a comment's thread to answer it.

### Outside the diff

- 🟠🐛 **Fix · bug: A video dropped on the Library now makes Electron navigate the app window to the file (confidence high)** (`apps/kaipu-record/src/renderer/src/features/library/components/import-drop-zone.tsx`): This PR deletes the Library's drop zone, and the Library page no longer calls `useFileDrop` (`library-page.tsx:53`: "the Library only lists"). The deleted component's docstring says the Library used to catch drops for the whole window. `useFileDrop` explains why that mattered (`use-file-drop.ts:9-11`): when nothing handles a dropped file, Electron navigates the window to it. Main has no `will-navigate` guard. The only handler is `setWindowOpenHandler` (`main/index.ts:400-403`), which does not cover in-window navigation. So a user who drops a video on the Library out of habit gets the app replaced by a bare file view, with no error and no way back except reloading. Fix: keep a window-level drop guard on the Library. The guard can redirect the files to Export (import, then `exportPath`) or just `preventDefault` and show a toast pointing to Export.

### Summary

**Batch 1 of 6.** I found one bug that should be fixed in this PR. The Library no longer catches file drops, and nothing else in the app stops Electron's default behaviour, so dropping a video on the Library now loads the file in the app window in place of the app. I also suggest one change: disable "Pick from Library" while an import is running, because the import finishing can replace the video the user just picked. The rest of this part checks out: the Prepare-to-Export rewiring, the redirect from old `/prepare` URLs, the new Email destination, and the screen's keyboard handling.

**Batch 2 of 6.** Part 2 has two fix-level problems, plus two smaller consider-level points that the author can decline.

1. **Dropped files replace the app UI (`library-page.tsx`).** The Library no longer mounts `useFileDrop`. That hook's docstring warns that an unhandled drop makes Electron navigate the window to the file, and main has no `will-navigate` guard. Dropping a file on the Library now loads that file in place of the app UI, not "does nothing" as the PR says.
2. **Wrong illustration (`export-stage.tsx`).** The 1080p → sharper text-crop illustration now also shows for TikTok · Reels (1080×1920) and LinkedIn · Feeds (1080×1080). For those copies the sharper-than-1080p claim is false.

Consider-level:
- Fill's crop is no longer shown: the framing preview is gone and the Fill/Fit hint is only a tooltip.
- An Email copy changes its label to "Slack · Discord" in Recent exports once it finishes.

`video-picker.tsx` and the removed `destination-detail.tsx` had nothing to flag.

**Batch 3 of 6.** I found no defects in part 3 and have one suggestion, at "consider" severity. **Sidebar badge (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx`):** the new Export badge works. It clears when the user opens Export or the Library, and a copy that just finished is not counted twice. The part it added, +1 while an export runs, has no test. Unlike finished copies, it also counts while its own progress card is on screen or the user is already on Export. **Deleted Prepare files:** nothing in the app still imports `PreparePage`, `DestinationList` or `PrepareDropZone`. `isPrimaryEnter` now lives in `export-page.tsx`. **Moved drop test:** `use-file-drop.test.tsx` covers the same window drop cases the deleted `ImportDropZone` test did. **Destinations test:** it matches the new email destination, which shares chat's Balanced preset. With the covered presets now in a Set, the test no longer catches a preset listed twice; that change looks intended.

**Batch 4 of 6.** Part 4 covers the three test files. The library-detail test changes only rename routes from /prepare to /export, and I found nothing wrong in them. The new Export page tests are thorough; two test names claim more than the tests check. The main finding: Library's rewritten test confirms that Library no longer handles file drops, but it never checks the drop's default. useFileDrop exists to stop Electron replacing the window with a dropped file, and Library no longer mounts it, so a video dropped on Library now navigates the app window to that file.

**Batch 5 of 6.** I found one minor test issue in this part and nothing else.

`sidebar.test.tsx:39` is named "with and without a video" but only renders the route with a video (`/export/asset-1`). The no-video route `/export` is never checked, though it is the one the sidebar link actually points at. I filed it as "consider".

The rest checks out:
- **Deleted Prepare tests:** every scenario, including drag-and-drop import of outside files, has an equivalent in `export-page.test.tsx`. The old `/prepare` URLs are tested to redirect to Export.
- **Stylesheets:** every CSS variable they use is defined in `packages/tokens/css/tokens.css` or `assets/base.css`. Every class is used by its component. The new `email` logo colour matches the new `email` destination in `destination-logo.tsx`.
- **Removed files:** nothing in the app still references `import-drop-zone`, `prepare-page` or `destination-list.module.css`.

**Batch 6 of 6.** Part 6 has no defects, only two small cleanups. The new routes match how the router uses them. Old Prepare URLs redirect to Export with the query kept, and `preparePath`/`prepareNewPath` now build Export URLs. `presetForPath` gives `/export*` the main window size, and the test covers that. Every class the export stage, recent-exports and video-picker components use exists in their stylesheets. Every `export.*` key they call exists in both locales, and `framing*` comes from `videoEditor`. The keys removed from `library.*` and `prepare.prepareAVideo` are no longer referenced. The backlog doc's claims match the code: the rail position, badge clearing, the three-item recent list and the route aliases. The two cleanups: an orphaned comment left in `library-page.module.css`, and two `prepare.drop*` i18n keys that look unused now that the Prepare drop zone is gone.

<details><summary>What the change connects to (17 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Dropping a file anywhere on the Export screen imports it and opens Export on it with the selected destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — The zone lights up through `drop.dragging`, the title reads importing through `drop.importing`, and the screen then opens on the new video. Extra files are named in a toast. If it fails: The hook is mounted for every ExportPage state (loading, not found, screen), so a drop never navigates the window while Export is open. Import errors go through `useImportVideos` (unchanged). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:36-57`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`.
- The Library stops handling file drops (drop zone and useFileDrop removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — A file dropped on the Library makes Electron load it in place of the app. If it fails: Electron's default navigation is not blocked: main has no `will-navigate` handler. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/main/index.ts:400-403`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:46-60`.
- Document-level Enter and arrow-key handler on the Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277-301`) — Enter on a card or on the body runs the primary action: open the existing copy, or start a copy. If it fails: Items in the VideoPicker dialog are buttons, so Enter there does not export. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:69-90`.
- Legacy `/prepare` URLs redirect to `/export`, keeping the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`) — Old links open the Export screen with `?to=` still applied. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- A copy started with an explicit destination (Email shares chat's preset) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-260`) — The status cards name Email. The `destEmail` copy exists in the messages. If it fails: When an export is already running, `usePrepareCopy` returns false and shows the busy toast (unchanged). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:95-119`, `packages/i18n/messages/en.json:881-884`.
- An unreadable probe redirects to `/export` with a toast (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`) — A toast, then the drop zone with the URL destination kept. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`.
- Library stops mounting the window-wide file drop handler (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — A file dropped on the Library navigates the window to the file, and the app UI disappears. If it fails: Platform default (navigate to the dropped file) is not intercepted, and main has no will-navigate guard. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-47`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:379`, `apps/kaipu-record/src/main/index.ts:393`.
- Upload-size card with text crops is shown for every send-more destination (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:93`) — The illustration says a 1080-wide copy is sharper than a 1080p upload. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:252-256`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:273`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:280`.
- Recent exports reads the export runner snapshot and the Library copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — The strip shows progress, then the finished copy, labelled by its preset's destination. If it fails: A runner in error status is not shown, and the row disappears silently (the error surfaces through the runner's own cards). Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:314`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- VideoPicker opens a list and closes on outside mousedown or Escape (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`) — The list closes. Picking a video navigates to exportPath with the chosen destination kept. Evidence: `apps/kaipu-record/src/renderer/src/features/library/tags/tag-chip.tsx:44`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`.
- The rail's Export item shows a badge: 1 for a running export plus the finished copies not announced yet (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`) — The badge and its aria label (export.railBadge) appear on the Export rail item. The Library item no longer has a badge. If it fails: When an export fails, the status goes to "error", so the running count drops to 0 and the error card shows instead. The ready-copies state lives only in memory, so a relaunch clears it, which the mod… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462-463`, `apps/kaipu-record/src/shared/routes.ts:17-24`, `packages/i18n/messages/en.json:946`.
- Removes PreparePage, DestinationList and PrepareDropZone, and moves the window drop test from ImportDropZone to useFileDrop (`apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:1-73`) — No remaining code imports the deleted modules. The new test covers the same cases as the deleted one, except the click and importing states of ImportDropZone, which was itself deleted. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:16-61`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375`.
- A file dropped on the Library window after Library's drop zone was removed (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Electron's default for an unhandled file drop is to navigate the window to the file, so the app UI is replaced. If it fails: Silent: the window shows the dropped file instead of Kaipu, and nothing reports an error. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`.
- A video dropped on Export is imported and Export opens on it with the selected destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:485`) — The route changes to /export/<new>?to=<dest>. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-52`.
- Sidebar Export entry carries the copy badge (running export + unseen finished copies); opening Export or the Library announces them, opening a copy's page forg… (`apps/kaipu-record/src/shell/sidebar.test.tsx:44`) — The rail's Export link shows a count and the aria label 'N copies in progress or ready'. The Library link no longer shows a badge. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:53`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/shared/routes.ts:15-20`.
- Deletion of the Prepare page tests; coverage replaced by Export page tests (`apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.test.tsx:1`) — Each Prepare scenario has an Export counterpart: destinations, YouTube 1440p/4K, GitHub limit, Reels framing, busy runner, unreadable probe, screenshots, reusing an existing copy, unexported edits, the Enter key, and drop/import of outside files including non-video files. The le… Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:132-372`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374-385`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:419-511`.
- New `/export/:assetId` and `/export` routes; legacy `/prepare/:assetId` and `/prepare` redirect to them (`apps/kaipu-record/src/shared/routes.ts:18`) — Every entry point that used to open Prepare now opens the Export page. The rail's Export item (ROUTES.exportNew, not `end`) lights up on both /export and /export/:id. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-22`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`, `apps/kaipu-record/src/shared/window-size.ts:82-88`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:52-53`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 11 | $0.49 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 18 | $0.62 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 13 | $0.38 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 11 | $0.38 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 20 | $0.46 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 17 | $0.49 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 6 batches · $2.81</sub>

<!-- wachi:review -->

<!-- agent-review sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=7fc66835-8818-4287-80e4-cbba156ae042 -->
