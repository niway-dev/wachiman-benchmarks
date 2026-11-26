# kaipu-bench-wachi-v3#92 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:31:18Z · commit 3ec7a13

👮 **Wachiman** · 🟠 **2 to fix in this PR** · 2 questions for you · 4 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 2 to fix · 🟡 4 to consider · ⚪ 0 for your information (6) · 4 Should · 2 Could |
| **Risk** | Medium: top fact `public-contract` at `webcam-track.ts:72`, see Risk facts |
| **Needs a person** | 1 direction and 1 trade-off, in `webcam-relay.ts:1` and `0032-…-capture.mdx:80` |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `webcam-track.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts`, `recorder-engine.ts` |

### To fix (2)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recorder-store.ts:928`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L928) | Camera-off is applied immediately but camera-on is queued, so an off that follows a queued on is undone |
| 🟠 Fix · Should · 🐛 bug | [`webcam-model.test.ts:105`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.test.ts#L105) | Seeded gap segments get random ids, which breaks Share's reuse fingerprint for takes with gaps |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🧹 cleanup | [`recorder-engine.ts:434`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L434) | New \`releaseWebcam\` declaration was inserted between \`releaseAll\` and its doc comment |
| 🟡 Consider · Should · 🧪 tests | [`recording-hub.test.ts:2065`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/recording-hub.test.ts#L2065) | Test title promises the hub-reset path but only abort is exercised |
| 🟡 Consider · Could · 🧪 tests | [`recorder-store.test.ts:1602`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.test.ts#L1602) | "On the take's own timeline" assertion is only a lower bound and cannot tell the timelines apart |
| 🟡 Consider · Could · 🧪 tests | [`webcam-relay.test.ts:78`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts#L78) | The cut test never exercises the "frame from a superseded camera is closed" branch |

### Questions for you (2)

- [`webcam-relay.ts:1`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts#L1) · direction — The always-running webcam file depends on Chromium's non-standard `MediaStreamTrackGenerator`/`Processor`. It also depends on mediabunny repeating the last frame when given an explicit frame rate while the relay is empty. Both are mocked in the tests. A person must decide whether this is worth shipping against a real camera, or whether a different approach is better.
- [`0032-…-capture.mdx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/documentation/src/content/docs/architecture/decisions/0032-webcam-is-its-own-track-and-the-bubble-is-excluded-from-capture.mdx#L80) · trade-off — Decision 6 is explicitly unverified: it assumes a hidden-then-shown bubble window stays excluded from the running ScreenCaptureKit stream. If that assumption is wrong, the face is burned into the screen file after the camera is turned back on. That can only be settled by owner QA on a real take.

### Risk facts

- `public-contract` · [`webcam-track.ts:72`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/shared/webcam-track.ts#L72) — Adds an optional `gaps` array to the sidecar's `webcam` field and to the finalize payload. It is sanitized in main and read by the editor and Share, and old sidecars without it stay valid.

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Camera toggled off mid-take parks the bubble window instead of destroying it; toggled on shows the same window (`apps/kaipu-record/src/main/recording/recording-hub.ts:299`) — Bubble disappears on off and reappears in the same place on on. The screen capture keeps excluding it, because it is the same native window that was on screen when the capture started. The camera light goes off through the bubble renderer's own `useCameraOn`. If it fails: If a reopen fails after the window was already re-shown, the webcam-ended report removes protection from the visible window. This is the same best-effort limitation as an unplugged camera and is docu… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/recording-hub.ts:456-460`, `apps/kaipu-record/src/main/recording/recording-hub.ts:494-499`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-847`, `apps/kaipu-record/src/main/recording/bubble-protection.ts:45-56`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:257-282`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1035-1068`.
- Engine reopens the camera on toggle-on and feeds the relay (turnWebcamOn) (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — The face returns in the webcam file at its place on the take's clock. The camera-off period is a hidden segment in the editor. A failed reopen shows a toast after saving. If it fails: The whole wait is bounded by the 3 s open plus the 3 s first-frame race, so at most about 6 s. The open race covers both `getUserMedia` attempts, because `openWebcam` runs inside it. A late stream is… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:1130-1145`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:72-114`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`.
- Camera-off gaps recorded in the sidecar and seeded as hidden segments in the editor (`apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:106`) — The editor lane shows the camera-off spans as hidden, and the export leaves the held frame out. If it fails: No exceptions in this path. `WEBCAM_MIN_SEGMENT_SECONDS` is declared after `gapSegments`, but only used when the function runs, so there is no TDZ error. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:806-809`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1095-1110`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:130-175`, `apps/kaipu-record/src/renderer/src/features/video-editor/scene.ts:140`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:10-31`.
- Bubble renderer follows the Camera toggle (useCameraOn) and releases the camera while the window is parked (`apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44`) — The in-use light goes off while the bubble is parked, and the preview resumes when the camera comes back on. If it fails: A rejected `getRecordingSettings` is swallowed and the state stays on, which is the old behaviour. Main also broadcasts to hidden windows, so a parked window still hears the toggle. Evidence: `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:38-61`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:143-144`, `apps/kaipu-record/src/main/recording/recording-hub.ts:285-292`.
- Camera toggled off then on mid-take: the store forwards `isCameraEnabled` to `turnWebcamOff`/`turnWebcamOn` and keeps the webcam file running (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924`) — The face is hidden in the editor over each gap through hidden segments seeded from `webcam.gaps`. A reopen failure shows the `record.webcamUnavailable` toast after the save (recorder-store.ts:1069). If it fails: `turnWebcamOn` is bounded by the open and first-frame timeouts (3 s each, recorder-engine.ts:784-808). Rejection or a late camera ends the file and tells the user. A stop mid-open is answered "unavai… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:769-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.test.ts:1646-1661`.
- Sidecar `webcam.gaps` is sanitized in main and seeded in the editor as hidden segments (`apps/kaipu-record/src/shared/webcam-track.ts:184`) — The editor lane stripes each gap and exports hide the face there. Share's fingerprint now includes the segments, with random ids (see finding). If it fails: A malformed gap is dropped on its own. An old sidecar has no key and reads as before. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/main/library/webcam-track-state.ts:21`, `apps/kaipu-record/src/main/recording/recording-writer.ts:291`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`, `apps/kaipu-record/src/renderer/src/features/library/components/share-recording.tsx:126-130`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-reuse.ts:81-84`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The change parks the camera bubble instead of destroying it during a take that records a webcam file. It adds a relay so a camera turned off and on again keeps feeding the same webcam file. It also records camera-off gaps and seeds them as hidden segments in the editor. I found one real defect: the store applies camera-off immediately but queues camera-on, so an off→on→off sequence with a busy queue can leave the camera open after the user turned it off. There are also two minor items, a detached doc comment and a test title that claims more than it tests. I could not check the mediabunny API usage (the three-argument `MediaStreamVideoTrackSource` constructor and `sizeChangeBehavior`) because the package is not installed in this checkout. Everything else I traced held: the hub, the bubble window lifecycle, the engine toggle, the renderer follow and the gap seeding.

**Batch 2 of 2.** I reviewed the 9 files of part 2 and found one defect that needs fixing plus two test-quality notes. The defect: `seedWebcamScene` gives each gap segment a random UUID (webcam-model.ts:155, not in this part). Share's reuse fingerprint hashes those ids, so any take with a camera-off gap gets a new fingerprint on every mount. The previously made Share file is never reused and the user silently re-encodes each time. The gap tests don't pin determinism, so CI won't catch it. The two test notes: the "own timeline" assertion in the store test is only a lower bound, and the relay test never reaches its "close a late frame" branch. The shared sanitizer, `WebcamGapLog`, the relay and the engine/store tests otherwise match the code I read (engine lines 654-820, store lines 823-1111). The `shared` file takes only relative value imports, as required. The docs match the code. The ADR 0032 decision 6 and the spec's mid-take item 7 both state their one unverified assumption (the exclusion of a hidden-then-shown window) openly."

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 17 | $0.53 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 31 | $0.62 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**New `releaseWebcam` declaration was inserted between `releaseAll` and its doc comment (confidence high)** ([`recorder-engine.ts:434`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L434))

The JSDoc "Frees everything acquired, for a start that failed or a prepared take released…" (lines 434-437) used to sit on `releaseAll`. The added `/** Releases the webcam relay… */ let releaseWebcam` now sits between them, so the first doc block is attached to nothing and `releaseAll` has none. Move the new declaration above the `releaseAll` comment.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 62 in / 30k out / 2.0M cache read / 162k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.15</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6IjZkNWU1MzM4LTIyMDQtNGMzMi1iZWY1LWQxNjg3ZjBiNWViMiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoyLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjUsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MX0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=6d5e5338-2204-4c32-bef5-d1687f0b5eb2 -->
