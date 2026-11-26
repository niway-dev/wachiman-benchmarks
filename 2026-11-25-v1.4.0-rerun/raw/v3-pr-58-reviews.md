# kaipu-bench-wachi-v3#58 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T00:07:40Z · commit e45c845

👮 **Wachiman** · review of the whole pull request, at `e45c845`: all 31 files reviewed.

2 finding(s): 2 to consider; 2 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 has two findings, both at "consider". First, the Library's new Ready to upload card does not call `markCopySeen` on Show in Finder or on drag. The ready toast does, and so does the ready-copies contract, so a copy the user already dragged out keeps its outline and still counts in the "copy ready" chip. Second, leaving the Library retires every ready card, including cards that never rendered because the Library was in list view or the filters hid them. The fingerprint fix (split on '#'), the session-wide minimize state and the move of the export cards to the bottom right all match what the PR describes.

**Batch 2 of 2.** I found nothing to flag in this part: four stylesheets, three backlog docs and the en/es message files.

- **Docs:** I checked the claims in the new backlog doc against the code, and they hold:
  - The widget's minimized state is kept per session in sessionStorage.
  - An error still shows as a full card, even when the widget is minimized.
  - Leaving the Library retires the cards; the sidebar watches the route for this, not the page's unmount.
  - ✕ brings the regular card back, still outlined as unseen.
  - Ready cards show newest first, only for copies the current filters show, and only in grid view.
  - The "#" fingerprint comparison in `copyDestinationOf` works as described.
- **Layout:** The Library grid always has 3 columns (`repeat(3, 1fr)`), so `span 2` fits. The export stack sits 40 px from the bottom, which clears the 28 px status bar. The pill and the status cards are still clickable, because each turns pointer-events back on inside the stack that turns them off.
- **Messages:** The removed keys (`hide`, `readyDragToUpload`) are no longer used anywhere in the app. `destinationTag` has no `archive` case on purpose: an archive copy falls to `other`, which reads "Archive copy". The tag colours match `destination-logo.module.css`.

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Show in Finder / drag the file from the Library's Ready to upload card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — The card and the unseen outline/chip stay after the user acts on the copy. If it fails: revealLocalRecording is fire-and-forget (void); a rejection is silent, the same as the sibling. startFileDrag is a send with no reply. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-295`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:9-13`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:76-98`.
- Retire ready cards when the route leaves the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:99-103`) — The next visit opens on the plain grid, and copies keep the unseen outline. If it fails: Cards hidden by list view or by filters are retired without ever being shown. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:93-100`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:126-133`.
- Minimize the export widget to a pill (session-wide, sessionStorage) (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:25-35`) — While minimized, the pill shows instead of the card; clicking it expands the card again. If it fails: If storage throws, the choice is kept in memory only. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:34-55`.
- Read a copy's destination back from the sidecar fingerprint (`apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:13-17`) — Destination tags appear on grid cards and in the Copies from this master panel. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:185-188`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-reuse.ts:18`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:98-103`.
- Minimize the export widget to a pill (− on the progress card) and expand it again (click the pill) (`apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:76`) — The pill renders inside `.exportStack` (fixed, bottom right, pointer-events none) and sets pointer-events:auto itself, so it stays clickable; StatusCard also sets pointer-events:auto. If it fails: sessionStorage unavailable: read() returns false and the setter keeps the choice in memory, so the widget only fails to persist across a reload. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:40-52`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:152`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:203`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.tsx:27-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-card.module.css:5`.
- The 'Ready to upload' card leads the Library grid across two columns; ✕ dismisses it, leaving the Library retires all cards (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:4`) — The grid is a fixed 3-column grid, so `grid-column: span 2` always fits; list view is unchanged as the doc states. Evidence: `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:126-133`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:407-445`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:366-371`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:87-105`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:96-104`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 9 | $0.44 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 20 | $0.48 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $0.92</sub>

<!-- wachi:review -->

<!-- agent-review sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:attempt id=20c4022d-8e8d-45b9-843c-2ae8c13f9cf6 -->
