# kaipu-bench-wachi-v3#117 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:803 · github-actions[bot] · 2026-11-26T20:10:13Z

| 👮 **Wachiman** | Camera turn-on is bounded by two sequential 3 s waits (about 6 s), and it holds the shared toggle queue |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`turnWebcamOn` first awaits `openWebcamWithin(..., WEBCAM_OPEN_TIMEOUT_MS)`, which is capped at 3 s (recorder-engine.ts:1130-1144). Then it races `webcamRelay.feed(camera)` against a second `WEBCAM_OPEN_TIMEOUT_MS` timer (lines 803-808). A camera that opens just inside the first bound and then sends no frame costs about 6 s before the file ends. The PR body says the failure shows "within about 3 s", and the `LiveWebcamControls` doc at line 163-164 reads as one bound.

The store runs this call on the same `queue` as the mic toggle, the mic level, noise suppression, system volume and ducking (recorder-store.ts:939). Until the call returns, those changes wait behind the camera open. A mic unmute right after the camera comes back can be delayed by up to 6 s, with no signal to the user. Consider one deadline for open plus first frame, taken at the start of `turnWebcamOn`. Alternatively, keep the camera work off the audio queue and have it wait only on its own earlier camera calls. Then fix the doc and PR text to match.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:943 · github-actions[bot] · 2026-11-26T20:10:13Z

| 👮 **Wachiman** | Off→on→off→on quickly closes the gap before the camera is back, so the held frame shows in the editor |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`turnWebcamOff` is called directly from the settings listener (line 928), but `turnWebcamOn` is queued (line 939). Take the sequence off, on, off, on while the first on is still opening. The first on is superseded in the engine and returns "ok" (recorder-engine.ts:790-793, 810). When it completes, the store's `webcamOn` is already true because the second on was heard, so `gaps.close(takeTimeMs())` at line 943 runs while the camera is off and the second on has not opened. The gap therefore ends too early. From that moment until the second on's first frame, the file shows the frozen frame and the editor does not hide it. The comment "Turned off again meanwhile: its gap goes on" only holds when no second on has been heard.

Close the gap only when the engine's "ok" is for the request that is current (for example, have `turnWebcamOn` return a distinct result for a superseded call), or close it after the last queued on.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-hub.test.ts:2065 · github-actions[bot] · 2026-11-26T20:10:13Z

| 👮 **Wachiman** | Test name claims the forced-reset path is covered, but only abort is exercised |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test "a bubble parked when the take is aborted or the hub reset is destroyed too" only calls `recordingAbort`. The hub gained `releaseParkedBubble()` in three other places, and none has a test. These are the forced reset (recording-hub.ts:1022), the `applyStopWindowState` call (line 846), and the abort call (line 554), which this test does cover. A regression in the reset or stop calls would leave a hidden, protected bubble window alive after a take. Either add tests for those two paths or rename this one to match what it covers.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:69 · github-actions[bot] · 2026-11-26T20:10:13Z

| 👮 **Wachiman** | Cut-camera test does not reach the guard it names |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The test is titled "a cut camera's frames never get through" and comments that a late frame is "dropped (and closed)". `relay.cut()` cancels the reader, so `first.push(late)` throws on the closed stream (the test swallows that in a try/catch). The `current !== reader` branch in `webcam-relay.ts:91-94`, which closes a frame read just before the cut, never runs. The test also never asserts `late.close`. The check passes because the stream is cancelled, not because the guard works. A test that has `read()` already resolved with a frame when `cut()` is called, and then asserts the frame is closed and not written, would cover it.

<!-- wachi:finding -->
