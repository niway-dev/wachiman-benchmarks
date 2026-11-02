=== COMMENT 4437265919 apps/kaipu-record/src/renderer/src/pages/export/export-copy.ts:29
👮 **Wachiman** · 🟡🧹 **Consider · cleanup: EXPORT_ORDER can silently miss a new destination**

`EXPORT_ORDER` is typed as `readonly DestinationId[]`. Unlike `EXPORT_NAME` and `GROUP_SENTENCE`, nothing checks that it covers every destination. It also repeats `DESTINATION_IDS` in the same order (`features/prepare/destinations.ts:37`). If someone adds a destination to `DESTINATION_IDS`, it type-checks but never appears in the bottom row and the arrow keys never reach it. You could derive the row from `DESTINATION_GROUPS.flatMap((g) => g.destinations)`, which already lists them in this order. Another option is a test that `EXPORT_ORDER` sorted equals `DESTINATION_IDS` sorted.

<!-- wachi:finding -->

=== COMMENT 4437265923 apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:40
👮 **Wachiman** · 🟡🐛 **Consider · bug: "Pick from Library" stays enabled while a dropped file is importing**

"Browse files" is disabled while `importing` (line 51), but the `VideoPicker` trigger is not. Say the user picks a Library video while a drop is still importing. `openVideo` navigates to that video. Then, when the import finishes, `usePrepareImport` navigates again to the imported video, so the screen jumps away from the one the user chose. You could pass `disabled={importing}` to the trigger `Button` as well.

<!-- wachi:finding -->

=== COMMENT 4437265927 apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:71
👮 **Wachiman** · 🟡🐛 **Consider · bug: Picker says role="dialog" but leaves keyboard focus on the trigger**

When the panel opens, focus stays on the trigger button, and closing it with Escape doesn't return focus anywhere. A screen reader user hears a dialog announced but is still on the button, and has to tab to reach the list. Two options: move focus to the first item (or the item marked `aria-current`) when the panel opens and give it back to the trigger on Escape, or drop `role="dialog"` and treat it as a disclosure. The disclosure route fits better with the `aria-expanded`/`aria-controls` the trigger already sets.

<!-- wachi:finding -->

=== COMMENT 4437265931 apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:86
👮 **Wachiman** · 🟠🧪 **Fix · tests: "does not take a video dropped on the window" would pass even if Library still took drops**

This test never stubs `window.electronAPI.pathForFile`, so it uses the default from `src/renderer/src/test/setup.ts:156`, which is `() => ""`. In `use-import-videos.ts:102-111`, `importDropped` treats a file with an empty path as skipped and returns before it reaches `importVideoFiles`. So if `LibraryPage` still mounted `useFileDrop` + `importDropped`, the drop would only show a toast, `importVideoFiles` would still never be called, and the assertion would still pass.

The fix: stub `pathForFile` the way `export-page.test.tsx:421` does, so a mounted handler would really reach `importVideoFiles`. Also assert that the drop was not handled: `expect(fireEvent.drop(...)).toBe(true)` means no listener called `preventDefault` (this mirrors `dropFiles` in export-page.test.tsx:416).

<!-- wachi:finding -->

=== COMMENT 4437265937 apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39
👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only checks the case with a video**

The test name says the Export link is active on Export both with and without a video, but it only renders `/export/asset-1`. The no-video case (`ROUTES.exportNew`, i.e. `/export`) is never checked for `aria-current="page"`. `sidebar.tsx:53` links to `ROUTES.exportNew`, so the no-video case is probably the easy one. Still, the test's name claims coverage it doesn't have. Add a `renderAt(ROUTES.exportNew)` assertion, or rename the test.

<!-- wachi:finding -->

=== COMMENT 4437265940 apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108
👮 **Wachiman** · 🟠🧹 **Fix · cleanup: Orphaned comment for the removed import drop strip**

The PR deletes the `.importZone` rule, but its comment (`/* NIW2-579: the "Drop a video here" strip, between the header and the toolbar. */`) is still there. It now sits right above the `.stickyBar` comment, so it reads as if it describes the sticky toolbar. Delete line 108.

<!-- wachi:finding -->

