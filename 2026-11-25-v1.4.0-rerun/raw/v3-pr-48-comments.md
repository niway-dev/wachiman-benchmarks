# kaipu-bench-wachi-v3#48 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T23:59:30Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Show in Finder / drag on the Library card do not mark the copy seen, unlike the ready toast (confidence high)**

The ready toast calls `markCopySeen(recording.assetId)` before both `revealLocalRecording` and `startFileDrag` (export-status-cards.tsx:280, :293), and the store's contract says a copy is unseen until the user opens it "or acts on its ready card (Show in Finder, drag it out)" (ready-copies.ts:10-11). The new Library card calls the same two IPCs (lines 80 and 93) but skips `markCopySeen`. So after a user drags the YouTube copy into the upload page from this card, the card stays, and once they leave the Library the copy keeps its pink outline and stays in the "1 copy ready" chip until they open its page. The same action on the toast clears all of that. Either call `markCopySeen(video.assetId)` in both handlers, as the toast does, or update the store's docstring if the card is meant to stay after an action.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225 · github-actions[bot] · 2026-11-25T23:59:30Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "opening the copy goes to its page and forgets it" never checks the forgetting (confidence high)**

The test asserts only the pathname (line 231). It never checks that `markCopySeen` ran, for example that `getReadyCopies().copies` no longer holds `asset-copy`. The sidebar route hook in the real app would also call `markCopySeen` on the detail route, but this test renders no sidebar, so the claim in its name goes unchecked. If `onOpen`'s `markCopySeen` call (library-page.tsx:416) were removed, the test would still pass.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/ready-copy-in-library.md:8 · github-actions[bot] · 2026-11-25T23:59:30Z

👮 **Wachiman** · 🟡📝 **Consider · docs: Status banner names a different base than the PR (confidence medium)**

The banner says this work is stacked on #459, and index.mdx:36 also says "stacked on #459". The PR description says it is stacked on #466 (`feature/floating-ready-window`), on top of #459 ← #467 ← #465. If #466 is the real base, update both the banner and the backlog row so they point at it.

<!-- wachi:finding -->
