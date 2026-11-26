# kaipu-bench-wachi-v3#13 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T21:54:17Z

| 👮 **Wachiman** | Show in Finder / drag on the Library ready card don't mark the copy seen |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The ready toast's matching buttons call `markCopySeen(recording.assetId)` before `revealLocalRecording` and `startFileDrag` (export-status-cards.tsx:280 and :293). The ready-copies contract says the same: a copy is unseen until the user opens it "or acts on its ready card (Show in Finder, drag it out)" (ready-copies.ts:10-11). The new card's Show in Finder (line 80) and drag (line 93) skip that step. So after the user reveals or drags the copy out from the Library, the big card stays up, the "1 copy ready" chip still counts it, and once the card is retired the regular card still has its unseen outline. Call `markCopySeen(video.assetId)` in both handlers, as the toast does (or pass an `onActed` callback the page wires up). The library-page test at library-page.test.tsx:196-213 should then check that the card goes away.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:180 · github-actions[bot] · 2026-11-25T21:54:17Z

| 👮 **Wachiman** | \`--bg-hover\` is not defined anywhere, so the ✕ hover always uses a white-tint fallback |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

No stylesheet in the repo defines `--bg-hover`. I searched every `*.css` file, and the tokens live in `packages/tokens/css/tokens.css`. That means `.dismiss:hover` always falls back to `rgba(255, 255, 255, 0.06)`. That works on the dark `--bg-card` (#171719). The light theme block sets `--bg-card: #ffffff` (tokens.css:61), and there the hover background can't be seen. Consider an existing token, or a tint that follows `--text-primary` (e.g. `color-mix(in srgb, var(--text-primary) 8%, transparent)`).

<!-- wachi:finding -->
