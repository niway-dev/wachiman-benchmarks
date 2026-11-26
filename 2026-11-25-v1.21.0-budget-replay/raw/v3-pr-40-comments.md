# kaipu-bench-wachi-v3#40 [replay r2] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:208 · github-actions[bot] · 2026-11-25T23:56:44Z

| 👮 **Wachiman** | Content protection is the card's only guard against being captured, and it does nothing on Linux |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The card has no timer, so it stays up across the next take. Nothing hides it when a screenshot or recording starts. The only thing keeping it out of the capture is `setContentProtection(true)` (line 208), and Electron implements that only on macOS and Windows; on Linux it does nothing. The capture toast it copies has a first guard as well: `captureWindowHooks` gets `dismissToast: () => captureToast?.dismiss()` (`apps/kaipu-record/src/main/index.ts:670`), and the toast's own comment calls content protection the "second guard behind `beforeCapture` dismissing it" (`apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:305-306`). `recordingReady` is never wired into those hooks or into the recording start. On a Linux build (the repo has `build:linux`), a card left up shows in the next screenshot or recording of that display, with no warning. Fix: hide it (`recordingReady?.close()`) from the same capture hook, and also when a recording starts.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-25T23:56:44Z

| 👮 **Wachiman** | \`recording-ready:show\` accepts any renderer, not only the main window |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The card-side channels check `isOwnSender` (lines 108-125), but the `recordingReadyShow` handler checks no sender at all. The preload exposes `showRecordingReady` to every window that loads it (`apps/kaipu-record/src/preload/index.ts:244`): the capture toast, the control bar, the camera bubble and the card itself. The payload is parsed, so the risk is low. Still, the contract says the request comes from the main window (`ipc.ts:530`). Checking `event.sender === mainWindow.webContents` would keep the bridge only as wide as that contract.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:171 · github-actions[bot] · 2026-11-25T23:56:44Z

| 👮 **Wachiman** | An action on a card whose recording was deleted still navigates to it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The card stays up indefinitely, so the user can delete the recording in the Library while it floats. The toast's equivalent hand-off looks the item up first and drops the open when it is gone (`apps/kaipu-record/src/main/index.ts:683-694`). Here `act` hands off the stale `assetId` with no check, and Prepare, the editor or the detail page opens on a missing asset. You could check the asset in `openInMain`, or hide the card when its asset is deleted.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48 · github-actions[bot] · 2026-11-25T23:56:44Z

| 👮 **Wachiman** | Docstring says the card goes away when the user leaves the page, which the floating window does not do |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The updated comment still says the card "stays until the user picks something, closes it or leaves the page". The floating window outlives every page: it closes only on an action, ✕ or Escape (`recording-ready-window.ts:89-90`). Only the in-app fallback ends when the user leaves the page.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:140 · github-actions[bot] · 2026-11-25T23:56:44Z

| 👮 **Wachiman** | The card now waits for the file probe, with no timeout and no fallback |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

Before this change the in-app card showed as soon as `showCard` was true and used `video.durationSeconds` until the probe came back. Now the floating window is only requested once `probeState.status` is "ready" or "error" (line 140), and the in-app card only shows after main answers false (`showInAppCard`, line 155). `probeSource` catches its own errors and returns null (probe-source.ts:42-43), so a rejection is covered. But `useSourceProbe` has no timeout (use-prepare-copy.ts:51-59). If reading `kaipu-media://recording/<id>` never settles, the request is never sent and the in-app card never renders, so the user gets no card at all and nothing says why. One option is to send the request after a short deadline with `preparable.durationSeconds` and `dimensions: null`, which the payload already allows.

<!-- wachi:finding -->
