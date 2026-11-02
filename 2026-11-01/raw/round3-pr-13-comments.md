=== COMMENT 4437283455 apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140
👮 **Wachiman** · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never checks that the button is missing**

The test's name says the button shows *only* when `onOpenExport` is given. It only renders with the handler and clicks the button. It never renders without the handler to check that "Open in Export →" is absent. The page relies on that case: `library-detail-page.tsx:513` passes `undefined` for a recording that is not preparable. Add a render without `onOpenExport` and a `queryByRole(...)` check that expects `null`.

<!-- wachi:finding -->

=== COMMENT 4437283460 apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100
👮 **Wachiman** · 🟡🧪 **Consider · tests: Drag test replaces the shared electronAPI stub and never restores it**

`window.electronAPI.startFileDrag = startFileDrag` overwrites the stub from `test/setup.ts:109`, and nothing puts the original back. `afterEach` at `setup.ts:99` does not reset `window.electronAPI`. Every later test in this file therefore runs with the mock. `export-status-cards.test.tsx:143-152` handles the same call with `vi.spyOn(window.electronAPI, "startFileDrag")` and `mockRestore()`. Using that pattern here keeps the stub intact between tests.

<!-- wachi:finding -->

=== COMMENT 4437283463 packages/i18n/messages/en.json:785
👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Archive card's accessible name reads "Export a copy for Archive copy"**

`destinationAria` is filled with the destination's display name in `destinations-panel.tsx:81`. For the archive destination that name is "Archive copy", so screen readers announce "Export a copy for Archive copy". The test pins this name at `library-detail-page.test.tsx:259`. The Spanish string has the same problem. One fix is a separate aria string for the archive card, such as "Export an archive copy".

<!-- wachi:finding -->

=== COMMENT 4437283467 apps/documentation/src/content/docs/backlog/prepare-screen.md:183
👮 **Wachiman** · 🟡📝 **Consider · docs: QA step says to drag the copy's row, but only the Drag button starts a drag**

In `master-copies-panel.tsx:165-179`, only the **Drag** button is `draggable` and calls `startFileDrag`. The rest of the row is a `<Link>` to the copy's page. Section 2 of this doc describes it correctly as "a **Drag** handle", but the validation script says "Drag the copy's row out of the page into Finder". A tester who drags the row itself drags a link, not the file. Change this line to say "the copy's Drag handle".

<!-- wachi:finding -->

