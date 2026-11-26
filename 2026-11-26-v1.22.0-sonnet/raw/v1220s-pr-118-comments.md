# kaipu-bench-wachi-v3#118 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-26T20:08:13Z

| 👮 **Wachiman** | Acting on the Library ready card does not mark the copy seen, unlike the toast card |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The toast's ready card calls `markCopySeen(recording.assetId)` on Show in Finder (export-status-cards.tsx:280) and on drag (export-status-cards.tsx:293). The store's own header says a copy stays unseen "until the user opens it ... or acts on its ready card (Show in Finder, drag it out)" (ready-copies.ts:7-11). The new Library card does neither on reveal (line 80) or drag (line 93). A user who drags the file out of the Library card is left with the "1 copy ready" chip. After leaving the Library, the regular card keeps the pink unseen outline until the copy's page is opened or the app relaunches. If clearing is deliberate here, note that `markCopySeen` also deletes the copy's `card` entry, so the card would vanish on click. Either decide this and update the store doc, or mark the copy seen on these two actions.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225 · github-actions[bot] · 2026-11-26T20:08:13Z

| 👮 **Wachiman** | "opening the copy ... forgets it" never asserts that the copy was forgotten |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "opening the copy goes to its page and forgets it", but it only asserts the pathname (line 231). The `markCopySeen` call in `onOpen` (library-page.tsx:416) is the only thing that forgets the copy in this test, because the Sidebar's route watch is not rendered. Add `expect(getReadyCopies().copies).toEqual([])`, or drop "and forgets it" from the name.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:1431 · github-actions[bot] · 2026-11-26T20:08:13Z

| 👮 **Wachiman** | PR body describes email wording that this head does not contain |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The PR body says email is now its own destination (#467) with "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag, and that before this change the tag said "Archive copy". At this head `DESTINATION_IDS` is youtube, vertical, square, github, chat and archive (`apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`). None of `progressTitle`, `readyTitle`, `pill`, `dragTo` or `destinationTag` has an `email` branch. `destinationTag` sends everything unlisted to `other {Archive copy}`. The same applies to es.json. Either the PR body is out of date or the email commit is missing from the branch. The backlog doc does not mention email either, so it is the body that disagrees with the code and docs. Fix the body, or add the keys together with the destination.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:99 · github-actions[bot] · 2026-11-26T20:08:14Z

| 👮 **Wachiman** | Minimized pill hides the percentage from screen readers |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The pill is a `<button aria-label={t("expand")}>` that wraps a `<span role="progressbar" aria-valuenow=…>` (`export-status-cards.tsx:199-224`). ARIA treats a button's children as presentational and the button's own label wins. Assistive tech therefore announces only "Show the export's progress", with no destination and no percent. Sighted users get "YouTube copy · 38%" while the button's accessible name carries neither. Consider an `aria-label` that includes the `pill` text, for example "Show the export's progress: YouTube copy · 38%". The nested progressbar role can then be dropped.

<!-- wachi:finding -->
