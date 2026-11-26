# kaipu-bench-wachi-v3#65 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T01:38:14Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

17 finding(s): 3 to fix, 14 to consider; 16 on their lines. Reply in a comment's thread to answer it.

### Outside the diff

- 🟡🧹 **Consider · cleanup: Chat destination still names Email now that Email has its own card (confidence medium)** (`packages/i18n/messages/en.json:828`): `prepare.destChat` is still "Slack · Discord · Email", and `sayChat`/`whyChat` (lines 841, 850) still talk about email. Email is now a separate destination (`destEmail`, line 881). The Export cards use `export.cardChat` ("Slack · Discord"), but `master-copies-panel.tsx:68` still names a Balanced copy with `DESTINATION_COPY.chat.name` (= `destChat`). So the Library detail says "Slack · Discord · Email" while Export lists Slack · Discord and Email as two different cards. If the overlap is meant to stay, say so in the doc's Email decision; otherwise drop "Email" from `destChat`.

### Summary

**Batch 1 of 6.** Part 1 has one finding, at "consider". The new `destination` input on `usePrepareCopy` is meant to make the progress and ready cards name Email. But the `progressTitle` and `readyTitle` ICU messages have no `email` branch, so an Email copy is announced as \"Preparing your export…\" (`use-prepare-copy.ts:119`). Nothing else in this part needs a change. The routing and legacy redirect, the drop/import flow, the keyboard handling and the email preset mapping all checked out against the unchanged hooks they call. A probe that stalls can leave \"Reading…\" on screen indefinitely, but that wait is inherited from Prepare, not introduced here.

**Batch 2 of 6.** Part 2 has one defect: the Library no longer handles window drops, and nothing in main blocks file navigation. A dropped MP4 then likely replaces the app window with the file and takes the background export runner down with it, which contradicts the PR body's \"dropping a file there does nothing\". The rest are suggestions: the radio groups ignore the arrow keys, the Keep card says \"sound as recorded\" for silent recordings, the picker dialog doesn't manage focus, and Recent exports names Email copies \"Slack · Discord\". The new stage, recent-exports and picker code otherwise wires correctly to the unchanged destination, estimate and runner code.

**Batch 3 of 6.** I reviewed all seven files in part 3. One bug needs fixing, in `sidebar.tsx`, plus two smaller suggestions.

- **Badge clears on the wrong screen (fix):** the new Export rail badge clears unseen finished copies on every `/export/*` URL. The only screen that lists those copies is `/export` with no video, so opening Export for a single video (`/export/:assetId`) wipes the count without showing any of them. Changing the match to `end: true` fixes it.
- **Missing test (consider):** the +1 the badge adds while an export is running has no test.
- **Stale docs (consider):** `ready-copies.ts` and `background-copy-toasts.md` still say the count sits on the Library rail item.

The deleted Prepare files left no remaining references in `src`; `isPrimaryEnter` now lives in `export-page.tsx`. The `use-file-drop` test checks what `use-file-drop.ts` actually does. The `destinations` test matches email sharing chat's preset.

One thing outside this part: the Library page no longer calls `useFileDrop`, so outside the Export page nothing catches a file dropped on the window. I found no navigation guard in the main process, which means Electron would open the dropped file in the window. That belongs to `library-page.tsx`, which another part covers.

**Batch 4 of 6.** Part 4 is three test files. The Export page tests match `export-page.tsx` and the message strings they assert. The library-detail tests only swap `/prepare` for `/export`. One real issue: the new Library test, \"does not take a video dropped on the window\", locks in a regression. With the Library's drop strip gone, nothing calls `preventDefault` on a file dropped there, and per `use-file-drop.ts`'s own comment Electron then navigates the window to the file. The test only checks that nothing was imported. There is also one small note about where an Export drop test is grouped.

**Batch 5 of 6.** I found no defects in this part, only three small "consider" findings. Every CSS token the new stylesheets use exists in packages/tokens or base.css. The drop and import tests removed with prepare-page.test.tsx were moved into export-page.test.tsx, so no coverage was lost. Two findings are test gaps in sidebar.test.tsx: the "with and without a video" test only renders the with-video URL, and nothing tests the running-export count the badge now adds. The third is a question, at low confidence, about whether the Library picker in the empty Export state can be clipped by `.screen`'s `overflow: hidden` at the default window size.

**Batch 6 of 6.** Part 6 covers routes, the window-size test, stylesheets, the backlog doc and the en/es messages. Nothing here blocks the merge. Three findings, all \"consider\":
- **Email wording:** the new Email destination's copy promises the file \"fits an attachment\", but the Balanced preset it uses has no size cap (about 5.4 MB/min).
- **Chat name:** `prepare.destChat` still reads \"Slack · Discord · Email\", though Email now has its own card.
- **Leftover comment:** `library-page.module.css` still has the comment for the removed drop strip.

Checked and fine:
- The removed i18n keys have no remaining references.
- The `data-tone` values in the stylesheet match `export-stage.tsx`.
- The \"stage scrolls on its own\" comment holds: the page's `.stage` container is the one with `overflow-y: auto`.
- The backlog doc's claims about the rail badge, the redirects and \"three in all\" Recent exports match the code.

Still open: I did not read `LegacyPrepareRedirect`, so I have not confirmed it keeps the `?to=` query.

