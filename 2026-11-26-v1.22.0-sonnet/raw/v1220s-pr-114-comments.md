# kaipu-bench-wachi-v3#114 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189 · github-actions[bot] · 2026-11-26T20:07:35Z

| 👮 **Wachiman** | "Where is it going?" can flash back between the export finishing and the re-list |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`running` comes from the runner and goes null as soon as the status leaves "exporting" (master-copies-panel.tsx:35). The finished copy only enters `exports` after `refresh()` returns from the effect at line 146-148, which is async. In that gap `hasCopies` is false, so `showDestinations` (line 190) is true again. The destinations panel reappears, "Export a copy" (line 436) disappears and the copies panel unmounts. After the refresh it flips back. The old `showCopies = master || …` never unmounted the panel on a master, so this is new. Consider keeping the panel hidden while `runner.ready` points at this recording, for example by treating `readyId === video.id`-like state as `hasCopies` until the list contains the copy. I did not run it, so I could not confirm how long the gap is.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T20:07:36Z

| 👮 **Wachiman** | A failed probe leaves "…" on every card for good |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The page passes `useSourceProbe(...).probe`, which is null both while loading and when the read fails or is unusable (use-prepare-copy.ts:29-31, 55-58). The panel can't tell the two apart, so a recording that can't be probed shows "…" (a loading hint) on six of the seven cards for as long as the page is open. The cards still open Prepare, so nothing breaks, but the size slot suggests something is still coming. Pass the probe status, or show nothing in that slot once the read has failed.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-26T20:07:36Z

| 👮 **Wachiman** | The drag test overwrites the global \`startFileDrag\` and never restores it |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`window.electronAPI.startFileDrag = startFileDrag` replaces the stub from test/setup.ts:153 for the rest of the file. The sibling test uses `vi.spyOn(window.electronAPI, "startFileDrag")` and `mockRestore()` (export-status-cards.test.tsx:143-152). Use `vi.spyOn` and restore it, so later tests, and later files if the environment is shared, don't see a leaked mock.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:74 · github-actions[bot] · 2026-11-26T20:07:36Z

| 👮 **Wachiman** | The GitHub copy's picture size is not pinned |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The YouTube row asserts its exact "2560 × 1440 · 22 MB". The GitHub row only checks a substring, `getByText("9.0 MB", { exact: false })`, so the `resolveExportTarget` dimensions for the `light` preset could be wrong and the test would still pass. Assert the full facts string, as the YouTube and GIF rows do.

<!-- wachi:finding -->
