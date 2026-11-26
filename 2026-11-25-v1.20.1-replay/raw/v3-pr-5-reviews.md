# kaipu-bench-wachi-v3#5 [replay] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:49:56Z · commit b2705a9

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 question for you · 3 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 3 to consider · ⚪ 0 for your information (4) · 1 Should · 3 Could |
| **Risk** | High: top fact `public-contract` at `ipc.ts:532`, see Risk facts |
| **Needs a person** | 1 trade-off, in `recording-ready-window.ts:197` |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `ipc.ts`, `index.ts`, `recording-ready.ts`, `electron-api.ts`, `recording-ready-window.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recording-ready-window.ts:208`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L208) | Card that is still up is never hidden before the next screenshot or recording |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`recording-ready-window.ts:225`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L225) | A re-shown window can flash the previous take's card |
| 🟡 Consider · Could · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` accepts any sender |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | Pressing Back to the fresh recording's page floats the desktop card again |

### Questions for you (1)

- [`recording-ready-window.ts:197`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L197) · trade-off — The window is focusable so Escape can work after a click, unlike the toast's focusable:false. Whether a focusable macOS panel can still pull Kaipu forward needs testing in Electron, which the PR says was not done.

### Risk facts

- `public-contract` · [`ipc.ts:532`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/shared/types/ipc.ts#L532) — Adds six new IPC channels between the main window, main and a new card window, with the payload and action shapes defined in shared/types/recording-ready.ts.
- `index.ts` — a process boundary
- `electron-api.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Main window asks main to float the ready card (`recording-ready:show`) (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — The card appears top-right on the recorded display after the renderer reports ready; showInactive keeps focus where it was. If it fails: createWindow throwing returns false and the page falls back to its in-app card. A window that is created but fails to load shows nothing and returns true, which the PR acknowledges. Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:305-307`, `apps/kaipu-record/src/main/index.ts:670`, `apps/kaipu-record/src/main/recording/area-geometry.ts:82-91`.
- Card action hands off to the main window (`openInMain`) (`apps/kaipu-record/src/main/index.ts:899`) — The main window comes forward and the renderer navigates through pathForHandOff. If it fails: If the main window had to be recreated, the send is queued until the renderer is ready, so nothing is lost. Evidence: `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/index.ts:683-707`.
- Hub records the latest take's display (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — Decides which display's corner the card opens in. If it fails: If the lookup fails or the take is stopped before it resolves, the value falls back to the countdown region or null, and the card opens on the cursor display. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:646-723`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- The recording page asks main to float "Your video is ready" once the probe settles (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — A frameless always-on-top window on the recorded display. If it cannot be created, the status-stack card appears. If it fails: A rejected IPC or a `false` answer sets `fallbackFor`, so the in-app card shows. `probeSource` catches its errors and returns null (status `error`), so the probe settles unless the media read hangs.… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-32`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-147`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`.
- Floating card renderer root: subscribe, report ready, render the payload, report actions and height (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — The card is rendered inside a padded transparent window that main resizes to the reported height. If it fails: Main ignores ready, resize and action messages from any sender other than its own window. Payloads and actions are validated with parsers before use. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:18-72`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-127`.
- The main window navigates on floating-card hand-offs (`apps/kaipu-record/src/renderer/src/shell/app-root.tsx:31`) — Main shows and focuses its window, then the router pushes the route. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28-34`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The floating "Your video is ready" window copies the capture toast's pattern closely: sender checks on the card's channels, validated payloads, and a fallback to the in-app card when the window cannot be created. Its one real gap is that it never closes before a screenshot or the next recording, while the toast is dismissed before every capture. Content protection is its only guard, and on Windows builds before 10 2004 (20H1) that guard paints the window black into captures. Two smaller points: a re-shown window can briefly show the previous take's card, and `recording-ready:show` accepts any sender.

**Batch 2 of 2.** I found one issue in this part, at "consider" level, and I didn't run any of the code (the instructions were read-only).

**The finding:** pressing Back to the fresh recording's page opens the floating card again.

- The page remembers that it already asked for the card only in a ref inside `useFloatingReadyCard`, and that ref is lost when the page unmounts.
- So if the user presses a chip or Edit first on the floating card and then goes Back, the page remounts with the same history entry and asks main again.
- Main doesn't check whether it already showed that recording, so the always-on-top window reopens over whatever the user is doing.
- The old in-app card had the same gap, but it reappeared inside the page rather than on the desktop.
- It also contradicts the backlog doc's claim that "the card never shows twice" (`floating-ready-window.md:51`).

**Checked and fine:**

- The card window's root follows the same setup as the capture toast: transparent window, crash forwarder with its own origin, subscribing before reporting ready.
- Main validates payloads and actions, and ignores messages that don't come from its own window.
- The in-app fallback appears when main answers false or the IPC fails.
- A probe that fails still settles as `error`, because `probeSource` catches its errors, so the card isn't held back by a bad file.
- The tests, CSS, i18n strings and docs match what the code does.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 11 | $0.64 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 10 | $0.44 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 24 in / 13k out / 450k cache read / 92k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.08</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6ImVmZDUzNDhjLWM3ZmYtNGUzZi1iY2NiLTkyY2JlZjlkYjUxOCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=efd5348c-c7ff-4e3f-bccb-92cbef9db518 -->
