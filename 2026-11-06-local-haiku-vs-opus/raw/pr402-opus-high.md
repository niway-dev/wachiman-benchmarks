# Wachiman review of branch `bench/pr-402` of pr-402 against origin/replay/pr-402/base (merge-base a25424d), at 01dfe73

All 26 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

4 finding(s): 1 to fix, 3 to consider

## Findings

### 🟠🐛 **Fix · bug: A crashed shade renderer is never replaced; the countdown shade stays blank for the rest of the session (confidence medium)**

`apps/kaipu-record/src/main/recording/recording-shade-window.ts:187`

The shade window used to be destroyed on every `hide` and created fresh for each take, so a renderer that crashed only cost that one take. Now one window is kept for the whole session, and `ensureWindow` only replaces it when `isDestroyed()` is true, i.e. after `closed` (lines 135, 187-193). A renderer crash does not close the BrowserWindow and does not emit `closed`. Nothing listens for `render-process-gone` here, and the hub's only such listener (recording-hub.ts:737) is for mic levels. After a crash, `ready` stays true. Each later `show` takes the reused path, sends state to a dead webContents and calls `showInactive` on a window with nothing in it. The user gets no countdown number, no dimming and no REC border for every take until the app restarts, and nothing tells them. The capture overlay windows do handle `render-process-gone`. The same handling here would fix it: on `webContents` `render-process-gone`, destroy the window, or set `this.window = null` and `ready = false`, so the next `show` or `prewarm` loads a new one.

### 🟡🧪 **Consider · tests: Test name says "crash" but only a destroyed window is covered (confidence high)**

`apps/kaipu-record/src/main/recording/recording-shade-window.test.ts:191`

"loads a new window when its page is gone (crash, closed)" only calls `destroy()`, which fires `closed`. A renderer crash leaves the window alive, and nothing in the class handles that case (see the finding at recording-shade-window.ts:187). Either add the crash case together with a `render-process-gone` handler, or drop "crash" from the name.

### 🟡🐛 **Consider · bug: A countdown acquisition that already failed is reused, so the app hides and then the take fails (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:330`

`startTake` reuses `early` whenever `needsNewAcquisition` is false. It does not check whether `early.acquired` already rejected or whether `early.failure` was set during the countdown (by `onError` at line 456, for example when the screen capture ends). `hideAppForTake` then hides the main window and announces the take (line 338). `beginTake` throws the stored failure (lines 526/529), and `recordingStop` brings the window back. The result is a hide and restore flash followed by an error toast, for a failure that was already known before the hide. A transient failure is also never retried, even though acquiring again at countdown end would match the old behaviour. Suggestion: record when the early acquisition has settled with an error or a `failure`, and in that case discard it and acquire again (or fail before hiding).

### 🟡❓ **Consider · question: Does a spare overlay that is reused for a later pick keep the intent of its first pick? (confidence low)**

`apps/kaipu-record/src/renderer/src/features/screenshots/overlay/capture-overlay.tsx:149`

`openedIntent` is set only once: `opened ?? incoming.intent ?? "capture"`. After that, every later state message leaves it alone. Suppose main reuses the same preloaded (`spare=1`) window for another pick without reloading or remounting it (the PR says it reuses preloaded overlay windows on every pick). Then the `query.intent` the children read would stay on the first pick's intent, even if the next pick opens for the other one. Does main reload the window, or reset this state, between picks?

## Summary

**Batch 1 of 3.** Part 1 (main process, preload/shared types, engine split, overlay spare reuse) mostly holds together. One defect: the countdown shade window now lives for the whole session but is only replaced when it is closed. A renderer crash is never detected, so the shade stays blank for the rest of the session. Its test claims to cover crashes but only covers a closed window.

**Batch 2 of 3.** I reviewed part 2 of 3 and found nothing blocking: one suggestion and one question for the author.

**What the change does.** `recorder-store.ts` now opens the take (session file, screen, mic, encoder, cursor track) while the countdown runs, and starts encoding only once the countdown ends and the app window is hidden. I checked the paths that matter:
- **Cancel during the countdown** releases everything that was opened.
- **Settings changed mid-countdown:** a different source, area, quality, watermark or mic device throws the early acquisition away and acquires again.
- **Mic, system-audio and level changes** made during the countdown reach the prepared engine through the live-settings forwarder.
- **Bounded wait:** the 10 s start timeout covers the whole start, and starts counting when the countdown ends.

**Suggestion (`recorder-store.ts:330`).** If the early acquisition fails during the countdown, it is still reused at the end. The app hides, the take fails straight away, and the window comes back with an error toast for a failure that was already known. A transient failure is also never retried.

**Question (`capture-overlay.tsx:149`).** In the preloaded overlay window, the intent is fixed by the first state message and never changes after that. If main reuses that window for a later pick without reloading it, the later pick could open with the wrong intent. I couldn't confirm from this part whether main reloads it.

The other files read fine:
- `overlay-query.ts` parses the new `spare` flag correctly.
- `main.tsx` mounts the shade without URL parameters.
- The shade tests now pass an explicit initial state and cover the new neutral and reset states.
- The new `prepareEngine` tests check that nothing is encoded before the take begins and that releasing frees every device.

