# kaipu-bench-wachi-v3#79 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:04:16Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

10 finding(s): 3 to fix, 7 to consider; 10 on their lines. Reply in a comment's thread to answer it.

**Risk map:** low — no risk facts in this change.
**Read first:** `apps/kaipu-record/src/renderer/src/pages/prepare/destination-detail.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx`, `apps/kaipu-record/src/renderer/src/pages/prepare/destination-list.tsx`.

### Summary

**Batch 1 of 6.** Part 1 has one defect worth fixing. The Export page switches to a full Loading state on every library re-list, for example the cloud catalog refresh that starts when the page mounts, or a copy being saved. That remounts ExportScreen and silently resets the destination, YouTube resolution and framing the user picked, so Enter can export the wrong copy. There is also a minor inconsistency in the destination kept after a probe-error redirect. The routes, the legacy redirect, the Email destination wiring and the docs entry look correct.

**Batch 2 of 6.** I reviewed the five files in part 2: the stage, recent exports, the video picker, the Library page edits and the deleted Prepare detail.

1. **Fix: dropping a file on the Library is no longer safe** (`library-page.tsx:53`). The PR says such a drop "does nothing". It did only because `useFileDrop` blocked the drop. `useFileDrop`'s own comment says that otherwise Electron navigates the window to the dropped file. I found no `will-navigate` guard in `main/index.ts`, so now the file replaces the app's window contents, with no message. Confidence is medium because I didn't run the app to confirm Electron's default.
2. **Consider: screen readers miss the size bar's verdict** (`export-stage.tsx:311`). The bar is marked as an image, so only its label is read: the two sizes. "Fits the 10 MB limit", "over the limit" and "N% lighter" are never announced.

The new message keys I checked against `en.json` all exist. The shapes `CopyPlan` gives (`scale`, `direction`, `underGithubFreeLimit`) match what the stage uses, including the `data-tone` styles. The picker's Escape and outside-click handling doesn't clash with the screen's Enter and arrow-key handling.

**Batch 3 of 6.** I found nothing to flag in this part (3 of 6).

- **Prepare page removal:** the old Prepare page, its destination list and its drop zone are deleted, and nothing in the source tree still imports them. `isPrimaryEnter` now lives in `export-page.tsx`.
- **Drop-hook test:** the test moved to `use-file-drop.test.tsx` and still covers the hook's real behaviour: enter/leave depth counting, accepting a file drop, ignoring drags with no files, and removing its listeners on unmount.
- **Destinations test:** `destinations.test.ts` matches `destinations.ts`. Email shares chat's `balanced` preset, and `destinationOfPreset("balanced")` still answers chat.
- **Rail badge:** the sidebar badge moves from Library to Export and now adds 1 while an export is running. Opening `/export` or `/library` still clears the finished copies, and its label string (`export.railBadge`) exists in `en.json`.

**Batch 4 of 6.** I read all three test files in part 4 and found one problem worth fixing: the new Library test passes even if a dropped video replaces the app window.

- **Library drop test (fix, medium confidence):** after this change, nothing on Library cancels a file drop. Only Export mounts the window drop handler (`useFileDrop`), and the main process has no navigation guard. In Electron, a file dropped on a page that does not cancel the event opens in the window instead of the app. The test at `library-page.test.tsx:80` only checks that no import was called, so it does not catch this. Confidence is medium because Electron's default behaviour is not in the repository's code; the absence of any guard is.
- **Unreadable-file test (consider):** it checks the path `/export` but not that `?to=youtube` is kept, though the code keeps it.
- **"Keep full quality keeps the full size" (consider):** the name promises the full size, but the test only checks the preset id.

The `library-detail-page.test.tsx` changes just switch the expected route from `/prepare` to `/export`, and look correct.

**Batch 5 of 6.** I found no defects in part 5, only two optional suggestions:

- **Sidebar test name overpromises.** The test "is active on Export with and without a video" only renders `/export/asset-1`, so the no-video route is never checked.
- **Focus ring may be clipped.** On the destination row, the keyboard focus outline reaches 4px out, but the scroll box only leaves 3px of room, so its outer pixel on the edge cards is probably cut off.

What I checked:

- **Stylesheets:** every CSS variable the new files use is defined, in `packages/tokens/css/tokens.css` or `assets/base.css`. Every class the new Export components use exists in their stylesheets. The `data-group` values match the destination groups `send-more` and `keep-light`.
- **Deleted files:** the removed `prepare-page.test.tsx` and `import-drop-zone.module.css` belong to deleted components.
- **Sidebar test:** it matches how `sidebar.tsx` now handles the badge: it moved from Library to the Export item, and opening either Export or the Library clears it.

