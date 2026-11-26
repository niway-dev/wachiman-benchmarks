# kaipu-bench-wachi-v3#103 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-26T17:35:32Z

| 👮 **Wachiman** | Library ready card's Show in Finder / drag don't mark the copy seen, unlike the toast's |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The toast's `ExportReadyCard` calls `markCopySeen` before `revealLocalRecording` and before `startFileDrag` (export-status-cards.tsx:279-294). The ready-copies.ts header (lines 9-11) says a copy is unseen "until the user opens it … or acts on its ready card (Show in Finder, drag it out)". The new Library `ReadyCopyCard` does neither on its two actions (lines 80 and 93). After the user reveals or drags the file from this card, the "1 copy ready" chip and the pink outline stay until they open the copy's page. If keeping the card on screen after a reveal is intended, so a drag can follow, say so in a comment. Otherwise mark the copy seen on drag only.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:216 · github-actions[bot] · 2026-11-26T17:35:32Z

| 👮 **Wachiman** | progressbar nested inside the pill's button is not exposed to assistive tech |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The pill is a `<button aria-label="Show the export's progress">`, and its `<span role="progressbar">` sits inside it. Button children are presentational in ARIA, so the progress value is not announced separately, and the button's own label carries no percent. The tests find the pill by its text, so they would not catch this. Put the percent in the button's accessible name (for example `aria-label` built from `pill`), or keep the progressbar outside the button.

<!-- wachi:finding -->
