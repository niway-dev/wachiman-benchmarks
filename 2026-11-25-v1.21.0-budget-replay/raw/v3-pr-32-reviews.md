# kaipu-bench-wachi-v3#32 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:52:05Z · commit 3ec7a13

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 1 to consider · ⚪ 0 for your information (2) · 2 Should |
| **Risk** | Medium: top fact `concurrency` at `recorder-store.ts:939`, see Risk facts |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `recorder-store.ts`, `webcam-track.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recording-hub.ts:304`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/recording-hub.ts#L304) | A camera that fails to reopen mid-take leaves the old, once-protected window, which the capture may not record |

### To consider (1)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🧪 tests | [`webcam-relay.test.ts:79`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts#L79) | The "late frame is dropped (and closed)" path is not exercised |

### Risk facts

- `concurrency` · [`recorder-store.ts:939`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L939) — Turning the camera on mid-take runs on the store's queue: it opens the camera and waits for a first frame (up to about 6 s), while turning it off acts at once and makes the in-flight open count as superseded through a request counter.
- `public-contract` · [`webcam-track.ts:72`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/shared/webcam-track.ts#L72) — This adds an optional `gaps` field to the sidecar's persisted `webcam` meta: sidecars written from now on carry it, and older sidecars without it read as "camera stayed on".

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Camera turned off mid-take parks the bubble instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — Bubble disappears, the in-use light goes off when the bubble renderer and the engine (turnWebcamOff) release their tracks. If it fails: If the renderer misses the broadcast, the hidden window keeps the camera until the take ends; releaseParkedBubble destroys it at finalize/abort/reset/stop. Evidence: `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-266`, `apps/kaipu-record/src/main/recording/recording-hub.ts:333-335`, `apps/kaipu-record/src/main/recording/recording-hub.ts:846`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:769-778`.
- Camera turned on again mid-take reopens the camera into the relay (what bounds the wait) (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — Bubble shows at once; the webcam file resumes after the first frame; the gap closes then. If it fails: On failure endWebcam reports the end; main only unprotects the existing window (see finding); the store marks webcamReopenFailed → webcamUnavailable notice after save. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:286`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:784-818`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-952`, `apps/kaipu-record/src/main/recording/recording-hub.ts:456-460`.
- Finalize records the parked bubble's placement before releasing it (`apps/kaipu-record/src/main/recording/recording-hub.ts:498`) — Editor seeds the webcam layout where the bubble was before the camera went off. Evidence: `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:236-239`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1042`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1068`.
- Camera turned off mid-take: the store asks the engine to park the webcam and opens a gap on the take's timeline (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924`) — The bubble hides and the camera light goes off. The gap reaches the sidecar as `webcam.gaps` and is seeded as hidden editor segments. If it fails: On a toggle during the countdown, `turnWebcamOff()` returns false (engine test 'cannot turn the camera off before the take begins'), so the file ends. Main later destroys and recreates the window whe… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-934`, `apps/kaipu-record/src/main/recording/recording-hub.ts:299-321`, `apps/kaipu-record/src/main/recording/recording-hub.ts:329-331`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx:1688-1691`.
- Camera turned on again mid-take: `turnWebcamOn` runs on the queue, and the result closes the gap or ends the file (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935`) — The webcam toast appears after the take. The editor hides the held frame across the gap. If it fails: Covered by the store tests 'a camera that cannot be opened again…' and 'turned off again while it reopened'. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.test.ts:1625-1661`, `apps/kaipu-record/src/main/recording/recording-hub.ts:301-305`.
- Renderer-supplied `webcam.gaps` sanitized in shared code before it is written to disk (`apps/kaipu-record/src/shared/webcam-track.ts:131`) — Gaps become hidden segments through `seedWebcamScene`/`gapSegments`. If it fails: An end past the recording is not clamped here. `gapSegments` clamps it when `durationSeconds` is passed. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:9-13`, `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 of 2. The park and show flow, the releases at finalize, abort and reset, the gap bookkeeping, the relay and the bounded reopen are consistent with each other. One problem: when the camera fails to reopen right after the parked window was shown again, main only drops protection on that existing window. By the PR's own reasoning that window may not be captured, so the face can be lost from both the webcam file and the screen. The small review budget meant only the key sections of each file were read in full.

**Batch 2 of 2.** I checked this part's tests and docs against the code and found nothing wrong.

- **Gap logic:** `sanitizeWebcamGaps` (drop bad gaps, clamp starts to 0, merge, sort, cap at 1000), `WebcamGapLog` and `gapSegments` (stretching and merging) behave the way their tests say. The expected values in the webcam-model and sanitizer tests are consistent with the code; for example, `ZOOM_LIMITS.minSeconds` is 1.
- **Store:** the off/on handling and the gap bookkeeping match the new store tests, including an off that arrives while the camera is reopening.
- **Docs:** ADR 0032 decision 6 and spec item 7 match the main-process code: the hub parks the bubble only while the take records a webcam file, and otherwise destroys or replaces it. Both docs mark the open questions about ScreenCaptureKit as unverified.

The one finding is a "consider": the relay test claims a late frame from a camera that was cut is dropped and closed, but the frame never reaches the relay in that test, so the branch that closes such frames is never run.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 10 | $0.63 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 11 | $0.57 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 28 in / 15k out / 592k cache read / 98k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.20</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6IjZiN2VmOGVkLTRiZDctNGY4OC05YjcxLWY1Y2U3MmEwMThlMSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MSwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjIsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=6b7ef8ed-4bd7-4f88-9b71-f5ce72a018e1 -->
