# kaipu-bench-wachi-v3#66 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T01:34:08Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Dragging a copy out here does not mark it seen, unlike the Ready card's Drag (confidence medium)**

The one other Drag of a finished copy, on the Ready card, calls `markCopySeen(recording.assetId)` right before `startFileDrag` (`features/status-cards/export-status-cards.tsx:234-235`). That clears the copy from the "unseen" set that drives the Library page's "1 copy ready" chip and outline (`features/video-editor/export/ready-copies.ts:9-12, 55-58`). This handle skips that call. So when a copy finishes while its card is hidden, and the user drags it out from "Copies from this original", the Library still outlines it as not yet looked at. Calling `markCopySeen(copy.assetId)` before `startFileDrag` would match the card. The store's doc comment names only the ready card's actions, so whether this new drag should count is your call.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-26T01:34:08Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: A failed probe leaves the destination cards showing "…" forever (confidence high)**

The page keeps only `.probe` from `useSourceProbe`, and that is `null` both while loading and after an error (`features/prepare/use-prepare-copy.ts:33-36, 55-57`). `DestinationsPanel` turns a null probe into "…" on every card except Archive (`destinations-panel.tsx:43, 91`). So for a file the probe can't read (no usable width, height or duration), the panel looks like it is still loading and never settles. Passing the status through, or showing nothing or a "size unknown" line when the status is `error`, would say what actually happened. This path matters more now that the probe runs for every local recording, not only heavy ones.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T01:34:08Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never checks the case with no screen (confidence high)**

The test only renders with `onOpenExport` set, then checks that the button is there and fires. The "only" half of the name is the case the page relies on: `onOpenExport` is `undefined` for a non-preparable item (`library-detail-page.tsx:513`), and the button must then be absent (`master-copies-panel.tsx:122`). Nothing asserts that. Adding `renderPanel([copy({})])` plus `expect(queryByRole("button", { name: "Open in Export →" })).toBeNull()` would cover it.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:184 · github-actions[bot] · 2026-11-26T01:34:08Z

👮 **Wachiman** · 🟡📝 **Consider · docs: QA step says to drag the copy's row, but only the Drag handle starts the file drag (confidence high)**

The manual test reads "Drag the copy's row out of the page into Finder." In `master-copies-panel.tsx:164-179`, only the **Drag** button is `draggable` and calls `startFileDrag`. The rest of the row is a `<Link>` (`master-copies-panel.tsx:153`), and dragging an anchor drags its URL, not the file. A tester who follows the doc literally gets a URL or nothing, and could report a bug that isn't there. Suggested wording: "Drag the copy's **Drag** handle into Finder." Line 109 already describes the handle this way.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:92 · github-actions[bot] · 2026-11-26T01:34:09Z

👮 **Wachiman** · 🟡📝 **Consider · docs: Metadata line order in the doc leaves out the capture label and the cloud size (confidence high)**

The doc lists the line as "Local · age · duration · resolution · size · N copies". The page actually renders the capture label (e.g. IMPORTED) between the resolution and the size, and can also show a cloud size and GIF specs (`library-detail-page.tsx:290-321`). This is a small gap, but the doc is presented as the description of the layout.

<!-- wachi:finding -->
