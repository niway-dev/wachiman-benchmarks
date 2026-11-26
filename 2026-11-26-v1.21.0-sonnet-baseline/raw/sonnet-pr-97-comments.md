# kaipu-bench-wachi-v3#97 [replay r2] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939 · github-actions[bot] · 2026-11-26T17:35:04Z

| 👮 **Wachiman** | A queued camera-on can reopen the camera after the user turned it off again |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The camera-on branch queues `handle.turnWebcamOn()` on `queue`, but the camera-off branch calls `handle.turnWebcamOff()` straight away (line 928), not through the queue. The comment at line 938 ("an off that follows waits for this camera to open and releases it") is therefore not what happens. Sequence: on#1 is still opening (up to 3 s + 3 s), then off (`cameraWanted=false`, `cameraRequest++`), then on#2 (queued behind #1, `webcamOn=true`), then off#2 (`webcamOn=false`, `turnWebcamOff` runs at once, `cameraWanted` stays false). When #1 finishes and the queue reaches #2, `turnWebcamOn` sees `cameraWanted === false` (recorder-engine.ts:781), so it opens the camera and feeds the relay. The call returns "ok", and `if (webcamOn)` is false, so the gap stays open. The user has the Camera toggle off, the bubble is parked, and the camera light is on and recording into the webcam file until the next toggle or the stop. The same happens when the queue is held by a mic `getUserMedia` or a noise-suppression reopen. Fix: at the top of the queued callback, return early when the camera is no longer wanted, e.g. `if (!active || !webcamOn) return;` before calling `handle.turnWebcamOn()`. Also correct the comment, and add a store test for on, off, on, off while the queue is busy.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-hub.test.ts:2065 · github-actions[bot] · 2026-11-26T17:35:04Z

| 👮 **Wachiman** | Test name claims the hub reset is covered, but only abort is exercised |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`a bubble parked when the take is aborted or the hub reset is destroyed too` only runs `recordingAbort`. The `forceReset` path (`releaseParkedBubble()` at recording-hub.ts:1022) and the stop path in `applyStopWindowState` (line 846) have no test. Split the test, or add cases for `forceReset` and for `recordingStop` with a parked bubble.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.test.ts:105 · github-actions[bot] · 2026-11-26T17:35:04Z

| 👮 **Wachiman** | Gap segments get random ids, so Share's "whole" fingerprint changes on every mount for a take with gaps |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`seedWebcamScene` gives each gap segment `crypto.randomUUID()` (`webcam-model.ts:155`). Share hashes the seeded layer including its segments: `wholeFingerprint` is `hash53(stableStringify(webcam))` (`export-reuse.ts:81-83`), and `share-recording.tsx:126-130` seeds the scene with `initialScene` on each mount. A take with a camera-off gap therefore gets a different fingerprint each time Share opens, so the comment "a second Share reuses the file" no longer holds and every Share re-encodes. Takes without gaps are unaffected (empty `segments`). This test only asserts the ids are unique (line 105), and nothing pins that seeding the same sidecar twice gives the same scene. Derive the id from the gap (for example `webcam-gap-${index}`), and add a test that `seedWebcamScene(x)` equals `seedWebcamScene(x)` for a sidecar with gaps.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-26T17:35:04Z

| 👮 **Wachiman** | The "dropped and closed" late-frame case is not exercised |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The comment at line 79 says a frame the cut camera still delivers is "dropped (and closed), not relayed". `relay.cut()` cancels the reader, so `first.push(late)` throws and is swallowed by the `try/catch` (lines 80-84). The `current !== reader` branch in `webcam-relay.ts:91-94` that closes the frame is never reached, and the assertion `written == [a1, b1]` would pass without it. Either test that branch (a frame already dequeued when `cut()` runs) or reword the comment so it does not claim coverage of the close.

<!-- wachi:finding -->
