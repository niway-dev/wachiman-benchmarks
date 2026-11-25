# kaipu-bench-wachi-v3#7 [replay r2] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/main/recording/recording-hub.ts:304 · github-actions[bot] · 2026-11-25T21:53:40Z

| 👮 **Wachiman** | A reopen that fails after the bubble is re-shown leaves the face in neither the webcam file nor the screen |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The parked window is swapped for a new, capturable one only when the webcam file ended *before* the Camera toggle came back on (`isParked() && !takeRecordsWebcam()`). The usual way a reopen fails runs in the other order. Main gets the on toggle, `takeRecordsWebcam()` is still true, and `show()` brings back the parked window (lines 304-305). The renderer then calls `turnWebcamOn`, which can fail up to 6 s later: `openWebcamWithin` waits 3 s, then the feed race waits another 3 s (recorder-engine.ts:784-816). It calls `endWebcam` → `onWebcamEnded` → `recordingWebcamEnded`, and main only runs `applyProtection()` on that same window (recording-hub.ts:456-460). The hub's own comments (lines 301-303 and 310-313) say a running capture leaves out the windows that were on screen when it started, and only a *new* window gets recorded. So lifting protection does not put this window back into the capture. For the rest of the take, the face is recorded neither in the webcam file (ended) nor in the screen. The store still sets `webcamUnavailable` on the premise that "the face went to the screen" (recorder-store.ts:946-951, 797). Fix: in the `recordingWebcamEnded` handler (and the webcam write-failure path at line 472), when the active take's bubble was parked and then re-shown, destroy it and `show()` a fresh window, as line 304 does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938 · github-actions[bot] · 2026-11-25T21:53:40Z

| 👮 **Wachiman** | Comment says a following off waits on the queue, but the off path runs synchronously |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says "On the queue, so an off that follows waits for this camera to open and releases it". The off branch (lines 924-934) calls `handle.turnWebcamOff()` at once, not through `queue`. What actually releases a late camera is the engine's `cameraRequest` bump: `turnWebcamOff` increments it, and `turnWebcamOn` stops a superseded stream (recorder-engine.ts:771-772, 790-792, 810). The comment should say that the engine discards a camera that opens late.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T21:53:40Z

| 👮 **Wachiman** | The "late frame is dropped and closed" path is never exercised or asserted |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says a frame the old camera still delivers after `cut()` is "dropped (and closed), not relayed". But `cut()` cancels the reader (webcam-relay.ts:66-70), so `first.push(late)` throws on the cancelled controller and is swallowed by the try/catch. The branch in webcam-relay.ts:91-93 that closes a frame read after the reader was replaced never runs, and nothing checks `late.close`. The test only shows that a frame which never got enqueued is not written. To cover that branch, the test needs a frame already queued when the cut happens, for example by pushing it before `relay.cut()` without flushing, then asserting `expect(late.close).toHaveBeenCalled()`.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/architecture/decisions/0032-webcam-is-its-own-track-and-the-bubble-is-excluded-from-capture.mdx:71 · github-actions[bot] · 2026-11-25T21:53:40Z

| 👮 **Wachiman** | Is "the webcam file keeps running, holding its last frame" verified against mediabunny? |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The decision says the file keeps running on the same clock through an off period, holding its last frame. webcam-relay.ts:9-11 relies on the same thing: mediabunny, given an explicit frame rate, would keep writing the last frame while the relay track carries none. mediabunny is not installed in this checkout, so I could not confirm that `MediaStreamVideoTrackSource` repeats frames on an idle track. It may just write nothing until the next frame, so the previous sample's duration stretches across the gap. The editor hides the gap either way, but the two behaviours give different files and possibly different `durationMs`/encodedSize behaviour. The ADR already lists the hidden-then-shown window as unverified. Should this claim be listed there too, or has it been checked?

<!-- wachi:finding -->
