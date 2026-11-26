# kaipu-bench-wachi-v3#87 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:03:30Z · commit b12d760

👮 **Wachiman** · 🟠 **2 to fix in this PR** · 2 questions for you · 7 to consider · whole PR at `b12d760`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 7 to consider · ⚪ 0 for your information (9) · 7 Should · 2 Could |
| **Risk** | Medium: top fact `public-contract` at `prepare-path.ts:13`, see Risk facts |
| **Needs a person** | 1 trade-off, in `destinations.ts:71` |
| **Coverage** | 47 of 47 files reviewed, whole pull request |
| **Read first** | `prepare-path.ts`, `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | A file dropped on the Library now navigates the app window to that file |
| 🟠 Fix · Should · 🐛 bug | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | Library no longer stops a dropped file from navigating the window, and this test locks that in |

### To consider (7)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`export-page.tsx:281`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L281) | Enter on a destination card does nothing while no destination is selected |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:212`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L212) | Selected destination is lost after opening an existing copy and coming back |
| 🟡 Consider · Should · 🐛 bug | [`export-stage.tsx:297`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx#L297) | GitHub's size bar is scaled to 10 MB but labelled "Original N MB" |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | "with and without a video" only checks the with-video URL |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:48`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L48) | The "in progress" half of the Export badge is not exercised |
| 🟡 Consider · Should · 🧹 cleanup | [`library-page.module.css:108`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css#L108) | Orphaned comment for the removed \`.importZone\` rule |
| 🟡 Consider · Could · 📝 docs | [`index.mdx:33`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/documentation/src/content/docs/backlog/index.mdx#L33) | The Prepare backlog rows still read 🟢 even though Export replaces that screen |

### Questions for you (2)

- [`destinations.ts:71`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts#L71) · trade-off — Email shares chat's Balanced preset, so a single file shows Ready on both cards and `destinationOfPreset` still answers chat. Someone has to decide whether a seventh card that adds no preset of its own is worth that ambiguity.
- [`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L92) · open question — Probe the picked video before showing the screen; on error, show a toast and redirect to /export: Can probeSource reject or hang, for example over IPC to main, and does it have a timeout of its own? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.

### Risk facts

- `public-contract` · [`prepare-path.ts:13`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts#L13) — Every caller of `preparePath` and `prepareNewPath`, including the recording page, the chips and the sibling branches, now lands on /export instead of /prepare.

<details><summary>What the change connects to (15 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Probe the picked video before showing the screen; on error, show a toast and redirect to /export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — Can probeSource reject or hang, for example over IPC to main, and does it have a timeout of its own? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.

**Closed, with the lines they rest on**

- Enter or Arrow keys anywhere on the Export screen select a destination or start an export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — The selection moves along the row and the stage changes. Enter starts `usePrepareCopy.start`, and the progress card and rail badge show the export. When the copy already exists, Enter opens it instead. If it fails: A second Enter while an export runs is caught by `isVideoExportBusy` and shows a toast. When nothing is selected, Enter on a card is swallowed (reported as a finding). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:262-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-101`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:80-90`.
- A video dropped on the window, or picked with Browse files, is imported and opened on Export with the current destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — Export opens on the new video with the selected card. When more than one file is dropped, a toast names the extra files. If it fails: `relist().then(navigate)` has no catch, so a failed refresh means no navigation, and this path is unchanged from Prepare. useFileDrop catches window drops while the page is mounted, so Electron does… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`.
- Legacy /prepare and /prepare/:assetId URLs redirect to Export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — The Export screen with `?to=` preserved. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`, `apps/kaipu-record/src/shared/routes.ts:17-24`.
- Library stops installing the window-wide file drop handler (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Dropping a file on Library falls back to the Electron default and navigates the window to the file. If it fails: The app UI is replaced by the dropped file; the renderer state and any running export are lost. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:400-403`.
- Export stage primary button starts a copy or opens the existing one; Fill/Fit and YouTube preset toggles (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:120-139`) — copy.start runs the background export runner; the progress shows in RecentExports and the rail badge. If it fails: Runner failures go through the existing usePrepareCopy and export-runner path, which this part does not change. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:309-325`.
- VideoPicker opens a list and closes it on outside mousedown or Escape (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`) — Picking calls onPick, which navigates to exportPath(assetId, current destination). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:86-89`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`.
- Rail badge moves from Library to the new Export item. It counts a running export plus finished copies that have not been announced, and either the Export or th… (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The badge and its badgeLabel (export.railBadge, "# copies in progress or ready") now sit on the Export rail item. The Library item has no badge any more. If it fails: The ready-copies store and the export runner are both in memory. A relaunch clears them. An error status does not count, and the error card shows instead. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:321-327`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462`, `apps/kaipu-record/src/shared/routes.ts:20`, `packages/i18n/messages/en.json:946`.
- Delete the Prepare page, its destination list and its drop zone, and move them under pages/export. (`apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx:1`) — Nothing in apps/kaipu-record/src imports pages/prepare, import-drop-zone or prepare-drop-zone any more, and the pages/prepare directory is gone. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375`, `apps/kaipu-record/src/renderer/src/pages/export/destination-row.tsx:11`.
- A file dragged from the OS and dropped on the Library page (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — On Export the drop zone lights up and the video is imported. On Library nothing intercepts the drop. If it fails: Without preventDefault, Electron's default for a dropped file is to navigate the window to it, and main has no will-navigate guard. The app's page is replaced and renderer state is lost, with no erro… Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-15`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:400`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:414-416`.
- Old /prepare URLs redirect to /export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — The user lands on Export with the destination from ?to=. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`.
- An unreadable recording (probe fails) sends the user to Export with no video (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329`) — A toast, then the empty Export screen. If it fails: The failure is shown to the user through the toast. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`.
- Sidebar Export badge counts the running export plus unseen finished copies, and clears on Export or Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44`) — The rail's Export item shows a numeric badge with the railBadge accessible label. The Library item no longer shows a badge. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:70-82`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/shared/routes.ts:18-20`.
- Deleted Prepare page tests replaced by Export page tests (`apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.test.tsx:1`) — Each removed case has an Export counterpart: Enter handling, busy export, unreadable file, screenshot, Ready copy, unexported edits, unknown ?to=, drop/import flows and legacy Prepare redirects. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:264-372`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374-385`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:419-520`.
- Old `/prepare/:assetId` and `/prepare` URLs redirect to the new Export routes and keep the query (`apps/kaipu-record/src/shared/routes.ts:21-24`) — Bookmarks and sibling-branch callers that still use `/prepare/...?to=` open on the Export screen with the same destination preselected. Because the redirect uses `replace`, Back does not bounce back through the redirect. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`.
- The rail gets an EXPORT entry pointing at `/export`, with the export badge moved there (`packages/i18n/messages/en.json:91`) — An "Export" / "Exportar" rail item with a count badge and an accessible label. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:52-53`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `packages/i18n/messages/en.json:946`, `packages/i18n/messages/es.json:946`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** I found no defects that block the merge in this part; I raised two keyboard/navigation findings at "consider" level. Export reuses the destinations, `usePrepareCopy`, `usePrepareImport` and the probe without changing them, as the PR says, and the legacy /prepare routes redirect with the query kept. Findings: (1) Enter on a destination card is swallowed while nothing is selected, so the card is not selected and nothing exports. (2) The selected destination is not written to the URL, so it resets after opening an existing copy and pressing Back. One contract stays open: the source probe has no timeout, so the screen can show \"Reading…\" forever. That behaviour was already there under Prepare.

**Batch 2 of 6.** I reviewed the five files in this part: the new Export stage, recent-exports and video-picker components, the Library page changes, and the deleted Prepare detail. There is one fix and one suggestion.

- **Fix (`library-page.tsx:53`):** with `useFileDrop` gone from the Library, nothing on that screen handles a dropped file any more. The PR says a drop there "does nothing", but the hook's own doc comment says an unhandled drop makes Electron navigate the window to the file. The main process has no `will-navigate` guard to stop it. So a user who drops an MP4 on the Library, as they could until now, loses the app UI and any running export.
- **Consider (`export-stage.tsx:297`):** GitHub's size bar is scaled to the 10 MB limit, but the label at its left still reads "Original N MB", so the bar suggests the wrong size.

Nothing else in the stage, recent exports or video picker looked wrong: their wiring to `export-page.tsx` matches what the deleted Prepare detail did.

**Batch 3 of 6.** I found nothing to flag in this part.

- **Sidebar:** the badge's logic is the same as before, with two changes. A running export now counts as 1, and opening Export (`/export` or `/export/:assetId`) also announces finished copies.
- **Deleted Prepare files:** nothing still imports them, and their exports now live under `pages/export`.
- **`use-file-drop.test.tsx`:** it carries over the drop-handling cases from the deleted `ImportDropZone` test and matches what `use-file-drop.ts` does.
- **`destinations.test.ts`:** it matches the new email destination. Email shares chat's balanced preset, and `destinationOfPreset("balanced")` still answers "chat".

Outside this part, so not reported as findings:

- The `backgroundCopy.libraryBadge` message is no longer used anywhere.
- The comments in `ready-copies.ts` still describe a badge on the Library rail item and announcing only from the Library page.

**Batch 4 of 6.** I found one problem in this part, in the Library tests. Library no longer mounts any window-level file-drop handling, and the main process has no `will-navigate` guard. So a file dropped on the Library window now hits Electron's default: the window navigates to the file, the app's page is replaced and renderer state is lost. That includes a background export running in the renderer. The new Library test ("does not take a video dropped on the window", `library-page.test.tsx:80`) only checks that nothing is imported. It passes while that happens, so it locks the regression in. I rated this medium confidence because Electron's default drop behaviour comes from the hook's own comment, not from code I could read.

Nothing else in this part needs a change:

- **Export page tests:** they line up with `export-page.tsx` (Enter and arrow-key handling, the legacy Prepare redirect, the probe-error redirect, "Ready" copies opening the existing file).
- **Library detail tests:** only the route changed, from `/prepare` to `/export`.

**Batch 5 of 6.** Part 5 is the sidebar test rewrite, the deleted Prepare test file and the new or changed Export stylesheets; I found no defects in it. Every CSS variable the new stylesheets use exists in `packages/tokens/css/tokens.css` or in the app's `base.css`. The `data-tone` and `data-group` selectors match the values that `destination-row.tsx` and `groupOf` actually produce. The page layout classes (`screen`, `stage`, `stageInner`, `row`) line up with how `export-page.tsx` uses them. Each case from the deleted `prepare-page.test.tsx` has a counterpart in `export-page.test.tsx`. Two optional test points, both in `sidebar.test.tsx`: the test whose name says the Export link is active "with and without a video" only checks the with-video URL, and the running-export part of the badge count is never exercised.

**Batch 6 of 6.** I found no defects in this part (routes, stylesheets, docs, i18n); I have two optional suggestions.

**What I checked**

- **Routes:** `routes.ts` only adds string literals, so the preload rule against value imports in `shared/` still holds.
- **Legacy redirect:** the old `/prepare` routes redirect to Export, keep the query and use `replace`.
- **Window size:** `/export` falls under the default window preset, which matches what `window-size.test.ts` now expects.
- **Stylesheets:** every class and `data-tone` value that `export-stage.tsx` uses exists in the rewritten `export-stage.module.css`.
- **i18n:**
  - The new `export.*` keys and the email destination keys are used by the code, and en and es have the same keys.
  - The deleted `library.import*` and `prepareAVideo` keys are not referenced anywhere any more.
- **Docs:**
  - The new backlog page is in the sidebar config.
  - Its claims about the rail badge and GitHub's 10 MB limit bar match `sidebar.tsx` and `export-stage.tsx`.

**Suggestions**

- `library-page.module.css:108`: the comment for the deleted `.importZone` rule is still there and now reads as if it describes the sticky bar. It can be deleted.
- `backlog/index.mdx:33`: the two Prepare rows still say 🟢 Ready to validate, but this PR deletes that screen. A "superseded by Export" note on them would stop QA from looking for it.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 9 | $0.45 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 12 | $0.44 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 12 | $0.35 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 8 | $0.34 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 14 | $0.40 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 17 | $0.47 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 84 in / 35k out / 1.7M cache read / 285k cache write · Claude subscription: API-equivalent estimate, not a bill · $2.45</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6IjMxNDYyYThiLTU2YjMtNDVmNi05NGQ2LTlhNWJlODA5MTgyZCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6OSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoyLCJjb25zaWRlciI6NywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjksImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=31462a8b-56b3-45f6-94d6-9a5be809182d -->
