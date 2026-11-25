# kaipu-bench-wachi-v3#2 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:943 · github-actions[bot] · 2026-11-25T21:49:37Z

| 👮 **Wachiman** | A superseded turn-on closes the gap before the next camera sends a frame |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

Take the sequence on → off → on while the first reopen is still opening. The second on sets `webcamOn = true` (line 936) and queues a second `turnWebcamOn`. The first call then sees `request !== cameraRequest` and returns "ok" (recorder-engine.ts:790-792). Its callback checks `if (webcamOn) gaps.close(takeTimeMs())`, and `webcamOn` is now true because of the *second* toggle, so the gap closes at that moment. The second camera has not opened yet, and no new frame has reached the file.

The editor then shows the frozen held frame from that point until the second camera's first frame arrives. If the second reopen fails, it shows the frozen frame until the file ends, because the `gaps.close` at line 948 is then a no-op. This contradicts the rule stated in webcam-gaps.ts:6-7: a gap closes when the first frame is back. Nothing tells the user.

The check reads the current toggle state, but what matters is whether this request was superseded. Possible fixes: have the engine return a distinct "superseded" result, or count pending turn-ons in the forwarder and close the gap only when this call was the latest on.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:803 · github-actions[bot] · 2026-11-25T21:49:37Z

| 👮 **Wachiman** | A reopen can wait up to twice \`WEBCAM_OPEN_TIMEOUT_MS\` |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`turnWebcamOn` first awaits `openWebcamWithin(..., WEBCAM_OPEN_TIMEOUT_MS)` (line 784). It then races `feed` against a second, fresh timer of the same length (line 806). A camera that opens slowly and then sends no frame keeps the bubble parked and the face out of both files for up to two timeouts before the fallback runs.

The PR's test plan says "within about 3 s", and the `LiveWebcamControls` doc (line 164) describes one timeout. A single deadline, taken before the open and shared by both steps, would match both.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T21:49:37Z

| 👮 **Wachiman** | The late-frame drop path is never exercised or asserted |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The comment says a frame the old camera still delivers after `cut()` is "dropped (and closed), not relayed", but nothing checks `late.close`. `cut()` calls `reader.cancel()` (webcam-relay.ts:66-70), which closes the fake stream, so `first.push(late)` most likely throws inside the `try` and the frame never reaches the reader. That means the branch at webcam-relay.ts:91-93 (`current !== reader` → `value.close()`) never runs in this test. It still passes because `written` is `["a1", "b1"]`, but it would pass just as well if that branch were deleted. To cover it, deliver the frame while the read is still pending. One way: push it on the first camera and call `relay.feed(second.track)` before the pump reads it. Then assert `expect(late.close).toHaveBeenCalled()`.

<!-- wachi:finding -->
