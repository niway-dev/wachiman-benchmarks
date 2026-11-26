# kaipu-bench-wachi-v3#116 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/app/router.tsx:66 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Library no longer handles window file drops, so a video dropped there makes Electron navigate to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This PR removes the Library's `useFileDrop`/`ImportDropZone`. The PR body says dropping a file on the Library "does nothing". `useFileDrop`'s own comment (`features/library/hooks/use-file-drop.ts:10-11`) says the opposite: a file dropped where nothing calls `preventDefault` makes Electron navigate the window to that file. The only remaining `useFileDrop` caller is `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which is mounted only by `ExportPage`. I found no `will-navigate` guard or window-level drop handler in `apps/kaipu-record/src` (`main/index.ts:400` only sets `setWindowOpenHandler`). A video dropped on the Library, a common place for it, will probably replace the app UI with the raw file and lose the renderer state. Before this PR the Library caught that drop. I did not check Electron's runtime behaviour, and the PR says the app was not run. Fix: a global drop guard (`dragover`/`drop` `preventDefault` for file drags) or a `will-navigate` handler in main, instead of relying on Export being mounted. The fix would live in the Library page and main, outside this part; I report it here because this is where the Library route changes.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:98 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Unreadable-file redirect drops the destination picked on screen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

When the probe fails, the redirect uses `exportNewPath(urlDestination)`. It ignores `current()`, which prefers the destination chosen with the cards (`chosen.current`). The unreadable-file case sends the user to `/export?to=<URL destination>`, not the one they had picked. The probe finishes before the stage is shown, so in practice no card has been picked yet, and the impact is small. Using `current()` would keep this redirect consistent with `openVideo` (line 87) and the drop-import path.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:156 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | \`?? []\` creates a new array on every render and defeats the \`useMemo\` on \`exports\` |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | ⚡ perf |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`lineage.exportsOf.get(video.assetId) ?? []` is a new array each render when the recording has no exports. `reusable` in `ExportScreen` (line 236) is memoized on `[exports]`, so it is recomputed on every render in that case. The cost is small. A module-level `const NO_EXPORTS: readonly LibraryVideo[] = []` fixes it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:359 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Arrow keys move the destination from anywhere outside inputs, radio groups and dialogs, including a focused sidebar link |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

`destinationStep` only skips inputs, content-editable elements, other radio groups and dialogs. A Left or Right arrow with focus on a sidebar link, or on any other focusable that uses arrows itself (tablist, menu, slider that is not an `<input>`), changes the selected destination and calls `preventDefault`. `isPrimaryEnter` already excludes `a[href]` and buttons. Consider scoping arrows to the row or to the body/stage focus. If other widgets must answer arrows, exclude their roles as well.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | A file dropped on the Library now navigates the window to that file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Library no longer calls `useFileDrop`, which was the only thing on that page calling `preventDefault` on `dragover` and `drop` (`use-file-drop.ts:29-47`). The hook's own comment says what happens without it: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`use-file-drop.ts:10-12`). The main process has no `will-navigate` guard. The only `webContents` handlers are `before-input-event`, `render-process-gone` and `setWindowOpenHandler` (`main/index.ts:379-400`). So on the Library, dropping a video or image now replaces the app UI with the browser's file view, and the user has to reload to get back. The PR's test step 12 says "dropping a file there does nothing", and that does not hold. The Library is also where people drag videos from Finder, so the mistake is likely, and nothing tells the user what happened. Pages that never used the hook were already exposed. The Library was protected, and this PR removes that protection. Fix: keep a drop guard that only calls `preventDefault`, either on the Library or once at the app shell. Alternatively, deny `will-navigate` to non-app URLs in the main process.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Finished Email exports show up as Chat in Recent exports |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The finished rows derive the destination with `destinationOfPreset(copy.export!.preset)`. Email shares the `balanced` preset, and `destinationOfPreset("balanced")` returns `chat` (`destinations.ts:102-107`), so an Email copy appears with Chat's logo and name. The running row does it correctly, using `running.destination ?? …` (line 50). The PR body mentions that both cards show "Ready", but not this. The same file can be labelled differently while it is running and after it finishes. Persisting the destination with the export, or labelling `balanced` neutrally, would remove the mismatch. Otherwise, document it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.test.tsx:6 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Library page no longer catches dropped files, so a video dropped there navigates the window away |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Before this PR the Library page called `useFileDrop` (via the deleted `ImportDropZone` wiring) and its `drop` handler called `preventDefault`. The only remaining `useFileDrop` callers are `pages/export/export-page.tsx` and `export-drop-zone.tsx` (through `usePrepareImport`). No other `drop` or `dragover` listener exists in `apps/kaipu-record/src`, and `main/index.ts` has no `will-navigate` handler (only `setWindowOpenHandler`, line 400). `use-file-drop.ts:10-11` documents the default: a file dropped where nothing handles it makes Electron navigate the window to that file. A user who drags a video onto the Library, where the old drop zone used to be, now loses the app UI and any in-memory state (the export runner, ready copies). `library-page.tsx:53` says outside videos come in through Export, but nothing keeps a drop on the Library from hitting the platform default. Fix: keep a `preventDefault`-only guard on Library, or use `useFileDrop` there to redirect the drop to Export. A `will-navigate` guard in main would also cover Record and Settings, which have the same exposure today. I did not read why Record and Settings were left unguarded, so I am not recommending a change to them here.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:105 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Comment says Export 'points at the copies', but the Export page does not use the unseen-copy state |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The doc comment says opening Export or the Library clears the finished ones because "both point at the copies". Only `library-page.tsx:61-63` reads `unseenCopyIds`. `pages/export/recent-exports.tsx` lists the newest three exports and does not read `useReadyCopies`/`unseenCopyIds`, and nothing on Export calls `markCopySeen`. Visiting Export clears the rail badge through `announceReadyCopies()` (line 119), while the Library chip and outline stay until the copy is opened. That may be intended, but the comment should say it. Also, `backgroundCopy.libraryBadge` (en.json and es.json, line 1487) now has no caller, since the sidebar uses `export.railBadge`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | A video dropped on Library is no longer handled, and the test asserts only that nothing is imported |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Before this change, Library mounted `useFileDrop`, which calls `preventDefault` on `drop` and so stops Electron navigating the window to the file (`features/library/hooks/use-file-drop.ts:40-47`). Now only `usePrepareImport` in `ExportPage` mounts it (`pages/export/export-page.tsx:85`). Library, Editor, Settings and the other pages have no drop handler. The main process has no `will-navigate` guard either; `main/index.ts` only sets `setWindowOpenHandler`. A user who drops a video on Library, the old import door, probably gets the window navigated to the raw file with the app gone until reload. The new test `does not take a video dropped on the window` only checks that `importVideoFiles` was not called. It does not check `fireEvent.drop`'s return value, so it passes whether or not the default is prevented, and it does not pin what should happen instead. Decide what a drop outside Export should do: for example a window-level guard that prevents the default, or a `will-navigate` block in main. Then assert that here the way `export-page.test.tsx` does with `dropFiles(...)`. If navigation is accepted, drop the test or rename it so it doesn't read as intended behaviour.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Test says "with and without a video" but only renders /export/asset-1 |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test name claims Export is active both with a video (`/export/:assetId`) and without (`/export`), but it only calls `renderAt("/export/asset-1")`. The bare `ROUTES.exportNew` case is not asserted, so a regression in the `/export` match would pass. Add a second `renderAt(ROUTES.exportNew)` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Badge's "in progress" half is not covered |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The label is "N copies in progress or ready", and `useExportBadge` (sidebar.tsx:121-122) adds 1 when `useExportRunner().status === "exporting"`. Every test here only drives `noteFinishedCopy`; none puts the runner in the exporting state. If the running term breaks, or double-counts with the ready card's asset, nothing fails. Add a case with a running export, including the one where it finishes and its ready card is on screen.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:884 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | New prepare.lineEmail/sayEmail/whyEmail keys have no reader; most of the prepare namespace is now dead |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This PR adds `destEmail`, `lineEmail`, `sayEmail` and `whyEmail` (and the same in es.json). Only `DESTINATION_COPY[d].name` is read anywhere (`features/prepare/components/master-copies-panel.tsx:68`). The `line`, `say` and `why` fields, and the whole of `GROUP_COPY` in `features/prepare/destination-copy.ts`, have no consumer now that `destination-detail.tsx` and `destination-list.tsx` are deleted. So three of the four new keys are written, translated and never shown. Many older `prepare.*` keys are orphaned by the same deletions: `pageSubtitle`, `back`, `changesCard`, `whyCard*`, `prepareAction*`, `anotherTitle`, `meterOriginal`, `soundStudio`, `dropChooseFile`, `dropFromLibrary` and others. The new `export` namespace duplicates several of them (`uploadSizeTitle`, `cropNote`, `openExisting`, `originalEditsNote`, `reading`). Drop the dead keys and the unused `DESTINATION_COPY` fields and `GROUP_COPY`, in en and es together, so the messages do not keep two vocabularies for one screen.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Orphan comment left where \`.importZone\` was removed |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The `.importZone` rule is deleted, but its comment (`NIW2-579: the "Drop a video here" strip, between the header and the toolbar`) stays. It now sits directly above `.stickyBar`, whose own comment follows it, and it describes a strip the Library no longer has. Delete the line.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/index.mdx:34 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Prepare backlog rows still present the removed Prepare screens as live |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The `prepare-screen` row (line 33) and the `prepare-drop-zone` row (line 34) still say 🟢 Ready to validate and link to docs that describe the Prepare screen, its drop zone and the Library strip. This PR deletes those screens and `export-screen.md` says Export replaces them. Neither doc gets a 'superseded by Export' banner. The CLAUDE.md status rule is to fold lasting knowledge into a reference doc and drop the row once validated. Someone doing owner QA from these rows would test UI that no longer exists. Mark both superseded and point them at `export-screen`, or merge them into it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/video-picker.module.css:54 · github-actions[bot] · 2026-11-26T20:09:00Z

| 👮 **Wachiman** | Keyboard focus on a picker item looks the same as hover |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`.item:hover` and `.item:focus-visible` share one rule with `outline: none`. The only focus cue is the faint `--bg-card-hover` background, and it is also what `.item[aria-current="true"]` competes with. Every other focusable control in the Export CSS, such as `.segment:focus-visible` (export-stage.module.css:151), draws an accent outline. Keep an outline on `:focus-visible` so keyboard users can see where they are in the list.

<!-- wachi:finding -->
