=== COMMENT 4437261028 apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:438
👮 **Wachiman** · 🟠📝 **Fix · docs: `releaseAll`'s doc comment is now attached to `releaseWebcam`**

The new `let releaseWebcam` and its own `/** … */` were inserted between `releaseAll`'s JSDoc (lines 434–437, "Frees everything acquired, for a start that failed or a prepared take released…") and `const releaseAll` (line 440). So the two doc blocks now sit one after the other above `releaseWebcam`. Editors attach the first block to the variable, and `releaseAll` has no doc at all. To fix it, move the `releaseWebcam` declaration and its comment above line 434, so the original block stays right above `releaseAll`.

<!-- wachi:finding -->

=== COMMENT 4437261031 apps/kaipu-record/src/main/recording/recording-hub.test.ts:2065
👮 **Wachiman** · 🟡🧪 **Consider · tests: Test name promises the hub-reset path but only exercises abort**

The test is named "a bubble parked when the take is aborted or the hub reset is destroyed too", but it only drives `recordingAbort`. The reset path, where `releaseParkedBubble()` was added after `bubbleProtection.reset()` (recording-hub.ts:1022), is never exercised, so if someone dropped that call the test would still pass. Either add a reset case or rename the test so it only claims abort.

<!-- wachi:finding -->

=== COMMENT 4437261038 apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79
👮 **Wachiman** · 🟡🧪 **Consider · tests: The "late frame is dropped (and closed)" path is never tested**

The comment says a frame the old camera still delivers after `cut()` is "dropped (and closed), not relayed". But `cut()` (`webcam-relay.ts:66-70`) cancels the reader first, so `first.push(late)` either throws (and the `catch` swallows it) or enqueues into a stream that was already cancelled. Either way, the pump never reads `late`, so the `current !== reader` branch that calls `value.close()` (`webcam-relay.ts:91-93`) never runs. The test also never asserts `late.close`. In a real camera that branch handles a frame that was already queued when the cut happened, and an unclosed `VideoFrame` there leaks GPU memory. One way to cover it: enqueue `late` *before* calling `relay.cut()` without flushing, then assert `expect(late.close).toHaveBeenCalled()` and that `written` does not contain `"a2"`.

<!-- wachi:finding -->

