# kaipu-bench-wachi-v3#34 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:52:48Z · commit dac8318

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 question for you · 4 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 4 to consider · ⚪ 0 for your information (5) · 4 Should · 1 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`master-copies-panel.tsx:174`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L174) | Drag handle skips markCopySeen, which the other drag site calls |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`destinations-panel.tsx:91`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx#L91) | Size shows "…" forever when the probe fails |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "shows only where there is an export screen" never tests the absent case |
| 🟡 Consider · Could · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | Test overwrites window.electronAPI.startFileDrag without restoring it |
| 🟡 Consider · Should · 🧪 tests | [`library-detail-page.test.tsx:525`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx#L525) | The copy's picture-size assertion accepts any height |

### Questions for you (1)

- [`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) · open question — Probe the source file for every local recording, not only heavy ones: What does useSourceProbe return when probeSource rejects: does it stay null with no visible error? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.

<details><summary>What the change connects to (7 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Probe the source file for every local recording, not only heavy ones (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — What does useSourceProbe return when probeSource rejects: does it stay null with no visible error? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.

**Closed, with the lines they rest on**

- Drag handle on a ready copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The file is dragged into another app; the Library's just-ready flag for that copy is not cleared. If it fails: startFileDrag is fire-and-forget IPC. If main does not start the drag, nothing happens and nothing is shown, the same as the sibling. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:54-55`.
- Probe the source for every local recording (was heavy || showCard only) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Adds the resolution to the metadata line, the per-destination estimates and each copy's picture size. If it fails: On error the probe is null: the metadata omits the resolution, copy rows show only the size, and the destination cards show "…" indefinitely. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`.
- Destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Navigates to Prepare with that destination selected. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`.
- "Not now" and the saved notice's ✕ are held in component state (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`) — On Back to the same entry, the notice (fromRecording is in history state) and the panel come back. This is intended ("until the page is left"). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-133`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`.
- Clicking a destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The route changes to /prepare/:assetId?to=<id>; the tests check all six search strings (test lines 253-266). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-83`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and shows "Export a copy" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — showDestinations turns false, so the panel unmounts and the primary Export a copy button renders (lines 436-441). A heavy master then gets the banner (line 517). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517-523`.
- The "Saved to your Library" notice on a fresh recording, dismissable with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A green status row above the player; ✕ hides it and brings back "This is your original. It never changes.". If it fails: On a remount under the same history entry (Back), the state resets and location.state still carries fromRecording, so the notice reappears. The post-recording card behaves the same way. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:134-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 reviewed: the new DestinationsPanel, the reworked MasterCopiesPanel and its test, the removed strip, and the detail page layout. One fix: the new Drag handle skips `markCopySeen`, which the existing ready-card drag calls, so a dragged copy stays flagged as new in the Library. Smaller points: the destination cards show "…" forever when the probe fails, and two test gaps. The PR body says "seven destinations… Email is its own card", but `DESTINATION_IDS` lists six (Email is part of chat's card).

**Batch 2 of 2.** I found one problem in this part, and it is minor: a "consider" about a weak test. The assertion on the copy's picture size (`library-detail-page.test.tsx:525`) is a regex that accepts any width and height, so a wrong height calculation would still pass. Pinning the exact string would fix that.

Checks that came back clean:

- **Destination count.** `DESTINATION_IDS` lists six destinations. That matches the backlog doc ("the design has seven… the code has six") and the six cards the tests click. The PR body's "Seven destinations… Email is its own card" is wrong about the code, but the body is not a file under review.
- **i18n.** The new keys match between `en.json` and `es.json`, and keeping `sendTo` is consistent with the body's note that the Library cards still use it.
- **Stylesheets and docs.** Nothing to flag.

One question is still open: what the page shows if reading the file fails. The page now reads every local recording's file, and I did not read `useSourceProbe`, so I can't say whether a failed read leaves the destination cards showing "…" for good with no error.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 10 | $0.62 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 8 | $0.52 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 20 in / 11k out / 402k cache read / 104k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.14</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6IjM0NzBhY2U1LWU1ZjQtNDA5NC1iYWYxLTgyMjYxNTViY2Q5NyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjUsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=3470ace5-e5f4-4094-baf1-8226155bcd97 -->
