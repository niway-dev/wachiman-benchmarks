# kaipu-bench-wachi-v3#32 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/main/recording/recording-hub.ts:304 · github-actions[bot] · 2026-11-25T23:52:05Z

| 👮 **Wachiman** | A camera that fails to reopen mid-take leaves the old, once-protected window, which the capture may not record |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

When the camera is turned on again mid-take, the hub sees `takeRecordsWebcam()` still true and shows the same parked window (still content-protected, lines 304-305). The engine then tries to reopen the camera, which can fail (busy, denied, or no frame within `WEBCAM_OPEN_TIMEOUT_MS`, recorder-engine.ts:794-817). In that case it ends the webcam file and reports `recordingWebcamEnded`. The handler only calls `bubbleProtection.webcamEnded` + `applyProtection` on the existing window (lines 456-460). This PR's own reasoning says a running capture keeps leaving out windows that were on screen when it started, and that only a *new* unprotected window is known to be recorded (lines 301-303; camera-bubble-window.ts:40-44). If so, from the failed reopen until the stop the face is in neither the webcam file nor the screen. The store then reports "main put the bubble back in the capture" (recorder-store.ts:946-947) and raises the webcam-unavailable notice, which may be false. The isParked/destroy swap at line 304 covers only a file that ended *while parked*, not one that ends right after the window was shown again. Suggested fix: when `recordingWebcamEnded` arrives during an active take with the camera on, recreate the bubble (destroy then show) instead of only unprotecting it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T23:52:05Z

| 👮 **Wachiman** | The "late frame is dropped (and closed)" path is not exercised |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says a frame the old camera still delivers after `cut()` is dropped and closed. In this test, `cut()` cancels the reader first, so `first.push(late)` throws inside the `try` and the frame never reaches the relay. The branch in `webcam-relay.ts:91-93` (`current !== reader` → `value.close()`) never runs, and the test does not check `late.close`. That branch handles a real case: a `read()` already pending when the camera is cut, which would otherwise leak a `VideoFrame`. To cover it, push the frame while a read is pending and then cut. For example: start the feed without pushing, call `relay.cut()`, then push. Then assert `late.close` was called and `written` does not contain `a2`.

<!-- wachi:finding -->
