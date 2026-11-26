# kaipu-bench-wachi-v3#120 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:166 · github-actions[bot] · 2026-11-26T20:08:14Z

| 👮 **Wachiman** | A card left up during the next take can show the main window mid-recording |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Nothing hides the card when a new recording (or a screenshot) starts. The only references to `recordingReady` in main are its creation and its shutdown registration (`main/index.ts:897`, `main/index.ts:1093`). The capture toast, by contrast, is dismissed before every capture (`dismissToast: () => captureToast?.dismiss()`, `main/index.ts:670`). The PR body's step 9 expects the card to stay up through the next take, and it is still clickable. A press there goes through `act()`, which calls `openInMain`. That runs `showMainWindow()` (`main/index.ts:449-457`), which has no guard on `activity.active`. The hub hides the main window at `recordingStart` (`recording-hub.ts:689`) so it stays out of the video. Pressing Open, Edit first or a chip during a take therefore brings the main window on screen and into the capture, and navigates the recorder's own renderer away. Content protection only keeps the card itself out of the capture.

Fix: have `RecordingReadyWindow` close when a take starts. For example, the hub calls `close()` on `recordingStart`, or `act()` ignores presses while `hub.isActive()` or `hub.isPending()`. Add a test for it.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-26T20:08:14Z

| 👮 **Wachiman** | \`recording-ready:show\` does not check which window is asking |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The card's three listeners (`cardReady`, `resize`, `action`) check `isOwnSender`, but the `ipcMain.handle` for `recordingReadyShow` accepts any sender. Every window that loads the shared preload, such as the capture toast, the control bar or the camera bubble, can call `window.electronAPI.showRecordingReady`. That lets it replace the card's `assetId` and so steer later hand-offs. `micLevelsReport` in `recording-hub.ts:786` restricts itself to the main window's webContents. Payload validation already exists. Consider also checking that `event.sender` is the main window's webContents, which the `openInMain` caller could pass in as a dep.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:134 · github-actions[bot] · 2026-11-26T20:08:14Z

| 👮 **Wachiman** | \`show()\` returns true for a window whose renderer never loads, so the card is silently lost |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`show()` answers true as soon as `createWindow` returns. If `loadURL` or `loadFile` fails (the promise is discarded with `void` in `createRecordingReadyWindow`), the renderer never sends `card-ready`, `rendererReady` stays false and nothing is shown. The page's in-app fallback only runs on a false answer (`use-floating-ready-card.ts:27`), so the user gets no card at all, and no later `show()` fixes it because the same window is reused. The PR notes this limit. Consider handling `did-fail-load` or a ready timeout by recreating the window or answering the fallback.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-26T20:08:14Z

| 👮 **Wachiman** | Router Back to the arrival entry floats the card again |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The ask is keyed on `location.key` and gated on `location.state.fromRecording`, which stays on the history entry (set at app-root.tsx:75, never cleared). The `asked` ref in `use-floating-ready-card.ts:18` and `cardDismissedFor` both reset when the page remounts. So the user picks a chip or Open on the floating card, the main window navigates to Prepare, and Back returns to the same entry. The page remounts, `showCard` is true again, and the card floats again over whatever app is in front. The in-app card had the same quirk, but a floating always-on-top window is far more intrusive. Consider clearing the state with `navigate(location.pathname, { replace: true, state: null })` once the card has been asked for.

<!-- wachi:finding -->
