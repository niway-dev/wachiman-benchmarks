=== COMMENT 4437282504 apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938
👮 **Wachiman** · 🟠📝 **Fix · docs: Comment says a later "off" waits on the queue, but the off branch runs right away**

The comment says the turn-on is queued "so an off that follows waits for this camera to open and releases it". The off branch (lines 924–934) never touches `queue`. It calls `handle.turnWebcamOff()` straight away. What actually lets an off cancel a camera that is still opening is the engine's `cameraRequest` counter (recorder-engine.ts:772, 790, 810). The behaviour is fine; the comment describes a mechanism that isn't there. Suggested wording: "queued behind the mic toggles; an off meanwhile supersedes it through the engine's request counter". One side effect is worth knowing: a mic toggle made after a camera-on now waits behind it on `queue`, for up to two `WEBCAM_OPEN_TIMEOUT_MS` (the open, then the first frame).

<!-- wachi:finding -->

=== COMMENT 4437282511 apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:946
👮 **Wachiman** · 🟡🐛 **Consider · bug: If the camera can't be reopened, the face may be recorded nowhere, not "back in the capture"**

The PR's premise (camera-bubble-window.ts:40-44, recording-hub.ts:301-303 and 310-314) is that a running capture leaves out a window that was protected when the capture started, so only a new window gets recorded. On a failed reopen, main has already called `cameraBubble.show()` on the parked window, which was protected at capture start. The `recordingWebcamEnded` handler (recording-hub.ts:456-460) then only unprotects that same window; it does not replace it the way line 304 does. By the PR's own reasoning, the face is then left out of the screen recording too. This comment and the `webcamReopenFailed` docs (line 797, "the face went to the screen") say otherwise, and the user is told the face went to the screen. This is the same best-effort path as an unplugged camera. Could the hub replace a protected window that is still showing when the webcam file ends mid-take, the way line 304 does for a parked one? If not, the comments should say the face may be lost.

<!-- wachi:finding -->

=== COMMENT 4437282517 apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:438
👮 **Wachiman** · 🟡🧹 **Consider · cleanup: The `releaseAll` JSDoc now sits on `releaseWebcam`**

The new `let releaseWebcam` and its JSDoc were inserted between the existing "Frees everything acquired, for a start that failed or a prepared take released…" block (lines 434-437) and `const releaseAll`. That block now documents `releaseWebcam`: two doc comments are stacked and `releaseAll` has none. Move the `releaseWebcam` declaration above the old comment.

<!-- wachi:finding -->

=== COMMENT 4437282526 apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79
👮 **Wachiman** · 🟡🧪 **Consider · tests: The late-frame test never reaches the drop-and-close branch it describes**

The comment says a frame the old camera delivers after `cut()` "is dropped (and closed), not relayed". But `cut()` (`webcam-relay.ts:66-70`) cancels the reader, so `first.push(late)` throws on a closed controller and the `try/catch` swallows it. The frame never reaches the pump, so the `current !== reader` branch at `webcam-relay.ts:91-93` (`value.close(); break;`) never runs, and `late.close` is never checked. The assertion that `written` is `["a1", "b1"]` would pass even if that branch were missing.

To cover the branch, enqueue the late frame before calling `cut()`, or call `feed(second)` while the first reader still has a frame queued. Then assert `expect(late.close).toHaveBeenCalled()`.

<!-- wachi:finding -->

