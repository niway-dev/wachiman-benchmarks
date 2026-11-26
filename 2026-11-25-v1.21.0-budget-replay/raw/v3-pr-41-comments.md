# kaipu-bench-wachi-v3#41 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:40 · github-actions[bot] · 2026-11-25T23:56:55Z

| 👮 **Wachiman** | "Pick from Library" stays enabled while an import runs |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

"Browse files…" is disabled while `importing` (line 51), but the Library picker trigger is not. If someone picks a Library video while a dropped or browsed file is still importing, `openVideo` navigates to `/export/<picked>`. Then `usePrepareImport`'s `onImported` finishes and navigates again to the imported video (`use-prepare-import.ts:48`), so the screen jumps away from the video they chose. Disabling the picker trigger while `importing`, as the Browse button already is, avoids that.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-25T23:56:55Z

| 👮 **Wachiman** | Enter-to-export does not skip dialogs, but the arrow handler does |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`destinationStep` ignores events whose target is inside `[role='dialog']` (line 364). `isPrimaryEnter` only skips fields, buttons and links. So if focus sits on something non-interactive inside a dialog, Enter starts an export behind the dialog. That happens with the Change video panel (`video-picker.tsx:69-75`, `role="dialog"`) after a click on its empty-state text or padding, or with any other app dialog. Adding the same `target.closest("[role='dialog']")` guard here would make the two handlers agree.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T23:56:55Z

| 👮 **Wachiman** | A file dropped on the Library now hits Chromium's default and can navigate the app window away |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Library no longer calls `useFileDrop`. That hook was what called `preventDefault()` on `dragover` and `drop` across the window (`features/library/hooks/use-file-drop.ts:25-51`). I searched `src/main` and found no `will-navigate` guard, so nothing else stops Chromium's default. When a file is dropped on a page that doesn't handle it, Chromium opens the file in the window. Dropping an MP4 on the Library, which is the screen users are most likely to drop onto out of habit, would then replace the app UI with a bare video player, with no way back. The PR says "dropping a file there does nothing", and that only holds if something still suppresses the default. Two ways to make it true: a cheap window-level `dragover`/`drop` `preventDefault` in the shell for screens that don't import, or a `will-navigate` guard on the main window. Either one would also cover every other screen.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-25T23:56:55Z

| 👮 **Wachiman** | Library drop test passes even though Electron opens the dropped file in the main window |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This test only checks that `importVideoFiles` was not called. Nothing now catches a file drop on the Library. `useFileDrop` was the window-level handler that called `preventDefault` (`features/library/hooks/use-file-drop.ts:40-47`), and after this PR its only caller is `usePrepareImport`, which only Export mounts (`pages/export/export-page.tsx:85`). The main process has no `will-navigate` guard either: `main/index.ts:400-403` only sets `setWindowOpenHandler`.

So when a user drops a video on the Library, the old place to bring a video in, Electron's default runs and the main window navigates to the file. The app UI is replaced by the file viewer, and anything in the session is lost. The comment at `use-file-drop.ts:10-11` warns about exactly this. The test name says the Library "does not take" the drop, but it would pass either way.

Fix: keep a window-level drop guard while the Library (or the whole shell) is mounted, for example `useFileDrop` with a toast pointing to Export, or a `will-navigate` block in main. Then have this test assert that `fireEvent.drop` returns false, as `dropFiles` does in `export-page.test.tsx:416`. I could not run Electron to watch it navigate, which is why confidence is medium.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-25T23:56:55Z

| 👮 **Wachiman** | "with and without a video" only renders /export/asset-1 |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. The bare `/export` case (`ROUTES.exportNew`), which is the NavLink's own `to`, is never checked for `aria-current`. Add `renderAt(ROUTES.exportNew)` with the same assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:10 · github-actions[bot] · 2026-11-25T23:56:55Z

| 👮 **Wachiman** | The no-video Export screen has nothing that scrolls in a short window |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`.wrap` no longer has `overflow-y: auto`. It keeps `flex: 1; min-height: 0`, and it sits directly in `.screen`, which has `overflow: hidden` (export-page.tsx:103-113, export-page.module.css:15). Next to it are a fixed header and the `flex-shrink: 0` Recent exports panel (recent-exports.module.css:3). When the window is too short, `.wrap` shrinks below the zone's content. The dashed zone then spills over the Recent exports panel and gets clipped by `.screen`, with no way to scroll to its buttons. Only the screen with a video gets its own scrolling `.stage`, so the page comment ("the stage scrolls on its own") does not cover this state. If the reason is the Library picker, one option is to make the picker escape the clipping some other way (a portal or fixed positioning) and keep a scroll box here.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-25T23:56:55Z

| 👮 **Wachiman** | Orphaned comment for the removed drop strip |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The `.importZone` rule was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still here. It now sits right above the toolbar's sticky-bar comment, so it reads as if it describes the toolbar. Delete it along with the rule.

<!-- wachi:finding -->
