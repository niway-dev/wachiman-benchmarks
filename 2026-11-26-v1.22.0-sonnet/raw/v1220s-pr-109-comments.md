# kaipu-bench-wachi-v3#109 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T20:03:55Z

| 👮 **Wachiman** | Dragging a copy out of this panel does not mark it seen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The ready card's Drag handle calls `markCopySeen(recording.assetId)` before `startFileDrag` (`export-status-cards.tsx:232-235`). `ready-copies.ts:9-10` says a copy stays unseen until the user opens it or acts on its ready card (Show in Finder, drag it out). This panel's Drag handle skips that step. A copy finished in the background and then dragged out from here stays unseen, so the Library page keeps outlining it and counting it in the "copy ready" chip. The sidebar only clears it when the user opens the copy's own page (`shell/sidebar.tsx:95`). Calling `markCopySeen(copy.assetId)` in `onDragStart` would match the card.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T20:03:55Z

| 👮 **Wachiman** | Unreadable file leaves every card size as "…" forever |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`estimate()` returns null whenever `probe` is null, and the card then renders `…`. `useSourceProbe` also returns a null probe in the `error` state (`use-prepare-copy.ts:55-58`). When the file can't be read, six cards show `…` indefinitely, which reads as still loading. The old strip showed no sizes, so this is a new state. Either hide the size span once the probe has failed, or pass the status down so the card can say so.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:98 · github-actions[bot] · 2026-11-26T20:03:55Z

| 👮 **Wachiman** | Drag test overwrites the global \`window.electronAPI.startFileDrag\` and never restores it |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test assigns `window.electronAPI.startFileDrag = startFileDrag` directly, so the mock leaks into later tests in the file. The sibling test uses `vi.spyOn(window.electronAPI, "startFileDrag")` and `mockRestore()` (`export-status-cards.test.tsx:143,152`). Use the same pattern.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T20:03:55Z

| 👮 **Wachiman** | "Open in Export →" test name promises an absence check that is not there |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The title says the button "shows only where there is an export screen to open", but the test only clicks the button with `onOpenExport` set. Nothing renders the panel without `onOpenExport` and asserts the button is absent. That is the half of the contract that matters, since the page passes `undefined` when `preparable` is null (`library-detail-page.tsx:513`). Add that assertion.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104 · github-actions[bot] · 2026-11-26T20:03:55Z

| 👮 **Wachiman** | Copy picture size is recomputed from the preset and the current probe, not read from the copy |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

`factsOf` shows `resolveExportTarget(preset, probe, probe.durationSec)` for each destination copy. The numbers come from the master's probe and the current preset rules, not from the copy's own file. If the preset tables change between releases, or a copy was made under different rules, the row shows a size the file doesn't have, with no error. Is that acceptable, or should the copy's real dimensions be stored or read? GIF rows already use the stored `copy.gif` size.

<!-- wachi:finding -->
