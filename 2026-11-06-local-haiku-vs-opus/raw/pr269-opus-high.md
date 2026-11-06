# Wachiman review of branch `bench/pr-269` of pr-269 against origin/replay/pr-269/base (merge-base 58a95f9), at 3159fb1

All 12 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

2 finding(s): 1 to fix, 1 to consider

## Findings

### 🟠🐛 **Fix · bug: Small file under-reserves video packets for variable-rate recordings, despite the doc comment's 30 fps floor (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:225`

The doc comment (lines 209-213) says the video rate "never assumes less than 30 fps" because a variable-rate screen recording can burst above its average. That floor only applies in the uncapped branch. When `maxFps` is set (every Small-file rung below 1080p), the rate is `Math.min(opts.maxFps, Math.max(1, opts.fps))`, so a recording whose average is, say, 10 fps reserves for about 13 fps. The cap still lets bursts through at up to 30 fps.

The worker's correction doesn't close the gap. In `export-worker.ts:203-206` it uses `computePacketStats(240)`, which only samples the first 240 packets, so a quiet opening drags the estimate down too. Once the real packet count passes `maximumPacketCount`, the muxer throws. The hook then silently re-runs the whole export with `fastStart: false` (`use-video-export.ts:210-221`). The user waits through two full encodes and gets a file without fast start, with no visible sign of either.

Suggested fix: when a cap is set, the cap is the hard upper bound, so use `Math.min(opts.maxFps, Math.max(30, Math.ceil(opts.fps)))`, which is just `maxFps` for today's 30 fps cap. That costs about 1.4 KB/s of reserve, which is small next to a 10 MB cap.

### 🟡📝 **Consider · docs: "What the user gets" describes behaviour this branch doesn't have yet (confidence high)**

`apps/documentation/src/content/docs/backlog/export-presets.md:32`

These bullets are written as if they already ship, but this branch doesn't do them. `useVideoExport` always finalizes with `title: t("editedTitle", …)` and only passes `derivedFromAssetId` (use-video-export.ts:234-240). It writes no `exportPreset` to the sidecar and adds no per-preset suffix like "(YouTube)" or "(10 MB)". No settings persistence for the last preset/framing exists either. The same goes for the `recordingStat` size check and "Making it smaller…" retry at lines 63-66: neither exists in the code (searched `apps/kaipu-record/src`).

The banner does list three stacked PRs, but the body doesn't say which PR delivers what. Consider tagging these items with the PR that brings them (UI / small-file), so the doc stays accurate when only PR 1 is merged.

## Summary

**Batch 1 of 2.** I reviewed part 1 (8 files) and found one problem, rated "fix" at medium confidence. For Small-file exports below 1080p, `packetCountsFor` in `export-presets.ts:225` skips the 30 fps floor its own doc comment promises. A screen recording whose frame rate varies, and averages low, can then outgrow the space reserved at the front of the file. When that happens the export silently runs a second time and the file comes out without fast start.

Not checked: the retry depends on mediabunny's error text containing "maximum packet count". `node_modules` isn't in the snapshot, so I couldn't confirm that wording; that contract stays open.

Checked and fine:
- **Fit/Fill framing:** redactions are applied before the frame is scaled or cropped, so they stay on the right pixels.
- **Mono downmix and silence:** consistent with each other.
- **fps cap:** keeps timestamps in order and the timeline length unchanged.
- **Retry teardown:** stale messages from the old worker are ignored, and the old writer session is aborted.

The `framingRect` tests assert the right values.

**Batch 2 of 2.** Part 2 holds the two test files and the backlog docs. I recomputed the expected values in export-presets.test.ts by hand against export-presets.ts, and every assertion matches the code. That covers the ladder rungs (e.g. small-10 at 120 s → 540p with v ≈ 521 kbps, and 300 s → not achievable with maxDurationSec 234), the pixel-scaled bitrates, packet counts, sizeForShortSide and the reservation size (≈430 KB). The new tests in use-video-export.test.ts follow the hook correctly: the default Original target, the vertical preset passed through, the single fast-start retry with a fresh session and the stale worker ignored, and a second packet-count error becoming a real failure. The doc's formulas and table match the code. One docs finding: some features the doc describes as shipping aren't in this branch (preset title suffixes, the `exportPreset` field in the sidecar, remembering the last preset in settings, and the small-file size check and retry).

