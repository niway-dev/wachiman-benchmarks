# kaipu-bench-wachi-v3#29 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-25T22:59:42Z

| 👮 **Wachiman** | Test replaces window.electronAPI.startFileDrag and never restores it |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This test assigns a `vi.fn()` straight onto the shared `window.electronAPI` mock from `test/setup.ts:153` and never puts the original back. If the mock object outlives one test, every later test in the run sees the spy. The sibling test at `export-status-cards.test.tsx:143-152` uses `vi.spyOn(window.electronAPI, "startFileDrag")` and then `mockRestore()`. Doing the same here keeps the tests isolated.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T22:59:42Z

| 👮 **Wachiman** | "Open in Export → shows only where…" never checks that the button is absent |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test's name says the button shows *only* when there is an export screen to open. It only renders with `onOpenExport` and clicks the button. It never renders without the prop and checks that `queryByRole("button", { name: "Open in Export →" })` is null. The page relies on that case at `library-detail-page.tsx:513`, which passes `undefined` when the recording is not preparable.

<!-- wachi:finding -->