**Batch 6 of 6.** Part 6 covers route constants, stylesheets, the backlog doc and i18n messages, and it is mostly clean. routes.ts only adds string literals (no workspace value import), so it follows the shared/preload rule. Every class export-stage.tsx uses is still defined, and the renamed `data-tone` values match the component. The new `export` i18n keys I spot-checked are used (railBadge, keepPicture, exportActionFull, openExisting, framingTitle), and en.json and es.json have the same keys. The removed library keys have no remaining callers. The backlog doc's statement that opening Export or the Library clears finished copies matches `useExportBadge`. One cleanup nit: library-page.module.css still has the comment for the deleted import strip. Not checked here: the legacy /prepare → /export redirect and whether it keeps the query live in router.tsx, which is in another part, so that contract is left open.

<details><summary>What the change connects to (10 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Source probe for the opened recording (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — Can probeSource reject, or does it always resolve to null on failure? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.
- New route constants `export` (/export/:assetId) and `exportNew` (/export); `prepare`/`prepareNew` kept as legacy redirects (`apps/kaipu-record/src/shared/routes.ts:17-24`) — Does the redirect in router.tsx (another part) keep `location.search` for both legacy routes? Files that would answer it: `apps/kaipu-record/src/renderer/src/app/router.tsx`.

**Closed, with the lines they rest on**
- Library re-list while the Export screen is open (libraryChanged broadcast) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117`) — The screen flashes to Loading; the selected destination, YouTube preset and framing go back to their initial values. If it fails: The user's choice is lost silently; Enter can then export the wrong preset. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:41-42`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:130-133`, `apps/kaipu-record/src/main/library/index.ts:73-75`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:212-221`.
- Start a copy for the selected destination, with Email passed explicitly (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:254`) — The progress and ready status cards; the screen stays open. If it fails: While another export runs, the busy toast appears and nothing starts; a throw in onSaved is captured. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-131`.
- Window-wide file drop on Export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — Export opens on the imported video; any extra files are named in a toast. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`.
- Library stops registering window-wide file drop handling (useFileDrop/useImportVideos removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — A file dropped on the Library is no longer imported. Electron's default navigation to the file takes over and replaces the app UI. If it fails: The renderer navigates away from the app with no error and no way back. Any renderer-side export state is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-47`, `apps/kaipu-record/src/main/index.ts:400`.
- VideoPicker opens a list; a document mousedown outside it or Escape closes it; picking a video navigates to Export for that video (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`) — The list closes. onPick calls openVideo, which navigates to exportPath with the current destination. If it fails: Arrow keys inside the dialog are ignored by destinationStep. Enter on an item is a button press, so isPrimaryEnter does not fire an export. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:384`.
- RecentExports reads useExportRunner for the running job and lists the newest exported copies; clicking a row navigates to /library/:assetId (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — The running row shows the job's percentage; finished rows show size, title and Ready. If it fails: An Email copy shows as Slack · Discord because destinationOfPreset("balanced") returns chat. The PR documents this. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:112`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65`.
- Rail Export item badge: running export (1) plus finished copies not announced; visiting /export or /library announces them (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The badge and its aria label (export.railBadge, 'in progress or ready') move from the Library item to the Export item. If it fails: In-memory store; after a relaunch nothing is pending, as before. When an export fails, status becomes 'error' and the running count drops to 0. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/shared/routes.ts:20`, `packages/i18n/messages/en.json:946`.
- A file dropped on Library is no longer imported (the drop strip was removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — With no listener cancelling the event, Electron's default navigates the window to the dropped file; this test does not assert against it. If it fails: The window shows the file in place of the app. Main has no will-navigate guard to stop it. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-51`, `apps/kaipu-record/src/main/index.ts:400`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:414-416`.
- An unreadable probe sends the user to /export, keeping ?to= (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329`) — A toast reading "Couldn't read this recording", then the empty Export screen. If it fails: The test does not check that the query is kept. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`.
- The Export rail item shows a badge: the copy being made now plus finished copies not yet shown; it clears when Export or the Library opens (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The badge count and its accessible label (export.railBadge) on the Export rail item; the tests at sidebar.test.tsx:44-79 cover it. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 12 | $0.63 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 10 | $0.54 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 12 | $0.44 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 6 | $0.41 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 10 | $0.44 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 10 | $0.46 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 70 in / 30k out / 1.3M cache read / 257k cache write · Claude subscription: API-equivalent estimate, not a bill · $2.91</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=6c3b3aab-2901-43d8-9d0c-86271e745333 -->
