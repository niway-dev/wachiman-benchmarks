=== COMMENT 4437282352 apps/kaipu-record/src/main/recording/recording-ready-window.ts:104
👮 **Wachiman** · 🟡🔐 **Consider · security: `recording-ready:show` accepts any renderer, not only the main window**

The card-side channels are gated by `isOwnSender`, but the `recordingReadyShow` handler (lines 104-107) takes any `invoke`. Every window that loads the shared preload (the card itself, the capture toast, overlays, the bar) can make an always-on-top, all-Spaces panel appear with an arbitrary `assetId`. A later action then makes the main window navigate to that id. The payload is validated, so the impact is small. Still, this is a new main-process entry point, and the IPC comment in `ipc.ts:530` describes it as "Main window → main". You could check the sender against the main window's `webContents`, for example with an `isMainWindowSender` dep passed in from `index.ts`, so the code enforces the contract the comment describes.

<!-- wachi:finding -->

=== COMMENT 4437282356 apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48
👮 **Wachiman** · 🟡📝 **Consider · docs: Doc comment still says the card goes away when the user leaves the page**

The updated comment says the card can float in its own window, but it still says it "stays until the user picks something, closes it or leaves the page". The floating window has no tie to the page. `RecordingReadyWindow` only hides on an action, ✕ or Escape (`recording-ready-window.ts:88-90`, `close()` at 150), so navigating away in the main window leaves it up. Suggest changing the wording to "leaves the page (in-app only)" or similar.

<!-- wachi:finding -->

