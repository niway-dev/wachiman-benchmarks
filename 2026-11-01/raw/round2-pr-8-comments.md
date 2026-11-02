=== COMMENT 4437281136 apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91
👮 **Wachiman** · 🟡🐛 **Consider · bug: An unreadable file leaves the size on every card at "…" for good**

`estimate` returns null whenever `probe` is null, and the card shows `…`. The page passes only `useSourceProbe(...).probe` (library-detail-page.tsx:142). `useSourceProbe` returns `{ status: "error", probe: null }` when `probeSource` fails (use-prepare-copy.ts:55-57), so for a file it can't read, every card except Archive keeps the loading ellipsis forever. Consider passing the probe status, or showing nothing once the status is `error`, so a failure doesn't look like it's still loading.

<!-- wachi:finding -->

=== COMMENT 4437281142 apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100
👮 **Wachiman** · 🟡🧪 **Consider · tests: The test replaces the shared `electronAPI` stub and never puts it back**

`window.electronAPI.startFileDrag = startFileDrag;` overwrites the global stub that test/setup.ts:109 builds once per file, and nothing restores it. Any later test in this file that drags gets this test's mock. The sibling test (export-status-cards.test.tsx:143-152) uses `vi.spyOn(window.electronAPI, "startFileDrag")` and calls `mockRestore()`. Doing the same here keeps the tests isolated.

<!-- wachi:finding -->

=== COMMENT 4437281146 apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140
👮 **Wachiman** · 🟡🧪 **Consider · tests: The "Open in Export" test never checks the case where the button should be missing**

The test is called "Open in Export → shows only where there is an export screen to open", but it only renders with `onOpenExport` and clicks the button. It never renders without the callback to check that the button is absent, which is the "only where" part of its name (master-copies-panel.tsx:122). Add a `queryByRole(..., { name: "Open in Export →" })` → null check on a render without `onOpenExport`.

<!-- wachi:finding -->

