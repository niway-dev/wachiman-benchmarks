# kaipu-bench-wachi-v3#90 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:03:41Z · commit dac8318

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 question for you · 3 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 3 to consider · ⚪ 1 for your information (5) · 3 Should · 1 Could · 1 FYI |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`master-copies-panel.tsx:174`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L174) | Drag skips markCopySeen, unlike the Ready card's Drag |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) | When the probe fails, the destination cards show "…" forever |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "Open in Export → shows only where…" never tests the case where it is hidden |
| 🟡 Consider · Could · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | Test replaces window.electronAPI.startFileDrag and never restores it |

### Questions for you (1)

- [`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) · open question — Probe the file for every local recording (previously only heavy ones): Does useSourceProbe catch and report a probe failure, or do the cards silently stay at "…" forever? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

<details><summary>For your information (1)</summary>

| | Where | Finding |
| --- | --- | --- |
| ⚪ Info · FYI · 📝 docs | [`prepare-screen.md:114`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/documentation/src/content/docs/backlog/prepare-screen.md#L114) | PR body says seven destinations; the doc and the code say six |

</details>

<details><summary>What the change connects to (8 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Probe the file for every local recording (previously only heavy ones) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Does useSourceProbe catch and report a probe failure, or do the cards silently stay at "…" forever? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`.

**Closed, with the lines they rest on**

- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The file is dragged under the copy's title (main sanitizes the name). The Library badge is not cleared for that copy. If it fails: startFileDrag returns void (fire-and-forget IPC), so a failure in main is not visible to the renderer. The button only renders when copy.id !== null. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-236`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-58`, `apps/kaipu-record/src/shared/types/electron-api.ts:254-259`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-175`.
- Destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The Prepare screen opens with the destination selected. If it fails: Synchronous navigation, nothing async. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`.
- "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel disappears, and "Export a copy" plus the heavy banner (for a heavy recording) appear. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- Probe of the source file now runs for every local recording (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution shows in the metadata line, sizes on the destination cards, and picture sizes on the copy rows. If it fails: An unusable probe gives status error with probe null. The page drops the status, so the cards show "…" indefinitely and the resolution never appears, with no error shown. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- Copy row picture size derived from the original's probe and the copy's preset (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`) — "2560 × 1440 · 22 MB". If it fails: Without a probe, only the size shows. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:479-504`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:186-188`.
- Click a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — Router navigates to Prepare with that destination preselected; the tests check every search string. If it fails: Synchronous navigation only. No async call, so there is no failure path. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and shows Export a copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts. Export a copy appears in the actions, and the heavy banner returns for a heavy master because it is gated on !showDestinations. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517-523`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292-306`.
- Saved-to-Library notice on a fresh recording, dismissable (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A green role=status notice above the player. After ✕, the masterNote line appears. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:134-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found no blockers in part 1. There is one fix: the new Drag handle in "Copies from this original" skips the `markCopySeen` call that the Ready card's Drag makes, so dragging a fresh copy out leaves the sidebar's Library badge counting it. I also have three "consider" notes:

- When the probe fails, the destination cards show "…" forever, because the page drops the probe's error status.
- The "Open in Export →" test never checks that the button is hidden when `onOpenExport` is missing.
- One test replaces the global `window.electronAPI.startFileDrag` and never restores it.

The PR description doesn't match the code in one place. It says the panel shows seven destinations with Email as its own card, but `DESTINATION_IDS` has six (`destinations.ts:36-43`). Email is still part of the chat card ("Slack · Discord · Email"), and the tests expect exactly that. The layout moves, the "Not now" dismissal keyed by asset id, and the heavy-banner condition now being `!showDestinations` all read correctly against the code.

**Batch 2 of 2.** I found no defects in this part's files: the tests, stylesheets, backlog docs and en/es messages.

- **Tests:** they match the rewritten page. The title row is checked through `back.parentElement`. The two master tags come from the title and the player. The notice's `<strong>` title is matched by exact text. The heavy-master case folds its banner into the panel. Removing the "file isn't read" assertion is correct, because the page now reads the file for every local recording.
- **Messages:** none of the removed `library.*` keys (`where*`, `copiesEmpty`, `copyProgress*`) are referenced anywhere in the repository. `sendTo` is kept because the Library card and row still use it.
- **Backlog doc:** it agrees with the code, including six destinations.
- **PR description:** it is wrong in one place. It claims seven destinations with Email as its own card, but `DESTINATION_IDS` has six. I filed this as an info note.

One question stays open: what happens if reading the file fails. I didn't read `useSourceProbe`, so I can't say whether the destination cards would then stay at "…" without any message.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 10 | $0.53 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 13 | $0.51 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**PR body says seven destinations; the doc and the code say six (confidence high)** ([`prepare-screen.md:114`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/documentation/src/content/docs/backlog/prepare-screen.md#L114))

The PR description says "Seven destinations, as in the design … Email is its own card". `DESTINATION_IDS` (apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43) still lists six, the tests click six cards (library-detail-page.test.tsx:253-260), and this doc says six. The doc is right and the PR body is wrong, so a reviewer following step 4 of "How to test it yourself" should expect six cards, not seven.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 28 in / 14k out / 657k cache read / 123k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.03</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6IjJiZTE0MGQzLTVmNjEtNGY4Zi05OWI4LTBkMjlhZGY5NTFmYyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MywiaW5mbyI6MX0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjEsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=2be140d3-5f61-4f8f-99b8-0d29adf951fc -->
