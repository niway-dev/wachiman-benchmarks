<!-- cap-0.75, api-key-3: 15 turns, $0.6 -->

I found two real bugs and one smaller inconsistency. I read the diff and the code it calls (`destinations.ts`, `resolveExportTarget`, `useSourceProbe`/`asPreparable`, `runningCopyOf`, the `startFileDrag` IPC in main, and the ready card's drag). I didn't run the tests.

### 1. The size on each destination card stays "…" for good if the file can't be read
`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43` and `:91`

- **What goes wrong:** every card except Archive shows `size ?? "…"`, and that is `null` whenever `probe` is `null`.
- **Why:** `useSourceProbe` returns `probe: null` both while it is loading and when it fails (`{ status: "error", probe: null }` in `use-prepare-copy.ts:57`). The page only passes `.probe` (`library-detail-page.tsx:142`), so the panel can't tell the two apart. A file it can't read shows "…" forever, which looks like it is still loading.
- **Fix:** pass the probe status in, and show nothing (or "—") on error.

### 2. Right after a copy finishes, the page briefly switches back to "Where is it going?"
`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189-191` and `:2057` in the diff (`{hasCopies && …}`)

- **What goes wrong:** while the first copy encodes, `running` is non-null, so `hasCopies` is true and "Copies from this original" shows the progress row.
- **Why:** when the export ends, `runningCopyOf` returns `null` because the status is no longer `"exporting"`. The new file isn't in `exports` until the `refresh()` started by the `readyId` effect (`:146-148`) comes back. In that gap `hasCopies` is false, so `showDestinations` turns true. The copies panel unmounts, the destinations panel and its "heavy to send" note come back, and "Export a copy" disappears. Then everything flips again when the list arrives.
- **Before this PR** the copies panel was always shown for a master (`showCopies = master || …`), so this didn't happen.
- **Fix:** keep `hasCopies` true while `runner.ready?.recording` is a copy of this asset that isn't listed yet.

### 3. Dragging from the copies panel doesn't mark the copy as seen
`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:170-175`

- **What goes wrong:** the new Drag handle copies the ready card's drag (`export-status-cards.tsx:231-236`) but leaves out `markCopySeen(copy.assetId)`.
- **Why it matters:** NIW2-586's Library badge points at unseen copies. Dragging a copy out of the ready card clears that badge; dragging the same copy from this panel doesn't, so the Library keeps pointing at a copy the user already used. This is less serious than the two above, and it may not have been a deliberate choice.

Things I checked that hold up:
- Every new i18n key is in both `en.json` and `es.json`, and nothing still uses the deleted `where*` / `copiesEmpty` / `copyProgress*` keys. `sendTo` is still used by `video-card.tsx` and `video-row.tsx`, so it was right to keep it.
- `presetForDestination(destination, probe)` and `planCopy` are called with the right arguments.
- `groupOf` tones are correct: amber for the `send-more` group, teal for the rest.
- `factsOf` gets the right picture sizes for the Reels and LinkedIn copies: those presets have a fixed canvas, so Fit vs Fill doesn't change the size.
- `startFileDrag(copy.id, copy.title)` matches the main handler, and the button only shows when `copy.id !== null`.
