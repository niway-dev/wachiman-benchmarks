# kaipu-bench-wachi-v3#42 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:56:58Z · commit 3ec7a13

👮 **Wachiman** · 🟣 **1 question for you** · 3 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 1 Should · 2 Could |
| **Risk** | High: top fact `data-migration` at `webcam-track.ts:72`, see Risk facts |
| **Needs a person** | 1 direction, in `recording-hub.ts:315` |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `webcam-track.ts`, `recorder-store.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · ⚡ perf | [`recorder-engine.ts:803`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts#L803) | Re-opening the camera can wait twice WEBCAM_OPEN_TIMEOUT_MS, and it holds up the shared toggle queue |
| 🟡 Consider · Could · 🐛 bug | [`recorder-store.ts:943`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L943) | A superseded re-open closes the gap before the newer camera has sent a frame |
| 🟡 Consider · Could · 🧪 tests | [`recorder-store.test.ts:1646`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.test.ts#L1646) | No test for off → on → off → on while the first reopen is still pending |

### Questions for you (1)

- [`recording-hub.ts:315`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/recording-hub.ts#L315) · direction — The park path assumes the platform's screen capture keeps a hidden-then-reshown window out of a running stream. The PR names this as an owner check it could not run, and no test here can settle it.

### Risk facts

- `data-migration` · [`webcam-track.ts:72`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/shared/webcam-track.ts#L72) — The sidecar's `webcam` field gains an optional `gaps` array. It is left out when empty, so old sidecars still read the same.
- `concurrency` · [`recorder-store.ts:939`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L939) — Re-opening the camera is put on the same promise queue as the live mic and audio toggles, so those wait while the camera opens.

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Camera toggled off mid-take parks the bubble instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — The bubble disappears and the camera light goes off once the bubble preview (useCameraPreview(false)) and the engine (turnWebcamOff) have both stopped their tracks. If it fails: If the bubble renderer never gets the broadcast, the hidden window keeps the camera open (light stays on) until the take ends and releaseParkedBubble destroys it. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-282`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:143-144`.
- Engine turnWebcamOn re-opens the camera and feeds the relay (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — The bubble window shows again. The webcam file resumes after the first frame, and the gap closes in the store. If it fails: The two timeouts are sequential, so the worst case is about 2×WEBCAM_OPEN_TIMEOUT_MS, and the store's shared queue is blocked for that long (reported as a finding). On failure endWebcam reports onWeb… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:741-754`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`, `apps/kaipu-record/src/main/recording/recording-hub.ts:456-460`.
- Bubble renderer reads and follows the Camera toggle (`apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44`) — The preview stops while the window is parked and opens again when the window is shown. If it fails: If the read rejects, the hook stays on its default (true). That is correct, because the window exists only while the camera is on or while it is parked by a toggle, and a toggle always comes with a b… Evidence: `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`.
- Main sanitizes renderer-supplied `webcam.gaps` before writing them to the sidecar (`apps/kaipu-record/src/shared/webcam-track.ts:131`) — The editor seeds each surviving gap as a hidden webcam segment (webcam-model.ts:111). If it fails: Malformed renderer input becomes no gaps, so the face stays visible. The whole meta is not rejected. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-185`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:111`.
- The editor seeds camera-off gaps as hidden segments (`apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135`) — The lane shows the gap striped, and `webcamAt` returns null inside it, so the face is hidden there. If it fails: scene.ts:153 seeds without a duration, so a stretched gap can run past the recording's end. That has no visible effect. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`, `apps/kaipu-record/src/renderer/src/features/video-editor/scene.ts:140`, `apps/kaipu-record/src/renderer/src/features/video-editor/scene.ts:153`.
- The store opens and closes gaps around turnWebcamOff/turnWebcamOn (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:928`) — The gaps go into the finalize meta, and the webcamUnavailable toast shows after the save (recorder-store.ts:1069-1070). If it fails: If the camera is turned on again before the first reopen resolves, the first "ok" closes the gap early (line 943). Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1069-1070`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 of 2 is reviewed: all 14 files, nothing skipped. I found nothing that blocks the merge.

The main-process side is consistent across every path I read:

- **Off mid-take:** the bubble is parked (hidden, kept, still protected) instead of destroyed.
- **Webcam file ended while parked:** turning the camera on replaces the window with a new, unprotected one, as the PR describes.
- **Take over:** `releaseParkedBubble` removes a parked bubble at finalize, abort, the stop window state and reset.

In the renderer, I left two "consider" findings:

- **Long wait on re-open (`recorder-engine.ts:803`):** turning the camera back on can wait up to twice `WEBCAM_OPEN_TIMEOUT_MS`, because the camera open and the wait for its first frame each have their own timeout. While it waits it blocks the queue that mic, noise-suppression, volume and ducking changes also go through. The PR's test steps say the fallback happens within about 3 s.
- **Gap closes early (`recorder-store.ts:943`):** if the camera goes on, off and on again quickly, the first re-open finishes as superseded and closes the gap before the newer camera has sent a frame. The editor would then show the frozen frame while the camera warms up, which is what the PR's "gap closes on the first new frame" rule is meant to avoid.

I did not check the PR's unverified assumptions about mediabunny and Chromium, as they are not visible in this repository:

- that mediabunny repeats the last frame through a gap when given an explicit frame rate;
- that a frame from a stopped camera stays valid;
- that ScreenCaptureKit keeps a hidden-then-shown window out of a running capture.

**Batch 2 of 2.** Part 2 of 2 looks correct, and the only finding is a test I'd suggest adding. I reviewed the new gap type and its sanitizer, the tests for the engine, store, gap log, relay and webcam model, and the documentation updates.

**What checks out**

- **Gap sanitizer** (`webcam-track.ts`): it drops malformed, empty and backwards gaps one by one and clamps starts to 0. It also sorts, merges overlaps, caps the list at 1000 and leaves the key out when nothing survives. The tests assert exactly this.
- **Editor model tests**: the expected stretching, merging and clamping match what `gapSegments` does.
- **Docs**: the ADR 0032 decision 6 addition and the revised spec item 7 match the store's behaviour. That includes the legacy path with no relay or during the countdown, and the reopen-failure fallback with its post-take notice.

**The one finding (a "consider" on tests)**

No test covers the camera being turned off, on, off and on again before the first reopen resolves. The first reopen then resolves "ok" while the camera is already on again, and `recorder-store.ts:943` closes the gap early. If the second reopen then fails, the gap never covers the rest of the off period. In both cases the editor briefly shows the frozen frame.

**Risk:** the sidecar gains an optional `webcam.gaps` field, which is backwards compatible with old sidecars.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 6 | $0.65 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 9 | $0.52 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 18 in / 14k out / 329k cache read / 104k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.17</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6ImQzOGE4ZTYxLTc2MjYtNDBjZC1hYjk4LTZiYmI1OGIwOGEwNSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=d38a8e61-7626-40cd-ab98-6bbb58b08a05 -->