**Batch 3 of 3.** I found nothing to flag in part 3. I checked the rewritten recorder-store tests against the head `recorder-store.ts` (`requestStartRecording`, `acquireDuringCountdown`, `startTake`, `needsNewAcquisition`, `hideAppForTake`, `stopOrCancelRecording`, `acquireStart`, `beginTake`, `discardStart`). Each assertion I traced matches the code:
- **Call order:** create, then prepare, then the hide (`recordingStart`), then `begin`.
- **Countdown cancel:** the take is released and its file aborted, with no `recordingStop` because the app was never hidden.
- **Failures:** a failure held from the countdown fails the start when the countdown ends, and the hide is undone.
- **Settings during the countdown:** the forwarder starts while the countdown runs, and `sync` applies the mic and system-audio toggles before `begin`.
- **Hide wait:** the 50 ms wait (`WINDOW_HIDE_SETTLE_MS`) happens only when the window was on screen.

The `setup.ts` stub for `recordingHideMainWindow` matches what the store expects. I did not trace the overlay tests for spare windows into the overlay component; I read them only for internal consistency. The new "Start sequence" section in `recording-pipeline.mdx` describes what the code does. That covers the acquisition order, the reasons for acquiring again, the order of the hide request and the IPC answer, the 50 ms wait, the cancel and failure handling, and the first tick going out at once. I did not check its claims about mediabunny's internals against the library itself.

