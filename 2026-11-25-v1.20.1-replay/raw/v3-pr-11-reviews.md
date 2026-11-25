# kaipu-bench-wachi-v3#11 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:54:19Z · commit b12d760

👮 **Wachiman** · ⚠️ **Partial: 11 of 47 files not reviewed** · 2 to fix in this PR · 2 questions for you · 2 to consider · whole PR at `b12d760`

> ⚠️ **Partial review: 36 of 47 files reviewed.** 11 not reviewed because a call ran out of its budget. They are listed under "Files not reviewed". Ask `/wachiman review <paths>` for the rest.

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 2 to consider · ⚪ 0 for your information (4) · 3 Should · 1 Could |
| **Risk** | At least medium: 11 files were not reviewed; top fact `public-contract` at `prepare-path.ts:13`, see Risk facts |
| **Needs a person** | 1 trade-off, in `destinations.ts:71` |
| **Coverage** | 36 of 47 files reviewed, whole pull request; 11 not reviewed, listed under Files not reviewed. Ask `/wachiman review <paths>` for the rest |
| **Read first** | `prepare-path.ts`, `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | Dropping a file on the Library now hits Electron's default and navigates the window to the file |
| 🟠 Fix · Should · 🧪 tests | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | "does not take a video dropped on the window" passes even if Library still imports drops |

### To consider (2)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:212`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L212) | A destination picked on screen is not in the URL, so Back loses it |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | "with and without a video" only checks the with-video URL |

### Questions for you (2)

