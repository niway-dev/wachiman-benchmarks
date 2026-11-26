# kaipu-bench-wachi-v3#54 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T00:07:56Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

4 finding(s): 4 to consider; 3 on their lines. Reply in a comment's thread to answer it.

### Outside the diff

- 🟡📝 **Consider · docs: Stale comment: the page now reads the file for every local recording, not only for the banner and the card (confidence high)** (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:10`): This PR removed the assertion `expect(probe).not.toHaveBeenCalled()` from the "up to 25 MB" test. The page now calls `useSourceProbe` for every preparable recording (`library-detail-page.tsx:142`), and the backlog doc says so (`prepare-screen.md:112-113`). The mock's header comment still says only "The banner and the post-recording card read the file". It should also mention the metadata resolution, the destination estimates and the copies' picture size.

### Summary

**Batch 1 of 2.** Part 1 of 2 has no blockers and nothing at "fix", just two small "consider" items.

The page change does what its comments describe. On a master that has no copies yet, "Where is it going?" shows the destination cards and the "Export a copy" button stays hidden. Once copies exist, the "Copies from this original" panel takes over, and the heavy-to-send banner appears whenever the destinations panel is hidden. The new "Saved to your Library" notice uses the same dismiss-per-visit pattern as the existing post-recording card, so after Back it reappears, just as the card already does.

The two items:
- **Drag doesn't mark the copy as seen** (`master-copies-panel.tsx:174`): the ready card's Drag calls `markCopySeen` before starting the drag; the new handle doesn't. A copy dragged out from the master's page keeps its "just ready" mark and its count in the Library badge until the user opens that copy's own page.
- **Estimates stuck on "…"** (`destinations-panel.tsx:91`): if the file can't be read, every card except Archive shows "…" for good, with nothing to tell the user it failed rather than still loading. The heavy-to-send text in the same panel already handles this case.

The copy rows' picture sizes are right: leaving out the framing doesn't change the width and height for any preset. The updated tests match the new message keys and layout.

**Batch 2 of 2.** Part 2 covers the detail-page tests, the stylesheets, the backlog docs and the en/es messages. The i18n keys this PR removes (`where*`, `copiesEmpty`, `copyProgress*`) are no longer used anywhere in the repo. `sendTo` is still used by the Library card and row. The new ICU plural follows the existing pattern, and en and es have the same keys. The doc's six-versus-seven-destinations note matches `DESTINATION_IDS`, and Prepare returns to the recording without route state, as the doc's walkthrough assumes. There are two small findings. A stale mock comment in the test file says the file is only read for the heavy banner. No test covers a file that can't be read, where every non-archive destination card keeps showing the loading \"…\".

<details><summary>What the change connects to (10 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Click a destination card in "Where is it going?" to open Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The Prepare page opens with the destination preselected. If it fails: If assetId is missing, openPrepare does nothing (library-detail-page.tsx:150), but that page has already returned 'file not found' by then. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`.
- Per-destination size estimate on each card, computed with planCopy and presetForDestination from the probe (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`) — Each card's size text, in amber for send-more destinations and teal for the others. If it fails: If the probe fails it stays null and every card shows '…' with no error message (reported as a finding). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:88-95`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:179-197`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`.
- useSourceProbe now runs for every preparable recording, not only heavy ones or those showing the card (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Dimensions appear in the meta line, plus card estimates and the copies' picture sizes. If it fails: An unusable probe gives status 'error' and probe null: the dimensions are simply left out and the cards show '…'. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:47-66`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:282-289`.
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The native drag works, but the copy's 'just ready' mark and the Library badge stay until its own page is visited. If it fails: startFileDrag returns void (fire and forget over the preload). A failure in main isn't shown in the renderer, the same as in the sibling. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-236`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:54-58`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:93-97`, `apps/kaipu-record/src/shared/types/electron-api.ts:259`.
- Picture size of a destination copy, computed with resolveExportTarget(preset, probe) without a framing (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`) — Shows e.g. '2560 × 1440 · 22 MB' in each copy row. If it fails: With no probe the row shows only the file size. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:478-485`.
- "Saved to your Library" notice, dismissed per location.key; masterNote hidden while it shows (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`) — A green notice over the player. Its body repeats what masterNote says, so hiding masterNote while it shows loses nothing. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-133`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `packages/i18n/messages/en.json:770`, `packages/i18n/messages/en.json:780`.
- Clicking a "Where is it going?" destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489`) — The router moves to /prepare/:assetId?to=<destination>. If it fails: Synchronous navigate; nothing async here. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-494`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and shows Export a copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts and the primary Export a copy button appears in the actions row; the heavy banner shows if the file is heavy. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:101-103`.
- "Saved to your Library" notice on a fresh recording, dismissed with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A green role=status notice above the player. While it shows, the standing masterNote is hidden. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:134-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx:152-153`.
- The page now probes the file for every local recording (resolution meta, destination estimates, copy picture size) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution appears in the meta line and estimates fill the cards once the probe resolves. If it fails: On an unusable result the hook goes to status "error" with probe null. The meta line simply omits the resolution, but the non-archive cards stay on "…" indefinitely with nothing saying the read faile… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:47-66`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 12 | $0.57 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 14 | $0.56 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $1.12</sub>

<!-- wachi:review -->

<!-- agent-review sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=8eaacd67-98cb-4243-bcad-794e281bf932 -->
