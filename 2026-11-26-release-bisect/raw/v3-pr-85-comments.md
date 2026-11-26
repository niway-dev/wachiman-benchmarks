# kaipu-bench-wachi-v3#85 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117 · github-actions[bot] · 2026-11-26T06:32:09Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: Any library re-list unmounts the Export screen and silently drops the picked destination and YouTube/Fill choices (confidence medium)**

`useLocalLibrary().refresh` calls `setLoading(true)` on every re-list (`use-local-library.ts:41-42`), and it re-lists on every `library:changed` broadcast (`use-local-library.ts:133`). That includes the one that follows the fire-and-forget `refreshCloudCatalog()` on mount (`use-local-library.ts:124-130`), and probably the one when a finished copy lands in the vault. During each re-list this page returns the "Loading" placeholder at line 117 instead of `<ExportScreen>`, so the screen unmounts. When it comes back, `selected` is re-seeded from `initialDestination={urlDestination}` (line 158), not from `chosen.current`. `youtube` and `framings` go back to their defaults too.

In practice: a signed-in user opens Export, picks GitHub with the arrows, and a moment later the catalog refresh lands. The stage flips back to "Where is it going?" (or to the `?to=` destination), and nothing says why. The same thing can happen right after Enter starts an export, which this PR keeps on screen on purpose.

Fix: show the loading state only when nothing has loaded yet, e.g. `if (isLoading && !video)`. Alternatively, seed `initialDestination` from `chosen.current ?? urlDestination` and lift the YouTube and framing state, so that a remount does not lose them.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-26T06:32:09Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Enter can start an export while the Change video list is open (confidence medium)**

