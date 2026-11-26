# kaipu-bench-wachi-v3#34 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:174 · github-actions[bot] · 2026-11-25T23:52:49Z

| 👮 **Wachiman** | Drag handle skips markCopySeen, which the other drag site calls |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The ready card's Drag handle (`features/status-cards/export-status-cards.tsx:234-235`) calls `markCopySeen(recording.assetId)` before `window.electronAPI.startFileDrag(...)`. `markCopySeen` is documented as "The user opened the copy or acted on it: nothing left to point at" (`video-editor/export/ready-copies.ts:54-55`), and it clears the Library's just-ready highlight and badge. The new Drag button here calls only `startFileDrag`. So a user who drags a fresh copy out from "Copies from this original" still sees it flagged as new in the Library and sidebar badge. Call `markCopySeen(copy.assetId)` before the drag, as the sibling does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-25T23:52:49Z

| 👮 **Wachiman** | Size shows "…" forever when the probe fails |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`useSourceProbe` returns `{ status: "error", probe: null }` when the file can't be read or the probe is unusable (`use-prepare-copy.ts:55-57`). The page passes only `.probe` (`library-detail-page.tsx:142`), so the panel can't tell loading apart from failure. Every card except the archive card keeps the loading ellipsis indefinitely. Consider passing the status, or showing nothing once the probe has failed.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-25T23:52:49Z

| 👮 **Wachiman** | "shows only where there is an export screen" never tests the absent case |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test name promises that the button is hidden when `onOpenExport` is omitted. The body only renders with `onOpenExport` and clicks the button. Add an assertion that `queryByRole("button", { name: "Open in Export →" })` is null when the prop is omitted. The default `renderPanel` call already omits it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-25T23:52:49Z

| 👮 **Wachiman** | Test overwrites window.electronAPI.startFileDrag without restoring it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The test assigns `window.electronAPI.startFileDrag = vi.fn()` directly and never restores it. The mock leaks into later tests in the same environment. `vi.spyOn(window.electronAPI, "startFileDrag")` with `restoreAllMocks`, or an `afterEach`, keeps the tests isolated.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:525 · github-actions[bot] · 2026-11-25T23:52:49Z

| 👮 **Wachiman** | The copy's picture-size assertion accepts any height |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says the copy's picture size "follows from the master's (2560 × 1440) and its preset", but `/× \d+ · 9.0 MB$/` accepts any width and height. If the height derivation were wrong (for example, the master's 1440 shown unscaled for the Light preset), the test would still pass. Pin the exact string the Light preset produces from the mocked 2560 × 1440 probe (line 14), as the post-recording card test does at line 815 with "1:18 · 2560 × 1440 · 4.0 MB".

<!-- wachi:finding -->
