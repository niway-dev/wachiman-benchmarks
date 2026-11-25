# kaipu-bench-wachi-v3#15 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/index.ts:900 · github-actions[bot] · 2026-11-25T21:54:42Z

| 👮 **Wachiman** | Hand-off brings the main window back without activating the app |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`openInMain` calls `showMainWindow()` (index.ts:449-457: `show()` + `focus()`) and nothing else. Every other place that brings the app back from a floating panel also calls `applyDockPolicy()` and `app.focus({ steal: true })`: `bringAppToFront` (index.ts:559-563), `applyStopWindowState` (recording-hub.ts:752-756) and `revealAbandoned` (recording-hub.ts:556-561). The hub's comment says why: "a window shown without activating the app comes back unfocused, with grey traffic lights". The card is a non-activating `panel` (recording-ready-window.ts:182), so pressing a chip does not activate Kaipu either. After the user switches to another app, a press on TikTok / Edit first / Open can show the main window behind the active app, or unfocused. That breaks the PR's step 5 ("Kaipu comes to the front"), and nothing tells the user. Fix: add `applyDockPolicy(); app.focus({ steal: true });` after `showMainWindow()` in `openInMain`, as `bringAppToFront` does.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-25T21:54:42Z

| 👮 **Wachiman** | \`recording-ready:show\` accepts any sender |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The other three channels check `isOwnSender`. The `recordingReadyShow` handler accepts a payload from any webContents that loads the preload: the card window itself, the capture toast, the capture panel and the overlays all expose `showRecordingReady`. The payload is validated, so the risk is low. Still, only the main window is meant to ask, and restricting the handler to `mainWindow.webContents` would match the rest of this class. Passing a `isMainWindowSender` dep would keep it testable.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-25T21:54:42Z

| 👮 **Wachiman** | A remount under the same history entry floats the card again after the user already acted on it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useFloatingReadyCard` tracks the ask in a ref (`use-floating-ready-card.ts:18`), and the ref only lives as long as the component. Actions taken on the floating card (chip, Edit first, ✕) never reach the page, so `cardDismissedFor` (line 129) is never set for them. Scenario: the user records, the card floats, and they press Edit first, which pushes `/editor/video/:id`. They then use history Back (mouse button or gesture). The page remounts under the original entry, where `fromRecording: true` and the same `location.key` still apply. `asked.current` is null again, and `showRecordingReady` floats the desktop card a second time. The in-app card already came back on Back before this PR, because the dismiss flag is component state too. A window that pops up on the desktop is more intrusive than that, though, and the backlog doc says "the card never shows twice". The page's own Back buttons push a fresh entry without state (`prepare-page.tsx:129,152`), so only history Back triggers this. One fix is to record the asked `location.key` outside the component, for example in a module-level Set or in history state through `navigate(..., { replace: true, state })`.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/floating-ready-window.md:51 · github-actions[bot] · 2026-11-25T21:54:42Z

| 👮 **Wachiman** | "the card never shows twice" does not hold on history Back |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

As the finding on `library-detail-page.tsx:141` explains, history Back to the recording's entry remounts the page and asks main again. The floating card then reappears even if the user already used it. Either fix that, or note it under "Not done".

<!-- wachi:finding -->
