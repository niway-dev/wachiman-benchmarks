# kaipu-bench-wachi-v3#88 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-26T17:03:50Z

| 👮 **Wachiman** | Dragging a copy out from the panel doesn't mark it as seen, unlike the ready card's Drag |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The only other place that drags a finished copy, the ready card (`export-status-cards.tsx:231-235`), calls `markCopySeen(recording.assetId)` before `startFileDrag`. The comment on `ready-copies.ts:54` says to call it when "the user opened the copy or acted on it". The new Drag handle calls `startFileDrag` and skips that step. If you drag a fresh copy straight out of "Copies from this original", it stays in the unseen ready-copies store. Only opening the copy's page clears it (`shell/sidebar.tsx:95`). Calling `markCopySeen(copy.assetId)` in `onDragStart` would make the two drag paths behave the same.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T17:03:50Z

| 👮 **Wachiman** | The "shows only where there is an export screen" test checks only the case where the button is present |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test's name promises that "Open in Export →" appears *only* when there is an export screen. It renders with `onOpenExport` and clicks the button, but it never renders without the prop to check that the button is missing. The page relies on that case: it passes `undefined` for a non-preparable recording (`library-detail-page.tsx:513`). Adding `expect(queryByRole('button', { name: 'Open in Export →' })).toBeNull()` for a render without the prop would cover what the name claims.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T17:03:50Z

| 👮 **Wachiman** | The test replaces the shared \`window.electronAPI.startFileDrag\` stub and never restores it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`window.electronAPI.startFileDrag = startFileDrag` overwrites the stub that `test/setup.ts:109` installs, and nothing puts it back. The sibling test does the same check with `vi.spyOn(window.electronAPI, "startFileDrag")` and then `mockRestore()` (`export-status-cards.test.tsx:143,152`). Using that pattern here keeps the mock from leaking into later tests in the file.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:183 · github-actions[bot] · 2026-11-26T17:03:50Z

| 👮 **Wachiman** | QA step says to drag the copy's row, but only the Drag button starts the file drag |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The validation step says "Drag the copy's row out of the page into Finder". In `master-copies-panel.tsx:153-163` the row's body is a `<Link>`, and only the separate `draggable` Drag button (`master-copies-panel.tsx:164-179`) calls `startFileDrag`. If someone follows this step literally and drags the row, they get the browser's default link drag (a URL), not the file, and could record a false failure. Line 109 of this doc already says the **Drag** handle does it. Suggested wording: "Drag the copy's **Drag** handle into Finder".

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:301 · github-actions[bot] · 2026-11-26T17:03:50Z

| 👮 **Wachiman** | Nothing tests a heavy master after "Not now": the hint should move from the panel to the banner |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

On a heavy master, the page moves the heavy-to-send hint into `DestinationsPanel` while it shows, and renders `HeavyToSendBanner` only when `heavy && !showDestinations` (`library-detail-page.tsx:496-503`, `517-523`). The "Not now" test uses `exportedOnlyItem`, and the heavy suite never presses "Not now". So nothing checks that dismissing the panel on a 119 MB master brings back the "Prepare a light copy →" banner. If that broke, the hint would quietly disappear. One more case in the NIW2-218 describe would cover it: click "Not now", then expect the banner button.

<!-- wachi:finding -->
