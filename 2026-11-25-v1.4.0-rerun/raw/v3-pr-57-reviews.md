# kaipu-bench-wachi-v3#57 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T00:08:04Z · commit 3ec7a13

👮 **Wachiman** · review of the whole pull request, at `3ec7a13`: all 23 files reviewed.

3 finding(s): 1 to fix, 2 to consider; 3 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** I reviewed all 14 files in part 1 and found one problem: a privacy bug in how the recorder store passes the Camera toggle to the engine. Camera-off runs immediately, but camera-on waits in a queue and never re-checks the toggle before it runs. After quick toggling, or a toggle made while a mic change is still opening its device, the camera can reopen after the user turned it off: the light is on and the face is recorded into the webcam file while the toggle says off. The rest of this part holds up: park versus destroy in main, the replacement window when the webcam file ended while the bubble was parked, the bubble's position read before a parked bubble is released at finalize, the relay's handoff between cameras, and the seeding of camera-off periods in the editor. I read and judged the code only; I did not build, test or run it.

**Batch 2 of 2.** I read every file in part 2 in full, plus the code under test: `webcam-relay.ts`, `webcam-gaps.ts`, the gap logic in `recorder-store.ts`, `turnWebcamOn`/`turnWebcamOff` in `recorder-engine.ts`, and `webcam-model.ts`.

The new tests' assertions match the code they test, and the `webcam-track.ts` sanitizer is sound. It also takes no value imports from workspace packages.

I found two minor issues, both "consider":
- **Relay test (`webcam-relay.test.ts:79`):** the test meant to show that a cut camera's late frame is dropped and closed doesn't exercise that path. After the cut, pushing the frame into the cancelled stream throws, and the `try/catch` swallows the error, so the frame never reaches the relay.
- **ADR 0032 decision 6 (line 67):** it doesn't mention that a take without a relay (no `MediaStreamTrackGenerator`), or one where the camera is turned off during the countdown, still ends the webcam file when the camera is turned off. The spec states this exception; the ADR doesn't.

<details><summary>What the change connects to (7 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Camera toggled off mid-take parks the bubble instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — The bubble disappears. The light goes off once both the preview and the recorder release the camera. If it fails: If the renderer has no relay, the engine ends the file instead and `recordingWebcamEnded` drops the protection. The next camera-on then destroys the parked window and creates a new one (recording-hub… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-271`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`.
- Finalize reads placedBounds, then releases the parked bubble (`apps/kaipu-record/src/main/recording/recording-hub.ts:498`) — A take that ends with the camera off still records where the bubble sat. If it fails: If finalize fails, the parked bubble is still released (as the hub test shows). Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:487-503`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-850`.
- Live camera off/on forwarded to the engine's turnWebcamOff/turnWebcamOn (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924`) — After quick toggling, the camera can end up open (light on, face recorded) while the toggle says off. If it fails: Superseded opens are cancelled through `cameraRequest` only if they were already running. An on that starts after a later off reopens the camera. Reported as a finding. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:769-819`.
- Reopening the camera mid-take (openWebcamWithin plus relay feed, with a timeout) (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:784`) — On failure the file ends and onWebcamEnded fires. Main drops the protection, so the face goes into the screen. After the take the store shows the 'camera wasn't available' notice. If it fails: Visible: after the take, a notice appears through `webcamUnavailable`. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:784-818`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`.
- Main sanitizes renderer-supplied `webcam.gaps` before writing the sidecar (`apps/kaipu-record/src/shared/webcam-track.ts:131`) — The editor seeds hidden webcam segments from the stored gaps (webcam-model.ts gapSegments), so the lane shows them striped and the export hides the face there. If it fails: Bad input from the renderer becomes no gaps. The face is then shown over the held frame, which degrades output but does not lose data. There is no IPC failure path. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-186`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`.
- Engine feeds a reopened camera into the relay (`relay.feed`) on turnWebcamOn (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:804`) — Store closes the gap on "ok" (if still on); on "unavailable" it closes the gap, marks webcamReopenFailed and shows the webcamUnavailable toast after the save. If it fails: If getUserMedia rejects or returns null, the file ends via endWebcam and onWebcamEnded fires, so main unprotects the bubble. If no frame arrives within the timeout, the same happens. The user learns… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1069-1070`.
- Store records camera-off gaps on the take's timeline and sends them with finalize (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:930`) — The sidecar gets `webcam.gaps`, and the editor seeds hidden segments from them. If it fails: Without a relay, off ends the file and no gap is logged, which is the legacy behaviour. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:806-809`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1015-1017`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:10-31`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 7 | $0.43 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 13 | $0.55 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $0.98</sub>

<!-- wachi:review -->

<!-- agent-review sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:attempt id=a0f9a39f-4f5e-4a43-a290-e36df7f7d7f8 -->
