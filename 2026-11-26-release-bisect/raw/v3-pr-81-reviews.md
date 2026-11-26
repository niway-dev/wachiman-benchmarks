# kaipu-bench-wachi-v3#81 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:30:11Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

6 finding(s): 2 to fix, 4 to consider; 6 on their lines. Reply in a comment's thread to answer it.

### Risk map

**Medium.**

- `public-contract` · `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:13` — `preparePath`/`prepareNewPath`, which every "export a copy" entry point calls, now return `/export/...` URLs instead of `/prepare/...`.

**Needs a person:**

- `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:71` (`tradeoff`) — Email is a separate destination over the same `balanced` preset as chat. A Balanced copy shows "Ready" on both cards, and lineage and master-copies label it as chat. Someone needs to decide whether that ambiguity is acceptable.
- `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277` (`direction`) — A document-wide Enter listener starts a background encode from almost any focus. That is convenient, but it is a global shortcut that other screens may copy.

**Read first:** `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts`, `apps/kaipu-record/src/renderer/src/pages/prepare/destination-detail.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx`.

### Summary

**Batch 1 of 6.** Part 1 has no defects. The one finding is optional: Enter-to-export checks less than the arrow keys do, because it does not ignore key presses that come from inside a dialog.

- **Routing:** the old `/prepare` URLs redirect to `/export` and keep the `?to=` destination. The path helpers now return Export URLs.
- **Email:** the destination reaches the export runner, and the status cards fall back to "your export" for it, as the PR says.
- **Shared logic:** the drop and import handling, the source probe and the copy start are reused unchanged, and the new page calls them the same way the removed Prepare page did.
- **Probe wait:** nothing limits how long reading the video's metadata can take, so an unreadable file that never answers leaves "Reading…" on screen until the user leaves. This behaviour is inherited from Prepare, not introduced here.

**Batch 2 of 6.** Part 2 has 2 findings: 1 fix and 1 consider. Fix (medium confidence): removing the Library's window drop handling leaves file drops unhandled. Nothing else in the renderer or main process blocks Electron's default, so a file dropped on the Library likely loads in place of the app. The PR body says such a drop "does nothing", but the app was not run in Electron. Consider: in Recent exports, an Email copy shows the Email logo while it runs and changes to \"Slack · Discord\" once it finishes. The new stage, picker and size-bar code match the deleted Prepare detail, and every i18n key they use exists in the new `export` namespace. One question is still open: whether opening a copy from Recent exports marks it seen.

**Batch 3 of 6.** Part 3 has no findings. The deleted pages/prepare files (destination-list, prepare-drop-zone, prepare-page) and the deleted ImportDropZone test have no importers left in the app. isPrimaryEnter is redefined in pages/export/export-page.tsx, and the pages/prepare directory is now empty. The new use-file-drop.test.tsx keeps the useFileDrop coverage the deleted test had (enter/leave depth, accepting a drop, ignoring drags without files, unmount) and checks it against the hook's window listeners. The only cases dropped are the click and disabled cases that tested ImportDropZone itself. The destinations.test.ts changes match destinations.ts: email is in keep-light and maps to the balanced preset, and destinationOfPreset("balanced") still returns "chat". In the sidebar, the badge moved from Library to the new Export item. It adds 1 while the export runner is exporting, and announces ready copies on both /export/* and /library. Announcing does not clear the Library page's unseen-copy outline.

**Batch 4 of 6.** Part 4 has one problem: one of the new Library tests hides a regression. This PR removes the Library's only drop handling, and that test (`library-page.test.tsx:80`) checks only that nothing is imported. Nothing else in the renderer or main stops an unhandled file drop, and the repository's own comment at `use-file-drop.ts:10-11` says Electron then navigates the window to the file. So dropping a file on the Library takes the window to the file instead of doing nothing, as the PR description claims, and work held in the renderer goes with it. I rated this "fix" with medium confidence: Electron's behaviour comes from the repo's comment and tests, and the author says the app was not run in Electron. The Export page tests match the code in `export-page.tsx`, `use-prepare-import.ts`, `use-prepare-copy.ts` and `prepare-path.ts`. That covers the keyboard, the existing-copy shortcut, the old Prepare URL redirect, the probe-error redirect and the drop import. The `library-detail-page.test.tsx` changes only switch the expected paths from `/prepare` to `/export`, in line with `preparePath`.

