# kaipu-bench-wachi-v3#119 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:08:24Z · commit dac8318

👮 **Wachiman** · 🟣 **1 question for you** · 6 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 6 to consider · ⚪ 0 for your information (6) · 2 Should · 4 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (6)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`destinations-panel.tsx:91`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx#L91) | Cards show "…" forever when the file cannot be read |
| 🟡 Consider · Could · ❓ question | [`library-detail-page.tsx:190`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L190) | Does "Where is it going?" flash back when an export finishes? |
| 🟡 Consider · Could · ⚡ perf | [`library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) | The file is now probed on every preparable recording page, not only when needed |
| 🟡 Consider · Could · 🐛 bug | [`master-copies-panel.tsx:109`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L109) | A copy's picture size is recomputed from the master's probe, not read from the copy |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | Test title claims the button is omitted without an export screen, but only the click is tested |
| 🟡 Consider · Should · 📝 docs | [`prepare-screen.md:183`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/documentation/src/content/docs/backlog/prepare-screen.md#L183) | Validation steps say to drag the copy's row, but only the Drag handle starts a drag |

### Questions for you (1)

- [`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:143-148`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L143) · open question — Panel visibility switches on `hasCopies` when an export finishes in the background: Is the finished copy already in `videos` (via broadcastLibraryChanged during recordingFinalize) before the runner's `running` becomes null? Files that would answer it: `apps/kaipu-record/src/main/recording/index.ts`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts`.

<details><summary>What the change connects to (7 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Panel visibility switches on `hasCopies` when an export finishes in the background (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:143-148`) — Is the finished copy already in `videos` (via broadcastLibraryChanged during recordingFinalize) before the runner's `running` becomes null? Files that would answer it: `apps/kaipu-record/src/main/recording/index.ts`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts`.

**Closed, with the lines they rest on**

- Drag handle on a ready copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-180`) — A native drag of the real file, named after the copy's title, into another app. The button is rendered only when `copy.id !== null`. If it fails: If the poster thumbnail is missing, main returns silently (`icon.isEmpty()`) and the drag does nothing with no error shown. A rejection in main is only logged to the console. This is existing behavio… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-175`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-236`, `apps/kaipu-record/src/main/library/index.ts:161-174`.
- A destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-494`) — Navigation to /prepare/:assetId?to=<destination>. The panel hides when a copy or running export exists (`hasCopies`) or after "Not now". The dismissal is keyed by assetId in page state, so it resets when the page is left and reopened. If it fails: No async work. Card sizes depend on the probe, which stays null ("…") if the read fails; see the finding on destinations-panel.tsx:91. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`.
- The page always probes the recording file and feeds the result to the metadata line, the cards and the copy rows (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution appears in the metadata line once read; the card sizes and the copy dimensions fill in. If it fails: A rejected or unusable probe leaves `probe` null: no resolution, "…" on the cards, size-only rows in the copies panel. Nothing tells the user the read failed. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:282-289`.
- Destination card click on "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The user lands on Prepare with that destination selected. The test walks all six cards and checks the resulting search string. If it fails: An unknown `to` value is ignored by Prepare (`isDestinationId` guard), so it falls back to the default destination. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:8-11`, `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx:70-71`.
- "Not now" hides the destinations panel and brings back "Export a copy" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel disappears and the primary button shows in the actions row. After Back, the component remounts and the question returns. If it fails: None. The state is keyed by assetId, so a lingering value cannot hide another recording's panel. The same mounted page going A→B→A through the lineage links keeps A dismissed. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- The page now probes the file for every local recording, not only a heavy one (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution joins the metadata line once the probe resolves. The cards show "…" until then. If it fails: If the probe errors, the hook returns `probe: null`. The cards then keep showing "…" and the resolution is omitted, with no error shown. The cards stay clickable. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:282-289`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-43`.
- Drag handle on a copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — The real file is dragged into another app. The button is not rendered when `copy.id` is null. If it fails: The channel is fire-and-forget (`ipcRenderer.send`), so a main-side failure is silent. That matches the existing ready card. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-179`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found no blockers in part 1. The restructure is coherent and the page tests cover the new flows, but nothing was run: this was a read-only review. I read the five files in full, plus `useSourceProbe`, the `startFileDrag` main handler and its other callers, `planCopy` and `resolveExportTarget`. I left five items at \"consider\" severity. The destination cards show \"…\" indefinitely when the probe fails. The page now probes the file on every preparable recording page. Copy dimensions are recomputed from the master's probe and not read from the copy. The destinations panel may flash back when an export finishes, which I could not confirm without tracing main's finalize broadcast. The \"Open in Export →\" test never checks the case where the prop is omitted. The Drag handle follows the same IPC path as the Ready card and GIF viewer. The deleted `where-is-this-going-strip.tsx` leaves no importers in this part; I did not search other parts.

**Batch 2 of 2.** Part 2 holds the recording-page test updates, the new `destinations-panel` stylesheet, the restyled copies panel, the deleted strip stylesheet, the page layout CSS, two docs pages and the en/es messages. I found nothing to fix. The removed i18n keys have no remaining users, and `sendTo` is kept because the Library card and row still use it. Every CSS token the new styles use is defined. The six `?to=` values the tests expect are accepted by Prepare. The one finding is a docs wording point: the manual check says to drag the copy's row, but only the Drag button is draggable. I wrote four contract entries for the new actions (destination card, Not now, always-on probe, Drag handle) and all four are closed.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 13 | $0.34 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 19 | $0.32 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 30 in / 21k out / 825k cache read / 148k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.66</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6IjgxMjYwNzUyLWM4NzItNDEzNy1hNGY5LWFhNDE4MmYyNTBmMSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NiwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjYsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=81260752-c872-4137-a4f9-aa4182f250f1 -->
