# kaipu-bench-wachi-v3#87 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:281 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | Enter on a destination card does nothing while no destination is selected |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The document keydown listener calls `preventDefault()` on every Enter that `isPrimaryEnter` accepts. That includes Enter on a card, because cards are `button[role='radio']` (`destination-row.tsx:63-76`) and line 384 lets radios through. The comment says this stops the card from clicking itself. When `selected` is null, though, `primary()` returns at line 263 without doing anything. So a keyboard user who tabs to the first card (the tab stop, `destination-row.tsx:73`) and presses Enter gets no result: the card is not selected and nothing exports. Space and the arrow keys still select. One option is to let the card's click run, or to call `select` on the focused card, when `plan` is null.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:212 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | Selected destination is lost after opening an existing copy and coming back |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`selected` starts from `?to=` (line 212). After that it lives only in component state and in the `chosen` ref (line 77), and the URL is never updated. When a card shows Ready, `primary()` opens that copy with `navigate('/library/…')` (line 162). Pressing Back remounts `ExportPage` and `ExportScreen` under the same history entry. `chosen` is then null again and `selected` goes back to the URL value, which is "Where is it going?" if the screen was opened without `?to=`. Writing the selection into `?to=` with `setSearchParams(..., { replace: true })` would keep it across Back.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | A file dropped on the Library now navigates the app window to that file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The PR removes `useFileDrop` from the Library and says that "dropping a file there does nothing". That isn't what happens. `useFileDrop` was what called `preventDefault()` on `dragover`/`drop` across the whole window. Its own doc comment says why: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-11`, `:29-46`). After this change, the only caller is `use-prepare-import.ts:55`, which is mounted only on Export. The main process has no `will-navigate` guard (`main/index.ts:400` only sets `setWindowOpenHandler`), so nothing else stops it.

The Library was the screen that took drops until now, so users are trained to drop files there. Doing that now replaces the whole renderer with the MP4: the rail, any running export (it runs in this renderer) and all UI state are gone, and nothing explains why.

Fix: keep a window-level guard that calls `preventDefault` on file `dragover`/`drop` outside Export. Either install it once at the app shell, or add `will-navigate` prevention in main. Optionally, show a toast pointing the user to Export.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:297 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | GitHub's size bar is scaled to 10 MB but labelled "Original N MB" |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

For GitHub, `scale` is `max(copyBytes, GITHUB_FREE_LIMIT_BYTES)`, so the bar's full width means 10 MB. The label on the left is still `barOriginal` ("Original {size}", line 316), so it reads as if the full width is the recording. With a 40 MB recording and an 8 MB copy, the bar is 80% full next to "Original 40 MB", which looks like 32 MB. Consider labelling the bar's end "10 MB limit" for GitHub, or drawing a limit marker.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | Library no longer stops a dropped file from navigating the window, and this test locks that in |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Before this PR, Library mounted the import drop zone, which used `useFileDrop`. That hook calls `preventDefault` on window `dragenter`/`dragover`/`drop` (`use-file-drop.ts:25-42`). Its doc says why: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`use-file-drop.ts:10-11`). After this PR, the only caller of `useFileDrop` is `usePrepareImport` (`use-prepare-import.ts:55`), which is mounted only by Export. The main process has no `will-navigate` guard either: a search of `src/main` for `will-navigate`/navigation handling finds only `setWindowOpenHandler` (`main/index.ts:400`).

The result: dragging a video from Finder onto the Library window, which used to import it, now replaces the app's page with the file. That throws away the renderer state, including a background export running in the renderer. This test only checks that `importVideoFiles` is not called. It does not check what happens to the drop, so it passes while the window navigates away. The new Export test checks exactly this case (`export-page.test.tsx:414-416`).

The check is also synchronous. If `importDropped` reaches `importVideoFiles` after an `await`, the assertion would pass even if the import ran.

Fix: keep a window-level drop guard while Library (or the whole shell) is mounted. It can refuse the drop, or redirect to Export, but it must call `preventDefault`. Then assert here that `fireEvent.drop` returns false, as the Export test does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | "with and without a video" only checks the with-video URL |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test's name says the Export link is active on Export both with and without a video, but it only renders `/export/asset-1`. The case with no video, `/export` (`ROUTES.exportNew`), is never asserted, even though it is the link's own target. Add a second `renderAt(ROUTES.exportNew)` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:48 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | The "in progress" half of the Export badge is not exercised |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`useExportBadge` now adds 1 when the export runner's `status === "exporting"` (sidebar.tsx:121-122), and the badge label reads "copy in progress or ready". These tests only produce finished copies through `noteFinishedCopy`. Nothing checks that a running export adds to the count, or that it keeps counting while Export is open, where the finished copies are cleared. A test that drives the runner into `exporting` would pin that behaviour.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | Orphaned comment for the removed \`.importZone\` rule |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The `.importZone` rule was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there, right above the `.stickyBar` comment. It now reads as if it describes the sticky bar. Delete line 108.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/index.mdx:33 · github-actions[bot] · 2026-11-26T17:03:31Z

| 👮 **Wachiman** | The Prepare backlog rows still read 🟢 even though Export replaces that screen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The new row (line 35) and `export-screen.md` both say Export *replaces* Prepare, and the Prepare page and its drop zone are deleted in this PR. The rows for "Prepare — where is your video going?" (line 33) and "Prepare: drop a video from outside" (line 34) still say 🟢 Ready to validate, with owner QA pending, and nothing points at Export. Someone doing QA from this table would go looking for a screen that no longer exists. Consider noting "superseded by Export" on those rows, or folding them into the new one.

<!-- wachi:finding -->
