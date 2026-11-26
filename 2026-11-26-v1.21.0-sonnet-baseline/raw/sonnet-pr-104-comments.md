# kaipu-bench-wachi-v3#104 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | Drag test overwrites the global electronAPI stub and never restores it |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`window.electronAPI.startFileDrag = startFileDrag` replaces the shared stub from `src/renderer/src/test/setup.ts:153` for the rest of the file. The other test that checks this call, `export-status-cards.test.tsx:143-152`, uses `vi.spyOn(...)` and `mockRestore()`. Use the same pattern here, or restore the original in `afterEach`. Otherwise a later test in this file sees the leaked mock.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | "shows only where there is an export screen" never checks the absent case |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "Open in Export → shows only where there is an export screen to open", but it only clicks the button with `onOpenExport` set. Nothing asserts that the button is missing when `onOpenExport` is omitted, and omitting it is what the page does for a non-preparable video (`library-detail-page.tsx:513`). Add a `queryByRole(...)` null assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | Size placeholder "…" never resolves if the file cannot be probed |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`probe` comes from `useSourceProbe(...).probe`, which is `null` for both "loading" and "error" (`use-prepare-copy.ts:42-67`). The prop doc says the cards show no estimate "until it is" read. When the probe errors, every non-archive card shows "…" indefinitely, as if still loading. The cards still work, so nothing breaks, but the placeholder is misleading. Consider hiding the size span when the probe has failed, or passing the probe status down.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:757 · github-actions[bot] · 2026-11-26T17:35:42Z

| 👮 **Wachiman** | Heavy master with copies keeps the banner, but no test covers it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The doc (prepare-screen.md:111) and the page (`heavy && !showDestinations` renders `HeavyToSendBanner`) say a heavy master that already has copies shows the "Prepare a light copy →" banner. The heavy-to-send tests only cover a heavy master with no copies (the hint inside the panel) and a heavy copy. A heavy master with one copy is the branch where the hint could be lost, since `showDestinations` is false there and the panel's `note` is not rendered. Add a case with a heavy master and an export child that expects the banner.

<!-- wachi:finding -->
