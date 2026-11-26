# kaipu-bench-wachi-v3#60 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18 · github-actions[bot] · 2026-11-26T00:08:44Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Back to the recording page re-floats the card over other apps (confidence medium)**

The guard against asking twice is a `useRef`, so it only lasts as long as one mount. If the user picks a chip on the floating card, main sends the main window to Prepare. When they press Back, `LibraryDetailPage` remounts under the same history entry: `location.key` is the same and `location.state.fromRecording` is still true (library-detail-page.tsx:101, 130-134, 144). `asked.current` is null again, so the hook calls `showRecordingReady` a second time, and the card they just acted on floats on the desktop again.

The in-app card had the same remount reset before this change, since `cardDismissedFor` is plain state. But a window floating over every app is more intrusive than a card in the main window's stack. It also contradicts this hook's own contract ("once per arrival … `key` is its history entry, so a revisit is a new one").

One fix: remember the keys already asked in module scope, or in `history.state` with a `navigate(..., { replace: true, state })`, so the record survives a remount under the same entry.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-26T00:08:44Z

👮 **Wachiman** · 🟡🔐 **Consider · security: `recording-ready:show` accepts any renderer, unlike the card's channels (confidence high)**

The three card channels check `isOwnSender` (lines 109, 114, 123). The `recording-ready:show` handler does not check who is calling. Every window that loads the shared preload gets `showRecordingReady` through the bridge: the capture toast, the capture panel and the floating card itself. Any of them can float an always-on-top, content-protected card for any `assetId`. The payload is validated, so the risk is low.

The repository's review rules call out any widening of the contextBridge. Limiting this handler to the main window's `webContents` (pass a `isMainWindow(sender)` dep from `main/index.ts`) would keep the boundary as narrow as the card's channels.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:146 · github-actions[bot] · 2026-11-26T00:08:44Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: A card renderer that never reports ready loses the card silently (confidence high)**

`show()` returns true as soon as `ensureWindow()` succeeds (line 146). The window only appears after `recording-ready:card-ready` (`present()`, line 221). If `?window=recording-ready` fails to load, or its renderer crashes, there is no `did-fail-load` or `render-process-gone` handling. The page has already been told the window is up, so it hides its in-app fallback, and the question never reaches the user. Nothing tells them.

The PR notes accept this. A cheap guard would close the gap: in `ensureWindow`, reset `rendererReady` on `render-process-gone`, and have the page time out to the in-app card if the window never reports ready.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48 · github-actions[bot] · 2026-11-26T00:08:45Z

👮 **Wachiman** · 🟡📝 **Consider · docs: Docstring says the card closes when the user leaves the page; the floating one does not (confidence high)**

"stays until the user picks something, closes it or leaves the page" is true only for the in-app fallback. The floating window, which is now the main path, has no tie to the page and stays up until an action, ✕ or Escape (recording-ready-window.ts:88-90). Say which variant this sentence describes. Line 47 is also longer than the surrounding comment lines; reflow it.

<!-- wachi:finding -->
