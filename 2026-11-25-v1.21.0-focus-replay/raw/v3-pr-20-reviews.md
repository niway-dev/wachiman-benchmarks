# kaipu-bench-wachi-v3#20 [replay] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:55:44Z · commit b2705a9

👮 **Wachiman** · 🟡 **Nothing to fix · 3 to consider** · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 1 Should · 2 Could |
| **Risk** | High: top fact `public-contract` at `index.ts:244`, see Risk facts |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `index.ts`, `recording-ready.ts`, `electron-api.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` accepts any sender |
| 🟡 Consider · Could · 🐛 bug | [`use-floating-ready-card.ts:18`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts#L18) | Back to the recording page floats the card again |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | Going Back to the recording page reopens the floating card on the desktop |

### Risk facts

- `public-contract` · [`index.ts:244`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/preload/index.ts#L244) — This line adds new contextBridge methods (`showRecordingReady`, `recordingReadyCard`, `onRecordingReadyOpen`), which every window that loads the shared preload can reach.
- `electron-api.ts` — a contract more than one side imports
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (7 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Main window asks main to float the card (`showRecordingReady` → `recording-ready:show`) (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — The card shows inactive at the top-right of the take's display once its renderer reports ready. If the window cannot be created, the page shows the in-app card. If it fails: If creation throws: false, and the in-app fallback shows. If the window is created but its renderer never loads: nothing shows and there is no fallback, as the PR body acknowledges. The rejected IPC… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-107`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:219-226`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:21-29`.
- Card action hands off to the main window (`openInMain` → `recording-ready:open`) (`apps/kaipu-record/src/main/index.ts:899`) — The main window comes forward and navigates via `pathForHandOff` to Prepare, the editor or the detail page. If it fails: When no main window exists yet, `sendToRenderer` returns early only if `mainWindow` is null after `showMainWindow`. `createWindow` sets it, so the send is queued. Evidence: `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/index.ts:897-903`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`.
- Floating card asked once per arrival on the recording page (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18`) — On browser Back to the same entry, the desktop card floats again. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-148`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-31`.
- Hub remembers the latest take's display (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — The card opens on the recorded display, or on the cursor's display otherwise. If it fails: An unknown id falls back to `getCursorDisplay`. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:710-714`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- Recording page asks main to float the ready card once the probe settles (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — A desktop window appears via main, or the in-app card appears as a fallback (library-detail-page.tsx:263). If it fails: Both a rejection and a false answer set fallbackFor, so the in-app card shows. A window that is created but whose renderer never loads shows nothing, and the doc admits it (floating-ready-window.md:5… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-31`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:129-155`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:263-277`.
- Main window navigates on a floating-card hand-off (`apps/kaipu-record/src/renderer/src/shell/app-root.tsx:31`) — The main window lands on Prepare, the editor or the recording's page. If it fails: If the hand-off never arrives, the main window does not navigate. Main closes the card first, so the press is silently lost. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/renderer/src/features/editor/open-in-editor.ts:26-35`, `apps/kaipu-record/src/renderer/src/features/editor/open-in-editor.ts:79-86`.
- Render target ?window=recording-ready (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — The card is painted in a transparent window. Main sizes the window to the reported frame height plus 2×16 px of padding (recording-ready-window.ts:73), which matches the 16 px body padding in main.css:85-89. If it fails: The card subscribes before calling ready (recording-ready-card.tsx:24-29). If no payload ever arrives, it renders nothing. Evidence: `apps/kaipu-record/src/renderer/src/main.tsx:63-71`, `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:18-72`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:16-19`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:73`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The floating "Your video is ready" window follows the capture toast's pattern. The card's own channels check their sender, and every payload and action is parsed before main acts on it. The contract file takes no value imports from workspace packages. Hand-offs reach a recreated main window through `sendToRenderer`'s queue. There are two "consider" points. First, `recording-ready:show` does not check that the main window is the sender. Second, the hook's "asked once" ref does not survive a remount, so browser Back to the recording page floats the card again.

**Batch 2 of 2.** This part of the review found one thing to consider and nothing that blocks or needs fixing.

**Going Back reopens the floating card** (`library-detail-page.tsx:141`). The record of whether the card was already asked for is lost when the recording page remounts. So pressing Back to the recording page reopens the always-on-top window, even after the user has pressed a chip or ✕. The in-app card already came back the same way before this change. The difference is that the floating window is outside the app and stays open after the user leaves the page, and the doc promises "once per arrival".

What I checked and found consistent:

- **Actions:** the floating card's buttons send the main window to the same routes as the in-app card, through the same helpers. Edit first is hidden when the recording can't be opened in the editor.
- **Window size:** the 16 px padding in the stylesheet matches what the main process adds when it sizes the window.
- **Tests:** they check the ask, the in-app fallback and the "no card" cases correctly.
- **Docs and messages:** the backlog doc and the new English and Spanish strings match the code.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 7 | $0.52 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 11 | $0.48 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 20 in / 13k out / 336k cache read / 86k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.01</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6ImRlNGRlNWY0LTFiMjUtNGU3My04MjBhLTM2OTdjMmRlNmVlOCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=de4de5f4-1b25-4e73-820a-3697c2de6ee8 -->
