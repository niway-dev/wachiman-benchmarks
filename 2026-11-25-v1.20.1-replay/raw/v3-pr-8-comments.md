# kaipu-bench-wachi-v3#8 [replay r2] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T21:53:51Z

| 👮 **Wachiman** | Show in Finder / drag on the Library ready card do not mark the copy seen, unlike the ready toast |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The ready toast's identical actions call `markCopySeen(recording.assetId)` before `revealLocalRecording` and before `startFileDrag` (`export-status-cards.tsx:280`, `:293`). The store documents acting on the ready card (Show in Finder, drag it out) as what makes a copy seen (`ready-copies.ts:10-11`). The new card calls `revealLocalRecording(localId)` (line 80) and `startFileDrag` (line 93) without marking it. After the user reveals or drags the copy out from the Library, the "Ready to upload" card stays, the "1 copy ready" chip keeps counting it, and once the card is retired the regular card is still outlined as unseen. Call `markCopySeen(video.assetId)` in both handlers, or pass an `onActed` callback from `library-page.tsx` the way `onOpen` already does. If the card should stay on screen while the user drags, that needs its own decision. The library-page test at `library-page.test.tsx:196-213` does not check seen state after these actions.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:93 · github-actions[bot] · 2026-11-25T21:53:51Z

| 👮 **Wachiman** | Drag name and displayed file name disagree for an untitled copy |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The card shows and labels the file as `title`, which falls back to `tLibrary("untitled")` (line 37). The drag passes the raw `video.title`, which can be an empty string. For an untitled copy, the button's aria-label says "Drag Untitled.mp4…" but main gets an empty name. Passing `title` keeps the two consistent. The extension is also hard-coded to `.mp4` (line 38), while the toast reads it from the real file path (`export-status-cards.tsx:243`).

<!-- wachi:finding -->
