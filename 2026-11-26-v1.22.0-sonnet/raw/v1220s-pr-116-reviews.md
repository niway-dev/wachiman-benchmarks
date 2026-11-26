# kaipu-bench-wachi-v3#116 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:09:00Z · commit b12d760

👮 **Wachiman** · 🟠 **3 to fix in this PR** · 4 questions for you · 12 to consider · whole PR at `b12d760`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 3 to fix · 🟡 12 to consider · ⚪ 0 for your information (15) · 7 Should · 8 Could |
| **Risk** | Medium: top fact `public-contract` at `routes.ts:22`, see Risk facts |
| **Needs a person** | 2 directions and 1 trade-off, in `prepare-path.ts:12`, `destinations.ts:71` and `library-page.tsx:53` |
| **Coverage** | 47 of 47 files reviewed, whole pull request |
| **Read first** | `routes.ts`, `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx` |

### To fix (3)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`router.tsx:66`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/app/router.tsx#L66) | Library no longer handles window file drops, so a video dropped there makes Electron navigate to the file |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | A file dropped on the Library now navigates the window to that file |
| 🟠 Fix · Should · 🐛 bug | [`use-file-drop.test.tsx:6`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx#L6) | Library page no longer catches dropped files, so a video dropped there navigates the window away |

<details><summary>To consider (12)</summary>

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:98`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L98) | Unreadable-file redirect drops the destination picked on screen |
| 🟡 Consider · Should · ⚡ perf | [`export-page.tsx:156`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L156) | \`?? []\` creates a new array on every render and defeats the \`useMemo\` on \`exports\` |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:359`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L359) | Arrow keys move the destination from anywhere outside inputs, radio groups and dialogs, including a focused sidebar link |
| 🟡 Consider · Could · 🐛 bug | [`recent-exports.tsx:65`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx#L65) | Finished Email exports show up as Chat in Recent exports |
| 🟡 Consider · Could · 📝 docs | [`sidebar.tsx:105`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L105) | Comment says Export 'points at the copies', but the Export page does not use the unseen-copy state |
| 🟡 Consider · Could · 🐛 bug | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | A video dropped on Library is no longer handled, and the test asserts only that nothing is imported |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | Test says "with and without a video" but only renders /export/asset-1 |
| 🟡 Consider · Could · 🧪 tests | [`sidebar.test.tsx:44`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L44) | Badge's "in progress" half is not covered |
| 🟡 Consider · Should · 🧹 cleanup | [`en.json:884`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/packages/i18n/messages/en.json#L884) | New prepare.lineEmail/sayEmail/whyEmail keys have no reader; most of the prepare namespace is now dead |
| 🟡 Consider · Should · 🧹 cleanup | [`library-page.module.css:108`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css#L108) | Orphan comment left where \`.importZone\` was removed |
| 🟡 Consider · Could · 📝 docs | [`index.mdx:34`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/documentation/src/content/docs/backlog/index.mdx#L34) | Prepare backlog rows still present the removed Prepare screens as live |
| 🟡 Consider · Could · 🐛 bug | [`video-picker.module.css:54`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/video-picker.module.css#L54) | Keyboard focus on a picker item looks the same as hover |

</details>

### Questions for you (4)

- [`prepare-path.ts:12`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts#L12) · direction — preparePath and prepareNewPath keep their Prepare names but now return Export URLs, with exportPath and exportNewPath as aliases. This keeps merges with the sibling branches conflict-free but leaves a mismatched name that later code will copy. Someone should decide whether to rename the helpers now or after the siblings land.
- [`destinations.ts:71`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts#L71) · trade-off — Email is a seventh destination over chat's Balanced preset. Both cards show Ready for the same file, destinationOfPreset('balanced') still answers chat, and the progress and ready cards say 'your export' for Email. Someone should decide whether that is acceptable or whether Email needs its own preset or ICU branch.
- [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) · direction — The Library gives up its drop strip and its import buttons, so Export becomes the only way in for outside videos. A person has to decide whether the Library should still guard against file drops, or whether the guard belongs at the app level.
- [`apps/kaipu-record/src/renderer/src/app/router.tsx:66`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/app/router.tsx#L66) · open question — Dropping a video file on the Library (or any non-Export page) after the Library's window-wide drop handler was removed: Does the main window block navigation to dropped files elsewhere (webPreferences, a navigation guard)? I found none in apps/kaipu-record/src. Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

### Risk facts

- `public-contract` · [`routes.ts:22`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/shared/routes.ts#L22) — The `/prepare/:assetId` and `/prepare` paths are demoted to legacy redirect sources; the new Export routes replace them, so any stored link or caller must go through the redirect in router.tsx (a different part).

<details><summary>What the change connects to (12 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Dropping a video file on the Library (or any non-Export page) after the Library's window-wide drop handler was removed (`apps/kaipu-record/src/renderer/src/app/router.tsx:66`) — Does the main window block navigation to dropped files elsewhere (webPreferences, a navigation guard)? I found none in apps/kaipu-record/src. Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

**Closed, with the lines they rest on**

- Email destination started as an export (copy.start with destination: plan.destination) (`apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`) — The progress and ready cards use an ICU select with no email branch, so they fall to 'other' and say 'your export'. DestinationLogo has the Mail icon. The PR body documents this. If it fails: None. destinationArg returns job.destination, which is still in the ICU select's other branch. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-67`, `packages/i18n/messages/en.json:1474`, `packages/i18n/messages/en.json:1480`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- Document-level Enter/arrow handler on the Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — Enter on a card or radio exports. While another export runs, start() shows the busy toast and returns false. If it fails: The listener is removed on unmount. The ref holds the latest handlers, so there is no stale closure. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:273-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:68-107`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-102`.
- Legacy /prepare and /prepare/:assetId redirect to Export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — Old URLs and Back land on Export, not on a dead route. Back does not return to the redirecting entry. If it fails: None found. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:167-173`, `apps/kaipu-record/src/renderer/src/app/router.tsx:72-74`, `apps/kaipu-record/src/shared/routes.ts:21-24`.
- Probe of the selected recording and import of dropped or browsed files (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — An error shows a toast and the empty Export screen. A rejected import calls reportError and the drop zone becomes usable again. relist().then(navigate) in usePrepareImport has no catch, but that file is unchanged. If it fails: Not silent. No operation here has a timeout, but nothing polls or retries either, so there is no unbounded wait. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:76-92`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-52`.
- Library page stops taking window-wide file drops and import buttons (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Dropping a file on the Library lets Electron's default run, which is navigating the window to the file. If it fails: The window is navigated away from the app and needs a reload. Nothing is shown to the user. main/index.ts has no will-navigate guard. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:10-12`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-47`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`, `apps/kaipu-record/src/main/index.ts:379-400`.
- Recent exports shows the running export and the newest finished copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — The percentage and the progress bar update with the runner. When the export ends, the running row disappears and the finished copy appears once the Library list has the new item. If it fails: When the export errors, the runner returns to status "error" and the row disappears with no message here. The error is reported elsewhere (status cards). Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26-27`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:314`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:418`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`.
- Video picker lists the Library's originals and opens the chosen one (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:12-16`) — The list shows originals only. Copies and screenshots are hidden, though a copy can still be opened by URL. If it fails: None found. The panel closes on Escape and on an outside mousedown, and the listeners are removed when it closes. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:22-26`, `apps/kaipu-record/src/renderer/src/features/library/lineage.ts:65-67`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`.
- Rail badge moves from the Library item to a new Export item and now also counts the export running right now (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export rail item shows a count with the label `export.railBadge`; the Library item no longer shows one. If it fails: No async call is added. The running count comes from the runner snapshot, so it drops to 0 when the export finishes or errors, and a finished copy then counts until Export or Library is opened. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-122`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-75`, `packages/i18n/messages/en.json:946`.
- Window-wide file drop moves from the Library to Export only (`apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:6`) — A file dropped on the Library falls to the Electron default instead of being imported. If it fails: Nothing in the renderer or main intercepts the drop on the Library, so the window can navigate to the dropped file. This is silent and the app state is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-15`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:48-51`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`, `apps/kaipu-record/src/main/index.ts:400`.
- A video dropped on the window while Export is mounted is imported and Export opens on it (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — Export reopens on the first imported video, keeping the destination. The tests cover multi-file drops (a toast names the rest) and non-video files (toast, no import). If it fails: Pages other than Export have no drop guard. A drop there falls to Electron's default of navigating the window to the file, and the main process has no `will-navigate` guard. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-57`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-47`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80-87`.
- Enter and the arrow keys act on the whole document while ExportScreen is mounted (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — Enter starts the copy or opens the existing one. The arrows move the selection. The tests cover fields, modifiers, buttons and the 1440p / 4K radiogroup. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:275-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:264-306`.
- Remove the library.importVideo, importing, importDropTitle, importDropHint and importDropActive messages (`packages/i18n/messages/en.json:606`) — The Library no longer shows the drop strip or import buttons; the Export drop zone uses the new export.drop* keys. If it fails: A missing key would throw at type-check time, because keys are typed from Messages. No stale reader remains. Evidence: `packages/i18n/messages/en.json:606`, `packages/i18n/messages/es.json:606`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:65`, `apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:36`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** Part 1 is mostly sound. The Email destination, the legacy redirect, the keyboard handling and the probe and import failure paths all check out. The one real problem is that the Library loses its window-wide drop handler, and nothing else guards file drops. That likely makes a video dropped on the Library navigate Electron to the file, which contradicts the PR's \"does nothing\" claim. I did not run Electron to confirm. Two smaller issues: the unreadable-file redirect ignores the destination picked on screen, and `?? []` defeats the `useMemo` on `exports`. I also note that arrow keys act from a focused sidebar link.

**Batch 2 of 6.** The new Export stage, the recent-exports strip and the video picker read correctly. The i18n keys they use exist in `en.json`, and the size and tone values match the CSS selectors. One real regression: the Library no longer calls `useFileDrop`, so a file dropped on it now makes Electron navigate the window to that file. The main process has no `will-navigate` guard, and the PR's own step 12 claims the drop \"does nothing\". A smaller point: finished Email exports appear as Chat in Recent exports, because `destinationOfPreset(\"balanced\")` returns `chat`.

**Batch 3 of 6.** Part 3 mostly deletes the Prepare page and the Library drop zone, moves the rail badge to a new Export item, and adds Email as a destination. I read the sidebar, `destinations.ts`, `routes.ts`, `ready-copies.ts` and `use-file-drop.ts`, and found two issues. One fix: the Library no longer has a window drop handler, so a video dropped there makes Electron navigate to the file, and I found no `will-navigate` handler. One consider: the `useExportBadge` doc comment says Export 'points at the copies', but the Export page does not read the unseen-copy state; `backgroundCopy.libraryBadge` is now unused. The new `use-file-drop.test.tsx` and the `destinations.test.ts` updates match the code.

**Batch 4 of 6.** The Export page tests match the implementation: the messages and routes they assert exist in `en.json` and `export-page.tsx`. The updated library-detail test only changes `/prepare` to `/export`. One concern, on the Library test: Library no longer takes dropped files, and the main process has no `will-navigate` guard. A video dropped on Library probably navigates the window to the raw file. The new Library test only asserts that nothing was imported, so it would pass either way.

**Batch 5 of 6.** I found nothing that blocks this part, only two test-coverage gaps in `sidebar.test.tsx`. The stylesheets use only CSS variables that exist (`tokens.css`, `base.css`). Every class they define is used by `destination-row.tsx`, `export-header.tsx`, `export-drop-zone.tsx` and `export-page.tsx`. The comment about seven destination cards matches the seven ids in `DESTINATION_IDS`. The deleted `prepare-page.test.tsx` has matching tests in `export-page.test.tsx`, and nothing in source still imports the deleted `import-drop-zone` files. The two gaps:

- **Active-state test:** it is named "with and without a video" but only renders `/export/asset-1`.
- **Badge test:** nothing covers the in-progress half of the Export badge (the exporting-runner term).

The documentation file `backlog/import-video.md` still points to the deleted `import-drop-zone.tsx`. That file belongs to another part of the review, so I did not report it.

**Batch 6 of 6.** The CSS, routes, tests, docs and messages in this part are consistent with the Export code I read. Every `export.*` key that export-stage, recent-exports, video-picker and the other export components reference exists in both en.json and es.json, and every class in the three export stylesheets is used. The `data-tone` values match `SizeDirection` and the GitHub limit tones. The findings are all minor and none blocks the merge. The Prepare i18n keys, and the new Email `line`/`say`/`why` keys, are dead because only `DESTINATION_COPY.name` has a reader. An orphan comment is left in library-page.module.css. The two Prepare backlog docs and their index rows are not marked superseded. The picker items have a weak keyboard-focus cue.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 19 | $0.34 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 20 | $0.34 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 16 | $0.22 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 14 | $0.21 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 17 | $0.21 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 28 | $0.39 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 104 in / 51k out / 2.6M cache read / 374k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.71</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6ImQyOWZkMGE3LTRkNGEtNDU5Yy04YTgxLTRjZGE1ZGNhZTI5MCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MTUsImJ5X3NldmVyaXR5Ijp7ImJsb2NrZXIiOjAsImZpeCI6MywiY29uc2lkZXIiOjEyLCJpbmZvIjowfSwiYnlfcGxhY2VtZW50Ijp7ImlubGluZSI6MTUsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=d29fd0a7-4d4a-459c-8a81-4cda5dcae290 -->
