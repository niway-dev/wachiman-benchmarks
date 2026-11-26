# kaipu-bench-wachi-v3#49 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:59:44Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

4 finding(s): 4 to consider; 4 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 has three things worth considering and nothing that blocks the merge.

1. **Drag doesn't mark the copy as seen.** The new Drag handle in "Copies from this original" calls `startFileDrag` but skips `markCopySeen`, which the ready card's drag calls. After someone drags a fresh copy out, the Library still outlines it as unseen.
2. **Estimates can show "…" forever.** When the file can't be read, the destination cards keep the loading ellipsis because the panel can't tell a failed read from one still loading.
3. **A test doesn't check what its name says.** The "Open in Export →" test never checks that the button is absent when there's no export screen.

The PR body says there are seven destinations with Email as its own card, but `DESTINATION_IDS` has six: Email is still part of the chat card ("Slack · Discord · Email"), as the new drag test confirms. The body's own step 4 also lists six.

The rest of the rewired detail page holds up:
- Prepare still opens through the same `openPrepare` → `preparePath` path as before.
- The heavy banner now also shows on a master that has copies.
- The panel is hidden while "Where is it going?" shows.
- Each copy row's picture size is worked out from the original's probe.

**Batch 2 of 2.** I found no defects in the part 2 files: the tests, stylesheets, backlog docs and i18n messages all match the head code. Checks:

- Removed i18n keys: none of `where*`, `copiesEmpty` or `copyProgress*` is referenced anywhere. `sendTo` is kept because the Library card and row still use it.
- New keys: they match their call sites. ETA strings carry no "left", so "Exporting · N% · 2 min left" doesn't repeat the word.
- Removed CSS classes: none are still referenced.
- Backlog doc: it correctly says the code has six destinations, not the design's seven. The PR body's "Seven destinations… Email is its own card" is wrong; the code lists six (`DESTINATION_IDS`).

I left one optional suggestion: a test that "Not now" on a heavy master brings back the "Prepare a light copy →" banner.

<details><summary>What the change connects to (8 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — Main drags the vault file under the copy's title. The copy stays unseen in the ready-copies store, so the Library keeps outlining it. If it fails: startFileDrag returns void (fire-and-forget IPC), so a failed drag shows nothing in the renderer. The same holds for the existing sibling call sites. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-236`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:8-12`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-58`, `apps/kaipu-record/src/shared/types/electron-api.ts:259`.
- Destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Navigates to the Prepare screen with the destination preselected. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`.
- Probe the file for every local recording and show estimates per destination and dimensions per copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The sizes on the cards, the resolution in the metadata line, and "W × H · size" on each copy row. If it fails: If the file can't be read, probeSource returns null, so status is error and probe is null. The page passes only the probe on, so the cards show "…" forever and the copy rows show only the file size.… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:88-95`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`.
- "Not now" hides the destinations panel; ✕ hides the Saved notice (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`) — After "Not now", Export a copy appears among the actions (line 436). After ✕, the masterNote line appears (line 341). If it fails: Nothing is stored, so a remount, Back included, brings the panel back. The PR describes this as intended. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`.
- Click a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router moves to /prepare/:assetId?to=<destination>. The test checks every card's search string. If it fails: Synchronous navigation, so there is no async failure path. Before the probe resolves, each size shows "…". The archive card always shows the file size. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-93`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel disappears and the primary "Export a copy" button appears, which opens Prepare with no ?to=. If it fails: Nothing is stored. The component remounts on Back or when the user leaves, so the panel returns. A param-only change (for example the Source link) reuses the instance, and the dismissal persists only… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517-523`.
- "Saved to your Library" notice and its ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`) — A green status bar above the player. The test at line 868 checks the text, the hide, and the masterNote that replaces it. If it fails: Router Back to the same history entry remounts the page with the same location.state. The notice shows again, in the same way the post-recording card does. This matches the existing card's behaviour. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.
- Drag handle on a copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The operating system drags the vault file. preventDefault suppresses the browser's own drag. If it fails: The call is fire-and-forget ipcRenderer.send. Main validates the id in its handler, and a failure there does not reach the renderer. This matches the existing status-card drag. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 14 | $0.60 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 18 | $0.68 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $1.28</sub>

<!-- wachi:review -->

<!-- agent-review sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=dc21f0fe-ebb5-48a8-bc8d-7567e7e3af1e -->
