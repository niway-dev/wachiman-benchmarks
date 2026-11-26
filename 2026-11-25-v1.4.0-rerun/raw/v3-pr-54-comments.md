# kaipu-bench-wachi-v3#54 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T00:07:56Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Drag doesn't mark the copy as seen, unlike the ready card's Drag (confidence high)**

The other place that drags a finished copy, `export-status-cards.tsx:233-235`, calls `markCopySeen(recording.assetId)` right before `startFileDrag`. `ready-copies.ts:54` describes that call as "the user opened the copy or acted on it". This new Drag handle skips it. If a user drags a just-finished copy out from the master's page, the copy keeps its "just ready" mark and still counts in the Library badge, because the sidebar clears it only on a visit to the copy's own page (`sidebar.tsx:95`). Suggested fix: call `markCopySeen(copy.assetId)` before `startFileDrag`, the same way the card does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T00:07:56Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Size estimates stay on "…" for good when the file can't be read (confidence medium)**

`useSourceProbe` sets `status: "error"` with `probe: null` when the probe can't be used (`use-prepare-copy.ts:55-57`). The page passes only `.probe` down (`library-detail-page.tsx:142`), so the panel can't tell "still reading" from "failed". In both cases every card except Archive shows `…` permanently. The heavy-to-send text in the same panel already handles this with `heavyBannerBodyNoEstimate`. Consider passing the probe status, or a flag for it, so the cards can drop the placeholder after a failure.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:284 · github-actions[bot] · 2026-11-26T00:07:56Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: No test for a file that can't be read: the destination cards would show "…" forever (confidence medium)**

`useSourceProbe` sets `{ status: "error", probe: null }` when the probe result is unusable (`features/prepare/use-prepare-copy.ts:55-57`). `DestinationsPanel` only looks at `probe`, so in that case every card except the archive one shows `"…"` (`destinations-panel.tsx:43`, `:91`). That `"…"` looks like it is still loading, but it never resolves. The new tests mock `probeSource` to always succeed (`library-detail-page.test.tsx:12-22`), so nothing covers this state. Consider adding a case where `probe` resolves to null. Also consider passing the probe's `status` to the panel so a failed read shows something other than the loading ellipsis.

<!-- wachi:finding -->
