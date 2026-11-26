# kaipu-bench-wachi-v3#43 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T23:56:51Z

| 👮 **Wachiman** | Show in Finder and drag on the Library card do not mark the copy seen, unlike the ready toast |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The ready toast's identical actions call `markCopySeen(recording.assetId)` before `revealLocalRecording` and before `startFileDrag` (`export-status-cards.tsx:280` and `:293`). The store's contract says a copy stays unseen only until the user "acts on its ready card (Show in Finder, drag it out)" (`ready-copies.ts:10-11`). The new card skips that step at line 80 and line 93. So after the user reveals or drags the copy out from the Library, the big card stays at the top of the grid, the "1 copy ready" chip stays, and the outline comes back after leaving. The fix is to call `markCopySeen(video.assetId)` in both handlers, as the toast does. Doing that removes the card, which is the intended result.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225 · github-actions[bot] · 2026-11-25T23:56:51Z

| 👮 **Wachiman** | "opening the copy … forgets it" never checks that it is forgotten |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test only checks that the pathname is `/library/asset-copy`. It never checks that `getReadyCopies().copies` no longer has `asset-copy`, which is the second half of its name and what `onOpen`'s `markCopySeen` call (library-page.tsx:416) is for. Removing that call would leave this test green.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/ready-copy-in-library.md:78 · github-actions[bot] · 2026-11-25T23:56:52Z

| 👮 **Wachiman** | Validation step 7 lists the two cards oldest first |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

Step 7 has you make a GitHub copy, then a chat copy, and expects "two cards, newest first, FOR GITHUB / FOR CHAT, Drag to GitHub / Drag to Slack". Newest first means the chat card comes first, which is what the PR body's step 7 says ("FOR CHAT / Drag to Slack, then FOR GITHUB"). Someone running QA from this doc would be checking for the wrong order. Suggest listing them as "FOR CHAT / FOR GITHUB, Drag to Slack / Drag to GitHub".

<!-- wachi:finding -->
