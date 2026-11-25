# kaipu-bench-wachi-v3#31 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:00:06Z · commit b12d760

👮 **Wachiman** · ⚠️ **Partial: 11 of 47 files not reviewed** · 2 to fix in this PR · 2 questions for you · 3 to consider · whole PR at `b12d760`

> ⚠️ **Partial review: 36 of 47 files reviewed.** 11 not reviewed because a call ran out of its budget. They are listed under "Files not reviewed". Ask `/wachiman review <paths>` for the rest.

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 3 to consider · ⚪ 0 for your information (5) · 3 Should · 2 Could |
| **Risk** | At least low: no risk facts in the files read; 11 files were not reviewed |
| **Needs a person** | 1 direction, in `library-page.test.tsx:73` |
| **Coverage** | 36 of 47 files reviewed, whole pull request; 11 not reviewed, listed under Files not reviewed. Ask `/wachiman review <paths>` for the rest |
| **Read first** | `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx`, `destination-list.tsx` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | A file dropped on the Library now navigates the app window away |
| 🟠 Fix · Should · 🐛 bug | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | A file dropped on Library is now left to Electron's default, which loads the file into the app window |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`export-drop-zone.tsx:40`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx#L40) | "Pick from Library" stays enabled while an import runs |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:375`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L375) | Enter-to-export skips dialogs less carefully than the arrow keys do |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | "with and without a video" only renders the with-video URL |

### Questions for you (2)

