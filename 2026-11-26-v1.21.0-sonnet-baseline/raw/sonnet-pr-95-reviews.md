# kaipu-bench-wachi-v3#95 [replay] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:30:45Z · commit b2705a9

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 question for you · 5 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 5 to consider · ⚪ 0 for your information (6) · 2 Should · 4 Could |
| **Risk** | High: top fact `public-contract` at `preload/index.ts:244`, see Risk facts |
| **Needs a person** | 1 trade-off, in `recording-ready-window.ts:89` |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `preload/index.ts`, `recording-ready.ts`, `electron-api.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`main/index.ts:899`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/index.ts#L899) | openInMain un-hides the main window into an active recording |

### To consider (5)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` does not check who is asking |
| 🟡 Consider · Could · 🐛 bug | [`recording-ready-window.ts:219`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L219) | A reshown card can flash the previous recording's content |
| 🟡 Consider · Should · 🧹 cleanup | [`post-recording-card.tsx:47`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx#L47) | Doc comment line is over-long after the edit |
| 🟡 Consider · Could · 🧪 tests | [`recording-ready-window.test.ts:204`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.test.ts#L204) | No test for an action arriving during an active take or after a card swap |
| 🟡 Consider · Could · 🐛 bug | [`main.css:85`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/assets/main.css#L85) | 16 px window padding may clip the card's shadow into a hard edge |

### Questions for you (1)

- [`recording-ready-window.ts:89`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L89) · trade-off — The card has no timer and stays up until an action, so a user can start another take with it still on screen. Whether it should auto-close when a take starts, or keep the 'question is the point' semantics and defer hand-offs, is a product decision.

### Risk facts

- `public-contract` · [`preload/index.ts:244`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/preload/index.ts#L244) — Adds `showRecordingReady`, `recordingReadyCard` and `onRecordingReadyOpen` to the `window.electronAPI` surface exposed to every window that loads the shared preload.
- `electron-api.ts` — a contract more than one side imports
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Hand-off after a card action: close the card, showMainWindow, send recording-ready:open (`apps/kaipu-record/src/main/index.ts:899`) — Main window comes forward and navigates to Prepare, the editor or the recording page. If it fails: During an active take (card left up from the previous one) the main window is shown into the recording and the recorder's page is navigated away. Evidence: `apps/kaipu-record/src/main/index.ts:184-186`, `apps/kaipu-record/src/main/index.ts:474-482`, `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/recording/recording-hub.ts:689`.
- showRecordingReady invoke from main-window renderer; window creation failure (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:134`) — Floating card, or in-app card on creation failure. If it fails: A window that is created but fails to load shows nothing and no fallback (acknowledged in the PR body). The handler does not validate the sender. Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-107`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:26-28`.
- lastTakeDisplayId remembered by the hub (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — Card opens on the recorded display, or the display under the pointer when null. If it fails: None found. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:707-714`, `apps/kaipu-record/src/main/recording/recording-hub.ts:934-941`.
- Library detail page asks main to float the 'Your video is ready' card instead of rendering it in-app (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — The card appears on the desktop, not in the app. If main answers false or the IPC rejects, setFallbackFor makes inApp true and the old in-app card shows. If it fails: A window that is created but cannot load its renderer shows nothing and does not fall back; the doc lists this under 'Not done'. A rejected IPC or a false answer does fall back, and the test covers b… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-32`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`.
- Floating card actions hand off to the main window, which navigates (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28`) — The user lands on Prepare, the editor or the recording's page. The card on the desktop closes. If it fails: The hand-off is a typed union validated in main (shared/types/recording-ready.ts). The renderer only builds a path from it, and the asset id is URL-encoded for Prepare. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/editor/open-in-editor.ts:32-35`, `apps/kaipu-record/src/shared/types/recording-ready.ts:37-40`.
- New render target ?window=recording-ready, with a card that reports its height to main (`apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:24`) — The window is sized to the card. Escape dismisses once the window has focus. If it fails: If main never sends a payload, the window renders nothing. The ready/onShow ordering is pinned by a test. The renderer-load failure case is documented as not handled. Evidence: `apps/kaipu-record/src/renderer/src/main.tsx:66-71`, `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:24-53`, `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.test.tsx:37-43`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The floating-card design is sound: payloads and actions are validated, card-side channels check the sender, and the fallback to the in-app card on creation failure works. One real defect: `openInMain` calls `showMainWindow()` unconditionally, so clicking the card during a later take un-hides the main window into the recording. The repo's other call sites guard against exactly this. Smaller points: `recording-ready:show` does not check its sender, the card can flash the previous recording's content when reshown, and one comment line in `post-recording-card.tsx` is over-long. I only read the code; nothing was built or run.

**Batch 2 of 2.** I found one low-confidence concern in part 2 and no defects. The renderer side matches the PR's claims. The ask is made once per arrival and waits until the file probe settles. It falls back to the in-app card when main answers false or the IPC rejects. Hand-offs go through the same helpers as the in-app card. The tests and docs match the code. The concern is that the floating window's 16 px padding may clip the status card's large shadow into a hard edge. The doc already says the window's size and shadow are unchecked in Electron.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 14 | $0.36 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 19 | $0.33 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 28 in / 18k out / 592k cache read / 111k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.69</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6IjlkNWUzOGNlLTk1YmUtNGY5Yi05Nzk5LTIwODc3MjZhMThlYyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6NSwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjYsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=9d5e38ce-95be-4f9b-9799-2087726a18ec -->
