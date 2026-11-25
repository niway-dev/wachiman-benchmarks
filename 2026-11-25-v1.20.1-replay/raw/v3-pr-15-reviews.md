# kaipu-bench-wachi-v3#15 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:54:42Z · commit b2705a9

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 3 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 3 to consider · ⚪ 0 for your information (4) · 2 Should · 2 Could |
| **Risk** | High: risky path `preload/index.ts`, see Risk facts |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `preload/index.ts`, `recording-ready.ts`, `electron-api.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`main/index.ts:900`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/index.ts#L900) | Hand-off brings the main window back without activating the app |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` accepts any sender |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | A remount under the same history entry floats the card again after the user already acted on it |
| 🟡 Consider · Could · 📝 docs | [`floating-ready-window.md:51`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/documentation/src/content/docs/backlog/floating-ready-window.md#L51) | "the card never shows twice" does not hold on history Back |

### Risk facts

- `preload/index.ts` — a process boundary
- `electron-api.ts` — a contract more than one side imports
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Card action hands off to the main window (openInMain) (`apps/kaipu-record/src/main/index.ts:899`) — The main window should come forward and navigate when the renderer handles recording-ready:open. Without app activation it may stay behind the active app. If it fails: If the main window was destroyed, showMainWindow recreates it and sendToRenderer queues the hand-off until the renderer is ready (index.ts:145-150), so the hand-off is not lost. Focus may still not b… Evidence: `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:559-563`, `apps/kaipu-record/src/main/recording/recording-hub.ts:752-756`.
- Main window asks main to float the card (recording-ready:show invoke) (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — The card appears top-right on the take's display once card-ready arrives. If it fails: If creation throws, the handler returns false and the page shows the in-app card. If the window is created but never loads its renderer, the handler still returns true and nothing is shown for that t… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:218-226`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:21-29`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:148-160`.
- Hub records the take's display (lastTakeDisplayId) (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — Picks the display the card opens on. When no display is known, the card opens on the display under the pointer. If it fails: If the lookup resolves after stop, the refinement is skipped and the value stays null or the region's display. The card then falls back to the cursor display. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:646-666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:707-713`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- Recording page asks main to float the ready card once the probe settles (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — The floating window paints once its renderer reports ready (recording-ready-window.ts:219-226). The in-app card appears only on fallback. If it fails: An IPC rejection or a false answer causes setFallbackFor, and the in-app card shows. If the window is created but its renderer never loads, nothing shows and there is no fallback (this is documented)… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-31`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-155`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:219-226`.
- Floating card hand-offs navigate the main window (`apps/kaipu-record/src/renderer/src/shell/app-root.tsx:31`) — The main window is shown and focused, and the route changes. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/renderer/src/features/editor/open-in-editor.ts:26-35`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:150`.
- New render target ?window=recording-ready (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — RecordingReadyCard subscribes, calls ready, and renders the payload. Main sizes the window from the reported height plus the 16px padding. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:24-53`, `apps/kaipu-record/src/renderer/src/assets/main.css:85-93`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:70-80`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 (IPC contract, main-side window manager, hub change, card renderer and tests) mostly follows the capture toast's pattern correctly: senders are checked, payloads and actions are validated, the window is recreated after close and stays dead after quit. There is one fix: the action hand-off shows the main window without the `applyDockPolicy()` + `app.focus({ steal: true })` step that every sibling reveal path takes, so Kaipu may not come to the front after a press on the non-activating panel. There is also one consider: the `show` handler accepts any sender.

**Batch 2 of 2.** Part 2 wires the floating "Your video is ready" card into the renderer: a new render target in main.tsx, the hand-off hook in AppRoot, the ask and in-app fallback on the recording page, plus tests, styles, the backlog doc and two i18n strings. The hand-offs use the same path helpers as the in-app card, and the fallback works when main answers false or the IPC fails. The one problem found: the `asked` ref does not survive a remount. History Back to the recording's entry therefore floats the desktop card again, even after the user acted on it, which contradicts the doc's "never shows twice".

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 9 | $0.65 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 11 | $0.51 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 24 in / 13k out / 470k cache read / 101k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.16</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6Ijk4OTkwYTQxLTMyNjktNDUzNS1hYzg4LTU1NWRhN2ExYTBiNiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=98990a41-3269-4535-ac88-555da7a1a0b6 -->
