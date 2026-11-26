# kaipu-bench-wachi-v3#62 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171 · github-actions[bot] · 2026-11-26T01:32:25Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Dragging a copy out does not mark it seen, unlike the ready card's Drag (confidence high)**

The existing native-drag call site in `export-status-cards.tsx:231-235` calls `markCopySeen(recording.assetId)` before `startFileDrag`, because dragging the file out counts as acting on the copy (`ready-copies.ts:54-58`). This new Drag handle skips that step. When a user drags a fresh copy out from "Copies from this original", the copy still counts in the Library badge (`sidebar.tsx:92-98`) and is still flagged just-ready on the Library card. The sidebar's own `markCopySeen` only covers the asset whose page is open, which here is the master, not the copy. Suggested fix: call `markCopySeen(copy.assetId)` in `onDragStart`, as the ready card does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T01:32:25Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: If the file read fails, the size estimates show "…" forever (confidence high)**

`useSourceProbe` reports `status: "error"` with `probe: null` when the probe can't be used (`use-prepare-copy.ts:51-58`). The page keeps only `.probe` (`library-detail-page.tsx:142`), so the panel can't tell "still reading" apart from "could not read". Every non-archive card then shows `…` permanently, which looks like an estimate that is still loading. Passing the status through, or showing nothing or a "no estimate" line on error, would avoid this.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T01:32:25Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "Open in Export" test never checks the 'only where there is an export screen' half (confidence high)**

The test name promises the button shows *only* when there is an export screen to open. It only checks that a click calls `onOpenExport` when the prop is passed. No test checks that `Open in Export →` is missing when `onOpenExport` is left out, which is the branch the page relies on for a non-preparable copy (`library-detail-page.tsx:513`). Suggested fix: add a `renderPanel([copy({})])` case that asserts `queryByRole("button", { name: "Open in Export →" })` is null.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:184 · github-actions[bot] · 2026-11-26T01:32:25Z

👮 **Wachiman** · 🟡📝 **Consider · docs: Validation step says to drag the copy's row, but only the Drag button starts the file drag (confidence high)**

The QA script says "Drag the copy's row out of the page into Finder". In `master-copies-panel.tsx:153-175`, the row is a `<Link>` (an anchor) plus a separate `draggable` Drag button. Only the button's `onDragStart` calls `window.electronAPI.startFileDrag`. If you drag the row body, the browser's default anchor drag runs and carries a URL, not the file. Someone following this step would see a failed drop and file it as a bug. Line 109 of the same doc already describes this correctly ("a **Drag** handle"). Suggested wording: "Drag the copy's **Drag** handle into Finder".

<!-- wachi:finding -->
