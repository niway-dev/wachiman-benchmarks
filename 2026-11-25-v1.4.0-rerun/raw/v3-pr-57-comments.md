# kaipu-bench-wachi-v3#57 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939 · github-actions[bot] · 2026-11-26T00:08:04Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A queued camera-on can open the camera after the user has already turned it off again (confidence high)**

Camera-on goes onto `queue` (line 939), but camera-off calls `handle.turnWebcamOff()` straight away (line 928). The queued callback calls `handle.turnWebcamOn()` without checking whether the camera is still wanted on.

Here is how it goes wrong. An on is queued behind something still pending: a mic `setMicrophoneEnabled` that is opening a device, or an earlier `turnWebcamOn` that is still opening the camera (rapid off→on→off→on→off). The last off then runs first. It sets `cameraWanted = false` in the engine (recorder-engine.ts:771). When the queued on finally runs, `turnWebcamOn` sees `cameraWanted === false`, sets it back to true and opens the camera (recorder-engine.ts:781-806).

The result: the toggle shows Camera off and main has parked (hidden) the bubble, yet the in-use light is on. The user's face is written into `<name>.webcam.mp4` until the next toggle or the end of the take. The gap stays open (`webcamOn` is false at line 943), so the editor hides that footage, but the raw file holds video the user turned off, and nothing tells them.

The comment at line 938 says an off "waits for this camera to open and releases it". That is not true, because the off is not queued.

Fix: start the queued callback with `if (!webcamOn) return;` (and leave the gap open). Another option is to run `turnWebcamOff` on the queue too.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-26T00:08:05Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The "cut camera's late frame is dropped and closed" path is never exercised (confidence medium)**

`relay.cut()` cancels the old reader (`webcam-relay.ts:66-70`). Once a ReadableStream is cancelled it is closed, so `first.push(late)` (`controller.enqueue`) throws a TypeError, which the `try/catch` at lines 80-84 swallows. The late frame never reaches the pump. That means the branch the comment describes (`current !== reader` → `value.close()`, `webcam-relay.ts:91-94`) never runs, and `late.close` is never asserted. The test only shows that a frame which can't be enqueued isn't relayed. To cover the real race, you could enqueue the late frame before calling `cut()` while a `read()` is pending (or hold the pump with a slow writer), then assert `expect(late.close).toHaveBeenCalled()` and that `written` lacks `a2`.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/architecture/decisions/0032-webcam-is-its-own-track-and-the-bubble-is-excluded-from-capture.mdx:67 · github-actions[bot] · 2026-11-26T00:08:05Z

👮 **Wachiman** · 🟡📝 **Consider · docs: Decision 6 leaves out the no-relay and countdown exceptions that the spec and code keep (confidence high)**

The ADR says that in a take that records a webcam file, turning the camera off parks the bubble and keeps the file running. The code only does this when the engine has a relay and the take has begun. `turnWebcamOff` returns false when `!webcamRelay || !webcamLive()` (`recorder-engine.ts:770`), and in that case the store calls `endWebcam()` (`recorder-store.ts:928-934`), which is the old rule. The spec's item 7 states this exception ("still applies where the recorder has no relay track … and during the countdown"), but the ADR, which is the decision of record, doesn't. A reader of the ADR alone would expect the gap behaviour in every take with a webcam file. Suggest adding one sentence matching the spec.

<!-- wachi:finding -->
