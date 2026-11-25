# kaipu-bench-wachi-v3#21 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:56:19Z · commit b12d760

👮 **Wachiman** · ⚠️ **Partial: 19 of 47 files not reviewed** · 3 to fix in this PR · 4 questions for you · 4 to consider · whole PR at `b12d760`

> ⚠️ **Partial review: 28 of 47 files reviewed.** 19 not reviewed because a call ran out of its budget. They are listed under "Files not reviewed". Ask `/wachiman review <paths>` for the rest.

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 3 to fix · 🟡 4 to consider · ⚪ 0 for your information (7) · 5 Should · 2 Could |
| **Risk** | At least medium: 19 files were not reviewed; top fact `public-contract` at `prepare-path.ts:13`, see Risk facts |
| **Needs a person** | 1 pattern others will copy and 1 direction, in `export-page.tsx:277` and `sidebar.tsx:121` |
| **Coverage** | 28 of 47 files reviewed, whole pull request; 19 not reviewed, listed under Files not reviewed. Ask `/wachiman review <paths>` for the rest |
| **Read first** | `prepare-path.ts`, `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx` |

### To fix (3)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | Dropping a file on the Library now falls through to Electron's default: the window navigates to the file |
| 🟠 Fix · Should · 🐛 bug | [`sidebar.tsx:117`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L117) | The badge clears on /export/:assetId, a screen that doesn't show the finished copies |
| 🟠 Fix · Should · 🐛 bug | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | Library no longer handles file drops, so a video dropped there navigates the Electron window to the file |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:375`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L375) | Enter can still start an export while the Change video picker is open |
| 🟡 Consider · Could · 🐛 bug | [`export-drop-zone.tsx:40`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx#L40) | Pick from Library stays enabled while an import is running |
| 🟡 Consider · Should · 📝 docs | [`export-page.tsx:55`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L55) | Comment says \`usePrepareCopy\` is reused unchanged, but it was changed |
| 🟡 Consider · Should · 🐛 bug | [`recent-exports.tsx:65`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx#L65) | An Email export changes from "Email" to "Slack · Discord" in Recent exports once it finishes |

### Questions for you (4)

- [`export-page.tsx:277`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L277) · pattern others will copy — A document-wide keydown listener makes Enter mean "export" wherever focus is not a field, button or link, so a single key press starts an encode. Someone needs to decide whether that is acceptable, or whether it should be scoped to the screen's container.
- [`sidebar.tsx:121`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L121) · direction — The badge now counts the export in progress, so it stays lit while the user watches the progress card on Export. Whether 'in progress' belongs in the same number as 'ready, unseen' is a product call.
- [`apps/kaipu-record/src/renderer/src/app/router.tsx:66`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/app/router.tsx#L66) · open question — The Library no longer takes window drops (PR claim: dropping a file there does nothing): Does main or the window config block navigation on file drop, so that dropping on the Library really does nothing? The search found only setWindowOpenHandler, which does not cover same-window navigation. Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.
- [`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) · open question — Library no longer intercepts files dropped on the window: Does any other layer (session or webPreferences) stop file navigation in the main window? Files that would answer it: `apps/kaipu-record/src/main/index.ts`.

### Risk facts

