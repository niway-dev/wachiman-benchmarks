# kaipu-bench-wachi-v3#66 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T01:34:08Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

5 finding(s): 5 to consider; 5 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 has no blockers or fix-level findings. The page layout, the new DestinationsPanel and the reworked MasterCopiesPanel hold together: the cards, Open in Export and Export a copy all go through `preparePath`, the destinations panel and the copies list never show at the same time, and a copy's picture size computed from the original's probe matches the canvas or tier the copy used.

There are three findings, all at the "consider" level:
- **Drag doesn't mark the copy seen.** The copy panel's Drag skips the `markCopySeen` call that the Ready card's Drag makes, so the Library keeps outlining a copy the user has already dragged out.
- **A failed probe looks like loading forever.** When the file can't be read, the destination cards stay on "…" indefinitely, because the page drops the probe's error status.
- **One test checks only half of its name.** The "Open in Export" test never checks that the button is absent when there is no export screen.

The PR body doesn't match the code in one place. It says "Seven destinations… Email is its own card", but at head `DESTINATION_IDS` lists six, and the tests still expect a combined "Slack · Discord · Email" card.

**Batch 2 of 2.** I reviewed all nine files in part 2 and found no defects in the tests, stylesheets or i18n files. The PR description says the panel has seven destinations, but `DESTINATION_IDS` has six (`destinations.ts:36-43`). The doc correctly says six. Two small doc fixes: the manual QA step says to drag the copy's row, but only the Drag handle starts the file drag; and the metadata line order in the doc leaves out the capture label and the cloud size. Checks: every CSS variable the new styles use is defined; none of the removed i18n keys is used anywhere under `apps/`; and the rewritten tests line up with the page's logic. Removing the old \"file isn't read\" assertion matches the change that now reads every local recording's file.

<details><summary>What the change connects to (9 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Clicking a destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router navigates to the Prepare route with the destination selected. If it fails: This is a synchronous navigate, so there is no async step that can fail. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`.
- The Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — Main starts a native drag of the vault file, named after copy.title. If it fails: startFileDrag returns void (fire-and-forget IPC), so a failure in main is invisible to the renderer. The same is true of the existing call sites. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/renderer/src/features/library/components/gif-viewer.tsx:25-27`, `apps/kaipu-record/src/shared/types/electron-api.ts:254-259`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-58`.
- The page now probes every local recording, not only heavy ones or ones showing the post-recording card (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution in the metadata line, the destination card estimates and each copy's picture size. If it fails: An unusable probe sets status to error with a null probe. The page drops the status, so the cards stay on "…". The hook has no catch on probeSource, so a rejection leaves the state at loading; that i… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- A copy row's picture size is derived from the original's probe and the copy's preset (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`) — The row reads "2560 × 1440 · 22 MB", or just the size when there is no probe. If it fails: With no probe and no gif info the row shows the size only. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:478-504`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:187`.
- "Not now" hides the destinations panel; the Saved notice ✕ dismisses the notice (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`) — The panel goes away and "Export a copy" appears among the actions (line 436). The notice goes away and the master note appears (line 341). If it fails: When the page remounts (Back to it, return from Prepare), "Not now" resets and the panel shows again. On Back the notice comes back too, because location.state still carries fromRecording under the s… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`.
- Click a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:78`) — Navigation to the Prepare page with that destination preselected. The tests assert pathname and search for all six cards. If it fails: This is synchronous navigation, with no async call. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and brings back Export a copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts, and the Export a copy button renders because showDestinations is false. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292-306`.
- Saved notice shown on a fresh recording, dismissed with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — The notice replaces masterNote until dismissed. After that, masterNote appears (tested). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:134-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — The file is dropped into another app. The doc's QA step wrongly says to drag the row. If it fails: This is fire-and-forget IPC. A failure in main is not shown in this component. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-179`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:1`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 14 | $0.58 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 18 | $0.61 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $1.19</sub>

<!-- wachi:review -->

<!-- agent-review sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=5d41c06a-6cfd-494f-8668-1c33c6363e07 -->
