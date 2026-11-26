# kaipu-bench-wachi-v3#23 [replay r2] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T22:58:55Z

| 👮 **Wachiman** | Show in Finder and drag on the Library ready card never mark the copy seen |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The ready-copies store says a copy stays unseen only until the user "acts on its ready card (Show in Finder, drag it out)" (`ready-copies.ts:10-11`). The toast's ready card follows that: it calls `markCopySeen(recording.assetId)` before `revealLocalRecording` and before `startFileDrag` (`export-status-cards.tsx:280`, `:293`). The new Library card calls the same two IPCs at lines 80 and 93 but skips `markCopySeen`. So after the user reveals the file or drags it into YouTube Studio, the big "Ready to upload" card stays at the top of the grid. Once it is retired, the copy keeps its pink unseen outline and stays counted in the "1 copy ready" chip, even though it has already been uploaded. The test at `library-page.test.tsx:196-213` doesn't assert this either. Fix: call `markCopySeen(video.assetId)` in both handlers, or pass in an `onActed` callback the way `onOpen` does.

<!-- wachi:finding -->
