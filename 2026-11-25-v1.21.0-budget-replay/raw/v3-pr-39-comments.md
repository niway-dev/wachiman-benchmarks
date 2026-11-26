# kaipu-bench-wachi-v3#39 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-25T23:56:10Z

| 👮 **Wachiman** | Dragging a copy out doesn't mark it as seen, unlike the ready card's drag |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The ready card's Drag (`export-status-cards.tsx:234-235`) calls `markCopySeen(recording.assetId)` before `startFileDrag`. The contract in `ready-copies.ts:9-10` says a copy stays unseen until the user opens it or acts on it, and it names "drag it out". The new Drag handle only calls `window.electronAPI.startFileDrag(copy.id!, copy.title)`. A user who drags a fresh copy into Slack from this panel still gets the Library's "1 copy ready" chip and outline for it. Fix: call `markCopySeen(copy.assetId)` right before `startFileDrag`, and assert it in the drag test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T23:56:10Z

| 👮 **Wachiman** | The "Open in Export" test only checks one side of its "only where" claim |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test's name says the button shows only where there is an export screen to open. It renders with `onOpenExport` set and clicks the button, but never renders without it to check that `queryByRole('button', { name: 'Open in Export →' })` is null. The page passes `undefined` for anything that isn't preparable (`library-detail-page.tsx:513`), so that is the branch to cover.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-25T23:56:10Z

| 👮 **Wachiman** | The test replaces the global \`window.electronAPI.startFileDrag\` and never restores it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`window.electronAPI.startFileDrag = startFileDrag` swaps the shared global mock and leaves the swap in place. Any later test in the same environment that relies on the original stub sees this `vi.fn()` instead. `vi.spyOn(window.electronAPI, 'startFileDrag')` with `restoreAllMocks`, or restoring it in `afterEach`, keeps the test isolated.

<!-- wachi:finding -->
