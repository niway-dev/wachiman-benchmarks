=== COMMENT 4437284710 apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:438
👮 **Wachiman** · 🟠📝 **Fix · docs: The JSDoc for `releaseAll` now sits on `releaseWebcam`**

The new `releaseWebcam` declaration and its own doc comment were added between the existing JSDoc ("Frees everything acquired, for a start that failed or a prepared take released…", lines 434–437) and `const releaseAll` (line 440). Because two doc blocks now come one after the other, editors and tooling attach the `releaseAll` description to `releaseWebcam`, and `releaseAll` has no doc. Move the `releaseWebcam` declaration and its comment above the `releaseAll` JSDoc.

<!-- wachi:finding -->

=== COMMENT 4437284713 apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938
👮 **Wachiman** · 🟡📝 **Consider · docs: Comment says a later "off" waits on the queue, but the off branch is not queued**

The comment says "On the queue, so an off that follows waits for this camera to open and releases it." The off branch above it (lines 924–934) is not queued. It runs synchronously and calls `handle.turnWebcamOff()` straight away. What actually makes a late camera give way is the engine's `cameraRequest` counter (recorder-engine.ts lines 772 and 790–793): the camera opened late finds `request !== cameraRequest` and stops itself. Rewording the comment to describe that mechanism would stop a later edit from relying on an ordering that does not exist.

<!-- wachi:finding -->

=== COMMENT 4437284717 apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79
👮 **Wachiman** · 🟡🧪 **Consider · tests: The 'late frame is dropped and closed' path is never exercised**

The comment says a frame the old camera still delivers after `cut()` is "dropped (and closed), not relayed". In this fake, though, `cut()` cancels the reader (`webcam-relay.ts:69`), so the stream is already closed and `first.push(late)` throws inside the `try/catch`. The frame never reaches the pump. So the branch at `webcam-relay.ts:91-93` (`current !== reader` → `value.close()`) is never covered, and `late.close` is never checked. To cover it, enqueue the frame before the cut is processed, for example push it and call `relay.cut()` without flushing in between. Then assert `expect(late.close).toHaveBeenCalled()` and that `written` does not contain `a2`. If the throwing path is the only case you meant to test, rewrite the comment to say so.

<!-- wachi:finding -->

