# kaipu-bench-wachi-v3#115 [replay r2] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-26T20:07:48Z

| 👮 **Wachiman** | \`recording-ready:show\` handler does not check who is asking |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The three card-to-main channels (`card-ready`, `resize`, `action`) are guarded by `isOwnSender`. `recording-ready:show` is an `ipcMain.handle` with no sender check (lines 104-107). The payload is validated by `parseRecordingReadyPayload`, but any window that loads the shared preload (capture overlay, capture panel, the card window itself) can float a card for an arbitrary `assetId`, and the Open/chip hand-offs then navigate the main window to that id. All those windows are first-party, so this is hardening and not an exploit. Checking `event.sender` against the main window would make the trust boundary match the other channels. The main window is not reachable from this class, so it needs a dep or a `showRecordingReady` guard in `index.ts`.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/index.ts:899 · github-actions[bot] · 2026-11-26T20:07:48Z

| 👮 **Wachiman** | Hand-off brings the main window forward without \`app.focus({ steal: true })\` |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

`openInMain` calls only `showMainWindow()` (index.ts:449-457: restore, show, focus). The floating card is a non-activating macOS panel, so the app can be inactive when the user presses a chip, Edit first or Open. The other paths that raise the app from such a state also call `applyDockPolicy()` and `app.focus({ steal: true })`: `bringAppToFront` (index.ts:559-563) and `applyStopWindowState` (recording-hub.ts:755-756). The backlog doc says this was not run in Electron yet. Did you check that the main window comes in front of another app after a press on macOS, or does it only get ordered in behind the frontmost app?

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:219 · github-actions[bot] · 2026-11-26T20:07:48Z

| 👮 **Wachiman** | Re-showing a hidden card can flash the previous recording's card |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

`close()` only hides the window, and the card renderer keeps its last payload. On the next `present()`, `webContents.send(payload)` and `showInactive()` run back to back in main (lines 223-225). The window can become visible before the renderer has rendered the new payload, so the old recording's duration and size, at the old height, may show for a frame or two. This is untested in Electron. Having the card report once it has rendered the new payload, or sending a clear on `close()`, would avoid it. Since the doc says QA is pending, check it there.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.module.css:1 · github-actions[bot] · 2026-11-26T20:07:48Z

| 👮 **Wachiman** | 16 px window padding is smaller than the card's shadow, so the shadow will be cut at the window edge |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The comment here and in main.css say the 16 px inset is there "so its shadow shows". The card reuses `.card` from status-card.module.css:11, whose shadow is `0 30px 80px -30px rgba(0,0,0,.8)`. That blur reaches about 40 px past the card at the sides and more below it, well beyond 16 px. In a transparent window the shadow will end in a hard rectangular edge at the window border instead of fading out. Nothing in the tests covers this, and the doc says the shadow is not yet checked in Electron. Either raise READY_WINDOW_PADDING, which main.css:80 and recording-ready-window.ts:18 must keep in sync, or give the floating card a tighter shadow. Check it in a real window.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18 · github-actions[bot] · 2026-11-26T20:07:48Z

| 👮 **Wachiman** | "Once per arrival" does not survive a remount, so Back re-floats the card |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The `asked` ref lives in the page component, so it resets whenever the page remounts. After a chip or Edit first, the hand-off navigates the main window to Prepare or the editor. Going Back lands on the same history entry, with the same `location.key` and the same `fromRecording` state. The page remounts, `showCard` is true again, and a new floating card opens over whatever app the user is in. The in-app card did the same on remount, so this is not a regression. But a desktop-wide notification the user already acted on is much more intrusive than a card inside the app. The doc (floating-ready-window.md:48-51) and the hook comment promise it is asked for "once per arrival". Consider recording the answered `key` somewhere that outlives the component, such as a module-level set or `history.replaceState` to clear `fromRecording`. If the repeat is intended, say so in the doc.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/floating-ready-window.md:30 · github-actions[bot] · 2026-11-26T20:07:48Z

| 👮 **Wachiman** | "Every action closes the window, then shows and focuses the main window" is not true of ✕ and Escape |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Dismiss (✕ or Escape) only closes the floating window. According to the card test (recording-ready-card.test.tsx:62-82) it sends `{kind: "dismiss"}`, and `RecordingReadyHandOff` has only prepare, editor and detail targets (use-recording-ready-hand-offs.ts:14-21), so there is no hand-off for it. The sentence reads as if dismissing also raises the main window. Say that only chips, More places, Edit first and Open take the user to the main window.

<!-- wachi:finding -->
