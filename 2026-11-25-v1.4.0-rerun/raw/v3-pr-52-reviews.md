# kaipu-bench-wachi-v3#52 [replay r2] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T00:08:07Z · commit 3ec7a13

👮 **Wachiman** · review of the whole pull request, at `3ec7a13`: all 23 files reviewed.

4 finding(s): 1 to fix, 3 to consider; 4 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** I found no blocking or must-fix defects in part 1. I traced the main-process logic that decides whether to park or destroy the bubble. Parking happens only during an active take that records a webcam file. The parked window is released on finalize, abort, stop and reset, and its position is read before the release, because the renderer sends recordingStop after finalize. I also traced the engine's turn-off/turn-on through the relay: superseded requests, timeouts and the take stopping mid-open all stop the camera they opened. The store's gap log is fed from both of those paths. One comment in recorder-store.ts describes queue ordering for a turn-off that does not exist (the turn-off runs synchronously and supersedes the turn-on through a request counter). One question stays open: whether mediabunny's MediaStreamVideoTrackSource supports the frameRate and sizeChangeBehavior options and repeats the last frame through a gap. The PR lists that as an assumption, and I did not check it against the library.

**Batch 2 of 2.** I reviewed part 2 of 2 (the shared gap type and its sanitizer, the tests, the ADR and the spec) and found one bug worth fixing, plus two test gaps.

**Bug (fix, medium confidence):** a take that has camera-off gaps never reuses its earlier Share export.
- Each gap becomes a hidden segment with a random `crypto.randomUUID()` id (`webcam-model.ts:155`).
- The Share fingerprint hashes the whole webcam layer, ids included (`export-reuse.ts:81-83`).
- So every new seeding produces a new fingerprint, and a second Share re-encodes the whole recording without telling the user why.
- The cause is in `webcam-model.ts`, which belongs to part 1, so I reported it on `webcam-model.test.ts:105`. Suggested fix: build the seeded ids from the gap itself (for example `gap-${startMs}`) and add a test that seeding the same sidecar twice gives the same fingerprint.
- It stays at medium confidence because I didn't read `stableStringify` to confirm it keeps the segment ids.

**Tests (consider):**
- `webcam-relay.test.ts:79` says a frame from a cut camera is "dropped (and closed)", but that code branch never runs in the test and the test never checks that the frame was closed.
- `recorder-engine.test.tsx:1683` uses a camera rate of 30, which equals the fallback `WEBCAM_FPS`. The test passes whether or not the engine reads the camera's own rate.

**Checked and fine:**
- The gap sanitizer validates each entry, clamps starts to 0, merges overlaps, caps the list at 1000, and adds no value import from a workspace package.
- The store and engine toggle logic matches what the tests claim, including turning the camera off again while it reopens and a camera that can't be reopened.
- What the ADR and spec say about parking the bubble, the relay, the countdown and no-relay fallbacks, and trailing gaps matches the code.

<details><summary>What the change connects to (6 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- The webcam encoder reads a MediaStreamTrackGenerator relay with an explicit frameRate and sizeChangeBehavior "contain" (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:691`) — Does this mediabunny version's MediaStreamVideoTrackSource accept a third argument with frameRate and the sizeChangeBehavior option, and does it repeat the last frame when the track sends no frames? Files that would answer it: `node_modules/mediabunny/dist/modules/src/media-source.d.ts`.

**Closed, with the lines they rest on**
- Camera turned off mid-take parks the bubble instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — The bubble is hidden and keeps its content protection. The bubble renderer's useCameraOn stops the preview camera (camera-bubble.tsx:44-60, 143-144) because recordingSettingsChanged goes to every window (recording-hub.ts:285-290). If it fails: If the renderer could not keep the file going (no relay), the engine reports the end, protection drops, and the next turn-on destroys the parked window and creates a new one (recording-hub.ts:304). T… Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/recording-hub.ts:494-499`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-846`, `apps/kaipu-record/src/main/recording/recording-hub.ts:868`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:236-271`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1042`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1068`.
- Engine turnWebcamOn reopens the camera into the relay (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — Frames reach the same webcam file. The store closes the gap when the result is ok (recorder-store.ts:939-944). If it fails: The result is "unavailable". The store sets webcamReopenFailed, which shows the existing camera-unavailable notice after the take (recorder-store.ts:946-951, 1018). Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:845-871`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:975-982`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-952`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1016-1018`.
- Sidecar gains `webcam.gaps`, sanitized in shared code before it lands on disk (`apps/kaipu-record/src/shared/webcam-track.ts:184`) — The editor seeds each gap as a hidden webcam segment, so the lane is striped and the export leaves the face out there. If it fails: Bad input is dropped silently, so the worst case is a gap that is not hidden. Gaps are not clamped to the duration here; the editor clamps them when durationSeconds is known. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-185`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`.
- Engine feeds the camera track into a relay; the encoder reads the relay track (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:659`) — The webcam file keeps running through off periods, holding its last frame. If it fails: The first feed is fire-and-forget (`void`). If it never delivers a frame, nothing detects it, the same as the old path with no frames. A reopen that delivers no frame within WEBCAM_OPEN_TIMEOUT_MS en… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:654-711`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:756-761`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:74-114`.
- Store camera toggle mid-take: turnWebcamOff opens a gap; turnWebcamOn on the queue closes it (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:928`) — Finalize sends gaps (finish(durationMs)) in the sidecar meta. The user gets a toast when the camera could not be reopened. If it fails: A turnWebcamOn that rejects would reject the queue promise. The engine's turnWebcamOn has no throwing await other than openWebcamWithin, which presumably resolves to null on failure. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:924-953`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:806-809`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017-1018`.
- Seeded gap segments feed the Share fingerprint (`apps/kaipu-record/src/renderer/src/features/library/components/share-recording.tsx:130`) — A second Share of a take with gaps re-encodes instead of reusing the earlier export. If it fails: Silent: the earlier export is never matched. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:155`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-reuse.ts:81-83`, `apps/kaipu-record/src/renderer/src/features/library/components/share-recording.tsx:126-130`, `apps/kaipu-record/src/renderer/src/features/video-editor/scene.ts:140`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 11 | $0.63 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 18 | $0.64 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $1.27</sub>

<!-- wachi:review -->

<!-- agent-review sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:attempt id=ae3ee769-840b-4a80-aae1-b4af6a91553a -->
