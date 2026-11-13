# Wachiman review of branch `bench/pr-463` of pr-463 against origin/replay/pr-463/base (merge-base c58b68f), at 3ec7a13

All 23 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

3 finding(s): 1 to fix, 2 to consider

## Findings

### 🟠🐛 **Fix · bug: A failed reopen leaves the face out of both files while the user is told it went to the screen (confidence medium)**

`apps/kaipu-record/src/main/recording/recording-hub.ts:304`

When the camera comes back on, main reacts to the settings broadcast at once. At that moment the webcam file is still live, so `takeRecordsWebcam()` is true and `show()` brings back the parked, protected window (line 304–305). The renderer's `turnWebcamOn` runs after that (recorder-store.ts:939–952). If the reopen fails (busy, denied, or no frame within `WEBCAM_OPEN_TIMEOUT_MS`), the engine calls `endWebcam` → `onWebcamEnded` → `recordingWebcamEnded`. That handler only runs `bubbleProtection.webcamEnded` + `cameraBubble.applyProtection()` (recording-hub.ts:456–460): it removes protection from the same window that was on screen when the capture started.

This PR's own comments (lines 301–303 and 310–313, camera-bubble-window.ts:40–43) say a running capture leaves out the windows that were on screen at its start, and that only a *new* window gets recorded. So after a failed reopen the face is in neither the webcam file nor the screen. Meanwhile recorder-store.ts:946–947 claims "main put the bubble back in the capture" and sets `webcamUnavailable`, which tells the user the face went to the screen. The destroy-and-recreate at line 304 only covers a file that ended *while parked*, not one that ends on the reopen attempt.

Possible fix: in the `recordingWebcamEnded` handler, when the bubble window was parked during this take (or is the window carried over from the capture start), destroy it and `show()` a new one, the same thing line 304 does for the parked case. No test covers this ordering: the hub test at recording-hub.test.ts:1998 sends `webcamEnded` before `camera(true)`.

### 🟡⚡ **Consider · perf: Camera-on can hold the shared toggle queue for two full open timeouts (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939`

`turnWebcamOn` awaits `openWebcamWithin(..., WEBCAM_OPEN_TIMEOUT_MS)` and then races `feed` against a second `WEBCAM_OPEN_TIMEOUT_MS` (recorder-engine.ts:784–808), so the worst case is 2× the timeout. It runs on the same `queue` the forwarder uses for the other live toggles (line 939). Any mic or system-audio toggle made while a camera is slow to reopen waits that long before it takes effect. If those toggles share this queue (they appear to), think about giving the camera reopen its own chain, or a single deadline that covers both steps.

### 🟡🧪 **Consider · tests: The "late frame is dropped (and closed)" claim is never asserted (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79`

The comment says a frame the old camera delivers after `cut()` is dropped and closed. But `cut()` cancels the reader before the push (`webcam-relay.ts:66-70`), so `first.push(late)` most likely throws into the empty `catch`. The frame never reaches the pump's `current !== reader` branch, which is the one that closes it (`webcam-relay.ts:91-94`). Nothing checks `late.close`, so the test passes whether or not a stale frame would be closed, and that branch has no coverage. Either assert `expect(late.close)…` in a setup where the frame really gets read (for example, enqueue it before the cut while a read is pending), or change the comment so it only claims what is checked: that `written` leaves out `a2`.

## Summary

**Batch 1 of 2.** Part 1 adds hide-not-destroy for a camera turned off mid-take: the bubble is parked, the webcam relay keeps one file running, and the gaps are seeded as hidden editor segments. One fix: if the camera fails to reopen, main has already re-shown the same parked window and only removes its protection. By the PR's own reasoning a running capture does not record that window, so the face can be lost from both files while the user is told it went to the screen. One consider: the reopen can hold the shared toggle queue for two open timeouts. The review stopped early because the cost limit was reached, so these points were not checked: whether mediabunny's `MediaStreamVideoTrackSource` accepts the third `{ frameRate }` argument (recorder-engine.ts:709), how the bubble receives the settings broadcast, and whether the screen-time base of `takeTimeMs` matches the editor's segments.

