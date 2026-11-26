# kaipu-bench-wachi-v3#106 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:36:40Z · commit b12d760

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 3 questions for you · 10 to consider · whole PR at `b12d760`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 10 to consider · ⚪ 0 for your information (11) · 5 Should · 6 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Needs a person** | 1 direction, in `library-page.tsx:53` |
| **Coverage** | 47 of 47 files reviewed, whole pull request |
| **Read first** | `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx`, `destination-list.tsx` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | A video dropped on the Library window is no longer caught, so Electron navigates to the file |

<details><summary>To consider (10)</summary>

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`destinations.ts:71`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts#L71) | Email copies are stored as "balanced" and read back as Chat everywhere else |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:212`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L212) | The destination picked on screen is not written to the URL |
| 🟡 Consider · Could · 🐛 bug | [`export-stage.tsx:201`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx#L201) | \`role="radio"\` buttons answer no arrow keys, though \`destinationStep\` assumes they do |
| 🟡 Consider · Could · 🐛 bug | [`recent-exports.tsx:65`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx#L65) | A finished Email copy is listed as "Slack · Discord" |
| 🟡 Consider · Could · ❓ question | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | Library now leaves a dropped file to the platform default, and the test only pins that nothing is imported |
| 🟡 Consider · Should · 🧪 tests | [`export-page.test.tsx:285`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx#L285) | Enter test claims "from the page or a card" but only fires on a card |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | Test name says "with and without a video" but only covers the with-video route |
| 🟡 Consider · Should · 🧹 cleanup | [`library-page.module.css:108`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css#L108) | Orphaned comment for the removed drop strip |
| 🟡 Consider · Should · 🧹 cleanup | [`en.json:881`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/packages/i18n/messages/en.json#L881) | New \`prepare.lineEmail\`, \`sayEmail\` and \`whyEmail\` keys are never read |
| 🟡 Consider · Could · 📝 docs | [`index.mdx:33`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/documentation/src/content/docs/backlog/index.mdx#L33) | Prepare backlog rows and docs still describe the removed Prepare screen |

</details>

### Questions for you (3)

- [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) · direction — Moving all video import to Export removes it from the Library, where users used to drop and import videos. Whether the Library should keep a drop-to-Export redirect or an import entry point is a product decision.
- [`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L95) · open question — Unreadable or unusable source file sends the user from /export/:id back to /export: Can `probeSource` reject instead of returning null? If so, `useSourceProbe` leaves the screen on "reading" with no error shown. Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.
- [`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) · open question — Library no longer takes file drops (the import strip, the Prepare button and the Import button are removed): Is there a global drop or navigation guard that is not found by searching `will-navigate` and `useFileDrop`? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

<details><summary>What the change connects to (13 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Unreadable or unusable source file sends the user from /export/:id back to /export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95`) — Can `probeSource` reject instead of returning null? If so, `useSourceProbe` leaves the screen on "reading" with no error shown. Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.
- Library no longer takes file drops (the import strip, the Prepare button and the Import button are removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Is there a global drop or navigation guard that is not found by searching `will-navigate` and `useFileDrop`? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

**Closed, with the lines they rest on**

- Global Enter and ArrowLeft/ArrowRight handler on the Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — Enter exports, or opens the existing copy when one exists. Arrows move the selection along the row and focus follows the selected card. If it fails: `isPrimaryEnter` does not exclude `role='dialog'`, though `destinationStep` does. Enter pressed on a non-button inside the picker panel would export. The panel holds only buttons, so this has no effe… Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:61-75`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-102`.
- A video dropped on, or browsed from, the Export screen is imported and Export opens on it (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — The drop zone lights up while dragging. After the import the screen opens on the new video with the chosen destination carried in `?to=`. If it fails: If the user leaves before the refresh finishes, the navigate still fires. That behaviour was already there. Several files imported: the first opens and the rest are named in a toast. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-57`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:21-58`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:76-88`.
- /prepare and /prepare/:assetId redirect to Export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — Old URLs land on Export with the destination kept. Back does not return to the dead URL. If it fails: None found. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`, `apps/kaipu-record/src/shared/window-size.ts:82-88`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-22`.
- Reading the recording's metadata before the stage shows (`useSourceProbe` → `probeSource`) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — The user sees "Reading…" while the probe runs. An unreadable file gives a toast and the picker screen. If it fails: If a media read stalls without rejecting, nothing bounds the wait: "Reading…" stays on screen. The sidebar still works, so the user can leave. No finding is raised, because this is existing probe beh… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:94-99`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:144-146`.
- New `destination` field on `usePrepareCopy.start`, used for Email (`apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`) — The progress and ready cards say Email rather than Chat for an Email export. If it fails: After the copy lands in the library it is identified from its preset alone, so it reads as Chat. See the first finding. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-128`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-260`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- Dropping a video on the Library window (the Library's drop zone and window-level drop were removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Imports now happen only on Export. A drop on the Library goes to the platform default. If it fails: No drop guard in the renderer and no will-navigate in main/index.ts, so Electron's default navigates the window to the dropped file. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-15`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-47`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`, `apps/kaipu-record/src/main/index.ts:400-403`.
- Primary Export button and Enter run `copy.start` for the picked destination, or open the existing copy (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:120`) — Progress shows in the Recent exports row on `/export` and in the status cards. Leaving the screen does not stop the export. If it fails: If another export is running, `start` returns false with a toast and the screen stays as it is. Enter on a card or on a radio exports; Enter on any other button or field is ignored. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-131`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`.
- Recent exports strip shows the running job and the three newest exported copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:26`) — The progress percent comes from `runner.fraction`. The label of an Email copy comes out as chat, because `destinationOfPreset` cannot tell them apart. If it fails: The strip is empty when there is no running job and no finished copy: it shows the empty text, with no error state. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:59-99`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:101-107`.
- VideoPicker ("Change video" and "Pick from Library") opens a list of the Library's originals (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:32`) — The page re-probes the new file and `ExportScreen` remounts through its `key`. If it fails: Escape or a click outside closes the list. Focus is not moved into the `role=dialog` panel or returned to the trigger. The list has only masters, and an empty Library shows `pickerEmpty`. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:12-16`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`.
- Export rail item shows a badge: copy running now plus finished copies not yet announced; opening /export or /library announces (clears) them (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — Badge on Export reads 'N copies in progress or ready'. It disappears after opening Export or Library. The Library page chip and outline still follow unseenCopyIds, which only markCopySeen clears. If it fails: No async call. If the store never changes, the badge stays at 0 or at the running count. The running count depends only on runner status 'exporting' (export-runner.ts:26), so it drops back when the s… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:49-80`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:32-76`.
- useFileDrop is now consumed only through usePrepareImport on the Export page; the Library page drop zone and its test are removed (`apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:20`) — Window-level drop handling exists only while Export is mounted, so a file dropped elsewhere gets the Electron default (navigate to the file). If it fails: The hook registers window listeners in an effect and removes them on unmount, so a remount re-registers them and nothing stale survives. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:16-61`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:4`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`.
- A video dropped on Export (or picked with Browse files) is imported, then Export opens on it with the selected destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — The new video opens in Export with `?to=` kept. Non-videos get an "Only videos can be imported" toast. If it fails: `run()` catches a rejection from `importVideoFiles` and reports it through `reportError`, and `busy` resets in `finally`. The failure is visible and the page stays usable. `useFileDrop` calls `preven… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:76-115`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-47`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:73-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:460-525`.
- Sidebar Export entry with a badge that counts the running export plus unseen finished copies, cleared on opening Export or the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — A number badge on the Export rail item with the accessible name `export.railBadge` ("N copies in progress or ready"). That key exists in en.json:946. If it fails: No new async call here. A copy that finishes while Export or the Library is open never badges, which the tests cover. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`, `packages/i18n/messages/en.json:946`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** Part 1 replaces Prepare with the Export screen and adds Email as a seventh destination over chat's preset. Nothing here blocks the merge. I found two things to consider. First, Email copies are stored as the `balanced` preset, so the Library and the recent-exports list show them as Chat, and Email and Chat share \"Ready\" and the existing-copy shortcut. Second, the destination picked on screen is not written to the URL, so Back can lose it. I checked the legacy `/prepare` redirects, drop-and-import, the keyboard handler, the probe failure path and the window-size table, and found no defect in them. I did not read the part-2 test file. The probe has no timeout, but that behaviour is unchanged from before.

**Batch 2 of 6.** The new Export stage, picker and recent-exports strip fit together, and every message key and every called symbol exists. Removing `useFileDrop` from the Library leaves a dropped file there unhandled, and I found no guard in `main/index.ts`, so Electron's default is to navigate the window to the file. Two lesser points: the custom `role=radio` controls answer no arrow keys, and a finished Email copy shows as \"Slack · Discord\" in Recent exports.

**Batch 3 of 6.** Nothing in this part needs changing. The Prepare screen files are deleted and Export replaces them. No references to the removed symbols remain (`DEFAULT_DESTINATION`, `isPrimaryEnter` in the old page, `ImportDropZone`, `useLibraryBadge`). The sidebar badge now sits on Export and adds the running copy. `destinations.test.ts` correctly handles email sharing chat's preset, and `use-file-drop.test.tsx` ports the old hook coverage. One thing I noticed outside this part: `apps/documentation/src/content/docs/backlog/import-video.md:112` still names the deleted `import-drop-zone.tsx`.

**Batch 4 of 6.** The three test files are consistent with the code they exercise. I checked these against the page code:

- **Enter and arrow handling:** the keyboard tests match `isPrimaryEnter` and `destinationStep`.
- **"Ready" cards:** the copy fixture's fingerprint `whole#q30-24fps-kfi10` matches the `whole` + balanced encoding.
- **Strings:** the asserted strings match `en.json`.
- **Routes:** the `/prepare` to `/export` redirect matches `LegacyPrepareRedirect`.
- **Drop and import:** the import/drop flow matches `usePrepareImport`.

Two findings, both "consider":

- **Library drop:** after Library lost its drop handling, a file dropped there may navigate the Electron window to the file. I found no guard in `main`, and the new test asserts only that nothing is imported.
- **Enter test:** the "from the page or a card" Enter test only fires on a card.

One contract is left open: `useSourceProbe` has no `.catch`, so a rejecting `probeSource` would leave the screen on "reading".

**Batch 5 of 6.** This part is safe to merge, with one small test-naming nit. The sidebar test, which moves the badge to Export, matches `sidebar.tsx`, and the new i18n key exists. The new CSS modules define every class their components use, and every token they reference exists in the repo. The deletions of the Prepare page test and the import drop zone styles belong to the page-level changes reviewed in the other parts. Outside this part's files, `apps/documentation/src/content/docs/backlog/import-video.md:112` still names the deleted `import-drop-zone.tsx`.

**Batch 6 of 6.** This part (routes, CSS, docs, i18n) is mostly consistent. The CSS classes in `export-stage.module.css` match `export-stage.tsx`, and every `export.*` key the export page reads exists in both locales. The three findings are all low severity. A leftover comment in `library-page.module.css` describes the removed drop strip. Several i18n keys are now dead, including the new Email `line`, `say` and `why` keys. The Prepare backlog docs and index rows don't say Export replaced them. The new `export-screen.md` doc matches the code I read. I did not review the `destination-row` and `export-page` CSS, which belong to other parts.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 19 | $0.43 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 23 | $0.46 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 17 | $0.30 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 21 | $0.44 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 16 | $0.26 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 17 | $0.31 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 100 in / 51k out / 2.5M cache read / 363k cache write · Claude subscription: API-equivalent estimate, not a bill · $2.21</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6ImNlMjM1MGRkLThjMmMtNDQxMi1hNjM1LTdlYTI5N2JmYjY4YiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MTEsImJ5X3NldmVyaXR5Ijp7ImJsb2NrZXIiOjAsImZpeCI6MSwiY29uc2lkZXIiOjEwLCJpbmZvIjowfSwiYnlfcGxhY2VtZW50Ijp7ImlubGluZSI6MTEsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=ce2350dd-8c2c-4412-a635-7ea297bfb68b -->
