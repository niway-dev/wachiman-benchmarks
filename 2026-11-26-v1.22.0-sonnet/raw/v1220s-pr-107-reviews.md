# kaipu-bench-wachi-v3#107 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:04:52Z · commit 3ec7a13

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 2 questions for you · 4 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 4 to consider · ⚪ 0 for your information (5) · 4 Should · 1 Could |
| **Risk** | Medium: top fact `public-contract` at `webcam-track.ts:72`, see Risk facts |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `webcam-track.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts`, `recorder-engine.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recorder-store.ts:939`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L939) | A queued camera-on can open the camera after the user has turned it off again |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · ❓ question | [`recorder-engine.ts:709`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L709) | Is the third constructor argument and the held-frame behaviour verified against mediabunny 1.61? |
| 🟡 Consider · Should · 🧹 cleanup | [`recorder-engine.ts:434`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L434) | New doc comment was inserted between releaseAll's JSDoc and releaseAll |
| 🟡 Consider · Should · 🧪 tests | [`recording-hub.test.ts:2065`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/recording-hub.test.ts#L2065) | Test title claims the hub reset path, which is not exercised; the stop path is untested too |
| 🟡 Consider · Should · 📝 docs | [`2026-10-30-webcam-track-design.md:329`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/documentation/src/content/docs/specs/2026-10-30-webcam-track-design.md#L329) | Section 3.2 still says a camera turned off ends the webcam file and unprotects the bubble |

### Questions for you (2)

- [`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:48`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts#L48) · open question — Webcam relay: a generator track fed from the live camera by a processor pump: Does mediabunny 1.61 accept a third constructor argument and repeat the last frame on its clock when the relay track is silent? Files that would answer it: `node_modules/mediabunny (type definitions and MediaStreamVideoTrackSource source)`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx`.
- [`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:48`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts#L48) · open question — WebcamRelay feeds the current camera's frames into a MediaStreamTrackGenerator that the encoder reads: Does mediabunny's MediaStreamVideoTrackSource, given an explicit frameRate, keep writing the last frame while a MediaStreamTrackGenerator track delivers none? Its source isn't in the checkout, and every test mocks it. Files that would answer it: `node_modules/mediabunny (after install)`.

### Risk facts

- `public-contract` · [`webcam-track.ts:72`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/shared/webcam-track.ts#L72) — Adds an optional `gaps` field to the `webcam` entry of the stored sidecar, which the editor reads and old sidecars lack.

<details><summary>What the change connects to (5 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Webcam relay: a generator track fed from the live camera by a processor pump (`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:48`) — Does mediabunny 1.61 accept a third constructor argument and repeat the last frame on its clock when the relay track is silent? Files that would answer it: `node_modules/mediabunny (type definitions and MediaStreamVideoTrackSource source)`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx`.
- WebcamRelay feeds the current camera's frames into a MediaStreamTrackGenerator that the encoder reads (`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:48`) — Does mediabunny's MediaStreamVideoTrackSource, given an explicit frameRate, keep writing the last frame while a MediaStreamTrackGenerator track delivers none? Its source isn't in the checkout, and every test mocks it. Files that would answer it: `node_modules/mediabunny (after install)`.

**Closed, with the lines they rest on**

- Camera toggled off mid-take parks the bubble window instead of destroying it; toggled on shows the same window (`apps/kaipu-record/src/main/recording/recording-hub.ts:299`) — The bubble disappears when the camera is turned off and returns in place when it is turned on. The take's face stays out of the screen capture. The recorded bubble position survives a camera that is off at the end. If it fails: `park()` with no window is a no-op, so a later `show()` creates a new protected window mid-take. Whether a running capture excludes it is the same unverified ScreenCaptureKit question the ADR lists.… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-321`, `apps/kaipu-record/src/main/recording/recording-hub.ts:329-335`, `apps/kaipu-record/src/main/recording/recording-hub.ts:493-499`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:81-87`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:236-239`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-266`.
- Camera turned on again mid-take: the engine reopens the camera and feeds the relay (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — The face reappears in the webcam file once a frame arrives. On failure the bubble goes back into the screen and the user sees a notice after saving. The wait is bounded at about 6 s, but it holds the queue shared with the audio toggles. If it fails: An off that arrives while the on is queued (not yet started) does not cancel it, so the camera opens while the toggle is off (finding at recorder-store.ts:939). If stop arrives while the reopen is pe… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:769-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:1130-1145`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`.
- The bubble renderer releases and reopens its camera preview following the Camera toggle (`apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44`) — The in-use light goes off while the bubble is parked, and the preview reopens when the camera is on. If it fails: If `getRecordingSettings` rejects, the error is swallowed and the state stays at its default of on until a broadcast arrives. A parked window would then keep the camera until the next toggle. The win… Evidence: `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`, `apps/kaipu-record/src/renderer/src/features/recording/hooks/use-camera-preview.ts:60-73`, `apps/kaipu-record/src/main/recording/recording-hub.ts:285-291`.
- Camera turned off mid-take keeps the webcam file running (relay cut, camera released) and records a gap (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924`) — The editor seeds each gap as a hidden webcam segment, striped in the lane and left out of exports. The camera light goes off during the gap. If it fails: A camera that cannot be reopened, sends no frame within 3 s, or is unplugged ends the file through endWebcam(), closes the gap, and shows the webcamUnavailable toast after the save. The store tests c… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:769-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`.
- Renderer-supplied webcam.gaps accepted into the sidecar by sanitizeWebcamTrackMeta (`apps/kaipu-record/src/shared/webcam-track.ts:184`) — The editor seeds hidden segments from the stored gaps (webcam-model.ts:111). If it fails: Malformed input yields no gaps and never fails the finalize. endMs is not capped to the take duration; seedWebcamScene clamps it only when it is given the duration. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-185`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I reviewed all 14 files of this part. The main-process parking logic and its ordering with finalize and stop hold up. The editor gap seeding, the gap log and the bubble renderer hook have no defects. There is one real bug: in `forwardLiveSettings`, a camera-on that is queued behind other live-settings work is not cancelled by a later off, so the camera can reopen while the toggle is off. Smaller points: a camera reopen can hold the shared queue for about 6 s and delay a mic mute; one orphaned doc comment; and a test title that claims more than it tests. How mediabunny 1.61 behaves with the relay track is unverified. `node_modules` is absent, so I could not read the library, and the engine tests mock the source.

**Batch 2 of 2.** I found nothing that blocks the merge in this part. The `webcam.gaps` sanitizer, the gap log, the relay and its tests are consistent with the engine and store code they exercise. The `shared` file takes only a relative value import, as the rules require. The one finding is a docs note: spec sections 3.2 (line 329) and the timeline paragraph (line 286) still say a camera turned off ends the webcam file, which decision 7 and ADR 0032 decision 6 now contradict for relay takes. I could not check one thing. The relay depends on mediabunny holding the last frame when given an explicit `frameRate`, and mediabunny isn't installed in the checkout. Every test mocks it, so no test in the diff exercises that behaviour.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 25 | $0.58 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 25 | $0.41 |

</details>

<details><summary>Details of findings with no thread (2)</summary>

**New doc comment was inserted between releaseAll's JSDoc and releaseAll (confidence high)** ([`recorder-engine.ts:434`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L434))

The block "Frees everything acquired, for a start that failed..." (lines 434-437) used to document `releaseAll`. The new `/** Releases the webcam relay... */` comment and `let releaseWebcam` now sit between it and `releaseAll` (line 440), so it documents nothing. Move the `releaseWebcam` declaration and its comment above the `releaseAll` JSDoc.

**Section 3.2 still says a camera turned off ends the webcam file and unprotects the bubble (confidence high)** ([`2026-10-30-webcam-track-design.md:329`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/documentation/src/content/docs/specs/2026-10-30-webcam-track-design.md#L329))

Line 329 lists "turned off" among the ways a webcam file ends and leaves the bubble unprotected. Decision 7 (line 86) and ADR 0032 decision 6 now say that where the recorder has a relay, turning the camera off parks the bubble (still protected) and keeps the file running. Only the no-relay and countdown paths still end the file on off. Line 286 has the same problem: "after its last frame (turned off) the layer is not drawn" no longer describes a relay take, where the file holds its last frame and the editor hides it through `gaps`. Qualify both lines or point them at decision 7, so a reader of section 3 does not learn the superseded rule.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 66 in / 32k out / 2.3M cache read / 179k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.00</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6Ijk5ZjFhNGUyLTk4MjItNDkzMi1iOTFjLWJmZTM2MzZjZDJkMiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6Mn0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=99f1a4e2-9822-4932-b91c-bfe3636cd2d2 -->
