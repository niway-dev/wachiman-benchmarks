# kaipu-bench-wachi-v3#50 [replay] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:206 · github-actions[bot] · 2026-11-25T23:59:49Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A card left up stays on screen through the next take, and content protection is all that keeps it out of the video (confidence medium)**

The card has no timer (line 90) and nothing closes it when a recording or screenshot starts. The capture toast it copies has `beforeCapture` dismissing it and uses content protection only as a "second guard" (`capture-toast-window.ts:305`). Here, protection is the only guard. The hub already knows protection is not enough on every platform: `fullDisplayBorderAllowed` (`area-geometry.ts:82-92`) says Windows builds before 19041 paint a protected window black instead of leaving it out, and skips the full-display border there. On those builds, and on Linux where `setContentProtection` does nothing, a card the user has not dismissed ends up in the next whole-display recording as a black or visible 452 px panel in the top-right corner, and nothing tells them. Suggested fix: close the card (`recordingReady.close()`) when a take starts (`recordingStart`) and in the screenshot capture hooks, as the toast does. Keep content protection as the second guard.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-25T23:59:49Z

👮 **Wachiman** · 🟡🔐 **Consider · security: `recording-ready:show` accepts any window's invoke (confidence high)**

The card's three `on` channels check `isOwnSender`, but the `show` handler does not check who is asking. The preload exposes `showRecordingReady` to every window that loads it: the capture toast, camera bubble, capture panel, and the ready card itself. Any of them can make main float the card for any asset id. The payload is validated, so the damage is limited to a spurious card and a hand-off to an arbitrary asset id. Still, the contract says only the main window asks (`ipc.ts:530`). Taking a `isMainWindowSender` dep and rejecting other senders, as `micLevelsReport` does (`recording-hub.ts:786`), would enforce that.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18 · github-actions[bot] · 2026-11-25T23:59:49Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Going Back to the recording page floats the card again (confidence medium)**

`asked` is a per-mount ref keyed by `location.key`. If the user picks a chip on the floating card, main navigates to Prepare. If they then press Back, the recording page remounts under the same history entry, which still has `fromRecording` in its state (`library-detail-page.tsx:101`). The ref is null again, so the hook asks main to re-show "Your video is ready" on the desktop, over whatever app is in front. The old in-app card also came back on remount, but only inside the page; now it is an always-on-top window. The doc comment says "once per arrival". Keeping the asked keys in module scope (a `Set<string>`), or replacing the history entry's state once asked, would make Back stop re-asking.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-25T23:59:49Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: No card at all, floating or in-app, until the probe settles (confidence medium)**

Before this change the in-app card showed as soon as `showCard` was true and used `video.durationSeconds` until the probe came back. Now the floating window is only requested once `probeState.status` is `ready` or `error` (line 140). The in-app fallback hangs off that same request, because `inApp` needs `request !== null` (use-floating-ready-card.ts:31). So the card waits on `probeSource` with no timeout, and nothing else can show it.

`useSourceProbe` has no rejection handler on `void probeSource(videoId).then(...)` (use-prepare-copy.ts:51). `probeSource` catches errors inside its `try`, but it does not guard against a read that never resolves (probe-source.ts:28-47). If that read stalls, the page stays at `loading` and the user gets no "Your video is ready" anywhere, with nothing to tell them.

You could cap the wait, for example by asking after a short timeout using `preparable.durationSeconds` and `dimensions: null`, the same values the payload already falls back to on `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-25T23:59:49Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Going Back to the recording's history entry pops the desktop card again (confidence medium)**

`useFloatingReadyCard` remembers what it already asked for in a ref (use-floating-ready-card.ts:18). That ref is lost when the page remounts. After a chip, Edit first or Open on the floating card, main pushes a new route from the detail entry, and that entry still carries `fromRecording` and the same `location.key`. A router Back to it remounts the page, `showCard` is true again (`cardDismissedFor` is reset state) and `showRecordingReady` runs a second time. The always-on-top window then reappears on the desktop after the user has already acted on it.

The old in-app card behaved the same way, but it stayed inside the app. The hook's doc comment says `key` is the history entry "so a revisit is a new one", while a Back revisit has the same key and is still asked again. To make "once per arrival" hold, keep the asked keys at module scope (or in a store that survives a remount), or replace the entry's `fromRecording` state once the ask is made.

<!-- wachi:finding -->
