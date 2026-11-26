# kaipu-bench-wachi-v3#102 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:943 · github-actions[bot] · 2026-11-26T17:36:51Z

| 👮 **Wachiman** | Off→on→off→on quickly closes the camera-off gap before the camera is back |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Sequence: off (gap opens, `webcamParked = true`), on #1 (queued; the engine opens the camera), off #2 (runs at once, not on the queue: `turnWebcamOff` bumps `cameraRequest`, `webcamOn` goes false then `webcamParked` true, `gaps.open` is a no-op), on #2 (`webcamOn = true`, queued behind #1). When #1 finishes, the engine sees `request !== cameraRequest` and returns "ok" (recorder-engine.ts:790-792, 810). The forwarder reads that "ok" as "the camera is back". `webcamOn` is true again because of on #2, so line 943 runs `gaps.close(takeTimeMs())`. The camera is still off, and on #2 has not opened it yet; that can take up to the open timeout. The sidecar gap ends early, so the editor and export show the frozen last frame as a live face for that stretch. Nothing reports it. Track a per-toggle token in the forwarder, or have the engine return a distinct result for a superseded open, and close the gap only for the open that actually fed a frame.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938 · github-actions[bot] · 2026-11-26T17:36:51Z

| 👮 **Wachiman** | Comment says the off waits on the queue; the off runs immediately |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

"On the queue, so an off that follows waits for this camera to open and releases it" is not what the code does. The off branch (line 928) calls `handle.turnWebcamOff()` directly, not through `queue`. It does not wait. It supersedes the pending open through `cameraRequest`, and the open then releases its own stream. Reword the comment to say that, so nobody "fixes" the off to queue behind the open.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:784 · github-actions[bot] · 2026-11-26T17:36:51Z

| 👮 **Wachiman** | turnWebcamOn can block the live-toggle queue for twice WEBCAM_OPEN_TIMEOUT_MS |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ⚡ perf |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The wait has two sequential bounds: `openWebcamWithin` (3 s) and then the `Promise.race` on the first frame (another 3 s). The worst case is about 6 s. The doc on `LiveWebcamControls.turnWebcamOn` (line 163-164) implies one `WEBCAM_OPEN_TIMEOUT_MS`. The forwarder runs this on its serial `queue` (recorder-store.ts:939), so a mic or system-audio toggle made in that window waits behind it, and the user sees nothing happening. If the camera is merely slow to wake, the whole webcam file ends and the face falls back to the screen. Either document the 2x bound or give the open and the first-frame wait one shared deadline.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:709 · github-actions[bot] · 2026-11-26T17:36:51Z

| 👮 **Wachiman** | Is a third constructor argument supported by MediaStreamVideoTrackSource in mediabunny 1.61.4? |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The relay path passes `{ frameRate }` as a third argument to `new MediaStreamVideoTrackSource(track, encodingConfig, …)`. The comment says it is what mediabunny reads from a camera track so it repeats the last frame through a gap. `node_modules` is not checked out here, so I could not confirm the signature in the pinned 1.61.4 (bun.lock). If the argument is ignored, the generator track has no frame rate, the held-frame behaviour the whole feature depends on does not happen, and TypeScript or the runtime would not necessarily say so. Can you point to the mediabunny option or source that reads it? Is there a test against the real library rather than a mock?

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-hub.test.ts:2065 · github-actions[bot] · 2026-11-26T17:36:51Z

| 👮 **Wachiman** | Test name claims the hub-reset path is covered; it only exercises abort |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

"a bubble parked when the take is aborted or the hub reset is destroyed too" only calls `recordingAbort`. The new `releaseParkedBubble()` in the reset/teardown block (recording-hub.ts:1022) has no test. The finalize test (line 2049) mocks `finalize` to reject, so it never checks that `placedBounds()` (the parked position) reaches the recorded bubble placement. Split out the reset case, and add a finalize that succeeds and asserts the placement comes from the parked window.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:78 · github-actions[bot] · 2026-11-26T17:36:51Z

| 👮 **Wachiman** | The cut-camera test never reaches the relay's stale-frame guard |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The test is named "a cut camera's frames never get through", and its comment says the old camera's late frame "is dropped (and closed)". `relay.cut()` cancels the reader, so the stream is closed. `first.push(late)` then throws and the `catch` swallows it, which means the frame never reaches the relay at all. The branch in `webcam-relay.ts:91-94` (`current !== reader` → `value.close()`) is never run. That branch covers a frame already read when the cut lands. Nothing asserts `late.close` was called either. A regression in that guard would pass this test. Cover it by letting a `read()` resolve after `cut()` but before the next feed, then asserting the frame is not written and that `close` was called. Otherwise, drop the comment's claim.

<!-- wachi:finding -->
