# kaipu-bench-wachi-v3#19 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:55:26Z · commit dac8318

👮 **Wachiman** · 🟣 **1 question for you** · 3 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 2 Should · 1 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`destinations-panel.tsx:91`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx#L91) | When the probe fails, six of the seven cards show "…" forever |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "Open in Export" test never checks the case where the button is hidden |
| 🟡 Consider · Could · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | Global \`window.electronAPI.startFileDrag\` is overwritten and never restored |

### Questions for you (1)

- [`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) · open question — The page now reads (probes) the file for every local recording, not only heavy ones: Does useSourceProbe surface a failed probe, or is it left null without telling anyone? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

<details><summary>What the change connects to (5 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- The page now reads (probes) the file for every local recording, not only heavy ones (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Does useSourceProbe surface a failed probe, or is it left null without telling anyone? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

**Closed, with the lines they rest on**

- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — Main drags the vault file under the copy's title into the target app. If it fails: startFileDrag returns void (fire and forget). If main refuses, no drag happens and nothing is shown, the same as the sibling call sites. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:233-235`, `apps/kaipu-record/src/renderer/src/features/library/components/gif-viewer.tsx:25-27`, `apps/kaipu-record/src/shared/types/electron-api.ts:257-259`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-180`.
- Every local recording page now probes the source file (was: only heavy or fresh-card pages) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Adds the resolution to the metadata line, the estimate on each destination card and the picture size of each copy. If it fails: On a failed probe, status is set to error and probe stays null. The metadata resolution is hidden, copies show only the file size, and the destination cards show "…" indefinitely (reported as a findi… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:282-289`.
- "Not now" dismisses the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel hides and "Export a copy" appears in the actions (line 436). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`.
- A destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — The router goes to /prepare/:assetId?to=<id>. The tests check this for all six ids (library-detail-page.test.tsx:253-266). If it fails: Synchronous client-side navigation with no async call, so there is nothing that can fail. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-494`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-39`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and brings back "Export a copy" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts, and the primary Export a copy button appears because showDestinations is now false. Tested at library-detail-page.test.tsx:292-306. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292-306`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found three small things in part 1, all at "consider" level, and nothing that blocks the merge.

1. **Probe failure in the destinations panel** (`destinations-panel.tsx:91`): when the file can't be read, six of the seven cards show the loading "…" indefinitely and never say the read failed. Only Archive shows a size.
2. **"Open in Export" test** (`master-copies-panel.test.tsx:140`): its name says the button shows "only where there is an export screen", but nothing checks that it is hidden when `onOpenExport` is omitted.
3. **Drag test** (`master-copies-panel.test.tsx:100`): it replaces the shared `window.electronAPI.startFileDrag` and never puts the original back, so later tests in the same worker can see the mock.

The rest checks out against the code:

- **Drag handle:** it calls the existing `startFileDrag(id, name)` IPC the same way the status-card and GIF-viewer drags do, so the Electron boundary isn't widened.
- **Probing every recording:** the probe hook already discards results that belong to a different file.
- **"Not now":** it is component state keyed by the recording, so it is never stored, as the PR says.
- **Panels:** the copies panel is now rendered only when there are copies or one is running. That is why the old empty state could go, and the page is its only caller.

**Batch 2 of 2.** I found nothing to flag in part 2 (tests, stylesheets, backlog docs and i18n messages); all nine files are in files_reviewed.

- **Tests:** they follow the new layout:
  - the title row;
  - the six destination cards, one per DESTINATION_IDS entry, each opening `/prepare/:id?to=<id>`;
  - "Not now" bringing back "Export a copy";
  - copies with their resolution and drag handle;
  - the saved notice keyed to a fresh recording.
- **Removed assertion:** the "up to 25 MB" test drops `probe not.toHaveBeenCalled`. That fits the change, since the page now probes every local recording.
- **i18n:** the en and es changes match each other. `sendTo` is kept for the Library cards.
- **Docs:** the backlog doc's claims match the code, including "the code has six destinations".
- **PR body:** it says seven destinations with Email as its own card. The code and the doc both say six, so the PR body is the stale one.

One question is open, recorded as a contract: what happens when the file probe fails. If it never resolves, the cards keep showing "…" and the resolution never appears; I did not read `use-prepare-copy.ts`, so I can't say whether that failure is shown anywhere.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 9 | $0.51 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 7 | $0.48 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 22 in / 9.5k out / 406k cache read / 89k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.98</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6ImI5NzM5N2JmLTY5MDUtNGFlYS05ZjE0LWE5MjQ3NzUyMjgxZCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=b97397bf-6905-4aea-9f14-a9247752281d -->
