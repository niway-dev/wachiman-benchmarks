# kaipu-bench-wachi-v3#95 [replay] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/index.ts:899 · github-actions[bot] · 2026-11-26T17:30:45Z

| 👮 **Wachiman** | openInMain un-hides the main window into an active recording |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The card has no timer and nothing closes it when a new take starts (`recordingReady` is only created at line 897 and destroyed at shutdown). The user can start another recording while it is up and then click a chip, Edit first or Open. `openInMain` calls `showMainWindow()` unconditionally. The hub deliberately hides the main window for the take (`recording-hub.ts:689`), and the repo guards against exactly this elsewhere: `triggerStartRecording` says "Don't un-hide the (deliberately hidden) main window into an active recording — it would get burned into the video" (`index.ts:475-481`), and the deep-link `focus` is guarded by `!hub?.isActive()` (`index.ts:184-186`). Here the main window appears, steals focus and navigates away from the Record page mid-take, and the recorder lives in that window. Guard `openInMain` (or `act`) on `hub?.isActive() || hub?.isPending()`: either close the card without handing off, or defer the hand-off until the take stops. Closing the card when a take starts would also fix it.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-26T17:30:45Z

| 👮 **Wachiman** | \`recording-ready:show\` does not check who is asking |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The three card-side channels check `isOwnSender`, but the `ipcMain.handle` for `recordingReadyShow` accepts any sender. Every window loads the same preload, so any of them (capture panel, toast, overlay) can call `showRecordingReady`. The payload is validated for shape, but `assetId` is free text. A caller can therefore make the card display arbitrary numbers, and the card's action then navigates the main window to `/library/<that id>`. The sender here should be the main window's webContents. `registerRecordingHub` takes a `getMainWindow` getter, so `createRecordingReadyWindow` could take one the same way and compare `event.sender`. The `micLevelsReport` handler (`recording-hub.ts:786`) already does this check.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:219 · github-actions[bot] · 2026-11-26T17:30:45Z

| 👮 **Wachiman** | A reshown card can flash the previous recording's content |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`close()` hides the window but leaves the card's React state on the old payload. `present()` then sends the new payload and calls `showInactive()` straight away. The IPC send is async to the renderer, so the window can paint once with the old recording's duration, size and chips (and its old height) before the new payload renders. The same applies when the same `assetId` is shown twice, because the `key` is unchanged and the card does not restart. Sending a clear (or `null`) on `close()`, or showing only after the renderer acknowledges the payload, avoids it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:47 · github-actions[bot] · 2026-11-26T17:30:45Z

| 👮 **Wachiman** | Doc comment line is over-long after the edit |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The edited JSDoc line ("when that window could not open. It asks where the video is going, with chips into Prepare, and stays until the") runs past the 100-column width the rest of the file's comments use. Re-wrap the paragraph.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.test.ts:204 · github-actions[bot] · 2026-11-26T17:30:45Z

| 👮 **Wachiman** | No test for an action arriving during an active take or after a card swap |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The tests cover close-then-hand-off ordering but nothing about hand-offs while a recording is active. That is the case in the `fix` finding on `main/index.ts:899`. `openInMain` is only a mock here, so the guard would live in `index.ts` and has no test. Add a test once the guard exists.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/assets/main.css:85 · github-actions[bot] · 2026-11-26T17:30:45Z

| 👮 **Wachiman** | 16 px window padding may clip the card's shadow into a hard edge |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The status card's shadow is `0 30px 80px -30px rgba(0,0,0,.8)` (status-card.module.css:11). It is offset 30 px down with an 80 px blur, so it reaches well past 16 px below the card, still at noticeable alpha. The transparent window is only 16 px larger than the card on every side (this rule, `READY_WINDOW_PADDING`), and `hasShadow` is false. The shadow would be cut off along the window's bottom edge, which on a transparent window shows as a faint rectangle. The doc already says size and shadow are unchecked in Electron. Check this on a real display. If it clips, give the floating card a tighter shadow or a larger padding.

<!-- wachi:finding -->
