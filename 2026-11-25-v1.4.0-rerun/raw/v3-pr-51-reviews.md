# kaipu-bench-wachi-v3#51 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T00:03:49Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

10 finding(s): 3 to fix, 7 to consider; 9 on their lines. Reply in a comment's thread to answer it.

### Outside the diff

- 🟡📝 **Consider · docs: Crop comment still says YouTube only (confidence high)** (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:156`): The comment `/* YouTube: an illustrated before / after of small text. */` is out of date. `UploadSizeCard` in `export-stage.tsx:252-257` draws the crops for every `send-more` destination: YouTube, TikTok · Reels and LinkedIn · Feeds. That matches the backlog doc, which says every upload destination gets the illustrated crop. Changing the comment to "Upload destinations: …" would keep it accurate.

### Summary

**Batch 1 of 6.** Part 1 (routes, the export-page components and the prepare helpers) has no blocking or "fix" issues. Two minor "consider" findings:
- **Enter while a dialog is open:** the screen-wide Enter-to-export check skips fields, buttons and links but not open dialogs (the arrow-key check does skip them). With the Change-video list open and focus on the page body, Enter starts an export behind it.
- **Duplicated destination order:** `EXPORT_ORDER` repeats `DESTINATION_IDS` and nothing checks that the two stay the same.

What checks out:
- **Email destination:** `destinationOfPreset("balanced")` still returns `chat`.
- **Changing video:** the new screen never starts from the previous video's probe, and the selected destination carries over through `?to=`.
- **Legacy redirect:** old `/prepare` URLs re-encode the id and keep the query.

One open question, outside this part: I found no guard in the main process against Electron opening a file dropped on the window. Now that the Library no longer takes drops, I can't confirm that a drop there "does nothing" as the PR says.

**Batch 2 of 6.** Part 2 has one fix and one consider. The fix: the Library no longer registers the window-wide drop guard, and the main process has no will-navigate guard, so a file dropped on the Library makes Electron replace the app UI with the file. That contradicts the PR's \"dropping a file there does nothing\". The consider: the Archive card always says \"sound as recorded\", even when the recording has no audio. The other new components (export-stage, recent-exports, video-picker) match the unchanged runner, CopyPlan and i18n contracts they call.

**Batch 3 of 6.** Part 3 has one problem, in `useExportBadge` (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117`): it clears the rail badge on `/export/:assetId` as well as on `/export`. Only the no-video `/export` screen lists recent exports. So copies that finish while the user stays on a recording's Export screen, and unrelated copies that finished earlier, lose their badge without being shown anywhere. Fix: match `/export` exactly (`end: true`) for the clearing.

Nothing else in this part needs a change:
- The deleted Prepare files (`prepare-page.tsx`, `destination-list.tsx`, `prepare-drop-zone.tsx`) have no remaining importers; the old `useLibraryBadge` name is gone too.
- The new `use-file-drop.test.tsx` matches what `useFileDrop` does, so the coverage from the deleted `import-drop-zone.test.tsx` carries over.
- The Email cases in `destinations.test.ts` are correct: a Balanced copy still maps back to `chat`, because `chat` comes before `email` in the destination list.

**Batch 4 of 6.** I reviewed the three test files in this part and have one finding, a fix with medium confidence.

**Library file drops (`library-page.test.tsx:80`):** Library no longer handles a file dropped on the window. Only Export does now. The repository's own drop hook says that when nothing handles a drop, Electron loads the dropped file in the window. The main process has no `will-navigate` guard to stop that. So dragging a video onto the Library likely replaces the app with the file. The new test only checks that no import starts, so it passes either way. It also checks synchronously, so it would not catch an import that starts after an `await`. I didn't run anything, and the cause is in `library-page.tsx`, which belongs to another part.

**The other two files:**
- **`export-page.test.tsx`:** its assertions match what `export-page.tsx` does: keyboard handling, reusing an existing copy, the old `/prepare` URLs redirecting, and drops importing and opening Export.
- **`library-detail-page.test.tsx`:** the `/prepare` → `/export` route updates are consistent with `preparePath`, which now builds `/export` URLs.

**Batch 5 of 6.** I found no defects in this part, only two small gaps in sidebar.test.tsx, both rated consider. The test named \"with and without a video\" only checks /export/asset-1. No test covers the in-progress (+1 while exporting) count that the Export badge now includes. The cases from the deleted Prepare test file have equivalents in export-page.test.tsx. Every CSS variable the new stylesheets use is defined in the tokens or base.css, and every class they define is used by its component.

**Batch 6 of 6.** I reviewed part 6: routes, the window-size test, the Export stylesheets, the removed Prepare and Library styles, the backlog doc and index, and the en/es messages. I found two minor comment issues and no defects:

- **Stale comment:** `library-page.module.css:108` still describes the drop strip this change deletes.
- **Out-of-date comment:** the crop comment at `export-stage.module.css:156` says YouTube only, but the crops are drawn for every upload destination.

What I checked:

- **Routes and window size:** the new routes match `router.tsx` and `prepare-path.ts`. The window-size test confirms both `/export` routes stay on the main window size.
- **Translations:** every `export.*` key the new screen uses exists in both en.json and es.json. Nothing in `apps/` still uses the removed translation keys.
- **Styles:** the `data-tone` and `aria-current` values in the stylesheets match what the components render.
- **Backlog doc:** the claims I checked hold: the legacy redirects, `preparePath()` returning Export URLs, the rail badge and when it clears.

