# kaipu-bench-wachi-v3#94 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T17:30:29Z

| 👮 **Wachiman** | Drag from the copies panel doesn't mark the copy as seen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The other call site of `startFileDrag(recording.id, recording.title)`, the ready card, calls `markCopySeen(recording.assetId)` first (`features/status-cards/export-status-cards.tsx:234`). `ready-copies.ts:8-10` defines a copy as unseen "until the user opens it ... or acts on its ready card (Show in Finder, drag it out)". This new drag handle skips that call. A copy the user drags out of this panel therefore stays in the unseen set, so the Library page keeps its "copy ready" chip and outline. Opening the master's page does not clear it either: the sidebar only marks the asset in the URL (`shell/sidebar.tsx:95`). Calling `markCopySeen(copy.assetId)` before the drag would match the sibling.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T17:30:29Z

| 👮 **Wachiman** | Size shows "…" forever when the file can't be read |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`size` is null whenever `probe` is null, and the panel renders "…". The page passes `useSourceProbe(...).probe`, which is also null in the `error` state (`use-prepare-copy.ts:55-58`), for example when `probeSource` returns null. After a failed read every non-archive card shows a loading-looking "…" permanently, with nothing to tell the user it failed. Consider rendering nothing, or a dash, once the probe has failed. That would mean passing the probe status into the panel.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T17:30:29Z

| 👮 **Wachiman** | "shows only where there is an export screen" test never checks the absent case |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test name promises the "Open in Export →" button appears only when `onOpenExport` is given. The body only clicks the button when the callback is given. Nothing asserts that the button is absent when the prop is omitted, and that is the branch the page relies on for non-preparable videos (`library-detail-page.tsx:513`). Add a `renderPanel([copy({})])` assertion that `queryByRole("button", { name: "Open in Export →" })` is null.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T17:30:30Z

| 👮 **Wachiman** | Test overwrites the global \`window.electronAPI.startFileDrag\` and never restores it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`window.electronAPI.startFileDrag = startFileDrag` replaces a property of the shared stub from `test/setup.ts:109`. The stub is not reset afterwards, so the mock leaks into later tests in the file and into any code that reads the same stub. Use `vi.spyOn(window.electronAPI, "startFileDrag")` with a restore in `afterEach`, or restore the original at the end of the test.

<!-- wachi:finding -->
