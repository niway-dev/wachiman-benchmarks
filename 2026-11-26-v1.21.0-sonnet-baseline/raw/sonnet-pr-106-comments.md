# kaipu-bench-wachi-v3#106 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:71 · github-actions[bot] · 2026-11-26T17:36:40Z

| 👮 **Wachiman** | Email copies are stored as "balanced" and read back as Chat everywhere else |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Email shares chat's preset (`balanced`), and the library only records the preset, not the destination. The Export screen passes `destination: plan.destination` (`export-page.tsx:258`), so the progress and ready cards say "Email". After that, every reader that goes from the preset to a destination answers "chat": `destinationOfPreset` in `recent-exports.tsx:65` and in `master-copies-panel.tsx:67-68`. Those two places label and badge an Email copy as Chat. The same sharing makes the Email card show "Ready" when only a Chat copy exists (`export-page.tsx:338`), and the other way round. Pressing Enter on Email then opens the existing Chat copy instead of encoding one (`export-page.tsx:262-265`). If that is the intent, nothing needs to change. If not, the destination has to be stored with the copy, or Email needs its own preset.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:212 · github-actions[bot] · 2026-11-26T17:36:40Z

| 👮 **Wachiman** | The destination picked on screen is not written to the URL |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The picked destination lives in `useState` (line 212) and the `chosen` ref (line 77). The URL keeps only the `?to=` it arrived with. `onOpenExisting` (line 162) navigates to the Library, so Back remounts `ExportScreen` with `initialDestination` read from the URL. If the page was opened without `?to=`, the user is back at "Where is it going?" and the pick is lost. Calling `setSearchParams({ to }, { replace: true })` in `select` would keep it across Back and reload. This is the author's call: the screen may be meant to start fresh each visit.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T17:36:40Z

| 👮 **Wachiman** | A video dropped on the Library window is no longer caught, so Electron navigates to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Library used to mount `useFileDrop`, which listens on `window` for `dragover` and `drop` and calls `preventDefault()`. Its own doc comment says why: "a file dropped where nothing handles it makes Electron navigate the window to that file". This PR removes that call, and no other non-test code in the renderer registers a window-level drop handler. `usePrepareImport` is the only other caller, and Export is the only page that uses it. I also found no `will-navigate` guard in `apps/kaipu-record/src/main/index.ts`, which only sets `setWindowOpenHandler`. The Library was the screen that told users to drop videos, so dropping one there now replaces the app with the raw video file. The app cannot be used again until it is reloaded. Mount a drop guard (for example `useFileDrop` with a handler that sends the user to Export), or add a `will-navigate` guard in the main window.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:201 · github-actions[bot] · 2026-11-26T17:36:40Z

