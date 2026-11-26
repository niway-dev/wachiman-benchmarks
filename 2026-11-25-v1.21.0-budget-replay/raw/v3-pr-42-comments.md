# kaipu-bench-wachi-v3#42 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:803 · github-actions[bot] · 2026-11-25T23:56:59Z

| 👮 **Wachiman** | Re-opening the camera can wait twice WEBCAM_OPEN_TIMEOUT_MS, and it holds up the shared toggle queue |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | ⚡ perf |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`turnWebcamOn` first awaits `openWebcamWithin(..., WEBCAM_OPEN_TIMEOUT_MS)` (784-787), then races `webcamRelay.feed(camera)` against a second, separate `WEBCAM_OPEN_TIMEOUT_MS` timer (802-808). Nothing bounds the call as a whole, so a camera that opens slowly and then sends no frame takes up to 2× the timeout before the file ends. The PR's test step 7 says "within about 3 s".

The store also runs this call on the forwarder's single `queue` (recorder-store.ts:939). Mic on/off, mic level, noise-suppression, volume and ducking changes go through that same queue (recorder-store.ts:864-884, 902), so they wait behind it. Suggested fix: use one deadline that covers both the open and the first frame, measured from the start of `turnWebcamOn`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:943 · github-actions[bot] · 2026-11-25T23:56:59Z

| 👮 **Wachiman** | A superseded re-open closes the gap before the newer camera has sent a frame |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Take this sequence: on (request 1, opening), off (request 2), on again (queued behind request 1). Request 1 sees `request !== cameraRequest` and returns "ok" (recorder-engine.ts:790-792). By then `webcamOn` is already true again because of the second on (line 936), so line 943 closes the gap right away. The newer camera is still opening at that point.

The editor would then show the held frame during the warm-up. The PR says this is exactly what closing the gap on the first new frame is meant to prevent. A fix is to close the gap only when the result belongs to the latest on, for example with a request counter kept in the forwarder.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.test.ts:1646 · github-actions[bot] · 2026-11-25T23:56:59Z

| 👮 **Wachiman** | No test for off → on → off → on while the first reopen is still pending |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This test covers off → on → off while the reopen is pending. It does not cover the case where the camera goes back on before that first `turnWebcamOn` resolves. In that case `webcamOn` is already `true` again (set synchronously at recorder-store.ts:936). The first call then resolves "ok" because the camera was turned off meanwhile (recorder-engine.ts:162-164), and `gaps.close(takeTimeMs())` at recorder-store.ts:943 closes the gap before the second camera's first frame reaches the file. If the second reopen then returns "unavailable", the `gaps.close` at line 948 does nothing, because no gap is open any more. Either way the editor shows the held frame for part of a period the camera was off. A test for this sequence would show whether the gap stays open until the second camera's frames arrive.

<!-- wachi:finding -->
