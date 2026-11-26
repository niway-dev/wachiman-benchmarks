# kaipu-bench-wachi-v3#68 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171 · github-actions[bot] · 2026-11-26T01:43:54Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Dragging a copy out doesn't clear its "copy ready" mark, unlike the ready card's drag (confidence high)**

The ready card's Drag handle calls `markCopySeen(recording.assetId)` before `startFileDrag` (`export-status-cards.tsx:231-235`). `ready-copies.ts:9-10` says a copy stays unseen until the user opens it or acts on it, and dragging it out counts as acting on it. The new Drag handle skips that call. The sidebar only marks the asset on the current detail route as seen (`sidebar.tsx:95`), and here that asset is the original. So after you drag a fresh copy out from "Copies from this original", the Library page keeps outlining it and still counts it in "1 copy ready". Suggested fix: call `markCopySeen(copy.assetId)` in `onDragStart`, the same way the sibling does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T01:43:54Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Cards show "…" forever when the file can't be read (confidence medium)**

`useSourceProbe` returns `{status: "error", probe: null}` when the probe is unusable (`use-prepare-copy.ts:55-57`). The page passes only `.probe` (`library-detail-page.tsx:142`), so the panel can't tell "still reading" from "failed". Every card except Archive then shows `…` with no end, which looks like loading that never finishes. The heavy-to-send text handles the same null with its own "no estimate" wording (`library-detail-page.tsx:582-583`). Consider passing the probe status, or dropping the size line on error.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T01:43:54Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never checks the case without one (confidence high)**

The test only renders with `onOpenExport` set and clicks the button. It never renders without the prop to check that "Open in Export →" is missing, so the "only where" half of its name is untested. The page relies on that half when `preparable` is null (`library-detail-page.tsx:513`).

<!-- wachi:finding -->
