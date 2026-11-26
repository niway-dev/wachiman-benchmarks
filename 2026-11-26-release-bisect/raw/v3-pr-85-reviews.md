# kaipu-bench-wachi-v3#85 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:32:09Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

17 finding(s): 5 to fix, 12 to consider; 16 on their lines. Reply in a comment's thread to answer it.

### Risk map

**Medium.**

- `public-contract` · `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:13` — preparePath/prepareNewPath, which every caller uses, now return /export URLs instead of /prepare URLs.
- `public-contract` · `apps/kaipu-record/src/shared/routes.ts:18` — The screen's canonical URL moves from /prepare/:assetId to /export/:assetId; old links survive only through the LegacyPrepareRedirect route.

**Needs a person:**

- `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:71` (`tradeoff`) — Email shares chat's Balanced preset, so a copy made for either shows Ready on both cards, Enter on Email opens the chat copy, and destinationOfPreset labels it chat everywhere else.
- `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121` (`direction`) — The badge now counts "in progress or ready" rather than only "unseen". Someone has to decide whether a copy that is visibly running (on /export, or with the progress card shown) should still raise the rail count.

**Read first:** `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts`, `apps/kaipu-record/src/shared/routes.ts`, `apps/kaipu-record/src/renderer/src/pages/prepare/destination-detail.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx`.

### Outside the diff

- Nit · 🟡🧹 **Consider · cleanup: Prepare screen strings were left behind after the screen was deleted (confidence high)** (`packages/i18n/messages/en.json:869`): The PR deletes the Prepare page, `destination-list`, `destination-detail` and `prepare-drop-zone`, but it only removes `prepare.prepareAVideo` from the messages. Several keys in the `prepare` namespace now have no reader in `apps/kaipu-record/src`, for example `prepareAction`, `prepareActionFull`, `prepareAgain`, `dropChooseFile`, `meterLabel`, `tagNotLighter` and `youtubeHint4k`. The Export screen has its own copies of these strings (`export.exportAction`, `export.exportAgain`, `export.barLabel`, …). Remove the orphaned keys from en.json and es.json. Keep the ones still in use, such as `dropMoreInLibrary` (use-prepare-import.ts:49) and the `why*` titles (destination-copy.ts:26).

### Summary

**Batch 1 of 6.** I reviewed all 13 files in part 1 and have one fix and two considers.

- **Fix (export-page.tsx:117):** whenever the Library reloads its list, the Export screen is briefly replaced by a loading view. That reload happens on every `library:changed`, including the cloud refresh that runs when the page opens. When the screen comes back, the destination the user picked resets to the URL's `?to=` and the YouTube and Fill/Fit choices go back to their defaults, with nothing on screen to say why. Confidence is medium: I did not confirm that a finished copy also fires the event.
- **Consider (export-page.tsx:375):** Enter can start an export while the Change video list is open. The arrow-key check skips dialogs, but the Enter check does not.
- **Consider (export-page.tsx:352):** the `destinationStep` comment says a held key is ignored, but the code never checks `event.repeat`.

Something outside this part: the Library no longer handles file drops, and the main process has no navigation guard. A file dropped on the Library is likely to make the window load that file, not "do nothing" as the PR says. That change is in `library-page.tsx`, so I recorded it under contracts rather than as a finding here.

The rest checks out: the route rename and redirects, the Email destination, and how the destination reaches the progress and ready cards.

**Batch 2 of 6.** I reviewed the five files in part 2 and found two fixes and two smaller suggestions.

Fixes:
- **Library drops** (`library-page.tsx:53`): the Library no longer handles file drops. A file dropped on it now makes Electron navigate the window to that file, losing the app's state. The PR says dropping does nothing; the code does not support that.
- **Before/after crops** (`export-stage.tsx:255`): the crops now show for TikTok · Reels and LinkedIn · Feeds too. Those copies are 1080p, yet they are drawn sharper than the "Uploaded at 1080p" before-crop.

Suggestions:
- The new upload-size and Fill/Fit radio groups do not respond to arrow keys.
- The GitHub limit verdict on the size bar is hidden from screen readers by `role="img"`.

`recent-exports.tsx`, `video-picker.tsx` and the deletion of `destination-detail.tsx` had nothing to flag.

**Batch 3 of 6.** I reviewed all seven files in this part and found one item to consider, nothing that blocks the merge.

**Deletions.** The three removed Prepare files are gone cleanly. No live code imports them: `isPrimaryEnter` and `DestinationSizes` now live under `pages/export/`, and nothing references `DEFAULT_DESTINATION` any more.

