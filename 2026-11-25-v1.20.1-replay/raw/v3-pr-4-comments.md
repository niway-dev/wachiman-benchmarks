# kaipu-bench-wachi-v3#4 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-25T21:49:27Z

| 👮 **Wachiman** | A failed probe leaves every destination card on "…" for good |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The page keeps only `.probe` from `useSourceProbe` and drops `.status`. When the file can't be read, `useSourceProbe` (use-prepare-copy.ts:55-57) returns `{ status: "error", probe: null }`. `DestinationsPanel` gets `null` and every card except Archive shows `"…"` (destinations-panel.tsx:43, 91), which looks exactly like loading. Before this change the probe only ran for heavy recordings or the card; now it runs for every local recording, so an unreadable file hits this on every visit. You could pass the status down and show a dash or hide the estimate on `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T21:49:27Z

| 👮 **Wachiman** | "shows only where there is an export screen" never checks the case with no export screen |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test only renders with `onOpenExport` set and clicks the button. Nothing checks that the button is missing when `onOpenExport` is omitted, which is the case the name promises (`onOpenExport={preparable ? … : undefined}` on the page). Add a `queryByRole(..., { name: "Open in Export →" })` that expects `null` for a render without the callback.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-25T21:49:27Z

| 👮 **Wachiman** | \`window.electronAPI.startFileDrag\` is overwritten and never restored |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The test assigns a `vi.fn()` straight onto the shared `window.electronAPI` and never restores it. Any later test in the same environment that relies on the original stub will see this mock instead. `vi.spyOn(window.electronAPI, "startFileDrag")` with restore, or putting the original back in `afterEach`, keeps the tests independent.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868 · github-actions[bot] · 2026-11-25T21:49:27Z

| 👮 **Wachiman** | The "Saved" notice's ✕ does not survive a trip to Prepare and Back, and no test covers it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`showSavedNotice` is `fromRecording && noticeDismissedFor !== location.key` (library-detail-page.tsx:136-137). `fromRecording` comes from the history entry's state (library-detail-page.tsx:101), but `noticeDismissedFor` is component state. Say the user dismisses the notice, picks a destination card (`navigate(preparePath(...))`, :149-151) and then presses Back. The page remounts under the same entry with `fromRecording` still true, and the green "Saved to your Library" notice comes back, hiding the standing master note again (:341). The post-recording card already worked this way, but the notice is new. This test only checks the ✕ on the same mount. If the notice is meant to stay hidden for the whole arrival, the dismissal has to outlive a remount (for example in a module-level set keyed by `location.key`), and a test that navigates away and back would pin it.

<!-- wachi:finding -->
