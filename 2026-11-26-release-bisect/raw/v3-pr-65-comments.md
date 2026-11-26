# kaipu-bench-wachi-v3#65 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:119 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Email copies are announced as "Preparing your export…", not as an email copy (confidence high)**

The new `destination` input (lines 73-77) exists so that the progress and ready cards can name Email, since it shares chat's `balanced` preset. `export-page.tsx:258` passes `"email"`, and `export-runner.ts:314` stores it on the job. But `export-status-cards.tsx:134/186` feeds it into the ICU `select` in `progressTitle`/`readyTitle` (`packages/i18n/messages/en.json:1474,1480`, same in es.json), and that select has no `email` branch. So an Email copy shows the Mail logo and the title "Preparing your export…" / "Your export is ready". Every other destination gets a title that names it. Add an `email {…}` case to both messages in both locales so the comment's intent actually holds.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A file dropped on the Library now opens the file in the app window instead of doing nothing (confidence medium)**

This change removes `useFileDrop` from the Library, and the Library was the only thing that called `preventDefault` on `dragover`/`drop` there (`features/library/hooks/use-file-drop.ts:49-51`). The main window does not stop a dropped file either: `main/index.ts:400-411` sets only a `setWindowOpenHandler`, and the repo has no `will-navigate` handler (a search of `src/main` found none). That leaves Chromium's default in place: when an MP4 is dropped on the Library, the main window navigates to the file's `file://` URL. The app UI goes away, and the renderer is replaced, along with anything running in it, including the background export runner (`features/video-editor/export/export-runner.ts`). The PR body says "dropping a file there does nothing", which is not what happens. Two possible fixes: keep a window-level `dragover`/`drop` `preventDefault` on screens that don't import, or block file navigation in main with `webContents.on('will-navigate', e => e.preventDefault())`. Either way, add a Library test that checks a drop is prevented. I could not confirm this in Electron because the app was not run, so it rests on the platform default.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:201 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: The YouTube 1440p/4K and Fill/Fit radio groups ignore the arrow keys (confidence high)**

These groups use `role="radiogroup"`/`role="radio"`, and `destinationStep` in `export-page.tsx:363` deliberately ignores arrows inside them, because such a group "answers its own arrows". Neither group here has an arrow handler, though. Each radio is a separate Tab stop, and ←/→ on it does nothing. Either add roving ←/→ selection (with `tabIndex` only on the checked radio), or use plain toggle buttons with `aria-pressed` so they don't claim radio behaviour. The same applies to the Fill/Fit group at line 233.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:111 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: The Keep card says "sound as recorded" even for a silent recording (confidence high)**

`keepPicture` always reads "… · sound as recorded · {size}". `planCopy` already knows when the recording has no audio (`plan.sound === "none"`, `features/prepare/destinations.ts:209-210`), and the Prepare detail this replaces showed `soundNone` in that case. For a silent recording, consider a variant without the sound clause.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:69 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: The picker is a `role="dialog"` but focus never moves into it or back to the trigger (confidence medium)**

When the picker opens, focus stays on the trigger. Escape and a click outside unmount the panel, but focus is never returned to the trigger. A keyboard user has to Tab into an unlabelled position to reach the list. And if focus was inside the list when Escape is pressed, focus falls back to `body`. Consider moving focus to the current or first item when the picker opens, and back to the trigger when it closes, or use a listbox/menu pattern instead of `dialog`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: A finished Email export is listed as "Slack · Discord" in Recent exports (confidence high)**

Each finished row is named from `destinationOfPreset(copy.export!.preset)`, and for the shared `balanced` preset that always returns `chat` (`destinations.ts:102-107`). So a copy the user exported from the Email card shows up here as "Slack · Discord". The PR accepts this for the Ready cards, but this list says what was exported, so the user sees the wrong name for their copy. If the recording metadata cannot carry the destination, consider a neutral name for `balanced` copies.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Opening Export for one video clears the rail badge, but that screen doesn't show any finished copies (confidence high)**

`onExport` matches `ROUTES.exportNew` with `end: false`, so it is true on `/export/:assetId` as well as `/export`, and `announceReadyCopies()` runs on both. The doc comment above the hook (lines 107-108) says Export clears the badge because it "points at the copies". Only the no-video screen does that, though: `RecentExports` is rendered only in the `!assetId` branch (`pages/export/export-page.tsx:101-112`). The `/export/:assetId` screen shows the export stage for one video and lists none of the finished copies.

So a user who opens a Library card's Export button (going to `/export/<id>`) has every unseen finished copy announced. The rail count disappears with no copy ever shown to them, and nothing tells them it happened.

Fix: use `end: true` here (`matchPath({ path: ROUTES.exportNew, end: true }, pathname)`). Then only `/export`, the screen that lists recent copies, clears the badge. `sidebar.test.tsx` only checks clearing on `ROUTES.exportNew`, so that test still holds.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The +1 for a running export has no test (confidence high)**

