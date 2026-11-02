=== REVIEW 5730243538 2026-11-01T21:00:44Z commit=3ec7a13
> [!IMPORTANT]
> Takes with camera-off gaps get a different export fingerprint every time they are seeded, so "already exported → reuse" stops matching for them. One smaller timing issue in the gap log is also inline.

**Reviewed changes**

I reviewed all four commits: the main-process change from destroy to park, the renderer camera relay, gap tracking in the store and sidecar, and the editor seeding.

- **Bubble parks instead of being destroyed**: during a take that records a webcam file, turning the camera off now hides and keeps the bubble window (`park()`), and it is released at finalize, abort, stop or reset.
- **Bubble preview follows the Camera toggle**: `useCameraOn()` makes the hidden window release its own camera stream.
- **Webcam relay**: the encoder reads a `MediaStreamTrackGenerator` that is fed through a `MediaStreamTrackProcessor`. It uses an explicit `frameRate` and `sizeChangeBehavior: "contain"`, and `turnWebcamOff` / `turnWebcamOn` handle supersession and timeouts.
- **Gap log in the store**: each off period is recorded in screen ms on the take's pause-aware clock. A failed re-open ends the file and shows the existing notice after the take.
- **Sidecar `webcam.gaps`**: these are sanitized (clamped, sorted, merged, capped) in `webcam-track.ts`.
- **Editor seeding**: `seedWebcamScene` turns each gap into a hidden segment. Short gaps are stretched to the minimum segment length and kept inside the recording.

<!--
Pullfrog review metadata. These findings were written against 3ec7a13;
if commits have landed on replay/pr-463/head since, treat every specific bug, file, or
line callout as POTENTIALLY STALE and re-diff before acting on it.

- Mode: Review (initial)
- Files reviewed: 23
- Commits reviewed: 4
- Base: replay/pr-463/base (c58b68f)
- Head: replay/pr-463/head (3ec7a13)
- Reviewed commits:
  - 7d1a4c6e — fix(desktop): the webcam sidecar keeps the camera-off gaps and the editor hides the face there
  - 0add032e — fix(desktop): a camera turned off mid-take parks the bubble instead of destroying it
  - 355c5b6f — fix(desktop): the recorder keeps one webcam file through a camera turned off and on
  - 3ec7a138 — docs(desktop): ADR 0032 and the webcam spec describe hide-not-destroy and the gaps
- Prior pullfrog review: none
-->


<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [Fix all ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog/1?action=fix&review_id=5730243538) ｜ [Fix 👍s ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog/1?action=fix-approved&review_id=5730243538) ｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog/actions/runs/41349360360/job/124975989043) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

