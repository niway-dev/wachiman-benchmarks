# kaipu-bench-wachi-v3#112 [replay r2] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939 · github-actions[bot] · 2026-11-26T20:09:22Z

| 👮 **Wachiman** | A queued camera-on still opens the camera after the user has turned it off again |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The camera-off branch (l.928) runs synchronously and never goes through `queue`, while the camera-on branch (l.939) is queued behind earlier items. The comment at l.938 says an off that follows 'waits for this camera to open and releases it', but that only holds when the on has already started. If the on is still waiting in the queue, the off runs first: `turnWebcamOff` sets `cameraWanted = false` (recorder-engine.ts:771). When the queued closure then runs, `turnWebcamOn` checks only `cameraWanted` (recorder-engine.ts:781). That flag is false, so it opens the camera and feeds the relay although `webcamOn` is false.

The queue is busy whenever an earlier `turnWebcamOn` is in flight (up to 3 s to open plus 3 s to feed), or a mic acquire or noise-suppression reopen is. A fast on, off, on, off with a slow camera therefore ends with:
- the camera light on while the toggle says off;
- real face frames written into the span the sidecar records as a gap;
- the bubble parked, so the user sees nothing.

The result 'ok' with `webcamOn` false leaves the gap open, so nothing signals the mismatch.

Fix: at the start of the queued closure, return early when `!webcamOn || !active`, so the engine is never asked to open for a toggle that was already reverted. The following on re-queues its own open.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-hub.test.ts:2065 · github-actions[bot] · 2026-11-26T20:09:22Z

| 👮 **Wachiman** | Test name promises the forced-reset path, but only abort is exercised |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test 'a bubble parked when the take is aborted or the hub reset is destroyed too' only calls `recordingAbort`. The `forceReset` path (`releaseParkedBubble()` at recording-hub.ts:1022) and the `applyStopWindowState` path (recording-hub.ts:846) have no test of their own. Either add the missing cases or rename the test to say 'aborted'. A regression that drops the call from reset or stop would pass today.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:709 · github-actions[bot] · 2026-11-26T20:09:22Z

| 👮 **Wachiman** | Does \`MediaStreamVideoTrackSource\` take a third argument that carries \`frameRate\`? |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The gap behaviour relies on this third constructor argument (`{ frameRate }`), which the comment says makes mediabunny write frames on the clock and repeat the last one. mediabunny is not installed in this checkout, and every engine test replaces `MediaStreamVideoTrackSource` with a `vi.fn` mock (recorder-engine.test.tsx:40). Nothing in the repo therefore exercises that argument against the real library. Could you confirm that mediabunny ^1.61.4 accepts it and honours it? If it is ignored, the file simply has no samples during a gap, and the last frame plays on through the MP4 sample durations. Most of the feature would still work, but the 'repeats its last frame' claim in the comment and ADR would be wrong.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.test.ts:105 · github-actions[bot] · 2026-11-26T20:09:22Z

| 👮 **Wachiman** | Gap segments get random ids, so Share's "whole" fingerprint changes on every open for a take with gaps |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`seedWebcamScene` gives each gap segment `crypto.randomUUID()` (webcam-model.ts:155), and this test pins that the ids are distinct. Share builds its scene with `initialScene(...)` in a `useMemo` (share-recording.tsx:126) and fingerprints it with `wholeFingerprint(scene.webcam)` (share-recording.tsx:130). `wholeFingerprint` hashes `stableStringify(webcam)` (export-reuse.ts:81-83), and that includes every segment `id`. Before this change `segments` was always `[]`, so the hash was stable. For a take with gaps the hash differs on each mount, and also before versus after the probe fills in `durationSec`. The "second Share reuses the file" behaviour (the comment at share-recording.tsx:123-125) therefore never hits for these takes. Each Share re-encodes and stores another export, and nothing tells the user. Fix: derive the ids from the gap, for example from its start and end, so the same sidecar always seeds the same scene. Add a test that two `seedWebcamScene` calls on the same meta are `toEqual`, which the current tests do not cover.

<!-- wachi:finding -->
