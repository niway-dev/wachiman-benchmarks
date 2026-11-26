# kaipu-bench-wachi-v3#64 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T01:33:47Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Dragging a copy out from the panel doesn't mark it as seen, unlike the ready card's drag (confidence medium)**

The other drag-out of a finished copy, in `export-status-cards.tsx:233-235`, calls `markCopySeen(recording.assetId)` before `startFileDrag`. `ready-copies.ts:9-10` says a copy stays UNSEEN until the user opens it or acts on it ("drag it out"). The new Drag handle here goes straight to `startFileDrag`. If a copy finishes in the background and the user drags it out from the master's "Copies from this original" panel, the Library still outlines it and counts it in its "copy ready" chip (`unseenCopyIds`). Calling `markCopySeen(copy.assetId)` in this `onDragStart` would match the sibling.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T01:33:47Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: A failed probe leaves every non-archive card on "…" forever (confidence high)**

`useSourceProbe` returns `{ status: "error", probe: null }` when the file can't be read (`use-prepare-copy.ts:55-57`). The page passes only `.probe` (`library-detail-page.tsx:142`), so the panel can't tell "still reading" from "couldn't read". On an error, the five estimate cards show `…` indefinitely, which looks like loading that never finishes. Consider passing the status, or a flag, so the cards can drop the size line, or say there is no estimate, once the probe has failed.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T01:33:47Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The "shows only where…" test never checks the case where the button is absent (confidence high)**

The test name says Open in Export → shows *only* where there is an export screen. The body only covers the case where `onOpenExport` is given and the click fires. No test asserts that the button is missing when `onOpenExport` is omitted, which is the branch `library-detail-page.tsx:513` relies on for non-preparable pages. Add `expect(within(renderPanel([copy({})])).queryByRole("button", { name: "Open in Export →" })).toBeNull()` (with a cleanup between renders), or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T01:33:47Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The test replaces the global `startFileDrag` stub and never restores it (confidence high)**

`window.electronAPI.startFileDrag = startFileDrag` overwrites the shared stub from `test/setup.ts:153`, and the `afterEach` in setup doesn't restore it. Later tests in this file then see the mock. The sibling test (`export-status-cards.test.tsx:143,152`) uses `vi.spyOn(window.electronAPI, "startFileDrag")` and `mockRestore()`. Following that pattern keeps tests from affecting each other.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:785 · github-actions[bot] · 2026-11-26T01:33:47Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: The archive card's accessible name reads "Export a copy for Archive copy" (confidence high)**

`destinationAria` puts each destination's display name into "Export a copy for {destination}". For the archive destination that name is "Archive copy", so screen readers announce "Export a copy for Archive copy" (asserted at `library-detail-page.test.tsx:259`). Spanish has the same problem through `destinationAria` in es.json. You could give the archive card its own label, such as "Export an archive copy", or use a name for it that doesn't repeat "copy".

<!-- wachi:finding -->
