# kaipu-bench-wachi-v3#86 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:02:41Z · commit dac8318

👮 **Wachiman** · 🟣 **2 questions for you** · 3 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 3 Should |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`destinations-panel.tsx:91`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx#L91) | An unreadable file leaves every estimate on "…" for good |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "shows only where there is an export screen" never checks the missing case |
| 🟡 Consider · Should · 📝 docs | [`prepare-screen.md:184`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/documentation/src/content/docs/backlog/prepare-screen.md#L184) | Validation step says to drag the copy's row, but only the Drag handle starts a file drag |

### Questions for you (2)

- [`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L171) · open question — The Drag handle on a ready copy starts a native file drag: What does startFileDrag do in main when the copy's vault file is missing, and does the user see anything? Files that would answer it: `apps/kaipu-record/src/preload/index.ts`, `apps/kaipu-record/src/main`.
- [`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) · open question — The page now probes the file for every local recording, not only heavy ones: Does useSourceProbe surface a probe failure, or do the cards stay at "…" with no message? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

<details><summary>What the change connects to (7 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- The Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — What does startFileDrag do in main when the copy's vault file is missing, and does the user see anything? Files that would answer it: `apps/kaipu-record/src/preload/index.ts`, `apps/kaipu-record/src/main`.
- The page now probes the file for every local recording, not only heavy ones (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Does useSourceProbe surface a probe failure, or do the cards stay at "…" with no message? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

**Closed, with the lines they rest on**

- Pick a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — The Prepare page opens with that destination chosen. If it fails: The estimates need the probe. On a probe failure they stay at "…" (reported as a finding), but navigation still works. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`.
- "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel disappears and the primary Export a copy button shows in the actions row. The heavy banner shows instead of the folded note. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The OS drag carries the real file into another app. If it fails: startFileDrag is fire-and-forget (void), the same as its siblings. The handle is gated on a local id. Evidence: `apps/kaipu-record/src/renderer/src/features/library/components/gif-viewer.tsx:25-28`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`, `apps/kaipu-record/src/shared/types/electron-api.ts:259`.
- The source probe is now read on every preparable recording page, not only for heavy files or the card (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution appears in the meta line, plus the estimates on destination cards and the picture size of each copy. If it fails: probeSource never rejects (it catches to null). On failure the meta dimensions are simply absent and the copy rows show only the file size. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:47-63`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:282-289`.
- A copy row shows its picture size, computed from the page's probe and the copy's preset (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`) — The row reads "2560 × 1440 · 22 MB". If it fails: Without a probe, the row shows only the size. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:478-503`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:187`.
- A destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The route changes to /prepare/:assetId?to=<id>. The tests check the search string for all six cards. If it fails: This is plain client navigation with no async call. openPrepare is a no-op when assetId is missing, but the page never renders the panel in that case. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-83`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and brings back Export a copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — showDestinations turns false, so the panel unmounts and the primary Export a copy button renders. If the recording is heavy, the heavy banner also shows. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517-523`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** In this part (part 1 of 2), the recording page's \"Where is this going?\" strip becomes a six-card destinations panel that shows each card's size estimate. The copies panel becomes a grid with picture sizes, a Drag handle and \"Open in Export →\", and the page layout is reorganised. I found no blocking defects. Two \"consider\" findings:\n\n- **Estimates stuck on \"…\":** when the file can't be read, five of the six destination cards keep a loading ellipsis that never resolves. The probe hook returns null both while loading and after a failure, so the panel can't tell them apart. The cards still open Prepare.\n- **Test name over-promises:** the \"Open in Export →\" test says the button shows *only* where there is an export screen, but it never checks that the button is absent when there isn't one.\n\nThe new drag handler matches how the existing file drags work (it cancels the browser's drag and passes the file id and title). The picture sizes of Reels and square copies are correct even though no framing is passed, because those presets have a fixed canvas.

**Batch 2 of 2.** I reviewed part 2: the page tests, the four stylesheets, the two backlog docs, and the en/es messages.

- **Stylesheets:** every class the new and changed components use exists in its stylesheet. The deleted strip stylesheet is no longer referenced anywhere.
- **Messages:** none of the removed `library.*` keys (`where*`, `copiesEmpty`, `copyProgress*`) is still used. `sendTo` stays because the Library's card and row still use it. The en and es files have matching keys.
- **Tests:** the updated tests fit the new layout. The heavy-file suite no longer asserts that small files skip the file read, which matches the new behaviour of reading every local recording.
- **Docs:** the backlog doc correctly says the code has six destinations, which matches `DESTINATION_IDS`. The PR description's claim of "seven destinations… Email is its own card" is wrong, but that is the PR text, not a file under review.
- **Finding:** one `consider` on the validation script in `prepare-screen.md`. It says to drag the copy's row into Finder, but the row is a link; only the Drag handle starts a file drag.

Two contracts are still open: what happens when `startFileDrag` fails in the main process, and how `useSourceProbe` handles a failed file read.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 11 | $0.48 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 12 | $0.48 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 32 in / 14k out / 660k cache read / 108k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.96</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6ImQ5Y2IyNzYwLTE4ZjYtNDA4ZC1hNWE0LTRjY2I1MGU4YmIwOCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=d9cb2760-18f6-408d-a5a4-4ccb50e8bb08 -->