<details><summary>What the change connects to (4 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Retry the export once without fast start when the moov reservation overflows (`apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:210`) — Does mediabunny's error for exceeding maximumPacketCount actually contain the text 'maximum packet count'? Files that would answer it: `node_modules/mediabunny/dist/modules/src/isobmff/isobmff-muxer.d.ts`.

**Closed, with the lines they rest on**
- Probe hardware encoder support with canEncodeVideo before creating CanvasSource (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:161`) — None. The export just uses a software encoder when hardware can't take the size. If it fails: A rejected probe is caught and treated as false, so the export carries on with 'no-preference'. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:158-171`.
- Compose a source-size view, then frame it onto the fixed preset canvas (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:296`) — The exported file shows Fit (with black or blurred padding) or Fill. Slides always use Fit. If it fails: If the view canvas has no 2D context, the worker throws, and that reaches the user as the generic error. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:150-156`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:295-297`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:315-318`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/compose-output-frame.ts:173-216`.
- FR9 fallback: a 'maximum packet count' worker error aborts the session and relaunches once with fastStart: false (exercised by the new hook tests) (`apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.test.ts:353`) — The status stays 'exporting' and progress restarts from 0. A second packet-count error, now with fastStart false, sets status 'error' with the generic message. If it fails: If the relaunch rejects, fail() runs only when activeRef is still true, so a cancel during the relaunch doesn't show an error. The tests cover a stray message from the old worker and a second failure… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:200-222`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:77-81`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:183-193`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.test.ts:76-78`.
- Tests call resolveExportTarget for each preset and source aspect and check the numbers against the code (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.test.ts:153`) — The worker gets the size and bitrates the export uses, and the sheet shows the size estimate. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:250-332`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:334-406`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:119-134`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 8 | 768 | 4 | reviewed | 6 | $0.55 |
| Batch 2 of 2 | 4 | 456 | 2 | reviewed | 7 | $0.50 |

Cost: $1.05, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 2 call(s), 13 turn(s), 2 min 20 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of 3159fb1 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:225 · 🟠🐛 Fix · bug: Small file under-reserves video packets for variable-rate recordings, despite the doc comment's 30 fps floor (confidence medium)
   The doc comment (lines 209-213) says the video rate "never assumes less than 30 fps" because a variable-rate screen recording can burst above its average. That floor only applies in the uncapped branch. When `maxFps` is set (every Small-file rung below 1080p), the rate is `Math.min(opts.maxFps, Math.max(1, opts.fps))`, so a recording whose average is, say, 10 fps reserves for about 13 fps. The cap still lets bursts through at up to 30 fps.

   The worker's correction doesn't close the gap. In `export-worker.ts:203-206` it uses `computePacketStats(240)`, which only samples the first 240 packets, so a quiet opening drags the estimate down too. Once the real packet count passes `maximumPacketCount`, the muxer throws. The hook then silently re-runs the whole export with `fastStart: false` (`use-video-export.ts:210-221`). The user waits through two full encodes and gets a file without fast start, with no visible sign of either.

   Suggested fix: when a cap is set, the cap is the hard upper bound, so use `Math.min(opts.maxFps, Math.max(30, Math.ceil(opts.fps)))`, which is just `maxFps` for today's 30 fps cap. That costs about 1.4 KB/s of reserve, which is small next to a 10 MB cap.
2. apps/documentation/src/content/docs/backlog/export-presets.md:32 · 🟡📝 Consider · docs: "What the user gets" describes behaviour this branch doesn't have yet (confidence high)
   These bullets are written as if they already ship, but this branch doesn't do them. `useVideoExport` always finalizes with `title: t("editedTitle", …)` and only passes `derivedFromAssetId` (use-video-export.ts:234-240). It writes no `exportPreset` to the sidecar and adds no per-preset suffix like "(YouTube)" or "(10 MB)". No settings persistence for the last preset/framing exists either. The same goes for the `recordingStat` size check and "Making it smaller…" retry at lines 63-66: neither exists in the code (searched `apps/kaipu-record/src`).

   The banner does list three stacked PRs, but the body doesn't say which PR delivers what. Consider tagging these items with the PR that brings them (UI / small-file), so the doc stays accurate when only PR 1 is merged.
```
