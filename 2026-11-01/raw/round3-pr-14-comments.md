=== COMMENT 4437284861 apps/kaipu-record/src/main/recording/recording-ready-window.ts:223
👮 **Wachiman** · 🟡🐛 **Consider · bug: A reused window can show the previous take's card for a frame**

After ✕ or an action, `close()` hides the window (line 153), but the card renderer still holds the old payload. On the next take, `present()` sends the new payload and calls `showInactive()` in the same tick (lines 223–225). The renderer has not repainted yet, so the hidden window's last frame (the old recording's duration and size) can appear briefly before the new card replaces it. One option: have the card clear its state when it is dismissed. Another: show the window only after the card has painted, for example on the first `resize` after a payload.

<!-- wachi:finding -->

=== COMMENT 4437284867 apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48
👮 **Wachiman** · 🟡📝 **Consider · docs: Doc comment says the card goes away when the user leaves the page**

The updated comment still says the card "stays until the user picks something, closes it or leaves the page". That is only true of the in-app fallback. The floating window (`recording-ready-window.ts:89-90`) has no tie to the page and stays until an action, ✕ or Escape. Reword the comment so it covers both cases.

<!-- wachi:finding -->

