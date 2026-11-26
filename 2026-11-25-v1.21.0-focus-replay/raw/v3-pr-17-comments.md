# kaipu-bench-wachi-v3#17 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:803 · github-actions[bot] · 2026-11-25T22:55:23Z

| 👮 **Wachiman** | Re-open can wait twice WEBCAM_OPEN_TIMEOUT_MS, not the single bound the contract states |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`turnWebcamOn` first awaits `openWebcamWithin(..., WEBCAM_OPEN_TIMEOUT_MS)` (line 784) and then races `webcamRelay.feed(camera)` against a second timer of the same length (lines 803-808). A camera that opens slowly and then sends no frame keeps the bubble shown (protected, with no face recorded anywhere) for up to 2× the timeout before the file ends and the bubble drops to the screen. The interface doc at line 163-164 and the PR's test step 7 ("within about 3 s") describe one timeout. Since the forwarder chains each re-open on `queue` (recorder-store.ts:939), later toggles wait that long as well. Either use one deadline for both steps or document the 2× bound.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938 · github-actions[bot] · 2026-11-25T22:55:23Z

| 👮 **Wachiman** | Comment says a later off waits on the queue, but the off path is not queued |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says "On the queue, so an off that follows waits for this camera to open and releases it." The off branch at lines 924-934 calls `handle.turnWebcamOff()` synchronously, outside `queue`. What makes this safe is the engine's `cameraRequest` supersession (recorder-engine.ts:771-772, 790-793, 810). Each toggle bumps the counter, and a camera that opens after it is superseded gets stopped. The code works, but the comment describes a mechanism that isn't there. Please reword it to point at the engine's supersession.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T22:55:23Z

| 👮 **Wachiman** | The comment says a late frame is "dropped (and closed)", but the test never checks that |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`relay.cut()` cancels the old reader (`webcam-relay.ts:66-70`). Cancelling closes the fake camera's stream, so `first.push(late)` throws inside the `try` and the frame never reaches the pump. Nothing runs the relay's `current !== reader` branch, which closes a frame that arrives after the switch (`webcam-relay.ts:91-94`), and the test never checks `late.close`. The test still shows that a cut camera's frames don't get through. But the close-on-switch path that the comment describes has no coverage. One way to cover it: call `feed` with a second camera while the first one's read is still pending and its frame is already queued, then check `late.close`. Or drop "(and closed)" from the comment.

<!-- wachi:finding -->
