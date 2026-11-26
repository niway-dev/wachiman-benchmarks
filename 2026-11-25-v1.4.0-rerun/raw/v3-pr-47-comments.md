# kaipu-bench-wachi-v3#47 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:943 · github-actions[bot] · 2026-11-25T23:59:16Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A superseded turnWebcamOn closes the gap before the camera is back (off→on→off→on) (confidence high)**

Take this sequence: on, then off, then on again, all while the first `turnWebcamOn` is still opening the camera.

1. The first on is queued. `webcamParked` becomes false.
2. The off runs right away, not on the queue. `turnWebcamOff` bumps `cameraRequest` (recorder-engine.ts:772), and `gaps.open` does nothing because a gap is already open.
3. The second on sets `webcamOn = true` and queues behind the first.
4. The first `turnWebcamOn` now sees `request !== cameraRequest`. It stops its stream and returns "ok" (recorder-engine.ts:790-792).
5. Back here, `webcamOn` is already true because of the second on, so `gaps.close(takeTimeMs())` closes the gap. The second camera has not delivered a frame yet.

From then until the second camera's first frame, or until the file ends if that reopen fails, the editor shows the held frozen frame. Nothing hides it and nothing tells the user. Opening a camera can take up to `WEBCAM_OPEN_TIMEOUT_MS`, so this does not need very fast toggling.

The comment at line 938 says an off that follows waits on the queue. It doesn't: the off branch runs synchronously and never touches `queue`.

Suggested fix: return a separate result from the engine for a superseded open (for example "superseded"), and leave the gap open in that case. Alternatively, keep a toggle generation in the forwarder and close the gap only when no later toggle has happened.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:438 · github-actions[bot] · 2026-11-25T23:59:16Z

👮 **Wachiman** · 🟡📝 **Consider · docs: releaseAll's doc comment now sits on releaseWebcam (confidence high)**

`let releaseWebcam` and its own `/** ... */` were inserted between the existing "Frees everything acquired, for a start that failed or a prepared take released" JSDoc (lines 434-437) and `const releaseAll`. Tooling now attaches that first comment to `releaseWebcam`, and `releaseAll` has no doc. Moving the `releaseWebcam` declaration above the old comment fixes it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T23:59:16Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The "cut camera's frame is dropped (and closed)" path is never exercised (confidence high)**

The comment says a frame the old camera still delivers is "dropped (and closed), not relayed", but `relay.cut()` cancels the reader synchronously (`webcam-relay.ts:66-70`), so the stream is already closed and `first.push(late)` throws inside the `try`. The frame never reaches the pump. The branch that drops and closes a stale frame (`webcam-relay.ts:91-93`, `if (current !== reader) { value.close(); break; }`) never runs, and nothing checks `late.close`. The test only shows that a cancelled stream cannot deliver. To cover the branch, read a frame that was enqueued before the cut while the pump is still awaiting `writer.write`, then call `feed` with a new camera and assert `late.close` was called and that `late` is missing from `written`.

<!-- wachi:finding -->
