# kaipu-bench-wachi-v3#105 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:35:42Z · commit b2705a9

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 question for you · 4 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 4 to consider · ⚪ 0 for your information (5) · 2 Should · 3 Could |
| **Risk** | High: top fact `public-contract` at `electron-api.ts:455`, see Risk facts |
| **Needs a person** | 1 trade-off, in `recording-ready-window.ts:187` |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `electron-api.ts`, `preload/index.ts`, `recording-ready.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`main/index.ts:897`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/index.ts#L897) | The ready card is not dismissed before a screenshot or the next take; only content protection keeps it out |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` does not check who sent it |
| 🟡 Consider · Should · 🧹 cleanup | [`post-recording-card.tsx:47`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx#L47) | JSDoc line was rewrapped badly |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | Back to a fresh recording's page floats the card again |
| 🟡 Consider · Could · 🧪 tests | [`recording-ready-card.test.tsx:62`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.test.tsx#L62) | Height reporting to main (\`api.resize\`) is not covered |

### Questions for you (1)

- [`recording-ready-window.ts:187`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L187) · trade-off — Making the card focusable so Escape works means the click that focuses it can steal focus from the app being used. The alternative is no keyboard dismissal. Whether Escape needing a click first is acceptable is a product call.

### Risk facts

- `public-contract` · [`electron-api.ts:455`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/shared/types/electron-api.ts#L455) — Adds `showRecordingReady`, `recordingReadyCard` and `onRecordingReadyOpen` to the preload's `KaipuElectronAPI`, which every window that loads the preload can call.
- `preload/index.ts` — a process boundary
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Main window asks main to float the card (`recording-ready:show`, invoke), main creates or re-targets one panel window (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — The card appears top-right on the take's display, or on the cursor's display when the take's display is unknown, without taking focus. It stays until an action, ✕ or Escape. If it fails: Create failure returns false, and the page then shows the in-app card. A window that was created but fails to load shows nothing and nothing falls back, as the PR notes. The card is not dismissed bef… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-107`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:208`, `apps/kaipu-record/src/main/screenshots/capture-window-hooks.ts:55-56`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:305-307`, `apps/kaipu-record/src/main/recording/area-geometry.ts:81-85`.
- Card action (chip, Edit first, Open, ✕, Escape) goes card → main (`recording-ready:action`), main closes and hands off to the main window (`recording-ready:ope… (`apps/kaipu-record/src/main/index.ts:897`) — The card closes first (hide called before `openInMain`, pinned by the test), then Kaipu comes forward and navigates. If it fails: A malformed or foreign press is dropped by `parseRecordingReadyAction` and `isOwnSender`. A press after close is a no-op because the payload is null. Edit first is ignored when `canEdit` is false, th… Evidence: `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/index.ts:897-903`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:122-126`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`, `apps/kaipu-record/src/shared/types/recording-ready.ts:47-61`.
- Hub remembers the display of the latest take (`lastTakeDisplayId`) (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — The card opens on the recorded display. If it fails: The lookup is async. If the user stops before it resolves, the early return leaves the id as set at start, which can be null; the card then falls back to the cursor's display. That is a fallback, not… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:646`, `apps/kaipu-record/src/main/recording/recording-hub.ts:666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:707-713`, `apps/kaipu-record/src/main/recording/recording-hub.ts:934-941`.
- Ask main to float 'Your video is ready' once per arrival (showRecordingReady IPC), with in-app fallback (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16`) — The card floats on the desktop. The in-app card appears only as a fallback, and the fallback now waits for the probe. The probe resolves to ready or error, since probeSource catches failures (probe-source.ts:42-43). If it fails: IPC rejection (no handler registered yet) or a false answer turns on the in-app card, so the card is not lost. A window that is created but never loads its renderer shows nothing, and the doc admits… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18-31`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/index.ts:895-903`.
- Hand-offs from the floating card navigate the main window (onRecordingReadyOpen -> navigate(pathForHandOff)) (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28`) — The main window comes forward and lands on Prepare, the editor or the recording page. The Open hand-off pushes /library/:id without fromRecording state, so the card does not re-ask on that entry. If it fails: If the main window's renderer is not mounted yet (or AppRoot is not rendered, for example during onboarding), the hand-off IPC is dropped and the click does nothing visible after the card has closed.… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/renderer/src/shell/app-root.tsx:27-31`, `apps/kaipu-record/src/main/index.ts:897-903`.
- New render target ?window=recording-ready (transparent window, crash forwarder, resize reporting) (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — Only the card paints in a window of 452 DIP width. The shadow shows in the 16px margin. If it fails: The crash-forwarder origin is a free string, so the new 'recording-ready' origin is accepted. If the renderer never sends `ready`, main never shows the window, and there is no timeout and no in-app f… Evidence: `apps/kaipu-record/src/renderer/src/main.tsx:60-71`, `apps/kaipu-record/src/renderer/src/assets/main.css:73-93`, `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:24-53`, `apps/kaipu-record/src/renderer/src/features/analytics/crash-forwarder.ts:8-17`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The floating-card design follows the capture toast closely. The IPC payloads are validated, the sender is checked on the card-side channels, and `src/shared` takes no value imports from workspace packages. The main gap is that the card is never dismissed before a screenshot or the next recording. The toast is dismissed in both cases, and here only content protection is relied on. The repo documents that content protection paints windows black on Windows builds before 10 2004, and the card has no timer. A smaller point: the `recording-ready:show` handler does not verify its sender. I did not read the backlog doc or the `backlog/index.mdx` row, which belong to the other part.

**Batch 2 of 2.** I found nothing that blocks the merge in this part. I only read the code and ran nothing.

- **Re-pop on Back (medium confidence):** the "asked once" guard in `useFloatingReadyCard` is a component ref. After a chip, Edit first or Open, Back remounts the recording page under the same history entry, so the card floats again. The old in-app card behaved the same way, but a floating always-on-top window is more intrusive. The doc's "once per arrival" does not hold across a remount.
- **Resize untested:** nothing in the tests checks the card's height reporting to main (`api.resize`).
- **Verified fine:**
  - The in-app fallback covers both a false answer and an IPC rejection.
  - The hand-off paths reuse `preparePath`, `editorPathFor` and the library-detail route.
  - The new `?window=recording-ready` branch matches the capture-toast one.
  - The doc, the backlog row and the i18n keys in both locales are consistent with the code.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 14 | $0.45 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 20 | $0.36 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 28 in / 19k out / 666k cache read / 136k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.81</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6IjJiYjYzZmQ5LWQ3MWYtNDUzZi05NDg5LTA3NGY1NDdlOTk3NiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjUsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=2bb63fd9-d71f-453f-9489-074f547e9976 -->
