# kaipu-bench-wachi-v3#98 [replay r2] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-26T17:34:32Z

| 👮 **Wachiman** | Library ready card's Show in Finder / drag don't mark the copy seen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The header comment in ready-copies.ts says a copy is unseen until the user "opens it or acts on its ready card (Show in Finder, drag it out)". The toast's ExportReadyCard does this: it calls `markCopySeen(recording.assetId)` before `revealLocalRecording` and `startFileDrag` (export-status-cards.tsx:280, 293). The new ReadyCopyCard calls neither (lines 80 and 93). After the user reveals or drags the file from the Library card, the copy keeps its "copy ready" chip and outline on the regular card until they open its page. Call `markCopySeen` in both handlers, or change the ready-copies.ts comment to say the Library card doesn't do this. Note that `markCopySeen` drops the whole entry, so the card would disappear on the first Show in Finder click; decide whether that is wanted.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:216 · github-actions[bot] · 2026-11-26T17:34:32Z

| 👮 **Wachiman** | role="progressbar" nested inside the pill's <button> |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

ARIA treats a button's children as presentational, so most screen readers will not expose the nested progressbar or its aria-valuenow. The pill's accessible name is the static "Show the export's progress", so the percentage is not announced as a value. Consider putting the percent in the button's own label, for example `aria-label` built from `pill`, and dropping the nested role.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:1413 · github-actions[bot] · 2026-11-26T17:34:32Z

| 👮 **Wachiman** | PR body describes email wording that is not in the messages |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The PR body says Email is now its own destination (#467) with its own text: "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag. None of the new `backgroundCopy` messages here or in es.json has an `email` case. `DESTINATION_IDS` in `features/prepare/destinations.ts` has no `email` entry either, since the groups are youtube/vertical/square, github/chat and archive. Either the body describes a base this head does not include, or that wording was dropped. Fix the body, or add the missing cases if the destination exists.

<!-- wachi:finding -->
