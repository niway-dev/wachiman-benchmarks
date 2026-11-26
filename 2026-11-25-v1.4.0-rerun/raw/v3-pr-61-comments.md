# kaipu-bench-wachi-v3#61 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:40 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: "Pick from Library" stays enabled while an import runs (confidence medium)**

"Browse files" is disabled while `importing` (line 51), but the `VideoPicker` trigger is not. If the user picks a Library video during a drop or dialog import, `openVideo` navigates to that video first. When the import finishes, `usePrepareImport` navigates again to the imported file (`use-prepare-import.ts:48`). The user's pick is then silently replaced. One option is to disable the picker's trigger while importing, as the browse button already is.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Dropping a file on the Library now loads that file in place of the app UI (confidence medium)**

The Library used to call `useFileDrop`, which listens on the whole window and calls `preventDefault` on `dragover` and `drop`. Its own docstring explains why: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-11`). After this change the only caller of `useFileDrop` is `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), which only the Export page mounts. Nothing in main guards against it either: `main/index.ts` has no `will-navigate` handler (its `webContents.on` calls are only `before-input-event` and `render-process-gone`).

So when someone drags an MP4 onto the Library as they could before, the main window navigates to `file://…/clip.mp4`. The Kaipu UI disappears with no error. The PR's test step 12 says that dropping a file "does nothing", which the code does not do.

Fix: keep a window-level guard that calls `preventDefault` on `dragover`/`drop` without importing anything, either on the Library or app-wide in the shell, or block the navigation in main with `will-navigate`. If you want the Library to send people to Export, the guard can also show a toast or navigate to `exportNewPath()`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:252 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: The "1080p → sharper" text-crop illustration is wrong for TikTok · Reels and LinkedIn · Feeds (confidence high)**

`UploadSizeCard` now renders for every `send-more` destination (line 93), and it always draws the before/after crops: a soft one labelled "Uploaded at 1080p" (`cropBefore`), then a sharp one labelled "Uploaded at {resolution}". The vertical canvas is 1080 × 1920 and the square canvas is 1080 × 1080 (`export-presets.ts:273,280`). For these two destinations the label reads "Uploaded at 1080p → Uploaded at 1080 × 1080": the copy is drawn as sharper even though it has the same pixels as a 1080p upload, or fewer in the square case. Users are told, with no qualification, that this copy will survive the platform's compression better, and for these presets that is false.

The deleted Prepare detail only showed the crops for YouTube (`d === "youtube"`), where 1440p and 4K really are above 1080p. Fix: render the `crops` block only when `plan.destination === "youtube"`. Or compare against a baseline that means something for the fixed canvases.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:228 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Fill's crop is no longer shown: the framing preview was removed and the hint is only a tooltip (confidence medium)**

The deleted `ShapeCard` showed a `FramingPreview` of the thumbnail on the new canvas, with the Fill/Fit hint as visible text. The new stage keeps only the two radio buttons and moves the hint into `title` (line 240). TikTok · Reels defaults to `fill` (`export-presets.ts:275`). From a landscape recording, Fill crops most of the width: `pictureChange` reports `edges: "cropped"`. The visible hint for that case comes from `uploadHintUp` and says "We scale it up cleanly." Nothing on screen says the sides are cut off, and keyboard and touch users never see the tooltip. Consider putting back a preview or a visible line based on `plan.picture.edges`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: An Email export turns into "Slack · Discord" in Recent exports when it finishes (confidence high)**

The running row uses `running.destination` (the job carries `destination: "email"`, `export-runner.ts:314`), so it shows the Email logo and the job's title. A finished row derives its destination from the preset: `destinationOfPreset(copy.export!.preset)` returns `chat` for `balanced` (`destinations.ts:102-107`). The same copy then switches to the Slack · Discord logo and name. `LibraryVideo` has no stored destination (`features/library/types.ts:44`). The PR documents that both cards show "Ready"; this label change in the strip is a separate visible result. One option is to name a `balanced` row neutrally, or to record the destination in the export metadata.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The new "in progress" part of the Export badge has no test (confidence high)**

