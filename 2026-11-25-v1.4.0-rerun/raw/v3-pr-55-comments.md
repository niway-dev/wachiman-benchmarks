# kaipu-bench-wachi-v3#55 [replay r2] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:208 · github-actions[bot] · 2026-11-26T00:08:11Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Nothing closes the card before a screenshot or recording; content protection is the only guard (confidence medium)**

The capture toast this copies uses content protection only as a backup. The screenshot hooks dismiss it before every shot first (`dismissToast: () => captureToast?.dismiss()`, `main/index.ts:670`; the toast's own comment at `capture-toast-window.ts:305` calls protection the "Second guard behind `beforeCapture`"). This card has no timer and stays up until the user acts, but nothing closes it before a capture: not the capture-window hooks, and not `recordingStart` in the hub (`recording-hub.ts:647-735`). On a system where `setContentProtection` does not exclude the window, the card ends up in the user's screenshot or recording with no warning. The app already knows such systems exist: `fullDisplayBorderAllowed` (`area-geometry.ts:87-92`) turns the border off on Windows builds older than 19041 because protection fails there. Electron also does not apply content protection on Linux. Closing the card (`recordingReady?.close()`) from the capture hooks and when a take starts would match the toast. The PR's test step 9 only checks macOS.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-26T00:08:11Z

👮 **Wachiman** · 🟡🔐 **Consider · security: `recording-ready:show` accepts a payload from any renderer (confidence high)**

The other three handlers check `isOwnSender`. The `show` handler only parses the payload. It never checks that the sender is the main window, which is the only intended caller (`ipc.ts:530-531`). Every window that loads the shared preload can call `showRecordingReady`: the card itself, the capture toast, the overlay, the panel and the bar. Any of them can float a card for any `assetId` and set the main window's next navigation target. The hub already guards its main-window-only channels with `e.sender.id !== getMainWindow()?.webContents.id` (`recording-hub.ts:786`). Passing a `isMainWindowSender` dep, or the main window getter, and returning false for other senders would keep the bridge as narrow as its contract says.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18 · github-actions[bot] · 2026-11-26T00:08:11Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: The asked-once ref resets on remount, so Back re-floats the desktop card (confidence medium)**

`asked` is a ref, so it lives only as long as this mount. The request key is `location.key` (`library-detail-page.tsx:144`), and `showCard` depends on `fromRecording` and on `cardDismissedFor`, which is component state (`library-detail-page.tsx:129-134`). Take this sequence: the user picks a chip on the floating card, lands in Prepare, then presses Back. The page remounts under the same history entry, so the location state still says fresh recording, and the ref is null again. The hook calls `showRecordingReady` again, and the always-on-top card reappears on the desktop for a recording the user has already acted on. The in-app card also reappeared on Back before this change, but a desktop window popping back up is more intrusive. The doc comment says "a revisit is a new one", but a Back revisit is the same entry. Keeping the set of asked keys in module scope, or in history state, would make it truly once per arrival.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48 · github-actions[bot] · 2026-11-26T00:08:11Z

👮 **Wachiman** · 🟡📝 **Consider · docs: Doc says the card stays "until … leaves the page", which is not true for the floating card (confidence high)**

The floating card lives in main (`recording-ready-window.ts:93-92` docs). Nothing closes it when the main window leaves the recording page: it stays until an action, ✕ or Escape. The new docstring now describes both hosts but keeps the in-app-only "or leaves the page" clause. Line 47 also runs far past the surrounding wrap width.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:140 · github-actions[bot] · 2026-11-26T00:08:11Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: If the file read never finishes, no card appears at all, not even in the app (confidence medium)**

The page only asks for the floating card once `probeState.status` is "ready" or "error". Before this change, the in-app card showed right away using `video.durationSeconds` and filled in the probe's numbers later. `probeSource` catches errors and returns null, but it has no timeout (`features/video-editor/export/probe-source.ts:28-46`). `useSourceProbe` stays on "loading" until the read finishes (`features/prepare/use-prepare-copy.ts:47-66`). So if a `kaipu-media://` read stalls, the request stays null and `inApp` stays false, and the user never sees "Your video is ready", with no error shown. One option is a short timeout after which the page asks anyway with the sidecar numbers. That is what happens today when the read fails (`dimensions: null`).

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:124 · github-actions[bot] · 2026-11-26T00:08:11Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: The floating card no longer goes away when the user leaves the page or deletes the recording (confidence medium)**

The in-app card unmounted when the user left the page, as the comment above still says. The floating window has no such tie to the page. Only its own actions, ✕ or Escape, or the next take close it (`main/recording/recording-ready-window.ts:150-172`). `doDelete` (line 212) removes the recording and navigates to `/library` but never closes the window. A card that stays on screen keeps the deleted asset's `assetId`, so its chips, Edit first and Open send the main window to Prepare, the editor or the recording page for a file that no longer exists. That page then shows "not found". This could be handled by having the page (or main, when it sees a library removal) close the card when its asset is deleted. Otherwise the doc could note it.

<!-- wachi:finding -->
