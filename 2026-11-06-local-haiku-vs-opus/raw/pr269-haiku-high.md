# Wachiman review of branch `bench/pr-269` of pr-269 against origin/replay/pr-269/base (merge-base 58a95f9), at 3159fb1

All 12 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

11 finding(s): 1 to fix, 9 to consider

## Findings

### 🟠🐛 **Fix · bug: fps cap drops about half the frames of a source that already runs at the cap (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:293`

The Small-file fps cap anchors `nextSlot` on the last kept frame (`nextSlot = outTs + minFrameGap`, line 294) and drops any frame that arrives before `nextSlot - 1e-6` (line 293). A source whose timestamps are not exact multiples of the cap interval lands slightly early against that anchor, so the frame after a kept one is often dropped. Example at a 30 fps cap: frames at 0.0000 and 0.0334 are kept (nextSlot becomes 0.06673), the frame at 0.0667 is dropped, and the next kept frame is at 0.1001. The output runs near 15 fps with no error. The cap applies to Small-file rungs below 1080p (export-presets.ts:356), so a 30 fps recording is the common case. A tolerance of half a gap (`outTs < nextSlot - minFrameGap / 2`) keeps the cadence. Confidence is medium because I did not read the recorder's timestamp code; the bug needs jitter in the source timestamps.

### 🟡🐛 **Consider · bug: Small file that cannot meet its cap is still encoded, over the cap, with no error (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:378`

resolveSmallFile sets `achievable = false` when even the lowest rung exceeds the budget (lines 372-381), and the worker then encodes at the floor. For 10 minutes at the 480p floor (250 kbps video + 64 kbps audio) that is about 23.5 MB against a 10 MB cap. Nothing in this PR reads `achievable`: a grep finds only export-presets.ts and its test. The page never sets presetId, so this is latent. Before the sheet offers Small file, either check `achievable` in the UI or refuse in the worker.

### 🟡📝 **Consider · docs: maxDurationSec is computed at the chosen rung, but its doc says the lowest rung (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:387`

The interface comment says `maxDurationSec` is the longest duration that fits the cap 'at the lowest rung' (line 182). The code divides by `pick.rung.floorBps` (line 387). `pick` is the highest rung that fits, or the lowest rung only when none fits. The two statements disagree, so either the comment or the code is wrong. No UI reads the field yet.

### 🟡🐛 **Consider · bug: packetCountsFor breaks its own 'never less than 30 fps' rule when maxFps is set (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:225`

The doc comment (lines 210-212) says the video rate 'never assumes less than 30 fps' because a variable-rate recording can burst. The maxFps branch (lines 223-225) uses `min(maxFps, max(1, fps))`, so a source below 30 fps with a 30 fps cap is counted at its own rate. The count can then be too small. The consequence is the FR9 retry in use-video-export.ts:210-221: the whole export runs a second time without fast start. The output is not corrupt, but the cost is a full re-encode. Either make the code match the comment, or correct the comment.

### 🟡📝 **Consider · docs: Discord limit cited as 20 MB, but the small-25 preset caps at 25 MB (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:14`

Line 13 cites Discord's no-Nitro limit as 20 MB. Line 14 then says the 25 MB cap is 'chat with margin'. A 25 MB file is over the 20 MB limit this comment cites. Which destination does `small-25` target, and is the 20 MB figure current? The comment should state one consistent reason for the 25 MB number.

### 🟡🐛 **Consider · bug: Blur padding downscales with default smoothing, so it aliases rather than blurs (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/compose-output-frame.ts:192`

The tiny canvas is about 1/24 of the output, so the view is downscaled roughly 40 to 60 times in one drawImage call (lines 191-203). `tinyCtx` keeps the default imageSmoothingQuality ('low'), which samples only a few source pixels per output pixel. The padding then looks like a noisy sample of the frame, not the averaged blur the comment describes (line 177). Setting `tinyCtx.imageSmoothingQuality = "high"`, or downscaling in several steps, would average the pixels. Confidence is medium because the result depends on the platform's drawImage implementation.

### 🟡🧪 **Consider · tests: createFramer and the other new worker logic have no tests (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/compose-output-frame.ts:173`

createFramer (lines 173-216), including the covers check and the blur and black padding, has no test. Neither does downmixToMono (export-worker.ts:440) or the fps cap (export-worker.ts:293). The worker cannot be unit-tested as written, so the fps-cap bug above went unnoticed. Moving the cap decision into a pure function next to framingRect would let it be tested.

