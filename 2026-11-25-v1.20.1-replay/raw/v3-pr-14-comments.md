# kaipu-bench-wachi-v3#14 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171 · github-actions[bot] · 2026-11-25T21:54:20Z

| 👮 **Wachiman** | Drag skips the markCopySeen step the ready card's drag takes |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The ready card's drag handler (`export-status-cards.tsx:231-235`) calls `markCopySeen(recording.assetId)` before `startFileDrag`. The new Drag handle here only calls `startFileDrag`. If a copy is still "unseen" and the user drags it from this panel, does it stay unseen, so the ready card or a "new" mark keeps nagging after it has been used? If it should count as seen, call the same helper here.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T21:54:20Z

| 👮 **Wachiman** | "shows only where…" test never checks the case where the button is absent |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test name promises that "Open in Export →" appears *only* when there is an export screen to open. The body only renders with `onOpenExport` and clicks the button. Add an assertion that the button is missing when `onOpenExport` is omitted (`renderPanel([copy({})])` → `queryByRole("button", { name: "Open in Export →" })` is null). The page relies on that case for non-preparable items (`library-detail-page.tsx:513`).

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-25T21:54:20Z

| 👮 **Wachiman** | Test overwrites window.electronAPI.startFileDrag and never restores it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`window.electronAPI.startFileDrag = startFileDrag` replaces the global mock for every test that runs after this one in the file (and for others, if the setup object is shared). Use `vi.spyOn(window.electronAPI, "startFileDrag")` with `restoreAllMocks`, or restore the original in a `finally`/`afterEach`.

<!-- wachi:finding -->
