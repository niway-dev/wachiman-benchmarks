# kaipu-bench-wachi-v3#27 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:803 · github-actions[bot] · 2026-11-25T23:00:07Z

| 👮 **Wachiman** | Re-opening the camera can take up to 2 × WEBCAM_OPEN_TIMEOUT_MS (6 s), and other live toggles wait behind it |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`turnWebcamOn` runs two timeouts one after the other. First `openWebcamWithin(…, WEBCAM_OPEN_TIMEOUT_MS)` (line 784), then a separate `Promise.race` with a second `WEBCAM_OPEN_TIMEOUT_MS` while it waits for the first frame (803–808). `WEBCAM_OPEN_TIMEOUT_MS` is 3000 (line 286), so the worst case is about 6 s, not the "within about 3 s" the PR's test plan promises. The interface doc at line 164 also suggests a single deadline.

The store also puts this call on the shared live-settings `queue` (recorder-store.ts:939), the same queue that carries mic on/off (902), mic level (864), system-audio volume (881) and ducking (884). While a camera is re-opening, those toggles wait up to 6 s before they apply. One shared deadline for the whole re-open, or keeping the camera re-open off the audio queue, would bound this.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938 · github-actions[bot] · 2026-11-25T23:00:07Z

| 👮 **Wachiman** | Comment says a following "off" waits on the queue, but off runs synchronously |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says "On the queue, so an off that follows waits for this camera to open and releases it". But the off branch (lines 924–934) calls `handle.turnWebcamOff()` directly and never touches `queue`. What actually releases a camera that is still opening is the engine's `cameraRequest` check (recorder-engine.ts:772, 790, 810). The behaviour is correct; the comment describes a mechanism that isn't there.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:943 · github-actions[bot] · 2026-11-25T23:00:07Z

| 👮 **Wachiman** | Fast off→on→off→on: a superseded re-open closes the gap before the camera is back |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Sequence: on (A queued), off, on (B queued after A). The engine answers A with "ok" because it was superseded (recorder-engine.ts:792/810). When A resolves, the second "on" has already set `webcamOn = true`, so `if (webcamOn) gaps.close(takeTimeMs())` closes the gap. B's camera hasn't delivered a frame yet. So the gap ends early, and the held frame shows in the editor while B's camera warms up (up to the re-open timeout). This contradicts the stated rule that a gap closes on the first new frame (webcam-gaps.ts:6–7). It would help if the engine told the caller whether "ok" came from a fed frame or from supersession, and only the first closed the gap.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T23:00:07Z

| 👮 **Wachiman** | The late-frame check never reaches the relay's drop branch |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says a frame the old camera delivers after `cut()` is "dropped (and closed), not relayed", but `cut()` cancels the reader (`webcam-relay.ts:66-70`). Once the stream is cancelled, `controller.enqueue` throws, so `first.push(late)` always ends up in the `catch`. The branch that closes a frame from a stale reader (`webcam-relay.ts:91-93`) never runs, and nothing asserts `late.close`. The test passes whether or not that branch works. To exercise it, read a frame that was queued before the cut (enqueue it before calling `relay.cut()`), then assert `late.close` was called and that it is not in `written`.

<!-- wachi:finding -->
