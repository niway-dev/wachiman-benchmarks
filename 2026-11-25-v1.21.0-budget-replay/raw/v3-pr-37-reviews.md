# kaipu-bench-wachi-v3#37 [replay r2] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:55:59Z · commit 3ec7a13

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 2 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 2 to consider · ⚪ 0 for your information (3) · 2 Should · 1 Could |
| **Risk** | Medium: top fact `public-contract` at `webcam-track.ts:72`, see Risk facts |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `webcam-track.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts`, `recorder-engine.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recorder-store.ts:939`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L939) | An off that arrives while the queued turn-on is still waiting leaves the camera open with the bubble hidden |

### To consider (2)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 📝 docs | [`recorder-store.ts:938`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L938) | Comment says a following off waits on the queue; it does not |
| 🟡 Consider · Could · 🧪 tests | [`webcam-relay.test.ts:79`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts#L79) | The "dropped (and closed)" late frame is never asserted closed |

### Risk facts

- `public-contract` · [`webcam-track.ts:72`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/shared/webcam-track.ts#L72) — The persisted sidecar's `webcam` field gains an optional `gaps` array that the editor reads to seed hidden segments; older readers ignore it and older sidecars omit it.

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Camera toggled on mid-take while parked: renderer reopens the camera and feeds the relay (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — Bubble is shown again by main; the gap closes when the first frame reaches the relay; if that fails, the file ends and the camera-unavailable notice is shown after save. If it fails: Open is bounded by WEBCAM_OPEN_TIMEOUT_MS and the first frame by another WEBCAM_OPEN_TIMEOUT_MS, so at most two timeouts in sequence. Failure ends the webcam file (endWebcam → onWebcamEnded) and sets… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`.
- Main parks instead of destroying the bubble on camera off during a webcam take; destroys it at finalize, abort, stop and reset (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — Bubble hides and comes back as the same window; it is gone after the take if the camera is still off. If it fails: If the webcam file ended while parked, camera on destroys the parked window and creates a new unprotected one (legacy path). Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:298-336`, `apps/kaipu-record/src/main/recording/recording-hub.ts:494-499`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-846`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1042`.
- Bubble preview follows the Camera toggle via getRecordingSettings and onRecordingSettingsChanged (`apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44`) — While parked, the preview releases the camera so the in-use light goes off. If it fails: If getRecordingSettings rejects, the preview stays on until the next broadcast, which matches the window existing only while the camera is on. Evidence: `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`.
- A renderer-supplied `webcam.gaps` array is sanitized and written to the sidecar, then seeded as hidden webcam segments in the editor (`apps/kaipu-record/src/shared/webcam-track.ts:184`) — The editor seeds each gap as a hidden segment in source seconds (stretched to the minimum segment length and clamped to the duration when known), so the lane stripes it and the face is hidden there. If it fails: Malformed renderer input is dropped entry by entry and cannot reject the whole meta. A store whose reopen failed closes the gap at the failure time, and a gap still open at stop is closed at the take… Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:170-186`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:106-158`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:10-31`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-961`.
- Turning the camera off or on mid-take through the engine's relay (what the engine tests exercise) (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx:1706`) — The camera light goes off, the file holds its last frame, and the editor hides that span. If it fails: A failed or timed-out reopen calls `endWebcam` and returns "unavailable". The store marks the file ended, closes the gap and tells the user once the take is saved. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:769-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-952`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I reviewed all 14 files in part 1 and found one bug worth fixing before merge, plus a misleading comment that goes with it.

The bug is a race in the mid-take camera toggle. The renderer queues "turn the camera back on" behind slower microphone work, but it applies "turn the camera off" immediately. If the user turns the camera on and then off again while that microphone work is still running, the off is applied first. The queued on then runs anyway and reopens the camera. The user's toggle says off and the bubble stays hidden, but the camera light stays on, and the face keeps going into the webcam file during what the sidecar records as a gap. This lasts until the take ends or the camera is toggled again. The comment on `recorder-store.ts:938` says the opposite: that an off waits for the on to finish.

The rest checked out:

- **Bubble window:** at finalize, abort, stop and reset, main records where the parked bubble was before destroying it. The renderer sends stop only after finalize, so that position survives.
- **Camera reopen:** the reopen is limited to two timeouts in a row (opening the camera, then its first frame).
- **Gaps in the editor:** gap seeding into hidden segments is consistent with the recorder's gap times.

I found no risk facts or open questions that need a person to decide.

**Batch 2 of 2.** I found one minor test issue in part 2 and nothing in the code or docs that needs a fix.

- **What I checked:** `sanitizeWebcamGaps` drops bad entries one by one, clamps starts to 0, sorts, merges overlapping gaps and keeps at most 1000. `WebcamGapLog` keeps the first off time when the camera is turned off twice, and closes a gap still open when the take stops. The editor's `gapSegments` stretches short gaps and keeps them inside the recording. The tests in this part match all of that, including the off-again-while-reopening race, which I checked against `recorder-engine.ts:769-819` and `recorder-store.ts:924-961`.
- **Docs:** ADR 0032 decision 6 and spec item 7 describe what the engine and store do. That covers the parked bubble, the relay track, gaps in screen ms, and falling back to the old rule when there is no track generator or the take is still counting down.
- **The test issue (consider):** in the relay test, the comment says a late frame from the turned-off camera is "dropped (and closed)", but nothing checks that it was closed.
- **Risk:** the sidecar format gains an optional `webcam.gaps` field, which other code reads.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 7 | $0.64 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 8 | $0.50 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 20 in / 12k out / 404k cache read / 102k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.14</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6IjMxNWUwN2FiLWU4Y2YtNDAwYS1iMjNmLTc4NDdiYzZjYWYwOCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MiwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=315e07ab-e8cf-400a-b23f-7847bc6caf08 -->
