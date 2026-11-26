# kaipu-bench-wachi-v3#73 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:251 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: "Ready" ignores Fill / Fit: a Fit vertical/square copy opens when Fill is picked (confidence medium)**

`existing` and the cards' `isReady` (line 338) look up `reusable[presetId]`. `findReusableExports` matches on `encodeFingerprint(WHOLE_RECORDING_FINGERPRINT, preset)` only (`features/video-editor/export/export-reuse.ts:74`). For `vertical` and `square`, that fingerprint is the bare `"whole"` (`export-presets.test.ts:396`), so it does not record the framing. Example: the user has a TikTok · Reels copy made with Fit, then switches the stage to Fill. The card still says Ready, and `primary` (Enter or the pink button, line 264) opens the existing Fit file instead of encoding a Fill copy. Nothing tells the user the framing differs. Fix: include the framing in the reuse key for presets with `framings.length > 0`, or skip `existing` for vertical and square unless the stored framing matches `framingOf(d)`. If the old Prepare page already did this, it is still a defect on the new screen, which now advertises Ready per card.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A file dropped on the Library now navigates the app window to that file (confidence high)**

The Library no longer calls `useFileDrop`, so nothing on this screen calls `preventDefault` on `dragover`/`drop`. The hook's own comment says what happens next (`features/library/hooks/use-file-drop.ts:10-11`): "a file dropped where nothing handles it makes Electron navigate the window to that file". Nothing in `src/main` guards against this: there is no `will-navigate` handler, only `setWindowOpenHandler` (`main/index.ts:400`). Step 12 of the PR says "dropping a file there does nothing", but it actually replaces the app UI with the video file. The Library is also where users have learned to drop files until now. Suggested fix: keep a window-level guard on the Library that only prevents the default (or forwards the file to Export), or add an app-wide `will-navigate` guard in the main process.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:252 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: The "sharper text" crop illustration is shown for TikTok · Reels and LinkedIn · Feeds, whose copies are no larger than 1080p (confidence medium)**

The removed Prepare detail showed the before/after crops only for YouTube, which uploads at 1440p or 4K. `UploadSizeCard` now shows them for every `send-more` destination. Those include `vertical` (1080 × 1920) and `square` (1080 × 1080) (`export-presets.ts:271-283`). The card draws "Uploaded at 1080p" as soft and "Uploaded at 1080 × 1920" as sharp. These copies are no wider than 1080p. With Fit, a 16:9 recording is scaled down (`uploadHintDown`), so its text gets smaller than in a 1080p upload. The illustration therefore promises a gain these destinations don't deliver. Suggested fix: render `.crops` only when `plan.destination === "youtube"`, as before.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:51 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟡🐛 **Consider · bug: Escape and outside-click close the picker but leave focus where it was (confidence medium)**

The panel is a `role="dialog"`, but opening it doesn't move focus into it, and Escape doesn't send focus back to the trigger. A keyboard user who closes the list with Escape stays on the trigger, which is fine. A user who has tabbed into the list loses focus when the panel unmounts, and focus falls to `body`. Consider focusing the trigger again when the panel closes.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟠🧪 **Fix · tests: "does not take a video dropped on the window" would pass even if the Library still imported drops (confidence high)**

This test only checks that `importVideoFiles` is never called. But this file never stubs `pathForFile`, so it uses the setup default `pathForFile: () => ""` (`src/test/setup.ts:156`). `importDropped` treats a file with an empty path as skipped and returns before `importVideoFiles` (`features/library/hooks/use-import-videos.ts:102-111`). So if `LibraryPage` still mounted `useFileDrop` + `importDropped`, the drop would show a "Skipped" toast and the assertion would still pass. The test you removed stubbed `pathForFile` to a real path for this reason. Fix: stub `window.electronAPI.pathForFile = vi.fn((f) => `/Users/me/Movies/${f.name}`)`, as `export-page.test.tsx:421` does, so the negative assertion can actually fail.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:85 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: The behavior this test pins lets a file dropped on the Library navigate the Electron window to that file (confidence medium)**

`useFileDrop` exists because "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:8-11`). Its only caller is now `usePrepareImport`, mounted only on Export. Main has no `will-navigate` guard, only `setWindowOpenHandler` (`main/index.ts:400-403`). Before this PR the Library took drops and called `preventDefault`. Now a video dragged onto the Library replaces the app's UI with the file, with no error and no way back in the UI. The test asserts the drop is ignored, but it never checks `fireEvent.drop`'s return value, which here would be `true` (default not prevented). Either keep a window-level drop guard while the Library is mounted, for example `useFileDrop` that sends the user to `/export` or just calls `preventDefault`, or block `will-navigate` in main. Then assert `!fireEvent.drop(...)` here, as `dropFiles` does at `export-page.test.tsx:416`. Medium confidence: the navigate-on-drop premise comes from the repo's own comment, and I could not check Electron's runtime behavior from the repo.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only renders the with-a-video URL (confidence high)**

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. Nothing checks that the rail item is lit on `ROUTES.exportNew` (`/export`). Both cases rely on `isActive(ROUTES.exportNew)` matching with `end: false` (`sidebar.tsx:68-69`), so a later `end: true` on that entry would break the bare `/export` case and this test would stay green. You could add a second `renderAt(ROUTES.exportNew)` with the same `aria-current` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:48 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟡🧪 **Consider · tests: The "in progress" part of the new badge has no test (confidence high)**

`useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (`sidebar.tsx:121-122`), and the label reads "copy in progress or ready". Every test here only feeds finished copies through `noteFinishedCopy`, so the running-export count is never exercised. The same goes for the subtraction of the copy whose ready card is showing (`ready?.recording.assetId`). If either drifts, the rail shows a wrong count and no test fails.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/export-screen.md:50 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟠🐛 **Fix · bug: A file dropped on the Library now navigates the app window to that file; it does not "do nothing" (confidence medium)**

This doc says the Library "no longer takes window drops", and the PR's test plan, step 12, says dropping a file there "does nothing". The code does not back that up. `useFileDrop` explains why it listens on the whole window: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`). The handlers that stop this are in the hook (`use-file-drop.ts:29-47`), and the Library no longer mounts it. Nothing in `apps/kaipu-record/src/main` registers a `will-navigate` guard either: a search of `src/` for `will-navigate` and for other `dragover`/`drop` listeners turns up only this hook.

So if a user drags an MP4 from Finder onto the Library, which used to import it, the main window loads `file:///…/clip.mp4` and the app UI is gone until a reload. Nothing tells them why. `library-page.test.tsx:81-86` checks only that `importVideoFiles` is not called. jsdom never navigates, so that test passes either way.

Fix it where the Library's drop handling was removed. Options: keep a window-level `dragover`/`drop` `preventDefault` in the shell for every screen, send Library drops to Export, or add a `will-navigate` guard in main. Then make this line say what actually happens.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T01:48:11Z

👮 **Wachiman** · 🟡🧹 **Consider · cleanup: Orphaned comment for the deleted `.importZone` rule (confidence high)**

The `.importZone` rule was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits directly above the `.stickyBar` comment and reads as if it describes the sticky bar. Delete it along with the rule.

<!-- wachi:finding -->
