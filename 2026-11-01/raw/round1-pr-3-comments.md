=== COMMENT 4437259107 apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100
👮 **Wachiman** · 🟡🧪 **Consider · tests: Drag test replaces the shared electronAPI mock and never restores it**

`window.electronAPI.startFileDrag = startFileDrag` overwrites the mock that `test/setup.ts:109` creates once per file. Nothing puts it back, so every later test in this file runs against this `vi.fn()`. The existing drag test in `export-status-cards.test.tsx:143-152` uses `vi.spyOn(window.electronAPI, "startFileDrag")` followed by `mockRestore()`. Using the same pattern here keeps the tests independent of each other.

<!-- wachi:finding -->

=== COMMENT 4437259109 apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140
👮 **Wachiman** · 🟡🧪 **Consider · tests: "Open in Export" test checks only that the button appears, not that it is hidden**

The test name says the button "shows only where there is an export screen to open", but the test only renders the panel with `onOpenExport` and clicks the button. It should also render without `onOpenExport` and assert that `queryByRole("button", { name: "Open in Export →" })` is null. That case covers a page with no preparable recording, where `library-detail-page.tsx:513` passes `undefined`.

<!-- wachi:finding -->

