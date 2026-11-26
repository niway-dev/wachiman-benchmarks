# kaipu-bench-wachi-v3#30 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18 · github-actions[bot] · 2026-11-25T23:00:35Z

| 👮 **Wachiman** | Back to the recording page floats the card again |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The asked-once guard is a ref, so it resets when the page remounts. The page builds the request from location.state.fromRecording (library-detail-page.tsx:101) and location.key (:144), and both survive in the history entry. So after a chip goes to Prepare, pressing Back remounts the page with the same key, and the card floats over every app again even though the user already answered it. The in-app card also came back on Back, but it stayed inside the page. One fix: keep the asked keys at module level instead of in a ref.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-25T23:00:35Z

| 👮 **Wachiman** | recording-ready:show accepts any sender |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The three card channels check isOwnSender, but the show handler does not. Any window that loads the shared preload (the card itself, the toast, the overlay) can invoke it and float a card for any assetId. The payload is validated, so the impact is small. Checking that the sender is the main window's webContents would match the other channels.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:145 · github-actions[bot] · 2026-11-25T23:00:35Z

| 👮 **Wachiman** | show() answers true before the card can paint |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

show() returns true as soon as the window exists, and present() waits for card-ready. If the renderer never loads (a failed loadFile, a crash), the page never shows its in-app card and the user sees nothing. The PR body states this limit. A timeout that falls back when card-ready never arrives would close the gap.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:47 · github-actions[bot] · 2026-11-25T23:00:35Z

| 👮 **Wachiman** | Docstring says the card goes away when the user leaves the page |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The floating card stays up after the main window leaves the page (it closes only on an action, the close button or Escape), so 'or leaves the page' is true only of the in-app fallback. Line 47 is also much longer than its neighbours.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-25T23:00:35Z

| 👮 **Wachiman** | Going Back to the recording page makes the floating card pop up again on the desktop |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The page keeps "once per arrival" in `useFloatingReadyCard` with a ref keyed by `location.key` (`use-floating-ready-card.ts:18-24`). A ref does not survive an unmount. Here is the sequence. After a take, `app-root.tsx:75` pushes `/library/:id` with `{ fromRecording: true }`, and the card floats. The user presses a chip in the floating window, and `useRecordingReadyHandOffs` navigates the main window to `/prepare/...`. The user then presses Back. The page remounts under the same history entry, so `location.state.fromRecording` is still true and `cardDismissedFor` is back to null (lines 129-134). `asked.current` is null again, so once the probe settles the page calls `showRecordingReady` again. Main does not dedupe (`recording-ready-window.ts:104-106,134-143`), so the always-on-top window reappears on the desktop for a recording the user already acted on. The same thing happens after ✕ on the floating card, followed by any trip away from the page and back. Before this change, the same reset only re-showed an in-page card. Now it opens a desktop window over other apps. The hook's own doc says "a revisit is a new one", but a Back to the same entry has the same key, so a revisit is not the only case that asks again. A possible fix is to record that the card was asked for outside the component, for example a module-level set of asked keys, or `navigate(location.pathname, { replace: true, state: { ...state, readyShown: true } })` once the ask is sent.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-25T23:00:35Z

| 👮 **Wachiman** | No card at all while the probe never settles |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The floating card is now held back until `probeState.status` is "ready" or "error". The in-app fallback sits behind the same ask, because `showInAppCard` needs `floatingCard.inApp`. Before this change, the in-app card showed right away and filled in its numbers later. `useSourceProbe` has no rejection handler or timeout (`use-prepare-copy.ts:51-59`), and `probeSource` calls `openRecordingInput` outside its `try` (`probe-source.ts:29-30`). If that throws, or the read hangs, the status stays "loading" and the user sees neither card. If that case is possible, consider asking with `dimensions: null` after a short timeout.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.module.css:2 · github-actions[bot] · 2026-11-25T23:00:35Z

| 👮 **Wachiman** | The header says the window is "452 DIP wide", but this rule only sets \`width: fit-content\` |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The 16 px inset comes from `main.css:85-89` (body padding), not from this module. The 452/420 figures depend on constants in `recording-ready-window.ts` (part 1). Make sure they still match, or point to the constant instead of repeating the number.

<!-- wachi:finding -->
