# kaipu-bench-wachi-v3#27 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:00:07Z · commit 3ec7a13

👮 **Wachiman** · 🟣 **1 question for you** · 4 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 4 to consider · ⚪ 0 for your information (4) · 3 Should · 1 Could |
| **Risk** | Medium: top fact `public-contract` at `recorder-store.ts:1109`, see Risk facts |
| **Needs a person** | 1 direction, in `camera-bubble-window.ts:262` |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `recorder-engine.ts`, `recorder-store.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts` |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`recorder-engine.ts:803`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L803) | Re-opening the camera can take up to 2 × WEBCAM_OPEN_TIMEOUT_MS (6 s), and other live toggles wait behind it |
| 🟡 Consider · Should · 📝 docs | [`recorder-store.ts:938`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L938) | Comment says a following "off" waits on the queue, but off runs synchronously |
| 🟡 Consider · Could · 🐛 bug | [`recorder-store.ts:943`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L943) | Fast off→on→off→on: a superseded re-open closes the gap before the camera is back |
| 🟡 Consider · Should · 🧪 tests | [`webcam-relay.test.ts:79`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts#L79) | The late-frame check never reaches the relay's drop branch |

### Questions for you (1)

- [`camera-bubble-window.ts:262`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/camera-bubble-window.ts#L262) · direction — The design relies on ScreenCaptureKit keeping a hidden-then-shown window out of a stream that is already running. The PR lists this as unverified, and only running the app can confirm it.

### Risk facts

- `public-contract` · [`recorder-store.ts:1109`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L1109) — The take's sidecar gains a new optional `webcam.gaps` field that the editor reads back when it seeds the scene.
- `concurrency` · [`recorder-engine.ts:783`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L783) — Overlapping camera toggles are ordered only by the `cameraRequest` counter, which tells a camera that finishes opening late that it was superseded.

<details><summary>What the change connects to (4 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Camera turned off mid-take parks the bubble instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — The bubble hides; its renderer preview follows the toggle (camera-bubble.tsx:44-61, 144) and releases the camera. If it fails: If the webcam file ended while the bubble was parked, the next camera-on replaces the window (legacy path). A bubble still parked when the take ends is destroyed at stop (hub:846), finalize (499), ab… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:304`, `apps/kaipu-record/src/main/recording/recording-hub.ts:329-335`, `apps/kaipu-record/src/main/recording/recording-hub.ts:757`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:422`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1068`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:770`.
- turnWebcamOn re-opens the camera and feeds the relay (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — The face returns to the webcam file; on failure the file ends and the notice shows after the take (recorder-store.ts:1018). If it fails: Bounded by two sequential 3 s timeouts (784-787, 803-808): worst case about 6 s, during which the shared live-settings queue is blocked. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:286`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:784-818`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939`.
- Renderer-supplied `webcam.gaps` are sanitized before they are written to the sidecar (`apps/kaipu-record/src/shared/webcam-track.ts:131`) — The editor seeds one hidden webcam segment per gap (webcam-model.ts:111, 135-158), so the lane shows those spans striped and exports leave the face out there. If it fails: Malformed input becomes no gaps rather than a rejected meta, so an old sidecar and a take without gaps read the same. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-185`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:106-158`.
- The store logs camera-off gaps through turnWebcamOff/turnWebcamOn and closes a still-open gap at the take's end (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924`) — The gaps go to the sidecar in the finalize meta, and a failed reopen produces the post-take toast (tested at recorder-store.test.ts:1625-1644). If it fails: A failed reopen ends the file and the gap at that point, and the user is told after the take. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-961`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:10-31`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.test.ts:1625-1661`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found nothing that blocks the merge. Three findings, all "consider":

- **Slow re-open:** turning the camera back on can take up to 6 s (two 3 s timeouts in a row), not the ~3 s the PR promises, and mic and system-audio toggles wait behind it on the same queue.
- **Inaccurate comment:** a comment in the recorder store describes a queue ordering that the code doesn't use. The behaviour itself is correct.
- **Early gap close:** a fast off→on→off→on sequence can close the gap before the second camera sends its first frame, so the frozen frame shows briefly in the editor.

The park/destroy logic in main and the release of a parked bubble at stop, finalize, abort and reset hold up. The bubble's position is still read before the parked window is destroyed, because the renderer sends the stop after finalize.

The main open point is for the owner: the design assumes ScreenCaptureKit keeps a hidden-then-shown window out of a capture that is already running, and only running the app can confirm that.

**Batch 2 of 2.** I found one thing worth changing in this part, and it is optional: a test that does not cover what its comment claims.

**What I checked**

- **Sidecar gaps:** `sanitizeWebcamGaps` drops bad entries one at a time, clamps starts below 0, sorts, merges overlaps and caps the list at 1000. `webcam-track.ts` stays free of value imports from workspace packages, as the shared-directory rule requires.
- **Editor seeding:** the expected values in `webcam-model.test.ts` match the stretch, clamp and merge rules in `gapSegments`.
- **Store tests:** the gap expectations in `recorder-store.test.ts` match how `forwardLiveSettings` opens and closes gaps, including the case where the camera is turned off again while it reopens.
- **Docs:** ADR 0032 decision 6 and the revised spec item 7 match the code paths I read. That covers the relay path, keeping the old behaviour without a relay or during the countdown, the trailing gap at stop, and the fallback when the camera cannot be reopened.

**Finding (consider, tests)**

- In `webcam-relay.test.ts`, the "cut camera" test wraps the late `push` in a `try/catch`. Because `cut()` cancels the reader, that push always throws, so the relay's drop-and-close branch for stale frames never runs and `late.close` is never asserted. The test would pass even if that branch were broken.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 10 | $0.73 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 8 | $0.50 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 22 in / 15k out / 469k cache read / 104k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.23</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6ImZhM2Y5ZjAyLWU3YTgtNDQ5NS04YWMyLWZiNjJhN2E1ZmVmOCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=fa3f9f02-e7a8-4495-8ac2-fb62a7a5fef8 -->
