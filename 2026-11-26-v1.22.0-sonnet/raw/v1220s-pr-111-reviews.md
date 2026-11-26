# kaipu-bench-wachi-v3#111 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:04:40Z · commit b12d760

👮 **Wachiman** · 🟠 **2 to fix in this PR** · 1 question for you · 11 to consider · whole PR at `b12d760`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 11 to consider · ⚪ 0 for your information (13) · 6 Should · 7 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 47 of 47 files reviewed, whole pull request |
| **Read first** | `destination-detail.tsx`, `export-page.tsx`, `prepare-page.tsx`, `export-stage.tsx`, `destination-list.tsx` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`use-prepare-copy.ts:119`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts#L119) | Email copies get the generic "export" title on the progress and ready cards |
| 🟠 Fix · Should · 🐛 bug | [`library-page.tsx:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L53) | A video dropped on the Library now navigates the window to the file |

<details><summary>To consider (11)</summary>

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🧹 cleanup | [`export-page.tsx:112`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L112) | Library detail URL is hard-coded instead of built from ROUTES |
| 🟡 Consider · Could · 🐛 bug | [`export-page.tsx:98`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx#L98) | Unreadable-file redirect drops a destination picked on screen |
| 🟡 Consider · Could · 🐛 bug | [`export-stage.tsx:111`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx#L111) | Keep card says "sound as recorded" even when the recording has no audio |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.tsx:121`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L121) | The new "in progress" half of the Export badge has no test |
| 🟡 Consider · Could · 🧹 cleanup | [`sidebar.tsx:66`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L66) | Message keys orphaned by this change |
| 🟡 Consider · Could · 🐛 bug | [`library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) | Test pins that a file dropped on Library is ignored, but nothing stops Electron from opening it |
| 🟡 Consider · Should · 🧪 tests | [`sidebar.test.tsx:39`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L39) | Test name claims "with and without a video" but only checks the with-video route |
| 🟡 Consider · Could · 🧪 tests | [`sidebar.test.tsx:32`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx#L32) | The badge's new "copy in progress" half has no test |
| 🟡 Consider · Could · 🐛 bug | [`destination-row.module.css:55`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/export/destination-row.module.css#L55) | Keyboard focus outline is clipped by the row's scroll box |
| 🟡 Consider · Should · 🧹 cleanup | [`en.json:786`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/packages/i18n/messages/en.json#L786) | About 60 keys of the deleted Prepare screen are left in the \`prepare\` namespace |
| 🟡 Consider · Should · 🧹 cleanup | [`library-page.module.css:108`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css#L108) | Stale comment left where the drop-strip rule was removed |

</details>

### Questions for you (1)

- [`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L80) · open question — A video file dropped anywhere on the Library page (behaviour change from the removed ImportDropZone): Does anything else (preload, window creation options, another global handler) cancel file-drop navigation on the Library screen? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

