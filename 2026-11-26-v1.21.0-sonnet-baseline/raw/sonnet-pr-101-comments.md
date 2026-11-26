# kaipu-bench-wachi-v3#101 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:251 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | "Ready" / Enter-opens-existing ignores Fill vs Fit for TikTok · Reels and LinkedIn · Feeds |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`existing` is `reusable[plan.target.presetId]` (and the card badge at line 338 does the same). `findReusableExports` matches only on preset and `encodeFingerprint("whole", preset)` (`export-reuse.ts:74`), and `ENCODE_REVISION` has no entry for `vertical` or `square` (`export-presets.ts:177-182`). The Fill/Fit choice is passed to the encoder (`use-prepare-copy.ts:115`) but is not part of the fingerprint. So after a Fill copy is exported, switching the Shape to Fit still shows the card as Ready. The primary action and Enter then open the Fill copy instead of encoding Fit, with no sign that the shape differs. "Export again" is the only way to get Fit. Fix by including the framing in the fingerprint or the reuse match for these two presets. If the old Prepare page had the same behaviour, this carries it over; the Export screen now advertises it on every card. I could not check the deleted `prepare-page.tsx`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | Library no longer catches window file drops; Electron's default now navigates the window to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Library page used to mount `useFileDrop`, which preventDefaults dragover/drop on the whole window. It is removed here (line 53 is now just a comment), and nothing else on this screen handles a drop. `use-file-drop.ts:9-11` says why that matters: "a file dropped where nothing handles it makes Electron navigate the window to that file". Nothing in `main/index.ts` stops it either: the only navigation hook is `setWindowOpenHandler` (line 400), with no `will-navigate` guard. A user who drags a video onto the Library, which used to show a drop zone there, now replaces the whole app window with the raw file. The user can only get back by reloading, and anything the renderer held, such as a recording in progress, is gone. Other pages such as Settings and the editor were already unguarded. The Library was the page people were taught to drop on, so this is a new exposure. Fix: keep a drop guard here, either `useFileDrop` redirecting to `navigate(exportNewPath())` or a plain preventDefault, or add a `will-navigate` guard in the main process.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:69 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | Picker is a \`role="dialog"\` with no focus handling |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The panel opens as `role="dialog"` but focus stays on the trigger. Items are not focused on open, and focus does not return to the trigger after Escape or a pick. A keyboard user opens the list and then has to Tab through the page to reach it, while `destinationStep` in export-page.tsx:364 already treats the dialog as its own keyboard scope, so the arrows do nothing there. Either move focus to the first item on open and back to the trigger on close, or drop the `dialog` role and use a disclosure pattern (`aria-expanded` plus a plain list).

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:3 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | A video dropped on the Library page is no longer caught, so Electron navigates the window to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useFileDrop` is the only handler that calls `preventDefault` on window `dragover` and `drop`. Its own comment (`use-file-drop.ts:10-11`) says a file dropped where nothing handles it makes Electron navigate the window to that file. Before this PR the Library page mounted it through the drop zone. The PR removes that wiring: `library-page.tsx` no longer references `useFileDrop`, and `ImportDropZone` and its test are deleted. The only remaining caller is `usePrepareImport`, mounted by `pages/export/export-page.tsx:85`. I found no `will-navigate` guard in `src/main`; the only navigation hook there is `setWindowOpenHandler` (`main/index.ts:400`).

So a user who still drops a clip on the Library (the old import door) replaces the app UI with the raw file until they reload. That is a regression on a page that used to handle the drop. The Library now says "Outside videos come in through Export" only in a code comment, not to the user.

Suggested fix: keep a drop guard on the Library (and ideally app-wide, e.g. a `will-navigate` handler in main or a global `useFileDrop` that redirects to Export), or confirm the Library change is intended and add a test for what a drop there does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:105 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | Comment says Export "points at the copies", but the Export page never reads the unseen-copy state |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment on `useExportBadge` says opening Export or the Library clears the finished ones because "both point at the copies". Only the Library does that: `library-page.tsx:61-63` uses `useReadyCopies` and `unseenCopyIds` for its chip and outlines. Nothing under `pages/export/` reads them (a grep for `unseenCopyIds` and `useReadyCopies` outside the sidebar and Library finds nothing there). So opening Export clears the rail badge for copies that Export never highlights. The copies stay unseen, so the Library chip still appears, but the badge is gone without the user having been shown them. The header of `ready-copies.ts` ("the Library page is open") and the name `libraryBadgeCount` are stale in the same way. Either have Export outline or announce the copies, or only announce on the Library and correct the comment.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | Dropping a file on the Library now falls through to Electron's default navigation, and the test pins that |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Before this PR the Library page mounted `useFileDrop`, which listens on `window` and calls `preventDefault` on every file drop. The hook's own comment (`use-file-drop.ts:10-11`) says a file dropped where nothing handles it makes Electron navigate the window to that file. The PR removes the Library drop zone, so `/library` has no handler now. The only `useFileDrop` callers left are Export's `usePrepareImport` and `ExportDropZone`. I found no `will-navigate` or `dragover` guard in `src/main/index.ts` or anywhere else under `src`. A user who drops a video on the Library, the screen they used before, now loses the app UI to a bare file view in the window. This test, `does not take a video dropped on the window`, only asserts that `importVideoFiles` was not called. It never checks `defaultPrevented`, so it passes while the window still navigates.

Fix: add a window-level guard on the pages that have no drop target. For example, a shell-level `dragover`/`drop` `preventDefault` for file drags, or `will-navigate` blocking in main. Then assert `defaultPrevented` in this test. If that is already handled elsewhere, point to it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | Test name says "with and without a video" but only checks one URL |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test only renders `/export/asset-1`, so the no-video route (`ROUTES.exportNew`, `/export`) is never checked for `aria-current`. The rail item points at `ROUTES.exportNew`, so `/export` is the case where `end: false` matters most. Add a second `renderAt(ROUTES.exportNew)` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | The "copy in progress" half of the Export badge has no test |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useExportBadge` in `shell/sidebar.tsx` adds 1 to the count while `status === "exporting"`. The badge label says "in progress or ready", but every test here only drives `noteFinishedCopy`. A test with `useExportRunner` in the exporting state would cover the new meaning of the badge. The prepare-page tests deleted in this part did not cover it either.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:882 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | New prepare.lineEmail/sayEmail/whyEmail are never read; most of the old prepare namespace is dead too |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`DESTINATION_COPY` (`features/prepare/destination-copy.ts`) is read in one place, `master-copies-panel.tsx:68`, and only for `.name`. Nothing reads `.line`, `.say` or `.why`, so `lineEmail`, `sayEmail` and `whyEmail` (en.json 882-884, same in es.json) are dead as soon as they are added. The Export screen uses `export.sentence*` instead. `GROUP_COPY` (`destination-copy.ts:25`) has no consumer. The keys only the deleted Prepare page used also remain in both locale files: `pageTitle`, `pageSubtitle`, `back`, `notPreparable*`, `group*Label`, `anotherTitle/Hint`, the `change*`, `why*`, `meter*`, `tag*`, `prepareAction*`, `prepareAgain`, `dropTitle/Body/Active/ChooseFile/FromLibrary` and others. Only `dropMoreInLibrary` and `dropImporting` (the latter is not read either; Export has its own) survive in the files I searched. Drop the dead keys, or the `line`/`say`/`why`/`GROUP_COPY` fields and the matching Email strings, so translators don't maintain copy nobody sees.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | Orphaned comment left after removing .importZone |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The `NIW2-579: the "Drop a video here" strip` comment used to label `.importZone`. That rule is now deleted, so the comment sits on top of the `.stickyBar` comment and describes a strip that no longer exists. Delete it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:3 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | Comment calls 900 × 670 the default window; it is the minimum |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`WINDOW_PRESETS.main` in `shared/window-size.ts:50` is 1040 × 760 by default, with `minWidth: 900, minHeight: 670`. The stage is sized against the smallest window the user can reach, not the default one. Reword the comment ("the smallest 900 × 670 window") so nobody tunes the layout for the wrong size.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/index.mdx:35 · github-actions[bot] · 2026-11-26T17:36:08Z

| 👮 **Wachiman** | Prepare backlog docs and rows still present Prepare as a live feature |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This PR deletes the Prepare page and its drop zone, and `export-screen.md` says Export replaces them. The rows for `prepare-screen` (line 33) and `prepare-drop-zone` (line 34) still read "🟢 Ready to validate · owner QA pending", and neither linked doc (`prepare-screen.md:8`) has a note that Export superseded it. Someone reading the backlog would validate a screen that no longer exists. Add a "Superseded by Export" banner to both docs and update their index rows, or fold their lasting parts into `export-screen.md`.

<!-- wachi:finding -->
