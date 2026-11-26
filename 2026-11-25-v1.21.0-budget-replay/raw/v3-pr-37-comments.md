# kaipu-bench-wachi-v3#37 [replay r2] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939 · github-actions[bot] · 2026-11-25T23:55:59Z

| 👮 **Wachiman** | An off that arrives while the queued turn-on is still waiting leaves the camera open with the bubble hidden |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Turning the camera on puts `handle.turnWebcamOn()` on `queue` (line 939), but turning it off calls `handle.turnWebcamOff()` straight away (line 928). It does not wait on the queue, whatever the comment on line 938 says. Mic toggles and noise-suppression reopens share this queue and can take a while (`acquireMicrophone`, `reopenMic`, lines 864-908). Suppose the user turns the camera on, then off, while one of those is still running. `turnWebcamOff` runs first. `cameraWanted` is already false, so it changes nothing that matters and returns true (recorder-engine.ts:769-777). Then the queued `turnWebcamOn` runs: `cameraWanted` is false, so it sets it to true, opens the camera and feeds the relay (recorder-engine.ts:781-818). `cameraRequest` was not bumped after this call began, so nothing marks it as superseded. Result: main has parked the bubble (hidden), the user's toggle says off, but the recorder holds the camera with the in-use light on until the take ends or the camera is toggled again. The face is also written into the file during what the sidecar records as a gap, because the gap stays open while `webcamOn` is false. Fix: have the queued task check `webcamOn` before calling `turnWebcamOn`. Or put the off on the same queue, or have `turnWebcamOff` bump a request that a not-yet-started `turnWebcamOn` checks.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938 · github-actions[bot] · 2026-11-25T23:55:59Z

| 👮 **Wachiman** | Comment says a following off waits on the queue; it does not |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The off branch (lines 924-934) calls `turnWebcamOff()` synchronously. It does not chain onto `queue`, so it never waits for this camera to open. Supersession actually comes from `cameraRequest` inside the engine. The comment should say that, or the code should match the comment (see the related finding on line 939).

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T23:55:59Z

| 👮 **Wachiman** | The "dropped (and closed)" late frame is never asserted closed |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The comment says a frame the cut camera still delivers is dropped and closed, but the test only checks `written`. It never checks `late.close`, and the `try/catch` around `first.push(late)` lets the test pass whether the frame reached the relay or `enqueue` threw first. A relay that leaked a late `VideoFrame` without closing it would still pass. You could assert `late.close` was called when the push did not throw, or drop "(and closed)" from the comment.

<!-- wachi:finding -->
