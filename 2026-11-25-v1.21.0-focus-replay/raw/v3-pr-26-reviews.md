# kaipu-bench-wachi-v3#26 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:59:38Z · commit b12d760

👮 **Wachiman** · ⚠️ **Partial: 19 of 47 files not reviewed** · 2 to fix in this PR · 2 questions for you · 5 to consider · whole PR at `b12d760`

> ⚠️ **Partial review: 28 of 47 files reviewed.** 19 not reviewed because a call ran out of its budget. They are listed under "Files not reviewed". Ask `/wachiman review <paths>` for the rest.

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 5 to consider · ⚪ 0 for your information (7) · 4 Should · 3 Could |
| **Risk** | At least medium: 19 files were not reviewed; top fact `public-contract` at `prepare-path.ts:13`, see Risk facts |
| **Needs a person** | 2 directions, in `export-page.tsx:277` and `sidebar.tsx:121` |
| **Coverage** | 28 of 47 files reviewed, whole pull request; 19 not reviewed, listed under Files not reviewed. Ask `/wachiman review <paths>` for the rest |
| **Read first** | `prepare-path.ts`, `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | A file dropped on the Library now navigates the app window to that file, not "nothing" |
| 🟠 Fix · Should · 🐛 bug | [`library-page.test.tsx:85`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L85) | Dropping a file on the Library now hands the drop to Electron, which opens the file in place of the app, and the new test accepts that |

### To consider (5)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`export-page.tsx:98`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L98) | The unreadable-file redirect drops the destination picked on screen |
| 🟡 Consider · Could · 🧹 cleanup | [`export-page.tsx:112`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L112) | Library detail paths are hard-coded and not encoded, unlike the Export paths |
| 🟡 Consider · Could · 🐛 bug | [`sidebar.tsx:117`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L117) | Badge is cleared on /export/:assetId, a screen that does not list finished copies |
| 🟡 Consider · Could · 🧪 tests | [`library-page.test.tsx:86`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L86) | The "no import" check runs before any async import could start |
| 🟡 Consider · Should · 🧪 tests | [`export-page.test.tsx:497`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx#L497) | The several-videos test never checks that all three files were imported |

### Questions for you (2)

- [`export-page.tsx:277`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L277) · direction — Enter on a document-wide listener starts an encode from any focus that isn't a button, link or field (the body, a destination card), with no confirmation. Whether a bare Enter should commit an export is a product call.
- [`sidebar.tsx:121`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L121) · direction — The badge now adds the export that is still running to the count of finished copies, even while its progress card is on screen, whereas a finished copy whose ready card is on screen is left out. Whether an in-progress export should count toward the badge is a product decision.

### Risk facts

- `public-contract` · [`prepare-path.ts:13`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts#L13) — `preparePath` keeps its name and signature but now returns `/export/...` URLs, so every existing caller (the recording page, chips, imports) now lands on the new screen.

<details><summary>What the change connects to (12 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Enter anywhere on the Export screen runs the primary action (opens the existing copy or starts an export) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — The export starts in the background and the progress card shows it; the screen stays where it is. If it fails: When another export is running, the busy toast is shown and nothing starts. `startExport` is fire-and-forget (`void`), and its failures go to the export runner's cards. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-102`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:82-89`.
- Dropping a file on the window while Export is open imports it and opens Export on it, keeping the destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — Export opens on the new video with `?to=` set; extra files are named in a toast. If it fails: If `refresh` rejects, `.then` never navigates, and that rejection is not handled in this hook. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`.
- An Email copy passes `destination: "email"` to the export runner (`apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`) — The progress and ready cards fall into the ICU `other` branch and read "your export", as the PR body says. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-57`, `packages/i18n/messages/en.json:1474`.
- Legacy /prepare URLs redirect to /export, keeping the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — Export opens with the same destination preselected. Evidence: `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`, `apps/kaipu-record/src/shared/routes.ts:18-24`.
- Library no longer handles window file drops (useFileDrop/useImportVideos removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Electron navigates the main window to the dropped file, and the app UI is replaced by the video. If it fails: Silent loss of the app view and of any renderer-side export in progress. No guard exists in main. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-51`, `apps/kaipu-record/src/main/index.ts:400-411`.
- Change video / Pick from Library opens a popover listing originals; picking navigates to Export for that video (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:86`) — Export reopens on the picked video, keyed by preparable.id, so the screen starts over. If it fails: Synchronous navigation only, with no async call to fail. Arrows inside the dialog are ignored by destinationStep, and Enter on a list button is ignored by isPrimaryEnter. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:150-163`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`.
- Recent exports shows the running export from useExportRunner plus the newest finished copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:35`) — A row with a percentage while exporting. Finished rows open /library/:assetId. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:112`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-105`.
- Rail Export item badge counts the running export plus unannounced finished copies (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`) — The badge sits on the Export rail item, labelled with export.railBadge ('# copy in progress or ready'). The Library item no longer has a badge. If it fails: If the export errors, status becomes 'error' and the running count drops to 0. The in-memory store means a relaunch starts with nothing pending. On /export/:assetId, finished copies are announced wit… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:101-113`, `packages/i18n/messages/en.json:946`.
- New Export rail item linking to ROUTES.exportNew (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:53`) — A new rail entry with the Upload icon and the label nav.export. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:68-69`, `apps/kaipu-record/src/shared/routes.ts:18-20`.
- Deleted the Prepare page, its destination list and its drop zone; isPrimaryEnter moved to the Export page (`apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx:1`) — /prepare URLs redirect to /export. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375`, `apps/kaipu-record/src/shared/routes.ts:21-24`.
- A file dropped on the Library window, which no longer has a drop zone (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Chromium's default runs: the window navigates to the dropped file, replacing the app UI. If it fails: The app UI is lost until a reload. No toast or error tells the user what happened. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:400`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:414-416`.
- A dropped video on Export is imported and opened, keeping the chosen destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:485`) — Navigates to /export/<new>?to=<destination>. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:213-216`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** Part 1 covers the router, the Export page, its header, drop zone and destination row, the Email destination, and the preparePath and usePrepareCopy changes. The claims I checked hold:

- The legacy `/prepare` URLs redirect to `/export` with the query kept.
- An Email copy falls into the ICU `other` branch, so the cards say "your export".
- A second export is blocked by the busy guard.
- Enter is excluded on buttons, links and fields, including the picker's items.

Two "consider" findings, no defects at fix level:

- The redirect after a failed probe (`export-page.tsx:98`) drops the destination picked on screen.
- The Library detail paths (`export-page.tsx:112` and `:162`) are hard-coded and not encoded, unlike the Export paths next to them.

**Batch 2 of 6.** One fix-level finding in this part. The PR takes window-wide drop handling off the Library, so a file dropped there now makes Electron navigate the app window to the file; the PR describes this as "does nothing". The new stage, picker and recent-exports components have no defects I could find. Removing destination-detail.tsx also drops the FramingPreview and the "What changes" card, which matches the redesign the PR describes.

**Batch 3 of 6.** Part 3 covers three deletions from the Prepare page, the rail's new Export item and its badge, a test that replaces the old drop-zone test with one aimed at the useFileDrop hook, and destination tests updated for Email. The new hook test matches use-file-drop.ts. The destinations tests match destinations.ts: Email uses chat's preset, and `destinationOfPreset("balanced")` returns "chat". No file still imports the deleted modules. One finding, at "consider": the sidebar clears the badge on /export/:assetId, but that screen does not list finished copies, so a copy that finishes while the user is there never shows in the badge.

**Batch 4 of 6.** Part 4 covers the new Export page tests and the route updates in the Library and Library-detail tests. The Export tests line up with `export-page.tsx`. My main concern is the Library: with its drop zone gone, nothing on that screen calls `preventDefault` on a file drop, and main has no navigation guard. A file dropped there should navigate the window to the file in place of the app. The new Library test ignores the result of `fireEvent.drop`, so it accepts that outcome; it also checks for an import before any async import could start. Separately, the several-videos Export test never checks that all three files were imported.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 11 | $0.60 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 9 | $0.51 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 15 | $0.60 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 8 | $0.46 |
| Batch 5 of 6 | 8 | 854 | 2 | 8 file(s) left after a retry | 8 | $0.56 |
| Batch 6 of 6 | 11 | 843 | 4 | 11 file(s) left: budget spent | 4 | $0.33 |

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

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 60 in / 23k out / 1.1M cache read / 249k cache write · Claude subscription: API-equivalent estimate, not a bill · $3.05</sub>

<!-- wachi:review -->

<!-- wachi:partial sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 state=eyJyIjpbImFwcHMvZG9jdW1lbnRhdGlvbi9zcmMvY29udGVudC9kb2NzL2JhY2tsb2cvZXhwb3J0LXNjcmVlbi5tZCIsImFwcHMvZG9jdW1lbnRhdGlvbi9zcmMvY29udGVudC9kb2NzL2JhY2tsb2cvaW5kZXgubWR4IiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9mZWF0dXJlcy9saWJyYXJ5L2NvbXBvbmVudHMvaW1wb3J0LWRyb3Atem9uZS5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9mZWF0dXJlcy9wcmVwYXJlL2NvbXBvbmVudHMvZGVzdGluYXRpb24tbG9nby5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvZGVzdGluYXRpb24tcm93Lm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9leHBvcnQtZHJvcC16b25lLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9leHBvcnQtaGVhZGVyLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9leHBvcnQtcGFnZS5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvZXhwb3J0LXN0YWdlLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9yZWNlbnQtZXhwb3J0cy5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvdmlkZW8tcGlja2VyLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2xpYnJhcnkvbGlicmFyeS1wYWdlLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL3ByZXBhcmUvZGVzdGluYXRpb24tbGlzdC5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9wcmVwYXJlL3ByZXBhcmUtcGFnZS50ZXN0LnRzeCIsImFwcHMva2FpcHUtcmVjb3JkL3NyYy9yZW5kZXJlci9zcmMvc2hlbGwvc2lkZWJhci50ZXN0LnRzeCIsImFwcHMva2FpcHUtcmVjb3JkL3NyYy9zaGFyZWQvcm91dGVzLnRzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3NoYXJlZC93aW5kb3ctc2l6ZS50ZXN0LnRzIiwicGFja2FnZXMvaTE4bi9tZXNzYWdlcy9lbi5qc29uIiwicGFja2FnZXMvaTE4bi9tZXNzYWdlcy9lcy5qc29uIl0sInQiOltdfQ -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6IjYzZDY2ZjczLTVmYzUtNGJkOS04OGE4LWEyNGJkZTA2Zjg5ZCIsInN0YXR1cyI6InBhcnRpYWwiLCJyZWFzb24iOm51bGwsImZpbmRpbmdzIjp7InRvdGFsIjo3LCJieV9zZXZlcml0eSI6eyJibG9ja2VyIjowLCJmaXgiOjIsImNvbnNpZGVyIjo1LCJpbmZvIjowfSwiYnlfcGxhY2VtZW50Ijp7ImlubGluZSI6NywiYm9keSI6MCwib3V0c2lkZV9kaWZmIjowfSwidW50aHJlYWRlZF9ibG9ja2luZyI6MH19 -->

<!-- wachi:attempt id=63d66f73-5fc5-4bd9-88a8-a24bde06f89d -->
