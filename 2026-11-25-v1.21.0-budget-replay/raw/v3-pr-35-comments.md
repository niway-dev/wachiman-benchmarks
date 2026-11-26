# kaipu-bench-wachi-v3#35 [replay] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-hub.ts:711 · github-actions[bot] · 2026-11-25T23:53:09Z

| 👮 **Wachiman** | A take stopped before the source lookup resolves never records its display |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The screen-source display is written only inside the `displayIdForSource` callback, and that callback returns early at line 710 once `activity.active` is false. If a whole-display take with no area and no countdown is stopped before the lookup resolves, `lastTakeDisplayId` stays null from line 666. The ready window then opens on the display under the pointer instead of the one that was recorded. One fix: record `displayId` before the early return, while still checking `take === takeCount`. Only the bar/shade work needs the `activity.active` guard.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-25T23:53:09Z

| 👮 **Wachiman** | \`recording-ready:show\` accepts any sender, not only the main window |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The card-side channels check `isOwnSender`. The `recordingReadyShow` handler does not: any window that loads the shared preload (capture toast, overlay, camera bubble, the card itself) can float the card with an arbitrary validated payload. The payload is parsed and the damage is small: a misleading card whose actions hand an arbitrary `assetId` to the main window. Should this check that the sender is the main window's `webContents`, the way the card channels check theirs?

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-25T23:53:09Z

| 👮 **Wachiman** | Back onto the recording page floats the desktop card again |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useFloatingReadyCard` remembers what it asked for only in a ref (`use-floating-ready-card.ts:18`), and the page keeps the dismissal only in `useState` (line 129). Router Back remounts the page under the same history entry, so `location.key` and `state.fromRecording` are unchanged, `showCard` is true again and the ref starts out null. Main is asked a second time and the always-on-top window pops up again, even if the user already used the floating card. Example: chip → Prepare → Back. The floating card's ✕ and its actions never reach the page. The in-app card already reappeared on Back before this change, but a desktop window that comes back is more intrusive. A fix: keep the asked/dismissed key outside the component, for example a module-level Set of `location.key`s, or replace the history state to drop `fromRecording` after asking.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:140 · github-actions[bot] · 2026-11-25T23:53:09Z

| 👮 **Wachiman** | A probe that never settles now hides the card entirely |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The request waits for `probeState.status` to be "ready" or "error". `probeSource` catches its own errors (`probe-source.ts:42-43`), so a failed read does settle. But if reading the file stalls, for example a slow or locked file on the `kaipu-media://` stream, the status stays "loading". The floating window is then never asked for, and the in-app fallback never shows either. Before this change the in-app card rendered at once with the library's numbers. A timeout that sends the payload with `dimensions: null` would keep the card from being lost.

<!-- wachi:finding -->
