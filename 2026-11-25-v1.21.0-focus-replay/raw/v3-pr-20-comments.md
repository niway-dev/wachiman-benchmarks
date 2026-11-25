# kaipu-bench-wachi-v3#20 [replay] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-25T22:55:44Z

| 👮 **Wachiman** | \`recording-ready:show\` accepts any sender |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The card's own channels check `isOwnSender` (lines 109, 114, 123), but the `recordingReadyShow` handler does not check who invoked it. Every window that loads the shared preload can call `showRecordingReady`: the card window itself, the capture toast, and the panels. Any of them can float a card with an arbitrary `assetId`, and a press on that card then navigates the main window to that id. The payload's shape is validated, but its origin is not. Only the main window is meant to ask (see the `ipc.ts:530` comment). Checking that `event.sender` is the main window's `webContents` would keep the new invoke to its one intended caller. That needs a `mainWebContents()` dep, as `openInMain` does for the other direction.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18 · github-actions[bot] · 2026-11-25T22:55:44Z

| 👮 **Wachiman** | Back to the recording page floats the card again |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`asked` is a ref, so it does not survive a remount. Suppose the user presses a chip on the floating card: main navigates to Prepare. They then press Back. `LibraryDetailPage` remounts under the same history entry, with the same `location.key` and the same `fromRecording` state (`library-detail-page.tsx:130-144`). The ref is `null` again, so `showRecordingReady` is invoked and the desktop card pops up over whatever the user is doing. The same happens after ✕. The in-app card also came back on remount, because `cardDismissedFor` is `useState`. But an always-on-top desktop window coming back is far more intrusive, and the hook's doc promises "once per arrival". Keeping the asked keys in module scope (or in a store keyed by `location.key`) would make a Back return stay quiet.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-25T22:55:44Z

| 👮 **Wachiman** | Going Back to the recording page reopens the floating card on the desktop |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useFloatingReadyCard` only skips a repeat request when its `asked` ref already holds `location.key` (`use-floating-ready-card.ts:18-24`). That ref, like `cardDismissedFor` (line 129), is reset whenever the page remounts. Here is the sequence: the user presses a chip on the floating card, and the main window navigates to Prepare (`use-recording-ready-hand-offs.ts:31`). The user then presses Back. The detail page remounts under the same history entry, which still carries `state.fromRecording`. `showCard` is true again, the ref is null, so `showRecordingReady` is called a second time and the always-on-top window comes back, even though the user already acted on it. The same thing happens after dismissing it with ✕ and then navigating away and back. Main handles that ✕ by itself, so the page never learns the card was dismissed.

The in-app card already reappeared on Back before this change. The difference now is that the card opens a desktop window outside the app, and it stays open after the user leaves the page. The doc (`floating-ready-window.md:48-51`) promises "once per arrival". One way to keep that promise is to remember the asked keys somewhere that survives a remount: a module-level Set, or replacing the history state to drop `fromRecording` once the card has been asked for.

<!-- wachi:finding -->