**Batch 5 of 6.** Part 5 covers the sidebar test, the deleted Prepare test and the stylesheets. I found one issue worth flagging, and it is minor.

**What checks out:**
- **Deleted Prepare test:** the cases from `prepare-page.test.tsx` have counterparts in `export-page.test.tsx`: busy, unreadable file, screenshot, Ready copy, unexported-edits warning, drops (one, several, non-video) and Back URLs. The deliberate behaviour changes have their own tests: Export stays on screen after an export starts, and an unknown `?to=` now picks nothing.
- **Stylesheets:** every CSS variable they use is defined in the tokens or in `base.css`.
- **Selectors:** the `data-group`, `data-tone` and `data-active` values match what `destination-row.tsx` and `destinations.ts` emit.

**The issue (consider, tests):** the sidebar test \"is active on Export with and without a video\" only renders `/export/asset-1`. The no-video URL `/export` is never asserted. The badge's new \"export in progress\" count is not tested either.

**Batch 6 of 6.** I found one cleanup issue in this part (routes, the window-size test, Export stylesheets, backlog docs and i18n messages): a leftover comment in `library-page.module.css` (line 108). It describes the "Drop a video here" strip, which this change removes.

Checks that came out clean:
- **Removed message keys:** no renderer code still uses the removed Library or Prepare keys.
- **New message keys:** every key in the new `export` namespace is used by the Export components, and en.json and es.json have the same keys.
- **CSS classes:** every class the Export stage, recent-exports and video-picker components use exists in their stylesheets. The new `data-tone` values (`fits`, `over`, `lighter`, `not-lighter`) match what `export-stage.tsx` sets.
- **Legacy routes:** the old Prepare routes redirect through `LegacyPrepareRedirect`, which keeps the query.
- **Backlog doc:** its claims about the rail badge, the redirects and the Recent exports list match the code I read.

`routes.ts` stays free of value imports from workspace packages, as the repository rule requires.

