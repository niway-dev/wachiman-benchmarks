## review by pullfrog[bot] at 2026-11-01T23:35:38Z

> ℹ️ No critical issues — one toggle race worth a look.

**Reviewed changes**

Reviewed all four commits. Together they keep a webcam file running when the camera is turned off and on mid-take, and they mark each off period as a hidden segment in the editor.

- **Park instead of destroy**: during an active take with a live webcam file, the hub now hides the bubble window and keeps it protected (`park`). Turning the camera back on shows the same window. A parked window is released at finalize, abort, stop and forced reset, and `placedBounds()` is read before that release.
- **Bubble preview follows the toggle**: `useCameraOn` drives `useCameraPreview`, so a parked bubble releases the camera itself.
- **Relay track in the engine**: the webcam encoder reads a `MediaStreamTrackGenerator` that is fed from the current camera. `frameRate` and `sizeChangeBehavior: "contain"` are both real mediabunny 1.61 options. `turnWebcamOff` / `turnWebcamOn` use `cameraRequest` so that a newer toggle supersedes an older one.
- **Gap log in the store**: `WebcamGapLog` records off periods on the take's screen clock and sends them with finalize. If the camera fails to reopen, the existing "camera wasn't available" toast is shown.
- **Sidecar and editor**: `sanitizeWebcamGaps` sorts, merges, clamps and caps the gaps. `seedWebcamScene` seeds each gap as a hidden segment stretched to the minimum segment length.

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
  - 7d1a4c6 — fix(desktop): the webcam sidecar keeps the camera-off gaps and the editor hides the face there
  - 0add032 — fix(desktop): a camera turned off mid-take parks the bubble instead of destroying it
  - 355c5b6 — fix(desktop): the recorder keeps one webcam file through a camera turned off and on
  - 3ec7a13 — docs(desktop): ADR 0032 and the webcam spec describe hide-not-destroy and the gaps
- Prior pullfrog review: none
-->


<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [Fix all ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog-v2/2?action=fix&review_id=5730804400) ｜ [Fix 👍s ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog-v2/2?action=fix-approved&review_id=5730804400) ｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog-v2/actions/runs/41362543016/job/125015796895) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

