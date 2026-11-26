# kaipu-bench-wachi-v3#79 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:117 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: Any library re-list unmounts the Export screen and resets the chosen destination, YouTube resolution and framing (confidence high)**

`useLocalLibrary().refresh` calls `setLoading(true)` (use-local-library.ts:41-42), and it runs on every `libraryChanged` broadcast (use-local-library.ts:133). Main sends that broadcast after the cloud catalog refresh that the hook starts on mount (use-local-library.ts:130, main/library/index.ts:73-75), on account changes (index.ts:85-87) and when library items are saved. Each time, line 117 swaps `ExportScreen` for the Loading text even though `video` is already known. When `ExportScreen` mounts again, its state starts over: `selected` goes back to `initialDestination` (the URL's `?to=`, not `chosen.current`), `youtube` goes back to `defaultYoutubePreset(probe)`, and the framings go back to their defaults (lines 212-221).

How it goes wrong: a signed-in user opens Export, picks YouTube and chooses 4K. The catalog refresh lands, the screen flashes to Loading and comes back on the URL's destination at 1440p. If they press Enter, they export the wrong copy, or nothing, with no message. The same reset happens when a finished copy is saved while they are still on the screen, which the PR makes the normal flow ("Export stays on screen after it starts").

Suggested fix: show the loading state only while there is no video to show (`if (isLoading && !video)`). Also seed `ExportScreen`'s selection from `current()`, so a remount keeps the destination the user picked.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:98 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: An unreadable file sends the user back with the URL's destination, not the one they picked (confidence high)**

Every other way out of this screen (`openVideo` at line 87, the drop import at line 85) carries `current()`, the destination the user picked on this screen. The probe-error redirect uses `urlDestination`, so a card picked before the error is forgotten. Using `current()` here would match the rest of the page.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Important · 🟠🐛 **Fix · bug: Without useFileDrop, a file dropped on the Library makes Electron navigate the window to that file (confidence medium)**

The PR says "dropping a file there does nothing", but that only held because `useFileDrop` was mounted. Its own comment says a file dropped where nothing handles it makes Electron navigate the window to that file (`features/library/hooks/use-file-drop.ts:8-11`), and it calls `preventDefault` on dragover and drop to stop that (`use-file-drop.ts:29-47`). The main process has no `will-navigate` guard: `main/index.ts` only has a `setWindowOpenHandler` (line 400), and that doesn't cover in-window navigation.

After this change, nothing on the Library calls `preventDefault`. A video dragged from Finder onto the Library replaces the app's renderer with the file. The Library, the rail and any export the renderer is running all disappear, and nothing in the UI explains why.

The Library used to be protected against this, so this is a regression. Fix: keep a window-level guard that calls `preventDefault` on `dragover`/`drop` for file drags on the Library. Better, put it once in the app shell or block it with `will-navigate` in main, so every screen is covered. Other screens such as the editor already lack the guard.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:311 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: role="img" hides the size bar's verdict from screen readers (confidence medium)**

The size-bar `<section>` is `role="img"`, so assistive tech ignores its children and reads only the `aria-label`. The label is `barLabel` ("Your recording {from}, the copy {to}"), so screen-reader users never hear "fits the 10 MB limit", "over GitHub's 10 MB free-plan limit" or "N% lighter". For GitHub, that verdict is the main point of the card. Consider adding `tag` to the label, or drop `role="img"` and set `aria-hidden` only on the bar itself (it already has it at line 326).

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Important · 🟠🧪 **Fix · tests: The Library test accepts the window opening the dropped file (confidence medium)**

After this change, nothing on Library calls `preventDefault` on `dragover` or `drop`. `useFileDrop` (`features/library/hooks/use-file-drop.ts:29-51`) is the only place in the renderer that does, and now only Export mounts it. The main process registers no `will-navigate` guard either: the only navigation hook is `setWindowOpenHandler` at `main/index.ts:400`. In Electron, a file dropped on a page that does not cancel the event navigates the window to that file. A user who drops a video on Library, which used to import it, now loses the app UI to a bare file view.

This test fires the drop and only checks that `importVideoFiles` was not called, so it passes in exactly that state. Its sibling in `export-page.test.tsx:414-416` checks the return value of `fireEvent.drop` for this very reason ("Electron does not navigate the window to the file").

Suggested fix: on Library (or app-wide, in the shell or with a main-process `will-navigate` guard), call `preventDefault` on `dragover` and `drop` for file drags. Then assert it here, e.g. `expect(fireEvent.drop(document.body, …)).toBe(false)`. It might also be worth showing a hint that videos come in through Export.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:329 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: The unreadable-file test does not check that the destination is kept (confidence high)**

`export-page.tsx:98` navigates to `exportNewPath(urlDestination)`, which carries `?to=youtube`. The test only asserts the pathname `/export`. Every other navigation test in this file also checks `router.state.location.search`. Adding `expect(router.state.location.search).toBe("?to=youtube")` would cover the URL the code builds.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:258 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "Keep full quality keeps the full size" only checks the preset id (confidence high)**

The test name promises the full size, but it only asserts `presetId: "maximum"`. The "Full size" text is checked on the card in another test (line 163), not on this stage. Either rename the test or also assert the "Full size" text on the stage or the button.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Nit · 🟡🧪 **Consider · tests: "active on Export with and without a video" only checks with a video (confidence high)**

This test renders only `/export/asset-1`, so the "without a video" case (`ROUTES.exportNew`, which the rail item links to and matches with `end: false` at `sidebar.tsx:69`) is never checked for `aria-current`. Rendering `ROUTES.exportNew` as well would cover what the test name promises.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/destination-row.module.css:84 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Nit · 🟡🐛 **Consider · bug: The scroll box may clip part of the focus outline on the edge cards (confidence medium)**

`.row` is a scroll box (`overflow-x: auto; overflow-y: hidden`) and leaves only 3px of padding for the ring (lines 48-52). The `:focus-visible` outline reaches 4px past the card's border (2px offset plus 2px width), so on the first and last cards and along the top and bottom edge, the outer pixel of the keyboard focus ring would likely be clipped. Raising the padding/negative margin to 4px, or using `outline-offset: 0`, would keep the whole ring visible.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T06:04:16Z

👮 **Wachiman** · Nit · 🟡🧹 **Consider · cleanup: Orphaned comment for the removed `.importZone` rule (confidence high)**

The `.importZone` rule was deleted, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits right above the `.stickyBar` comment, so it reads as if it describes the sticky bar. Delete line 108 along with the rule.

<!-- wachi:finding -->
