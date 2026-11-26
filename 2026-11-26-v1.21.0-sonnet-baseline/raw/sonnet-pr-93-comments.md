# kaipu-bench-wachi-v3#93 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-26T17:30:39Z

| 👮 **Wachiman** | Library ready card's Show in Finder / drag do not mark the copy seen, unlike the ready toast |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`ExportReadyCard` calls `markCopySeen(recording.assetId)` before `revealLocalRecording` (export-status-cards.tsx:280) and before `startFileDrag` (:293). The `ready-copies.ts` header (lines 9-11) defines "unseen" as cleared when the user opens the copy or acts on its ready card (Show in Finder, drag it out). The new `ReadyCopyCard` does neither (here and at line 93). A user who drags the file out of the Library card therefore keeps the "1 copy ready" chip. After they leave the Library, the regular card also comes back with the "just ready" outline, for a file they already took. If leaving the copy unseen is intended, say so in the `ready-copies.ts` comment. If not, mark it seen on those two actions.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102 · github-actions[bot] · 2026-11-26T17:30:39Z

| 👮 **Wachiman** | Cards are retired on leaving the Library even if they were never rendered |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`retireReadyCards()` runs on any route change away from `/library`, but the card only renders in grid view (library-page.tsx:408-421) and only when the copy passes the current filters and is already in `videos` (the `leading` memo, library-page.tsx:126-132). If the user is in list view, has a filter that hides the copy, or leaves before the rescan includes it, the card is retired without ever being shown. The `retireReadyCards` comment says "every card it showed has been seen", which is false in those cases. The copy then comes back only as the outlined regular card on the next visit. Consider retiring only cards that were actually rendered, or accept this and narrow the comment.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:202 · github-actions[bot] · 2026-11-26T17:30:39Z

| 👮 **Wachiman** | Pill's aria-label hides its own progress text from assistive tech |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The minimized pill is a `<button aria-label={t("expand")}>` whose visible content is the percent text and a `role="progressbar"` span. The button's label replaces its content in the accessible name. Children of a button are also presentational, so the nested progressbar is not exposed. Screen-reader users hear only "Show the export's progress" and never the percent. A label such as "YouTube copy · 38% — show the export's progress", or an `aria-live` region outside the button, would keep the information.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/ready-copy-in-library.md:8 · github-actions[bot] · 2026-11-26T17:30:39Z

| 👮 **Wachiman** | Doc and PR description disagree on the stack base and on email wording |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The doc says the work is stacked on #459. The PR description says it is stacked on #466 (#459 ← #467 ← #465 ← #466). The PR description also says email is now its own destination (#467), with "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag. This doc does not mention email. `DESTINATION_IDS` in `destinations.ts` (36-43) has no `email`, and neither message file has an email branch. Either the description is stale or the email wording is missing from this head; see the question on `en.json`.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:1431 · github-actions[bot] · 2026-11-26T17:30:39Z

| 👮 **Wachiman** | PR description promises an email destination's wording, but no message has an email branch |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The description says email "gets its own text" (Exporting for email, Email copy ready, Drag to an email, FOR EMAIL tag), instead of "your export" and "Archive copy". In this head, `progressTitle`, `readyTitle`, `pill`, `dragTo` and `destinationTag` (en.json 1413-1431, es.json 1413-1431) have no `email` branch. `destinationTag` maps every unknown value to `other` → "Archive copy". `DestinationId` (`prepare/destinations.ts:36-44`) has no `email`. If a destination is ever added without a matching branch, it silently reads as an archive copy. Is the email part intentionally not in this head? If so, the description should say so.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:199 · github-actions[bot] · 2026-11-26T17:30:39Z

| 👮 **Wachiman** | Minimized pill: the button's aria-label hides the percent and the nested progressbar |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The pill (rendered in the same part-1 file; its CSS is `.pill` in the part-2 stylesheet) is a `<button aria-label={t("expand")}>` that contains a `role="progressbar"` span. The button's label overrides its content, and a button's children are presentational for assistive tech. A screen-reader user hears only "Show the export's progress", never the destination or the percent. Fold the pill text into the label, for example by reusing `t("pill", …)`, and drop the nested progressbar role.

<!-- wachi:finding -->
