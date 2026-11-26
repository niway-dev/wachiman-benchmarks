# kaipu-bench-wachi-v3#120 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:08:14Z · commit b2705a9

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 3 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 3 to consider · ⚪ 0 for your information (4) · 1 Should · 3 Could |
| **Risk** | High: risky path `index.ts`, see Risk facts |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `index.ts`, `recording-ready.ts`, `electron-api.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recording-ready-window.ts:166`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L166) | A card left up during the next take can show the main window mid-recording |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` does not check which window is asking |
| 🟡 Consider · Could · 🐛 bug | [`recording-ready-window.ts:134`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L134) | \`show()\` returns true for a window whose renderer never loads, so the card is silently lost |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | Router Back to the arrival entry floats the card again |

### Risk facts

- `index.ts` — a process boundary
- `electron-api.ts` — a contract more than one side imports
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Main window asks main to float the card (`recording-ready:show`, invoke) (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — The card appears top-right on the recorded display, or the pointer's display, without taking focus. If it fails: A creation failure returns false and the page falls back to the in-app card. An IPC rejection also falls back. A load failure after creation leaves nothing visible and no fallback. The handler does n… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-107`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:21-29`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:148-160`.
- Card press -> close -> `openInMain` (show main window, send `recording-ready:open`) (`apps/kaipu-record/src/main/index.ts:897`) — The main window comes forward and navigates to Prepare, the editor or the recording's page. If it fails: The card is not closed when a new take starts. A press during a take shows the main window into the recording (finding on `recording-ready-window.ts`:166). Senders are validated, actions are parsed,… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:122-126`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`, `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/recording/recording-hub.ts:689`.
- Hub remembers the take's display (`lastTakeDisplayId`) (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — The card opens on the recorded display, or the pointer's display when the id is null or unknown. If it fails: A window source or a failed lookup leaves null, so the card uses the cursor display. This is not an error. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:646`, `apps/kaipu-record/src/main/recording/recording-hub.ts:666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:707-713`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- Page asks main to float the 'Your video is ready' card (showRecordingReady) once the probe settles (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — The card appears in its own window; the in-app card shows only on fallback. Dimensions come from the probe, or are omitted when the probe errored. If it fails: IPC rejection or a false answer sets fallbackFor and the in-app card shows. A window that creates but fails to load shows nothing, which the doc admits. Back to the same history entry remounts the pa… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-32`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/editor/open-in-editor.ts:26-29`, `apps/kaipu-record/src/renderer/src/shell/app-root.tsx:75`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`.
- Hand-off from the floating card navigates the main window (onRecordingReadyOpen) (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28`) — Main window navigates to Prepare, the editor or the recording page. If it fails: If AppRoot is unmounted when the hand-off arrives, the navigation is lost. The main-process side is outside this part. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/renderer/src/shell/app-root.tsx:30-31`, `apps/kaipu-record/src/renderer/src/features/editor/open-in-editor.ts:32-35`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found one thing to fix: the floating card is never dismissed when the next take starts, and a press on it then shows the main window during the recording. The capture toast is dismissed before every capture; this card is not. Two smaller points are optional. The `recording-ready:show` handler doesn't check which window is asking, and a card window whose renderer fails to load is silently lost with no in-app fallback. The shared contract (`recording-ready.ts`) has no value imports, and the card's actions and payload are validated in main. `assetId` in hand-offs comes from main's stored payload, not from the card. I did not run anything; this was a read-only review.

**Batch 2 of 2.** I read all 13 files in this part and found one issue, a "consider". After a floating-card action, router Back to the recording page re-floats the card. The renderer wiring, the fallback to the in-app card, the tests, the CSS, the docs and the i18n keys are otherwise consistent. I read only this part's files and the renderer code they call. I did not read `recording-ready-window.ts`, only grepped it for its width and padding constants. I did not read the main-process hand-off sender. Nothing was run.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 15 | $0.30 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 17 | $0.23 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 30 in / 17k out / 661k cache read / 116k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.53</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6ImU3ZWMyOWM3LWY3NDEtNGEzNC1iYjAzLTVhMjZjMGExY2FiMCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=e7ec29c7-f741-4a34-bb03-5a26c0a1cab0 -->