**Batch 2 of 2.** I reviewed all nine files in part 2: the gap sanitizer in shared/webcam-track.ts, the new tests for the engine, store, gap log, relay, sanitizer and editor model, and the updates to ADR 0032 and the webcam-track spec. I found no bugs, and the shared file takes no value imports from workspace packages. The sanitizer does what its doc comment says: it drops bad entries, clamps starts to 0, sorts, merges and caps the list. The tests' expectations match webcam-gaps.ts, webcam-relay.ts and webcam-model.ts as written. The ADR and spec text matches the code, including the legacy rule that still applies without a relay or during the countdown. There is one small test finding: the relay test says a late frame is "dropped (and closed)" but never asserts the close.

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Camera turned on again mid-take: main shows the parked window and the renderer reopens the camera into the relay (`apps/kaipu-record/src/main/recording/recording-hub.ts:304`) — The bubble comes back on screen. The editor gets gaps plus webcamUnavailable on failure. If it fails: Reopen fails → file ends → same window unprotected, which by the PR's own comments the running capture does not record. Face lost silently; reported as finding. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-322`, `apps/kaipu-record/src/main/recording/recording-hub.ts:456-460`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:935-952`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779-819`.
- Whole wait of turnWebcamOn (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:784`) — Queued live toggles wait for it. If it fails: Worst case is 2× WEBCAM_OPEN_TIMEOUT_MS; the timer is cleared after the race. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:784-809`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939`.
- Parked bubble released at the end of a take (`apps/kaipu-record/src/main/recording/recording-hub.ts:333`) — The camera window goes away once the take ends with the camera off. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:494-499`, `apps/kaipu-record/src/main/recording/recording-hub.ts:551-554`, `apps/kaipu-record/src/main/recording/recording-hub.ts:844-846`, `apps/kaipu-record/src/main/recording/recording-hub.ts:1019-1022`.
- Main sanitizes renderer-supplied `webcam.gaps` before writing the sidecar (`apps/kaipu-record/src/shared/webcam-track.ts:131`) — The editor seeds each gap as a hidden webcam segment (webcam-model.ts:111, 135-158). If it fails: Hostile or garbage input is dropped one entry at a time. The cap bounds sidecar size. No value import from a workspace package was added to src/shared. Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-186`, `apps/kaipu-record/src/shared/webcam-track.ts:9-13`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-158`.
- The relay feeds a new camera track into the same encoder track (`apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:74`) — The webcam file keeps running through camera-off periods. The editor hides the held frame through the gaps. If it fails: A processor that cannot be built or a camera that ends before a frame resolves false. The engine then ends the file (per the tests at recorder-engine.test.tsx:1723-1735). Evidence: `apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.ts:66-123`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.test.tsx:1723-1735`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 6 | $0.56 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 6 | $0.40 |

Cost: $0.97, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 2 call(s), 12 turn(s), 1 min 41 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of 3ec7a13 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/main/recording/recording-hub.ts:304 · 🟠🐛 Fix · bug: A failed reopen leaves the face out of both files while the user is told it went to the screen (confidence medium)
   When the camera comes back on, main reacts to the settings broadcast at once. At that moment the webcam file is still live, so `takeRecordsWebcam()` is true and `show()` brings back the parked, protected window (line 304–305). The renderer's `turnWebcamOn` runs after that (recorder-store.ts:939–952). If the reopen fails (busy, denied, or no frame within `WEBCAM_OPEN_TIMEOUT_MS`), the engine calls `endWebcam` → `onWebcamEnded` → `recordingWebcamEnded`. That handler only runs `bubbleProtection.webcamEnded` + `cameraBubble.applyProtection()` (recording-hub.ts:456–460): it removes protection from the same window that was on screen when the capture started.

   This PR's own comments (lines 301–303 and 310–313, camera-bubble-window.ts:40–43) say a running capture leaves out the windows that were on screen at its start, and that only a *new* window gets recorded. So after a failed reopen the face is in neither the webcam file nor the screen. Meanwhile recorder-store.ts:946–947 claims "main put the bubble back in the capture" and sets `webcamUnavailable`, which tells the user the face went to the screen. The destroy-and-recreate at line 304 only covers a file that ended *while parked*, not one that ends on the reopen attempt.

   Possible fix: in the `recordingWebcamEnded` handler, when the bubble window was parked during this take (or is the window carried over from the capture start), destroy it and `show()` a new one, the same thing line 304 does for the parked case. No test covers this ordering: the hub test at recording-hub.test.ts:1998 sends `webcamEnded` before `camera(true)`.
2. apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939 · 🟡⚡ Consider · perf: Camera-on can hold the shared toggle queue for two full open timeouts (confidence medium)
   `turnWebcamOn` awaits `openWebcamWithin(..., WEBCAM_OPEN_TIMEOUT_MS)` and then races `feed` against a second `WEBCAM_OPEN_TIMEOUT_MS` (recorder-engine.ts:784–808), so the worst case is 2× the timeout. It runs on the same `queue` the forwarder uses for the other live toggles (line 939). Any mic or system-audio toggle made while a camera is slow to reopen waits that long before it takes effect. If those toggles share this queue (they appear to), think about giving the camera reopen its own chain, or a single deadline that covers both steps.
3. apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts:79 · 🟡🧪 Consider · tests: The "late frame is dropped (and closed)" claim is never asserted (confidence medium)
   The comment says a frame the old camera delivers after `cut()` is dropped and closed. But `cut()` cancels the reader before the push (`webcam-relay.ts:66-70`), so `first.push(late)` most likely throws into the empty `catch`. The frame never reaches the pump's `current !== reader` branch, which is the one that closes it (`webcam-relay.ts:91-94`). Nothing checks `late.close`, so the test passes whether or not a stale frame would be closed, and that branch has no coverage. Either assert `expect(late.close)…` in a setup where the frame really gets read (for example, enqueue it before the cut while a read is pending), or change the comment so it only claims what is checked: that `written` leaves out `a2`.
```
