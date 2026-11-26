# kaipu-bench-wachi-v3#107 [replay] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939 · github-actions[bot] · 2026-11-26T20:04:53Z

| 👮 **Wachiman** | A queued camera-on can open the camera after the user has turned it off again |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The comment at line 938 says the camera-on goes on the queue "so an off that follows waits for this camera to open and releases it". But the off branch (lines 924-934) does not go on the queue: it calls `handle.turnWebcamOff()` synchronously. That only works when `turnWebcamOn` is already running, because `cameraRequest++` makes it discard its late camera (recorder-engine.ts:790). If the queue is busy (a mic open, a noise-suppression reopen, or an earlier camera open), the on sits queued, not started. An off in that window sets `cameraWanted = false` (it was already false) and returns true. The queued `turnWebcamOn` then runs with `cameraWanted === false`, takes the open path (recorder-engine.ts:781-783), opens the camera and feeds the relay. Back in the store, `webcamOn` is false, so the gap stays open and nothing releases the camera. The result is the camera light on and the face written under a gap, while the bubble is parked and its own preview released. It stays that way until the next toggle or the stop, with no error or other signal. Fix: in the queued callback, return without calling the engine when `!webcamOn` (the parked state is already set by the off), or put the off on the queue too.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:709 · github-actions[bot] · 2026-11-26T20:04:53Z

| 👮 **Wachiman** | Is the third constructor argument and the held-frame behaviour verified against mediabunny 1.61? |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The comment says mediabunny writes frames on the clock and repeats the last one while none arrives, given an explicit `frameRate`. `new MediaStreamVideoTrackSource(track, config, { frameRate })` passes a third argument, and `sizeChangeBehavior: "contain"` is a new option. The engine tests replace `MediaStreamVideoTrackSource` with a `vi.fn()` mock, so nothing in the suite exercises either. The ADR marks the mid-take behaviour as pending owner QA. Was the gap-hold behaviour (the file stays continuous while the relay track is empty) checked against the real library, or only assumed from its docs? If mediabunny ignores the argument, the webcam file would have a timeline hole after the camera-off gap. Every later frame would then sit at the wrong time against `gaps` and `startOffsetMs`.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-hub.test.ts:2065 · github-actions[bot] · 2026-11-26T20:04:53Z

| 👮 **Wachiman** | Test title claims the hub reset path, which is not exercised; the stop path is untested too |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

"a bubble parked when the take is aborted or the hub reset is destroyed too" only calls `recordingAbort`. The `releaseParkedBubble()` added in the reset path (recording-hub.ts:1022) and in `applyStopWindowState` (recording-hub.ts:846) have no test. Each is a place where a parked window could be left alive for good. Add cases for those two, or narrow the title.

<!-- wachi:finding -->
