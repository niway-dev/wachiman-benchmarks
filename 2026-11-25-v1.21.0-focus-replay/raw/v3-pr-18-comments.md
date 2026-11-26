# kaipu-bench-wachi-v3#18 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:16 · github-actions[bot] · 2026-11-25T22:55:29Z

| 👮 **Wachiman** | Do Share copies get tagged with a Prepare destination? |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

`copyPresetOf` treats any recording whose fingerprint starts with `whole` as a destination copy. The doc comment says Share writes that fingerprint too (see `export-runner.ts:55` and `:128`). `destinationOfPreset` maps `light` to github and `balanced` to chat (`destinations.ts:62-69`). So a Share export at `balanced` would show "For chat" in the grid, and Prepare never made it. Are Share copies meant to carry a destination tag? If they are not, the sidecar needs to say which flow made the copy. Also, `destinationOfPreset` asserts its result with `!`. A `whole` preset outside `DESTINATION_PRESETS` returns `undefined` while its type says `DestinationId`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:97 · github-actions[bot] · 2026-11-25T22:55:29Z

| 👮 **Wachiman** | Fallback for an editor export differs from the toast's |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

For an editor export, the Library card passes `destination ?? "other"` to `dragTo`, while the ready toast passes `job.destination ?? "export"` (`export-status-cards.tsx:63`). Today both land on the ICU `other` branch ("Drag to upload"). If `pill`/`dragTo` ever gets a separate `export` branch, the two will drift apart. Reusing one helper would keep them in step.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:216 · github-actions[bot] · 2026-11-25T22:55:29Z

| 👮 **Wachiman** | The pill's progressbar is inside a button, so screen readers hide it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

In ARIA, a button's children are presentational. The `role="progressbar"` span inside the pill's `<button>` is therefore not exposed, and the button's `aria-label` ("Show the export's progress") replaces its text. A screen-reader user hears no percent while the widget is minimized. One fix is to put the percent in the button's accessible name; another is to move the progressbar out of the button.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/ready-copy-in-library.md:8 · github-actions[bot] · 2026-11-25T22:55:29Z

| 👮 **Wachiman** | Status banner names a different stack base than the PR |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The banner says the branch is stacked on #459 (Prepare drop zone), and the new row in `backlog/index.mdx:36` says the same. The PR description says it is stacked on #466 (`feature/floating-ready-window`), with the chain #459 ← #467 ← #465 ← #466. It would help to make the banner and the index row match the real base so reviewers check the right parent.

<!-- wachi:finding -->
