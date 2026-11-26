# kaipu-bench-wachi-v3#28 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T23:00:10Z

| 👮 **Wachiman** | Show in Finder and drag on the Library card don't mark the copy as seen, but the toast's buttons do |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`ExportReadyCard` calls `markCopySeen(recording.assetId)` before `revealLocalRecording` and before `startFileDrag` (export-status-cards.tsx:280, 293). The store's contract agrees: a copy stays unseen "until the user opens it … or acts on its ready card (Show in Finder, drag it out)" (ready-copies.ts:10-11). The new card calls the IPC on its own (here and at line 93). So a user who drags the copy into YouTube from the Library and then moves to another screen still sees the "1 copy ready" chip and the pink outline on that copy when they come back, even though they already used it. Calling `markCopySeen` here also removes the big card, because `markCopySeen` filters the copy out (ready-copies.ts:76-79). Decide which you want: keep the card but call `markCopySeen` after the drag, or document that the Library card works differently from the toast.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:4 · github-actions[bot] · 2026-11-25T23:00:10Z

| 👮 **Wachiman** | Two or more Ready cards leave an empty cell at the top right of the Library grid |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The Library grid is always `grid-template-columns: repeat(3, 1fr)` and uses the default sparse auto-placement (`library-page.module.css:366-369`; no `grid-auto-flow` anywhere in the renderer). The page renders every ready card first, then the regular cards (`library-page.tsx:408-425`). With `grid-column: span 2`, the first ready card takes row 1, columns 1–2. The second one cannot fit in column 3, so it moves to row 2, columns 1–2. Sparse placement never goes back, so row 1, column 3 stays empty, and every further ready card leaves another hole. This is exactly validation step 7 in the new doc ("two cards, newest first"), and the PR says each finished copy gets its own card. Adding `grid-auto-flow: row dense` to `.grid` would let the first regular card fill the gap. The ready cards stay first and in order, because they come first in the DOM.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:1413 · github-actions[bot] · 2026-11-25T23:00:10Z

| 👮 **Wachiman** | The PR body promises email wording that does not exist at this head |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The description says email is its own destination, with "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag. Neither locale has an `email` branch in `progressTitle`, `readyTitle`, `pill`, `dragTo` or `destinationTag`, and `DESTINATION_IDS` has no `email` (`destinations.ts:36-43`). Also, `destinationTag` maps `other` to "Archive copy", so any destination added later without its own branch would be tagged as an archive copy. Either the description belongs to a different commit, or the merge it mentions (#467) is missing. The new doc also says the PR is stacked on #459 (`ready-copy-in-library.md:8-9`), while the body says #466.

<!-- wachi:finding -->
