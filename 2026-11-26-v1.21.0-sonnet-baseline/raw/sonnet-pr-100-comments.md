# kaipu-bench-wachi-v3#100 [replay r2] feat(desktop): float "Your video is ready" outside the app window - bot inline comments

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:134 · github-actions[bot] · 2026-11-26T17:35:27Z

| 👮 **Wachiman** | show() answers true before the card can paint, so a card window that never loads loses the prompt with no in-app fallback |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`show()` returns true as soon as `ensureWindow()` has created the `BrowserWindow`. Nothing is painted until the card renderer sends `recording-ready:card-ready` (line 108-112, `present()` at 219-226). `load` (line 258-269) discards the `loadURL`/`loadFile` promise with `void`, so a failed load or a renderer crash is neither logged nor handled. In that case the page's `useFloatingReadyCard` has already received `true`, so it never sets `inApp`, and the user sees no "Your video is ready" card at all. The same applies if the window is created but never becomes ready. The recording itself is saved, so only the prompt is lost. The toast this is modelled on has the same shape, but its content is a transient notice, not a question. Consider `.catch` on the load promise that logs and calls something that resets `rendererReady`/`window` so the next `show()` recreates it, and optionally a ready timeout that makes `show()` resolve false.

<!-- wachi:finding -->

## apps/kaipu-record/src/main/recording/recording-ready-window.ts:104 · github-actions[bot] · 2026-11-26T17:35:27Z

| 👮 **Wachiman** | \`recording-ready:show\` does not check who is asking, unlike the card's own channels |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🔐 security |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The card channels (ready, resize, action) all go through `isOwnSender`. The `invoke` handler for `recordingReadyShow` validates the payload shape but not the sender. Every window loads the same preload, so the capture panel, control bar, overlay and toast windows can all call `window.electronAPI.showRecordingReady`. The `assetId` is any non-empty string, and a later "Open" or chip press hands it back to the main window to navigate. Other main-side handlers that act for the main window only already check the sender, for example `micLevelsReport` in `recording-hub.ts` (`e.sender.id !== getMainWindow()?.webContents.id`). Consider making the same check here; the handler has the `event` it needs but ignores it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:27 · github-actions[bot] · 2026-11-26T17:35:27Z

| 👮 **Wachiman** | Bare \`X satisfies T;\` statement is an expression statement oxlint may flag |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

`RECORDING_READY_DESTINATIONS satisfies ReadonlyArray<DestinationId>;` has no runtime effect and exists only for the type check. The repo enables `no-unused-expressions` (warn) in `.oxlintrc.json`, and every other `satisfies` in `apps/kaipu-record/src` is attached to a declaration. It also adds a value import of the constant that nothing else in this file uses at runtime. A type-level pin would avoid both, for example `type _Pinned = RecordingReadyDestination extends DestinationId ? true : never`, or a `const` typed with `satisfies`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141 · github-actions[bot] · 2026-11-26T17:35:27Z

| 👮 **Wachiman** | The floating card comes back when the page remounts under the same history entry |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useFloatingReadyCard` keeps its "asked once" guard in a ref, so it lives only as long as the component. `fromRecording` is read from `location.state`, which stays on the history entry. Take a chip or Edit first from the floating card: main navigates the main window to Prepare or the editor, and the detail page unmounts. Router Back then remounts the page on the same entry, with the same `location.key` and `fromRecording` still true. The ref is new, so main is asked again and the card floats a second time over whatever the user was doing. The page cannot know the user already acted in the other window. The doc and the hook comment both say "once per arrival", which is not true across a remount. The in-app card had the same reappearance, but it only showed inside the app. A floating, always-on-top card is more intrusive. One option is to clear `fromRecording` from the entry (`navigate(location.pathname, { replace: true, state: null })`) once the card has been asked for. Another is to keep the asked keys in module scope.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:140 · github-actions[bot] · 2026-11-26T17:35:27Z

| 👮 **Wachiman** | The card now waits on the probe, which has no timeout |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

Before this change the in-app card showed at once, with the numbers filled in later. Now `showCard && probeSettled` gates both the floating ask and the fallback. `probeSource` never throws (`probe-source.ts:42`), but it has no timeout. If mediabunny's `getPrimaryVideoTrack` or `computePacketStats` stalls on a slow or odd file, the status stays `loading` and the user gets no card at all, floating or in-app, with nothing visible. A fallback timer (settle as `error` after a few seconds) would keep the card from being lost.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:768 · github-actions[bot] · 2026-11-26T17:35:27Z

| 👮 **Wachiman** | New "no floating card" test duplicates the two tests below it and misses the probe-error path |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test at 768 mixes two cases (Settings off, opened from the Library) in one body and with one shared spy. The tests at 834 and 844 already cover those cases for the in-app card, so this one is redundant; if it fails, the name does not say which case broke. Meanwhile no test covers the path where the probe fails. That path asks for the card with `dimensions: null` and the sidecar duration, and the in-app fallback would then show without dimensions. Consider splitting this test, or folding the `showRecordingReady` not-called assertion into the existing tests, and adding a probe-error case.

<!-- wachi:finding -->
