# Wachiman review of branch `bench/pr-465` of pr-465 against origin/replay/pr-465/base (merge-base 13b7ff5), at dac8318

All 14 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

5 finding(s): 5 to consider

## Findings

### 🟡🐛 **Consider · bug: Dragging a copy out doesn't mark it seen, but the ready card's Drag does (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`

The existing Drag in `ExportReadyCard` (`features/status-cards/export-status-cards.tsx:232-235`) calls `markCopySeen(recording.assetId)` before `startFileDrag`. `ready-copies.ts:54-55` describes that as "the user opened the copy or acted on it: nothing left to point at." The new Drag handle in this panel only calls `startFileDrag`. So when a user drags a fresh copy out from "Copies from this original", the ready-copies store still holds it as unseen, and the indicator keeps pointing at a file the user has already sent. Calling `markCopySeen(copy.assetId)` in this `onDragStart` would make the two Drag paths behave the same.

### 🟡🧪 **Consider · tests: Test replaces `window.electronAPI.startFileDrag` and never restores it (confidence high)**

`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100`

This test assigns `window.electronAPI.startFileDrag = vi.fn()` directly, so the mock stays in place for every later test in the file. The sibling test (`export-status-cards.test.tsx:143,152`) uses `vi.spyOn(window.electronAPI, "startFileDrag")` and calls `mockRestore()` at the end. Using the same pattern here keeps the shared stub from `test/setup.ts` intact.

### 🟡🧪 **Consider · tests: "shows only where there is an export screen" never tests the case where it is hidden (confidence high)**

`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140`

The test's name promises "Open in Export →" shows *only* when there is an export screen. It renders with `onOpenExport` and checks the click, but never renders without it to check that the button is absent. The page relies on that absence: it passes `undefined` for a non-preparable item (`library-detail-page.tsx:513`). Adding `renderPanel([copy({})])` with `queryByRole("button", { name: "Open in Export →" })` expected to be null would cover it.

### 🟡🧪 **Consider · tests: No test that a heavy master shows the banner after "Not now" (confidence high)**

`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292`

On a heavy master with no copies, the heavy-to-send hint lives only inside the destinations panel (library-detail-page.tsx:496-503). Once "Not now" hides the panel, the page relies on `heavy && !showDestinations` (library-detail-page.tsx:517) to bring back `HeavyToSendBanner`. The "Not now" test here uses the 20 MB-class `exportedOnlyItem`, and the heavy suite (lines 712-755) never presses "Not now". So nothing covers the hand-off from panel to banner, and a regression would make the heavy hint disappear without anything failing. Suggested fix: add one case in the NIW2-218 suite that clicks "Not now" on `withSize(119_000_000)` and checks for the "Prepare a light copy →" button.

### 🟡📝 **Consider · docs: Doc leaves out the banner that appears after "Not now" on a heavy master (confidence high)**

`apps/documentation/src/content/docs/backlog/prepare-screen.md:111`

The doc says "A heavy copy, or a heavy master with copies, keeps the banner". The code also shows the banner on a heavy master with no copies once "Not now" has hidden the panel, because the condition is `heavy && !showDestinations` (library-detail-page.tsx:517). Suggested fix: add that case so the QA script matches what the owner will see.

## Summary

**Batch 1 of 2.** Part 1 covers the new DestinationsPanel, the reworked MasterCopiesPanel, the reworked detail-page layout, the deleted strip and the panel test. I found no blocker or fix-level defect. These parts check out: the new destination cards and \"Open in Export →\" both navigate to Prepare through the existing `openPrepare`; \"Not now\" hides the panel until the page is left; and the source probe, now read for every preparable recording, degrades cleanly when it is null. Three suggestions: (1) the copy row's Drag skips the `markCopySeen` call that the ready card's Drag makes before dragging, so the copy stays \"unseen\" after the user drags it out; (2) the Drag test overwrites `window.electronAPI.startFileDrag` and never restores it; (3) the \"Open in Export\" test never checks the case where the button should be hidden.

**Batch 2 of 2.** Part 2 holds the tests, stylesheets, docs and messages. The test, CSS and doc changes match library-detail-page.tsx and destinations-panel.tsx. The i18n keys that were removed are no longer referenced; `sendTo` is kept for the Library card and row. I found two "consider" items: no test for a heavy master after "Not now", where the banner takes the panel's place, and the doc does not describe that state. One contract is still open: what happens when the file probe, which now runs on every local recording, fails.