<details><summary>What the change connects to (11 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Renderer invokes recordingHideMainWindow at the end of a countdown (`apps/kaipu-record/src/main/recording/recording-hub.ts:599`) — The main window leaves the screen before the take begins encoding; the recorder waits when told true. If it fails: The handler takes no input and is synchronous; a missing or destroyed window answers false. How the renderer handles a rejected invoke is in another part. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:599-604`, `apps/kaipu-record/src/preload/index.ts:135`, `apps/kaipu-record/src/main/recording/recording-hub.test.ts:224-243`.
- Shade window prewarmed at launch and reused across takes (`apps/kaipu-record/src/main/recording/recording-shade-window.ts:57`) — The countdown shade appears without waiting for a renderer load. If it fails: A window that is closed or destroyed is recreated by ensureWindow. A renderer crash is not detected, so the shade stays blank for the session (finding). Evidence: `apps/kaipu-record/src/main/recording/recording-shade-window.ts:72-92`, `apps/kaipu-record/src/main/recording/recording-shade-window.ts:105-116`, `apps/kaipu-record/src/main/recording/recording-shade-window.ts:134-195`, `apps/kaipu-record/src/main/recording/recording-hub.ts:737`, `apps/kaipu-record/src/main/index.ts:1029-1033`.
- Overlay spares keyed only by display geometry; mode, intent and frame display sent as state before show (`apps/kaipu-record/src/main/screenshots/capture-overlay-windows.ts:404`) — Picks in another mode, intent or cursor display reuse the loaded windows. If it fails: When the displays differ, the spares are destroyed and fresh windows are loaded. The renderer's spare=1 handling is in another part. Evidence: `apps/kaipu-record/src/main/screenshots/capture-overlay-windows.ts:238-251`, `apps/kaipu-record/src/main/screenshots/capture-overlay-windows.ts:399-412`, `apps/kaipu-record/src/main/screenshots/capture-overlay-windows.ts:476-480`, `apps/kaipu-record/src/main/screenshots/capture-overlay-windows.ts:686-700`, `apps/kaipu-record/src/main/screenshots/screenshot-ipc.ts:82-87`.
- prepareEngine/begin/release split (`apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:205`) — The take starts as the countdown ends. If it fails: If output.start rejects, begin calls releaseAll and rethrows. A screen track that ends during the countdown fires onError. How the store reacts is in another part. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:526-547`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:657-706`.
- Acquire the take (session file, screen, mic, encoder, cursor track) during the countdown (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:266`) — The countdown hands over to recording without the roughly 1 s 'Starting…' wait. Devices (and the mic indicator) are open during the countdown. If it fails: A rejection during the countdown is swallowed (line 506) and only surfaces at countdown end, after the app has been hidden (see finding). A hang is bounded by START_TIMEOUT_MS, counted from countdown… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:266-283`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:330-343`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:398-408`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:505-506`.
- Hide the main window via recordingHideMainWindow, then wait 50 ms if it was visible (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:380`) — The app is out of the first encoded frame. If it fails: A rejection is treated as visible (waits 50 ms). An invoke that never answers keeps `hidden` pending, and `began` is then bounded by the 10 s START_TIMEOUT_MS race, which fails the usual way (toast,… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:380-389`, `apps/kaipu-record/src/main/recording/recording-hub.ts:599-604`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:537-546`.
- What bounds the start wait: acquired + hidden + prepared.begin raced against START_TIMEOUT_MS (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:525`) — Worst case: 'Starting…' for 10 s, then an error toast and the app restored. If it fails: The timeout or a cancel sets pendingStart=null; `began` re-checks pendingStart after awaiting hidden, so a late resolution does not begin encoding. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:525-546`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:577-598`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:658-661`.
- Live-settings forwarder attached to the prepared engine during the countdown (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:490`) — Mic, system-audio and level changes made during the countdown are in effect at the first frame. If it fails: Once discarded, writeBack is inactive (active=false), so a stale engine cannot rewrite the user's settings. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:712-812`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:559-560`.
- Cancel during the countdown after the take was acquired early (tests at recorder-store.test.ts:726 and :749) (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.test.ts:726`) — The countdown overlay goes away and the store is idle. No bar or shade was shown for this take. If it fails: If the acquisition settles after the cancel, discardStart releases it through start.engine.then(release). If the acquisition rejects, the error is swallowed, and acquireStart's catch keeps it from be… Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:398-408`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:658-666`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:505-507`.
- Input changed between the countdown's acquisition and its end, which forces a second acquisition (test at recorder-store.test.ts:272) (`apps/kaipu-record/src/renderer/src/features/recording/recorder-store.test.ts:272`) — The take records the new source or area, and the status reaches recording. If it fails: If the fresh acquisition fails, beginTake's catch discards it, calls recordingStop and goes idle with an error toast. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:311-344`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:355-372`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:577-598`.
- Wait for the main window to hide before the take encodes, using the new recordingHideMainWindow IPC (test :685, setup.ts:171 default) (`apps/kaipu-record/src/renderer/src/test/setup.ts:171`) — The take's first frames do not show the app window. If it fails: A rejection is treated as visible, so the cost is only 50 ms. If the invoke never answers, the START_TIMEOUT_MS race in beginTake fails the start and restores the app. Evidence: `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:380-389`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:89`, `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:537-546`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 3 | 15 | 998 | 8 | reviewed | 7 | $0.55 |
| Batch 2 of 3 | 6 | 701 | 4 | reviewed | 7 | $0.68 |
| Batch 3 of 3 | 5 | 625 | 2 | reviewed | 4 | $0.51 |

Cost: $1.74, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 3 call(s), 18 turn(s), 3 min 4 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of 01dfe73 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/main/recording/recording-shade-window.ts:187 · 🟠🐛 Fix · bug: A crashed shade renderer is never replaced; the countdown shade stays blank for the rest of the session (confidence medium)
   The shade window used to be destroyed on every `hide` and created fresh for each take, so a renderer that crashed only cost that one take. Now one window is kept for the whole session, and `ensureWindow` only replaces it when `isDestroyed()` is true, i.e. after `closed` (lines 135, 187-193). A renderer crash does not close the BrowserWindow and does not emit `closed`. Nothing listens for `render-process-gone` here, and the hub's only such listener (recording-hub.ts:737) is for mic levels. After a crash, `ready` stays true. Each later `show` takes the reused path, sends state to a dead webContents and calls `showInactive` on a window with nothing in it. The user gets no countdown number, no dimming and no REC border for every take until the app restarts, and nothing tells them. The capture overlay windows do handle `render-process-gone`. The same handling here would fix it: on `webContents` `render-process-gone`, destroy the window, or set `this.window = null` and `ready = false`, so the next `show` or `prewarm` loads a new one.
2. apps/kaipu-record/src/main/recording/recording-shade-window.test.ts:191 · 🟡🧪 Consider · tests: Test name says "crash" but only a destroyed window is covered (confidence high)
   "loads a new window when its page is gone (crash, closed)" only calls `destroy()`, which fires `closed`. A renderer crash leaves the window alive, and nothing in the class handles that case (see the finding at recording-shade-window.ts:187). Either add the crash case together with a `render-process-gone` handler, or drop "crash" from the name.
3. apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:330 · 🟡🐛 Consider · bug: A countdown acquisition that already failed is reused, so the app hides and then the take fails (confidence medium)
   `startTake` reuses `early` whenever `needsNewAcquisition` is false. It does not check whether `early.acquired` already rejected or whether `early.failure` was set during the countdown (by `onError` at line 456, for example when the screen capture ends). `hideAppForTake` then hides the main window and announces the take (line 338). `beginTake` throws the stored failure (lines 526/529), and `recordingStop` brings the window back. The result is a hide and restore flash followed by an error toast, for a failure that was already known before the hide. A transient failure is also never retried, even though acquiring again at countdown end would match the old behaviour. Suggestion: record when the early acquisition has settled with an error or a `failure`, and in that case discard it and acquire again (or fail before hiding).
4. apps/kaipu-record/src/renderer/src/features/screenshots/overlay/capture-overlay.tsx:149 · 🟡❓ Consider · question: Does a spare overlay that is reused for a later pick keep the intent of its first pick? (confidence low)
   `openedIntent` is set only once: `opened ?? incoming.intent ?? "capture"`. After that, every later state message leaves it alone. Suppose main reuses the same preloaded (`spare=1`) window for another pick without reloading or remounting it (the PR says it reuses preloaded overlay windows on every pick). Then the `query.intent` the children read would stay on the first pick's intent, even if the next pick opens for the other one. Does main reload the window, or reset this state, between picks?
```