<details><summary>What the change connects to (17 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- The Library stops calling useFileDrop; window drops are caught only on Export (`apps/kaipu-record/src/renderer/src/app/router.tsx:69`) — Does anything else (the main process or the shell) stop a file dropped on the Library from making the window navigate to file://? Files that would answer it: `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts`, `apps/kaipu-record/src/main/index.ts`.

**Closed, with the lines they rest on**
- Export of a copy from the Export screen (Enter or the Export button) passes an explicit destination to usePrepareCopy (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252`) — The progress and ready cards use job.destination; for 'email' destinationArg passes the raw id into an ICU select that has no email branch, so the cards say 'your export', as the PR body says. If it fails: When an export is already running, start returns false and shows a toast, and the screen stays as it is. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-119`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-57`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`.
- Change video / Pick from Library navigates to the Export screen for another recording, keeping the picked destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86`) — The new recording opens with the same card selected. useSourceProbe reports a stale probe as loading (use-prepare-copy.ts:64-66), so the new screen never starts with the previous video's probe. If it fails: If the probe fails, the effect shows the shareReadError toast and replaces the route with /export?to=. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-99`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-52`.
- The document-level keydown listener for Enter (export) and Left/Right (move the selection) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — With the VideoPicker dialog open and focus on <body>, Enter starts an export behind it (reported as a finding). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-75`.
- Old /prepare and /prepare/:assetId URLs redirect to Export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — #/prepare/<id>?to=github lands on #/export/<id>?to=github without adding a history entry. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:167-173`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`.
- Library stops registering the window-wide file drop handler (useFileDrop / useImportVideos removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — A file dropped on Library makes Electron navigate the window to the file, replacing the app UI. If it fails: The app UI is lost until reload. There is no guard in main (no will-navigate handler). Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:48-51`, `apps/kaipu-record/src/main/index.ts:400`.
- VideoPicker item click closes the list and calls onPick, which navigates to exportPath(assetId, current destination) (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:86-89`) — Export remounts on the new asset. The ExportScreen key resets state, and the destination is kept through ?to=. If it fails: Synchronous navigation, no async step. Enter on an item is a button press, which isPrimaryEnter ignores. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:152`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:384`.
- RecentExports reads the export runner snapshot and the Library list. A finished row opens /library/:id (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — The running row shows its percentage. Finished rows come from the Library and are filtered to exports (export preset set). If it fails: When the export finishes, the runner goes idle and the row disappears. The new copy appears after the Library refreshes. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26-27`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:59`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:71`, `apps/kaipu-record/src/renderer/src/features/library/types.ts:44`.
- DestinationStage primary / Export again / YouTube preset / Fill-Fit callbacks (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:121-139`) — The export starts in the background and the screen stays. The YouTube toggle re-plans with the new preset. If it fails: Start failures go through the unchanged usePrepareCopy / export runner (runner status 'error'). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:317-320`.
- Rail badge moves from Library to the new Export item and adds 1 while an export runs (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`) — The Export rail item shows the badge with the label export.railBadge ('N copies in progress or ready'). The Library item no longer carries a count. If it fails: The ready-copies store is in memory (ready-copies.ts:14) and the hook re-runs on pathname and copies changes, so a remount re-evaluates correctly. However, being on /export/:assetId announces every u… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462-463`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:101-112`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:59-70`, `packages/i18n/messages/en.json:946`.
- Deletion of Prepare page components (PreparePage, DestinationList, PrepareDropZone) and ImportDropZone test (`apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx:1`) — /prepare and /prepare/:assetId redirect to /export with the query kept. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:167-173`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:16-61`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:1-73`.
- Email added as a destination sharing the 'balanced' preset (`apps/kaipu-record/src/renderer/src/features/prepare/destinations.test.ts:45-51`) — A Balanced copy is labelled as the chat copy. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:37-45`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:64-73`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- Dropping an OS file on the Library window after the Library import door was removed (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — No import happens. Based on the hook's own comment, Electron's default handling of the drop most likely navigates the main window to the file. If it fails: The app UI is most likely replaced by the dropped file, and nothing guards this in main (there is no will-navigate handler). Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:32-34`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`, `apps/kaipu-record/src/main/index.ts:400-403`.
- Dropped video on Export is imported and navigates to /export/:assetId with ?to= kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:460`) — Export opens on the imported video with the selected destination still picked. If it fails: If more than one video is imported, a toast names the rest. If relist() rejects, it does not navigate: the void promise has no catch. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-52`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`.
- Sidebar Export item badge: counts the running export plus finished copies not announced yet; it clears when the user opens Export or the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export item in the rail shows the count and the label from export.railBadge. If it fails: The store lives in memory, so a relaunch clears it, as the store's own comment states. No async calls. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-75`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.
- New routes `/export/:assetId` and `/export`; `/prepare/:assetId` and `/prepare` become legacy redirects (`apps/kaipu-record/src/shared/routes.ts:18`) — Every "prepare a copy" entry point opens the Export screen. The window stays on the main preset, which the updated window-size test pins for /export/abc-123 and /export. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:69-74`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-22`, `apps/kaipu-record/src/shared/window-size.test.ts:21-22`.
- Rail EXPORT entry with a badge; visiting Export or Library announces ready copies (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:53`) — A badge count on the EXPORT rail item. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-120`, `packages/i18n/messages/en.json:946`, `packages/i18n/messages/es.json:946`.
- Removal of the library.import* and prepare.prepareAVideo i18n keys (`packages/i18n/messages/en.json:606`) — None. No missing-key fallbacks. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:94`, `apps/kaipu-record/src/renderer/src/features/prepare/destination-copy.ts:17`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 11 | $0.53 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 15 | $0.50 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 16 | $0.51 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 10 | $0.38 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 17 | $0.47 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 18 | $0.49 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 6 batches · $2.87</sub>

<!-- wachi:review -->

<!-- agent-review sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=fb54d18f-5e98-4e5e-9d63-be6d468b53b7 -->
