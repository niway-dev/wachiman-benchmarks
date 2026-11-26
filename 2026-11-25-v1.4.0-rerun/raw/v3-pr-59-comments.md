# kaipu-bench-wachi-v3#59 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T00:08:37Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: Drag test replaces the shared electronAPI stub and never puts it back (confidence high)**

`window.electronAPI.startFileDrag = startFileDrag` overwrites the global stub from `src/renderer/src/test/setup.ts:153` for the rest of this file, and nothing restores it (setup's `afterEach` only runs `cleanup()`). The other test of this call, `export-status-cards.test.tsx:143-152`, uses `vi.spyOn(window.electronAPI, "startFileDrag")` and then `mockRestore()`. Doing the same here stops the mock from leaking into later tests in this file.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T00:08:38Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never tests the case without one (confidence high)**

The test only renders the panel with `onOpenExport` and clicks the button. The "only" half of its name, that the button is absent when `onOpenExport` is omitted (the GIF/screenshot case at `library-detail-page.tsx:513`), is never asserted. Add a render without `onOpenExport` that checks the "Open in Export →" button is not there.

<!-- wachi:finding -->
