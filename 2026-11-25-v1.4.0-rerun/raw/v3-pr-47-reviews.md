# kaipu-bench-wachi-v3#47 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:59:16Z · commit 3ec7a13

👮 **Wachiman** · review of the whole pull request, at `3ec7a13`: all 23 files reviewed.

3 finding(s): 1 to fix, 2 to consider; 3 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 has one bug worth fixing: quick off→on→off→on toggles mid-take can close a webcam gap too early. In that case the editor shows a frozen frame with no warning (recorder-store.ts:943). The comment above that code also wrongly says an off waits on the queue. Separately, a doc comment in recorder-engine.ts is now attached to the wrong declaration. The main-process park/destroy flow is consistent across finalize, abort, stop and reset, and so are the bubble preview following the toggle and gap seeding.

**Batch 2 of 2.** Part 2 has one test finding at "consider" and nothing more serious. The gap sanitizer in `webcam-track.ts` drops each malformed gap on its own, clamps starts below 0, merges overlapping gaps, caps the list at 1000 gaps and leaves the key out when no gap is usable; its tests match. The tests for the gap log, the store and the engine match what `recorder-store.ts`, `webcam-gaps.ts` and the engine's toggle contract do. That includes turning the camera off again while it is reopening, a reopen that fails (a toast after the take) and a camera still off at the stop (a trailing gap). The editor's seeding tests match `gapSegments`: short gaps are stretched to the 1 s minimum, then merged and kept inside the recording. Decision 6 in ADR 0032 and the revised spec item 7 match main's park-or-destroy logic in `recording-hub.ts`. The one finding: the relay test that claims a frame from a cut camera is \"dropped (and closed)\" never reaches that branch, because the cut has already cancelled the stream. As a result, `webcam-relay.ts:91-93` has no test.

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Camera toggled off mid-take parks the bubble window instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — The bubble disappears. The camera light goes off once the bubble's preview and the recorder's camera both stop. If it fails: If the renderer has no relay, turnWebcamOff returns false and the engine ends the file. The webcamEnded IPC then removes protection from the parked, hidden window. On the next on, the hub destroys it… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/recording-hub.ts:494-499`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-854`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:146-152`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-271`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1042`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1068`.
- Engine reopens the camera mid-take and feeds the same file through the relay (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — The face comes back in the webcam file, and the store closes the gap. If it fails: A timeout or denial ends the file, and the store sets webcamReopenFailed, which shows the notice after the take. A superseded open returns "ok", and the store then closes the gap too early (see findi… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:741-820`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:74-114`.
- Finalize reads placedBounds for a bubble that is parked at the stop (`apps/kaipu-record/src/main/recording/recording-hub.ts:498`) — The recorded layout of a take that ends with the camera off uses the bubble's last position. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:494-502`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:236-239`.
- Main sanitizes renderer-supplied `webcam.gaps` before writing them to the sidecar (`apps/kaipu-record/src/shared/webcam-track.ts:184`) — The editor turns each gap into a hidden webcam segment (webcam-model.ts gapSegments), which the lane shows striped and exports leave out. If it fails: Malformed input from the renderer is dropped item by item and never fails the meta, so old sidecars and takes without gaps read the same. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-186`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-153`.
- The store records camera-off gaps when the camera is toggled during a take that has a relay (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`) — The gaps go out through `webcamGaps(endMs)` at finalize; a gap still open at stop is closed at the take's end. If it fails: A reopen that fails ends the file. Main receives `onWebcamEnded` and unprotects the bubble, and the user sees the `webcamUnavailable` toast. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-962`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:14-30`, `apps/kaipu-record/src/main/recording/recording-hub.ts:299-334`.
- The relay feeds a new camera track into the same generator track (`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:74-114`) — The webcam file keeps one clock across the camera-off period. If it fails: A camera that never delivers a frame and never ends leaves `feed` pending. The engine guards this with `WEBCAM_OPEN_TIMEOUT_MS`, according to its doc comment. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:66-123`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:159-166`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 9 | $0.54 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 10 | $0.43 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $0.98</sub>

<!-- wachi:review -->

<!-- agent-review sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:attempt id=857ea3e6-c4e9-4a28-a982-bbf97f442326 -->
