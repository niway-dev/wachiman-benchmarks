# kaipu-bench-wachi-v3#96 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:338 · github-actions[bot] · 2026-11-26T17:32:03Z

| 👮 **Wachiman** | Email and Chat are indistinguishable once a copy exists |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Email shares chat's `balanced` preset (destinations.ts:69-71), and 'Ready' is keyed on the preset alone: `reusable[presetForDestination(d, probe, youtube)]` (line 338), and again for `existing` at line 251. After one balanced copy is exported, both the Chat and Email cards show 'Ready'. Enter on Email then opens the existing copy instead of exporting, which is the same behaviour as Chat. The library side maps the stored preset back with `destinationOfPreset` (recent-exports.tsx:65, master-copies-panel.tsx:67), which always answers 'chat', so a copy exported for Email is labelled and iconed as Chat. The `destination` passed through `usePrepareCopy` only affects the live progress and ready cards, and is not persisted. This is a visible inconsistency, not data loss, and may be the intended 'same file' trade-off. If it is, say so on the Email card or in the backlog doc.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:95 · github-actions[bot] · 2026-11-26T17:32:03Z

| 👮 **Wachiman** | Retrying a video that failed to probe may bounce straight back out |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

When the probe fails, the effect at lines 95-99 toasts and navigates to `/export`. `/export` and `/export/:assetId` both render `<ExportPage />`, so the component instance, and with it `useSourceProbe`'s `{id, probe}` state, probably survives that navigation. I have not confirmed that react-router reuses the instance across sibling routes here. Picking the same video again would then render once with `state.id === videoId` and status `error` (use-prepare-copy.ts:66), before the probe effect resets it to loading. The error effect would fire again with the stale value. The user would get a second 'Couldn't read' toast and be bounced out without the file being re-probed. Does a retry of the same video work on the first pick? Clearing the probe state when `videoId` becomes null would avoid the stale value.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T17:32:03Z

| 👮 **Wachiman** | A video dropped on the Library now makes Electron navigate the window to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Before this change the Library mounted `useFileDrop`, which listens on `window` and calls `preventDefault` on `dragover` and `drop` for file drags. That is what stopped Electron's default of navigating to the dropped file. This diff removes the hook and the drop zone, and the page now has no drop handling. A user who drags a video from Finder or Explorer onto the Library, which used to import it, now gets the default. `use-file-drop.ts:10-12` says as much: a drop where nothing handles it navigates the window to that file. I found no guard in main: the only handler in `main/index.ts` is `setWindowOpenHandler` (line 400), and there is no `will-navigate` handler. The renderer would be replaced by a bare file view, which also discards in-renderer state such as a running background export (the runner lives in the renderer). The comment on line 53 says outside videos come in through Export, but a user dropping on the Library has no way to know that. Fix: keep a drop target on the Library that does nothing but swallow the drag (or redirect to `/export`). A main-side `will-navigate` guard would also work.

Other routes, such as the recording detail and the editor, never handled drops, so this problem was already there. The change newly exposes it on the one screen where users were told to drop files.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:122 · github-actions[bot] · 2026-11-26T17:32:04Z

| 👮 **Wachiman** | Library-named badge pieces are now Export-only; one i18n key is orphaned |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The rail badge moved from Library to Export. `libraryBadgeCount` (ready-copies.ts:70) is still named after the Library and is now only called here at line 122. The `backgroundCopy.libraryBadge` message in en.json and es.json (line 1487) has no remaining reader, because the badge label now comes from `export.railBadge`. Rename the helper, e.g. to `railBadgeCount`, and drop the dead key. `libraryChip` is still used by library-page.tsx:139.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T17:32:04Z

| 👮 **Wachiman** | Dropping a video on Library now falls through to Electron's default (navigate to the file); the test only checks that nothing is imported |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Library used to mount the drop hook, which called `preventDefault` on dragover and drop. The `useFileDrop` docstring says the reason: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-14`). `LibraryPage` no longer mounts it (`pages/library/library-page.tsx:53`). Now `useFileDrop` is only used through `usePrepareImport`, which only Export mounts, so nothing handles the drop on Library. A search of `src` found no `will-navigate` guard. `main/index.ts:400` only sets `setWindowOpenHandler`. Library is where users keep their videos, so a video dropped there by habit would replace the app with the file. The page and any export running in the renderer would be lost until a reload. The new test `does not take a video dropped on the window` only asserts `importVideoFiles` was not called, so it passes in exactly that situation. Either keep a guard on Library that calls `preventDefault` on file drags and perhaps toasts "drop it on Export", or add an app-wide guard. In either case assert the result of the drop. `dropFiles` in `export-page.test.tsx:410-417` shows how: it returns `!fireEvent.drop(...)`, which is true only when a listener called `preventDefault`. Other pages (Editor, Settings) were already unguarded before this PR. I did not check whether anything outside `src` guards navigation.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T17:32:04Z

| 👮 **Wachiman** | Test says "with and without a video" but only covers the with-video route |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "is active on Export with and without a video" but renders only `/export/asset-1`. The sidebar's NAV entry points at `ROUTES.exportNew` (`/export`) and relies on `matchPath` with `end: false` (sidebar.tsx:53, 68-69) to light up on `/export/:assetId`. The bare `/export` case is the one that isn't asserted. Add a second `renderAt(ROUTES.exportNew)` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:59 · github-actions[bot] · 2026-11-26T17:32:04Z

| 👮 **Wachiman** | Badge coverage dropped: running copy and "finishes while Library is open" are no longer tested |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The old test "a copy that finishes while the Library is open never badges" was replaced by a navigate-to-Library test, which is a different path. In `useExportBadge`, `onLibrary` also calls `announceReadyCopies()` from the effect on `[pathname, copies]` (sidebar.tsx:118-119), so a copy finishing while the Library is already open is cleared by that effect. Nothing now asserts this. The badge also adds `running = status === "exporting" ? 1 : 0` (sidebar.tsx:121), and the new label "copy in progress or ready" depends on it, but no test drives `useExportRunner` into `exporting`. Both are new or changed behaviour of the rail badge with no assertion.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T17:32:04Z

| 👮 **Wachiman** | Orphaned comment for the removed drop strip |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The comment `NIW2-579: the "Drop a video here" strip, between the header and the toolbar.` now sits right above the `.stickyBar` comment, because the `.importZone` rule below it was deleted. The strip no longer exists in the Library, so the comment describes nothing. Delete line 108.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:3 · github-actions[bot] · 2026-11-26T17:32:04Z

| 👮 **Wachiman** | "Default 900 × 670 window" is the minimum, not the default |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`WINDOW_PRESETS.main` in `src/shared/window-size.ts:50` is `1040 × 760` with `minWidth: 900` and `minHeight: 670`. So 900 × 670 is the smallest size the window can take, which is a good size to design the stage for. Calling it the default misstates the sizing basis. Say "the minimum 900 × 670 window".

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/index.mdx:33 · github-actions[bot] · 2026-11-26T17:32:04Z

| 👮 **Wachiman** | Prepare backlog rows and docs still describe a screen that is deleted |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This PR deletes the Prepare screen. `/prepare` now only redirects, and the Library no longer takes drops. Yet the two Prepare rows (index.mdx:33-34) and their docs, backlog/prepare-screen.md and backlog/prepare-drop-zone.md, still carry the "🟢 Ready to validate" banners and describe the Prepare UI and the Library drop strip as live. The new doc says it "replaces Prepare" but does not mark the old ones as superseded. Add a short "Superseded by Export" banner to both docs and update their index rows, so a reader or QA pass does not validate behaviour that no longer exists.

<!-- wachi:finding -->