`useExportBadge` now adds 1 while `status === "exporting"` (line 121), and `export.railBadge` reads "# copy in progress or ready". `sidebar.test.tsx` only tests finished copies made with `noteFinishedCopy`. Nothing checks that a running export adds 1, that it stops counting when the export finishes or fails, or that a finished copy is not counted twice in the moment the export finishes (`export-runner.ts:462-463` sets `ready` and then calls `noteFinishedCopy`). Also note that the running export counts even while its progress card is on screen or the user is on Export. Finished copies follow the opposite rule: `libraryBadgeCount` leaves out the copy whose card is on screen, and a copy that finishes while Export is open never adds to the badge. Consider adding a test that mocks `useExportRunner` with `status: "exporting"`, and decide whether the running copy should follow the same on-screen rule.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: Library no longer intercepts file drops, and this test approves it without checking the window default (confidence medium)**

This test drops a file on the Library window and only checks that `importVideoFiles` is not called. It never checks whether the drop was `preventDefault`ed. Before this PR, Library mounted `useFileDrop` (through its import drop zone). That hook says why it exists: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`).

After this PR, the only caller of `useFileDrop` is `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), and only `ExportPage` uses that (`pages/export/export-page.tsx:85`). `library-page.tsx` has no drop handling left. I found no `will-navigate` guard in `src/main`.

So a user who drags a video onto Library, the screen where they would most expect it to land, gets the main window replaced by the file. The whole app UI is gone with no error.

The Export test checks for this case: `dropFiles` returns `!fireEvent.drop(...)` (export-page.test.tsx:414-416). This test should do the same and assert the drop was prevented. The behaviour also needs a fix: either keep a window-level drop guard on Library (for example, send the drop to Export), or add one at the app shell or main process (`will-navigate`). That fix lands in `library-page.tsx`, which is in another part of this review.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:285 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "Enter exports, from the page or a card" only presses Enter on a card (confidence high)**

The only Enter press here is `fireEvent.keyDown(card(/^YouTube/), …)`. The "from the page" path, where the target is `document.body` and `isPrimaryEnter` sees no button ancestor (export-page.tsx:375-386), is never tested with a destination selected. The only body-level Enter test is in the nothing-picked case (line 165). Add a `fireEvent.keyDown(document.body, { key: "Enter" })` that expects `start` to be called, or drop "from the page" from the test name.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:368 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "an unknown ?to= picks nothing" does not check that no card is selected (confidence high)**

The test only checks that the "Where is it going?" heading is shown. It would be stronger if, like line 161, it also asserted that every radio in the row has `aria-checked="false"`. That is the property `isDestinationId` (export-page.tsx:74) is meant to guarantee.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only renders /export/asset-1 (confidence high)**

The test is named for both Export routes but only renders `/export/asset-1`. The no-video route `/export` (`ROUTES.exportNew`) is never checked for `aria-current`. That is the route the NavLink actually points at (`sidebar.tsx:53`), and its `end` default is what makes the detail route light up. Add `renderAt(ROUTES.exportNew)` with the same assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment for the removed `.importZone` rule (confidence high)**

The `.importZone` rule was removed, but its comment `/* NIW2-579: the "Drop a video here" strip, between the header and the toolbar. */` was left in place. It now sits directly above the toolbar's own comment and describes a strip the Library no longer has. Delete it along with the rule.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:878 · github-actions[bot] · 2026-11-26T00:12:21Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: `prepare.dropChooseFile` / `prepare.dropFromLibrary` look unused after the Prepare drop zone was deleted (confidence medium)**

`pages/prepare/prepare-drop-zone.tsx` was deleted, and the Export drop zone uses its own `export.pickFromLibrary` / `export.browseFiles` keys. A search of `apps/kaipu-record/src/renderer/src` finds no remaining reference to `dropChooseFile` or `dropFromLibrary`. `dropMoreInLibrary` is still used, in `features/prepare/use-prepare-import.ts:49`. This PR already removes the Library's dead `import*` keys, so drop these two from en.json and es.json as well (and check the other `prepare.drop*` keys).

<!-- wachi:finding -->