<details><summary>What the change connects to (17 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Recent exports: a finished row opens the copy's Library page (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:68`) — Does opening the copy's page mark it seen, so the rail badge's unseen count drops the way it does when the copy is opened from the Library? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx`.

**Closed, with the lines they rest on**
- Enter anywhere on the Export screen runs the primary action (open the existing copy or start an encode) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — The progress card appears and the screen stays on Export. With an existing copy, the app navigates to `/library/<id>`. If it fails: If an export is already running, `isVideoExportBusy` shows the busy toast, so nothing is lost silently. The listener is removed on unmount. Because `keys.current` is refreshed on every render, the ha… Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:262-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:275-301`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-102`.
- Email destination passes destination: "email" through usePrepareCopy to the export runner (`apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`) — The status cards' ICU select has no `email` branch, so the title falls through to `other` ("your export"). The job icon uses DestinationLogo, which now has a Mail icon for email. If it fails: The master copies panel identifies copies by preset, so a finished Email copy is listed as "Slack · Discord · Email". The PR calls this a deliberate decision. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-67`, `packages/i18n/messages/en.json:1474`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:66-72`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- Source probe for the Export screen (useSourceProbe → probeSource); the screen shows "Reading…" until it resolves (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — Shows "Reading…" first, then the screen or the toast. If it fails: Nothing bounds the whole wait: `probeSource` awaits several media reads in sequence with no timeout. It catches rejections and returns null, which becomes an error. A read that never settles leaves "… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`.
- A file dropped on the window, or picked with Browse files, is imported and opened on Export with the selected destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — Export opens on the imported video. If it fails: A video can be dropped anywhere on Export because `useFileDrop` catches window drops while the page is mounted. `chosen` is reset when assetId changes, and openVideo/drop write the selection into `?t… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`.
- Legacy /prepare and /prepare/:assetId URLs redirect to Export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — The old deep links land on Export. Evidence: `apps/kaipu-record/src/shared/routes.ts:18-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- Library no longer handles window file drops (useFileDrop/ImportDropZone removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — The PR says a drop does nothing. In practice the Electron default applies, and the window navigates to the dropped file. If it fails: The renderer app is replaced by the file view, and its state is lost until a reload. Nothing in the code catches it. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:25-56`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:400-403`.
- VideoPicker: the open list closes on Escape or on a click outside it (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`) — The list closes. When an item is picked, onPick navigates to Export for that video. Evidence: `apps/kaipu-record/src/renderer/src/features/library/tags/tag-chip.tsx:44`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`.
- DestinationStage primary action: export, or open the existing copy (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:120-141`) — The export runs in the background, and its progress shows in the Recent exports strip and the rail badge. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`.
- The rail's Export item shows a badge: 1 for a running export plus the finished copies not yet announced (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The badge and its aria label ('# copy in progress or ready') appear on the EXPORT rail item. The Library item no longer has a badge. If it fails: On error, status becomes 'error', so the running count drops to 0 and the error card shows the failure. No new async call is made here. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121-122`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:70-75`, `packages/i18n/messages/en.json:946`.
- Visiting /export or /export/:assetId announces ready copies, which clears the rail badge for finished copies (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117-119`) — The badge clears while the user is on Export. The Library page keeps outlining the unseen copies. If it fails: The state is in memory only: a relaunch starts with nothing pending, as before. After a remount the effect re-runs on the same pathname, and announceReadyCopies returns early when every copy is alrea… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-64`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:78-80`, `apps/kaipu-record/src/shared/routes.ts:18-20`.
- A file from the OS is dropped on the Library page, which no longer mounts any drop handling (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — In Electron, an unhandled file drop navigates the main window to the file, so the app UI goes away. The test checks only that importVideoFiles is not called. If it fails: The renderer unloads with no error. Renderer state is lost, including a background export, which runs in the renderer. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`, `apps/kaipu-record/src/main/index.ts:400-411`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:414-416`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:89-91`.
- Old /prepare and /prepare/:assetId URLs redirect to Export, keeping the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — The Export screen opens with the ?to= destination preselected. If it fails: This is a synchronous redirect with no async step. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-22`.
- Probe failure on Export: a toast, then a replace-navigation to /export carrying the URL destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329`) — The user sees a toast and the empty Export screen with its drop zone. If it fails: A failure is visible to the user. A probe that never resolves leaves the screen on 'Reading…'. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:94-99`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`.
- The rail badge for finished and running copies moves from Library to the new Export entry. Opening Export (or the Library) marks the ready copies as announced. (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export rail item shows the count with the label from export.railBadge ("N copies in progress or ready"). The Library item no longer shows a badge. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.
- The no-video drop zone wrapper no longer scrolls (`overflow-y: auto` removed) and now takes `flex: 1` inside the non-scrolling column `.screen`. (`apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:2`) — On a window shorter than the zone plus the header and Recent exports, the zone overflows instead of scrolling. The main window's minimum height is 670 px, so at the supported sizes it should fit. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:2-11`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.module.css:9-16`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:103-112`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.module.css:2-7`, `apps/kaipu-record/src/shared/window-size.ts:50`.
- Legacy `/prepare/:assetId` and `/prepare` URLs now redirect to `/export/:assetId` and `/export` (`apps/kaipu-record/src/shared/routes.ts:21-24`) — Old deep links and existing preparePath() callers land on the Export screen with the same destination preselected. If it fails: No async work. A missing assetId falls back to ROUTES.exportNew. `replace` keeps router Back from bouncing back into the redirect. Evidence: `apps/kaipu-record/src/renderer/src/app/router.tsx:69-74`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/shared/routes.ts:17-24`.
- New Export rail badge, which also clears finished copies on Export and Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-120`) — The badge count shows on the EXPORT rail entry, with an accessible label from export.railBadge (en and es plurals). Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:115-119`, `packages/i18n/messages/en.json:946`, `packages/i18n/messages/es.json:946`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 16 | $0.61 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 14 | $0.55 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 13 | $0.38 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 14 | $0.51 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 14 | $0.39 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 16 | $0.49 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 100 in / 39k out / 2.3M cache read / 341k cache write · $2.95</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=61b355d7-52c0-4228-8742-fa7a0d70e7a7 -->
