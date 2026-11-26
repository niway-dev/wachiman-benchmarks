# kaipu-bench-wachi-v3#80 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T06:27:22Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: Drag handle skips markCopySeen, so the dragged copy stays "unseen" in the Library (confidence high)**

The only other drag-out of a finished copy, the ready card (`features/status-cards/export-status-cards.tsx:234-235`), calls `markCopySeen(recording.assetId)` right before `window.electronAPI.startFileDrag(...)`. The ready-copies store spells out that contract: a copy stays UNSEEN until the user opens it or acts on it, and "drag it out" counts (`features/video-editor/export/ready-copies.ts:9-10`). The new Drag handle calls `startFileDrag` only. So after a background export finishes and the user drags the copy out from "Copies from this original", the Library page still outlines that copy and still counts it in its "copy ready" chip (`unseenCopyIds`, `ready-copies.ts:78`). Fix: call `markCopySeen(copy.assetId)` before `startFileDrag`, the way the ready card does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T06:27:22Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: If the file read fails, the destination cards show "…" forever (confidence high)**

`useSourceProbe` returns `{status: "error", probe: null}` when the read fails or comes back unusable (`features/prepare/use-prepare-copy.ts:55-57`). The page keeps only `.probe` (`library-detail-page.tsx:142`), so the panel cannot tell "still loading" from "failed". Every card except Archive then shows the loading `…` for good, and the user never learns there will be no estimate. The page now reads the file for every local recording, so this state can show up more often than before. Consider passing the status down and leaving the size out (or showing a plain fallback) when the read fails.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T06:27:22Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never checks the case without one (confidence high)**

The test name says the button shows *only* when there is an export screen to open, but it only renders with `onOpenExport` set and clicks the button. Nothing checks that the button is missing when `onOpenExport` is omitted, which is what happens on the page when `preparable` is null (`library-detail-page.tsx:513`). Add a render without `onOpenExport` that asserts `queryByRole("button", { name: "Open in Export →" })` is null.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:236 · github-actions[bot] · 2026-11-26T06:27:22Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: No page test for a master whose first copy is still exporting (confidence high)**

The page shows the copies panel in place of "Where is it going?" when a copy is exporting, even if no finished copy exists yet (`hasCopies = exports.length > 0 || running !== null`, library-detail-page.tsx:189-191). The tests here only cover two cases: no copies at all (destinations panel), and a finished copy (the lineage test at :484-495). None of them mocks `useExportRunner` mid-export to check three things: the panel goes away, "Export a copy" shows, and the running row appears. The old empty-state assertion ("No copies yet…") was also removed, and no test replaced it with a check that a master with no copies shows no "Copies from this original" region.

<!-- wachi:finding -->