**Rewritten tests.**
- `use-file-drop.test.tsx` makes the same checks as the old `import-drop-zone.test.tsx` for `use-file-drop.ts`, using a `data-dragging` attribute in place of the deleted zone.
- The `destinations.test.ts` changes match `destinations.ts`: email shares chat's `balanced` preset, and `destinationOfPreset("balanced")` still answers chat.

**Sidebar (`sidebar.tsx`).** The badge now sits on the Export item, and opening Export or the Library clears the finished copies. One thing to consider (line 121): while an export is running, the badge adds 1 on every page. That includes `/export`, where Recent exports already shows the copy's progress, and pages where the progress card is visible. Finished copies get the opposite treatment: they never count while on screen. No sidebar test covers the running case.

**Outside this part.** `backlog/import-video.md:112` still points at the deleted `import-drop-zone.tsx`. I didn't file it as a finding because that file belongs to another part.

**Batch 4 of 6.** I reviewed all three test files in this part (the Export page, Library detail and Library tests) and found one problem that needs fixing and two small test-naming points.

**Needs fixing**
- **Dropping a file on the Library is not harmless.** The Library no longer listens for file drops. With no listener, Electron's default is to load the dropped file in the main window. The repo's own `use-file-drop.ts` comment says so, and I found no navigation guard in `src/main`. That would replace the app's screen with the file and lose anything running in the renderer, including a background export. The PR's claim that a drop on the Library "does nothing" is therefore wrong.
- `library-page.test.tsx:80` passes anyway: it only checks that nothing was imported. The Export test, by contrast, checks that the drop's default was blocked.
- I rated this medium confidence. I confirmed there is no drop handler or navigation guard, but I could not rule out a guard set elsewhere, for example in the window's configuration.
- Suggested fix: keep a window-wide guard that blocks the default without importing. It could sit in the app shell, or in the main process as a `will-navigate` handler. Then assert in this test that the drop was blocked.

**Worth considering**
- The "with a video open" drop test sits under the `ExportPage with no video` suite.
- The Email test's title promises "the cards say where it went", but nothing asserts it. The PR's stated decision that a Balanced copy shows "Ready" on both the Slack · Discord and Email cards is not covered either.

The Library detail test only swaps `/prepare/…` for `/export/…` and is consistent with the new routes.

**Batch 5 of 6.** I reviewed this part's stylesheets, the sidebar test and the deleted Prepare test. One likely bug: `.screen` keeps `overflow: hidden`, which probably clips the \"Pick from Library\" list on Export with no video, even though the drop-zone CSS comment says the list must not be clipped. The clipping estimate comes from reading the CSS, not from rendering the page. The sidebar test has two small gaps: the \"with and without a video\" test only renders one URL, and nothing tests the badge's count for an export in progress. The cases from the deleted Prepare test reappear in `export-page.test.tsx`. Every CSS variable the new stylesheets use is defined in the tokens or `base.css`.

**Batch 6 of 6.** Part 6 has three "consider" findings and no blockers or fixes. It covers routes, the window-size test, stylesheets, the backlog doc and the i18n messages. Things I checked that hold up:
- `routes.ts` adds only literals, with no value imports.
- The legacy redirects keep the query.
- The badge and route claims in the backlog doc match `sidebar.tsx` and `router.tsx`.
- Every `data-tone` value in the stylesheet matches what `export-stage.tsx` emits.
- The removed `library.import*` keys have no readers left.

The three findings:
- **Email copy:** the strings promise an Email copy "fits an attachment", but the Balanced preset has no size cap.
- **Orphaned strings:** several `prepare.*` keys used only by the deleted Prepare components are still in en.json and es.json.
- **Stale comment:** a comment from the removed drop strip is left in `library-page.module.css`.

