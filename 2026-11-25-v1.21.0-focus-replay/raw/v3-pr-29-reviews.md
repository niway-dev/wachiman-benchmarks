# kaipu-bench-wachi-v3#29 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:59:42Z · commit dac8318

👮 **Wachiman** · 🟡 **Nothing to fix · 2 to consider** · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 2 to consider · ⚪ 1 for your information (3) · 2 Should · 1 FYI |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (2)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | Test replaces window.electronAPI.startFileDrag and never restores it |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "Open in Export → shows only where…" never checks that the button is absent |

<details><summary>For your information (1)</summary>

| | Where | Finding |
| --- | --- | --- |
| ⚪ Info · FYI · 📝 docs | [`prepare-screen.md:114`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/documentation/src/content/docs/backlog/prepare-screen.md#L114) | PR body says seven destinations; the code and this doc say six |

</details>

<details><summary>What the change connects to (7 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — Main calls event.sender.startDrag with the vault file and the title as the drag name. If it fails: The call is fire-and-forget over ipcRenderer.send, so the renderer never learns about a failure. Main checks the id and name in its own handler. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/shared/types/electron-api.ts:259`, `apps/kaipu-record/src/main/library/index.ts:161`, `apps/kaipu-record/src/main/library/index.ts:173`.
- Destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Route navigation to the Prepare screen. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`.
- Per-destination size estimate from planCopy, and each copy's picture size from resolveExportTarget (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:44`) — Size text on each card, toned by groupOf. If it fails: If the probe never resolves, the cards keep showing "…" and still work, and the copy rows show only the file size. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:179-190`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:62-69`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`.
- "Not now" and the Saved notice ✕ hide UI through component state (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`) — The panel or notice disappears. "Export a copy" and, if the file is heavy, the heavy banner appear. If it fails: On remount, including Back to the same history entry, the state resets. The notice reappears because fromRecording stays in history state, and the destinations panel reappears. This matches the exist… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-133`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- Clicking a destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`) — Route changes to the Prepare screen with the destination selected. If it fails: This is synchronous navigation with no async call. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:150`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36`.
- "Not now" hides the destinations panel and brings back Export a copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292-306`) — The panel disappears and the primary Export a copy button appears among the actions. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`.
- The "Saved to your Library" notice and its dismiss button (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`) — The notice hides and the standing masterNote appears under the metadata. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found nothing that blocks this part; there are two small test findings.

**What I checked:**

- **Page layout:** I traced the new detail-page layout: the title row, the metadata line, the Saved notice, and the switch between the destinations panel and the copies panel.
- **Drag handle:** the new drag in `master-copies-panel.tsx` calls `startFileDrag(id, title)` the same way the export ready card does (`export-status-cards.tsx:235`). The handle only appears when the copy has a local file, so the `copy.id!` is safe.
- **Size estimates:** the destination cards call `planCopy` without framing. That doesn't change the picture size, because Reels and feeds have a fixed canvas.
- **Dismiss state:** "Not now" and the notice's ✕ only live in component state, keyed by recording or arrival, like the existing post-recording card. They come back after a remount or Back, which fits "nothing is stored".

**Test findings:**

- `master-copies-panel.test.tsx:100` sets `window.electronAPI.startFileDrag` and never restores it. The sibling test uses `spyOn` and then `mockRestore`.
- `master-copies-panel.test.tsx:140` is named "shows only where…" but never checks that the button is absent when `onOpenExport` is not passed.

**PR description:**

- **Seven destinations:** the body says the panel lists seven, with Email as its own card. `DESTINATION_IDS` (`destinations.ts:36-43`) has six, and Email is inside the "Slack · Discord · Email" card, as the tests expect. The panel will show six cards.
- **Probe on every visit:** the page now reads the file for every local recording on every visit. The body says this openly.
- **Heavy banner:** it now also shows on an original once "Not now" is clicked or copies exist. Before, it showed only on copies.

**Batch 2 of 2.** I reviewed all 9 files in part 2 of 2 and found no defects in them.

**Tests**

- The page tests match the rendering code in `library-detail-page.tsx`: the title row, the six destination cards, "Not now", the "Saved" notice, the copies count and the Export a copy button.
- The heavy-file test no longer asserts that the file isn't read. That is consistent with the PR now reading the file for every local recording.

**i18n**

- The removed `library.where*`, `copiesEmpty` and `copyProgress*` keys have no remaining references anywhere in the repository.
- `sendTo` stays, because `video-row.tsx` and `video-card.tsx` still use it.

**Documentation**

- `backlog/prepare-screen.md` matches the code, including its note that the code has six destinations.

**One info note:** the PR body says there are seven destinations with Email as its own card. `DESTINATION_IDS` has no email entry, so the description is wrong, not the code or the doc.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 7 | $0.61 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 8 | $0.48 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**PR body says seven destinations; the code and this doc say six (confidence high)** ([`prepare-screen.md:114`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/documentation/src/content/docs/backlog/prepare-screen.md#L114))

The PR body says "Seven destinations, as in the design. Since the export-screen merge, Email is its own card." But `DESTINATION_IDS` (features/prepare/destinations.ts:36) has no email entry: chat covers Slack · Discord · Email. The page test expects six cards (library-detail-page.test.tsx:254-259). This doc (line 114) correctly says the code has six. Only the PR description is wrong.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 20 in / 10k out / 369k cache read / 101k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.09</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6Ijk0OTZhMTNjLTEzMTgtNGI1OS1hODdiLTNlM2RhYjQ3Njk1MyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MiwiaW5mbyI6MX0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjIsImJvZHkiOjEsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=9496a13c-1318-4b59-a87b-3e3dab476953 -->
