# kaipu-bench-wachi-v3#90 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T17:03:41Z

| 👮 **Wachiman** | Drag skips markCopySeen, unlike the Ready card's Drag |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Ready card's Drag (`features/status-cards/export-status-cards.tsx:234-235`) calls `markCopySeen(recording.assetId)` before `startFileDrag`, because dragging a copy out counts as acting on it (`ready-copies.ts:54-58`). This new Drag handle only calls `startFileDrag`. If the user drags a freshly finished copy into another app from the original's page, the copy stays in the ready-copies snapshot, and the sidebar's Library badge (`shell/sidebar.tsx:98`) keeps counting it. Fix: call `markCopySeen(copy.assetId)` before `window.electronAPI.startFileDrag(...)`, the same as the sibling does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-26T17:03:41Z

| 👮 **Wachiman** | When the probe fails, the destination cards show "…" forever |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The page keeps only `.probe` from `useSourceProbe` and drops `status`. When the file can't be read, the hook returns `{status: "error", probe: null}` (`use-prepare-copy.ts:55-57`). `DestinationsPanel` then renders `size ?? "…"` (`destinations-panel.tsx:91`) on every card except Archive, so a failed read looks the same as one still loading. Now that the probe runs for every local recording, this state is easier to hit. One option is to pass the status through and leave out the size, or show a 'no estimate' text, when it is `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T17:03:41Z

| 👮 **Wachiman** | "Open in Export → shows only where…" never tests the case where it is hidden |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test name promises the button shows *only* when there is an export screen to open. The test only renders the panel with `onOpenExport` set and clicks the button. It never renders the panel without the prop to check that the button is absent, which is the branch at `master-copies-panel.tsx:122`. A second render with no `onOpenExport` and a `queryByRole(...)` that expects null would cover it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T17:03:41Z

| 👮 **Wachiman** | Test replaces window.electronAPI.startFileDrag and never restores it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`window.electronAPI.startFileDrag = startFileDrag` assigns a mock to the shared global, and nothing puts the original back. Later tests in this file, or files that share the environment, inherit the mock. `vi.spyOn(window.electronAPI, "startFileDrag")` with `restoreAllMocks`, or restoring it in an `afterEach`, keeps the test isolated.

<!-- wachi:finding -->
