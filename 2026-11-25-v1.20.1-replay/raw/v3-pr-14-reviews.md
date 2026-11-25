# kaipu-bench-wachi-v3#14 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:54:19Z · commit dac8318

👮 **Wachiman** · 🟣 **2 questions for you** · 3 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 1 Should · 2 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · ❓ question | [`master-copies-panel.tsx:171`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L171) | Drag skips the markCopySeen step the ready card's drag takes |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "shows only where…" test never checks the case where the button is absent |
| 🟡 Consider · Could · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | Test overwrites window.electronAPI.startFileDrag and never restores it |

### Questions for you (2)

- [`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L171) · open question — Drag handle starts a native file drag of a copy: Does skipping markCopySeen leave a dragged copy flagged as unseen? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx`.
- [`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L171) · open question — The Drag handle on a copy row starts a native file drag: What does main's startFileDrag handler do when the copy's vault file is missing? Files that would answer it: `apps/kaipu-record/src/main`.

<details><summary>What the change connects to (6 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Drag handle starts a native file drag of a copy (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — Does skipping markCopySeen leave a dragged copy flagged as unseen? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx`.
- The Drag handle on a copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — What does main's startFileDrag handler do when the copy's vault file is missing? Files that would answer it: `apps/kaipu-record/src/main`.

**Closed, with the lines they rest on**

- Destination card click opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Prepare screen opens with the destination selected. If it fails: No async: navigate only; it does nothing when assetId is missing, which can't happen past the early return. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`.
- "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — Panel disappears and "Export a copy" appears among the actions (line 436); the heavy banner takes over the hint (line 517). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- Probe the source file for every local recording page, not only heavy ones or fresh recordings (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Dimensions in the metadata line, estimates on the destination cards and picture sizes on copy rows; until the probe returns they show nothing or an ellipsis. If it fails: With a null probe, dimensions are hidden, the cards show an ellipsis and the rows show only the file size. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:282-289`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:106-113`.
- A destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router goes to /prepare/:assetId?to=<id>. The tests check all six ids. If it fails: Synchronous navigation with no async work. Estimates show "…" until the probe resolves (the archive card shows its size right away). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-91`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and brings back Export a copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts and the Export a copy button renders (it is gated on !showDestinations). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292-306`.
- "Saved to your Library" notice on a fresh recording, dismissed with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A role=status banner. After ✕, the masterNote line appears. If it fails: location.state survives Back to the same entry, so on remount the notice shows again, the same as the existing card. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:134-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 reworks the recording detail page: the title gets its own row, a DestinationsPanel replaces the old strip, and the copies panel gets picture sizes, a progress bar, Drag and "Open in Export". The page wiring holds up. showDestinations/hasCopies switch cleanly between the two panels, and the heavy-to-send banner moves to wherever the panel isn't showing. openPrepare is reached the same way the existing callers reach it. The copy dimensions come from resolveExportTarget without framing, which is harmless: framing doesn't change the canvas size. Three minor points: the new Drag handler skips the markCopySeen step that the ready card's drag takes (asked as a question), one test's name promises a negative case it never checks, and one test overwrites window.electronAPI.startFileDrag without restoring it.

**Batch 2 of 2.** I found no defects in the tests, stylesheets, docs or messages of part 2.

- **Tests:** they follow the new layout:
  - The title shares its row with the way back and the tag.
  - Each of the six destination cards opens `?to=<id>` and shows its tone.
  - "Not now" hides the panel and brings back "Export a copy".
  - The Saved notice is followed through ✕.
- **Messages:** none of the removed `library.*` keys (`where*`, `copiesEmpty`, `copyProgress*`) is still used under `apps/`. The ETA strings ("N min") combine with "… left" without repeating a word.
- **Docs:** the backlog doc's statement that the code has six destinations matches `DESTINATION_IDS`.
- **PR body:** it contradicts the code once. It claims seven destinations, with Email as its own card. `destinations.ts` lists six groups' worth (youtube, vertical, square, github, chat, archive), and so does the test at `library-detail-page.test.tsx:253-260`, so the description needs that note fixed.
- **Open question:** I did not read main's `startFileDrag` handler, so what the Drag handle does when the copy's file is missing is unconfirmed.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 9 | $0.61 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 9 | $0.53 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 24 in / 11k out / 499k cache read / 102k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.14</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6IjljMDQxMGJjLTAzMGYtNGQ0MC05YjE2LWFjMDU5MDU2NGY1NiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=9c0410bc-030f-4d40-9b16-ac0590564f56 -->