### 🟡📝 **Consider · docs: Frame-cap comment says durations come from timestamp deltas; the code passes an explicit duration (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:291`

The comment at lines 290-292 says the kept frame's sample lasts until the next kept one because 'the muxer derives durations from timestamp deltas'. Line 300 passes an explicit duration, `Math.max(wrapped.duration, minFrameGap)`, so the muxer does not derive it. The code can work in practice because the explicit duration is at least the gap, but the comment describes the wrong mechanism.

### ⚪📝 **Info · docs: Presets are not reachable from the UI in this PR, but the Original path changes for every export (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:119`

The page starts the export without presetId or sourceInfo (video-editor-page.tsx:599), so every real export takes the Original path with defaults. Presets are therefore only reachable through the hook's API. The Original path does change for all users: fastStart is now 'reserve' (export-worker.ts:146), the encoder choice is gated by canEncodeVideo (export-worker.ts:161-171), and a packet overflow restarts the export once (use-video-export.ts:210-221). The PR body's 'export presets pipeline' wording is accurate, but the Original changes are user-visible and are not described.

### 🟡📝 **Consider · docs: Doc describes the sidecar field, title suffixes and remembered preset as current behaviour; none exist at head (confidence high)**

`apps/documentation/src/content/docs/backlog/export-presets.md:33`

The 'What the user gets' section (lines 32–35) says the last preset and framing are remembered app-wide in settings, that the exported library item carries `exportPreset` in its sidecar, and that the title suffix depends on the preset ('(YouTube)', '(vertical)', '(10 MB)', …). None of this is in the repository at head. `exportPreset` appears nowhere outside this doc. The hook always finalizes with `t("editedTitle", { title: args.title })` and passes no preset field (use-video-export.ts:233-240). Presets are also not reachable from the UI: video-editor-page.tsx:599 calls `videoExport.start` without `presetId`, `framing` or `sourceInfo`, and export-sheet.tsx:53 says the presets row is still to be added. The status banner says these are PRs 2 and 3 of a stack, but the body is written in the present tense with no per-section marker, so a reader of this PR would take them as shipped. Mark the PR-2/PR-3 items as planned, or name the PR that delivers each one.

### 🟡📝 **Consider · docs: Small-file post-export size check and retry are documented as implemented; this branch has neither (confidence high)**

`apps/documentation/src/content/docs/backlog/export-presets.md:63`

The 'How it works → Small file' paragraph (lines 63–66) says that after the worker finishes, 'the hook stats the temp file (`recordingStat` IPC)', re-encodes once at a lower rate when the file is over the cap, and shows 'Making it smaller…' and 'Export anyway'. At head there is no `recordingStat` symbol anywhere in the repository. The hook's done path finalizes straight away with no size check (use-video-export.ts:224-253), and the export sheet has no preset warning (export-sheet.tsx:53). This is the design of PR 3 written in the present tense. Label it as planned, as the status banner does for the stack.

## Summary

**Batch 1 of 2.** Reviewed all 8 files in this part. The main new risk is the Small-file fps cap in export-worker.ts:293: its 1e-6 tolerance and anchoring on the last kept frame drop about half the frames of a source already at the cap when timestamps jitter (fix, medium confidence). The rest is consider or info: an over-cap Small-file path that nothing checks (achievable is never read), a maxDurationSec doc/code mismatch, a packet-count comment the code does not follow, a Discord 20 MB vs 25 MB comment that conflicts, blur padding that aliases, missing tests for createFramer and the fps cap, and one stale comment on durations. Two behaviour changes need a check outside this diff: mediabunny's overflow error text and whether canEncodeVideo accepts QUALITY_HIGH. mediabunny is not installed in the snapshot, so its APIs were not verified. The page passes no presetId, so the presets are not reachable from the UI in this PR, but every export now takes the changed Original path. Nothing was built or run.

**Batch 2 of 2.** Four files in this part reviewed: two test files and two backlog docs. I did not run the tests (read-only), so I checked the test assertions by hand against export-presets.ts, use-video-export.ts and export-worker.ts. The numeric expectations for dimensions, bitrates, the Small-file ladder (achievable flags, heights, max durations), packet counts and the size estimate all match the code. The FR9 retry test matches the hook's flow. I found no test asserting the wrong thing. The findings are two backlog-doc claims that describe PR 2 and PR 3 behaviour in the present tense: the sidecar `exportPreset` field, preset title suffixes, settings memory, and the post-export `recordingStat` size check. None of these exist at head. Also, presets cannot be reached from the UI in this PR: video-editor-page.tsx:599 always starts Original. The index.mdx row and the sidebar entry are consistent with the doc. No ADRs exist in the snapshot to check against.

