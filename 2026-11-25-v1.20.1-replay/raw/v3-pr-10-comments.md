# kaipu-bench-wachi-v3#10 [replay r2] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:146 · github-actions[bot] · 2026-11-25T21:54:09Z

| 👮 **Wachiman** | \`show()\` answers true before the card window has loaded, so a renderer that never loads loses the card with no fallback |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`show()` returns `true` as soon as `ensureWindow()` has built the BrowserWindow. `present()` only paints after `recording-ready:card-ready` arrives (line 221). If `loadURL`/`loadFile` rejects (the rejection is dropped with `void` at lines 261/265), or the renderer throws before `api.ready()`, the window never appears. The page has already been told `true`, so it never shows the in-app card. Nothing logs it, and the user just never gets asked "Where do you want to send it?" for that take. The PR body mentions this. A cheap fix is to answer only after `card-ready`, or after a short timeout: keep a pending resolve in `show` and settle it from the `recordingReadyCardReady` handler, or with `false` on `did-fail-load` or the timeout. The window would then be the first choice and the in-app card the real fallback.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-25T21:54:09Z

| 👮 **Wachiman** | \`recording-ready:show\` accepts an invoke from any renderer |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The card's other channels check `isOwnSender` (lines 109, 114, 123). `recording-ready:show` takes a payload from any webContents. The preload exposes `showRecordingReady` to every window, including the capture panel, the toast, the overlay and the card window itself (preload/index.ts:244). Any of them can float a card with an arbitrary `assetId`, and its actions then navigate the main window to that id. The payload is validated, so the impact is small. Still, only the main window is meant to ask (ipc.ts:530). A sender check against the main window's webContents, passed in as a dep like `openInMain`, would close it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48 · github-actions[bot] · 2026-11-25T21:54:09Z

| 👮 **Wachiman** | Docstring still says the card goes away when the user leaves the page |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The updated comment says the card is now mainly a floating desktop window, but it still says it "stays until the user picks something, closes it or leaves the page". The floating window does not close on navigation. `RecordingReadyWindow` hides only on an action, ✕/Escape, or quit (recording-ready-window.ts:149-172), so it outlives the page. Only the in-app fallback goes away with the page.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-25T21:54:09Z

| 👮 **Wachiman** | Floating card outlives the page and the recording it points to |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Once `showRecordingReady` answers true, the page is done with the card. Main keeps the window up until one of its own actions runs (`recording-ready-window.ts:149-172`). The in-app card went away when the page unmounted. The floating one stays always-on-top after the user leaves the page, and also after they delete the recording from this page (`doDelete`, line 212). If the recording was deleted, pressing a chip, Edit first or Open on the card sends the main window to a missing asset ("File not found" or a broken Prepare). One option: close the floating card when the page removes the asset, or have main close it on a library change that drops `payload.assetId`.

<!-- wachi:finding -->
