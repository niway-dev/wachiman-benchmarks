# kaipu-bench-wachi-v3#22 [replay r2] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:438 · github-actions[bot] · 2026-11-25T22:59:08Z

| 👮 **Wachiman** | releaseAll's doc comment now documents releaseWebcam |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The new `let releaseWebcam` and its own JSDoc sit between the existing "Frees everything acquired, for a start that failed or a prepared take released…" block (lines 434-437) and `releaseAll` (line 440). Editors and doc tooling now attach that block to `releaseWebcam`, so `releaseAll` has no comment and `releaseWebcam` has two. Move the declaration above the old comment.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938 · github-actions[bot] · 2026-11-25T22:59:08Z

| 👮 **Wachiman** | Comment says an off waits on the queue, but the off branch runs right away |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

"On the queue, so an off that follows waits for this camera to open and releases it" is not what the code does. Only the on branch is queued. The off branch (lines 924-934) calls `handle.turnWebcamOff()` synchronously while `turnWebcamOn` may still be waiting. The camera that opens late is released by the engine's `cameraRequest` check (recorder-engine.ts:790-793 and 810), not by any ordering on the queue. Reword the comment to name that mechanism, so nobody later relies on ordering that isn't there.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · github-actions[bot] · 2026-11-25T22:59:08Z

| 👮 **Wachiman** | The "dropped (and closed)" late-frame path is claimed but never asserted |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The comment says a frame the old camera still delivers after `cut()` is "dropped (and closed), not relayed", but the test never checks `late.close`. Because `cut()` cancels the reader (`webcam-relay.ts:69`), `first.push(late)` most likely throws on the cancelled controller, and the catch swallows it. That means the relay's own drop branch (`webcam-relay.ts:91-93`, `value.close()` when `current !== reader`) never runs here. Only `written` shows the frame was not relayed. The fix is to assert `expect(late.close).toHaveBeenCalled()` when the push succeeds, or to reword the comment. A separate case where the frame is read before the cut but written after it would actually cover the close branch.

<!-- wachi:finding -->
