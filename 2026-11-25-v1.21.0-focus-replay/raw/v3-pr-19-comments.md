# kaipu-bench-wachi-v3#19 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-25T22:55:26Z

| 👮 **Wachiman** | When the probe fails, six of the seven cards show "…" forever |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The page passes only `useSourceProbe(...).probe` (library-detail-page.tsx:142). When `probeSource` returns an unusable result, `useSourceProbe` sets `{ status: "error", probe: null }` (use-prepare-copy.ts:55-57). So `estimate()` returns null for every card except Archive (line 43), and each one shows the loading ellipsis `"…"` for as long as the page is open. The "Where is it going?" cards then look like they are still loading. Consider passing the probe status, or a flag for it, and showing no size (or `sizeFull`) once the read has failed.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T22:55:26Z

| 👮 **Wachiman** | "Open in Export" test never checks the case where the button is hidden |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "shows only where there is an export screen to open", but it only renders with `onOpenExport` and clicks the button. No test renders without `onOpenExport` and asserts that the button is absent. That absence is the branch at master-copies-panel.tsx:122, which the page relies on for non-preparable copies (library-detail-page.tsx:513).

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-25T22:55:26Z

| 👮 **Wachiman** | Global \`window.electronAPI.startFileDrag\` is overwritten and never restored |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The test assigns a `vi.fn()` straight onto the shared `window.electronAPI` object and never restores it. Any later test in the same worker that relies on the setup's `startFileDrag` sees this mock instead. `vi.spyOn(window.electronAPI, "startFileDrag")` with `restoreAllMocks`, or an `afterEach` that restores the original, keeps the tests isolated.

<!-- wachi:finding -->
