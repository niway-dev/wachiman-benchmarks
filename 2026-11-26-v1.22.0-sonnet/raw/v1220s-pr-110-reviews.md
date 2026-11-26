# kaipu-bench-wachi-v3#110 [replay] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:04:29Z · commit b2705a9

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 2 questions for you · 2 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 2 to consider · ⚪ 0 for your information (3) · 1 Should · 2 Could |
| **Risk** | High: top fact `public-contract` at `index.ts:244`, see Risk facts |
| **Needs a person** | 1 trade-off, in `recording-ready-window.ts:208` |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `index.ts`, `recording-ready.ts`, `electron-api.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recording-ready-window.ts:208`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L208) | The ready card relies on content protection alone; the toast it copies is also dismissed before each capture |

### To consider (2)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` does not check who sent it, unlike the other three handlers in this class |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | Floating card is asked for again when the page remounts under the same history entry |

### Questions for you (2)

- [`recording-ready-window.ts:208`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L208) · trade-off — The card is meant to stay up with no timer, so only content protection keeps it out of later captures. Whether that is enough on Windows before 19041 and on Linux, or whether to close it on capture or take start as the toast does, is a product decision.
- [`apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts#L18) · open question — Page remount under the same history entry (Back) re-asks for the card: Is a re-floating card on Back intended? The old in-app card behaved the same way. Files that would answer it: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx`, `apps/kaipu-record/src/renderer/src/shell/app-root.tsx`.

### Risk facts

- `public-contract` · [`index.ts:244`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/preload/index.ts#L244) — Adds `showRecordingReady`, `recordingReadyCard` and `onRecordingReadyOpen` to the `contextBridge` API, and the API reaches every window that loads the preload.
- `electron-api.ts` — a contract more than one side imports
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (7 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Page remount under the same history entry (Back) re-asks for the card (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18`) — Is a re-floating card on Back intended? The old in-app card behaved the same way. Files that would answer it: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx`, `apps/kaipu-record/src/renderer/src/shell/app-root.tsx`.

**Closed, with the lines they rest on**

- Main window asks main to float the card (`recording-ready:show`, invoke) (`apps/kaipu-record/src/preload/index.ts:244`) — A card floats top-right on the recorded display, or on the display under the pointer when the take's display is unknown. In-app fallback otherwise. If it fails: Creation failure returns false, so the in-app fallback is used. A window that is created but fails to load its renderer returns true and then shows nothing; the author states this in the PR notes. Th… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-107`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:21-31`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141-155`.
- Card actions go to main, which hides the card and opens the main window on a typed hand-off (`apps/kaipu-record/src/main/index.ts:897`) — The main window comes to the front and navigates through `preparePath`, `editorPathFor` or the `libraryDetail` route. ✕ and Escape only hide the card. If it fails: The action sender is checked with `isOwnSender`, and the action is parsed by `parseRecordingReadyAction`. After `close()` sets `payload` to null, a late press is ignored. Edit sent when `canEdit` is… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:122-126`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:261-265`, `apps/kaipu-record/src/main/index.ts:746-753`, `apps/kaipu-record/src/shared/types/recording-ready.ts:47-61`.
- The hub remembers the display of the latest take (`lastTakeDisplayId`) (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — The card opens on the recorded display, falling back to the cursor display when the id is null or matches no display. If it fails: A stop before the lookup resolves leaves the value from start (possibly null), which gives the cursor-display fallback rather than an error. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:643-666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:707-714`, `apps/kaipu-record/src/main/recording/recording-hub.ts:934-941`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- Card reports its height (`recording-ready:resize`) and Escape (dismiss) (`apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:41`) — The window fits the card. The first show uses the default 290 DIP height until the card reports. If it fails: A malformed height or a foreign sender is ignored. If the renderer never reports ready, the window is never shown, and that state is silent. Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:113-121`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:219-226`, `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:41-53`.
- Library detail page asks main to float "Your video is ready" via showRecordingReady, once the file probe has settled (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — The card appears in its own always-on-top window. The page shows no card unless the ask failed. If it fails: If the IPC rejects or main answers false, the .then handlers call fallBack and the in-app card shows. If the window is created but its renderer never loads, nothing shows and there is no fallback; th… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-32`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:741-766`.
- Floating card actions are handed off to the main window and navigated by pathForHandOff (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13`) — The main window navigates to Prepare, the editor or the recording page after main has closed the card and shown the window. If it fails: The hook is mounted once in AppRoot. If the main window's renderer is not mounted when the hand-off is sent, the event is lost; that is main-side (part 1) and I did not review it. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/renderer/src/features/editor/open-in-editor.ts:32-35`, `apps/kaipu-record/src/renderer/src/shell/app-root.tsx:30-31`.
- Card window root renders PostRecordingCard from main's payload and reports presses and height (`apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:18`) — The card paints in a transparent window. Escape and ✕ send a dismiss action to main. If it fails: Nothing renders until a payload arrives; if main never sends one, the window stays transparent and empty. Main sizes the window only after it receives a resize. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:24-29`, `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:41-53`, `apps/kaipu-record/src/renderer/src/assets/main.css:85-93`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-card.module.css:16`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The floating-card change follows the toast's pattern and its contracts hold up. Hand-offs are queued for a recreated main window, payloads and actions are validated, and `shared/` has no value imports. I found two issues:

- **Fix:** the card relies on `setContentProtection` alone to stay out of the next shot or take. The toast is also dismissed in `beforeCapture`, and the card is not.
- **Consider:** `recording-ready:show` is the only handler in the class that does not check its sender.

I did not run anything.

**Batch 2 of 2.** The renderer side of the floating \"Your video is ready\" window looks sound. It subscribes before signalling ready, falls back to the in-app card when the ask fails, and reuses the in-app card's route helpers. Tests, CSS dimensions (452 = 420 + 2×16), i18n keys and docs are consistent with the code I read. My one finding is a consider: the \"once per arrival\" guard is a ref, so Back from Prepare remounts the page and floats the card again, which contradicts the comment and the doc. I did not review the main-process window manager or the preload, which are in part 1.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 16 | $0.38 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 16 | $0.23 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 26 in / 22k out / 626k cache read / 133k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.62</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6IjE1NzdlNDAwLWUwZmEtNGY1Yi04MTFjLTA3ODk3ZWExYTlkOSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MiwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=1577e400-e0fa-4f5b-811c-07897ea1a9d9 -->
