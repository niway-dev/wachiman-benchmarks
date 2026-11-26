# kaipu-bench-wachi-v3#72 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T01:44:27Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Drag handle skips markCopySeen, which the other copy-drag call site runs (confidence medium)**

The other drag of a finished copy, the ready card's Drag (`features/status-cards/export-status-cards.tsx:231-235`), calls `markCopySeen(recording.assetId)` before `startFileDrag`. Its doc says it runs when "the user opened the copy or acted on it" (`features/video-editor/export/ready-copies.ts:54-58`). The new Drag here calls only `startFileDrag`. A copy that finishes in the background and is then dragged out from "Copies from this original" stays in the ready-copies store, so the Library rail badge keeps counting it until the user opens the copy's page or the Library. One fix is to call `markCopySeen(copy.assetId)` before `startFileDrag`, the same as the sibling does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T01:44:27Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: A failed probe leaves every card's size at "…" for good (confidence medium)**

`useSourceProbe` returns `{ status: "error", probe: null }` when the file can't be read or the probe isn't usable (`features/prepare/use-prepare-copy.ts:51-58`). The page passes on only `.probe` (`pages/library-detail/library-detail-page.tsx:142`), so this panel can't tell "still reading" from "couldn't read". In both cases `estimate()` returns null for every card except the archive card (line 43), and the size slot shows `…` permanently. The heavy-to-send text on the same page handles a missing estimate with its own wording (`heavyBannerBodyNoEstimate`, `library-detail-page.tsx:582-583`). You could pass the probe status as well, and either leave the size slot empty or show a short "no estimate" line once the status is `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T01:44:27Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never checks the absent case (confidence high)**

The test's name says the button appears only when there is an export screen to open, but it only renders with `onOpenExport` set and clicks the button. No case renders without `onOpenExport` and asserts that `queryByRole("button", { name: "Open in Export →" })` is null. That is the branch the page relies on for screenshots and GIFs (`onOpenExport={preparable ? … : undefined}`, `library-detail-page.tsx:513`). Adding that assertion, for example to the "no local file" case, would test what the name promises.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:492 · github-actions[bot] · 2026-11-26T01:44:27Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: No page test for a master whose only copy is still exporting (confidence high)**

`hasCopies` is also true when a background export of this master is running but no copy has landed yet (`exports.length > 0 || running !== null`, library-detail-page.tsx:189). In that state the page hides "Where is it going?", brings back "Export a copy" and shows the copies panel with only the "Exporting · N%" row. Every page test here leaves `useExportRunner` idle, so they only reach the copies state through a finished copy in the list (lines 487–495). A test that puts the runner in `exporting` for `asset-b`, with no exports, would pin this hand-off. It is the state a user lands in right after picking a destination.

<!-- wachi:finding -->
