# kaipu-bench-wachi-v3#76 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-26T06:00:32Z

👮 **Wachiman** · Nit · 🟡⚡ **Consider · perf: Source probe now runs on every local recording's page, not only heavy/fresh ones (confidence medium)**

Before, `useSourceProbe` was only given an id when the heavy banner or the post-recording card needed numbers (`heavy || showCard`). Now it gets `preparable?.id` every time the page opens for a local recording or copy, so every visit reads the file. That gets the resolution into the metadata line and the destination estimates. If probing is expensive (decoding a long recording's header or demuxing it), consider whether the metadata line is worth a probe on every visit, or whether the result should be cached per id.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T06:00:32Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: Overwrites `window.electronAPI.startFileDrag` and never restores it (confidence high)**

The test assigns `vi.fn()` straight onto the shared `window.electronAPI` stub (set once per file in `src/renderer/src/test/setup.ts:109`) and leaves it there. The sibling test in `features/status-cards/export-status-cards.test.tsx:143-152` uses `vi.spyOn(window.electronAPI, "startFileDrag")` and then `mockRestore()`. Using the same pattern here would keep later tests in the file from seeing a stale mock.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T06:00:32Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never tests the absent case (confidence high)**

The test name promises the button appears only when `onOpenExport` is given. It only renders with the callback and clicks it. Add a check that `renderPanel([copy({})])` without `onOpenExport` has no "Open in Export →" button. That is the copy-of-a-non-local-recording path the page relies on at `library-detail-page.tsx:513`.

<!-- wachi:finding -->
