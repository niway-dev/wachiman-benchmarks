# kaipu-bench-wachi-v3#114 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:07:35Z · commit dac8318

👮 **Wachiman** · 🟡 **Nothing to fix · 4 to consider** · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 4 to consider · ⚪ 0 for your information (4) · 1 Should · 3 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:189`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L189) | "Where is it going?" can flash back between the export finishing and the re-list |
| 🟡 Consider · Could · 🐛 bug | [`destinations-panel.tsx:91`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx#L91) | A failed probe leaves "…" on every card for good |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | The drag test overwrites the global \`startFileDrag\` and never restores it |
| 🟡 Consider · Could · 🧪 tests | [`master-copies-panel.test.tsx:74`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L74) | The GitHub copy's picture size is not pinned |

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Drag handle on a ready copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164`) — The OS drag starts with the copy's file under its title. A copy with no local file (`id === null`) gets no button. If it fails: If the poster is missing, main returns silently and no drag starts. On any other error main logs it and the user sees nothing. The same happens on the existing paths. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:228-240`, `apps/kaipu-record/src/main/library/index.ts:161-175`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-180`.
- A destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Prepare opens with the destination preselected. If it fails: The `destinationsDismissedFor` state is local, so it is lost on remount or Back (the panel returns), as the PR describes. The synchronous navigation has no failure path. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:8-11`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`.
- The page now probes every local recording, not only heavy ones (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution in the metadata line, the card sizes, and the copies' picture sizes appear once the read finishes. Until then the cards show "…" and the metadata omits the resolution. If it fails: A rejected or unusable probe becomes `status: error` with `probe: null`, so every dependent element silently falls back to no resolution and "…" on the cards (see the finding on destinations-panel.ts… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:29-31`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`.
- Destination card on 'Where is it going?' opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — The app navigates to /prepare/:assetId with ?to=<destination> (or no query for 'Export a copy'). The page test asserts all six destinations and the empty case. If it fails: The navigation is synchronous and does nothing async. When assetId is missing it does nothing, but the page has already shown 'File not found' in that case. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:161`.
- Drag handle on each copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — A real file is dragged into another app. The button only renders when copy.id is not null, so a cloud-only copy has no handle. If it fails: startFileDrag is called without await or catch. A failure in main would be silent, but the page test only checks that the button is visible and not the IPC. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-180`.
- The page probes the file whenever it shows a local recording, not only when it is heavy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution joins the metadata line, the destination cards and copy rows show picture sizes and estimates, and the cards show '…' until the probe returns. If it fails: If the probe fails, probe stays null: no resolution, estimates stay '…', and copy rows show only the file size. The page still works. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:112-113`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The change is sound overall. The new native-drag call matches the existing status-card and GIF paths, and `preparePath` is reused unchanged. I found four things, none blocking. The destinations panel can reappear briefly when an export finishes, until the re-list returns, because `hasCopies` flips back to false. A recording that can't be probed leaves \"…\" on six of the seven destination cards. The drag test overwrites `window.electronAPI.startFileDrag` and never restores it. The GitHub row's picture size isn't pinned in the panel test. The PR body says \"seven destinations\", but `DESTINATION_IDS` has six. The part 2 docs and messages may repeat the seven.

**Batch 2 of 2.** I found nothing to flag in this part; this is a read-only review and I did not run the tests. The CSS and message changes match the components that use them. The CSS variables the new stylesheets use are defined, either in the app's `base.css` or in `packages/tokens`. The removed `where-is-this-going-strip` keys (`whereTitle`, `copiesEmpty`, `copyProgress` and the rest) are no longer referenced. The `sendTo` key is still used by `video-card.tsx` and `video-row.tsx`. The test changes assert the new behaviour: title row, destination cards, 'Not now', saved notice, copies grid. The docs match the code on layout, the six destinations, the banner rule and the file now being read on every local recording. Opening a recording via browser Back would show the saved notice again, since `fromRecording` stays in the history entry. The Prepare screen's own back and 'started' paths navigate without that state, and the post-recording card already worked this way.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 16 | $0.31 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 19 | $0.31 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 40 in / 19k out / 1.1M cache read / 131k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.62</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6IjQ5OTIxOWRlLWE1ZGItNDk1Ni05ODQ3LTM4OTdjMzFhODAzZSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=499219de-a5db-4956-9847-3897c31a803e -->
