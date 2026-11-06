# Wachiman review of branch `bench/pr-466` of pr-466 against origin/replay/pr-466/base (merge-base 13b7ff5), at b2705a9

All 28 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

4 finding(s): 4 to consider

## Findings

### 🟡🐛 **Consider · bug: `show()` answers true before the card can paint, so a card that never loads also loses the in-app fallback (confidence medium)**

`apps/kaipu-record/src/main/recording/recording-ready-window.ts:146`

`show()` returns true as soon as `ensureWindow()` has built the `BrowserWindow` (line 137). The window only paints after its renderer sends `recording-ready:card-ready` (`present()`, line 221), and `load` throws away the `loadURL`/`loadFile` promise (lines 261, 265). If the page or preload fails to load (the black-window failure CLAUDE.md describes), or the renderer crashes before `ready()`, the main window has already been told `true`. `useFloatingReadyCard` then never sets `inApp`, so the user sees no card anywhere and gets no error. That contradicts the hook's promise that the card is "never lost". One option: resolve the invoke only on `card-ready`, with a timeout that resolves false. Another: listen for `did-fail-load` / `render-process-gone` and tell the main window to fall back.

### 🟡🔐 **Consider · security: `recording-ready:show` accepts any sender (confidence high)**

`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`

The other three channels go through `isOwnSender`, but the `recording-ready:show` handler takes an invoke from any webContents running the shared preload: the card window itself, the capture toast, the capture panel and so on. The payload is parsed, so the risk is small. Still, the contract (`ipc.ts:530`) says this channel comes from the main window only. Checking the sender against the main window's webContents (passed in through deps) would keep the bridge as narrow as the doc says.

### 🟡🐛 **Consider · bug: A remount under the same history entry pops the floating card again after the user acted on it (confidence medium)**

`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`

`useFloatingReadyCard` remembers the asked key only in a ref (`use-floating-ready-card.ts:18`), and the page's dismissal lives in `useState` (`library-detail-page.tsx:129`). Both reset when the page remounts. Router Back to this entry brings back the same `location.key` and the same `fromRecording` state, so `showCard` is true again and the page calls `showRecordingReady` a second time. For example: the user presses Edit first or a chip on the floating card, main navigates the main window away, and Back then floats "Your video is ready" over the desktop again. The in-app card already reappeared on remount before this PR, but that stayed inside the page. The new window is always on top and shows on every Space, so the repeat is much more intrusive. It also contradicts the doc's "once per arrival". One fix: keep the asked keys in a module-level `Set` (or in history state) so a remount under the same key does not ask again.

### 🟡🐛 **Consider · bug: The floating card stays up after its recording is deleted (confidence medium)**

`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:214`

