# kaipu-bench-wachi-v3#82 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:27:26Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

4 finding(s): 4 to consider; 4 on their lines. Reply in a comment's thread to answer it.

**Risk map:** low — no risk facts in this change.
**Read first:** `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/where-is-this-going-strip.tsx`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx`.

### Summary

**Batch 1 of 2.** Part 1 holds the new DestinationsPanel, the reworked MasterCopiesPanel and its test, the removed strip, and the library detail page. The layout and state logic match what the PR describes. Card clicks and Open in Export go through the existing openPrepare/preparePath path. Copy picture sizes come from resolveExportTarget; leaving out framing is safe because canvas presets have a fixed size.

I found three minor issues, all at "consider":
- **Drag skips `markCopySeen`.** The new Drag handle doesn't call it, but the ready card's identical drag does. A copy dragged out from the original's page keeps counting toward the Library badge.
- **Estimates hang on a failed read.** The page discards the probe's error status, so when the file can't be read the destination cards show "…" forever.
- **Open in Export test is half-done.** It never checks that the button is absent when `onOpenExport` is omitted.

One claim in the PR body doesn't hold: it says there are seven destinations with Email as its own card. `DESTINATION_IDS` in `destinations.ts` has six, and Email is still part of the chat card ("Slack · Discord · Email"), as the test asserts.

**Batch 2 of 2.** Part 2 covers the page tests, the stylesheets, the docs and the messages. They match the new layout in `library-detail-page.tsx`, `destinations-panel.tsx` and `master-copies-panel.tsx`.

- **Messages:** every removed `library.*` key (`where*`, `copiesEmpty`, `copyProgress*`) is unused in the repository. `sendTo` is still used by the Library card and row, and en.json and es.json stay in step with each other.
- **Stylesheets:** every CSS variable the new styles use is defined in `packages/tokens/css/tokens.css` or `base.css`.
- **Tests:** they assert what their names say. That covers the six destination cards and their `?to=` values, the amber/teal size tones, "Not now" bringing back Export a copy, the "Saved" notice hiding the master note until ✕, and the copy's facts line and Drag handle. The page test checks that the Drag handle is visible, not that dragging it calls `startFileDrag`.
- **Docs:** the backlog doc says six destinations, matching `DESTINATION_IDS` in the code. The PR body's "Seven destinations, as in the design" is wrong; the doc is right.

One finding: a QA step in the doc (`prepare-screen.md:183`) says to drag the copy's row, but only the Drag handle starts the file drag.

<details><summary>What the change connects to (8 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- "Not now" hides the destinations panel, keyed by assetId in component state (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`) — Does the route keep LibraryDetailPage mounted when :assetId changes? If it does, dismissing on A, opening a copy and returning to A leaves the panel hidden. The comment promises "until the page is left". Files that would answer it: `apps/kaipu-record/src/renderer/src/app.tsx`, `apps/kaipu-record/src/renderer/src/routes.ts`.

**Closed, with the lines they rest on**
- Clicking a destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The Prepare route opens with the destination preselected. If it fails: Synchronous navigation, so there is no async failure. openPrepare is a no-op when assetId is missing, which can't happen after the !assetId early return. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:161`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`.
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The OS drag carries the copy file under its title. The copy stays in the ready-copies list and keeps counting toward the Library badge. If it fails: startFileDrag is fire-and-forget. If main refuses it, nothing happens and nothing is shown, the same as the siblings. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/renderer/src/features/library/components/gif-viewer.tsx:25-27`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-58`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-98`.
- The page now probes the file of every local recording, not only heavy ones or ones with the card (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution shows in the meta line, along with the destination estimates and each copy's picture size. If it fails: probeSource catches every error and returns null. useSourceProbe then sets status "error", but the page keeps only .probe. The resolution never appears, copies show only their file size, and the dest… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- Copy rows show picture size derived from the source probe and the copy's preset (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`) — The row reads "2560 × 1440 · 22 MB". A GIF uses its stored gif dimensions. If it fails: With no probe, the row shows only the file size. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:478-517`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:529-561`.
- Clicking a destination card in "Where is it going?" opens Prepare on that destination (asserted by the test) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`) — The router moves to /prepare/<assetId>?to=<destination>. The test checks the pathname and the search for all six cards. If it fails: This is synchronous navigation with no async call. The card sizes wait for useSourceProbe and show "…" until it arrives, so a failed probe leaves "…" showing but the cards still work. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-95`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`.
- "Not now" hides the destinations panel and brings back Export a copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292-306`) — The panel unmounts and the primary Export a copy button appears in the actions. On a heavy master, the heavy banner returns because `heavy && !showDestinations` is now true. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517-523`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:101-102`.
- The Drag handle on a copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:526-528`) — The OS drag carries the real file. The page test only checks that the button is visible, not that dragging calls the IPC. If it fails: startFileDrag returns nothing to the renderer, so a failure in main is silent here, just as it is for the existing ready card. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-179`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`.
- The "Saved to your Library" notice shows when location.state.fromRecording is set, until ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`) — A green role=status notice sits above the player, and masterNote stays hidden until the notice is dismissed. If it fails: Browser Back to the same history entry remounts the page with the same location.state, and the dismissal is lost with the component state, so the notice comes back. This is the same as the existing p… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:134-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 14 | $0.65 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 15 | $0.59 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 40 in / 19k out / 1.0M cache read / 129k cache write · $1.24</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=f957759f-9fbf-42bf-b376-d3a859ceb455 -->
