# kaipu-bench-wachi-v3#117 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:10:13Z · commit 3ec7a13

👮 **Wachiman** · 🟣 **3 questions for you** · 4 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 4 to consider · ⚪ 0 for your information (4) · 2 Should · 2 Could |
| **Risk** | Medium: top fact `concurrency` at `recorder-engine.ts:779`, see Risk facts |
| **Needs a person** | 1 direction and 2 trade-offs, in `camera-bubble-window.ts:262`, `webcam-relay.ts:48` and `recording-hub.ts:301` |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `recorder-engine.ts`, `recorder-store.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts` |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`recorder-engine.ts:803`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L803) | Camera turn-on is bounded by two sequential 3 s waits (about 6 s), and it holds the shared toggle queue |
| 🟡 Consider · Could · 🐛 bug | [`recorder-store.ts:943`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L943) | Off→on→off→on quickly closes the gap before the camera is back, so the held frame shows in the editor |
| 🟡 Consider · Should · 🧪 tests | [`recording-hub.test.ts:2065`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/recording-hub.test.ts#L2065) | Test name claims the forced-reset path is covered, but only abort is exercised |
| 🟡 Consider · Could · 🧪 tests | [`webcam-relay.test.ts:69`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts#L69) | Cut-camera test does not reach the guard it names |

### Questions for you (3)

- [`camera-bubble-window.ts:262`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/camera-bubble-window.ts#L262) · direction — The design depends on a hidden-then-shown native window staying excluded from an already-running ScreenCaptureKit stream. The PR body lists this as unverified and the author could not run the app. The code cannot settle it, so the owner has to confirm it on a real take before this approach is trusted.
- [`webcam-relay.ts:48`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts#L48) · trade-off — The relay uses `MediaStreamTrackGenerator` and `MediaStreamTrackProcessor`, which are Chromium-only, have no DOM types here, and are an unverified assumption for Electron 39. Without them the code silently falls back to ending the webcam file when the camera is turned off. A person should decide whether that silent fallback and the extra non-standard dependency are acceptable.
- [`recording-hub.ts:301`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/recording-hub.ts#L301) · trade-off — If the camera can't be reopened, the fallback relies on a running capture picking up a window that drops its protection. The PR calls this best effort and unverified. The "your face was recorded in the screen instead" notice may then be untrue, with the face in neither file.

### Risk facts

- `concurrency` · [`recorder-engine.ts:779`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L779) — Camera off/on toggles race with an in-flight reopen, a stop and the encoder. A request counter handles the supersession, and the reopen is serialized with audio toggles on a shared queue, so the order of those operations decides the result.
- `public-contract` · [`recorder-store.ts:1109`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L1109) — The finalize meta and the sidecar's `webcam` field gain an optional `gaps` array that main persists, and the editor reads it back.

<details><summary>What the change connects to (7 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Camera turned off mid-take parks the bubble window instead of destroying it; turned on again shows the same window (`apps/kaipu-record/src/main/recording/recording-hub.ts:299-322`) — The bubble disappears when the camera is off and returns in the same place. The raw screen file never shows it. After the take, the parked window is gone. If it fails: If the webcam file ends while the window is parked, `recordingWebcamEnded` drops the protection of a hidden window. The next camera-on replaces it. Whether a running capture then records the new wind… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/recording-hub.ts:456-460`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:81-86`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-271`, `apps/kaipu-record/src/main/recording/recording-hub.ts:854`, `apps/kaipu-record/src/main/recording/recording-hub.ts:919-924`.
- Finalize reads `placedBounds()` before `releaseParkedBubble()`; `recordingStop` also releases a parked bubble (`apps/kaipu-record/src/main/recording/recording-hub.ts:494-499`) — A take that ends with the camera off keeps the bubble's recorded position and size in the sidecar. If it fails: On finalize failure the renderer calls `recordingAbort`, which releases the parked window. No parked window is left behind. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:494-499`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-847`, `apps/kaipu-record/src/main/recording/recording-hub.ts:550-554`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1042-1068`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:236-239`.
- `turnWebcamOn` reopens the camera, feeds the relay and waits for the first frame (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`) — Success: the gap closes at the first frame. Failure: the file ends via `endWebcam`, the engine reports `onWebcamEnded`, main unprotects the bubble, and the take shows the "camera wasn't available" notice after saving. If it fails: The worst case is about 6 s of no face in either file, then the file ends. The shared queue also delays audio toggles meanwhile (finding at recorder-engine.ts:803). The notice says the face was recor… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:1130-1145`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:286`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-953`.
- Bubble preview follows the Camera toggle (`useCameraOn`) so a parked window releases the camera (`apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`) — Parked: the preview stops its camera and the light goes off. On: the preview reopens. If it fails: If the settings read rejects and no broadcast arrives, the preview stays on. The window only exists while the camera is on, except when parked. Outside a take it is destroyed, so this cannot hold the… Evidence: `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:143-144`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:106-110`.
- Camera-off gaps are sent with finalize and validated in main (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`) — The editor seeds each gap as a hidden segment, stretched to the minimum segment length and clamped to the recording length. If it fails: Malformed renderer input is dropped per entry and does not fail the finalize. A gap shorter than a frame period can be dropped. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1095-1110`, `apps/kaipu-record/src/main/recording/area-geometry.ts:112-123`, `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/renderer/src/features/recording/elapsed.ts:30-33`.
- Sidecar `webcam.gaps` is accepted from the renderer and written to disk, and re-read on load (`apps/kaipu-record/src/shared/webcam-track.ts:131`) — Each gap becomes a hidden webcam segment in the editor. The webcam lane shows it striped and exports leave the face out there. If it fails: Malformed gaps are dropped one by one and never fail the whole meta. Both writer paths (`recording-writer.ts:291`, `:331`) and the sidecar read (`webcam-track-state.ts:21`) go through the sanitizer,… Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-185`, `apps/kaipu-record/src/main/recording/recording-writer.ts:291`, `apps/kaipu-record/src/main/library/webcam-track-state.ts:21`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`.
- Camera toggled off and on mid-take keeps the webcam file running through a relay track and records gaps (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx:1602`) — The in-use light goes off while the file keeps running. The editor shows a striped hidden segment. A failed reopen ends the file and shows the post-take toast `webcamUnavailable`. If it fails: Reopen rejected or timed out: `endWebcam` runs, the engine reports `onWebcamEnded`, and the store closes the gap and toasts after the save. The tests cover this case, an off during a reopen, and an u… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:768-820`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:72-123`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx:1693-1767`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found three low-severity issues in this part and no blockers.

- **Turn-on wait (`recorder-engine.ts:803`):** `turnWebcamOn` runs two sequential 3 s bounds, an open and then a first frame, so it can wait about 6 s. The PR body says "within about 3 s". The call also runs on the store's shared queue, so mic and audio toggles wait behind it.
- **Gap closes early (`recorder-store.ts:943`):** if the camera goes off, on, off, on in quick succession, the gap closes before the camera is back. The editor then shows the frozen frame instead of hiding it.
- **Test name (`recording-hub.test.ts:2065`):** the test says the "hub reset" path is covered but only calls abort. The new `releaseParkedBubble` calls in `applyStopWindowState` and the forced reset have no test.

I checked the ordering that looked risky. The renderer sends `recordingFinalize` before `recordingStop`, so finalize reads `placedBounds()` while the window is still parked. The trailing-gap bubble position is kept.

Two things I could not check:

- **mediabunny:** it is not installed in the checkout, and the engine test mocks it. I could not confirm that the engine's third constructor argument, `{ frameRate }`, is honoured. The behaviour of the held frame through a gap is untested.
- **ScreenCaptureKit:** the PR's own unverified assumptions about it also stay open.

**Batch 2 of 2.** Part 2 holds the shared `WebcamGap` type and sanitizer, the tests, and the ADR 0032 and spec edits. I found nothing to fix. I read the sanitizer, the gap-to-segment seeding, the relay, and the engine and store paths the tests exercise, and the new test cases match that code, the sanitizer, the gap log and `gapSegments`. `src/shared` takes no workspace value import. The sidecar is sanitized on both write and read, so unsorted or NaN gaps cannot reach the editor. The ADR and spec match the code: the window is parked and kept protected, gaps are in screen ms, a trailing gap is closed at the take's end, and a failed reopen ends the file. The one note is a relay test, `webcam-relay.test.ts:69`, that passes through stream cancellation and never runs the late-frame guard it names. I did not run any tests.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 27 | $0.71 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 26 | $0.41 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 60 in / 42k out / 2.2M cache read / 194k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.12</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6ImIwNzliNDlhLTU4ZWYtNGNlNC1iZTkzLTcyMzQ3MWIwZDNmMSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=b079b49a-58ef-4ce4-be93-723471b0d3f1 -->
