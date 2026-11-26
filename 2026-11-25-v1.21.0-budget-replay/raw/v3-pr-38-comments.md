# kaipu-bench-wachi-v3#38 [replay r2] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T23:56:05Z

| 👮 **Wachiman** | Show in Finder and the drag on the Library ready card never mark the copy seen |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The toast's ready card calls `markCopySeen(recording.assetId)` right before `revealLocalRecording` and before `startFileDrag` (`export-status-cards.tsx:280` and `:293`). The store's contract says a copy is unseen until the user opens it "or acts on its ready card (Show in Finder, drag it out)" (`ready-copies.ts:10-11`). The new Library card calls the same two IPCs at lines 80 and 93 but skips that step. So after the user has revealed the file or dragged it into YouTube Studio, the copy stays unseen. When the card retires, the regular card comes back with the pink outline, and the "1 copy ready" chip still counts the copy. That pointer is wrong, and only opening the copy's page clears it. Fix: call `markCopySeen(video.assetId)` in both handlers, as the toast does, or take an `onActed` callback from the page. The library-page test at `library-page.test.tsx:196-213` checks only the IPC calls, so it would not catch this.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:93 · github-actions[bot] · 2026-11-25T23:56:05Z

| 👮 **Wachiman** | The drag passes the raw title while the label uses the "Untitled" fallback |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`fileName` uses `title`, which falls back to `tLibrary("untitled")` (line 37). The drag, however, passes `video.title` (line 93), which can be an empty string for an untitled item. The extension is also guessed from `kind` here, while the toast reads it from the real `filePath` (`export-status-cards.tsx:243`). If main treats an empty name as missing, the dragged file falls back to the vault id, and the shown name no longer matches the dragged file. Passing `title` would keep the two in step.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225 · github-actions[bot] · 2026-11-25T23:56:05Z

| 👮 **Wachiman** | "opening the copy goes to its page and forgets it" never checks the forgetting |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test asserts only the new pathname. It does not check that `markCopySeen` ran, for example that `getReadyCopies().copies` no longer contains `asset-copy`. The second half of its name is untested.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/ready-copy-in-library.md:77 · github-actions[bot] · 2026-11-25T23:56:05Z

| 👮 **Wachiman** | Validation step 7 lists the cards oldest first |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

Step 7 makes a GitHub copy and then a chat copy and expects "two cards, newest first, FOR GITHUB / FOR CHAT, Drag to GitHub / Drag to Slack". `readyCards` reverses the oldest-first list (`ready-copies.ts:103-105`), so the chat card comes first. The PR body's own step 7 gets it right ("FOR CHAT / Drag to Slack, then FOR GITHUB"). A QA tester reading the doc would expect the wrong order. Suggest swapping to FOR CHAT / FOR GITHUB and Drag to Slack / Drag to GitHub.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:1431 · github-actions[bot] · 2026-11-25T23:56:05Z

| 👮 **Wachiman** | The vertical destination gets three different names |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

For `vertical`, the new strings say "Exporting for Reels and TikTok" (1413), "Vertical copy ready" (1418), "Vertical copy" in the pill (1429), "Drag to TikTok or Reels" (1430) and "For Reels" on the tag (1431). So one copy can show FOR REELS on the poster next to "Drag to TikTok or Reels". `es.json` has the same split (1413/1418/1429-1431). Consider picking one name across the five strings.

<!-- wachi:finding -->
