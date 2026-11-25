# kaipu-bench-wachi-v3#30 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:00:35Z · commit b2705a9

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 6 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 6 to consider · ⚪ 0 for your information (7) · 4 Should · 3 Could |
| **Risk** | High: top fact `public-contract` at `index.ts:244`, see Risk facts |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `index.ts`, `recording-ready.ts`, `electron-api.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | Going Back to the recording page makes the floating card pop up again on the desktop |

### To consider (6)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`use-floating-ready-card.ts:18`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts#L18) | Back to the recording page floats the card again |
| 🟡 Consider · Should · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | recording-ready:show accepts any sender |
| 🟡 Consider · Should · 🐛 bug | [`recording-ready-window.ts:145`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L145) | show() answers true before the card can paint |
| 🟡 Consider · Should · 📝 docs | [`post-recording-card.tsx:47`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx#L47) | Docstring says the card goes away when the user leaves the page |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:142`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L142) | No card at all while the probe never settles |
| 🟡 Consider · Could · 📝 docs | [`recording-ready-card.module.css:2`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.module.css#L2) | The header says the window is "452 DIP wide", but this rule only sets \`width: fit-content\` |

### Risk facts

- `public-contract` · [`index.ts:244`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/preload/index.ts#L244) — This adds new preload bridge methods (showRecordingReady, recordingReadyCard, onRecordingReadyOpen) to the API every window sees.
- `electron-api.ts` — a contract more than one side imports
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (7 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Card action (chip, Edit, Open) hands off to the main window (`apps/kaipu-record/src/main/index.ts:899`) — The main window comes forward and navigates via pathForHandOff. If it fails: A queued send is delivered once the renderer reports ready. Evidence: `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`.
- Floating window creation and show (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:174`) — A card in the top-right corner of the recorded display, shown inactive. If it fails: A creation failure returns false, so the in-app card shows. A load failure shows nothing (no fallback). Evidence: `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:274-325`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`.
- Asking for the floating card once per arrival (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:21`) — The card floats again after Back. If it fails: A rejected IPC falls back to the in-app card. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141-155`.
- The hub records the last take's display (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — The card's display placement. If it fails: A failed lookup leaves the countdown's display or null, so the card uses the cursor's display. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:707-714`.
- Page asks main to float the ready card once per arrival (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — A frameless always-on-top window appears; the in-app card shows only when main answers false or the IPC rejects. If it fails: If the IPC rejects or answers false, the page falls back to the in-app card (use-floating-ready-card.ts:25-28). If the window is created but its renderer never loads, nothing shows (documented as not… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18-31`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:129-155`, `apps/kaipu-record/src/renderer/src/shell/app-root.tsx:75`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-106`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`.
- Floating card window root renders main's payload and reports presses (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — The card is painted inside a transparent window that main sizes from resize reports. If it fails: If the payload never arrives, the window renders nothing (recording-ready-card.tsx:55). Evidence: `apps/kaipu-record/src/renderer/src/main.tsx:63-71`, `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:24-71`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:218-223`.
- Main window navigates on a hand-off from the floating card (`apps/kaipu-record/src/renderer/src/shell/app-root.tsx:31`) — The main window shows Prepare, the editor or the detail page. Evidence: `apps/kaipu-record/src/renderer/src/shell/app-root.tsx:27-31`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28-33`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 closely follows the capture toast's window pattern. The window manager validates every card channel against its own sender, and hand-offs are queued until the main renderer is ready. The four findings are all at "consider": Back to the recording page floats the card again; the show channel accepts any sender; a renderer that fails to load leaves no card at all; and the PostRecordingCard docstring is stale.

**Batch 2 of 2.** I reviewed the 13 files in part 2: the renderer side of the floating "Your video is ready" window and its fallback. I left one fix and two smaller notes.

- **Fix: Back makes the floating card pop up again.** The page guards its single request for the window with a ref keyed by the history entry. That ref resets when the page remounts. So when the user goes Back to the recording page (for example after pressing a chip in the floating card), the page asks main to show the card again, and main shows it on the desktop again.
- **Consider: no card if the file read never finishes.** Holding the request until the file has been read also holds back the in-app fallback. If the read never completes, neither card appears.
- **Consider: stale size comment.** A CSS comment repeats window sizes that are defined elsewhere.

The tests, the docs and the new i18n strings match the code.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 11 | $0.69 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 11 | $0.48 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 32 in / 17k out / 636k cache read / 89k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.18</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6ImEwYWQ0NzM4LWNiZWUtNGVhOC05MDllLTVhZDJiYTVmYmU1MiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6NiwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjcsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=a0ad4738-cbee-4ea8-909e-5ad2ba5fbe52 -->
