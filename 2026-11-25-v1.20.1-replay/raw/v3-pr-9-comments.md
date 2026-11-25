# kaipu-bench-wachi-v3#9 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-25T21:53:39Z

| 👮 **Wachiman** | If the file can't be read, the destination cards show "…" forever |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`useSourceProbe` reports `status: "error"` with `probe: null` when the file can't be read (use-prepare-copy.ts:55-57). The page keeps only `.probe` (library-detail-page.tsx:142) and passes it here. So an unreadable file looks exactly like one that is still loading: every non-archive card shows `…` for good, and nothing tells the user the estimate won't arrive. You could pass the probe status down and show nothing, or a short "size unknown" line, when it is `error`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:100 · github-actions[bot] · 2026-11-25T21:53:39Z

| 👮 **Wachiman** | The test replaces the shared \`startFileDrag\` stub and never puts it back |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`window.electronAPI` is created once in test/setup.ts:109. This test assigns `window.electronAPI.startFileDrag = vi.fn()` directly, so the mock carries over into every later test in the file. The sibling test does `vi.spyOn(window.electronAPI, "startFileDrag")` and then `mockRestore()` (export-status-cards.test.tsx:143,152). Use the same pattern here.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:791 · github-actions[bot] · 2026-11-25T21:53:39Z

| 👮 **Wachiman** | "Send to…" survives only on the Library cards, so the same action now has two names |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The recording page renames the core action to "Export a copy" (`exportCopy`, used at library-detail-page.tsx:439). The Library's icon buttons still label it `sendTo` ("Send to…"), at video-row.tsx:119-120 and video-card.tsx:121-122. So the same Prepare entry point is called "Send to…" on the list and "Export a copy" one click later. If the rename is meant to apply everywhere, switch those two components to `exportCopy` and drop `sendTo`. If the split is intended, update prepare-screen.md:117, which still describes the Library button as "Send to…" with no note about the split.

<!-- wachi:finding -->
