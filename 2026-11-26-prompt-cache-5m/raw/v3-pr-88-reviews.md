# kaipu-bench-wachi-v3#88 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:03:50Z · commit dac8318

👮 **Wachiman** · 🟣 **2 questions for you** · 5 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 5 to consider · ⚪ 0 for your information (5) · 2 Should · 3 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (5)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`master-copies-panel.tsx:174`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L174) | Dragging a copy out from the panel doesn't mark it as seen, unlike the ready card's Drag |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | The "shows only where there is an export screen" test checks only the case where the button is present |
| 🟡 Consider · Could · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | The test replaces the shared \`window.electronAPI.startFileDrag\` stub and never restores it |
| 🟡 Consider · Should · 📝 docs | [`prepare-screen.md:183`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/documentation/src/content/docs/backlog/prepare-screen.md#L183) | QA step says to drag the copy's row, but only the Drag button starts the file drag |
| 🟡 Consider · Could · 🧪 tests | [`library-detail-page.test.tsx:301`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx#L301) | Nothing tests a heavy master after "Not now": the hint should move from the panel to the banner |

### Questions for you (2)

- [`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) · open question — The page now probes every local recording, not only heavy ones or those showing the card: Does useSourceProbe surface or log a failed probe, and does it cancel on unmount? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.
- [`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) · open question — Read the file (probe) on every local recording, not only heavy ones: Does useSourceProbe surface a rejected probe, or do the cards stay on "…" with no message? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

<details><summary>What the change connects to (8 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- The page now probes every local recording, not only heavy ones or those showing the card (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Does useSourceProbe surface or log a failed probe, and does it cancel on unmount? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.
- Read the file (probe) on every local recording, not only heavy ones (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Does useSourceProbe surface a rejected probe, or do the cards stay on "…" with no message? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

**Closed, with the lines they rest on**

- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — Main runs a native drag of the vault file. The preload sends the IPC fire-and-forget (ipcRenderer.send), and main checks the id for path separators and '..'. If it fails: The IPC has no reply, so a bad or missing file fails silently in main. The handle only renders when copy.id !== null. The copy stays unseen in the ready-copies store until its page is opened. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161-164`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:54-58`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:95`.
- A destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router navigates to the Prepare screen with the destination preselected. If it fails: Synchronous navigation with no async step. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`.
- "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — showDestinations turns false. The 'Export a copy' button appears, and the heavy banner shows if the recording is heavy. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- "Saved to your Library" notice and its ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`) — The notice shows for a master. While it shows, the masterNote line is hidden (line 341). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`.
- "Open in Export →" in the copies panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:513`) — Navigates to Prepare with nothing preselected. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:122-126`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:437`.
- Click a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router moves to /prepare/<assetId>?to=<destination>; the test checks all six. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-83`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- Dismiss the "Saved to your Library" notice (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:407`) — The notice goes away and the standing "This is your original…" note appears. After a round trip to Prepare and Back, the notice is back. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.
- Drag a copy's Drag handle (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — Main starts a native drag of the real file. Dragging the row's link part instead does the browser's default URL drag. If it fails: startFileDrag is fire-and-forget (ipcRenderer.send / ipcMain.on), so the renderer gets no feedback if main can't resolve the id. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:153-179`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The PR body's claims for this part hold up against the code. "Where is it going?" shows only for a master with no copies and nothing exporting. "Not now" is component state keyed by assetId, so nothing is stored. "Export a copy" waits until the panel is gone, and the heavy hint folds into the panel while it shows. The probe now runs for every local recording. A destination copy's picture size comes from the original's probe and the copy's preset. Framing does not change a fixed canvas's size, so leaving it out is harmless. I found three things to consider. The new Drag handle skips the `markCopySeen` call that the ready card's Drag makes. The Open-in-Export test never checks that the button is missing without the prop. And a test overwrites the shared `startFileDrag` stub instead of spying on it and restoring it.

**Batch 2 of 2.** I found two small issues in this part and nothing that blocks the merge. I only read code; nothing was built or run.

**What checks out**

- The stylesheets match the class names the page and the two panels use.
- The old strip's stylesheet is removed and nothing still references it.
- The new player width cap works because the player frame is always 16:9.
- `en.json` and `es.json` add and remove the same keys. `sendTo` stays because the Library card and row still use it.
- The tests assert what the page now renders, including the `cleanup()` calls added before the second render.

**Findings**

1. **QA step in `prepare-screen.md` (line 183):** it says to drag the copy's *row* into Finder. Only the separate Drag button starts the file drag; the row itself is a link, so dragging it hands over a URL instead of the file.
2. **Missing test:** nothing checks that pressing "Not now" on a heavy master brings back the "Prepare a light copy →" banner.

**Claims in the PR body that don't match the code**

- It says the panel has seven destinations. `DESTINATION_IDS` lists six, and the backlog doc correctly says six.

**Behaviour to know about**

- If the user dismisses the "Saved to your Library" notice, goes to Prepare and comes back with Back, the notice shows again. It works the same way the existing ready card already does, and that code is in part 1.
- I could not confirm what the cards show if reading the file fails. If it never finishes, they may stay on "…" with no message. That question is left open in the contracts.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 11 | $0.51 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 12 | $0.56 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 28 in / 18k out / 645k cache read / 118k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.08</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6ImQ0M2Q4ODI1LTk5ZmYtNDFiYS04ZWU1LWQ0ZjNiZDBjYzMyMyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NSwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjUsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=d43d8825-99ff-41ba-8ee5-d4f3bd0cc323 -->
