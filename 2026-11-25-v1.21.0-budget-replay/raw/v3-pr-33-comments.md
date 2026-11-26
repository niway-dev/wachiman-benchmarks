# kaipu-bench-wachi-v3#33 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T23:51:57Z

| 👮 **Wachiman** | Show in Finder / drag on the Library ready card never mark the copy seen |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The ready-copies contract says a copy stays unseen until the user opens it "or acts on its ready card (Show in Finder, drag it out)" (`ready-copies.ts:10-11`), and the sibling toast does exactly that: `ExportReadyCard` calls `markCopySeen(recording.assetId)` before `revealLocalRecording` and before `startFileDrag` (`export-status-cards.tsx:280`, `:293`). The new Library card calls the IPCs directly (lines 80 and 93) and skips `markCopySeen`. So after the user drags the YouTube copy out of the Library card, the copy keeps its "1 copy ready" chip and its outline after the card retires. Either call `markCopySeen` the way the toast does, or, if the card should stay up so the user can drag again, update the contract comment in `ready-copies.ts`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102 · github-actions[bot] · 2026-11-25T23:51:57Z

| 👮 **Wachiman** | Leaving the Library retires cards the user never saw (list view or filtered out) |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`retireReadyCards()` clears `card` on every copy when the route leaves the Library. But `library-page.tsx:126-132` only renders a ready card for copies the current filters show, and only in grid view (`library-page.tsx:407`). A copy that finished while the user was in list view, or behind a kind or storage filter, loses its card without ever showing it. That contradicts the docstring at `ready-copies.ts:93-95` ("every card it showed has been seen"). If that is intended, the comment should say so. Otherwise, retire only the ids the page actually rendered.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225 · github-actions[bot] · 2026-11-25T23:51:57Z

| 👮 **Wachiman** | "opening the copy … forgets it" never checks the forgetting |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test asserts only the new pathname. Nothing checks that `markCopySeen` ran (for example that `getReadyCopies().copies` no longer has `asset-copy`). If the `markCopySeen` call at `library-page.tsx:416` were removed, the test would still pass.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/background-copy-toasts.md:16 · github-actions[bot] · 2026-11-25T23:51:57Z

| 👮 **Wachiman** | The update banner leaves the old wording in the doc's body and front matter |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The new banner covers the minimize, the new position and the Library card. It does not say that this PR also replaced every string the doc quotes. The description (line 3) and the body (lines 29–38, 60–68) still quote "Preparing your YouTube copy…", "· you can keep working", "Your YouTube copy is ready" and "Drag to upload". The validation steps also tell QA to look for those strings. `en.json:1413-1418` now say "Exporting for YouTube" / "YouTube copy ready", and the `hide` key is gone. Either add a line to the banner saying the wording changed, or update the quoted strings. Otherwise a validator following steps 1–6 will think the build is wrong.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:1413 · github-actions[bot] · 2026-11-25T23:51:57Z

| 👮 **Wachiman** | The PR body promises email wording, but no message has an \`email\` branch |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The description says email is now its own destination with "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag. None of the `select` messages added here has an `email` case: `progressTitle`, `readyTitle`, `pill`, `dragTo` and `destinationTag` at lines 1413–1431, and the same keys in es.json. `DESTINATION_IDS` at this head (`features/prepare/destinations.ts:36-43`) also has no `email`. So the email claim does not match the code. Is the email wording supposed to land in this PR (from the #467 merge)? If so, it is missing from both locales. If not, the description should drop that bullet.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:180 · github-actions[bot] · 2026-11-25T23:51:57Z

| 👮 **Wachiman** | ✕ hover background falls back to a white tint that won't show in the light theme |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`--bg-hover` is not defined in `packages/tokens/css/tokens.css` (it defines `--bg-card-hover`), so this rule always uses the fallback `rgba(255, 255, 255, 0.06)`. On the light theme's `--bg-card: #ffffff` (tokens.css:61), that hover state cannot be seen. `var(--bg-card-hover)` would follow the theme.

<!-- wachi:finding -->
