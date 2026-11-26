# kaipu-bench-wachi-v3#86 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T17:02:42Z

| 👮 **Wachiman** | An unreadable file leaves every estimate on "…" for good |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`estimate` returns null whenever `probe` is null, and the card then shows `"…"`. `useSourceProbe` returns `probe: null` both while it is loading and after it fails (`status: "error"`, use-prepare-copy.ts:55-57), and `probeSource` turns every read failure into null (probe-source.ts:42-43). So when the file can't be read, five of the six cards keep a loading ellipsis that never resolves, and nothing tells the user it failed. The cards still open Prepare. Consider passing the probe status in and showing no size (or the `sizeFull`-style fallback) once it is `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T17:02:42Z

| 👮 **Wachiman** | "shows only where there is an export screen" never checks the missing case |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test name says the button appears *only* when there is an export screen, but it only renders with `onOpenExport` and clicks it. No assertion checks that the button is absent when `onOpenExport` is omitted (the guard at master-copies-panel.tsx:122). Add a render without it and assert `queryByRole("button", { name: "Open in Export →" })` is null.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:184 · github-actions[bot] · 2026-11-26T17:02:42Z

| 👮 **Wachiman** | Validation step says to drag the copy's row, but only the Drag handle starts a file drag |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The validation script says "Drag the copy's row out of the page into Finder." In `master-copies-panel.tsx:153-163` the row's body is a `<Link>` to the copy's page. Dragging that part gives the browser's own link drag, a URL. Only the separate **Drag** button (`master-copies-panel.tsx:164-179`) calls `startFileDrag` and hands over a real file. Someone validating by this script could drag the name or logo, get no file in Finder, and report the feature broken. Suggest "Drag the copy's **Drag** handle into Finder", which is how line 110 and the PR's own test steps word it.

<!-- wachi:finding -->
