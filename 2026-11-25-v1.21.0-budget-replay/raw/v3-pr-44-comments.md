# kaipu-bench-wachi-v3#44 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-25T23:56:50Z

| 👮 **Wachiman** | A failed probe leaves the destination cards on "…" for good |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The page keeps only `useSourceProbe(...).probe` and throws away `status`. When the file can't be read, `useSourceProbe` sets `{ status: "error", probe: null }` (use-prepare-copy.ts:55-57). `DestinationsPanel` then renders `size ?? "…"` (destinations-panel.tsx:91) on every card except Archive, and that is the same ellipsis it shows while the file is still loading. Nothing tells the user the estimate will never come. The same applies when `probeSource` rejects: the `.then` has no catch, so the state stays at "loading". Pass the status down, or a `probeFailed` flag, and show no size or an "unknown" label on error instead of the loading glyph.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-25T23:56:50Z

| 👮 **Wachiman** | Dragging a copy from the panel doesn't mark it seen the way the ready card does |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The other `startFileDrag` call for a finished copy, in export-status-cards.tsx:231-235, calls `markCopySeen(recording.assetId)` before it starts the drag, and also before Reveal (line 221). This new Drag handle hands over the same file but skips that step. A user who drags the copy from "Copies from this original" will still see it as unseen in the places `ready-copies` drives. Call `markCopySeen(copy.assetId)` here too, unless the panel is meant not to count as seeing the copy.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T23:56:50Z

| 👮 **Wachiman** | "shows only where there is an export screen" never checks the case where it's hidden |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test name says the button shows *only* when `onOpenExport` is given, but it only renders with the callback and clicks it. Add a render without `onOpenExport` that asserts `queryByRole("button", { name: "Open in Export →" })` is null. That's the copy-page path where `preparable` is null (library-detail-page.tsx:513).

<!-- wachi:finding -->
