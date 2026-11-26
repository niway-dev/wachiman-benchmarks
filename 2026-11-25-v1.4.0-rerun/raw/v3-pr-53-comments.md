# kaipu-bench-wachi-v3#53 [replay r2] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-26T00:07:34Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Show in Finder / drag on the Library ready card do not mark the copy seen, unlike the toast (confidence high)**

The toast's buttons (`ExportReadyCard`, export-status-cards.tsx:280 and :293) call `markCopySeen(recording.assetId)` before `revealLocalRecording` and `startFileDrag`. The store's own contract says the same thing: a copy stays unseen "until the user opens it … or acts on its ready card (Show in Finder, drag it out)" (ready-copies.ts:10-11). The new Library card skips that step at both buttons (lines 80 and 93). So once the user has revealed or dragged out the YouTube copy from the Library, the "1 copy ready" chip and the pink outline stay on its regular card after they leave and come back, even though they already acted on it. If the card should stay visible after a drag (to allow a second drag), you could still clear the unseen state, for example by calling `markCopySeen` only on the copy's later regular card, or by adding a store action that keeps `card` and drops the unseen flag. Either way, the two surfaces for the same action should agree.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225 · github-actions[bot] · 2026-11-26T00:07:34Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "opening the copy … and forgets it" never checks that it was forgotten (confidence high)**

The test only checks `router.state.location.pathname`. It never checks that `markCopySeen` ran, for example with `getReadyCopies().copies` being empty. Removing `markCopySeen(video.assetId)` from `onOpen` (library-page.tsx:416) would leave this test green. In the real app the sidebar's route watch would also mark it seen, which hides the gap. Add an assertion on the ready-copies store.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/background-copy-toasts.md:16 · github-actions[bot] · 2026-11-26T00:07:34Z

👮 **Wachiman** · 🟡📝 **Consider · docs: The update note leaves out the renamed card text, so the validation steps below check for text that no longer exists (confidence high)**

The new note lists three changes: the ✕ became a minimize, the cards moved, and the Library card is new. It doesn't mention that this PR also rewrote the card text in `packages/i18n/messages/en.json:1413-1418`. "Preparing your YouTube copy…" is now "Exporting for YouTube". The progress line lost "· you can keep working". "Your YouTube copy is ready" is now "YouTube copy ready". "Preparing your export…" is now "Exporting your video". The ready card's "Drag to upload" now names the destination (`dragTo`). This doc is still 🟢 waiting for owner QA, and its "What the user sees" section (lines 29-38) and "How to validate" steps 1, 2, 5 and 6 (lines 60-68) still quote the old text, so QA following them would look for labels that are gone. Suggested fix: add the renamed text to the update note, or update those lines.

<!-- wachi:finding -->
