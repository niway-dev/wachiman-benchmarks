# kaipu-bench-wachi-v3#12 [replay r3] fix(desktop): turning the camera off and on mid-take keeps the face in its own track - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:54:21Z · commit 3ec7a13

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 3 to consider · whole PR at `3ec7a13`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 3 to consider · ⚪ 0 for your information (4) · 3 Should · 1 Could |
| **Risk** | Medium: top fact `public-contract` at `webcam-track.ts:72`, see Risk facts |
| **Coverage** | 23 of 23 files reviewed, whole pull request |
| **Read first** | `webcam-track.ts`, `camera-bubble-window.ts`, `recording-hub.ts`, `bubble-protection.ts`, `recorder-engine.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`recorder-store.ts:939`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L939) | Camera reopen goes on the shared toggle queue, so a mic mute waits behind it for seconds |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 📝 docs | [`recorder-store.ts:938`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts#L938) | Comment says a following off waits on the queue, but off runs synchronously |
| 🟡 Consider · Could · ❓ question | [`recording-hub.ts:305`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/main/recording/recording-hub.ts#L305) | After a failed reopen, the face depends on a running capture picking up a dropped protection |
| 🟡 Consider · Should · 🧪 tests | [`webcam-relay.test.ts:79`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/renderer/src/features/recording/webcam-relay.test.ts#L79) | The 'late frame is dropped (and closed)' case is never asserted, and the drop branch never runs |

### Risk facts

- `public-contract` · [`webcam-track.ts:72`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/3ec7a138c3a878b38284fd13c801ab7226a34abb/apps/kaipu-record/src/shared/webcam-track.ts#L72) — The sidecar's `webcam` field gains an optional `gaps` array in screen ms; old sidecars omit it and new readers treat its absence as a take whose camera stayed on.

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Camera turned on mid-take reopens the camera into the webcam relay (turnWebcamOn) (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:779`) — The bubble window is shown at once by main. The webcam file resumes when the first frame passes, and the gap closes then (recorder-store.ts:943). If it fails: The whole wait is bounded by 2×WEBCAM_OPEN_TIMEOUT_MS (an open timeout plus a feed timeout), not the ~3 s the PR claims. On failure endWebcam reports the end and the store sets webcamReopenFailed, wh… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:784-818`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939-952`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:902-908`.
- Camera off mid-take parks the bubble instead of destroying it (`apps/kaipu-record/src/main/recording/recording-hub.ts:309`) — The bubble disappears and the camera light goes off once both the preview and the recorder tracks stop. If it fails: If the renderer never receives the settings broadcast, the preview keeps the camera open in a hidden window until the take ends. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:299-335`, `apps/kaipu-record/src/main/recording/camera-bubble-window.ts:262-266`, `apps/kaipu-record/src/renderer/src/features/camera-bubble/camera-bubble.tsx:44-61`.
- Finalize reads placedBounds before releasing a parked bubble (`apps/kaipu-record/src/main/recording/recording-hub.ts:498`) — A take that ends with a trailing gap still records the bubble layout. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:497-499`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1042`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1068`.
- Main sanitizes renderer-supplied `webcam.gaps` before writing the sidecar (`apps/kaipu-record/src/shared/webcam-track.ts:184`) — The editor seeds each stored gap as a hidden webcam segment (webcam-model.ts:111, 135-157), so the lane shows it striped and the export hides the face there. If it fails: Bad input is dropped rather than rejected, so the rest of the meta still lands on disk. Gaps past the take's end are not clamped here. The editor clamps them when durationSeconds is known (webcam-mod… Evidence: `apps/kaipu-record/src/shared/webcam-track.ts:131-154`, `apps/kaipu-record/src/shared/webcam-track.ts:184-186`, `apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:135-157`.
- Store finishes the gap log at stop and sends the gaps with finalize (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1017`) — A trailing gap ends at durationMs and is seeded as hidden through the end of the take. If it fails: When no live session exists, the gaps come back as an empty list. The take then simply has no gaps. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:1015-1017`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:961`, `apps/kaipu-record/src/renderer/src/features/recording/webcam-gaps.ts:27-30`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I reviewed every file in part 1 of 2. I read the engine's relay and toggle code, the store forwarder, and the hub's park and release logic against their callers.

1. **Fix: a camera reopen can delay the mic mute for seconds.** The reopen shares the live-controls queue with the audio toggles. Turning the mic off right after turning the camera on can wait up to twice the camera-open timeout before it takes effect. During that wait the take keeps recording audio the user meant to cut, and nothing tells them.
2. **Consider: a comment describes the queue wrongly.** It says a following camera-off waits on the queue. It does not: off runs immediately, and a late camera is released by the request counter instead.
3. **Question: does the failed-reopen fallback work?** If the camera cannot be reopened, the plan is for the face to fall back into the screen recording. That only works if a running capture picks up a protection dropped from an existing window, which the hub's own comment says is not known to work.

The whole camera-on wait is bounded by about twice the camera-open timeout, not the "about 3 s" the PR states. A parked bubble's bounds are still read correctly at finalize, because the renderer sends stop after finalize.

**Batch 2 of 2.** I reviewed the sidecar gap schema and its sanitizer, the tests for the engine, store, gap log, relay and editor seeding, and the ADR 0032 and spec updates. The gap sanitizer, the gap log and the editor seeding agree with each other: gaps are in screen ms, sorted, merged and capped, and a trailing gap is closed at the take's duration. The docs also match what the code does: a camera turned off before the take begins, or on a recorder without a relay track, keeps the old rule. I found one thing to consider, a test gap: the relay test describes a late frame being dropped and closed, but it neither asserts that nor exercises the code that closes it.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 14 | 851 | 5 | reviewed | 7 | $0.59 |
| Batch 2 of 2 | 9 | 606 | 4 | reviewed | 8 | $0.41 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 18 in / 11k out / 326k cache read / 88k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.00</sub>

<!-- wachi:review -->

<!-- wachiman sha=3ec7a138c3a878b38284fd13c801ab7226a34abb -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiIzZWM3YTEzOGMzYTg3OGIzODI4NGZkMTNjODAxYWI3MjI2YTM0YWJiIiwiYXR0ZW1wdCI6IjllMTgwZDc1LWE5MDItNDllZC04ZWE5LTk3NTcwODU5YWZiNyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=9e180d75-a902-49ed-8ea9-97570859afb7 -->
