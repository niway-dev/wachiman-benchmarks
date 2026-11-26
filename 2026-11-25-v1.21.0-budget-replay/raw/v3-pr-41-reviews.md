# kaipu-bench-wachi-v3#41 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:56:55Z · commit b12d760

👮 **Wachiman** · 🟠 **2 to fix in this PR** · 3 questions for you · 5 to consider · whole PR at `b12d760`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 5 to consider · ⚪ 0 for your information (7) · 4 Should · 3 Could |
| **Risk** | Medium: top fact `public-contract` at `prepare-path.ts:13`, see Risk facts |
| **Needs a person** | 1 trade-off and 1 direction, in `export-page.tsx:277` and `sidebar.tsx:121` |
| **Coverage** | 47 of 47 files reviewed, whole pull request |
| **Read first** | `prepare-path.ts`, `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | A file dropped on the Library now hits Chromium's default and can navigate the app window away |
| 🟠 Fix · Should · 🧪 tests | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | Library drop test passes even though Electron opens the dropped file in the main window |

### To consider (5)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`export-drop-zone.tsx:40`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx#L40) | "Pick from Library" stays enabled while an import runs |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:375`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L375) | Enter-to-export does not skip dialogs, but the arrow handler does |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | "with and without a video" only renders /export/asset-1 |
| 🟡 Consider · Could · 🐛 bug | [`export-drop-zone.module.css:10`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css#L10) | The no-video Export screen has nothing that scrolls in a short window |
| 🟡 Consider · Should · 🧹 cleanup | [`library-page.module.css:108`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css#L108) | Orphaned comment for the removed drop strip |

### Questions for you (3)

- [`export-page.tsx:277`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L277) · trade-off — A document-wide Enter handler starts an encode from almost any focus position. That is fast for the main flow, but someone must decide whether it is acceptable that a stray Enter starts a background export.
- [`sidebar.tsx:121`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L121) · direction — The Export badge now also counts an export in progress, including one started from the Editor, and it shows even while the user is on the Export page that displays it. Someone has to decide whether the Export item should carry editor-started work, and whether the Library item should lose its badge altogether.
- [`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:460`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx#L460) · open question — Video dropped on Export is imported, then the Library is re-listed and Export opens on it: Does a rejected refresh() after import leave the user with no feedback? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts`.

### Risk facts

- `public-contract` · [`prepare-path.ts:13`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts#L13) — `preparePath` keeps its name but now returns `/export/...` URLs, which every existing "Prepare for…" entry point and sibling branch picks up.

<details><summary>What the change connects to (11 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Video dropped on Export is imported, then the Library is re-listed and Export opens on it (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:460`) — Does a rejected refresh() after import leave the user with no feedback? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts`.

**Closed, with the lines they rest on**

- Old /prepare and /prepare/:assetId URLs redirect to Export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — The Export screen opens with ?to= preselected. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/app/router.tsx:69-74`.
- A video dropped on Export or browsed from the drop zone is imported, then Export opens on it with the current destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — The import state shows in the drop-zone title; the screen then navigates to the new video. If it fails: If refresh() rejects, `relist().then(navigate)` never navigates and the rejection goes unhandled (unchanged hook). A Library pick made during an import is overridden when the import finishes (see fin… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:36-54`.
- Enter exports and the arrow keys move the selection, through a document-level keydown listener (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — The export starts in the background (a busy toast shows if another export is already running) or the existing copy opens. If it fails: Enter is not filtered for dialogs (see finding). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:262-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-101`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:69-75`.
- Email added as a destination that shares the balanced preset (`apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:43`) — Progress and ready cards name the email destination through their ICU select's fallback branch; Recent exports and the master-copies panel label finished balanced copies as chat. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-104`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65`.
- Library stops listening for window file drops (useFileDrop removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Dropping a file on the Library falls through to Chromium's default handling. If it fails: No will-navigate guard in main, so a dropped file can navigate the main window to file:// and the app UI is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:25`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:49`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`.
- VideoPicker opens a list; picking navigates to Export for that video, keeping the destination (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:86`) — Export reopens on the picked video with the same destination selected. If it fails: Synchronous, so no async failure. Enter inside the dialog is on a button, which isPrimaryEnter excludes, and arrows inside role=dialog are ignored by destinationStep. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:152`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:384`.
- DestinationStage primary / Export again buttons (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:121`) — The export starts in the background; the screen stays. If it fails: Handled by the unchanged usePrepareCopy / export runner. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`.
- The rail badge moves from Library to the new Export item. It counts the running export plus finished copies nobody has been shown yet, and it clears when /expo… (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export rail item shows the count with the label export.railBadge ("# copies in progress or ready"). If it fails: The store lives in memory, so a relaunch clears it, as before. When an export fails, the status becomes "error" and the in-progress 1 drops out. Copies that finish while the user is on /export are an… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462-463`, `apps/kaipu-record/src/shared/routes.ts:17-24`, `packages/i18n/messages/en.json:946`.
- File dropped on the window while the Library page is shown (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — jsdom has no navigation. In Electron the default is that the main window navigates to the dropped file. If it fails: The renderer navigates away from the app and session state is lost. Main has no will-navigate guard, only setWindowOpenHandler. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`, `apps/kaipu-record/src/main/index.ts:400-403`.
- The Export rail item carries the badge: one for a copy being made plus finished copies the user has not seen. Opening Export or the Library clears it. (`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44`) — The rail shows a badge count with the label "N copy/copies in progress or ready" on the Export link. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `packages/i18n/messages/en.json:946`.
- Legacy /prepare/:assetId and /prepare URLs are kept in ROUTES and routed to a redirect component instead of the Prepare page (`apps/kaipu-record/src/shared/routes.ts:22`) — Old deep links land on Export. The window keeps the main preset for both old and new paths, as window-size.test.ts checks. Evidence: `apps/kaipu-record/src/renderer/src/app/router.tsx:69-74`, `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/shared/window-size.test.ts:17-31`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** I reviewed the 13 files in part 1 and found two issues, both minor ("consider"); nothing blocks the merge. First, "Pick from Library" stays clickable while an import is running, so a finished import can pull the screen away from the video the user just picked. Second, the Enter-to-export handler does not ignore dialogs the way the arrow-key handler does, so Enter can start an export behind an open dialog. The rest checks out. The old /prepare URLs redirect to Export with the query kept. `preparePath` now builds Export URLs. `destinationOfPreset("balanced")` still returns chat. The email destination reaches the progress cards through the new `destination` field. The keyboard listener is removed when the screen unmounts.

**Batch 2 of 6.** The Export stage, recent exports and video picker look correct. The picker's Escape and outside-click listeners are added and removed together, and the page-level Enter and arrow handlers leave the picker's dialog and the stage's own radio groups alone. One concern, at medium confidence: with `useFileDrop` gone from the Library, nothing suppresses Chromium's default for dropped files, and I found no `will-navigate` guard in main. A video dropped on the Library could therefore navigate the window away instead of doing nothing as the PR states.

**Batch 3 of 6.** Part 3 has no findings. Prepare's page, destination list and drop zone are deleted, and nothing in apps/kaipu-record/src still imports them. isPrimaryEnter now lives in pages/export/export-page.tsx, and the pages/prepare directory is gone entirely. In the sidebar, the badge moves to the new Export item and adds 1 while an export runs. It cannot count a finishing export twice, because the runner sets the status back to idle before it calls noteFinishedCopy. The badge clears on /export, /export/:assetId and /library. The new use-file-drop test keeps the hook coverage from the deleted import-drop-zone test. The destinations test now uses a Set so that email can share chat's "balanced" preset, and it pins destinationOfPreset("balanced") to chat.

**Batch 4 of 6.** I found one problem in this part, and it is in a test. The new Library test "does not take a video dropped on the window" (`library-page.test.tsx:80`) only checks that no import happens. It does not check that the drop is blocked, and with this PR it isn't. Only Export now mounts `useFileDrop`, and the main process has no `will-navigate` guard. So a file dropped on the Library is likely to make Electron navigate the main window to that file, replacing the app. I couldn't confirm the navigation in Electron itself.

The rest of this part looks right:

- The Export page tests match `export-page.tsx`: they cover the keyboard rules, the legacy `/prepare` redirect, the drop and import flow, and reopening a copy that already exists.
- The `library-detail-page.test.tsx` changes just follow the route rename from `/prepare` to `/export`.

**Batch 5 of 6.** I found no defects in this part, only two suggestions. The sidebar tests match the new Export badge in `sidebar.tsx` and the `railBadge` message in `en.json`. Every CSS custom property the new stylesheets use is defined in the tokens or in `base.css`, and the class names match the components that use them. The two suggestions: (1) the sidebar test named \"with and without a video\" only checks the URL with a video; (2) the no-video Export screen lost its scroll box, so in a short window the drop zone may be clipped.

**Batch 6 of 6.** Part 6 (routes, the window-size test, the Export stylesheets, the removed Library and Prepare CSS, the backlog docs and i18n) has no defects. I found one optional cleanup and nothing to fix.

- **routes.ts** adds `export` and `exportNew` as plain literals, with no workspace value import. `/prepare` and `/prepare/:assetId` now go to `LegacyPrepareRedirect`.
- **Stylesheets:** every class the new export TSX uses is defined in its module, including the `data-tone` values `fits`, `over`, `lighter` and `not-lighter`.
- **Stage scrolling:** `.stage` itself has no overflow, but its container in `export-page.module.css` has `overflow-y: auto`. So the comment's claim that the stage scrolls on its own holds.
- **i18n:** no code still references the removed `library.import*` / `importDropTitle`, `importDropHint`, `importDropActive` keys or `prepare.prepareAVideo`. The new keys match between `en.json` and `es.json`.
- **Finding (consider):** an orphaned comment for the deleted drop strip is left in `library-page.module.css:108`, above the toolbar's comment.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 8 | $0.52 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 8 | $0.54 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 11 | $0.46 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 11 | $0.49 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 13 | $0.50 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 11 | $0.51 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 70 in / 29k out / 1.3M cache read / 272k cache write · Claude subscription: API-equivalent estimate, not a bill · $3.01</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6IjJlYjgyOWNmLTJlNGMtNDY0ZS05MzdkLWUxODY2MTlkZjQ5YyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoyLCJjb25zaWRlciI6NSwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjcsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=2eb829cf-2e4c-464e-937d-e186619df49c -->
