# kaipu-bench-wachi-v3#105 [replay r3] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/index.ts:897 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | The ready card is not dismissed before a screenshot or the next take; only content protection keeps it out |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The capture toast is hidden before every screenshot by `captureWindowHooks.dismissToast` (`main/index.ts:670`, `screenshots/capture-window-hooks.ts:55-56`). That call carries the comment "the last quiet capture's toast is always on top and would land in this shot", and it runs even though the toast also calls `setContentProtection(true)`. The new window gets no equivalent. It has no timer, it is `focusable`, and nothing hides it when a screenshot or `recordingStart` begins. Only `setContentProtection(true)` (`recording-ready-window.ts:208`) keeps it out of captures.

The repo already records that content protection is not enough everywhere. `area-geometry.ts:81-85` says Windows builds before 10 2004 paint a content-protected window black in captures instead of omitting it. There, a card left up from the previous take lands as a black 452-wide rectangle in the next recording or screenshot. The card stays until the user acts, so this is likely rather than a corner case. The PR's own test step 9 expects the card never to appear in the result, and nothing but content protection enforces that.

Fix: wire `recordingReady.close()` into the screenshot hooks next to `dismissToast`. Also call it when a recording starts, probably next to `bar.reset()` in the `recordingStart` handler. Closing the card on a new take also avoids a stale card for a previous asset sitting over the new take's controls.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | \`recording-ready:show\` does not check who sent it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The `recordingReadyCardReady`, `recordingReadyResize` and `recordingReadyAction` listeners check `isOwnSender`. The `recordingReadyShow` handler does not, and the payload parser (`recording-ready.ts:64`) does not check that the asset exists. The preload exposes `showRecordingReady` to every window that loads it (capture overlay, toast, bar, panel). Any of them can therefore raise an always-on-top card on top of the user's screen with arbitrary duration and size text. Pressing a chip, Edit first or Open then sends the main window to a route for that arbitrary `assetId`. The card is app-local, so the impact is small. Still, `micLevelsReport` in `recording-hub.ts:786` restricts its sender to the main window's webContents. The same check here would keep the new channel from widening the bridge. The handler would need a `getMainWindow` dep, or the sender id passed in.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:47 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | JSDoc line was rewrapped badly |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

Line 47 is far longer than the rest of the block (about 120 characters), so the JSDoc now reads as if it were edited mid-line. Re-flow the paragraph to the surrounding width.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | Back to a fresh recording's page floats the card again |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The 'asked once' guard is a `useRef` inside `useFloatingReadyCard` (use-floating-ready-card.ts:18), so it dies with the component. After a chip, Edit first or Open on the floating card, the main window navigates away. Browser/router Back then remounts `LibraryDetailPage` under the same history entry. `location.key` and `state.fromRecording` are unchanged, so `showCard` is true again. Once the probe settles, `showRecordingReady` is called again and the card re-opens over the desktop, though the user already acted on it. The in-app card did the same, because `cardDismissedFor` is also component state, but a floating always-on-top window is far more intrusive. The doc says 'once per arrival' (floating-ready-window.md:48-51), which is not true across a remount. Consider keeping the asked/acted key outside the component, for example in a module-level set keyed by `location.key`, or clearing `fromRecording` from the history state once the card has been shown. If the re-pop is acceptable, say so in the doc.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.test.tsx:62 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | Height reporting to main (\`api.resize\`) is not covered |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`RecordingReadyCard` reports its height through `api.resize` (recording-ready-card.tsx:41-53). That is how main fits the transparent window to the card, and a wrong height clips the card or leaves a dead transparent area. No test asserts it. The `resize: vi.fn()` stub is never checked. jsdom reports a height of 0, so `report()` never calls it. Stub `getBoundingClientRect` on the frame and assert that `api.resize` is called with the height after a payload lands, and again when the observer fires.

<!-- wachi:finding -->
