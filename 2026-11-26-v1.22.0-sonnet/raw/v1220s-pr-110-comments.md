# kaipu-bench-wachi-v3#110 [replay] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:208 · github-actions[bot] · 2026-11-26T20:04:29Z

| 👮 **Wachiman** | The ready card relies on content protection alone; the toast it copies is also dismissed before each capture |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The capture toast has two guards. `createCaptureWindowHooks.beforeCapture` calls `dismissToast()`, with the comment "always on top and would land in this shot" (`main/screenshots/capture-window-hooks.ts:55-56`). `setContentProtection` is only the second guard (`capture-toast-window.ts:305-307`). The ready card has no such dismissal: `index.ts` wires nothing into `beforeCapture` for it, and nothing closes it when a new take starts. It stays up, always on top, until an action, ✕ or Escape.

The repo already records where content protection fails. On Windows builds before 10 2004 (19041) it paints the window black in captures instead of excluding it (`area-geometry.ts:81-92`, which is why `fullDisplayBorderAllowed` exists). Beyond that, I don't believe Electron implements it on Linux, and `build:linux` is a packaging target. On those platforms a card the user left up lands in the next screenshot or recording as a black or visible rectangle, with no error or log.

Suggested fix: add a `dismissReadyCard` dep to `createCaptureWindowHooks`, called next to `dismissToast()`, that calls `recordingReady?.close()`. Also close it in the `recordingStart` handler. Alternatively, ask the author to confirm that content protection is relied on deliberately for every shipped platform.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-26T20:04:29Z

| 👮 **Wachiman** | \`recording-ready:show\` does not check who sent it, unlike the other three handlers in this class |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The `card-ready`, `resize` and `action` listeners all return early unless `isOwnSender(event.sender)`. The `recordingReadyShow` handler accepts any sender. `showRecordingReady` is on the shared preload API, so every window that loads the preload can call it: the capture panel, the toast, the bubble and the card itself. Only the main window's recording page is meant to. The payload shape is validated, but `assetId` is a free string. It ends up in a hand-off that the main window turns into a route.

Suggested fix: accept the call only from the main window's webContents. Pass a `isMainWindowSender` dep, as `micLevelsReport` does with `getMainWindow()?.webContents.id`. The impact today is small, because only first-party pages load.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-26T20:04:29Z

| 👮 **Wachiman** | Floating card is asked for again when the page remounts under the same history entry |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The "asked once" guard is a `useRef` in `useFloatingReadyCard` (use-floating-ready-card.ts:18), so it dies with the component. `showCard` depends on `location.state.fromRecording`, which is kept in the history entry. A chip on the floating card hands off to `/prepare/...` (use-recording-ready-hand-offs.ts:31). Pressing Back then remounts this page under the same `location.key` with `fromRecording` still true. The ref is empty and `cardDismissedFor` is reset, so main is asked again and the card floats up a second time. The in-app card had the same remount behaviour, but the floating one is a separate window that the user already acted on. This contradicts the comment here and the doc's "once per arrival". If that is not intended, keep the asked key somewhere that survives a remount (a module-level set, or clear `fromRecording` from the history state after the first ask). If it is intended, the comment and doc should say it re-appears on Back.

<!-- wachi:finding -->
