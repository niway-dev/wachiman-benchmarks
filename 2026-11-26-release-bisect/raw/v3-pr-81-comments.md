# kaipu-bench-wachi-v3#81 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-26T06:30:11Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Enter-to-export skips fields and buttons but not dialogs, unlike the arrow keys (confidence low)**

The keydown listener runs on the whole document (line 299), so Enter counts as "export" whenever `isPrimaryEnter` says yes. `destinationStep` ignores events from inside `[role='dialog']` (line 364), but `isPrimaryEnter` never checks for a dialog. On a non-button target inside a dialog drawn over Export, such as a `role="radio"` button or a focusable that isn't a button, Enter starts an encode behind the dialog. Within this part, the VideoPicker's dialog only holds buttons, so it is safe today. Consider adding the same `target.closest("[role='dialog']")` check here.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T06:30:11Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: A file dropped on the Library now falls through to Electron's default and replaces the app with the file (confidence medium)**

This change removes `useFileDrop` from the Library. The only remaining caller is `usePrepareImport`, which only Export mounts (`features/prepare/use-prepare-import.ts:55`). Nothing else in the renderer calls `preventDefault` on `dragover`/`drop`: `use-file-drop.ts:25-56` is the only window-level handler. The main process has no `will-navigate` guard either: `main/index.ts` sets only `setWindowOpenHandler` at line 400. With no handler, Electron's default for a file dropped on a BrowserWindow is to load that file in the window. The renderer loses the React app and its in-memory state, and the user has to reload. The PR body says that on the Library "dropping a file there does nothing", but it also says the app was not run in Electron. Suggested fix: keep a window-level `dragover`/`drop` `preventDefault` outside Export, either app-wide in the renderer or as a `will-navigate` block in main. That restores "does nothing" on the Library and on every other screen.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-26T06:30:11Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: An Email export changes to "Slack · Discord" in Recent exports once it finishes (confidence high)**

While the job runs, the row uses `running.destination` (line 50), which is `email` for an Email export. Once the file lands, the finished row gets its destination from `destinationOfPreset(copy.export!.preset)`, and for `balanced` that returns `chat` (`features/prepare/destinations.ts:69-71,102-107`). So the same export shows as "Email · anywhere" at some percentage, then as "Slack · Discord". The PR accepts that `destinationOfPreset("balanced")` returns `chat`, but here the strip contradicts itself. Possible fixes: persist the job's destination with the copy, or label a `balanced` copy neutrally in this strip.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T06:30:11Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: Library no longer intercepts file drops, so dropping a file there takes the window to that file; the new test hides this (confidence medium)**

This PR removes the Library's only drag/drop handling. After it, `useFileDrop` is mounted only through `usePrepareImport` on Export (`features/prepare/use-prepare-import.ts:55`, `pages/export/export-page.tsx:85`). No other `dragover`/`drop` listener exists in `apps/kaipu-record`, and no `will-navigate` guard exists in `src/main/index.ts` (around lines 400-411, only `setWindowOpenHandler`). The repository describes the result itself. `use-file-drop.ts:10-11` says that "a file dropped where nothing handles it makes Electron navigate the window to that file", and `export-page.test.tsx:414-416` checks for this with `!fireEvent.drop(...)`.

So on the Library, a file dragged from Finder does not "do nothing" as the PR body says (step 12). The main window navigates away from the app to the file. Any work the renderer holds is lost with it, including a running background export, which `usePrepareCopy` documents as living in the renderer and surviving page changes (`use-prepare-copy.ts:89-91`). The author says the app was not run in Electron.

This test checks only that `importVideoFiles` is not called. It ignores the return value of `fireEvent.drop`, so it passes either way and reads as proof that the drop is harmless.

Suggested fix: keep a window-wide guard on the Library that calls `preventDefault` on `dragover`/`drop` for file drags and does not import. A no-op `useFileDrop(() => {})` would also work. Then assert in this test that the drop was prevented, as `dropFiles` does in `export-page.test.tsx:416`. Before turning this into an app-wide guard, check the record and editor pages: they had no guard before this PR either, which is outside this change.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T06:30:11Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "with and without a video" only checks the URL with a video (confidence high)**

The test is named "is active on Export with and without a video", but it renders only `/export/asset-1` (line 40). The no-video URL is `/export` (`ROUTES.exportNew`), which is also the NavLink's own `to` (`sidebar.tsx:53`), and it is never asserted here. The badge's new `running` term (`sidebar.tsx:121`, "in progress" in the label) is not covered either: every badge test uses only `noteFinishedCopy`. To match the name, add `renderAt(ROUTES.exportNew)` with the same `aria-current` assertion. A case with the export runner in `exporting` would cover the in-progress count.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T06:30:11Z

👮 **Wachiman** · Nit · 🟡🧹 **Consider · cleanup: Orphaned comment for the removed `.importZone` rule (confidence high)**

This change removes the `.importZone` rule but leaves its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar."). The comment now sits directly above the `.stickyBar` comment and describes a strip the Library no longer has. Delete line 108.

<!-- wachi:finding -->
