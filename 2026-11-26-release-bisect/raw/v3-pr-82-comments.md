# kaipu-bench-wachi-v3#82 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T06:27:26Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Drag handle skips markCopySeen, which the ready card's drag calls (confidence medium)**

The ready card's Drag (`export-status-cards.tsx:231-235`) calls `markCopySeen(recording.assetId)` before `startFileDrag`, so the copy leaves the ready list and stops counting toward the Library badge (`ready-copies.ts:55-58`, `sidebar.tsx:92-98`). The new handle here sends the same file with the same IPC but never calls `markCopySeen(copy.assetId)`. If someone drags a fresh copy straight from the original's page without opening the copy's own page, the sidebar still shows it as unseen. Calling `markCopySeen(copy.assetId)` before the IPC would match the sibling.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T06:27:26Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: An unreadable file leaves every estimate at "…" for good (confidence high)**

`useSourceProbe` returns `status: "error"` with `probe: null` when `probeSource` throws or the probe is unusable, for example a file with no duration (`use-prepare-copy.ts:29-31,51-58`; `probe-source.ts:42-43`). The page keeps only `.probe` (`library-detail-page.tsx:142`), so this panel can't tell "still reading" from "failed". Five of the six cards then show the loading ellipsis forever, and nothing says the size is unknown. One option is to pass the probe status and show nothing, or a "size unknown" text, on error.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T06:27:26Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never checks the omitted case (confidence high)**

The test passes `onOpenExport` and asserts that the button calls it. Its name promises the other half too: with no `onOpenExport` (a page where `preparable` is null, `library-detail-page.tsx:513`), the button must not render. Nothing asserts that. Adding `renderPanel([copy({})])` followed by `queryByRole("button", { name: "Open in Export →" })` returning null would cover it.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:183 · github-actions[bot] · 2026-11-26T06:27:26Z

👮 **Wachiman** · Nit · 🟡📝 **Consider · docs: QA step says to drag the copy's row; only the Drag handle starts the file drag (confidence high)**

The validation step says "Drag the copy's row out of the page into Finder". In `MasterCopiesPanel`, though, the native file drag (`startFileDrag`) is wired only to the separate **Drag** button (`master-copies-panel.tsx:164-179`). The rest of the row is a `<Link>` (`master-copies-panel.tsx:153`), and dragging that starts the browser's own link drag, not the file. Someone following this step could drag the row, get a link instead of the video and report a false failure. Line 110 of the same doc already says "a **Drag** handle", so this step could say the same: "Drag the copy's **Drag** handle into Finder."

<!-- wachi:finding -->
