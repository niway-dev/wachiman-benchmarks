# kaipu-bench-wachi-v3#78 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-26T06:00:51Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: A failed probe leaves every destination card at "…" forever (confidence high)**

The page keeps only `.probe` from `useSourceProbe` and drops its `status`. When the read fails, `useSourceProbe` sets `{ status: "error", probe: null }` (`use-prepare-copy.ts:55-57`). `DestinationsPanel` cannot tell that apart from loading, so every card except Archive shows the "…" placeholder (`destinations-panel.tsx:43`, `:91`) for as long as the page is open. Now that this page probes every local recording and puts the estimates on the main panel, consider passing the status down, or showing no size or `sizeFull` once the status is `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T06:00:51Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "shows only where there is an export screen" never checks the case without one (confidence high)**

The test's name promises the button is absent when `onOpenExport` is omitted, but it only renders with the callback and clicks it. Add an assertion that `queryByRole("button", { name: "Open in Export →" })` is null when `renderPanel` gets no `onOpenExport`. That is the case for a copy page without a preparable source (`library-detail-page.tsx:513`).

<!-- wachi:finding -->
