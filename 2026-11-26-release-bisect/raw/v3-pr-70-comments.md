# kaipu-bench-wachi-v3#70 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T01:43:57Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Drag from the copies panel doesn't mark the copy as seen, unlike the ready card's Drag (confidence high)**

The ready card's Drag handle calls `markCopySeen(recording.assetId)` just before `startFileDrag` (`status-cards/export-status-cards.tsx:234-235`). `ready-copies.ts:8-10` says a copy stays UNSEEN until the user opens it or acts on it ("drag it out"). This handle skips that step. After a user drags a freshly finished copy out from here, the Library page still outlines it and still counts it in its "copy ready" chip. Suggested fix: call `markCopySeen(copy.assetId)` before `window.electronAPI.startFileDrag(...)`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T01:43:57Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: An unreadable file leaves every destination card on "…" for good (confidence high)**

The panel only receives `probe`, and `estimate` returns null whenever `probe` is null (line 43), so the card renders `"…"`. `useSourceProbe` returns `{ status: "error", probe: null }` when the read fails or comes back unusable (`use-prepare-copy.ts:51-58`). The page passes only `.probe` (`library-detail-page.tsx:142`), so the cards can't tell a failed read from one still loading. For a file that can't be probed, six of the cards show a loading ellipsis forever. Before this change, the strip showed no numbers at all. Suggested fix: pass the probe status (or an `estimatesFailed` flag) and drop the size line, or show a plain fallback, when the status is `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T01:43:57Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never checks the case without one (confidence high)**

The test only renders with `onOpenExport` and clicks the button. The "only where" half of the name is the case where `onOpenExport` is omitted (`master-copies-panel.tsx:122`, and `library-detail-page.tsx:513` for a non-preparable item), and no test asserts that `Open in Export →` is absent then. Add `renderPanel([copy({})])` and assert `queryByRole("button", { name: "Open in Export →" })` is null.

<!-- wachi:finding -->