| 👮 **Wachiman** | \`role="radio"\` buttons answer no arrow keys, though \`destinationStep\` assumes they do |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The 1440p / 4K control and the Fill / Fit control are plain `<button role="radio">` elements inside a `radiogroup`. They have no `onKeyDown`, no roving `tabIndex` and no arrow handling. `destinationStep` in export-page.tsx:363 returns null for arrows pressed inside a radiogroup, and its comment says those groups "answer their own arrows". They do not, so Left and Right do nothing there, and a keyboard user can only move between options by tabbing. The role also promises arrow navigation to screen readers. Either add arrow handling to these segmented controls, or let `destinationStep` handle them. Alternatively, use native `input type=radio` elements.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-26T17:36:40Z

| 👮 **Wachiman** | A finished Email copy is listed as "Slack · Discord" |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`destinationOfPreset(copy.export!.preset)` loses the destination. Email shares the `balanced` preset with chat, and `destinationOfPreset` is documented in destinations.ts:12-13 to answer "chat" for it. A copy exported for Email is therefore shown in Recent exports with the chat logo and the name "Slack · Discord". While it is running, the row uses `running.destination`, so it reads correctly, and it changes label once the copy is saved. Nothing tells the user. The label could be more neutral for `balanced` copies, or the destination could be stored with the export.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T17:36:40Z

| 👮 **Wachiman** | Library now leaves a dropped file to the platform default, and the test only pins that nothing is imported |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Library used to mount `useFileDrop`, which calls `preventDefault` on `dragover` and `drop`. Its own comment (`use-file-drop.ts:10-11`) says that a file dropped where nothing handles it makes Electron navigate the window to that file. After this change the only mounts of `useFileDrop` are inside `usePrepareImport`, which only Export uses. I found no `will-navigate` guard under `apps/kaipu-record/src/main`. A video dropped on Library therefore navigates the window to the file, and the app UI is gone until a reload. This test asserts only `importVideoFiles` was not called, so it passes either way and does not show the drop is harmless. Does something outside this part, such as a main-process guard or a global handler, stop the navigation? If not, consider keeping a drop guard (preventDefault, with no import) on Library, and make the test assert that `fireEvent.drop` returns false.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:285 · github-actions[bot] · 2026-11-26T17:36:40Z

| 👮 **Wachiman** | Enter test claims "from the page or a card" but only fires on a card |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The only keydown in this test is on the YouTube card (line 288). Enter on the page body with a destination selected is never exercised. Line 165 covers only the "nothing picked" case. `isPrimaryEnter` has a separate `!target` and body path, so the "page" half of the title is untested. Fire `Enter` on `document.body` here as well, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T17:36:40Z

| 👮 **Wachiman** | Test name says "with and without a video" but only covers the with-video route |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test renders only `/export/asset-1` and asserts `aria-current`. The no-video route (`ROUTES.exportNew`, `/export`) is registered in `renderAt` but never checked for the active state. Add a second `renderAt(ROUTES.exportNew)` assertion, or rename the test to match what it checks.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T17:36:41Z

| 👮 **Wachiman** | Orphaned comment for the removed drop strip |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The PR deleted `.importZone`, but the comment above it (`NIW2-579: the "Drop a video here" strip, between the header and the toolbar`) is still here. It now sits directly above the `.stickyBar` comment and describes nothing. Remove it.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:881 · github-actions[bot] · 2026-11-26T17:36:41Z

| 👮 **Wachiman** | New \`prepare.lineEmail\`, \`sayEmail\` and \`whyEmail\` keys are never read |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The only consumer of `DESTINATION_COPY` is `master-copies-panel.tsx:68`, which reads `.name`. `GROUP_COPY` has no readers at all. So `lineEmail`, `sayEmail` and `whyEmail` (en and es) are dead on arrival; only `destEmail` is used. Export reads its own `export.*` keys (`cardEmail`, `sentence*`). Drop the three keys, or drop the `line`, `say` and `why` fields, together with the older keys they pair with (`whyYoutube` and the rest, `groupSendMoreWhy` and the rest, `whyBigger`, `whySmaller`, `whyKeep`). Also dead after this PR: `prepare.dropChooseFile` and `prepare.dropFromLibrary`, whose only caller was the deleted Prepare drop zone. A grep of `apps/kaipu-record/src` finds no use.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/index.mdx:33 · github-actions[bot] · 2026-11-26T17:36:41Z

| 👮 **Wachiman** | Prepare backlog rows and docs still describe the removed Prepare screen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Prepare rows at lines 33-34 still read as live work ("full-screen Prepare replaces the Share sheet", "drop anywhere on Prepare"). They link to `prepare-screen.md` and `prepare-drop-zone.md`, which have no superseded note pointing at `export-screen`. `background-copy-toasts.md:36` still says the badge sits on LIBRARY, but `export-screen.md` says it moved to EXPORT. The Prepare page, drop zone and destination list are deleted in this PR. Mark those rows and docs as replaced by Export, or fold them in, so readers don't validate a screen that no longer exists.

<!-- wachi:finding -->
