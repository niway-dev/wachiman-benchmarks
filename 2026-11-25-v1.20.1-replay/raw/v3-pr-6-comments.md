# kaipu-bench-wachi-v3#6 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-25T21:50:40Z

| 👮 **Wachiman** | Enter can start an export while the Change video list is open |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`destinationStep` ignores arrow keys whose target is inside `[role='dialog']` (line 364), but `isPrimaryEnter` has no matching check. The Change video picker is a `role="dialog"` panel (video-picker.tsx:69-75). Its own keydown listener only handles Escape (video-picker.tsx:50-52). Suppose the list is open and focus is on `body`, which happens after clicking the panel's padding or its empty-state text. Pressing Enter then reaches `keys.current.primary()` and starts encoding the current video behind the open list. Consider returning false when no dialog is open is not the case, i.e. when `target.closest("[role='dialog']")` matches, or when any picker is open, as `destinationStep` already does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T21:50:40Z

| 👮 **Wachiman** | A file dropped on the Library now opens in place of the app |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Library used to call `useFileDrop`. That hook catches `dragover` and `drop` on the whole window, and its own comment says why: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-11`). This PR deletes the hook from the Library. I found no other listener and no `will-navigate` guard in `src/` (the main process sets only `setWindowOpenHandler`, `main/index.ts:400`). So a video dragged from Finder onto the Library now loads in the window and the renderer is gone. That includes any export the renderer's runner is doing at that moment. The PR's test step 12 says "dropping a file there does nothing", which this code does not do. To keep the Library from importing while still stopping the default, add a small window-level listener that only calls `preventDefault()` on file drags, or block file navigations in the main process with `will-navigate`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-25T21:50:40Z

| 👮 **Wachiman** | "does not take a video dropped on the window" passes even if Library still imports drops |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This test no longer mocks `window.electronAPI.pathForFile`, and the line that did (`pathForFile = vi.fn((f) => `/Users/me/Movies/${f.name}`)`) was removed. The global default in `src/renderer/src/test/setup.ts:156` is `pathForFile: () => ""`. When `importDropped` gets an empty path, it puts the file in `skipped`, shows the "Only videos can be imported" toast and returns before calling `importVideoFiles` (`features/library/hooks/use-import-videos.ts:102-111`). So `expect(importVideoFiles).not.toHaveBeenCalled()` holds whether or not LibraryPage still listens for drops, and the test can't catch a regression. To fix it, put back `window.electronAPI.pathForFile = vi.fn((f: File) => `/Users/me/Movies/${f.name}`)` in this test, as `export-page.test.tsx:421` does. Optionally, also assert that `fireEvent.drop` returned true (nothing called preventDefault) or that no "Only videos" toast appeared. With either check, a hook that is still mounted would make the test fail.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-25T21:50:40Z

| 👮 **Wachiman** | Orphaned comment for the removed \`.importZone\` rule |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The `.importZone` rule was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits right above the `.stickyBar` comment, so it reads as if it describes the sticky bar. Delete line 108.

<!-- wachi:finding -->
