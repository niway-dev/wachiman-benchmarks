# kaipu-bench-wachi-v3#35 [replay] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:53:08Z · commit b2705a9

👮 **Wachiman** · 🟡 **Nothing to fix · 4 to consider** · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 4 to consider · ⚪ 0 for your information (4) · 4 Could |
| **Risk** | High: top fact `public-contract` at `index.ts:244`, see Risk facts |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `index.ts`, `recording-ready.ts`, `electron-api.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`recording-hub.ts:711`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-hub.ts#L711) | A take stopped before the source lookup resolves never records its display |
| 🟡 Consider · Could · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` accepts any sender, not only the main window |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | Back onto the recording page floats the desktop card again |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L140) | A probe that never settles now hides the card entirely |

### Risk facts

- `public-contract` · [`index.ts:244`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/preload/index.ts#L244) — The preload bridge gains `showRecordingReady`, `recordingReadyCard` and `onRecordingReadyOpen`, which widens the renderer-to-main API exposed to every window that loads this preload.
- `electron-api.ts` — a contract more than one side imports
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Main window asks main to float the ready card (`showRecordingReady` → `recording-ready:show`) (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — The card is painted via `recording-ready:payload` and `showInactive()` at the top-right of the recorded or cursor display. If it fails: A creation throw returns false and the renderer shows the in-app card. A load failure after creation returns true and nothing ever shows (no fallback, as the PR acknowledges). Sender is not checked. Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:218-226`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:21-29`.
- Card action hands off to the main window (`recording-ready:open`) (`apps/kaipu-record/src/main/index.ts:897`) — The main window comes forward and navigates. If it fails: An action without a payload is ignored. Foreign senders are ignored. Edit is dropped when canEdit is false. Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`, `apps/kaipu-record/src/main/index.ts:897-903`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`.
- Hub remembers the take's display for placement (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — Decides which display's corner the ready card opens in. If it fails: If the take stops before the lookup resolves, the value stays null and the card falls back to the cursor display. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:707-713`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- Recording page asks main to float the ready card once per arrival (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — The card appears in a desktop window. When the window cannot be created or the IPC fails, it appears in the status stack instead. If it fails: A rejected IPC or a false answer falls back to the in-app card. A probe that never settles shows no card at all. On Back the page remounts, the ref resets and the window is asked for again. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-31`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:129-155`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-107`.
- Main window navigates on a floating-card hand-off (`apps/kaipu-record/src/renderer/src/shell/app-root.tsx:31`) — The main window lands on Prepare, the editor or the recording's page. If it fails: The detail route pushes without fromRecording state, so the card is not shown again. A ✕ sends no hand-off. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:165-172`.
- The recording-ready render target (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — Only the card paints. It is 420px wide inside a 452 DIP window with 16px padding. If it fails: If the renderer fails to load, nothing shows and the page does not fall back to the in-app card. The doc acknowledges this. Evidence: `apps/kaipu-record/src/renderer/src/main.tsx:62-71`, `apps/kaipu-record/src/renderer/src/assets/main.css:85-93`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:15-19`, `apps/documentation/src/content/docs/backlog/floating-ready-window.md:55-56`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 adds the floating "Your video is ready" window, its IPC contract and the preload bridge. The contract file keeps the no-value-import rule, inputs that cross IPC are parsed, and the card-side channels check that the sender is the card's own window. I found nothing that blocks the merge. There are two considers. First, the hub drops the take's display when the take stops before the source lookup resolves, so the card opens on the cursor's display instead. Second, `recording-ready:show` does not check its sender. A window that is created but whose renderer never loads still shows nothing, which the author acknowledges in the PR.

**Batch 2 of 2.** I reviewed part 2: the recording page's request for the floating card, the card window root, hand-off routing, tests, styles, the docs and the i18n keys. The wiring matches the capture-toast pattern, and the width and padding numbers agree with main's constants. Two "consider" findings. First, router Back remounts the page with the same history key and `fromRecording` state, so the desktop window floats again after the user already acted on it. Second, gating the request on the file read means a read that stalls shows no card anywhere, where before the in-app card rendered at once.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 4 | $0.44 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 13 | $0.50 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 20 in / 11k out / 315k cache read / 82k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.94</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6IjA3M2NkMDhjLTBjMjUtNGE1ZC1iNjA5LThhODc1MDIzN2VjNyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=073cd08c-0c25-4a5d-b609-8a8750237ec7 -->
