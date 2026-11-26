# kaipu-bench-wachi-v3#22 [replay r2] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:59:08Z · commit 3ec7a13

👮 **Wachiman** · 🟣 **2 questions for you** · 3 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 1 Should · 2 Could |
| **Risk** | Medium: top fact `concurrency` at `recorder-store.ts:939`, see Risk facts |
| **Needs a person** | 1 direction, in `webcam-relay.ts:53` |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `recorder-store.ts`, `webcam-track.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 📝 docs | [`recorder-engine.ts:438`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L438) | releaseAll's doc comment now documents releaseWebcam |
| 🟡 Consider · Could · 📝 docs | [`recorder-store.ts:938`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L938) | Comment says an off waits on the queue, but the off branch runs right away |
| 🟡 Consider · Could · 🧪 tests | [`webcam-relay.test.ts:79`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts#L79) | The "dropped (and closed)" late-frame path is claimed but never asserted |

### Questions for you (2)

- [`webcam-relay.ts:53`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts#L53) · direction — The relay uses Chromium-only Insertable Streams (MediaStreamTrackProcessor and MediaStreamTrackGenerator) and falls back silently to the old 'off ends the file' behaviour. Someone has to decide whether that silent fallback is acceptable.
- [`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:691`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L691) · open question — The webcam encoder reads a relay track and is given an explicit frameRate and sizeChangeBehavior: Does the installed mediabunny version accept the third constructor argument ({ frameRate }) and repeat the last frame when none arrives? Its package was not under head/node_modules. Files that would answer it: `node_modules/mediabunny/dist/mediabunny.d.ts`.

### Risk facts

- `concurrency` · [`recorder-store.ts:939`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L939) — Camera-on requests are queued while camera-off runs synchronously; a counter in the engine (cameraRequest) decides which request wins.
- `public-contract` · [`webcam-track.ts:72`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/shared/webcam-track.ts#L72) — The on-disk sidecar `webcam` field gains an optional `gaps` array that the editor and later readers consume; older sidecars lack it and read as no gaps.

<details><summary>What the change connects to (5 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- The webcam encoder reads a relay track and is given an explicit frameRate and sizeChangeBehavior (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:691`) — Does the installed mediabunny version accept the third constructor argument ({ frameRate }) and repeat the last frame when none arrives? Its package was not under head/node_modules. Files that would answer it: `node_modules/mediabunny/dist/mediabunny.d.ts`.

**Closed, with the lines they rest on**

- Camera turned off mid-take parks the bubble window instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — The bubble disappears and the in-use light goes off once the renderer stops its preview. Turning the camera back on shows the same protected window. If it fails: If the bubble renderer never gets the broadcast, the window stays hidden with the camera still held until the take ends. Every take-end path destroys it then (recording-hub.ts:499, 554, 846, 1022). Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-282`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-868`.
- Finalize reads placedBounds for a parked bubble before releasing it (`apps/kaipu-record/src/main/recording/recording-hub.ts:498`) — The editor gets the bubble's recorded layout even when the camera was off at the stop. If it fails: recordingStop at recorder-store.ts:685 belongs to a failed begin, which never finalizes. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1042`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1068`, `apps/kaipu-record/src/main/recording/recording-hub.ts:868`.
- turnWebcamOn reopens the camera and feeds the relay (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — In the worst case the call settles after about 2×WEBCAM_OPEN_TIMEOUT_MS. The user does not wait on it; it runs on the forwarder's queue. A failure ends the webcam file, and webcamReopenFailed sets webcamUnavailable at the stop. If it fails: A failed open or no first frame calls endWebcam and returns "unavailable". The store closes the gap and flags the reopen failure. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`.
- Main sanitizes renderer-supplied `webcam.gaps` before writing the sidecar (`apps/kaipu-record/src/shared/webcam-track.ts:184`) — The editor seeds each gap as a hidden webcam segment (webcam-model.ts:111, 135-158), so the lane stripes it and the face is hidden there. If it fails: Malformed input degrades to no `gaps` key, which reads the same as an old sidecar. Gaps are not clamped to durationMs here; the editor clamps them when the duration is known (webcam-model.ts:140-147). Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:170-186`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:106-158`.
- Renderer logs camera-off periods and closes a trailing one at the take's end (`apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:27`) — The gaps are sent with finalize as `webcam.gaps`. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:10-31`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.test.ts:1-38`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 covers the camera toggled mid-take. In the main process the bubble window is parked (hidden, still protected) and released by every take-end path. In the renderer, the bubble releases its camera when the Camera toggle goes off. The engine relays the webcam through a track generator so the file keeps running on the take's clock, the store records the camera-off periods, and the editor seeds those periods as hidden segments. Checked and sound: the ordering of finalize and stop for placedBounds, the countdown fallback (webcamLive is false before begin, so off ends the file, matching main's destroy), and the request counter that releases a camera opening late. Both findings are documentation: a doc comment displaced onto the wrong declaration, and a comment that wrongly says the off toggle waits on the queue. One premise is still open: that the installed mediabunny honours the third constructor argument ({ frameRate }) that keeps the file running through a gap.

**Batch 2 of 2.** I found no defects in this part; the one finding is optional.

- **Gap sanitizer (`webcam-track.ts`):** it drops malformed or backwards gaps, clamps a start below 0, merges overlaps and caps the list at 1000. It uses no workspace value imports, as the `src/shared` rule requires.
- **Tests:** the expected values in `webcam-model.test.ts` match `gapSegments` (stretching, merging and the end clamp), and `webcam-gaps.test.ts` matches the `WebcamGapLog` code.
- **Docs:** decision 6 in ADR 0032 and the revised spec item 7 describe what `webcam-relay.ts` and `webcam-gaps.ts` actually do.
- **Finding (consider):** a comment in the relay test says a late frame from a cut camera is closed, but the test never checks this. It never runs the relay's own drop-and-close branch either.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 6 | $0.55 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 6 | $0.42 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 14 in / 12k out / 233k cache read / 86k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.97</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6IjIzNzNkYTA2LWFkOTItNGVmMC1iOGI1LTkyM2RhNTBhOTI4ZCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=2373da06-ad92-4ef0-b8b5-923da50a928d -->
