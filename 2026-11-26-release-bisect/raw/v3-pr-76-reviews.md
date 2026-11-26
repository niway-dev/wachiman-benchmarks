# kaipu-bench-wachi-v3#76 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:00:32Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

4 finding(s): 3 to consider; 3 on their lines. Reply in a comment's thread to answer it.

**Risk map:** low — no risk facts in this change.
**Read first:** `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/where-is-this-going-strip.tsx`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx`.

### For your information

- Nit · ⚪📝 **Info · docs: Doc and code say six destinations; the PR body says seven (confidence high)** (`apps/documentation/src/content/docs/backlog/prepare-screen.md:114`): This doc says the code has six destinations, and that matches `DESTINATION_IDS` (youtube, vertical, square, github, chat, archive; `features/prepare/destinations.ts:36-43`). The PR description's "Seven destinations, as in the design. … Email is its own card" is wrong, and the test at `library-detail-page.test.tsx:253-260` checks six cards. The doc can stay as it is; only the PR description needs fixing.

### Summary

**Batch 1 of 2.** I found no defects in part 1. Three points are worth considering:
- **Probe runs more often:** the library detail page now reads the source file for every local recording, not only heavy or fresh ones (`library-detail-page.tsx:142`). Worth checking if probing is expensive.
- **Mock not restored:** `master-copies-panel.test.tsx:100` replaces the shared `startFileDrag` stub and leaves it replaced.
- **Half-tested claim:** the "Open in Export" test (`master-copies-panel.test.tsx:140`) checks that the button shows when there is an export screen, but never that it is hidden when there is none.

What I checked against the existing code:
- **Drag:** the new Drag button calls the same native drag as the ready card and the GIF viewer.
- **Picture size:** the size shown for YouTube, vertical and square copies does not depend on the framing, so leaving it out is safe.
- **Hiding and showing the panels:** the dismiss and show/hide logic for the new panels holds up.

**Batch 2 of 2.** I found no defects in this part's tests, stylesheets, docs or messages; the only finding is an `info` note about the PR description.

- **i18n keys:** the removed `library.*` keys (`where*`, `copiesEmpty`, `copyProgress*`) are no longer referenced anywhere in the repository. `sendTo` is still used by `video-card.tsx` and `video-row.tsx`, so keeping it is right. The new keys are present in both `en.json` and `es.json` and are used.
- **Tests:** they match the new page:
  - the title row holds the back link, the title and the master tag;
  - the six destination cards open Prepare with the right `?to=`;
  - "Not now" brings back "Export a copy";
  - the fresh-recording notice and the master note swap places;
  - the copies panel shows the copy's picture size and its Drag handle.
- **Docs:** the backlog doc describes the code correctly, including six destinations.
- **PR description:** it says "Seven destinations… Email is its own card", but `DESTINATION_IDS` lists six, matching the doc and the tests. Only the description needs correcting.
- **Not now:** it lasts only for the visit, as the doc says. It resets when the user leaves the page or comes back with Back.
- **Saved notice:** if the page remounts under the same history entry, the notice appears again. The existing post-recording card behaves the same way, so I did not raise it as a finding.

<details><summary>What the change connects to (7 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Drag a ready copy out of "Copies from this original" (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — Main starts a native drag of a hard-linked, friendly-named file into another app. If it fails: The IPC is fire-and-forget (ipcRenderer.send). Main ignores ids containing path separators or '..'. A failure on main's side is silent: the drag simply does not start. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:232-235`, `apps/kaipu-record/src/renderer/src/features/library/components/gif-viewer.tsx:25-28`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161-164`, `apps/kaipu-record/src/shared/types/electron-api.ts:256-259`.
- Pick a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Navigates to the Prepare/Export screen with that destination chosen. If it fails: Navigation is synchronous. Size estimates show '…' until the probe resolves, and stay that way if it never does. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`.
- "Not now" dismisses the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel hides, and the Export a copy button and the heavy banner show. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- Copy row facts: picture size from resolveExportTarget(preset, probe) (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`) — Shows '2560 × 1440 · 22 MB', or only the size when there is no probe. If it fails: No probe means only the size is shown. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:478-503`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:257-284`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:179-190`.
- Clicking a destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router moves to /prepare/:assetId?to=<destination>. The tests check every card's search string. If it fails: This is synchronous navigation with no async work. If assetId is missing, openPrepare does nothing, but the page has already returned the not-found state by then. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:161-171`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-93`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and brings back "Export a copy" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts and the primary Export a copy button appears in the actions (preparable && !showDestinations). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:101-102`.
- The "Saved to your Library" notice on a fresh recording, dismissed with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A green role=status notice sits above the player. Once it is dismissed, "This is your original. It never changes." appears under the metadata. If it fails: On a remount under the same history entry, the dismissed state is lost while location.state still says fromRecording, so the notice appears again. The existing card behaves the same way. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:134-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 10 | $0.57 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 8 | $0.53 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 22 in / 11k out / 441k cache read / 98k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.10</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=3659e80a-1e42-45d9-b329-96a1cd8b0e95 -->
