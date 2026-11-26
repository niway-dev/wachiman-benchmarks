# kaipu-bench-wachi-v3#84 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:27:25Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

7 finding(s): 5 to consider; 5 on their lines. Reply in a comment's thread to answer it.

**Risk map:** low — no risk facts in this change.
**Read first:** `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/where-is-this-going-strip.tsx`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx`.

### For your information

- Nit · ⚪📝 **Info · docs: The PR body says seven destination cards, but the panel renders six (confidence high)** (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73`): The PR notes say "Seven destinations, as in the design … Email is its own card over chat's Balanced preset". The panel maps `DESTINATION_IDS`, which lists six ids (`features/prepare/destinations.ts:36-43`). Email shares the `chat` card ("Slack · Discord · Email", as the test at `master-copies-panel.test.tsx:103` shows).

- Nit · ⚪📝 **Info · docs: PR body says seven destinations; the code and this doc say six (confidence high)** (`apps/documentation/src/content/docs/backlog/prepare-screen.md:114`): The PR's "Notes for review" says "Seven destinations, as in the design. Since the export-screen merge, Email is its own card." `DESTINATION_IDS` (features/prepare/destinations.ts:36-43) has six entries, and Email still shares a card with Slack · Discord ("chat"). This doc line and the test at library-detail-page.test.tsx:253-260 both say six, which is correct. The PR description is the part that's wrong.

### Summary

**Batch 1 of 2.** Part 1 (destinations panel, copies panel, detail page, panel test): the layout and wiring match the description. Destination cards and Open in Export go through `openPrepare`/`preparePath`, and Drag reuses the existing `startFileDrag` IPC without widening it. Four small findings: (1) the Drag handle skips `markCopySeen`, which the other copy-drag call site (the ready status card) calls, so the Library badge keeps counting a copy the user already dragged out. (2) The destination cards show "…" permanently when the file can't be read. (3) The test for when Open in Export shows doesn't check the case where it shouldn't. (4) The PR body claims seven destination cards, but `DESTINATION_IDS` has six.

**Batch 2 of 2.** I found no defects in part 2. The tests, stylesheets, backlog docs and i18n messages match the new detail page:
- The keys removed from en.json and es.json (`where*`, `copiesEmpty`, `copyProgress*`) have no remaining callers.
- `sendTo` is kept, as the PR body says.
- The removed strip stylesheet has no remaining importer.
- The page and panel CSS classes match what the components use.
- The tests check the title row, all six destination cards and their `?to=` values, Not now, the Saved notice and the copies panel.

Two small suggestions and one note:
- **Doc gap (consider):** the doc doesn't mention that a heavy master shows the banner again after "Not now".
- **Missing test (consider):** no page-level test covers a master whose only copy is still exporting.
- **PR description (info):** it claims seven destinations, but the code and the updated doc correctly say six.

<details><summary>What the change connects to (9 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Click a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — The Prepare screen opens with that destination selected. If it fails: Synchronous navigation, with no async step to fail. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`.
- "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel goes away; Export a copy and the heavy banner (if the file is heavy) show instead. If it fails: Nothing is persisted. On Back or remount the state resets and the panel shows again, as the PR notes intend. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- Drag handle starts a native file drag of a copy (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The file is dragged under the copy's title. The Library badge still counts the copy as unseen. If it fails: startFileDrag returns void; a failure in main is invisible to the renderer, the same as the existing call sites. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:54-58`, `apps/kaipu-record/src/shared/types/electron-api.ts:255-259`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-98`.
- Probe the file for every local recording, not only heavy ones or with the card shown (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Shows the resolution in the metadata line, the card size estimates, and each copy's picture size. If it fails: probeSource catches and returns null, which becomes status error and probe null. The resolution and dimensions are silently omitted, and the destination cards show "…" forever. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- Saved notice dismiss (✕) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:407`) — The green notice disappears and the "This is your original" line shows. If it fails: The state is local only. Back to the same history entry remounts the page, so the notice shows again while fromRecording is still in location.state. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-133`.
- A destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Navigates to /prepare/:assetId?to=<id>; the tests check each search string. If it fails: Synchronous navigation, so there is no async failure path. Before the probe resolves, the cards show "…" instead of an estimate. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-96`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and brings back "Export a copy" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel disappears, the primary "Export a copy" button and, on a heavy master, the heavy banner appear. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517-523`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:101-103`.
- "Saved to your Library" notice on a fresh recording, dismissed with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A green role=status notice above the player. After ✕, "This is your original. It never changes." appears under the metadata. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:134-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.
- Drag handle on a copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — The OS drag carries the real file. The browser drag is prevented. If it fails: startFileDrag returns void, so a main-side failure gives the renderer no feedback (same as the existing ready card). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-180`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`, `apps/kaipu-record/src/shared/types/electron-api.ts:259`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:109-110`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 13 | $0.61 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 13 | $0.60 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 36 in / 17k out / 933k cache read / 135k cache write · $1.21</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=8c4b3c05-9375-48a9-b81a-457d934c2658 -->