<details><summary>What the change connects to (17 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Export empty state drop zone layout inside the Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:2`) — Does the picker panel fit inside .screen at the 900×670 default window? Files that would answer it: `apps/kaipu-record/src/renderer/src/pages/export/export-header.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx`.
- Add /export and /export/:assetId routes; turn /prepare and /prepare/:assetId into legacy redirects (`apps/kaipu-record/src/shared/routes.ts:17-24`) — I did not read LegacyPrepareRedirect in export-page.tsx (another part of this review), so I have not confirmed that it keeps the `?to=` query and uses replace, which would stop Back from looping into the redirect. Files that would answer it: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx`.

**Closed, with the lines they rest on**
- Export button / Enter starts a copy with an explicit destination (email included) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-260`) — Progress and ready cards use job.destination for the logo and the ICU title (export-status-cards.tsx:55-62,134,186). "email" has no select branch, so the title falls back to "export" (en.json:1474,1480). If it fails: While another export runs, the user sees a toast and nothing starts. probeSource never throws (probe-source.ts:42-43). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-131`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-62`, `packages/i18n/messages/en.json:1474`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:314`.
- File drop / Browse files on Export imports and opens the video with the chosen destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — Navigates to /export/:assetId?to=<current>. ExportScreen is keyed by id, so it remounts with initialDestination from the URL. If it fails: useFileDrop catches the window drop, so Electron does not navigate to the file. Import failures surface through useImportVideos toasts (not re-read here). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:36-57`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-22`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`.
- Probe of the selected recording gates the screen ("Reading…") (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92-99`) — "Reading…" until the probe is ready. On error the user sees a toast and is sent to /export with ?to= kept. If it fails: probeSource catches every error and returns null, which becomes the error toast. No timeout bounds the mediabunny reads over kaipu-media://, so a stalled read leaves "Reading…" up until the user navi… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`.
- Document-level Enter/Arrow handler on the Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:275-301`) — Enter exports or opens the existing copy unless the target is a field or a non-radio button or link. Picker items are buttons, so Enter there picks the item and does not export. If it fails: Enter with nothing selected does nothing (primary returns when plan is null). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:262-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:82-89`.
- Legacy /prepare URLs redirect to /export keeping the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`) — The Export screen opens with ?to= preserved. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- Library no longer handles a file dropped on the window (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Chromium navigates the main window to the dropped file's file:// URL; nothing in main blocks it. If it fails: The app UI is replaced, and the renderer-owned export runner and app state are lost. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:49-56`, `apps/kaipu-record/src/main/index.ts:400-411`.
- Recent exports reads the export runner and lists the newest copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — The running row's percentage comes from runner.fraction; when the export finishes, the copy appears in the useLocalLibrary list. If it fails: If the runner errors, status becomes "error" and the running row disappears; the error is surfaced by the runner's own cards, not by this list. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26-27`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:321-322`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:337-338`.
- DestinationStage primary / Export again buttons (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:120-141`) — The export runs in the background; the screen stays and the progress card shows it. If it fails: Start failures go through the runner's error state and toasts (unchanged code). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:322-324`.
- VideoPicker opens a list and picks a video (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-90`) — Picking a video navigates to exportPath(v.assetId, current destination). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`.
- The Export rail item's badge clears (announces) unseen finished copies when Export opens (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117`) — The rail badge goes to 0 on any /export/* URL. The Library chip and outlines stay until each copy is opened (markCopySeen). If it fails: On /export/:assetId the badge clears even though no finished copy is shown. The notice is lost silently (reported as a finding). Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-120`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-64`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:101-112`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:26-36`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:59-63`.
- The Export badge adds 1 while an export is running (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121`) — The badge shows 1 while exporting, then counts unseen copies once the export finishes. It drops to 0 on error. If it fails: An error or cancel takes the running export out of the count; the error card is what tells the user. Nothing is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:463`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:70-75`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:35`.
- The ImportDropZone test is replaced by a test of useFileDrop alone (`apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:1`) — The test covers the depth counter, preventDefault on file drops, ignoring non-file drags, and removing the listeners on unmount. All of these match use-file-drop.ts. If it fails: The Library page no longer calls useFileDrop, so outside the Export page nothing intercepts a dropped file. No will-navigate guard was found in main. The fix belongs to library-page.tsx, which is in… Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:16-60`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53-54`.
- A file dropped on the window while the Library page is shown (the test asserts nothing is imported) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — On Library, no handler takes the drop. Per the hook's own comment, Electron then navigates the window to the dropped file, replacing the app UI. If it fails: The failure is silent: no toast or error appears, and the app view is replaced by the file. The test does not check whether the default was prevented, so it passes while this happens. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-15`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-47`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`, `apps/kaipu-record/src/main/index.ts:400-403`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:414-416`.
- Old /prepare and /prepare/:assetId URLs redirect to Export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — The tests check the pathname, the search and the destination heading after the redirect. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:167-173`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:375-386`.
- An unreadable probe shows a toast and redirects to /export (asserted by a test) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329`) — A toast, then the empty Export screen. If it fails: The test covers the failure path: a toast is shown, the page redirects, and no export starts. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:94-99`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329-337`.
- Export rail item badge: counts a running export plus finished copies not yet announced; cleared on /export* or /library (`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44`) — Rail badge number and accessible name via tExport('railBadge'). Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/shared/routes.ts:18-20`.
- Remove library.importVideo/importing/importDrop* and prepare.prepareAVideo messages (`packages/i18n/messages/en.json:603-608`) — No missing-message fallbacks: a search of apps/ finds no remaining reference to the removed keys. Evidence: `packages/i18n/messages/en.json:603-608`, `packages/i18n/messages/es.json:603-608`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 13 | $0.50 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 15 | $0.61 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 21 | $0.63 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 10 | $0.38 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 14 | $0.38 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 24 | $0.55 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 6 batches · $3.05</sub>

<!-- wachi:review -->

<!-- agent-review sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=adb244f4-dc35-4f85-8f25-46ec300b4735 -->
