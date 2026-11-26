# kaipu-bench-wachi-v3#60 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T00:08:44Z · commit b2705a9

👮 **Wachiman** · review of the whole pull request, at `b2705a9`: all 28 files reviewed.

4 finding(s): 4 to consider; 4 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** I found no blockers or fixes in part 1, only four "consider" findings.

The floating window follows the capture toast's pattern closely: the card's IPC channels check the sender, every payload and action that crosses IPC is validated, the window is content-protected and shown with `showInactive`, and it is destroyed on quit. The contract file has no value imports, so it is safe for the preload bundle.

The four findings:
- **Back re-floats the card:** `useFloatingReadyCard` guards with a ref that resets on remount. Pressing Back to the same history entry floats the card on the desktop again, against the hook's own "once per arrival" contract.
- **No sender check on `recording-ready:show`:** unlike the card's channels, any window with the preload can call it.
- **Silent loss when the card renderer never loads:** `show()` reports success, so the page hides its in-app fallback and the card shows nowhere. The PR notes accept this.
- **Stale docstring:** `PostRecordingCard` says the card closes when the user leaves the page, which is true only for the in-app fallback.

The tests cover what their names say. Nothing was run, per the instructions.

**Batch 2 of 2.** I reviewed all 13 files in part 2 and found nothing to flag. Each file was read in full, along with the code these files call into outside this part, which I read only. The page asks main for the floating window once per history entry, and only after the file has been read or failed to read. Reading the file always finishes because `probeSource` catches its own errors. A false answer or a failed call shows the in-app card instead, so the card does not appear twice. On Back to the same page the floating card is asked for again; the old in-app card already came back that way. The floating card's buttons route through the same helpers as the in-app card (`preparePath` and `editorPathFor`). The 16 px padding in CSS matches main's window sizing. The tests check what their names say. The backlog doc's claims match the code (content protection, the macOS non-activating panel, always on top, the take's display), and so does the new sidebar/index entry. The en and es messages each gain one key, and `post-recording-card` uses it.

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Main window asks main to float the ready card (`showRecordingReady` → `recording-ready:show`) (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:26`) — The card appears inactive at the top-right of the recorded display. The page shows its in-app card only when the invoke resolves false or rejects (library-detail-page.tsx:155). If it fails: If creating the window throws, the invoke returns false and the in-app card shows. If the window is created but its renderer never reports ready (load failure, crash), the invoke still returns true:… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-107`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:218-226`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:119-120`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-31`.
- Card action hands off to the main window (`openInMain` → showMainWindow + sendToRenderer `recording-ready:open`) (`apps/kaipu-record/src/main/index.ts:897-903`) — Kaipu comes forward and the renderer navigates through pathForHandOff (use-recording-ready-hand-offs.ts:13-33). If it fails: No mainWindow webContents: sendToRenderer returns early (index.ts:146-147), but showMainWindow has just created the window, so it exists. Evidence: `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/index.ts:897-903`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-33`.
- Hub remembers the display the latest take recorded (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — The ready window opens on that display. Otherwise it opens on the display under the cursor (recording-ready-window.ts:237-244). If it fails: If the lookup fails or the source is a window, the value is null and the card falls back to the cursor's display. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:646-666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:707-714`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- Recording page asks main to float "Your video is ready" once the probe settles, and shows the in-app card only on a false answer or a rejected IPC (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — When main answers true, the floating window shows and showInAppCard stays false. When main answers false or the IPC rejects, fallbackFor is set to the key and the StatusCardPortal card renders. If it fails: A rejected IPC and a false answer both lead to the in-app card. On a remount under the same history entry (Back), the ref resets and the window is asked for again. The old in-app card also came back… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-32`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-47`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:263-277`, `apps/documentation/src/content/docs/backlog/floating-ready-window.md:55-56`.
- Hand-offs from the floating card navigate the main window (useRecordingReadyHandOffs in AppRoot) (`apps/kaipu-record/src/renderer/src/shell/app-root.tsx:31`) — The main window routes to Prepare, the editor or the recording page. Main shows and focuses the window before this runs. If it fails: Open pushes /library/:id without fromRecording state. If the page is already mounted, it keeps its instance and its asked ref, so Back does not re-float the card. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:13-34`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.test.ts:4-18`.
- New render target ?window=recording-ready renders RecordingReadyCard on a transparent body (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — The window shows the PostRecordingCard (it needs no StatusStack context) with Open wired to onOpen and the openFloatingHint title. If it fails: Until a payload arrives it renders null, so the transparent window shows nothing. Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:18-72`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-card.tsx:1-2`, `apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:122-128`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:16-19`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:73`, `apps/kaipu-record/src/renderer/src/assets/main.css:85-93`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 9 | $0.48 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 15 | $0.46 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $0.94</sub>

<!-- wachi:review -->

<!-- agent-review sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:attempt id=dcc64798-0eee-4002-9866-172b09188c9c -->
