# kaipu-bench-wachi-v3#84 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T06:27:25Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Drag handle doesn't mark the copy as seen, unlike the ready card's drag (confidence high)**

The other copy-drag call site, the ready status card at `features/status-cards/export-status-cards.tsx:233-235`, calls `markCopySeen(recording.assetId)` before `startFileDrag`. `ready-copies.ts:54-58` describes that call as "The user opened the copy or acted on it: nothing left to point at." The new Drag handle skips it. After a user drags a fresh copy out of "Copies from this original", the Library badge (`shell/sidebar.tsx:92-98`) still counts that copy as waiting. The sidebar's route effect clears it only for the original's assetId, not the copy's. Suggested fix: call `markCopySeen(copy.assetId)` before `startFileDrag`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T06:27:25Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Destination sizes stay on "…" forever when the file can't be read (confidence high)**

`probeSource` returns null on any read error (`video-editor/export/probe-source.ts:42-43`). `useSourceProbe` then reports `{status: "error", probe: null}` (`use-prepare-copy.ts:55-57`), and the page only passes `.probe` (`library-detail-page.tsx:142`). In that case every card except Archive shows `…` permanently, which looks like it is still loading. Suggested fix: pass the probe status through and show no size, or a "size unknown" line, once the status is `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T06:27:25Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "Shows only where there is an export screen" never checks the case where there isn't one (confidence high)**

The test name says the button shows *only* when `onOpenExport` is given. The test only renders with the callback and clicks it. Nothing checks that the button is missing when `onOpenExport` is omitted, which is the copy/GIF page case (`library-detail-page.tsx:513`). Suggested fix: add a `renderPanel([copy({})])` without the callback and assert that `queryByRole("button", { name: "Open in Export →" })` is null.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:111 · github-actions[bot] · 2026-11-26T06:27:25Z

👮 **Wachiman** · Nit · 🟡📝 **Consider · docs: Doc leaves out the heavy master after "Not now" (confidence high)**

The doc says the banner stays for "a heavy copy, or a heavy master with copies". The page also shows `HeavyToSendBanner` whenever `heavy && !showDestinations` (library-detail-page.tsx:517), and that includes a heavy master with no copies after the user clicks "Not now" (library-detail-page.tsx:190-191, 494). Suggested wording: "wherever the Where is it going? panel isn't showing (a copy, a master with copies, or after Not now)".

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:492 · github-actions[bot] · 2026-11-26T06:27:25Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: No page test for a master whose only copy is still exporting (confidence medium)**

`hasCopies` is also true when the runner is exporting this recording (`running !== null`, library-detail-page.tsx:188-189). In that state the page should hide "Where is it going?", show "Export a copy" and render the "Exporting · N%" row. The page tests only cover copies that already exist in the list (lines 462-534), so nothing checks that this page wires `runningCopyOf` to the panel. A test that mocks `useExportRunner` with `status: "exporting"` for `asset-b` would cover it, alongside the PR's step 6.

<!-- wachi:finding -->
