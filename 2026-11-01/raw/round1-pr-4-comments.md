=== COMMENT 4437260458 apps/kaipu-record/src/main/recording/recording-ready-window.ts:225
👮 **Wachiman** · 🟡🐛 **Consider · bug: A re-used hidden window can flash the previous recording's card**

`close()` only hides the window, so its React tree keeps showing the last payload. On the next `show()`, `rendererReady` is still true, and `present()` sends the new payload and calls `showInactive()` straight away (lines 223–225). React has not re-rendered yet at that point, so for a frame or two the window can still show the previous take's duration and size, at the previous card height. You could avoid this by clearing the card when it is hidden: for example, send a null payload on close, or have the card ack the paint before main shows the window.

<!-- wachi:finding -->

=== COMMENT 4437260463 apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48
👮 **Wachiman** · 🟡📝 **Consider · docs: Docstring says the card closes when the user leaves the page, which the floating window does not do**

The updated comment says the card "stays until the user picks something, closes it or leaves the page". That is still true for the in-app fallback. The floating window, though, has no tie to the page: `RecordingReadyWindow` hides only on an action, ✕ or Escape (recording-ready-window.ts:88-90, 149-155). Please name the two cases separately.

<!-- wachi:finding -->

=== COMMENT 4437260467 apps/kaipu-record/src/main/recording/recording-ready-window.test.ts:247
👮 **Wachiman** · 🟡🧪 **Consider · tests: Test name says Edit first is ignored, but the test asserts it closes the card**

After the press, `{ kind: "edit" }` with `canEdit: false` is expected to hide the window (`hide` called once, line 257); only the hand-off is dropped, because `act()` always closes the card before calling `handOffFor`. The name "ignores Edit first" says the press does nothing, which is not what the test checks. Rename it to something like "Edit first the card did not offer closes it without opening anything", or change `act()` if ignoring the press is what you meant.

<!-- wachi:finding -->

