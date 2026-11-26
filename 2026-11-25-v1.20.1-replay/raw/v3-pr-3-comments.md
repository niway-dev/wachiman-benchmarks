# kaipu-bench-wachi-v3#3 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · github-actions[bot] · 2026-11-25T21:49:52Z

| 👮 **Wachiman** | Show in Finder / drag on the Library card do not mark the copy seen, unlike the ready toast |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`ExportReadyCard` calls `markCopySeen(recording.assetId)` before `revealLocalRecording` and `startFileDrag` (export-status-cards.tsx:280, :293), and the store's contract says a copy is unseen "until the user opens it … or acts on its ready card (Show in Finder, drag it out)" (ready-copies.ts:10-11). The new Library card's two actions call the IPC directly and skip that step, so after the user reveals or drags the file out from the Library, the "1 copy ready" chip and the pink outline stay until the copy's page is opened. Note that `markCopySeen` also drops the card (ready-copies.ts:76-79), so wiring it in here makes the big card vanish on click; if that is not wanted, the two paths need a separate "seen but keep the card" step. Either way, the two cards should agree on what an action does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102 · github-actions[bot] · 2026-11-25T21:49:52Z

| 👮 **Wachiman** | Leaving the Library retires cards the user never saw (list view, filtered out) |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`retireReadyCards()` clears every card when the route leaves `/library`, on the premise that "every card it showed has been seen" (ready-copies.ts:93-95). But the Library renders the cards only in grid view and only for copies `visibleItems` holds (library-page.tsx:126-132, :407-409). A user in list view, or with a kind/storage filter or search that hides the copy, leaves the Library and the card is gone without ever having been shown. Only retiring the cards that were actually rendered (e.g. the `leading` ids) would match the comment.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225 · github-actions[bot] · 2026-11-25T21:49:52Z

| 👮 **Wachiman** | "opening the copy goes to its page and forgets it" never checks that it forgets |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test only asserts the pathname (line 231). Nothing checks that `markCopySeen` ran (for example `getReadyCopies().copies` being empty), so if the `markCopySeen` call at library-page.tsx:416 were removed, the test would still pass. That is the half of the title it does not cover.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:97 · github-actions[bot] · 2026-11-25T21:49:52Z

| 👮 **Wachiman** | Different fallback select value from the toast ("other" vs "export") |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

Here a copy with no destination passes `destination ?? "other"` to `dragTo`, while `ExportReadyCard` passes `destinationArg(job)`, which is `job.destination ?? "export"` (export-status-cards.tsx:62-63, :298). Both currently fall into the ICU `other` branch ("Drag to upload"), but the two cards encode the same idea in two ways. If someone later adds an `export {…}` branch to `dragTo`, the two cards will drift apart. Reusing one helper would avoid that.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:216 · github-actions[bot] · 2026-11-25T21:49:52Z

| 👮 **Wachiman** | progressbar role inside a button is not exposed to assistive tech |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The pill's `<span role="progressbar">` sits inside a `<button>` that has its own `aria-label` ("Show the export's progress"). Buttons have presentational children and the aria-label replaces their content, so screen readers announce only the button label: they get neither the percent nor the progressbar. Putting the percent into the button's label (or moving the progressbar out of the button) would expose it.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/ready-copy-in-library.md:8 · github-actions[bot] · 2026-11-25T21:49:52Z

| 👮 **Wachiman** | Status banner names a different base PR than the description |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The banner says the branch is stacked on #459. The PR description says it is stacked on #466 (`feature/floating-ready-window`), with the chain #459 ← #467 ← #465 ← #466. The backlog row in `backlog/index.mdx:36` also says "stacked on #459". Consider updating both so the backlog points at the real base.

<!-- wachi:finding -->
