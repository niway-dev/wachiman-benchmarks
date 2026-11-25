# kaipu-bench-wachi-v3#26 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:98 · github-actions[bot] · 2026-11-25T22:59:38Z

| 👮 **Wachiman** | The unreadable-file redirect drops the destination picked on screen |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

When the probe fails, the page navigates to `exportNewPath(urlDestination)`. It does not use `current()`, the helper that `openVideo` (line 87) and `usePrepareImport` call to carry the destination over. So a destination chosen on screen (stored in `chosen.current`) is lost, while Change video and a drop would have kept it. In practice the probe runs before `ExportScreen` mounts, so `chosen` is usually null at this point. It is not null when a dropped or changed video fails to probe after the user picked a card on the previous video: `chosen` is reset by the `assetId` effect, and the URL then carries the destination. If this path is meant to behave like the others, pass `current()`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:112 · github-actions[bot] · 2026-11-25T22:59:38Z

| 👮 **Wachiman** | Library detail paths are hard-coded and not encoded, unlike the Export paths |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`navigate(`/library/${v.assetId}`)` here and at line 162 builds the path by hand. Next to it, `exportPath` and `LegacyPrepareRedirect` (line 171) build theirs from `ROUTES.*` and pass `assetId` through `encodeURIComponent`. `ROUTES.libraryDetail` exists to stop this kind of drift (routes.ts:4-7). Using `ROUTES.libraryDetail.replace(":assetId", encodeURIComponent(...))` would match the rest of the file.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T22:59:38Z

| 👮 **Wachiman** | A file dropped on the Library now navigates the app window to that file, not "nothing" |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This PR removes `useFileDrop` from the Library. Nothing else in the renderer now calls `preventDefault` on `dragover`/`drop` on that screen. `use-file-drop.ts:8-11` states the consequence itself: "a file dropped where nothing handles it makes Electron navigate the window to that file". The main process has no `will-navigate` guard to stop it (`src/main/index.ts:400-411` sets only a `setWindowOpenHandler`).

The Library is where users have been dropping videos up to now (NIW2-579). After this change, the same drop replaces the whole renderer with the dropped MP4. That unloads the app UI, and with it the renderer-side export runner and any copy still exporting. The user gets no message. The PR's test step 12 ("dropping a file there does nothing") is not what the code does.

Possible fixes: keep a window-wide drop guard that only calls `preventDefault`, mounted at the shell or Library level. Or keep `useFileDrop` on the Library and send the files to Export. A `will-navigate` handler in main that denies navigation away from the app URL would also cover every other screen.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117 · github-actions[bot] · 2026-11-25T22:59:38Z

| 👮 **Wachiman** | Badge is cleared on /export/:assetId, a screen that does not list finished copies |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`matchPath({ path: ROUTES.exportNew, end: false })` matches `/export/:assetId` too, so `announceReadyCopies()` runs on the per-recording Export screen. The effect also re-runs whenever `copies` changes (line 120), so any copy that finishes while the user is there is announced straight away. But `RecentExports`, the list that shows finished copies, only renders on `/export` with no asset (`pages/export/export-page.tsx:101-113`). The per-recording screen does not navigate away after a copy starts (no `onStarted` navigation in `export-page.tsx`), so the user is still on it when the copy finishes. If they close or hide the ready card, that copy never shows up in the rail badge, and it never appeared in a list on that screen either. The doc comment says Export clears finished copies because it "points at the copies", which is only true for `/export`. Possible fix: use `end: true` for the Export match, as the Library match already does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:85 · github-actions[bot] · 2026-11-25T22:59:38Z

| 👮 **Wachiman** | Dropping a file on the Library now hands the drop to Electron, which opens the file in place of the app, and the new test accepts that |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This PR removes the Library's drop zone. After that, `useFileDrop` is only used through `usePrepareImport` on Export (`features/prepare/use-prepare-import.ts:55`). It is the only listener in the renderer that calls `preventDefault` on `dragover`/`drop` (`features/library/hooks/use-file-drop.ts:29-47`). Main does not guard navigation either: there is no `will-navigate` handler, and only `setWindowOpenHandler` at `main/index.ts:400`.

So when a user drops a video or PDF on the Library, or on any screen other than Export, Chromium's default runs and the main window navigates to the file:// URL. The app UI is replaced by the bare file until a reload. Before this PR the Library took the drop, so this is the screen where users already drop files.

The new test `does not take a video dropped on the window` only checks that `importVideoFiles` was not called. It ignores the result of `fireEvent.drop`, which the Export tests use at `export-page.test.tsx:416` for exactly this reason ("Electron does not navigate the window to the file"). As written, the test locks in the window being navigated away.

Fix: keep an app-wide handler, for example in the shell, that calls `preventDefault` on file `dragover`/`drop` outside Export. A gentle toast pointing to Export would help too. Then assert here that `fireEvent.drop(...)` returns `false`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:86 · github-actions[bot] · 2026-11-25T22:59:38Z

| 👮 **Wachiman** | The "no import" check runs before any async import could start |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The test checks `importVideoFiles` synchronously, right after the drop. The old import path called it asynchronously (the removed test needed `waitFor`), so a drop handler that came back would still pass this test. Also, `pathForFile` is not stubbed here any more. Awaiting a tick, or a `waitFor` on a negative with a short timeout, before the assertion would make the test meaningful.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:497 · github-actions[bot] · 2026-11-25T22:59:38Z

| 👮 **Wachiman** | The several-videos test never checks that all three files were imported |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "all are imported", but it only asserts the navigation to the first video and the toast. Unlike the single-file test at line 471, it never checks that `importVideoFiles` received all three paths. Adding `expect(window.electronAPI.importVideoFiles).toHaveBeenCalledWith([...three paths])` would make it test what its name says.

<!-- wachi:finding -->
