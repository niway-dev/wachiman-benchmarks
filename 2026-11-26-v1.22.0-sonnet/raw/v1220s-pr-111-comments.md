# kaipu-bench-wachi-v3#111 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119 · github-actions[bot] · 2026-11-26T20:04:40Z

| 👮 **Wachiman** | Email copies get the generic "export" title on the progress and ready cards |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The Export screen now passes `destination: "email"` through here, and `job.destination` reaches `destinationArg(job)` in `status-cards/export-status-cards.tsx:55-56`. That value feeds the ICU `select` in `videoEditor.progressTitle` and `readyTitle` (`packages/i18n/messages/en.json:1474,1480`, `es.json:1474,1480`). The select only has the cases youtube, vertical, square, github, chat and archive, plus `other`. `email` falls into `other`, so an Email export shows "Preparing your export…" and "Your export is ready" instead of naming the place. The new `destination` doc comment (line 74-76) says the cards name the destination, which is not true for Email. The fix is to add an `email {…}` case to both messages in en.json and es.json, for example "copy for email".

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:112 · github-actions[bot] · 2026-11-26T20:04:40Z

| 👮 **Wachiman** | Library detail URL is hard-coded instead of built from ROUTES |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Lines 112 and 162 navigate to `/library/${assetId}` as a template literal, without `ROUTES.libraryDetail` and without `encodeURIComponent`. `exportPath` in `prepare-path.ts` builds its URL from `ROUTES` and encodes the id, and `routes.ts:4-8` says literal paths drift silently. Build these two URLs the same way, with `ROUTES.libraryDetail.replace(":assetId", encodeURIComponent(id))`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:98 · github-actions[bot] · 2026-11-26T20:04:40Z

| 👮 **Wachiman** | Unreadable-file redirect drops a destination picked on screen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The probe-error redirect keeps `urlDestination` (`?to=`) only. The screen's other exits (`openVideo` and the drop import) use `current()`, which prefers `chosen.current`. If the user picks a card on the previous video and then changes to a video whose file cannot be read, the destination they picked is lost on the redirect to `/export`. Using `current()` here would keep it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | A video dropped on the Library now navigates the window to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Library used to call `useFileDrop`, which listens on `window` and calls `preventDefault` on `dragover` and `drop`. Its own comment says a file dropped where nothing handles it "makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:9-11`). The only remaining caller is `usePrepareImport`, which only the Export page uses (`features/prepare/use-prepare-import.ts:55`). A search of `src/main` finds no `will-navigate` guard. So a user who drops a video on the Library, the screen that used to take drops, now replaces the app UI with the file until they reload. Either keep a no-import window drop guard on the Library (for example `useFileDrop` with a handler that navigates to Export, or only `preventDefault`), or add a `will-navigate` guard in the main process. I did not check the Home or Editor pages, which may already have this problem; the Library is the one this PR changes.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:111 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | Keep card says "sound as recorded" even when the recording has no audio |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`keepPicture` always reads "{width} × {height} · sound as recorded · {size}" (`packages/i18n/messages/en.json:927`). `plan.sound` can be `"none"` when the source has no audio (`features/prepare/destinations.ts:209-210`). The removed `ChangesCard` showed `soundNone` for that case. Text that claims sound for a silent recording is misleading. Pick the line from `plan.sound`, or drop the clause when it is `"none"`. The same removal means `plan.smoothness` (the frame-rate cap) is no longer shown anywhere on the screen.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | The new "in progress" half of the Export badge has no test |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`useExportBadge` now adds 1 while `status === "exporting"`. `sidebar.test.tsx` only covers finished copies (`noteFinishedCopy`). Nothing drives `useExportRunner` to "exporting", so the running count, its sum with the unseen count, and the "in progress" accessible label are unpinned. Add a case that mocks the runner as exporting and expects `1`, then one with an unseen copy as well and expects `2`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:66 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | Message keys orphaned by this change |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The rail no longer reads `backgroundCopy.libraryBadge` (the `tCopy` hook is removed). It is still defined at `packages/i18n/messages/en.json:1487` and in es.json, and no ts/tsx under `apps/` references it. The deleted Prepare components also leave `prepare.anotherTitle`, `anotherHint`, `groupPostLabel`, `groupSendLabel`, `groupKeepLabel`, `dropFromLibrary`, `listUpTo` and `notPreparableTitle` unreferenced in code, apart from DESTINATION_COPY's key strings. Remove the keys from en.json and es.json, or confirm the Export screen reuses them.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | Test pins that a file dropped on Library is ignored, but nothing stops Electron from opening it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useFileDrop` is now only used by `usePrepareImport`, so only Export mounts it (`use-prepare-import.ts:55`). Its own comment says why it listens on the window: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`use-file-drop.ts:10-11`). The main process has no `will-navigate` or similar guard (searched `apps/kaipu-record/src/main`). The Library page used to catch the drop. After this change a video dropped on Library, which is where users have been told to drop videos, probably navigates the app window to the file. The test asserts only that `importVideoFiles` is not called, so it passes either way. Consider asserting that the drop's default is prevented (`fireEvent.drop` returns false, as `dropFiles` does in the Export test). If it isn't prevented, add a navigation guard or a window-level handler that swallows file drops. Whether the old behaviour was already missing on other screens (Home, Editor) is outside this part.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | Test name claims "with and without a video" but only checks the with-video route |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test renders `/export/asset-1` only. The `/export` (no video) case, which is the route the rail link points at (`ROUTES.exportNew`), is never asserted active. Add a second `renderAt(ROUTES.exportNew)` assertion or narrow the name.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:32 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | The badge's new "copy in progress" half has no test |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`useExportBadge` (sidebar.tsx:111-123) adds `running = status === "exporting" ? 1 : 0` to the finished-copy count, and the label is now "copy in progress or ready". Every badge test here only exercises `noteFinishedCopy`. A running export lighting the badge, and the on-screen ready card being excluded, are untested.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/destination-row.module.css:55 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | Keyboard focus outline is clipped by the row's scroll box |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`.row` has `overflow-x: auto; overflow-y: hidden` with only 3px of padding, sized for the 3px selected ring. `.card:focus-visible` (line 84-87) draws a 2px outline with a 2px offset, so it extends 4px and is clipped by 1px on the top, bottom and edge cards. Since the row is keyboard-driven (arrow keys, one tab stop), increase the padding/negative margin to at least 5px, or use `outline-offset: 0`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T20:04:41Z

| 👮 **Wachiman** | Stale comment left where the drop-strip rule was removed |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The `.importZone` rule is gone, and its comment ("NIW2-579: the \"Drop a video here\" strip, between the header and the toolbar") now sits directly above the `.stickyBar` comment and rule. It describes a strip the Library no longer has and reads as if it documented `.stickyBar`. Delete the line.

<!-- wachi:finding -->