`destinationStep` ignores arrows inside `[role='dialog']` (line 364), but `isPrimaryEnter` has no matching check. `VideoPicker` renders its list as `role="dialog"` (`video-picker.tsx:69-71`). If focus is on a non-button spot in or around the open list (the panel's padding, the "no videos" text, or the body after a click there), Enter reaches the document listener and runs `primary()`. That starts an encode, or opens the existing copy, while the user is choosing another video. Adding `if (target.closest("[role='dialog']")) return false;` would make Enter behave the same way as the arrows.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:352 · github-actions[bot] · 2026-11-26T06:32:09Z

👮 **Wachiman** · Nit · 🟡📝 **Consider · docs: The destinationStep doc comment says it ignores a held key, but the code never checks event.repeat (confidence high)**

The comment lists "a held key" among the cases that return null. The function checks key, `defaultPrevented`, `isComposing`, modifiers, fields, radiogroups and dialogs, but not `event.repeat` (lines 357-365). A held arrow therefore moves the selection repeatedly. Either drop the claim from the comment or add the check, whichever behaviour is intended.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T06:32:09Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: A file dropped on the Library now makes Electron navigate the window to that file (confidence high)**

The Library used to mount `useFileDrop`, and that hook's own contract (`features/library/hooks/use-file-drop.ts:8-11`) says it exists because "a file dropped where nothing handles it makes Electron navigate the window to that file". The hook is the only `dragover`/`drop` handler in the app (`use-file-drop.ts:48-51`), and the main process sets `setWindowOpenHandler` (`main/index.ts:400`) but has no `will-navigate` guard. With the hook removed here, nothing calls `preventDefault` on a drop while the Library is open, so dropping an MP4 on the Library swaps the renderer for the file and throws away the app's state. The PR says "dropping a file there does nothing", but the code does not do that. To keep the Library from importing while still blocking the default, add a window-level `dragover`/`drop` `preventDefault` (in the shell, or as an option on `useFileDrop`), or add a `will-navigate` guard in the main process.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:255 · github-actions[bot] · 2026-11-26T06:32:09Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: TikTok/LinkedIn before/after crop shows a 1080p copy as sharper than a 1080p upload (confidence high)**

`UploadSizeCard` now renders the crops for every `send-more` destination (line 93), not only YouTube (the deleted detail rendered them only when `d === "youtube"`). For TikTok · Reels and LinkedIn · Feeds, `resolution` is the copy's own canvas, which is 1080 × 1920 or 1080 × 1080 (`export-presets.ts:273,280`). The "before" crop is hard-coded as the soft "Uploaded at 1080p" (`cropBefore`), and the "after" is the sharp "Uploaded at 1080 × 1920". Both are 1080p uploads, so the illustration promises sharper text that this copy cannot give. Show the crops only when the copy's short side is larger than 1080 (YouTube), or pick a different comparison for the fixed-canvas destinations.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:201 · github-actions[bot] · 2026-11-26T06:32:09Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Upload-size and Fill/Fit radio groups do not answer arrow keys (confidence medium)**

These are `role="radiogroup"`/`role="radio"` buttons with no arrow-key handling (lines 201-218 and 233-248). `destinationStep` in `export-page.tsx:363` hands arrows inside any non-row radiogroup back to the group, "which answers its own arrows", but these groups never handle them. Arrow keys on 1440p/4K or Fill/Fit therefore do nothing, while ARIA radio semantics tell assistive tech users that arrows change the choice. You could add left/right handling, or use plain toggle buttons (`aria-pressed`) instead of the radio roles.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:311 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: GitHub limit verdict is hidden from screen readers by role="img" (confidence medium)**

`SizeBarCard` puts `role="img"` on the card, which makes its children presentational, and its `aria-label` (`barLabel`) only says "Your recording X, the copy Y". The tag that carries the card's main message ("fits the 10 MB limit" / "over GitHub's 10 MB free-plan limit" / "N% lighter") is never announced. You could put the tag in the label, or limit `role="img"` to the bar itself (`styles.bar`).

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: The running export adds 1 to the badge even where it is already on screen (confidence high)**

`running` counts whenever `status === "exporting"`, on every route. A finished copy is left out of the badge when its card is on screen (`libraryBadgeCount(copies, ready?.recording.assetId)`), and finished copies stop counting once Export is open (`announceReadyCopies`). The running copy gets neither exception. So on `/export` the rail shows "1" for a copy whose progress row is in Recent exports (`recent-exports.tsx:35-62`), and on other pages it shows "1" while the progress card is visible. That clashes with the sidebar test "a copy that finishes while Export is open never badges". If the badge is meant to be the "out of sight" count, skip the running copy while on `/export` (`onExport` is already computed in the effect) and while the progress card is visible (`!runner.progressHidden`, which `export-status-cards.tsx:35-37` uses). Either way, no sidebar test covers the running case.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: A file dropped on Library now gets Electron's default: the window navigates to the file. The test checks only that nothing was imported (confidence medium)**

The Library no longer mounts `useFileDrop`. That hook is now mounted only through `usePrepareImport` on Export (`features/prepare/use-prepare-import.ts:55`). The hook's own comment explains why it exists: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`). The main process has no `will-navigate` guard either: no match in `src/main`, and no other `drop`/`dragover` listener in `src`.

So dropping a video on the Library replaces the app's renderer with the file. Everything held in that renderer is lost, including the background export runner. Leaving the page this way is not a window close, so the `setExportActive` close confirmation probably never fires. The PR body says "dropping a file there does nothing", which is wrong.

This test codifies the regression. It checks only `importVideoFiles` not called and ignores `fireEvent.drop`'s return value. The Export test does check it (`export-page.test.tsx:414-416`, `!fireEvent.drop(...)`).

Fix: keep a window-wide drop guard that calls `preventDefault` on `dragover`/`drop` without importing. It could sit in the app shell, or in main as `will-navigate` → `preventDefault`. Then assert here that the drop was prevented, as the Export test does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:485 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: The "with a video open" drop test sits under `describe("ExportPage with no video")` (confidence high)**

This test renders `/export/asset-1`, so it covers the screen with a video. It only shares the `pathForFile` `beforeEach` with the no-video block. Move it, or the `beforeEach`, into a "drops" describe so the suite name matches what it covers.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:251 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: The test says "the cards say where it went" but nothing asserts it (confidence high)**

The body checks the `% lighter` text and the `balanced`/`email` start args. Nothing checks what the cards show for an Email copy. The PR's stated decision, that a Balanced copy reads "Ready" on both Slack · Discord and Email, is not covered here either. Add that assertion or shorten the test title.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.module.css:15 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: `.screen { overflow: hidden }` still clips the "Pick from Library" list on Export with no video (confidence medium)**

`export-drop-zone.module.css:10` drops the scroll box so that "the Library picker opens below its button and must not be clipped". But the drop zone renders inside `.screen` (`export-page.tsx:103-113`), and `.screen` keeps `overflow: hidden`. The picker's `.panel` is absolutely positioned against `.root` (`video-picker.module.css:1-12`), which sits inside `.screen`, so `.screen` still clips it.

Rough layout at the minimum main window (670 high, so the page is 614): the header is about 82px, Recent exports about 100px, and the centred zone about 236px. That puts the "Pick from Library" button's bottom near y≈380. The panel opens 6px below it and can be up to `min(320px, 45vh)` ≈ 301px tall, so it ends near y≈686, about 70px past the bottom of `.screen`. With more than about 7 recordings in the list, the last rows scrolled into the panel's bottom stay under the clip and can't be clicked.

These numbers are estimates from the CSS; I did not render the page. Please check with a long Library at 900×670. Two possible fixes: open this picker upward (it already takes an `align` prop), or render the panel through a portal.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "with and without a video" only renders /export/asset-1 (confidence high)**

The test name promises both URLs, but it only renders `/export/asset-1`. Bare `/export` (`ROUTES.exportNew`, the link's own target) is never checked for `aria-current`. Add a second `renderAt(ROUTES.exportNew)` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:48 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: The badge's new "in progress" count is never exercised (confidence high)**

`useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (`sidebar.tsx:121-122`), and the label reads "copy in progress or ready". Every test here drives only `noteFinishedCopy`, so the running-export term is untested. That includes the case where it must not double-count once the copy finishes and becomes `ready`. A test that puts the runner into `exporting` would pin it.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:882 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: Email copy promises it "fits an attachment", but the Balanced preset has no size cap (confidence medium)**

`lineEmail` ("Balanced, fits an attachment") and `whyEmail` ("A balanced copy stays small enough to attach") say every Email copy fits as an attachment. But the Email destination uses the Balanced preset, and that preset has no byte cap (`export-presets.ts:137`, `:178`, `:255`: a quality tier plus 24 fps, and no limit like GitHub's `GITHUB_FREE_LIMIT_BYTES`). A long recording can produce a Balanced copy larger than common mail attachment limits. The same wording is in es.json:882/884. Either soften the wording (for example "usually small enough to attach") or draw a limit bar for Email the way GitHub has one.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T06:32:10Z

👮 **Wachiman** · Nit · 🟡🧹 **Consider · cleanup: Comment left over from the removed drop strip (confidence high)**

`.importZone` was deleted, but its comment ("NIW2-579: the \"Drop a video here\" strip, between the header and the toolbar.") is still there, right above the `.stickyBar` comment. A reader will think it describes the toolbar. Delete line 108.

<!-- wachi:finding -->