<details><summary>What the change connects to (12 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- A video file dropped anywhere on the Library page (behaviour change from the removed ImportDropZone) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Does anything else (preload, window creation options, another global handler) cancel file-drop navigation on the Library screen? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx`.

**Closed, with the lines they rest on**

- Start a copy for Email from the Export screen (Enter or the primary button) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252`) — The progress and ready cards take the Email logo (`DestinationLogo` has an `email` icon). Their titles use the ICU `select`, which has no `email` case, so the title reads "Preparing your export…" and "Your export is ready". If it fails: Wrong title text, no crash. If another export is running, `start` shows the busy toast and returns false. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-119`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-56`, `packages/i18n/messages/en.json:1474`, `packages/i18n/messages/en.json:1480`.
- Drop or browse a video on Export, then open it with the destination that was picked (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — The new video opens on Export with the same card selected. With more than one file, a toast names the rest. If it fails: If `refresh` fails, `useLocalLibrary` catches the error and shows a retry toast, so the new video is not in `videos`. The page then shows "file not found" with a link back to Export. On unmount, the… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-57`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:21-58`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:41-62`.
- Legacy /prepare URLs redirect to /export (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — Old links and history entries land on Export with `?to=` kept, and `replace` keeps Back from looping. If it fails: None found. Evidence: `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`, `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-25`.
- Global Enter and Arrow key handler on the Export screen (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — Arrows move the selected card and focus follows when it started on a card. Enter exports, or opens the existing copy. If it fails: `isPrimaryEnter` has no `[role='dialog']` exclusion, unlike `destinationStep`. The picker's items are buttons, so Enter there is not hijacked today. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:273-301`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:68-112`.
- File dropped on the Library window (no handler any more) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Electron's default for an unhandled file drop is to navigate the window to the file; with no main-process guard the app UI is replaced by the video. If it fails: Window left on the raw file until reload; no error shown. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:9-11`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`.
- Recent exports strip: running row and finished rows (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — Running row shows percent and bar from runner.fraction; finished rows come from recentCopies(videos), opening /library/:assetId on click. If it fails: If the export fails or is cancelled the running row disappears and nothing is added; the failure is reported by the status cards, not here. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:15-20`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:68`.
- Video picker (Change video / Pick from Library) (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:32-60`) — A dialog panel under the trigger; picking navigates and keeps the chosen destination through ExportPage's `chosen` ref. If it fails: No async work; an empty list shows pickerEmpty. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:12-16`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`.
- Rail badge moves from Library to a new Export item and now also counts the running export (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export rail item shows a number for the copy being made plus finished copies not yet shown. The Library item no longer carries a badge. Opening Export clears the finished part while the running part stays. If it fails: No async call, so no rejection path. The store is in memory, so a relaunch loses pending badges, as before. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-75`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:61-62`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:26-36`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.
- Delete ImportDropZone and its test; drop behavior is now tested on the `useFileDrop` hook alone (`apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:20`) — No user-visible change from the test move itself. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:20-72`.
- Dropping a video on Export imports it and opens it, with the destination kept (usePrepareImport -> preparePath) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:460`) — The screen navigates to /export/<new asset> with the same ?to= after the library re-lists, and a toast names the extra videos. If it fails: A non-video drop gets a toast and the default is prevented (the tests assert both). An import that fails or is cancelled opens nothing. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-52`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:12-15`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:77-88`.
- Rail "Export" item with a badge that counts the running export plus finished-unseen copies, cleared on opening Export or the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111`) — The Export rail item shows a count with the aria-label 'N copies in progress or ready'; the Library item has no badge. If it fails: No async call added. The state is in memory, so the badge is lost on relaunch, as before. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:61-75`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.
- Removed the Library's import strings (`importVideo`, `importing`, `importDropTitle`, `importDropHint`, `importDropActive`) from the `library` namespace in en.j… (`packages/i18n/messages/en.json:603`) — The Library shows no import strip or button. Export shows its own strings. If it fails: A missing key would show as a raw key or throw in next-intl-style lookups. I found no remaining reader of the removed keys. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:109`, `apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:36`, `packages/i18n/messages/en.json:606`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 6.** Part 1 of 6 mostly holds up: the legacy redirect, the drop-to-import flow and the keyboard handling check out. One defect: an Email export shows the generic \"Preparing your export…\" and \"Your export is ready\" titles, because the ICU `select` in `progressTitle` and `readyTitle` has no `email` case. There are two minor cleanups on `export-page.tsx`.

**Batch 2 of 6.** The new Export stage, recent-exports strip and video picker are internally consistent, and I found no defect in them. I traced the CSS tones, the `plan.direction` values, the GitHub limit constants and the routing helpers, and all of them match. One regression: removing the drop handling from the Library leaves a file dropped there to Electron's default, which navigates the window to the file, because `use-file-drop.ts` is now mounted only on Export and no `will-navigate` guard exists in main. A smaller issue is that the Keep card always says \"sound as recorded\", even for a silent recording. I did not read the CSS modules for the stage, recent exports or picker beyond the stage's bar styles, and I did not read the tests, which belong to other parts.

**Batch 3 of 6.** This part removes the Prepare page, destination list and drop zone, moves the rail badge from Library to a new Export item, and adds an `email` destination test. I found nothing that breaks. Two small points: the \"in progress\" half of the Export badge (`sidebar.tsx:121`) has no test, and the i18n keys the old code used are left behind. The `destinations.test.ts` changes are consistent with `destinations.ts`. The `use-file-drop.test.tsx` hook tests carry over the deleted component's cases.

**Batch 4 of 6.** The Export page tests match the page code I read: destination order, the ?to= handling, the Enter and arrow-key rules, the legacy /prepare redirect and the drop-import flow. The library-detail test only renames /prepare to /export, which is consistent with `preparePath`. One concern in the Library test: it asserts that a file dropped on Library is not imported, but doesn't check that the drop's default is prevented. No guard against Electron navigating to the dropped file was found in the main process.

**Batch 5 of 6.** This part has no defects. It swaps the Library badge for an Export rail badge, deletes the Prepare and import-drop-zone tests and styles, and adds the Export screen's stylesheets. Every CSS custom property the new files use is defined in `tokens.css` or `base.css`, and every class the `.tsx` files reference exists in its module. I left three small notes: the sidebar test named \"with and without a video\" only checks the with-video route, the badge's running-export half has no test, and the card focus outline in the destination row is clipped by 1px.

**Batch 6 of 6.** Nothing in this part blocks the merge. It holds the Export stage, recent-exports and video-picker CSS, the Prepare list CSS deletion, routes, i18n and the backlog docs. The two findings are both cleanup. About 60 keys of the deleted Prepare screen remain in the `prepare` namespace in en.json and es.json, with no reader in the repo. A stale NIW2-579 drop-strip comment is left in library-page.module.css. The CSS classes I read match the components, the new `export.*` keys are all present in both locales, and no reader remains for the removed Library import keys. The doc matches what I read of the code.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 20 | $0.34 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 23 | $0.33 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 14 | $0.22 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 11 | $0.18 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 16 | $0.20 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 22 | $0.31 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**About 60 keys of the deleted Prepare screen are left in the `prepare` namespace (confidence high)** ([`en.json:786`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b12d760bd90b1e9619bab115f500f9c1a30cccf3/packages/i18n/messages/en.json#L786))

This PR deletes destination-list, destination-detail, prepare-page and prepare-drop-zone, but their strings stay in `prepare`. I grepped `apps/**/*.{ts,tsx}` and found no reader for `pageSubtitle`, `back`, `notPreparableTitle`/`notPreparableBody`, `groupPostLabel`, `groupSendLabel`, `anotherTitle`/`anotherHint`, `detailTitle`/`detailMeta`, `changesCard`, `change*`, `whyCard*`, `barUnderLimit`/`barOverLimit`, `prepareNote`, `listUpTo`, `meter*`/`tag*` (the size meter uses the `videoEditor` namespace), `youtubeHint*`/`youtubeOption`, `prepareAction*`, `prepareAgain`, `dropTitle`, `dropBody`, `dropActive`, `dropChooseFile` and `dropFromLibrary`. Only `dropMoreInLibrary` (use-prepare-import.ts:49), `dest*`, `copy*` and the `where*` keys still have readers. `GROUP_COPY` in `features/prepare/destination-copy.ts` has no reader either, and `DESTINATION_COPY` is read only for `.name` (master-copies-panel.tsx:68). So `line*`, `say*` and `why*` (including the new `lineEmail`, `sayEmail`, `whyEmail`) have no reader in this PR. The same keys are left in es.json at the same lines. Dropping them would keep the catalog honest. Keep any key a sibling branch still needs.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 88 in / 46k out / 2.1M cache read / 367k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.59</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJiMTJkNzYwYmQ5MGIxZTk2MTliYWIxMTVmNTAwZjljMWEzMGNjY2YzIiwiYXR0ZW1wdCI6IjJlNzljMWViLTM3MjItNGNhNS1iZGJhLWYzNGZiYjYzZmVmYSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MTMsImJ5X3NldmVyaXR5Ijp7ImJsb2NrZXIiOjAsImZpeCI6MiwiY29uc2lkZXIiOjExLCJpbmZvIjowfSwiYnlfcGxhY2VtZW50Ijp7ImlubGluZSI6MTIsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MX0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=2e79c1eb-3722-4ca5-bdba-f34fbb63fefa -->
