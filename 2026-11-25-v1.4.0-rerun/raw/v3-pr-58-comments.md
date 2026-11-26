# kaipu-bench-wachi-v3#58 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-26T00:07:40Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Show in Finder and the drag here do not mark the copy as seen, unlike the ready toast (confidence medium)**

The ready toast's Show in Finder and drag both call `markCopySeen(recording.assetId)` before calling into IPC (`export-status-cards.tsx:280` and `:293`). The store's contract matches that: a copy is unseen until the user "acts on its ready card (Show in Finder, drag it out)" (`ready-copies.ts:10-11`). The Library's new card calls `revealLocalRecording` / `startFileDrag` directly (lines 80 and 93), so the copy stays unseen. After the user drags the file to YouTube and leaves the Library, the copy's regular card still has the pink outline and still counts in the "1 copy ready" chip.

If the card should stay up after a drag, so the user can drag the file again, one option is to keep the card while clearing the unseen state on leave. Otherwise, call `markCopySeen(video.assetId)` here as the toast does. Either way, update the `ready-copies.ts` comment so it describes what actually happens.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102 · github-actions[bot] · 2026-11-26T00:07:40Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Leaving the Library retires cards that were never shown (list view, filtered out) (confidence high)**

`retireReadyCards()` clears every card when the route leaves `/library`. But the Library renders ready cards only in grid view and only for copies the current filters show (`library-page.tsx:126-132`, `:407-421`). A copy that finishes while the user is in list view, or that the filters hide, loses its "Ready to upload" card the moment the user navigates away, before they ever see it. That contradicts the `retireReadyCards` doc ("every card it showed has been seen", `ready-copies.ts:93-96`). Consider retiring only the asset ids the page actually rendered as leading cards, for example a list the page reports to the store.

<!-- wachi:finding -->
