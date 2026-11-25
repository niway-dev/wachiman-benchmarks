# kaipu-bench-wachi-v3#24 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:59:09Z · commit dac8318

👮 **Wachiman** · 🟣 **1 question for you** · 5 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 5 to consider · ⚪ 0 for your information (5) · 2 Should · 3 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (5)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`master-copies-panel.tsx:174`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L174) | Drag here skips markCopySeen, unlike the ready card's Drag |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "shows only where there is an export screen" never checks the case where it's hidden |
| 🟡 Consider · Could · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | Test overwrites window.electronAPI.startFileDrag and never restores it |
| 🟡 Consider · Should · 🧪 tests | [`library-detail-page.test.tsx:269`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx#L269) | No test covers a failed probe: the destination cards would show "…" for good |
| 🟡 Consider · Could · 📝 docs | [`prepare-screen.md:184`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/documentation/src/content/docs/backlog/prepare-screen.md#L184) | QA step says to drag the copy's row, but the drag starts from the Drag handle |

### Questions for you (1)

- [`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) · open question — The page now probes every preparable recording, not only heavy ones: Does useSourceProbe surface or swallow probe errors, and does it cancel when the id changes? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

<details><summary>What the change connects to (4 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- The page now probes every preparable recording, not only heavy ones (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Does useSourceProbe surface or swallow probe errors, and does it cancel when the id changes? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

**Closed, with the lines they rest on**

- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — Main runs an OS file drag of the copy's file, named after its title; the button only renders when copy.id !== null. If it fails: startFileDrag returns void (fire-and-forget IPC), so a failure in main is silent here, the same as the sibling. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:54-58`, `apps/kaipu-record/src/shared/types/electron-api.ts:259`.
- Destination card opens Prepare on that destination; Not now hides the panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`) — Navigates to Prepare. After Not now, the Export a copy button and the heavy banner show (lines 436, 517). If it fails: Synchronous navigation only. Without a probe, the cards show … in place of their estimates. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`.
- Clicking a "Where is it going?" destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router moves to /prepare/:assetId?to=…, and the test checks pathname and search for all six DESTINATION_IDS. If it fails: Navigation is synchronous, so there is no async failure. The panel's sizes depend on useSourceProbe. When the read fails, status is "error" with probe null, which the page ignores, so the non-archive… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-91`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" and the "Saved to your Library" ✕ hide the panel and the notice; the dismissal lives in component state (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`) — The panel goes away and "Export a copy" appears (library-detail-page.tsx:436). The masterNote comes back once the notice is hidden (library-detail-page.tsx:341). If it fails: Nothing is stored, so after a remount (Back, leaving and coming back) the panel and, for a fromRecording entry, the notice come back. The PR states this is intended. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292-306`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 replaces the strip with a destinations panel, adds a Drag handle and picture sizes to the copies panel, and reorganizes the detail page. The only behavioural difference from existing code: the new Drag handle skips `markCopySeen`, which the ready card's identical drag calls. The other two findings are test gaps: the Open in Export test never checks that the button is hidden without a handler, and one test replaces `window.electronAPI.startFileDrag` without restoring it.

**Batch 2 of 2.** Part 2 covers the tests, stylesheets, docs and i18n messages. The i18n removals are clean: no code still uses `whereTitle`, `whereBody`, `whereChipAria`, `copiesEmpty` or `copyProgress*`, and `sendTo` stays because `video-card.tsx` and `video-row.tsx` still use it. The en and es key sets match.

The test file was updated in step with the new layout. It now covers six destination cards, Not now, the Saved notice, the copies count and the Drag handle. Two `cleanup()` calls were added before re-rendering, which fixes duplicate-DOM queries.

The backlog doc correctly says the code has six destinations (`DESTINATION_IDS` in `destinations.ts:36-43`). The PR body is wrong on this point: it says seven, with Email as its own card.

Findings:

- **Missing test (consider):** no test covers a failed probe. Because the page now reads the file for every local recording, a failed read leaves every non-archive card on "…" with nothing telling the user why.
- **QA step (consider):** one step in the doc says to drag the copy's row, but the drag starts from the separate Drag handle.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 8 | $0.54 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 8 | $0.52 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 22 in / 11k out / 422k cache read / 95k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.06</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6ImUwMzViYzA3LWM1MWMtNGJjYy1hYTBiLWQ1OTk5ZDljNDkyOCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NSwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjUsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=e035bc07-c51c-4bcc-aa0b-d5999d9c4928 -->
