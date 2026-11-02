=== COMMENT 4437292595 apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:40
👮 **Wachiman** · 🟡🐛 **Consider · bug: "Pick from Library" stays enabled while a dropped or browsed file is importing**

The "Browse files" button is disabled while `importing` is true (line 51), but the `VideoPicker` trigger at line 40 is not. If someone picks a Library video during an import, `openVideo` navigates to that video. When the import finishes, `usePrepareImport` navigates again, this time to the imported file, so their pick is replaced without warning. To avoid this, pass `disabled={importing}` to the trigger's `Button` the same way the Browse button does.

<!-- wachi:finding -->

=== COMMENT 4437292599 apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65
👮 **Wachiman** · 🟡🐛 **Consider · bug: A finished Email export is listed as "Chat" in Recent exports**

Finished rows get their destination from `destinationOfPreset(copy.export!.preset)`. Email and chat use the same `balanced` preset (`destinations.ts:69-71`), and `destinationOfPreset("balanced")` returns `"chat"` (that module's header says this on purpose). So a copy exported for Email shows the Chat logo and the `cardChat` name here.

The running row is different: it uses `running.destination` (line 50), so it shows Email while the export runs. When the export finishes, the same item switches to Chat. The fix is either to save the destination with the copy's export metadata, or to show a neutral label for `balanced` copies.

<!-- wachi:finding -->

=== COMMENT 4437292605 apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:312
👮 **Wachiman** · 🟡🐛 **Consider · bug: Screen readers never hear the GitHub fits/over-limit result**

The card has `role="img"`, so its children are presentational, and assistive tech reads only `aria-label`. That label is `barLabel` ("Your recording {from}, the copy {to}"). The `tag` computed at lines 299-306 (`barFitsLimit` / `barOverLimit` / `barLighter`) and the `barPicture` line are visible on screen but are not in the accessible name.

For GitHub, the whole point of this card is the 10 MB free-limit result, and screen-reader users lose it. One fix is to add `tag` to the aria-label. Another is to drop `role="img"` and keep only the bar itself `aria-hidden`.

<!-- wachi:finding -->

=== COMMENT 4437292612 apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80
👮 **Wachiman** · 🟠🧪 **Fix · tests: "does not take a video dropped on the window" would pass even if Library still handled drops**

This test no longer stubs `pathForFile`, so the default from `src/test/setup.ts:156` applies, and that default returns `""`. `importDropped` in `features/library/hooks/use-import-videos.ts:102-111` treats an empty path as "skipped" and returns before it calls `window.electronAPI.importVideoFiles`. So if `LibraryPage` still mounted `useFileDrop` + `importDropped`, which is the regression this test is meant to catch, `importVideoFiles` would still never be called and the test would pass.

Fix: stub `window.electronAPI.pathForFile = vi.fn((f: File) => `/Users/me/Movies/${f.name}`)`, as the removed test and `export-page.test.tsx:421` do. You can also assert that `fireEvent.drop(...)` returns `true` (nothing called `preventDefault`), the inverse of `dropFiles` in the Export test. Either change makes the test fail if Library still takes drops.

<!-- wachi:finding -->

=== COMMENT 4437292617 apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39
👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only renders the with-a-video URL**

The test says Export is active "with and without a video", but it only renders `/export/asset-1`. The case without a video (`ROUTES.exportNew`) is never checked. The router already registers both routes (lines 19–20). Add a second `renderAt(ROUTES.exportNew)` with the same `aria-current` check, or rename the test. The nav item's `to` is `ROUTES.exportNew` and it is matched with `end: false` (`sidebar.tsx:53`, `sidebar.tsx:69`), so the bare route is the one the name claims and the one most likely to break if someone sets `end`.

<!-- wachi:finding -->

=== COMMENT 4437292623 apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108
👮 **Wachiman** · 🟠🧹 **Fix · cleanup: Leftover comment for the deleted `.importZone` rule**

This PR removes the `.importZone` rule, but its comment `/* NIW2-579: the "Drop a video here" strip, between the header and the toolbar. */` is still here. It now sits right above the `.stickyBar` comment, so it reads as though it describes the sticky toolbar. Delete line 108 along with the rule.

<!-- wachi:finding -->

=== COMMENT 4437292630 apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:3
👮 **Wachiman** · 🟠📝 **Fix · docs: Comment calls 900 × 670 the default window; it is the minimum**

The header comment says the stage is sized so YouTube's card and the button fit "the default 900 × 670 window". In `src/shared/window-size.ts:50` the `main` preset is `width: 1040, height: 760, minWidth: 900, minHeight: 670`, so 900 × 670 is the smallest the window can be, not its default. Change the wording to "the minimum 900 × 670 window" so nobody resizes the stage against the wrong target.

<!-- wachi:finding -->

