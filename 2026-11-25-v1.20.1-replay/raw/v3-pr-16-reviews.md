# kaipu-bench-wachi-v3#16 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:55:23Z · commit b12d760

👮 **Wachiman** · 🟠 **2 to fix in this PR** · 3 questions for you · 6 to consider · whole PR at `b12d760`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 6 to consider · ⚪ 1 for your information (9) · 6 Should · 2 Could · 1 FYI |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Needs a person** | 1 direction, in `export-stage.tsx:228` |
| **Coverage** | 47 of 47 files reviewed, whole pull request |
| **Read first** | `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx`, `destination-list.tsx` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | A file dropped on the Library now sends the whole window to that file |
| 🟠 Fix · Should · 🧪 tests | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | "Does not take a dropped video" does not check that the window stops the drop, so Electron can still open the file in the app window |

### To consider (6)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:98`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L98) | Unreadable-file redirect drops the destination picked on this screen |
| 🟡 Consider · Should · 📝 docs | [`destination-row.tsx:13`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/destination-row.tsx#L13) | \`DestinationSizes.sizeText\` doc promises an "up to" form the row never gets |
| 🟡 Consider · Could · 🐛 bug | [`export-stage.tsx:228`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx#L228) | Fill / Fit lost its preview, and the frame-rate cap and sound changes are no longer shown |
| 🟡 Consider · Should · 🧹 cleanup | [`sidebar.tsx:122`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L122) | Badge moved to Export, but the old Library vocabulary stays behind |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | "with and without a video" only renders the with-video URL |
| 🟡 Consider · Should · 🧹 cleanup | [`library-page.module.css:108`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css#L108) | Orphaned comment for the removed import strip |

### Questions for you (3)

- [`export-stage.tsx:228`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx#L228) · direction — Someone has to decide whether dropping the Fill/Fit still preview and the smoothness and sound rows (which Prepare showed) is intended by the design or a regression.
- [`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L85) · open question — Files dropped anywhere on the Export screen are imported and the Export screen opens on the first one: Does `useImportVideos` show a visible error when the import IPC rejects, and does `useFileDrop` always preventDefault on drop? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts`.
- [`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) · open question — A file dropped on the Library window after the Library's drop handling was removed: Does any shell-level listener or main-process setting (setWindowOpenHandler, will-navigate, webPreferences) stop file drops on screens other than Export? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/shell/app-shell.tsx`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

<details><summary>For your information (1)</summary>

| | Where | Finding |
| --- | --- | --- |
| ⚪ Info · FYI · 🐛 bug | [`recent-exports.tsx:65`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx#L65) | Email copies show as Slack · Discord in Recent exports |

</details>

<details><summary>What the change connects to (12 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Files dropped anywhere on the Export screen are imported and the Export screen opens on the first one (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — Does `useImportVideos` show a visible error when the import IPC rejects, and does `useFileDrop` always preventDefault on drop? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts`.
- A file dropped on the Library window after the Library's drop handling was removed (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Does any shell-level listener or main-process setting (setWindowOpenHandler, will-navigate, webPreferences) stop file drops on screens other than Export? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/shell/app-shell.tsx`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

**Closed, with the lines they rest on**

- Old `/prepare` and `/prepare/:assetId` URLs redirect to Export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — Bookmarked or status-card links to Prepare open Export with `?to=` kept. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- Enter anywhere on the document runs the primary action (export, or open the existing copy) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — Starts the background export, or navigates to the existing copy in the Library. If it fails: When `copy.start` returns false (busy), the busy toast is shown. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:82-90`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-101`.
- A probe error on the picked video shows a toast and redirects to `/export` (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95`) — The user sees a "can't read" toast and lands on the drop zone. If it fails: A destination picked on this mount is lost (reported as a finding). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:84-99`.
- Library stops taking window file drops (removes useFileDrop/ImportDropZone) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — A dropped file makes Chromium navigate the window to the file, and the app UI is replaced. If it fails: With no will-navigate guard in main, the window leaves the app, and renderer-owned export state is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/main/index.ts:396`, `apps/kaipu-record/src/main/index.ts:400-411`.
- VideoPicker opens a list; picking navigates to Export on that video (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:86`) — Export reopens on the chosen video and keeps the chosen destination. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`.
- RecentExports shows the running job from useExportRunner and the newest finished copies (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:35`) — The running row shows a percentage; finished rows open the copy's Library page. If it fails: Email copies show as chat (balanced preset). Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:59`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:71`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- Rail Export item shows a badge: 1 while an export runs, plus finished copies not yet announced; visiting /export or /export/:id announces them (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`) — The badge renders on the Export rail item with the export.railBadge plural label. The Library item no longer shows a badge. If it fails: If the export errors, status becomes "error" and the running +1 disappears. The error card (ExportStatusCards) shows the failure. State is in memory and resets on relaunch, as documented. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-122`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462-463`, `apps/kaipu-record/src/shared/routes.ts:18-20`, `packages/i18n/messages/en.json:946`.
- Old /prepare URLs redirect to /export and keep the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — The Export screen opens with ?to= preselected. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`.
- A probe failure sends the user to Export with no video and shows a toast (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329`) — A toast plus the drop-zone screen. If it fails: The failure is visible to the user, and the replace navigation keeps Back from looping to the failed entry. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`.
- The rail's Export item shows the badge (running export plus finished copies the user has not seen). Opening Export or the Library clears it. (`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44`) — The Export link's accessible name includes the railBadge count, and its text shows the number. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`.
- Bar tag and fill colours keyed on the new `data-tone` attribute instead of `data-direction` (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:262`) — The size bar's tag and fill show teal for lighter/fits and amber for not-lighter/over. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:320`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:329`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:262-270`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:288-291`.
- Removed library i18n keys (importVideo, importing, importDropTitle/Hint/Active) and prepare.prepareAVideo (`packages/i18n/messages/en.json:603`) — No missing-message fallback is rendered. Evidence: `apps/kaipu-record/src/main/library/index.ts:192`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** Part 1 of 6 (router, route helpers, the new `email` destination and the Export page shell). I found nothing blocking and two "consider" items:

1. **Lost destination on an unreadable file** (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:98`): when a video can't be read, the redirect back to `/export` drops a destination the user picked on the same screen. The other exits keep it.
2. **Wrong doc comment** (`apps/kaipu-record/src/renderer/src/pages/export/destination-row.tsx:13`): the `DestinationSizes.sizeText` comment lists an "up to" size form that the destination cards are never given.

Checked and fine:

- The legacy Prepare redirects keep the `?to=` query.
- Imports from a dropped file now open Export directly.
- Email shares chat's preset, and `destinationOfPreset` still answers "chat", as the comment says.
- The global Enter handler leaves buttons and fields alone.

Still open: I did not verify how the import hooks handle failures (`use-import-videos.ts`, `use-file-drop.ts`).

**Batch 2 of 6.** Part 2 has one bug to fix. `library-page.tsx` dropped `useFileDrop` along with the drop strip, and nothing else guards the window: there is no `will-navigate` handler in main. So a file dropped on the Library makes Electron navigate the window to that file, which contradicts the PR's claim that it "does nothing". In the new stage, the Fill/Fit preview and the frame-rate and sound change rows are gone without mention. Email copies in Recent exports show as Slack · Discord, a knock-on effect of the shared Balanced preset the PR already notes. The picker and the Recent exports strip are otherwise sound.

**Batch 3 of 6.** I found no defects in this part of the PR, only one cleanup suggestion about stale naming.

**Rail badge (`sidebar.tsx`).** The new `useExportBadge` counts each export once:

- **While an export runs:** the badge shows +1.
- **When it finishes:** the runner sets the status to idle and records the finished copy at the same moment (`export-runner.ts:462-463`).
- **While its ready card is on screen:** that copy is left out of the count, so the running +1 and the finished copy never stack.
- **Opening `/export` or `/export/:assetId`:** finished copies are cleared from the badge, as opening the Library already did.

**Deleted files and remaining callers.** Nothing still imports the deleted Prepare files or the deleted `ImportDropZone`. `isPrimaryEnter` now lives in `export-page.tsx`.

**Tests.** `use-file-drop.test.tsx` carries over every `useFileDrop` test from the deleted `import-drop-zone.test.tsx`. Only the tests for the deleted component itself were dropped. The `destinations.test.ts` changes match the new Email destination, which shares the Balanced preset: `destinationOfPreset("balanced")` still returns `chat`.

**Cleanup suggestion.** The badge moved to Export, but some Library-era names stayed behind:

- The `backgroundCopy.libraryBadge` message string is now unused.
- `libraryBadgeCount` now feeds the Export badge.
- The doc comment in `ready-copies.ts` still describes a Library badge.

**Batch 4 of 6.** Part 4 covers three test files. The Export page tests match what export-page.tsx does: legacy redirect, the probe-error path, the keyboard guards, the Ready-copy reuse and drop import. The library-detail path updates are simple renames. One gap: the Library's new "does not take a dropped video" test checks only that no import ran. It does not check that the drop's default was prevented, while the Export tests do check that. With the Library's useFileDrop gone and no will-navigate guard in main, a file dropped on the Library likely makes Electron load the file in place of the app, and this test would still pass.

**Batch 5 of 6.** I found one small test issue in part 5 and nothing that blocks the merge.

**Sidebar tests**

- The new tests match the sidebar code: the Export item sits right after Editor, the badge moves from Library to Export, and opening either Export or the Library clears it.
- One test is named "is active on Export with and without a video", but it only renders the with-video URL, `/export/asset-1`. The bare `/export` route is never checked (`sidebar.test.tsx:39`). I flagged it at "consider".

**Removed Prepare tests**
Deleting `prepare-page.test.tsx` goes with removing the Prepare page itself. Its coverage was meant to move to `export-page.test.tsx`, which belongs to another part, so I did not check that here.

**Stylesheets**

- I found nothing wrong in the stylesheets of this part.
- Of the CSS variables they use, I confirmed that `--tone-heavy` and `--tone-saving` are defined in `base.css`. The search also found a shared token file, `packages/tokens/css/tokens.css`, which should define `--accent-primary-ring`, `--border-light`, `--bg-card-hover`, `--font-mono`, `--bg-app` and `--accent-primary-soft`. I did not open it to confirm each one.

**Batch 6 of 6, retry.** I found one minor issue in this part, and nothing that should block the merge.

- **Finding (consider, cleanup):** `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108` still has the comment for the import strip, even though its `.importZone` rule was removed. It now reads as if it described the toolbar below it.
- **Stage stylesheet:** the new tone selectors in `export-stage.module.css` match the `data-tone` attribute that `export-stage.tsx` sets on the size bar's tag and fill, so the bar's colours still apply.
- **Removed messages:** a search of `apps/kaipu-record/src` found no remaining use of the removed message keys (the Library's import keys and `prepareAVideo`).
- **No problems:** the route definitions, the window-size test additions, the new stylesheets, the backlog doc and its index row, and the en/es message additions.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 5 | $0.40 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 11 | $0.58 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 13 | $0.50 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 5 | $0.39 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 5 | $0.32 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed after a retry | 10 | $0.71 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**Email copies show as Slack · Discord in Recent exports (confidence high)** ([`recent-exports.tsx:65`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx#L65))

A finished row gets its destination from `destinationOfPreset(copy.export!.preset)`, which returns `chat` for `balanced` (`features/prepare/destinations.ts:102-107`). A copy exported for Email is therefore listed with the Slack · Discord logo and name. The running row uses `running.destination`, so it shows Email correctly. The PR body already lists the shared Balanced preset as a decision; this is one more place where it shows.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 56 in / 25k out / 913k cache read / 272k cache write · Claude subscription: API-equivalent estimate, not a bill · $2.90</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6IjFlMWVhMTg1LWY1MjMtNDE0Ni1iYmRlLTAwYzc5Y2QxMGI5NiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6OSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoyLCJjb25zaWRlciI6NiwiaW5mbyI6MX0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjgsImJvZHkiOjEsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=1e1ea185-f523-4146-bbde-00c79cd10b96 -->