- [`library-page.test.tsx:73`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L73) · direction — Importing by drag-and-drop now works only on the Export screen. A person has to decide whether the Library (or the whole app shell) should still take dropped videos or just ignore them safely.
- [`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:94-99`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L94) · open question — A probe of the picked video fails, or the video is dropped onto Export: Does probeSource have its own timeout? If not, a hung probe leaves Export on 'Reading…' for good Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`. ⚠️ A citation did not resolve in the head.

<details><summary>What the change connects to (12 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- A probe of the picked video fails, or the video is dropped onto Export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:94-99`) — Does probeSource have its own timeout? If not, a hung probe leaves Export on 'Reading…' for good. Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`. ⚠️ A citation did not resolve in the head.

**Closed, with the lines they rest on**

- Enter on the Export screen starts a copy, or opens the copy that already exists (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`) — The progress card names the destination. For Email the ICU select falls back to 'your export', because destinationArg passes 'email' and the select has no email branch. If it fails: A second Enter while an export runs shows the busy toast. A held key is ignored through event.repeat. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-131`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-57`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:376`.
- Old /prepare URLs redirect to /export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`) — The same screen opens on the same video with the same destination. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- Library stops handling window file drops (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — The platform default runs: the window loads the dropped file and the app UI is gone. If it fails: Leaves the app in an unrecoverable view with no visible error. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-51`, `apps/kaipu-record/src/main/index.ts:537-541`.
- Recent exports row for a running job (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:35`) — A progress row with its percentage above at most two finished copies. If it fails: No async call here; if the job fails, the runner status leaves 'exporting' and the row disappears. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:59-71`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- VideoPicker list with outside-click and Escape close (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45`) — The list closes on Escape or a click outside; picking a video navigates via onPick. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`.
- DestinationStage renders the plan and the primary action (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:59`) — Stage card, then the Export or Open existing button. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:183-228`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:250-266`.
- The rail's Export item shows a badge: 1 while an export is running, plus the finished copies that have not been announced yet. The Library item no longer has a… (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export rail item gets a numeric badge, labelled with export.railBadge. If it fails: When an export fails, status is "error", so running is 0 and the badge drops. The progress card brings the error back, so the failure is not silent. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462-463`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:70-75`.
- Opening /export or /export/:assetId now calls announceReadyCopies, as opening the Library already did. (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117-119`) — The finished-copies part of the badge clears while Export is open. The running count does not clear. Evidence: `apps/kaipu-record/src/shared/routes.ts:18-20`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-64`.
- File dropped on the Library window after the Library drop zone was removed (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Chromium's default drop handling navigates the main window to the dropped file's file:// URL, replacing the app UI. If it fails: Silent: no toast and no error. The main process has no will-navigate guard to stop the navigation. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:49-51`, `apps/kaipu-record/src/main/index.ts:400-403`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80-87`.
- Unreadable probe redirects to /export with a toast (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329`) — The toast says "Couldn't read this recording to prepare a file." and the empty Export screen opens. If it fails: The error is shown to the user; the replace keeps history clean. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`.
- Legacy /prepare URLs redirect to /export, keeping the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — Old links open the Export screen with the same destination. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`.
- The sidebar Export entry shows a badge for the copy being made plus finished copies nobody has seen yet; opening Export or the Library clears it (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export rail item gets a count badge, and its accessible label comes from export.railBadge. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** I found no blockers or fixes in part 1, only two "consider" items. The new routes and redirects, the Email destination, `usePrepareCopy`'s `destination` override and the Export screen all do what the PR body says.

1. **Import race (`export-drop-zone.tsx:40`).** "Pick from Library" stays enabled during an import, unlike "Browse files…". A video picked mid-import is replaced when the import finishes and navigates to the imported file.
2. **Enter in dialogs (`export-page.tsx:375`).** `isPrimaryEnter` doesn't skip `[role='dialog']`, though `destinationStep` does. It's harmless today because the picker's items are buttons.

One question stays open: I couldn't confirm whether `probeSource` has its own timeout. If it doesn't, a probe that never answers leaves the screen on "Reading…" for good; `probe-source.ts` would settle it.

**Batch 2 of 6.** I found one problem in this part. `library-page.tsx` no longer calls `useFileDrop`, and nothing else in the app stops a file drop: the renderer has no other drop handler and `src/main/index.ts` has no `will-navigate` guard. So a file dropped on the Library loads in the app window and replaces the whole UI. That contradicts the PR's claim that the drop "does nothing".

`export-stage.tsx`, `recent-exports.tsx` and `video-picker.tsx` match the plan data from `destinations.ts` and the export runner's job shape; I found nothing to flag in them, or in the deleted `destination-detail.tsx`.

**Batch 3 of 6.** No findings in part 3.

- **Deleted Prepare files:** destination-list, prepare-drop-zone, prepare-page and the ImportDropZone test are gone. Nothing in the repository still imports them, and `isPrimaryEnter` now lives in export-page.tsx.
- **use-file-drop.test.tsx:** it keeps the window-level drop coverage that the old ImportDropZone test had, minus the cases about the deleted component, and it matches the hook in use-file-drop.ts.
- **destinations.test.ts:** it correctly reflects that email shares chat's "balanced" preset and that `destinationOfPreset("balanced")` stays "chat", as destinations.ts:69-71 and :102-105 show.
- **sidebar.tsx:** the old Library badge is now the Export badge. It counts 1 for a running export plus finished copies not yet announced, and opening Export or the Library announces them. The runner sets status to idle before `noteFinishedCopy`, so the same export is never counted twice.

**Batch 4 of 6.** I found one problem in this part, rated "fix". With the Library's drop zone gone, nothing on the Library prevents the default drop anymore, and the main process has no navigation guard (no `will-navigate` handler). So a video dropped on the Library is opened by Electron in place of the app UI, with no error. The new Library test passes anyway because it only checks that no import happens, not that the drop was prevented. The Export page tests match the code I read in `export-page.tsx`: the probe-error redirect, the legacy `/prepare` redirect and the Enter/arrow key handling. The changes to `library-detail-page.test.tsx` only swap the Prepare routes for the Export ones.

**Batch 5 of 6.** I found one minor test issue in this part and nothing else to flag.

- **Sidebar test (`sidebar.test.tsx:39`):** the test named "is active on Export with and without a video" only renders `/export/asset-1`. The `/export` case is never checked.
- **Sidebar badge logic:** I checked the tests against `sidebar.tsx`. Moving the badge from Library to Export matches what the code does: opening Export or the Library clears it, and opening a copy's page forgets that copy.
- **Stylesheets:** they are layout and styling only. The `--tone-*` variables they use are defined in `base.css`. I did not trace where the other variables come from; they probably come from the shared UI tokens.
- **`prepare-page.test.tsx` and `import-drop-zone.module.css`:** both are deleted outright. They go together with the deleted Prepare page and import drop-zone components in other parts of this pull request.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 9 | $0.54 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 14 | $0.61 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 10 | $0.43 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 7 | $0.42 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 4 | $0.30 |
| Batch 6 of 6 | 11 | 843 | 4 | 11 file(s) left after a retry | 8 | $0.59 |

</details>

<details><summary>Files not reviewed (11)</summary>

**Because a call ran out of its budget (11)**

- `apps/documentation/src/content/docs/backlog/export-screen.md`
- `apps/documentation/src/content/docs/backlog/index.mdx`
- `apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/video-picker.module.css`
- `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css`
- `apps/kaipu-record/src/renderer/src/pages/prepare/destination-list.module.css`
- `apps/kaipu-record/src/shared/routes.ts`
- `apps/kaipu-record/src/shared/window-size.test.ts`
- `packages/i18n/messages/en.json`
- `packages/i18n/messages/es.json`

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 62 in / 22k out / 1.1M cache read / 245k cache write · Claude subscription: API-equivalent estimate, not a bill · $2.89</sub>

<!-- wachi:review -->

<!-- wachi:partial sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 state=eyJyIjpbImFwcHMvZG9jdW1lbnRhdGlvbi9zcmMvY29udGVudC9kb2NzL2JhY2tsb2cvZXhwb3J0LXNjcmVlbi5tZCIsImFwcHMvZG9jdW1lbnRhdGlvbi9zcmMvY29udGVudC9kb2NzL2JhY2tsb2cvaW5kZXgubWR4IiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvZXhwb3J0LXN0YWdlLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9yZWNlbnQtZXhwb3J0cy5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvdmlkZW8tcGlja2VyLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2xpYnJhcnkvbGlicmFyeS1wYWdlLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL3ByZXBhcmUvZGVzdGluYXRpb24tbGlzdC5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3NoYXJlZC9yb3V0ZXMudHMiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvc2hhcmVkL3dpbmRvdy1zaXplLnRlc3QudHMiLCJwYWNrYWdlcy9pMThuL21lc3NhZ2VzL2VuLmpzb24iLCJwYWNrYWdlcy9pMThuL21lc3NhZ2VzL2VzLmpzb24iXSwidCI6W119 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6IjAwY2MyODEwLTc3MTgtNDg1My1hMGVlLTIwMmJkZGZmOWQ1MSIsInN0YXR1cyI6InBhcnRpYWwiLCJyZWFzb24iOm51bGwsImZpbmRpbmdzIjp7InRvdGFsIjo1LCJieV9zZXZlcml0eSI6eyJibG9ja2VyIjowLCJmaXgiOjIsImNvbnNpZGVyIjozLCJpbmZvIjowfSwiYnlfcGxhY2VtZW50Ijp7ImlubGluZSI6NSwiYm9keSI6MCwib3V0c2lkZV9kaWZmIjowfSwidW50aHJlYWRlZF9ibG9ja2luZyI6MH19 -->

<!-- wachi:attempt id=00cc2810-7718-4853-a0ee-202bddff9d51 -->
