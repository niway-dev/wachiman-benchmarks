# kaipu-bench-wachi-v3#89 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | Enter-to-export ignores open dialogs, but the arrow-key handler skips them |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`destinationStep` returns null inside `[role='dialog']` (line 364). `isPrimaryEnter` has no matching check. It only skips fields, buttons and links. While the Change video / Pick from Library panel is open (`role="dialog"`, video-picker.tsx:69-71), focus can land on a non-button element: the empty-list `<p>`, or the body after a click inside the panel. Enter then starts an export of the selected destination behind the open list. The same applies to any other dialog the shell shows over Export. Adding `if (target.closest("[role='dialog']")) return false;` would make Enter behave like the arrows. When `document.activeElement` is the body, closing the picker first would also work.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:112 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | Library detail paths are built by hand, with no encoding |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`/library/${v.assetId}` is hard-coded here and again at line 162. Everywhere else in this file paths come from `ROUTES` (`ROUTES.exportNew`), and `exportPath` encodes the asset id (`encodeURIComponent`, prepare-path.ts:13). Building these from `ROUTES.libraryDetail` with the id encoded would keep both links in step with the route table.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | Dropping a file on the Library now navigates the whole app window to that file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Library used to mount `useFileDrop`, which calls `preventDefault` on window `dragover`/`drop`. Its own doc comment says why that matters: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:9-11`). This PR removes that call. The only remaining caller is `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which is mounted only on Export. Nothing else intercepts drops: no other renderer code listens for `dragover`/`drop`, and the main process sets only `setWindowOpenHandler` with no `will-navigate` guard (`main/index.ts:400-403`). So if a user drags an MP4 onto the Library, which is where they used to drop videos until now, Chromium's default runs and loads `file:///…mp4` in the main window. The app UI is replaced and there is nothing to navigate back with. Step 12 of the PR's test plan says "dropping a file there does nothing", but nothing in the code makes that true. Fix: keep a window-level guard that swallows file drops on screens that don't import (for example in the shell, or `will-navigate` + `preventDefault` in main), or keep `useFileDrop` on the Library with a handler that sends the files to Export.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:201 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | 1440p/4K and Fill/Fit radiogroups don't respond to arrow keys |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

Both segmented controls declare `role="radiogroup"` with `role="radio"` buttons (lines 201-217 and 233-248), but they have no key handling and no roving `tabindex`. `destinationStep` in `export-page.tsx:363` skips arrows inside any non-card radiogroup because such a group "answers its own arrows". These groups don't, so ←/→ on a focused 1440p/4K or Fill/Fit radio does nothing, and each option is a separate Tab stop. Screen readers announce a radio group, which tells users the arrows should work. Either handle ←/→ in these groups (move `aria-checked` and focus), or drop the radio roles and use plain toggle buttons with `aria-pressed`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | The running-export part of the Export badge has no test |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`useExportBadge` now adds 1 while `status === "exporting"`, and the label changed to "# copy in progress or ready" to cover it. `sidebar.test.tsx` only drives `noteFinishedCopy` and never puts the runner into `exporting`. Nothing pins the in-progress count, or the way it combines with the ready-card exclusion when the export finishes (exporting → idle with `ready` set, `export-runner.ts:462`). Also, the test named "is active on Export with and without a video" (`sidebar.test.tsx:39`) only renders `/export/asset-1`, so it never checks bare `/export`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | Library drop test passes while a dropped file makes Electron navigate the window away from the app |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This test checks only that `importVideoFiles` is not called. It ignores the return value of `fireEvent.drop`, which tells whether anything called preventDefault.

After this PR, `useFileDrop` is mounted only through `usePrepareImport` on Export (`features/prepare/use-prepare-import.ts:55`, `pages/export/export-page.tsx:85`). The Library page no longer listens for drops at all.

The hook's own comment explains why that matters: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`). Main has no `will-navigate` guard either: `main/index.ts:400-411` only sets `setWindowOpenHandler`, and searching for `will-navigate` finds nothing.

So dropping an MP4 on the Library now replaces the app UI with the file. Before this PR, the same drop imported the file. A copy exporting in the background in the renderer ("Runs in the background") is lost along with the page.

This test names the behaviour as intended ("does not take a video dropped") and stays green.

Suggested fix, in two parts:
- Keep a window-level drop guard while the Library is mounted. It could forward the drop to Export or just refuse it.
- Make this test assert `expect(fireEvent.drop(...)).toBe(false)`, the same way `dropFiles` does in `export-page.test.tsx:416`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | "with and without a video" only checks the with-a-video URL |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. The case without a video (`/export`, `ROUTES.exportNew`) is the one that depends on the NavLink's `to` matching exactly, and it is never checked for `aria-current`. The link is `ROUTES.exportNew` with no `end` (`sidebar.tsx:53`), so both cases do work today. A future `end: true` would break the `/export/:assetId` case, and only half of what the title claims is pinned. Add `renderAt(ROUTES.exportNew)` with the same assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:48 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | The "in progress" half of the new badge is untested |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The badge is now `running + libraryBadgeCount(...)` (`sidebar.tsx:121-122`), and its label says "copy in progress or ready" (`en.json:946`). Every test here only calls `noteFinishedCopy`, so no test covers the export that is still running, which the new label and count were added for. This includes whether it still badges while Export itself is open: `running` is counted on every page, unlike the finished copies. A test that mocks `useExportRunner` with `status: "exporting"` would cover it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | Leftover comment for the removed \`.importZone\` rule |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The `.importZone` rule was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits right on top of the `.stickyBar` comment, so it reads as if it described the sticky bar. Delete line 108.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:3 · github-actions[bot] · 2026-11-26T17:04:31Z

| 👮 **Wachiman** | Comment calls 900 × 670 the default window size; it is the minimum |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment says the stage is sized so YouTube's card and the button fit "the default 900 × 670 window". The `main` preset (`apps/kaipu-record/src/shared/window-size.ts:50`) opens at 1040 × 760, and 900 × 670 is its `minWidth`/`minHeight`. Saying "the smallest 900 × 670 window" would describe the constraint correctly.

<!-- wachi:finding -->
