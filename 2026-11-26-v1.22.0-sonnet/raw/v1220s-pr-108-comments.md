# kaipu-bench-wachi-v3#108 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-26T20:03:27Z

| 👮 **Wachiman** | Library ready card's Show in Finder / drag do not mark the copy seen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The toast's `ExportReadyCard` calls `markCopySeen(recording.assetId)` before `revealLocalRecording` (export-status-cards.tsx:280) and before `startFileDrag` (:293). `ready-copies.ts:9-11` says a copy is unseen "until the user opens it or acts on its ready card (Show in Finder, drag it out)". The new `ReadyCopyCard` does neither call (lines 80 and 93). After the user reveals or drags the file from the Library card, the copy stays unseen, so the "1 copy ready" chip and the outline remain. Either call `markCopySeen` in both handlers, or change the comment to say the Library card does not count as acting on the copy.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:216 · github-actions[bot] · 2026-11-26T20:03:27Z

| 👮 **Wachiman** | Progress percent inside the pill is hidden from assistive tech |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The `role="progressbar"` span sits inside a `<button>` that has its own `aria-label={t("expand")}`. Button children are presentational, and the button's label replaces its content, so a screen reader announces only "Show the export's progress" and never the percent. Sighted users get the percent in the pill text. Put the percent into the button's accessible name, for example by labelling it with the `pill` message plus the expand hint, and drop the nested progressbar role.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:126 · github-actions[bot] · 2026-11-26T20:03:27Z

| 👮 **Wachiman** | Ready cards are retired on leaving the Library even if the list view hid them |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

Cards render only in the grid branch (line 408 onward). `retireReadyCards` runs whenever the route leaves `/library` (sidebar.tsx:102), whatever the view. A user in list view never sees the "Ready to upload" card, yet it is retired when they leave. The comment at ready-copies.ts:94 says the cards were "seen", which is not true in that case. Consider showing the cards in list view too, or retiring only when the grid was shown.

<!-- wachi:finding -->
