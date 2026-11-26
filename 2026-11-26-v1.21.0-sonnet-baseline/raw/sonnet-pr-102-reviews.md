# kaipu-bench-wachi-v3#102 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:36:51Z · commit 3ec7a13

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 question for you · 6 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 6 to consider · ⚪ 0 for your information (7) · 3 Should · 4 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts`, `recorder-engine.ts`, `webcam-relay.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recorder-store.ts:943`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L943) | Off→on→off→on quickly closes the camera-off gap before the camera is back |

### To consider (6)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 📝 docs | [`recorder-store.ts:938`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L938) | Comment says the off waits on the queue; the off runs immediately |
| 🟡 Consider · Could · ⚡ perf | [`recorder-engine.ts:784`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L784) | turnWebcamOn can block the live-toggle queue for twice WEBCAM_OPEN_TIMEOUT_MS |
| 🟡 Consider · Could · ❓ question | [`recorder-engine.ts:709`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L709) | Is a third constructor argument supported by MediaStreamVideoTrackSource in mediabunny 1.61.4? |
| 🟡 Consider · Should · 🧹 cleanup | [`recorder-engine.ts:434`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L434) | New releaseWebcam declaration split the releaseAll doc comment from its function |
| 🟡 Consider · Should · 🧪 tests | [`recording-hub.test.ts:2065`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/recording-hub.test.ts#L2065) | Test name claims the hub-reset path is covered; it only exercises abort |
| 🟡 Consider · Could · 🧪 tests | [`webcam-relay.test.ts:78`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts#L78) | The cut-camera test never reaches the relay's stale-frame guard |

### Questions for you (1)

- [`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:48`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts#L48) · open question — Webcam relay: encoder reads a MediaStreamTrackGenerator fed from the live camera track: Does mediabunny 1.61.4 accept the third constructor argument and repeat the last frame on a frame-rate-less generator track? Files that would answer it: `node_modules/mediabunny (not present in this checkout)`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx`.

<details><summary>What the change connects to (6 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Webcam relay: encoder reads a MediaStreamTrackGenerator fed from the live camera track (`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:48`) — Does mediabunny 1.61.4 accept the third constructor argument and repeat the last frame on a frame-rate-less generator track? Files that would answer it: `node_modules/mediabunny (not present in this checkout)`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx`.

**Closed, with the lines they rest on**

- Camera toggled off mid-take: main parks the bubble window instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — The bubble disappears when the camera is off, and the same window returns when it is on. The in-use light goes off because the bubble renderer stops its preview (`useCameraOn` then `useCameraPreview(false)`). The recorder's own track is stopped by `turnWebcamOff`. If it fails: If the renderer cannot keep the file (turnWebcamOff returns false, so it ends the file), main has already parked. `recordingWebcamEnded` then drops the hidden window's protection, and on destroys and… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/recording-hub.ts:454-460`, `apps/kaipu-record/src/main/recording/recording-hub.ts:491-499`, `apps/kaipu-record/src/main/recording/recording-hub.ts:550-554`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-847`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-271`, `apps/kaipu-record/src/renderer/src/features/recording/hooks/use-camera-preview.ts:69-73`.
- turnWebcamOn: reopen the camera and feed the relay, awaiting the first frame (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — Success: the same file continues and the gap closes. Failure: the file ends, main puts the bubble back in the capture, and the store raises `webcamUnavailable` for a notice after the save. If it fails: The wait is bounded at about 6 s, and the serial live-toggle queue is held for that long. A superseded open returns "ok" without the camera being on, which the forwarder misreads (finding at recorder… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:1102-1145`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`.
- Camera-off gaps are logged in the forwarder and written to the sidecar at stop; the editor seeds them as hidden segments (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017`) — Hidden stripes appear in the webcam lane, and the export leaves the face out during the gaps. If it fails: A `turnWebcamOn` still in flight at the stop is cut off: the open gap is closed at the end, and `webcamReopenFailed` is read before the queue callback can set it, so no notice appears in that case. T… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:806-809`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1015-1018`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:10-30`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`, `apps/kaipu-record/src/renderer/src/features/video-editor/scene.ts:140-153`, `apps/kaipu-record/src/renderer/src/features/library/components/share-recording.tsx:126-129`.
- Camera turned off mid-take keeps the webcam file running and records a gap (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924`) — The editor's webcam lane stripes each off period and the export hides the face there. If the camera cannot be reopened, a toast appears after the save. If it fails: Reopen failure or timeout: `endWebcam()` closes the file, the gap closes at that time, and `webcamReopenFailed` leads to the post-take toast. A malformed or oversized `gaps` array is trimmed in `sani… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1098-1110`, `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-185`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`, `packages/i18n/messages/en.json:319`.
- The renderer sends `webcam.gaps` through finalize to main, which sanitizes it (`apps/kaipu-record/src/shared/webcam-track.ts:184`) — Old sidecars and takes without gaps read the same. If it fails: Non-array input, non-object entries, and non-finite or string numbers are dropped without throwing. The file uses only relative value imports, so the preload-bundle rule holds. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:9-13`, `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.test.ts:152-203`.
- Relay track feeds a new camera track into the same encoder after off then on (`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:74`) — The webcam file keeps running through a camera-off gap, holding its last frame. If it fails: A camera that ends, or sends no frame before the timeout, makes `feed` resolve false and the engine ends the file. `stop()` closes the writer and stops the generator. A frame already read when a cut… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:66-122`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:655-665`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:769-819`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 parks the camera bubble instead of destroying it when the camera is toggled off mid-take, adds a relay track so the webcam file survives camera-off gaps, and records those gaps in the sidecar for the editor. The main-process side (`BubbleProtection`, `CameraBubbleWindow`, hub park/destroy decisions, finalize/abort/reset release) reads consistently. I found one real defect: a quick off→on→off→on closes the recorded gap before the camera is back, so the editor and export show the frozen last frame as a live face. The rest is minor: a misleading comment, a 6 s worst-case wait on the toggle queue, a displaced doc comment, and a test whose name claims more than it covers. I could not confirm that mediabunny 1.61.4 accepts the third constructor argument the relay depends on (no `node_modules` in the checkout), so I raised it as a question.

**Batch 2 of 2.** I found one issue in this part, a test-quality one. The shared sanitizer, the gap log, the relay, the seeding of gaps into the editor, and the docs are consistent with the store and engine code they describe. `sanitizeWebcamGaps` uses only relative imports, so the `src/shared` rule holds. ADR 0032 is still \"Proposed\", so the added decision 6 is not a rewrite of an accepted record. The post-take toast text matches the ADR's claim. The one issue: `webcam-relay.test.ts` does not exercise the stale-frame guard in `webcam-relay.ts` (the `current !== reader` branch) that its comment describes, because the cancelled stream throws and the test swallows it. I did not run any tests.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 22 | $0.73 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 19 | $0.42 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**New releaseWebcam declaration split the releaseAll doc comment from its function (confidence high)** ([`recorder-engine.ts:434`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L434))

The "Frees everything acquired, for a start that failed…" block (lines 434-437) now sits above the `releaseWebcam` doc and declaration. `releaseAll` (line 440) no longer has its comment. Move `let releaseWebcam` and its one-line doc above the `releaseAll` comment.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 46 in / 35k out / 1.4M cache read / 166k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.16</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6ImU2YzZmNTg4LWUxYjgtNGM0My05ZTEyLTFiYjYwMGQ0ZGRiNiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6NiwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjYsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MX0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=e6c6f588-e1b8-4c43-9e12-1bb600d4ddb6 -->
