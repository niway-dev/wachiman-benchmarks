# kaipu-bench-wachi-v3#45 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/index.ts:899 · github-actions[bot] · 2026-11-25T23:57:16Z

| 👮 **Wachiman** | Hand-off does not check that the recording still exists |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The capture toast's hand-off (`openSavedScreenshot`, index.ts:683-689) first calls `currentVault().describe(id)` and drops the hand-off when the item is gone. `openInMain` sends `recording-ready:open` with no such check. The floating card has no timer and stays up until an action (recording-ready-window.ts:88-90), so the user has plenty of time to delete the recording from the main window. A chip, Edit first or Open pressed after that still shows the main window and navigates to Prepare, the editor or the detail page for an asset that no longer exists. Two possible fixes: check the asset like the toast does, or close the floating card when its recording is removed.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:18 · github-actions[bot] · 2026-11-25T23:57:16Z

| 👮 **Wachiman** | Back to the recording page floats the card again after the user acted |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The `asked` ref only guards StrictMode's second effect run. It does not survive a remount. Here is the sequence: the user presses a chip on the floating card and lands on Prepare, then presses Back. The detail page remounts under the same history entry, with the same `location.key` and the `fromRecording` state still set (library-detail-page.tsx:130-134). The ref is null again, so the page asks main a second time and the desktop card pops up over whatever the user is doing. The doc line "`key` is its history entry, so a revisit is a new one" says the opposite. The old in-app card also came back on Back, because `cardDismissedFor` is component state. A window floating on the desktop makes that much more intrusive, though. Remembering the asked keys outside the component would fix it, for example in a module-level Set or in history state.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:48 · github-actions[bot] · 2026-11-25T23:57:16Z

| 👮 **Wachiman** | Docstring says the card goes away when the user leaves the page |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment still says the card "stays until the user picks something, closes it or leaves the page". The floating window does not react to navigation. It closes only on an action, ✕ or Escape (recording-ready-window.ts:88-90, 149-155). Leaving the page now ends only the in-app fallback.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-hub.ts:710 · github-actions[bot] · 2026-11-25T23:57:16Z

| 👮 **Wachiman** | A take stopped before the source lookup resolves keeps a stale or null display |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

For a whole-display take with no countdown region, line 666 sets `lastTakeDisplayId` to null. The real display is set only inside the `displayIdForSource` callback (line 711), and that callback returns early when the take is no longer active. If the user stops a very short take before the lookup resolves, the ready card falls back to the display under the pointer (recording-ready-window.ts:237-244) instead of the recorded one. The bar has to skip a stopped take, but the display id could still be recorded before that early return.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-25T23:57:16Z

| 👮 **Wachiman** | Floating card is asked for again when the page remounts under the same history entry |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useFloatingReadyCard` remembers in a ref (`use-floating-ready-card.ts:18`) that it already asked for this `location.key`, and that ref goes away when the component unmounts. When the user leaves the page and comes back to the same entry with router Back, `location.key` and `state.fromRecording` are the same as before, so `showCard` is true again. The new mount then calls `showRecordingReady` once more, and the desktop window pops up again even if the user already pressed ✕ or used a chip in the floating card (those never set `cardDismissedFor`). The in-app card already reappeared this way, since `cardDismissedFor` is plain state. But that card was on the page the user was looking at. The new one is a window shown over whatever app the user is in. Possible fix: keep the set of keys already asked for at module level, or in `sessionStorage`, instead of a per-mount ref. I found no `navigate(-1)` in the renderer, so this needs an OS or router Back to happen.

<!-- wachi:finding -->
