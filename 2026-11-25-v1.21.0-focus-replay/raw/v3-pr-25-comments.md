# kaipu-bench-wachi-v3#25 [replay r2] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:146 · github-actions[bot] · 2026-11-25T22:59:23Z

| 👮 **Wachiman** | \`show\` answers true before the card can paint, so a failed load or a crashed card renderer loses the card silently |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`show()` returns true as soon as `ensureWindow()` has created the BrowserWindow (line 146). The window only appears later, in `present()`, after the card renderer sends `recording-ready:card-ready` (lines 108-112, 221). The load is fire-and-forget: `void browserWindow.loadURL/loadFile` at lines 261-267 drops the rejection. Nothing listens for `did-fail-load` or `render-process-gone` either. If the page never loads or its renderer dies, `ready()` never arrives and nothing is shown. The main window has already been told `true`, so `useFloatingReadyCard` never sets its fallback (use-floating-ready-card.ts:26-28) and the in-app card is suppressed. That contradicts the hook's "never lost" promise, and the user sees no card and no error.

A renderer that crashes after its first `ready` has a second problem. The window is not `closed`, so `rendererReady` stays true. Later `show()` calls then send into a dead webContents and still return true.

Fix: drop the window and reset `rendererReady` on `render-process-gone` and `did-fail-load`, and log the rejected load. Optionally, resolve the `recording-ready:show` invoke only after `card-ready`, with a timeout, so the page can fall back.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48 · github-actions[bot] · 2026-11-25T22:59:23Z

| 👮 **Wachiman** | Docstring still says the card goes away when the user leaves the page |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The updated comment says the card stays "until the user picks something, closes it or leaves the page". The floating window (`RecordingReadyCard` / `RecordingReadyWindow`) does not close on navigation: it stays up until an action, ✕ or Escape (recording-ready-window.ts:88-90). Only the in-app fallback goes away on leaving the page. Line 47 also runs well past the width of the surrounding lines.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-25T22:59:23Z

| 👮 **Wachiman** | Remounting under the same history entry asks for the floating card again |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useFloatingReadyCard` remembers that it already asked in a component ref (`use-floating-ready-card.ts:18`), and `cardDismissedFor` is component state (line 129). Both are lost when the page unmounts. If the page remounts under the same history entry (a history Back to `/library/:id` that still carries `state.fromRecording`), `showCard` is true again with the same `location.key`, the ref is `null`, and main is asked to float the card again. The card then reappears on the desktop, over whatever app is in front, after the user already acted on it or dismissed it.

The in-app Back buttons on Prepare push `/library/:id` with no state (`prepare-page.tsx:129,152`), so they don't trigger this. Only real history Back does, and the old in-app card had the same reset. The difference is that a repeat now pops a window outside the app, which goes against the doc's "asks main once per arrival" and "the card never shows twice".

Possible fix: remember the keys already asked in a module-level `Set`, or mark the history entry with `navigate(..., { replace: true, state: { ...state, fromRecording: false } })` once the card has been shown.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/floating-ready-window.md:51 · github-actions[bot] · 2026-11-25T22:59:23Z

| 👮 **Wachiman** | "The card never shows twice" holds only while the page stays mounted |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The once-per-arrival guard is a ref in the hook (`use-floating-ready-card.ts:18-24`), so it does not survive a remount under the same history entry (see the finding on `library-detail-page.tsx:141`). Either soften the sentence or make the guard outlive the component.

<!-- wachi:finding -->
