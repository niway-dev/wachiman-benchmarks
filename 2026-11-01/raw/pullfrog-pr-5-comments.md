=== COMMENT 4437318211 apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53
With `useFileDrop` gone, no route other than Export calls `preventDefault` on `dragover`/`drop`. A video dropped on the Library now makes Electron navigate the window to `file://…/clip.mp4` and replaces the app. `use-file-drop.ts` documents exactly this, and `main/index.ts` has no `will-navigate` guard. The Library used to absorb this. The new test at `library-page.test.tsx:80-87` only checks that nothing was imported, so jsdom can't catch it.

<details><summary>Technical details</summary>


````markdown
# Unhandled file drops navigate the Electron window

## Affected sites
- apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53: the Library no longer mounts any window drop handler.
- apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80-87: asserts `importVideoFiles` was not called, but not that the drop was `defaultPrevented`.
- apps/kaipu-record/src/main/index.ts: no `will-navigate` handler on `mainWindow.webContents`.

## Required outcome
- Dropping a file on the Library (or any non-Export route) leaves the app where it is, with no navigation to the file.
- A test asserts the drop is `defaultPrevented` on the Library.

## Suggested approach
- Add an app-wide guard that `preventDefault`s file `dragover`/`drop` at the shell level, or block file navigation in main with `webContents.on("will-navigate", …)`. Then the Library (and Record/Editor) are safe without importing anything.
````

</details>

=== COMMENT 4437318217 apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108
This comment described the `.importZone` rule removed just above it. It now sits orphaned on top of `.stickyBar`'s own comment.

```suggestion

```

