# kaipu-bench-wachi-v3#31 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:40 · github-actions[bot] · 2026-11-25T23:00:06Z

| 👮 **Wachiman** | "Pick from Library" stays enabled while an import runs |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

"Browse files…" is disabled while `importing` is true (line 51), but the VideoPicker trigger is not. If someone picks a Library video during a drop or import, the page opens on that video. When the import then finishes, `usePrepareImport`'s `onImported` calls `navigate(preparePath(first.assetId, to))` (features/prepare/use-prepare-import.ts:48), which moves them off the video they just picked and onto the imported one. One fix is to disable the trigger while `importing`, the same way Browse files is disabled.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-25T23:00:06Z

| 👮 **Wachiman** | Enter-to-export skips dialogs less carefully than the arrow keys do |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

`destinationStep` ignores events from inside `[role='dialog']` (line 364). `isPrimaryEnter` does not, so an Enter pressed in any dialog on a non-button element (for example the VideoPicker panel, which is `role="dialog"`) starts an export from the document-level listener. Today the picker's items are buttons, so they are excluded. Adding the same `[role='dialog']` check to `isPrimaryEnter` would make the two consistent and keep a future dialog from exporting by accident.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T23:00:07Z

| 👮 **Wachiman** | A file dropped on the Library now navigates the app window away |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Before this change the Library called `useFileDrop`, which runs `preventDefault()` on window `dragover`/`drop` (`features/library/hooks/use-file-drop.ts:29-51`). This PR removes that call. In the renderer, that hook was the only thing handling drops (a search for `"drop"`/`ondrop` finds only it), and `src/main/index.ts` has no `will-navigate` guard. When a drop is not prevented, Chromium/Electron's default is to load the dropped file in the BrowserWindow. So an MP4 dragged onto the Library replaces the whole app UI with a bare video player, and there is no rail to get back. The PR says "dropping a file there does nothing", which is not what happens. Fix: keep a window-level handler that prevents `dragover`/`drop` outside Export, or block navigation in main with `will-navigate`. Either one also covers the other screens.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-25T23:00:07Z

| 👮 **Wachiman** | A file dropped on Library is now left to Electron's default, which loads the file into the app window |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This test covers the Library after its drop zone was removed. It only checks that `importVideoFiles` is not called (line 86). Before this PR, the Library's window-wide `useFileDrop` called `preventDefault` on `dragover` and `drop`. Now the only caller of `useFileDrop` is `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which only Export mounts. The main process does not guard navigation either: `main/index.ts:400-403` sets a window-open handler but adds no `will-navigate` listener.

So when a user drops a video on the Library (where it used to be imported), Chromium's default runs: the main window navigates to `file:///…/clip.mp4`, and the app UI is replaced by the media file with no error.

The test passes while that happens. Two fixes: keep a `preventDefault`-only drop guard on the shell (or Library), or block `will-navigate` in main. Then make this test check what `dropFiles` in `export-page.test.tsx:416` checks, `expect(fireEvent.drop(...)).toBe(false)`, so it actually covers "does not take a video dropped on the window".

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-25T23:00:07Z

| 👮 **Wachiman** | "with and without a video" only renders the with-video URL |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. The `/export` case (`ROUTES.exportNew`, the link's own target) is never checked here. It also only works because `isActive` in `sidebar.tsx:68-69` uses `end: false` for the Export entry. Rendering `ROUTES.exportNew` in the same test and checking `aria-current` there too would make the test cover what its name says.

<!-- wachi:finding -->
