# kaipu-bench-wachi-v3#12 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939 · github-actions[bot] · 2026-11-25T21:54:21Z

| 👮 **Wachiman** | Camera reopen goes on the shared toggle queue, so a mic mute waits behind it for seconds |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The camera-on path puts `handle.turnWebcamOn()` on `queue`. The mic toggle (`:902`), mic level (`:864`), noise suppression (`:868`), system-audio volume (`:881`) and ducking (`:884`) all use that same queue. `turnWebcamOn` can wait up to `WEBCAM_OPEN_TIMEOUT_MS` in `openWebcamWithin` and then up to `WEBCAM_OPEN_TIMEOUT_MS` again in the feed race (`recorder-engine.ts:784-808`). A user who turns the camera on and then mutes the mic during a busy or slow camera reopen sees the mic toggle off, but the mute reaches the engine only after both waits. The take keeps recording audio they meant to cut, and nothing tells them. The camera on/off pair does not need this queue for ordering: `turnWebcamOff` runs synchronously and supersedes through `cameraRequest`. Keeping camera operations on their own chain would leave the audio controls immediate.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938 · github-actions[bot] · 2026-11-25T21:54:21Z

| 👮 **Wachiman** | Comment says a following off waits on the queue, but off runs synchronously |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

"On the queue, so an off that follows waits for this camera to open and releases it": the off branch (`:924-934`) calls `handle.turnWebcamOff()` directly and never touches `queue`. A camera that opens late is actually released by the `cameraRequest` supersession check in the engine (`recorder-engine.ts:790-792`, `:810`). The comment should describe that mechanism.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-hub.ts:305 · github-actions[bot] · 2026-11-25T21:54:21Z

| 👮 **Wachiman** | After a failed reopen, the face depends on a running capture picking up a dropped protection |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The comment at `:301-303` says a new unprotected window is "the one a running capture is known to record", and it destroys a parked window only when the webcam file has already ended. In the common failure order, turning the camera on shows the parked, protected window first (`:305`). The renderer's reopen then fails up to 2×`WEBCAM_OPEN_TIMEOUT_MS` later, and only `applyProtection` removes the protection from that same window. The fallback the PR promises ("the bubble falls back into the screen recording") therefore rests on the mechanism this comment says is not known to work. Has a running ScreenCaptureKit stream been seen to pick up a protection drop on an existing window? If not, should the webcam-ended handler recreate a window that was shown from a park?

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T21:54:21Z

| 👮 **Wachiman** | The 'late frame is dropped (and closed)' case is never asserted, and the drop branch never runs |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says a frame the old camera still delivers after `cut()` is dropped and closed. But `cut()` cancels the reader first (webcam-relay.ts:66-70), so `first.push(late)` throws into the empty `catch`, and the frame never reaches the pump. As a result, the `current !== reader` branch that calls `value.close()` (webcam-relay.ts:91-94) never runs, and nothing checks `late.close`. The test only shows that the frame was not written. If the frame-closing branch matters (a VideoFrame left open holds camera memory), test it with a frame that is already queued when `cut()` runs: push it before `cut()`, then assert `late.close` was called.

<!-- wachi:finding -->
