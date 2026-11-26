# kaipu-bench-wachi-v3#74 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T06:00:25Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: A failed probe leaves six destination cards showing "…" for good (confidence medium)**

`useSourceProbe` sets `{ status: "error", probe: null }` when the file can't be read (`use-prepare-copy.ts:55-57`). The page passes on only `.probe` (`library-detail-page.tsx:142`), so the panel can't tell "still reading" from "failed". Every card except Archive then shows `…` indefinitely and nothing says why. One option is to pass `status` through and render no size, or the full-size text, on `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T06:00:25Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: Test replaces window.electronAPI.startFileDrag and never restores it (confidence medium)**

`window.electronAPI` is built once at module level in `test/setup.ts:109`. Assigning `startFileDrag` directly means the `vi.fn()` stays in place for every later test in the same worker. The sibling test in `export-status-cards.test.tsx:143-152` uses `vi.spyOn(window.electronAPI, "startFileDrag")` and calls `mockRestore()`. Using the same pattern here avoids leaking the mock into other tests.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868 · github-actions[bot] · 2026-11-26T06:00:25Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: The "Saved" notice test doesn't cover coming back to the page (confidence medium)**

Whether the notice shows depends on `location.state.fromRecording` and on a `noticeDismissedFor` that lives only in component state (library-detail-page.tsx:101, 136-137). Say the user leaves for Prepare from a card and comes back with Back. The history entry still carries `fromRecording`, but the remounted page has lost the ✕. So "Saved to your Library." would show again, and the standing "This is your original" note would hide again. The post-recording card already behaves this way, so it may be intended. Still, the doc says the notice shows "only when the page was opened by a fresh recording" (prepare-screen.md:95-97). A test that clicks ✕, navigates away and back, and then asserts what should happen would pin down the intended behaviour.

<!-- wachi:finding -->
