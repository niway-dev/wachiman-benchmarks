# kaipu-bench-wachi-v3#46 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:57:30Z · commit b12d760

👮 **Wachiman** · 🟠 **2 to fix in this PR** · 3 questions for you · 5 to consider · whole PR at `b12d760`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 5 to consider · ⚪ 0 for your information (7) · 6 Should · 1 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 47 of 47 files reviewed, whole pull request |
| **Read first** | `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx`, `destination-list.tsx` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | Dropping a file on the Library now loads that file in place of the app |
| 🟠 Fix · Should · 🧪 tests | [`library-page.test.tsx:85`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L85) | Test of a drop on the Library ignores whether the window navigates to the file |

### To consider (5)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`export-page.tsx:98`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L98) | An unreadable file drops the destination picked on screen |
| 🟡 Consider · Could · 🐛 bug | [`recent-exports.tsx:65`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx#L65) | A finished Email copy is listed under Slack · Discord in Recent exports |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | "Active with and without a video" only checks the with-a-video case |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:44`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L44) | The badge's in-progress count is never tested |
| 🟡 Consider · Should · 🧹 cleanup | [`library-page.module.css:108`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css#L108) | Stale comment for the removed "Drop a video here" strip |

### Questions for you (3)

- [`apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts#L55) · open question — Drop a file on the Library (it no longer mounts a window drop handler): Does anything else (another main-process guard, a preload handler) stop the default file-drop navigation on screens without useFileDrop? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`, `apps/kaipu-record/src/preload/index.ts`.
- [`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L92) · open question — Probe the picked recording before showing the Export screen: Can probeSource reject or hang, or does it always resolve with an unusable result on failure? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.
- [`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) · open question — A file dropped on the window while the Library (or any non-Export screen) is open: Does the app shell or main process stop file navigation some other way that a text search for will-navigate/dragover listeners misses (e.g. a preload listener or a webPreferences setting)? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/preload/index.ts`, `apps/kaipu-record/src/renderer/src/shell/app-shell.tsx`.

<details><summary>What the change connects to (10 closed, 3 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Drop a file on the Library (it no longer mounts a window drop handler) (`apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`) — Does anything else (another main-process guard, a preload handler) stop the default file-drop navigation on screens without useFileDrop? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`, `apps/kaipu-record/src/preload/index.ts`.
- Probe the picked recording before showing the Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — Can probeSource reject or hang, or does it always resolve with an unusable result on failure? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.
- A file dropped on the window while the Library (or any non-Export screen) is open (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Does the app shell or main process stop file navigation some other way that a text search for will-navigate/dragover listeners misses (e.g. a preload listener or a webPreferences setting)? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/preload/index.ts`, `apps/kaipu-record/src/renderer/src/shell/app-shell.tsx`.

**Closed, with the lines they rest on**

- Enter or arrow keys anywhere on the Export screen (document keydown listener) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — Enter starts the copy, or opens the existing one. A second Enter while an export runs hits the isVideoExportBusy toast. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:82-90`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-101`.
- Email destination passed to usePrepareCopy over chat's balanced preset (`apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`) — Status cards fall back to the ICU 'other' branch for email, as the PR says. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:37-46`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:104`.
- Legacy /prepare URLs redirect to /export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — #/prepare/<id>?to=github becomes #/export/<id>?to=github, and replace keeps Back clean. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-14`.
- Library no longer mounts useFileDrop (window drop handling removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Dropping a file on the Library navigates the window to the file instead of doing nothing. If it fails: Chromium's default drop navigation replaces the app UI. No will-navigate guard exists in main. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/main/index.ts:400-403`.
- DestinationStage renders the upload size, framing and size bar from the plan and calls onPrimary/onExportAgain (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:59`) — The stage re-renders from the plan that export-page.tsx recomputes on every render. If it fails: copy.start is fire-and-forget into the export runner, the same as before. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:250-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:309-325`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:129-160`.
- VideoPicker opens a list; closes on document mousedown outside or Escape (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45`) — Picking an item closes the list and navigates through onPick (exportPath). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`.
- The rail badge moves from Library to the new Export item and adds 1 while an export is running; opening /export or /export/:id announces (clears) the finished… (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — Badge plus an aria label (export.railBadge, present in en/es) on the Export rail item; the Library item no longer carries a badge. If it fails: When the export fails, status becomes 'error' and running drops to 0. The error card is the visible signal and the badge does not stick. The state is in memory and re-derived on every render; the eff… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:50-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462-463`, `apps/kaipu-record/src/shared/routes.ts:17-24`, `packages/i18n/messages/en.json:946`.
- Legacy /prepare URLs redirect to /export, keeping the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — The Export screen opens with the destination from ?to=. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`.
- Rail Export entry shows a badge (running export + unseen finished copies), cleared on Export or Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The badge number and the badgeLabel tExport('railBadge') appear on the Export rail item only; the Library item no longer carries one (sidebar.test.tsx:50-51). Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.
- New routes `/export/:assetId` and `/export`; `/prepare` routes kept as legacy redirects (`apps/kaipu-record/src/shared/routes.ts:18`) — The window-size test now expects `/export/abc-123` and `ROUTES.exportNew` to get the default preset. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/shared/window-size.test.ts:21-22`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** Part 1 (the router, the prepare helpers and the new Export page, header, drop zone and row) reads correctly overall. These hold up: the legacy redirect, Email's preset sharing (destinationOfPreset still returns chat), stale-probe handling on Change video, and the Enter guards (picker items are buttons). One consider: a failed probe returns to /export without the destination picked on screen. Two open contracts. First, probeSource has no catch or timeout, so a rejection would leave "Reading…" on screen. Second, the Library no longer mounts useFileDrop, and the main process has no will-navigate guard. The PR's claim that a drop on the Library "does nothing" looks doubtful, since Chromium's default navigates to the dropped file; this is in library-page.tsx, another part.

**Batch 2 of 6.** Part 2 of 6 (export stage, recent exports, video picker, the Library page and the deleted destination detail): one fix and one consider.

- **Fix, file drop on the Library:** The Library no longer mounts the window-wide drop handler. The main process has no `will-navigate` guard, so dropping a file on the Library now makes Electron load that file in place of the app. The UI and any export in progress are lost. The PR body says such a drop "does nothing", which is wrong.
- **Consider, Recent exports naming:** A finished Email copy is relabelled "Slack · Discord" in Recent exports.

I found nothing to flag in the export stage, the video picker or the deleted file.

**Batch 3 of 6.** Part 3: no findings. The sidebar moves the badge from Library to the new Export item. It counts the running export plus finished copies not yet announced, and opening Export or the Library clears the finished ones. The runner records a finished copy at the moment the ready card appears, and that copy is left out of the count, so the switch from running to ready does not count it twice. Nothing in the app still imports the deleted Prepare components (DestinationList, PrepareDropZone, PreparePage); isPrimaryEnter and usePrepareImport now live in export-page.tsx. The new use-file-drop test keeps the hook's coverage that the deleted drop-zone test had. The destinations test matches the new email destination, which shares chat's preset. Stale doc mentions of the deleted files (import-video.md, prepare-drop-zone.md) and the Library-rail wording in ready-copies.ts sit in other parts' files, so they are not reported here.

**Batch 4 of 6.** Part 4 covers three test files. The Export page tests line up with `export-page.tsx`: destinations, keyboard handling, the legacy `/prepare` redirect, drop/import, and an unreadable probe. The library-detail test updates are mechanical `/prepare` → `/export` route changes. One finding, at medium confidence: the new Library test for a dropped file never checks that the drop is default-prevented. With the Library's drop handler gone and no `will-navigate` guard in main, a file dropped outside Export would load into the window. This test would not catch that.

**Batch 5 of 6.** I found no defects in this part, only two optional test gaps (severity "consider") in `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx`.

**Sidebar tests.**

- They match the new behaviour: the Export entry sits right after Editor, the badge moved off Library, and it clears on Export or Library.
- The test "is active on Export with and without a video" only checks `/export/asset-1`, never the bare `/export` route the rail link points to.
- The badge's +1 while an export is running is never tested, though the badge label says "in progress or ready".

**Deleted `prepare-page.test.tsx`.** Its cases are replaced in `export-page.test.tsx`: destinations, YouTube 1440p/4K, Fill or Fit, GitHub's 10 MB limit, one export at a time, unreadable file, Ready copies, the edits warning, old `/prepare` URLs, and the drop and import cases. Two kinds of case are gone with nothing in their place:

- the "Back to recording" button;
- the "Prepare another video" footer, including dropping a file on it.

Neither of those controls exists on the Export screen.

**Stylesheets.** Every CSS variable the new and changed stylesheets use is defined in `packages/tokens/css/tokens.css` or `apps/kaipu-record/src/renderer/src/assets/base.css`. The classes match what the Export components use. The deleted `import-drop-zone.module.css` went together with its component, and the new `email` logo colour matches the new Email destination.

**Batch 6 of 6.** I reviewed all 11 files in part 6 and found one small issue. `library-page.module.css:108` still has the comment for the "Drop a video here" strip whose CSS rule this PR removes; that line can go.

What checked out:

- **Routes.** `routes.ts` adds string literals only, so it introduces no value imports into `shared/`.
- **Removed strings.** The Library keys deleted from `en.json` and `es.json` (`importVideo`, `importing`, `importDropTitle`, `importDropHint`, `importDropActive`) and `prepareAVideo` are no longer used anywhere under `apps/`.
- **New stylesheets.** The classes in the three new or rewritten stylesheets match the ones the components use. The CSS rules for the new size-bar tones (`fits`, `over`) match the values `export-stage.tsx` sets.
- **Translations.** The new `export` strings in English and Spanish have the same keys and placeholders.

I did not check the backlog doc's claims about other parts' code against that code: the Email "Ready" behaviour and the `githubPlans().free` limit.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 13 | $0.61 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 12 | $0.56 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 11 | $0.46 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 6 | $0.40 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 10 | $0.51 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 8 | $0.40 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 68 in / 27k out / 1.3M cache read / 268k cache write · Claude subscription: API-equivalent estimate, not a bill · $2.94</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6Ijc1M2RmNjliLWU5YTktNDdhYS1hZmZiLTFmN2I5OTllYTk0ZSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoyLCJjb25zaWRlciI6NSwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjcsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=753df69b-e9a9-47aa-affb-1f7b999ea94e -->