- `public-contract` · [`prepare-path.ts:13`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts#L13) — preparePath()/prepareNewPath() keep their names but now return /export URLs, so every caller, including sibling branches, lands on the new screen.

<details><summary>What the change connects to (11 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- The Library no longer takes window drops (PR claim: dropping a file there does nothing) (`apps/kaipu-record/src/renderer/src/app/router.tsx:66`) — Does main or the window config block navigation on file drop, so that dropping on the Library really does nothing? The search found only setWindowOpenHandler, which does not cover same-window navigation. Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.
- Library no longer intercepts files dropped on the window (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Does any other layer (session or webPreferences) stop file navigation in the main window? Files that would answer it: `apps/kaipu-record/src/main/index.ts`.

**Closed, with the lines they rest on**

- Enter or ←/→ anywhere on the Export screen exports or moves the selected destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — The selection moves and the stage re-renders. Enter starts `copy.start`, or opens the existing copy through `onOpenExisting`. If it fails: If an export is already running, `usePrepareCopy.start` shows the busy toast and returns false (use-prepare-copy.ts:99-101). Enter with focus on body while the picker dialog is open still exports (re… Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:262-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-101`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:68-75`.
- Old /prepare URLs redirect to /export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — The Export screen opens with `?to=` preselected. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- A file dropped on Export is imported and Export opens on it with the current destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — The ExportScreen remounts (key is preparable.id) with `initialDestination` taken from the URL. If it fails: If `refresh()` rejects, the `.then` never runs and nothing is shown. This is unchanged hook behaviour. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:150-160`.
- The source probe gates the Export screen ("Reading…" until it resolves) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — An error shows the toast "shareReadError" and replaces the URL with /export. If it fails: Nothing bounds the whole wait. If the kaipu-media protocol never answers, the screen stays on "Reading…" with no error. This behaviour is unchanged from Prepare. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`.
- Starting a copy passes the destination explicitly (Email shares chat's preset) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:254`) — The progress and ready cards name the destination. For Email they say "your export", per the PR. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:73-77`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- Enter and the arrow keys while the VideoPicker dialog is open (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45`) — Enter on a picker item clicks that item and does not start an export. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/features/library/tags/tag-chip.tsx:44`.
- Recent exports shows the running job and then the finished copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:35`) — An Email copy changes to Slack · Discord when it finishes. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:59`, `apps/kaipu-record/src/shared/types/library-storage.ts:49`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- Rail EXPORT item carries the badge: 1 while an export runs, plus finished copies not yet announced (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`) — Rail badge number and its aria label export.railBadge ('# copies in progress or ready') on the Export item. If it fails: When an export errors, status becomes 'error' and the +1 disappears. The error card brings itself back (export-status-cards), so the failure stays visible. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121-122`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:70-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462-463`, `packages/i18n/messages/en.json:946`.
- announceReadyCopies() now also runs on any /export URL (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117-119`) — The rail badge clears without the copies being pointed at, on the recording Export screen. If it fails: The user is never told about copies that finished with their ready card hidden or closed while on /export/:assetId. This is silent, but not lost: the Library still outlines them. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:101-115`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:11-36`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:61-62`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:60-64`.
- A file from the OS is dropped on the Library screen (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — With nothing calling preventDefault, Electron's default runs and the window navigates to the dropped file, replacing the app UI. If it fails: Silent: no toast. The app UI is gone until the user reloads or restarts. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`, `apps/kaipu-record/src/main/index.ts:400-403`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80-87`.
- Old /prepare URLs redirect to /export keeping ?to= (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — The Export screen opens with the destination from the URL. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374-387`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** I found nothing that blocks the merge in this part, only three "consider" items:

- **Enter while the picker is open:** the Export screen's Enter handler skips dialogs for the arrow keys but not for Enter. With the Change video picker open and focus dropped to the page body, Enter starts an encode behind it.
- **Pick from Library during an import:** that button stays enabled while an import runs. When the import finishes, the app navigates to the imported video and replaces the one the user just picked.
- **Stale comment:** a doc comment still says `usePrepareCopy` is reused unchanged, but this PR adds a destination override to it.

The /prepare → /export redirect, the destination carried in `?to=` when a dropped file is imported, and the Email destination override all work as the PR describes.

One question is still open and sits in another part's file: the Library no longer intercepts window drops, and I found no guard in the app that stops Electron opening a dropped file in the window. So the PR's claim that dropping a file on the Library "does nothing" is unverified.

**Batch 2 of 6.** Part 2 has two findings. The more serious one: the Library no longer catches files dropped on the window, and the main process has no `will-navigate` guard, so a dropped MP4 is probably loaded into the window in place of the app, not ignored as the PR claims (fix, medium confidence, not run). The second: in Recent exports, an Email export changes to Slack · Discord's logo and name once it finishes, because only the preset is stored (consider). `export-stage.tsx` and `video-picker.tsx` look correct, and so does the keyboard handling around the picker. `destination-detail.tsx` is removed cleanly.

**Batch 3 of 6.** Part 3 covers three deleted Prepare components, the rail badge moving from LIBRARY to the new EXPORT item, the move of the useFileDrop tests, and the destinations test update for Email. Nothing still imports the deleted Prepare components; `isPrimaryEnter` now lives in export-page.tsx. The moved useFileDrop tests keep the same assertions, minus the ImportDropZone-specific ones. The destinations test correctly covers Email sharing the Balanced preset, with `destinationOfPreset("balanced")` still returning chat. One defect: the badge's clear-on-view match uses `end: false`, so it also fires on /export/:assetId, which does not show the finished copies. A copy that finishes while the user stays on Export, now the behaviour after starting an export, is announced at once and drops off the badge. Outside this part: backlog/import-video.md:112 still references the deleted import-drop-zone.tsx.

**Batch 4 of 6.** I found one problem in this part. Library no longer handles file drops, and nothing else on that screen stops Electron's default, so a video dropped on Library now replaces the app window with the file. The new Library test only checks that nothing is imported; it does not check the drop is refused. The Export page tests match what `export-page.tsx` does, and the library-detail test updates match the move from /prepare to /export.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 9 | $0.58 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 12 | $0.57 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 14 | $0.52 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 8 | $0.45 |
| Batch 5 of 6 | 8 | 854 | 2 | 8 file(s) left after a retry | 8 | $0.56 |
| Batch 6 of 6 | 11 | 843 | 4 | 11 file(s) left after a retry | 4 | $0.47 |

</details>

<details><summary>Files not reviewed (19)</summary>

**Because a call ran out of its budget (19)**

- `apps/documentation/src/content/docs/backlog/export-screen.md`
- `apps/documentation/src/content/docs/backlog/index.mdx`
- `apps/kaipu-record/src/renderer/src/features/library/components/import-drop-zone.module.css`
- `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-logo.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/destination-row.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/export-header.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/export-page.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.module.css`
- `apps/kaipu-record/src/renderer/src/pages/export/video-picker.module.css`
- `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css`
- `apps/kaipu-record/src/renderer/src/pages/prepare/destination-list.module.css`
- `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.test.tsx`
- `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx`
- `apps/kaipu-record/src/shared/routes.ts`
- `apps/kaipu-record/src/shared/window-size.test.ts`
- `packages/i18n/messages/en.json`
- `packages/i18n/messages/es.json`

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 54 in / 24k out / 1.0M cache read / 214k cache write · Claude subscription: API-equivalent estimate, not a bill · $3.15</sub>

<!-- wachi:review -->

<!-- wachi:partial sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 state=eyJyIjpbImFwcHMvZG9jdW1lbnRhdGlvbi9zcmMvY29udGVudC9kb2NzL2JhY2tsb2cvZXhwb3J0LXNjcmVlbi5tZCIsImFwcHMvZG9jdW1lbnRhdGlvbi9zcmMvY29udGVudC9kb2NzL2JhY2tsb2cvaW5kZXgubWR4IiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9mZWF0dXJlcy9saWJyYXJ5L2NvbXBvbmVudHMvaW1wb3J0LWRyb3Atem9uZS5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9mZWF0dXJlcy9wcmVwYXJlL2NvbXBvbmVudHMvZGVzdGluYXRpb24tbG9nby5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvZGVzdGluYXRpb24tcm93Lm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9leHBvcnQtZHJvcC16b25lLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9leHBvcnQtaGVhZGVyLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9leHBvcnQtcGFnZS5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvZXhwb3J0LXN0YWdlLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9yZWNlbnQtZXhwb3J0cy5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvdmlkZW8tcGlja2VyLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2xpYnJhcnkvbGlicmFyeS1wYWdlLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL3ByZXBhcmUvZGVzdGluYXRpb24tbGlzdC5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9wcmVwYXJlL3ByZXBhcmUtcGFnZS50ZXN0LnRzeCIsImFwcHMva2FpcHUtcmVjb3JkL3NyYy9yZW5kZXJlci9zcmMvc2hlbGwvc2lkZWJhci50ZXN0LnRzeCIsImFwcHMva2FpcHUtcmVjb3JkL3NyYy9zaGFyZWQvcm91dGVzLnRzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3NoYXJlZC93aW5kb3ctc2l6ZS50ZXN0LnRzIiwicGFja2FnZXMvaTE4bi9tZXNzYWdlcy9lbi5qc29uIiwicGFja2FnZXMvaTE4bi9tZXNzYWdlcy9lcy5qc29uIl0sInQiOltdfQ -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6IjZhNTBkNjllLTdkODAtNGM2Mi04ZTUxLTA4Mzk1NzljMWFiNSIsInN0YXR1cyI6InBhcnRpYWwiLCJyZWFzb24iOm51bGwsImZpbmRpbmdzIjp7InRvdGFsIjo3LCJieV9zZXZlcml0eSI6eyJibG9ja2VyIjowLCJmaXgiOjMsImNvbnNpZGVyIjo0LCJpbmZvIjowfSwiYnlfcGxhY2VtZW50Ijp7ImlubGluZSI6NywiYm9keSI6MCwib3V0c2lkZV9kaWZmIjowfSwidW50aHJlYWRlZF9ibG9ja2luZyI6MH19 -->

<!-- wachi:attempt id=6a50d69e-7d80-4c62-8e51-0839579c1ab5 -->