<details><summary>What the change connects to (9 closed, 4 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Mp4OutputFormat fastStart changes from false to 'reserve' for every preset, Original included, with maximumPacketCount set on each track (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:146`) — Does mediabunny's reserve path throw the 'maximum packet count' text on overflow, and does it throw when maximumPacketCount is missing? mediabunny is not installed in this snapshot, so neither can be read here. Files that would answer it: `node_modules/mediabunny (absent from the snapshot)`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts`.
- CanvasSource hardwareAcceleration becomes conditional on canEncodeVideo('avc', ...) for the output size (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:161-171`) — Does canEncodeVideo accept the QUALITY_HIGH sentinel as `bitrate`? If it does not, the probe returns false on every export and every export loses prefer-hardware. Files that would answer it: `mediabunny type declarations for canEncodeVideo (absent from the snapshot)`.
- Small-file fps cap drops clip frames before the next slot (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:293-294, 300`) — Do the source frame timestamps from the recorder vary from the exact 1/30 grid by more than a fraction of a frame? If they are exact, the frame drop does not happen. Files that would answer it: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/rebase-timestamp.ts`.
- Export from the editor with no preset: the sheet's Export calls start() with no presetId, so it resolves to Original (`apps/kaipu-record/src/renderer/src/pages/video-editor/video-editor-page.tsx:599`) — Does the default export without presetId produce the same packet layout and size as the pre-PR export? That needs the base-commit version of use-video-export.ts and export-worker.ts, which were not read. Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts (base commit 58a95f9)`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts (base commit 58a95f9)`.

**Closed, with the lines they rest on**
- start() resolves the export target (size, framing, bitrates, packet counts) before the source is fetched (`apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:120`) — None for Original, the only preset the page can select (video-editor-page.tsx:599 passes no presetId). If it fails: resolveExportTarget throws only for an id missing from PRESETS (export-presets.ts:256, and preset.canvas is dereferenced at line 292). It runs after activeRef is set true (use-video-export.ts:107) an… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:107-108`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:119-134`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:256-258`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:292`.
- Worker probes the source with videoTrack.computePacketStats(240) before the output is started (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:203`) — None on success. If it fails: A rejection becomes null (line 203 catch) and the code uses 30 fps (line 206). Silent, and the renderer's estimate still bounds the reservation. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:203-213`.
- Fixed-canvas presets compose a source-size view and then frame it onto the target canvas (createFramer) (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:119-156, 296, 317; apps/kaipu-record/s…`) — None in this PR: no UI passes a fixed-canvas preset. When enabled, the output is Fit with padding or a Fill crop. If it fails: If tinyCtx is null (compose-output-frame.ts:182), blur padding silently becomes black padding. No error is raised. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:119-156`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:296`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:317`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/compose-output-frame.ts:178-209`.
- A packet-reserve error triggers one relaunch with fastStart false (`apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:209-222`) — The progress bar resets to 0 and the export restarts. The output is a file without fast start. If it fails: A rejected relaunch goes to fail if still active (lines 218-219). Stray messages from the dead worker are dropped by the workerRef check (line 202). cancel() during the relaunch is honoured by the ac… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:183`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:189`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:202`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:210-221`.
- A Small-file target with achievable false is encoded at the floor bitrate (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:378-381`) — None today, because no UI reads achievable. The worker encodes and finalises a file over the cap. If it fails: Silent over-cap output (see the consider finding at export-presets.ts:378). Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:372-384`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:196-198`.
- Small-file audio is averaged to mono per decoded sample (downmixToMono) (`apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:356-362, 436-458`) — Small-file audio is mono. If it fails: A copyTo error reaches the runExport catch and is posted as an error message (lines 91-94). finally cancels the output (lines 391-400). The failure is visible. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:356-362`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:436-458`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:91-94`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:391-400`.
- Adds backlog/export-presets to the Backlog sidebar (`apps/documentation/astro.config.mjs:91`) — A sidebar link to the backlog page. If it fails: A missing page would fail the docs build. The page exists in this PR (checked with Glob). Evidence: `apps/documentation/astro.config.mjs:90-92`, `apps/documentation/src/content/docs/backlog/export-presets.md`. ⚠️ A citation did not resolve in the head.
- start() with presetId, framing or sourceInfo (the preset path) (`apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:119-134`) — No production path reaches it in this PR. The only callers that pass presetId are the tests (use-video-export.test.ts:324, :337). Evidence: `apps/kaipu-record/src/renderer/src/pages/video-editor/video-editor-page.tsx:599-608`, `apps/kaipu-record/src/renderer/src/features/video-editor/components/export-sheet.tsx:53`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:119-134`.
- FR9 retry: a packet-count error from the worker relaunches the export once without fast start (`apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:210-222`) — The export takes longer and the file has moov at the end. The progress bar resets to 0 (:217). Nothing else changes. If it fails: A rejection from the retry's launch() reaches fail() (:218-220) and shows the generic error. A stray message from the dead worker is dropped by the workerRef identity guard (:202). A second packet-co… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:77-81`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:154-181`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:185-187`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:195-202`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:210-223`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:262-270`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 8 | 768 | 4 | reviewed | 24 | $0.27 |
| Batch 2 of 2 | 4 | 456 | 2 | reviewed | 18 | $0.16 |

## Notices

- Contract "Adds backlog/export-presets to the Backlog sidebar": evidence not verified: apps/documentation/src/content/docs/backlog/export-presets.md is not path:line.

Cost: $0.43, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 2 call(s), 42 turn(s), 8 min 44 s.

stop: complete

Claude Haiku 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of 3159fb1 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:293 · 🟠🐛 Fix · bug: fps cap drops about half the frames of a source that already runs at the cap (confidence medium)
   The Small-file fps cap anchors `nextSlot` on the last kept frame (`nextSlot = outTs + minFrameGap`, line 294) and drops any frame that arrives before `nextSlot - 1e-6` (line 293). A source whose timestamps are not exact multiples of the cap interval lands slightly early against that anchor, so the frame after a kept one is often dropped. Example at a 30 fps cap: frames at 0.0000 and 0.0334 are kept (nextSlot becomes 0.06673), the frame at 0.0667 is dropped, and the next kept frame is at 0.1001. The output runs near 15 fps with no error. The cap applies to Small-file rungs below 1080p (export-presets.ts:356), so a 30 fps recording is the common case. A tolerance of half a gap (`outTs < nextSlot - minFrameGap / 2`) keeps the cadence. Confidence is medium because I did not read the recorder's timestamp code; the bug needs jitter in the source timestamps.
2. apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:378 · 🟡🐛 Consider · bug: Small file that cannot meet its cap is still encoded, over the cap, with no error (confidence high)
   resolveSmallFile sets `achievable = false` when even the lowest rung exceeds the budget (lines 372-381), and the worker then encodes at the floor. For 10 minutes at the 480p floor (250 kbps video + 64 kbps audio) that is about 23.5 MB against a 10 MB cap. Nothing in this PR reads `achievable`: a grep finds only export-presets.ts and its test. The page never sets presetId, so this is latent. Before the sheet offers Small file, either check `achievable` in the UI or refuse in the worker.
3. apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:387 · 🟡📝 Consider · docs: maxDurationSec is computed at the chosen rung, but its doc says the lowest rung (confidence high)
   The interface comment says `maxDurationSec` is the longest duration that fits the cap 'at the lowest rung' (line 182). The code divides by `pick.rung.floorBps` (line 387). `pick` is the highest rung that fits, or the lowest rung only when none fits. The two statements disagree, so either the comment or the code is wrong. No UI reads the field yet.
4. apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:225 · 🟡🐛 Consider · bug: packetCountsFor breaks its own 'never less than 30 fps' rule when maxFps is set (confidence medium)
   The doc comment (lines 210-212) says the video rate 'never assumes less than 30 fps' because a variable-rate recording can burst. The maxFps branch (lines 223-225) uses `min(maxFps, max(1, fps))`, so a source below 30 fps with a 30 fps cap is counted at its own rate. The count can then be too small. The consequence is the FR9 retry in use-video-export.ts:210-221: the whole export runs a second time without fast start. The output is not corrupt, but the cost is a full re-encode. Either make the code match the comment, or correct the comment.
5. apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:14 · 🟡📝 Consider · docs: Discord limit cited as 20 MB, but the small-25 preset caps at 25 MB (confidence medium)
   Line 13 cites Discord's no-Nitro limit as 20 MB. Line 14 then says the 25 MB cap is 'chat with margin'. A 25 MB file is over the 20 MB limit this comment cites. Which destination does `small-25` target, and is the 20 MB figure current? The comment should state one consistent reason for the 25 MB number.
6. apps/kaipu-record/src/renderer/src/features/video-editor/export/compose-output-frame.ts:192 · 🟡🐛 Consider · bug: Blur padding downscales with default smoothing, so it aliases rather than blurs (confidence medium)
   The tiny canvas is about 1/24 of the output, so the view is downscaled roughly 40 to 60 times in one drawImage call (lines 191-203). `tinyCtx` keeps the default imageSmoothingQuality ('low'), which samples only a few source pixels per output pixel. The padding then looks like a noisy sample of the frame, not the averaged blur the comment describes (line 177). Setting `tinyCtx.imageSmoothingQuality = "high"`, or downscaling in several steps, would average the pixels. Confidence is medium because the result depends on the platform's drawImage implementation.
7. apps/kaipu-record/src/renderer/src/features/video-editor/export/compose-output-frame.ts:173 · 🟡🧪 Consider · tests: createFramer and the other new worker logic have no tests (confidence high)
   createFramer (lines 173-216), including the covers check and the blur and black padding, has no test. Neither does downmixToMono (export-worker.ts:440) or the fps cap (export-worker.ts:293). The worker cannot be unit-tested as written, so the fps-cap bug above went unnoticed. Moving the cap decision into a pure function next to framingRect would let it be tested.
8. apps/kaipu-record/src/renderer/src/features/video-editor/export/export-worker.ts:291 · 🟡📝 Consider · docs: Frame-cap comment says durations come from timestamp deltas; the code passes an explicit duration (confidence high)
   The comment at lines 290-292 says the kept frame's sample lasts until the next kept one because 'the muxer derives durations from timestamp deltas'. Line 300 passes an explicit duration, `Math.max(wrapped.duration, minFrameGap)`, so the muxer does not derive it. The code can work in practice because the explicit duration is at least the gap, but the comment describes the wrong mechanism.
9. apps/kaipu-record/src/renderer/src/features/video-editor/export/use-video-export.ts:119 · ⚪📝 Info · docs: Presets are not reachable from the UI in this PR, but the Original path changes for every export (confidence high)
   The page starts the export without presetId or sourceInfo (video-editor-page.tsx:599), so every real export takes the Original path with defaults. Presets are therefore only reachable through the hook's API. The Original path does change for all users: fastStart is now 'reserve' (export-worker.ts:146), the encoder choice is gated by canEncodeVideo (export-worker.ts:161-171), and a packet overflow restarts the export once (use-video-export.ts:210-221). The PR body's 'export presets pipeline' wording is accurate, but the Original changes are user-visible and are not described.
10. apps/documentation/src/content/docs/backlog/export-presets.md:33 · 🟡📝 Consider · docs: Doc describes the sidecar field, title suffixes and remembered preset as current behaviour; none exist at head (confidence high)
   The 'What the user gets' section (lines 32–35) says the last preset and framing are remembered app-wide in settings, that the exported library item carries `exportPreset` in its sidecar, and that the title suffix depends on the preset ('(YouTube)', '(vertical)', '(10 MB)', …). None of this is in the repository at head. `exportPreset` appears nowhere outside this doc. The hook always finalizes with `t("editedTitle", { title: args.title })` and passes no preset field (use-video-export.ts:233-240). Presets are also not reachable from the UI: video-editor-page.tsx:599 calls `videoExport.start` without `presetId`, `framing` or `sourceInfo`, and export-sheet.tsx:53 says the presets row is still to be added. The status banner says these are PRs 2 and 3 of a stack, but the body is written in the present tense with no per-section marker, so a reader of this PR would take them as shipped. Mark the PR-2/PR-3 items as planned, or name the PR that delivers each one.
11. apps/documentation/src/content/docs/backlog/export-presets.md:63 · 🟡📝 Consider · docs: Small-file post-export size check and retry are documented as implemented; this branch has neither (confidence high)
   The 'How it works → Small file' paragraph (lines 63–66) says that after the worker finishes, 'the hook stats the temp file (`recordingStat` IPC)', re-encodes once at a lower rate when the file is over the cap, and shows 'Making it smaller…' and 'Export anyway'. At head there is no `recordingStat` symbol anywhere in the repository. The hook's done path finalizes straight away with no size check (use-video-export.ts:224-253), and the export sheet has no preset warning (export-sheet.tsx:53). This is the design of PR 3 written in the present tense. Label it as planned, as the status banner does for the stack.
```