- [`destinations.ts:71`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts#L71) · trade-off — Email shares chat's balanced preset, so both cards show 'Ready' for the same file and the status cards fall back to 'your export'; a person must decide whether that ambiguity is acceptable.
- [`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L95) · open question — The source probe gates the screen; a probe error shows a toast and redirects to /export: Can probeSource reject or hang, for example on an IPC failure, rather than resolving null? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.

### Risk facts

- `public-contract` · [`prepare-path.ts:13`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts#L13) — preparePath() and prepareNewPath() keep their names but now return /export URLs, which every sibling entry point that links to Prepare relies on.

<details><summary>What the change connects to (10 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- The source probe gates the screen; a probe error shows a toast and redirects to /export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95`) — Can probeSource reject or hang, for example on an IPC failure, rather than resolving null? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.

**Closed, with the lines they rest on**

- Enter and the left/right arrows are handled on the whole document while ExportScreen is mounted (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — Enter starts the copy, or opens the existing one when a reusable export exists (lines 262-266). The arrows move the pink selection, and focus follows it when it was on a card (lines 289-296). If it fails: When no destination is selected, primary() returns without doing anything (line 263). When an export is already running, copy.start shows the busy toast (use-prepare-copy.ts:99-101). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:262-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:50-58`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:82-89`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-101`.
- Old /prepare URLs redirect to /export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — The Export screen opens with ?to= kept. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- A video dropped on Export, or picked with Browse files, is imported and Export opens on it with the current destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — The Export screen opens on the new video. Extra files are named in a toast. If it fails: The navigate call is chained on relist() with no catch (use-prepare-import.ts:48), so a failed refresh leaves the user on the drop zone with no message. This code is unchanged by this part. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:39-56`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`.
- Email is a new destination that shares the balanced preset (`apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:71`) — A Balanced copy shows 'Ready' on both the Chat and Email cards (export-page.tsx:338). The PR body says this is intended. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:37-45`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:104`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:338`.
- Library no longer handles window file drops (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — With no handler, Electron's default for a dropped file applies: it navigates the main window to the file URL. If it fails: The app UI is replaced by the dropped file, and renderer state is lost until the user reloads. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:29-47`, `apps/kaipu-record/src/main/index.ts:400-403`.
- Recent exports row for the running job (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:47`) — Shows the logo, the source title and the rounded percentage. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:59`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:314`.
- Rail badge moves from Library to Export and adds 1 while an export is running; opening /export (any sub-path) or /library clears the finished-copy part. (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The badge and its aria label (export.railBadge, 'copies in progress or ready') show on the Export rail item through Rail's badge/badgeLabel props. The Library item no longer has a badge. If it fails: The state is in memory (ready-copies store and export runner), so a relaunch starts at zero, as before. An export in the 'error' status counts as 0 and is not on the badge. The error card in ExportSt… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-75`, `apps/kaipu-record/src/shared/routes.ts:13-24`, `packages/i18n/messages/en.json:946`.
- Test asserts LibraryPage ignores a file dropped on the window (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — None. The test passes whether or not a drop handler is mounted on Library. If it fails: A regression where Library still imports dropped files would not be caught. Evidence: `apps/kaipu-record/src/renderer/src/test/setup.ts:156`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:96-112`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:421`.
- Export tests cover a dropped video being imported and opened with the selected destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:485`) — The route becomes /export/asset-9?to=chat; a toast reports the extra videos. If it fails: importVideoFiles rejecting is reported via reportError in run() (use-import-videos.ts:84-85); not covered by these tests. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-56`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:76-92`.
- Export rail item badges running and unseen finished copies; opening Export or the Library clears them (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The badge and aria label on the Export link (tests at sidebar.test.tsx:44-79). Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** Part 1 (routing, the Export page and its header, drop zone and destination row, the Email destination, path helpers) has one finding, rated "consider". A destination picked on the Export screen lives only in component state. It is never written to `?to=`, so going back to the screen from another page drops the choice, along with the YouTube resolution and framing settings.

The rest of what I checked holds:

- **Old URLs:** `/prepare` links redirect to Export and keep their query.
- **Keyboard:** Enter skips fields, buttons and links, and the arrows skip other option groups and pop-ups.
- **Email:** it reuses chat's preset without changing which destination that preset maps back to.
- **Dropped files:** a video dropped on Export carries the destination picked at the moment the import finishes.

One question is still open. The file probe has no error handler and no time limit (`use-prepare-copy.ts:51`). If that promise rejects or never settles, the screen stays on "Reading…" with no message. Whether it can actually reject or hang is unverified (I did not read `probe-source.ts`). This part does not change that code.

**Batch 2 of 6.** I reviewed all five files in this part and found one issue worth fixing. I did not run the app; the check was done by reading the code.

**Dropping a file on the Library (`library-page.tsx:53`).** The PR says this now does nothing. In fact, no code handles the drop any more, so Electron's default should take over: it opens the dropped file in the main window in place of the app. I rated this medium confidence because that default is standard Electron behaviour, not something I saw in this repository.

- Before this PR, the Library's file-drop hook blocked that default (`use-file-drop.ts:29-47`).
- The main process doesn't block navigation either: `main/index.ts:400` only handles new windows.

The user would lose the app screen and any export state the renderer holds until they reload. The fix is either to block file drops on the Library (or app-wide in the shell), or to add a navigation guard in the main process.

**The other four files look fine:**

- **Export stage (`export-stage.tsx`):** the GitHub size bar is drawn against the 10 MB free limit, and its colour and label follow whether the copy fits.
- **Recent exports (`recent-exports.tsx`):** the in-progress row falls back to the preset's destination when the job doesn't name one, which matches the export runner.
- **Video picker (`video-picker.tsx`):** Escape or a click outside closes the list, and the listeners are removed when it closes.
- **Deleted Prepare detail (`destination-detail.tsx`):** its removal matches the new stage.

**Batch 3 of 6.** I found nothing to fix in the seven files of this part.

- **Deleted Prepare files:** nothing still uses `destination-list`, `prepare-drop-zone`, `prepare-page` or `import-drop-zone`. `isPrimaryEnter` now lives in `pages/export/export-page.tsx`.
- **New `use-file-drop.test.tsx`:** it keeps every hook case from the deleted `import-drop-zone.test.tsx`, checking the hook's `dragging` state directly instead of the drop zone's markup. The two cases that tested the zone's own button (click and importing) were dropped along with the component.
- **`destinations.test.ts`:** it now accounts for Email sharing Chat's `balanced` preset. The preset coverage is collected as a set so `balanced` is not listed twice, and `destinationOfPreset("balanced")` is checked to return Chat.
- **`sidebar.tsx`:** `useExportBadge` clears finished copies the same way the old Library badge did, and also does it on any `/export` path. It adds 1 while an export is running. The `export.railBadge` message exists in `en.json`.

Two stale leftovers sit in files from other parts, so I did not report them here:

- The `backgroundCopy.libraryBadge` message is no longer used by any code.
- The comment at the top of `ready-copies.ts` still says the count is on the Library rail item.

**Batch 4 of 6.** I found one problem in this part. The Library test "does not take a video dropped on the window" (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) passes no matter what the page does with a drop. It leaves `pathForFile` at the default test stub, which returns an empty path, so the dropped file is skipped before `importVideoFiles` could ever be called. If Library started taking drops again, the test would still pass. The fix is to give `pathForFile` a real path, as the Export tests do, and also check that the page leaves the drop alone and shows no toast.

The new Export page tests match the code in `export-page.tsx`: picking a destination, the Enter and arrow keys, keeping the destination when a dropped video is imported, and the redirect from old Prepare links. The Library detail tests only change the expected address from `/prepare` to `/export`.

**Batch 5 of 6.** I reviewed all eight files in this part and found one minor test gap.

**The finding:** in `sidebar.test.tsx:39`, the test named "is active on Export with and without a video" only renders `/export/asset-1`. The bare `/export` URL is never checked, so its active state isn't pinned by a test. Either add that case or rename the test.

**Checked and fine:**

- **Removed Prepare page test:** its cases now live in `export-page.test.tsx`. That covers the drop zone, several dropped videos, a non-video file, the one-export-at-a-time rule, an unreadable file, screenshots, copies already marked Ready, and the unexported-edits warning.
- **Rewritten sidebar tests:** they match `useExportBadge` in `sidebar.tsx`. The count is the export running now plus finished copies the user hasn't seen. Opening Export or the Library clears it, and opening a copy's page forgets that copy.
- **Stylesheets:** every CSS variable used in the new stylesheets is already used elsewhere in the renderer. I only searched for that usage; I didn't open the file that defines them.
- **Removed `import-drop-zone.module.css`:** its component is removed in the same PR.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 8 | $0.51 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 9 | $0.45 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 8 | $0.37 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 9 | $0.45 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 5 | $0.34 |
| Batch 6 of 6 | 11 | 843 | 4 | 11 file(s) left after a retry | 8 | $0.63 |

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

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 56 in / 21k out / 890k cache read / 248k cache write · Claude subscription: API-equivalent estimate, not a bill · $2.75</sub>

<!-- wachi:review -->

<!-- wachi:partial sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 state=eyJyIjpbImFwcHMvZG9jdW1lbnRhdGlvbi9zcmMvY29udGVudC9kb2NzL2JhY2tsb2cvZXhwb3J0LXNjcmVlbi5tZCIsImFwcHMvZG9jdW1lbnRhdGlvbi9zcmMvY29udGVudC9kb2NzL2JhY2tsb2cvaW5kZXgubWR4IiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvZXhwb3J0LXN0YWdlLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2V4cG9ydC9yZWNlbnQtZXhwb3J0cy5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3JlbmRlcmVyL3NyYy9wYWdlcy9leHBvcnQvdmlkZW8tcGlja2VyLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL2xpYnJhcnkvbGlicmFyeS1wYWdlLm1vZHVsZS5jc3MiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvcmVuZGVyZXIvc3JjL3BhZ2VzL3ByZXBhcmUvZGVzdGluYXRpb24tbGlzdC5tb2R1bGUuY3NzIiwiYXBwcy9rYWlwdS1yZWNvcmQvc3JjL3NoYXJlZC9yb3V0ZXMudHMiLCJhcHBzL2thaXB1LXJlY29yZC9zcmMvc2hhcmVkL3dpbmRvdy1zaXplLnRlc3QudHMiLCJwYWNrYWdlcy9pMThuL21lc3NhZ2VzL2VuLmpzb24iLCJwYWNrYWdlcy9pMThuL21lc3NhZ2VzL2VzLmpzb24iXSwidCI6W119 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6IjYyZGFmYTQ2LTMxNTktNGZlZi04ZjIzLWJlMDk3MGQwOGFhYSIsInN0YXR1cyI6InBhcnRpYWwiLCJyZWFzb24iOm51bGwsImZpbmRpbmdzIjp7InRvdGFsIjo0LCJieV9zZXZlcml0eSI6eyJibG9ja2VyIjowLCJmaXgiOjIsImNvbnNpZGVyIjoyLCJpbmZvIjowfSwiYnlfcGxhY2VtZW50Ijp7ImlubGluZSI6NCwiYm9keSI6MCwib3V0c2lkZV9kaWZmIjowfSwidW50aHJlYWRlZF9ibG9ja2luZyI6MH19 -->

<!-- wachi:attempt id=62dafa46-3159-4fef-8f23-be0970d08aaa -->
