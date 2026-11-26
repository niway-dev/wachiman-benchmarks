# kaipu-bench-wachi-v3#24 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-25T22:59:09Z

| 👮 **Wachiman** | Drag here skips markCopySeen, unlike the ready card's Drag |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The other place that drags a finished copy, the ready card at `features/status-cards/export-status-cards.tsx:231-235`, calls `markCopySeen(recording.assetId)` before `startFileDrag`, because acting on the copy means there is nothing left to point at (`features/video-editor/export/ready-copies.ts:54-58`). The new Drag handle only calls `startFileDrag(copy.id!, copy.title)`. If a user drags a just-finished copy out of "Copies from this original", it stays in the ready-copies store as unseen, so whatever shows from that store keeps pointing at a copy the user already used. To match the sibling, call `markCopySeen(copy.assetId)` in `onDragStart`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T22:59:09Z

| 👮 **Wachiman** | "shows only where there is an export screen" never checks the case where it's hidden |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This test only renders the panel with `onOpenExport` set, clicks the button and asserts the callback ran. Nothing renders the panel without `onOpenExport` and checks that "Open in Export →" is absent, which is the "only where" part of the test's name. The page relies on that: it passes `undefined` for anything that isn't preparable (`library-detail-page.tsx:513`). Add a second render with no `onOpenExport` and assert `queryByRole("button", { name: "Open in Export →" })` is null.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-25T22:59:09Z

| 👮 **Wachiman** | Test overwrites window.electronAPI.startFileDrag and never restores it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`window.electronAPI.startFileDrag = startFileDrag` assigns to the shared global and doesn't restore it afterwards. Later tests in the same environment that use `startFileDrag` will see this mock. Using `vi.spyOn(window.electronAPI, "startFileDrag")` with `restoreAllMocks`, or restoring the original in `afterEach`, keeps the test self-contained.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:269 · github-actions[bot] · 2026-11-25T22:59:09Z

| 👮 **Wachiman** | No test covers a failed probe: the destination cards would show "…" for good |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The page now reads the file for every local recording. `useSourceProbe` returns `{ status: "error", probe: null }` when the read fails (`use-prepare-copy.ts:55-57`). The page keeps only `.probe` (`library-detail-page.tsx:142`). `DestinationsPanel.estimate` then returns null for every card except Archive (`destinations-panel.tsx:43`) and renders "…" (`destinations-panel.tsx:91`). A failed read therefore looks exactly like one still in progress, and the cards stay on "…" with nothing telling the user why. The new size test (lines 269-290) only covers the success path. Add a case where `probeSource` resolves to an unusable result, and decide what the cards should show in that case.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:184 · github-actions[bot] · 2026-11-25T22:59:09Z

| 👮 **Wachiman** | QA step says to drag the copy's row, but the drag starts from the Drag handle |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The QA script says "Drag the copy's row out of the page into Finder". The section above (line 109) and the test at `library-detail-page.test.tsx:527` describe a separate **Drag** button that sits beside the row's link, and the stylesheet puts it outside `.link` (`master-copies-panel.module.css:62`). The row itself is a link to the copy's page. Write "Drag the copy's Drag handle into Finder" so QA tests the control that actually starts the drag.

<!-- wachi:finding -->
