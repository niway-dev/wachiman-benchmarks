# kaipu-bench-wachi-v3#113 [replay r2] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-26T20:07:46Z

| 👮 **Wachiman** | Library ready card's Show in Finder and drag don't mark the copy seen, unlike the toast |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The toast's `ExportReadyCard` calls `markCopySeen(recording.assetId)` on Show in Finder and on drag start (export-status-cards.tsx:280, 293). The new `ReadyCopyCard` does neither (here and at line 93). The header comment in `ready-copies.ts` (lines 9-11) still says a copy is unseen "until the user opens it or acts on its ready card (Show in Finder, drag it out)". In the Library the user can reveal or drag the file and the "1 copy ready" chip and pink outline stay until they open the copy or leave. If keeping the card on screen after an action is intended, update that comment. If not, call `markCopySeen` like the toast does. Note that `markCopySeen` also drops the whole entry, so the card would disappear on click.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225 · github-actions[bot] · 2026-11-26T20:07:46Z

| 👮 **Wachiman** | "opening the copy goes to its page and forgets it" never checks that it was forgotten |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test only asserts `router.state.location.pathname`. Nothing checks that `markCopySeen` ran, e.g. `getReadyCopies().copies` is empty or `readyCards(...)` is `[]`. Removing the `markCopySeen` call in `onOpen` (library-page.tsx:416) would leave it green, because the Sidebar that would also forget the copy isn't rendered in this test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:199 · github-actions[bot] · 2026-11-26T20:07:46Z

| 👮 **Wachiman** | Pill's progress is hidden from assistive tech |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The pill is a `<button aria-label={t("expand")}>` with a `role="progressbar"` span inside it. Button children are presentational, and the aria-label replaces the button's name. A screen-reader user hears only "Show the export's progress" and never the destination or percent. Put the percent in the button's label (or expose it with `aria-describedby`) and drop the nested progressbar role.

<!-- wachi:finding -->
