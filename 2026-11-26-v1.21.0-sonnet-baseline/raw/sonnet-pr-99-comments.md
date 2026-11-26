# kaipu-bench-wachi-v3#99 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T17:35:20Z

| 👮 **Wachiman** | Test name promises an absence check the body does not make |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

"Open in Export → shows only where there is an export screen to open" only renders with `onOpenExport` and clicks. Nothing renders the panel without the prop and asserts the button is missing, which is the "only where" half of the name. Add that assertion, or rename the test to what it checks.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139 · github-actions[bot] · 2026-11-26T17:35:20Z

| 👮 **Wachiman** | Dismissal state outlives the "until the page is left" its comment promises |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`destinationsDismissedFor` is plain `useState` keyed by `video.assetId`. The component stays mounted when the user goes master → copy (via the copy link or the Source link) → back to the master, because only the `:assetId` param changes. So "Not now" then stays in force for that master, and the comment's "until the page is left" is not true for that path. A copy with no copies of its own never shows the panel, so the user can hide it by accident and then has only "Export a copy". The same applies to `noticeDismissedFor` keyed by `location.key`: on Back from Prepare the page remounts under the same history entry, with `fromRecording` still in `location.state`, so the green "Saved to your Library" notice shows again. Either align the comment with this behaviour or reset the state when `assetId` changes.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:306 · github-actions[bot] · 2026-11-26T17:35:20Z

| 👮 **Wachiman** | No page-level test for the panel hand-over while a first copy exports |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The page decides between "Where is it going?" and "Copies from this original" with `hasCopies = exports.length > 0 || running !== null` (library-detail-page.tsx:189), and re-lists when `runner.ready` changes (library-detail-page.tsx:146-148). Every test in this file starts from a static list. None mocks the export runner to check that the destinations panel disappears and the copies panel shows the running row as soon as an export starts. None checks that the list refreshes when a copy finishes. The panel's own test covers the running row in isolation, but not this wiring. A regression here would leave the question on screen over a running export, or the finished copy missing until the next navigation. Consider one test that drives `useExportRunner` (or the module it reads) through exporting and then ready.

<!-- wachi:finding -->