The in-app card went away with the page. The floating window has no tie to the page at all: `doDelete` (`library-detail-page.tsx:212-217`) removes the recording and goes back to the Library, but nothing asks main to close the card (`RecordingReadyWindow.close` is reachable only through the card's own actions, `recording-ready-window.ts:149-172`). Its chips, Edit first and Open still hand off to the deleted `assetId` (`use-recording-ready-hand-offs.ts:13-21`), and they land on a missing-file page. One fix: close the floating card when the page deletes the recording it is showing, or when main learns the asset is gone.

## Summary

**Batch 1 of 2.** Part 1 has no blockers and no defects that need fixing before merge, only two "consider" findings. The floating ready window copies the capture toast's pattern closely: the same sender checks, the same Space handling, the same content protection, and the payload and action are parsed before use. The shared contract in `shared/types/recording-ready.ts` has no value imports, as the preload rule requires.

1. **The card can be lost silently.** In `recording-ready-window.ts`, `show()` answers true as soon as the window exists, before the card has painted. If the page or preload fails to load, the main window has already been told it worked, so its in-app fallback never shows and the user sees no card at all.
2. **`recording-ready:show` accepts any sender.** The other three channels check that the message comes from the card window; this one takes a request from any of the app's windows. The payload is validated, so the risk is small.

One question stays open: when the main window has been destroyed, the hand-off is queued until the new window is ready. I did not confirm that the hand-off listener in `app-root.tsx` is subscribed by the time that queue is sent.

**Batch 2 of 2.** Part 2 wires the floating card into the render targets, the recording page and AppRoot. The page gating, the fallback when the window cannot open, the hand-off routing, the CSS sizing and the i18n keys all match the main-process window code. Two judgement calls remain. First, a remount under the same history entry (router Back) floats the card again, because the asked key lives only in a ref. Second, the floating card outlives its page, so it stays up after its recording is deleted.

<details><summary>What the change connects to (5 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Card action hands off to the main window (`openInMain`) (`apps/kaipu-record/src/main/index.ts:899`) — Is the queued `recording-ready:open` flushed after AppRoot's `onRecordingReadyOpen` subscription on a recreated main window? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/shell/app-root.tsx`.

**Closed, with the lines they rest on**
- Main window asks main to float the ready card (`recording-ready:show`) (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — The card appears inactive at the top-right of the recorded display once the card renderer sends ready. If it fails: If window creation throws, the call returns false and the page falls back to its in-app card. If the load fails or the renderer never sends ready, the call has already returned true: no card shows an… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:218-226`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:258-269`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:21-31`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:148-160`.
- Card window IPC: ready, resize and action, each with a sender check (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:108-126`) — The window resizes to fit the card. An action hides the card and then opens the main window. If it fails: Malformed or foreign messages are ignored without any log. Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:246-248`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:363-365`, `apps/kaipu-record/src/shared/types/recording-ready.ts:47-61`.
- Recording page asks main to float the ready card once the probe settles, and falls back to the in-app card (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — The floating window paints after its renderer reports ready (present()). The in-app card shows only when main answers false or the IPC rejects. If it fails: If the IPC rejects or main returns false, fallBack sets inApp and the in-app card shows. If the window is created but its renderer never loads, nothing shows (the doc admits this). On a remount under… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-32`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:219-226`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-155`.
- Main window navigates on a hand-off from the floating card (`apps/kaipu-record/src/renderer/src/shell/app-root.tsx:31`) — The main window is shown and focused by main and routed to Prepare, the editor or the detail page. If it fails: If the asset was deleted meanwhile, the hand-off lands on a missing-asset page (finding). Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`.
- New render target ?window=recording-ready (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — The card is inset 16px (body padding) and the frame height is reported; main adds 2×16 to size the window. If it fails: Under StrictMode, ready is sent twice, and main presents twice, which is harmless. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:24-53`, `apps/kaipu-record/src/renderer/src/assets/main.css:85-93`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:70-80`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 5 | $0.58 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 13 | $0.58 |

Cost: $1.16, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 2 call(s), 18 turn(s), 2 min 22 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of b2705a9 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/main/recording/recording-ready-window.ts:146 · 🟡🐛 Consider · bug: `show()` answers true before the card can paint, so a card that never loads also loses the in-app fallback (confidence medium)
   `show()` returns true as soon as `ensureWindow()` has built the `BrowserWindow` (line 137). The window only paints after its renderer sends `recording-ready:card-ready` (`present()`, line 221), and `load` throws away the `loadURL`/`loadFile` promise (lines 261, 265). If the page or preload fails to load (the black-window failure CLAUDE.md describes), or the renderer crashes before `ready()`, the main window has already been told `true`. `useFloatingReadyCard` then never sets `inApp`, so the user sees no card anywhere and gets no error. That contradicts the hook's promise that the card is "never lost". One option: resolve the invoke only on `card-ready`, with a timeout that resolves false. Another: listen for `did-fail-load` / `render-process-gone` and tell the main window to fall back.
2. apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · 🟡🔐 Consider · security: `recording-ready:show` accepts any sender (confidence high)
   The other three channels go through `isOwnSender`, but the `recording-ready:show` handler takes an invoke from any webContents running the shared preload: the card window itself, the capture toast, the capture panel and so on. The payload is parsed, so the risk is small. Still, the contract (`ipc.ts:530`) says this channel comes from the main window only. Checking the sender against the main window's webContents (passed in through deps) would keep the bridge as narrow as the doc says.
3. apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · 🟡🐛 Consider · bug: A remount under the same history entry pops the floating card again after the user acted on it (confidence medium)
   `useFloatingReadyCard` remembers the asked key only in a ref (`use-floating-ready-card.ts:18`), and the page's dismissal lives in `useState` (`library-detail-page.tsx:129`). Both reset when the page remounts. Router Back to this entry brings back the same `location.key` and the same `fromRecording` state, so `showCard` is true again and the page calls `showRecordingReady` a second time. For example: the user presses Edit first or a chip on the floating card, main navigates the main window away, and Back then floats "Your video is ready" over the desktop again. The in-app card already reappeared on remount before this PR, but that stayed inside the page. The new window is always on top and shows on every Space, so the repeat is much more intrusive. It also contradicts the doc's "once per arrival". One fix: keep the asked keys in a module-level `Set` (or in history state) so a remount under the same key does not ask again.
4. apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:214 · 🟡🐛 Consider · bug: The floating card stays up after its recording is deleted (confidence medium)
   The in-app card went away with the page. The floating window has no tie to the page at all: `doDelete` (`library-detail-page.tsx:212-217`) removes the recording and goes back to the Library, but nothing asks main to close the card (`RecordingReadyWindow.close` is reachable only through the card's own actions, `recording-ready-window.ts:149-172`). Its chips, Edit first and Open still hand off to the deleted `assetId` (`use-recording-ready-hand-offs.ts:13-21`), and they land on a missing-file page. One fix: close the floating card when the page deletes the recording it is showing, or when main learns the asset is gone.
```