`useExportBadge` now adds 1 while `status === "exporting"`, and the badge label ("# copy in progress or ready") depends on that. `sidebar.test.tsx` only seeds copies through `noteFinishedCopy`. No test starts or mocks an export, so it never checks that a running export counts, or that the badge drops after the export finishes, errors or is cancelled. A test that mocks `useExportRunner` to return `status: "exporting"` would cover it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡📝 **Consider · docs: Ready-copy docs still say the count is on the Library rail item (confidence high)**

This PR moves the count from the Library item to the Export item. Two docs still describe the old behaviour:
- the module comment in `features/video-editor/export/ready-copies.ts:5-12` and `:60` ("the Library rail item then carries a count", "The Library page is open … so the rail badge clears");
- `apps/documentation/src/content/docs/backlog/background-copy-toasts.md:3,35`, under "Library rail badge".

`libraryBadgeCount` is also now the Export badge's count. Consider updating these docs, and renaming the function, alongside this hook.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Library now leaves a dropped file to Electron's default, which navigates the window to the file; the test only checks that nothing was imported (confidence medium)**

After this PR, Export is the only place that mounts `useFileDrop`, through `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`, `pages/export/export-page.tsx:85`). Nothing else in the renderer listens for `dragover` or `drop`, and the main process only sets `setWindowOpenHandler` (`main/index.ts:400-403`), with no `will-navigate` guard. The hook's own doc says what happens next: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`use-file-drop.ts:10-11`). The Export test relies on the same behaviour when it checks `!fireEvent.drop(...)` (`export-page.test.tsx:414-416`).

Until now, Library handled drops on the whole window. Someone who keeps dropping a video on the Library out of habit will now have the app's UI replaced by the raw file, with no error. This test, "does not take a video dropped on the window", locks that in: it only asserts that `importVideoFiles` was not called, never what happened to the drop. If it checked `fireEvent.drop(...)` the way `dropFiles` does in the Export test, it would fail.

Suggested fix: keep a window-level guard that calls `preventDefault` on file `dragover`/`drop` while Library is mounted (or once in the app shell). It could also send the user to Export with the files. Then assert in this test that the drop was default-prevented.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:485 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: A test about a drop with a video open sits under "ExportPage with no video" (confidence high)**

This test renders `/export/asset-1` and picks a destination card first, so a video is open. It still sits inside `describe("ExportPage with no video")` (line 419), only because that block's `beforeEach` stubs `pathForFile`. Moving it, or renaming the block to something like "ExportPage drops and imports", would keep the test report honest about what each case covers.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only renders the with-video URL (confidence high)**

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. The bare `/export` route (`ROUTES.exportNew`) is never checked for `aria-current="page"`. The rail item links to `ROUTES.exportNew` without `end` (`shell/sidebar.tsx:53`), so both URLs probably work today, but the test doesn't show it. Add a second `renderAt("/export")` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The badge's new "copy in progress" count is never tested (confidence high)**

`useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (`shell/sidebar.tsx:121-122`), and the label changed to "copy in progress or ready". Every badge test here only seeds finished copies through `noteFinishedCopy`. Nothing covers the running export being counted, or whether that count survives opening Export. A test that puts the runner in `exporting` would cover the half of the badge this PR adds.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:10 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡❓ **Consider · question: Can the Library picker still be clipped by `.screen { overflow: hidden }`? (confidence low)**

The comment says `.wrap` is not a scroll box so the Library picker opening below its button is not clipped. But `ExportDropZone` is rendered directly inside `styles.screen` (`pages/export/export-page.tsx:103-105`), and that element has `overflow: hidden` (`export-page.module.css:15`). The picker panel is absolutely positioned at `top: calc(100% + 6px)` with `max-height: min(320px, 45vh)` (`video-picker.module.css:7-11`). At the default 900 × 670 window, the zone is vertically centred under the header, and the panel's lower part may fall below `.screen`'s bottom edge and get cut off. Its own scroll range then ends inside the hidden area. Did you check this at the default window size with a long Library?

<!-- wachi:finding -->

## packages/i18n/messages/en.json:882 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: "fits an attachment" is not guaranteed by the Balanced preset (confidence medium)**

The new Email destination uses the Balanced preset (`destinations.ts`, doc line 55). Balanced has no size cap: `export-presets.ts:255` gives it no canvas and no limit, and `export-presets.ts:115` notes it measured about 5.4 MB/min. So a recording of five minutes or more comes out above the common 25 MB attachment limits. `lineEmail` ("Balanced, fits an attachment") and `whyEmail` ("stays small enough to attach", line 884), plus their Spanish versions at es.json:882/884, promise a fit the app never checks. Either make the wording conditional ("usually small enough to attach") or show the estimate against an attachment limit, the way GitHub's bar is drawn against its 10 MB limit.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T01:38:15Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment for the removed drop strip (confidence high)**

`.importZone` was deleted, but its heading comment "NIW2-579: the \"Drop a video here\" strip, between the header and the toolbar." is still there. It now sits directly above `.stickyBar`'s comment, so it reads as if it describes the toolbar. Remove it.

<!-- wachi:finding -->