<details><summary>What the change connects to (16 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- A file from the OS is dropped on the Library window (platform default, no handler) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — Does the app shell or BrowserWindow config elsewhere stop file navigation (e.g. webPreferences or a navigation handler not named will-navigate)? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx`, `apps/kaipu-record/src/renderer/src/app/router.tsx`.
- Pick from Library list opening below its button on Export with no video (`apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:10`) — Does the rendered layout at 900×670, with a long Library, actually push the panel past the bottom of `.screen`? My estimates come from the CSS, not a render. Files that would answer it: `apps/kaipu-record/src/renderer/src/pages/export/export-header.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx`.

**Closed, with the lines they rest on**
- Export screen renders ExportScreen only after the library has loaded; library re-lists gate it again (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117`) — Selection, YouTube resolution and framing reset to the URL/defaults after any re-list. If it fails: Silent loss of the user's choices on screen. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:41-42`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:124-133`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:158`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:212`.
- Probe the selected recording before the stage renders (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:92`) — "Reading…" until the probe resolves; on error, a shareReadError toast and the drop zone. If it fails: probeSource catches errors and returns null (error path is visible). Nothing bounds a probe that never settles, so "Reading…" would stay up until the user navigates away. This is the same as before t… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95-99`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:144-146`.
- Start a copy with an explicit destination (Email over chat's preset) (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252`) — Progress and ready cards use job.destination; email falls to the ICU 'other' branch ("your export"), as the PR says. If it fails: When another export is running, start returns false after the busy toast. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:97-129`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:55-57`, `packages/i18n/messages/en.json:1474`.
- Window-wide file drop on Export imports and opens the video (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:85`) — On Export: import, then navigation to /export/:id?to=. If it fails: Import errors go through useImportVideos toasts. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:36-57`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/main/index.ts:400-403`.
- Legacy /prepare URLs redirect to /export keeping ?to= (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — Old links land on Export. Evidence: `apps/kaipu-record/src/shared/routes.ts:17-24`, `apps/kaipu-record/src/renderer/src/app/router.tsx:68-74`.
- Library stops registering window-wide file drop handling (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Dropping a file on the Library window lets Chromium's default run: the window navigates to the file. If it fails: The renderer navigates away from the app, losing state; there is no will-navigate guard in main. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:48-51`, `apps/kaipu-record/src/main/index.ts:400`.
- Upload-size card with before/after crops for every send-more destination (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:93`) — The crop labelled 'Uploaded at 1080p' is drawn soft and the 1080-wide copy is drawn sharp. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:273`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:280`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:184-187`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:252-257`.
- GitHub size bar drawn against the 10 MB free limit (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:296-307`) — Tag 'fits the 10 MB limit' or 'over …' with the matching tone. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:202-203`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:311`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:323`.
- Recent exports strip reads the export runner and the Library (`apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:34-36`) — Up to three rows: the job in progress with its percentage, then the newest finished copies. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:59`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:71`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`.
- VideoPicker popover (Change video / Pick from Library) (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`) — Export reopens on the picked video and keeps the chosen destination. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`.
- Rail badge moves from Library to the new Export item and adds 1 while an export is running (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`) — The Export rail item shows the count with the label export.railBadge ("# copy in progress or ready"). The Library item has no badge any more. The Library page still outlines unseen copies through unseenCopyIds. If it fails: Everything is in-memory, synchronous state with no async step. The running copy is counted even on /export and while its progress card is shown (finding at line 121). Opening /export marks every unse… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:12-36`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:61-62`, `packages/i18n/messages/en.json:946`, `apps/kaipu-record/src/shared/routes.ts:17-20`.
- Email destination shares chat's 'balanced' preset; tests changed to match (`apps/kaipu-record/src/renderer/src/features/prepare/destinations.test.ts:44-52`) — An existing Balanced file reads as the chat copy wherever destinationOfPreset is used (Recent exports, master copies panel). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:37-45`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:64-73`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:102-107`, `apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65`.
- Video dropped on Export: imported, then Export opens on it with the selected destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:460`) — Navigates to /export/<new>?to=<destination>, and a toast names any extra videos. If it fails: When importVideoFiles rejects, run() catches the error, calls reportError and resets busy, so the drop zone stays usable. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-import-videos.ts:76-115`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:75-88`.
- Old /prepare URLs redirect to /export, keeping the query (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:374`) — Export opens with the ?to= destination selected. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:167-173`.
- Export rail badge: counts the running export plus unseen finished copies; cleared on opening Export or the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44`) — The Export rail item shows a count, with the aria label "N copies in progress or ready". Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44-79`.
- Legacy /prepare and /prepare/:assetId URLs redirect to /export and /export/:assetId (`apps/kaipu-record/src/shared/routes.ts:21`) — The Export screen opens with the same destination preselected. Because the redirect uses `replace`, browser or router Back skips the legacy entry. If it fails: With no assetId it falls back to /export. Both paths stay on the main window preset (window-size.test.ts:21-24). Evidence: `apps/kaipu-record/src/renderer/src/app/router.tsx:72-74`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168-173`, `apps/kaipu-record/src/shared/window-size.test.ts:17-31`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 19 | $0.67 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 12 | $0.57 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 15 | $0.43 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 11 | $0.44 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 19 | $0.50 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 21 | $0.59 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 114 in / 48k out / 2.6M cache read / 341k cache write · $3.20</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=8d2bd023-2bb5-4ccc-a2dc-32247cce3843 -->
