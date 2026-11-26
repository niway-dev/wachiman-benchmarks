# kaipu-bench-wachi-v3#49 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-25T23:59:44Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Dragging a copy out leaves it marked as unseen (confidence medium)**

The other copy drag, the ready card's drag, calls `markCopySeen(recording.assetId)` right before `startFileDrag` (`features/status-cards/export-status-cards.tsx:234-235`). The contract in `ready-copies.ts:9-10` says a copy stops being unseen when the user acts on it, and "drag it out" is one of the actions it lists. The new Drag handle skips that step. If someone drags a fresh copy out from "Copies from this original", the Library keeps outlining it and its "1 copy ready" chip keeps counting it until they open the copy's own page. Suggested fix: call `markCopySeen(copy.assetId)` before `startFileDrag`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-25T23:59:45Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: If the file can't be read, every estimate shows "…" for good (confidence high)**

`probeSource` returns `null` when it can't read the file (`probe-source.ts:42-43`). `useSourceProbe` then reports `status: "error"` with `probe: null` (`use-prepare-copy.ts:55-57`). The page passes only `.probe` through (`library-detail-page.tsx:142`), so the panel can't tell "still loading" from "failed". Every card except Archive keeps showing the loading ellipsis forever. The heavy-to-send text on the same panel already falls back to wording with no estimate (`heavyBannerBodyNoEstimate`). Suggested fix: pass the probe status too, and show no size, or a "no estimate" line, when it is `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T23:59:45Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The "shows only where…" test never checks the case without the button (confidence high)**

The test is named "Open in Export → shows only where there is an export screen to open", but it only renders with `onOpenExport` and clicks the button. Nothing renders the panel without `onOpenExport` to check the button is absent. That absent case is the one the page relies on for non-preparable sources (`library-detail-page.tsx:513`). Suggested fix: add a `renderPanel([copy({})])` and assert `queryByRole("button", { name: "Open in Export →" })` is null.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:292 · github-actions[bot] · 2026-11-25T23:59:45Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: No test covers "Not now" on a heavy master bringing back the heavy-to-send banner (confidence high)**

On a heavy master, the heavy-to-send hint now moves between two places depending on `showDestinations`. It sits inside `DestinationsPanel` as its `note` (library-detail-page.tsx:496-503). After "Not now", the standalone banner takes over (`heavy && !showDestinations`, library-detail-page.tsx:517). The "Not now" test at line 292 uses a 500-byte item. The heavy tests at 712/748 never press "Not now". So nothing checks that dismissing the panel still leaves the user a way to make the light copy. Consider adding a test with `withSize(119_000_000)`: click "Not now", then check that "Prepare a light copy →" appears and opens `?to=github`.

<!-- wachi:finding -->
