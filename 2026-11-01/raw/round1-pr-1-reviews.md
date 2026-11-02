=== REVIEW 5730178724 2026-11-01T20:43:03Z commit=3ec7a13
👮 **Wachiman** · review of the whole pull request, at `3ec7a13`: all 23 files reviewed.

3 finding(s): 1 to fix, 2 to consider; 3 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** I reviewed part 1 of 2 and found no blockers and two small findings.\n\n**What holds up:**\n- **Bubble window parking:** the camera-bubble window parks during a take that records a webcam file, and finalize, abort and reset all release it. Finalize reads `placedBounds` before `releaseParkedBubble()`, and the renderer sends `recordingStop` only after finalize, so a take that ends with the camera off still records where the bubble was.\n- **Camera off and on in the engine:** turning the camera off releases it and keeps the webcam file running; turning it on reopens it. A request superseded by a later toggle is detected through `cameraRequest`, and the countdown and no-relay cases fall back to ending the file, as before.\n\n**Findings:**\n- **recorder-engine.ts:438 (fix):** the new `releaseWebcam` declaration was inserted between `releaseAll`'s doc comment and `releaseAll` itself, so that comment now describes the wrong variable.\n- **recording-hub.test.ts:2065 (consider):** the test's name covers the hub-reset path, but it only exercises abort.

**Batch 2 of 2.** Part 2 checks out apart from one test gap. I read the gap sanitizer, `WebcamGapLog`, the relay and the editor's gap seeding against their tests and found no wrong assertions. The ADR 0032 and spec updates match the code: the legacy path still applies without a track generator and during the countdown, and a camera still off at the stop leaves a trailing gap. The one finding: the relay test claims a camera frame that arrives after a cut is dropped and closed, but it never exercises that path or asserts the close.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 7 | $0.39 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 6 | $0.24 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 2 batches · $0.63</sub>

<!-- wachi:review -->

<!-- agent-review sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:attempt id=ebef883f-57c6-485f-99be-657ad0630b9b -->

