# kaipu-bench-wachi-v3#44 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:56:50Z · commit dac8318

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 question for you · 2 to consider · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 2 to consider · ⚪ 0 for your information (3) · 2 Should · 1 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Needs a person** | 1 trade-off, in `library-detail-page.tsx:142` |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) | A failed probe leaves the destination cards on "…" for good |

### To consider (2)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`master-copies-panel.tsx:174`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L174) | Dragging a copy from the panel doesn't mark it seen the way the ready card does |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "shows only where there is an export screen" never checks the case where it's hidden |

### Questions for you (1)

- [`library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) · trade-off — The page now reads the file on every visit to a local recording, not only for heavy files. That pays for the resolution and the estimates; a person should decide whether that cost is acceptable on large vault files.

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Destination card click opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Navigates to the Prepare screen with the destination preselected. If it fails: No async; when assetId is missing it does nothing (line 150). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`.
- "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel disappears, and the Export a copy button and the heavy banner appear (lines 436, 517). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`.
- Probe the source file for every local recording (it used to run only for heavy files or the card) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Resolution in the metadata line, size estimates on the destination cards, picture size on each copy. If it fails: On a probe error the probe stays null: the metadata line has no resolution, the cards show "…" forever, and a copy row shows only its file size. A rejection of probeSource is not caught. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- Drag handle starts a native file drag of a copy (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The OS drag of the vault file, named after the copy's title. If it fails: startFileDrag is fire-and-forget (void); the handle only renders when copy.id is not null. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/shared/types/electron-api.ts:255-259`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164`.
- Destination card / "Not now" in "Where is it going?" and "Export a copy" on the recording page (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489`) — The URL becomes /prepare/:assetId?to=<id>, or has no query for Export a copy. The tests at lines 253-266 and 292-306 assert exactly that. If it fails: Pure navigation, no async call. The probe-dependent sizes and the resolution stay hidden or show "…" until useSourceProbe resolves. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292-306`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-39`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The new layout does what the PR describes. The Where is it going? panel only appears when an original has no copies and nothing is exporting, and Not now brings back Export a copy and the heavy banner. One thing is wrong today: the page now reads the file for every local recording but keeps only the result, not whether reading it failed. When the read fails, the destination cards stay on the loading "…" for good. Two smaller points: the new Drag handle skips the `markCopySeen` step the ready card's drag takes, and the Open in Export test never checks the case where the button is hidden.

**Batch 2 of 2.** I found nothing to report in part 2 (tests, stylesheets, backlog docs, i18n messages).

**Tests:** The updated tests in `library-detail-page.test.tsx` match what `library-detail-page.tsx` renders:

- the title row, with the back button, the title and the master tag together and no actions in it;
- the destinations panel shown only before the first copy, and "Not now" hiding it;
- the "Export a copy" button, which waits until the panel is gone;
- the "Saved to your Library" notice, which hides the standing master note until it is dismissed;
- the "1 copy" count in the metadata.

The removed `probe not called` assertion fits the page now reading every local recording's file. The `cleanup()` calls added between renders are imported.

**Messages:** The removed i18n keys (`where*`, `copiesEmpty`, `copyProgress*`) have no remaining callers in `apps/kaipu-record/src`. `sendTo` stays.

**PR body vs. code:** The PR body says there are seven destinations with Email as its own card. `DESTINATION_IDS` in `destinations.ts` lists six, and the six cards the test checks match that. `backlog/prepare-screen.md` (line 114) correctly says the code has six. So the PR description is the stale part, not the doc.

**Stylesheets:** The CSS changes are layout only. The player width cap `min(100%, max(420px, (100vh − 300px) · 16/9))` gives about 658px at the default 670px window height, which matches the doc's claim.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 9 | $0.58 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 7 | $0.47 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 20 in / 9.7k out / 389k cache read / 97k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.05</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6ImQwNjYyMGMwLTZkOWUtNDZiNS1iNGFlLWI5MDI4MmEyNjFlNSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MiwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=d06620c0-6d9e-46b5-b4ae-b90282a261e5 -->