<details><summary>What the change connects to (7 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Probe the file for every local recording, not only heavy ones (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — What does useSourceProbe return when the probe rejects or never resolves? Is the failure reported, or do the cards stay on "…" for good? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

**Closed, with the lines they rest on**
- Clicking a destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The page navigates to the Prepare route with that destination preselected. If it fails: This is synchronous navigation with no async step. Before the probe arrives, size estimates show "…" (the archive card shows its size right away). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- "Not now" dismisses the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel hides. The primary "Export a copy" button appears, and the heavy banner too if the file is heavy. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- The Drag handle on a copy row starts a native file drag through main (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — Main runs a native drag of a hard-linked file with a friendly name. If it fails: `startFileDrag` is fire-and-forget (`ipcRenderer.send`). Main validates the id (rejects path separators and `..`) and returns silently on failure. The handle only renders when `copy.id !== null`. Evidence: `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161-164`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:232-235`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:54-55`.
- The source probe now runs for every preparable recording, not only heavy ones or fresh ones with the ready card (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The dimensions meta and the size estimates appear once the probe resolves. If it fails: If the probe fails or never delivers, `probe` stays null: no dimensions, "…" on the destination cards, and file size only on copy rows. That is a degraded but working display. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:282-289`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`.
- Click a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — Goes to /prepare/:assetId?to=<destination>. The tests at library-detail-page.test.tsx:253-266 assert this for all six destinations. If it fails: Synchronous navigation with no async call. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts and "Export a copy" appears among the actions. If it fails: The state is only component state. Leaving the page or going Back remounts the component and resets it, so the panel shows again, as the comment promises. A lineage link to another recording keeps th… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- The "Saved to your Library" notice and its ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`) — A role=status notice above the player. The test at library-detail-page.test.tsx:868-881 covers it. If it fails: After ✕ and then Back to the same history entry, the component remounts with fresh state and the notice shows again, which matches the card's behaviour. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 7 | $0.59 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 6 | $0.47 |

Cost: $1.06, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 2 call(s), 13 turn(s), 2 min 4 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of dac8318 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171 · 🟡🐛 Consider · bug: Dragging a copy out doesn't mark it seen, but the ready card's Drag does (confidence medium)
   The existing Drag in `ExportReadyCard` (`features/status-cards/export-status-cards.tsx:232-235`) calls `markCopySeen(recording.assetId)` before `startFileDrag`. `ready-copies.ts:54-55` describes that as "the user opened the copy or acted on it: nothing left to point at." The new Drag handle in this panel only calls `startFileDrag`. So when a user drags a fresh copy out from "Copies from this original", the ready-copies store still holds it as unseen, and the indicator keeps pointing at a file the user has already sent. Calling `markCopySeen(copy.assetId)` in this `onDragStart` would make the two Drag paths behave the same.
2. apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · 🟡🧪 Consider · tests: Test replaces `window.electronAPI.startFileDrag` and never restores it (confidence high)
   This test assigns `window.electronAPI.startFileDrag = vi.fn()` directly, so the mock stays in place for every later test in the file. The sibling test (`export-status-cards.test.tsx:143,152`) uses `vi.spyOn(window.electronAPI, "startFileDrag")` and calls `mockRestore()` at the end. Using the same pattern here keeps the shared stub from `test/setup.ts` intact.
3. apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · 🟡🧪 Consider · tests: "shows only where there is an export screen" never tests the case where it is hidden (confidence high)
   The test's name promises "Open in Export →" shows *only* when there is an export screen. It renders with `onOpenExport` and checks the click, but never renders without it to check that the button is absent. The page relies on that absence: it passes `undefined` for a non-preparable item (`library-detail-page.tsx:513`). Adding `renderPanel([copy({})])` with `queryByRole("button", { name: "Open in Export →" })` expected to be null would cover it.
4. apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292 · 🟡🧪 Consider · tests: No test that a heavy master shows the banner after "Not now" (confidence high)
   On a heavy master with no copies, the heavy-to-send hint lives only inside the destinations panel (library-detail-page.tsx:496-503). Once "Not now" hides the panel, the page relies on `heavy && !showDestinations` (library-detail-page.tsx:517) to bring back `HeavyToSendBanner`. The "Not now" test here uses the 20 MB-class `exportedOnlyItem`, and the heavy suite (lines 712-755) never presses "Not now". So nothing covers the hand-off from panel to banner, and a regression would make the heavy hint disappear without anything failing. Suggested fix: add one case in the NIW2-218 suite that clicks "Not now" on `withSize(119_000_000)` and checks for the "Prepare a light copy →" button.
5. apps/documentation/src/content/docs/backlog/prepare-screen.md:111 · 🟡📝 Consider · docs: Doc leaves out the banner that appears after "Not now" on a heavy master (confidence high)
   The doc says "A heavy copy, or a heavy master with copies, keeps the banner". The code also shows the banner on a heavy master with no copies once "Not now" has hidden the panel, because the condition is `heavy && !showDestinations` (library-detail-page.tsx:517). Suggested fix: add that case so the QA script matches what the owner will see.
```
