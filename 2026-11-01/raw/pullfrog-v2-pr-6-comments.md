## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 by pullfrog[bot]

With `useFileDrop` removed, nothing on the Library calls `preventDefault` on `dragover` / `drop` any more. `use-file-drop.ts` says what happens then: "a file dropped where nothing handles it makes Electron navigate the window to that file". `main/index.ts` has no `will-navigate` guard. A user who drops a video on the Library, as NIW2-579 taught them to, will probably see the app replaced by a bare video player. The new test cannot catch this because jsdom never navigates.

<details><summary>Technical details</summary>

````markdown
# Unhandled file drops on the Library navigate the Electron window

## Affected sites
- apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 — the `useFileDrop` call that absorbed drops was removed
- apps/kaipu-record/src/main/index.ts:400 — `setWindowOpenHandler` is set, but there is no `will-navigate` handler for the main window
- apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 — only checks that `importVideoFiles` is not called

## Required outcome
- Dropping a file anywhere in the app outside Export must not navigate the window away from the renderer.

## Suggested approach (optional)
- Add a window-wide guard: either `mainWindow.webContents.on("will-navigate", e => e.preventDefault())` for non-app URLs in main, or a shell-level `dragover`/`drop` `preventDefault` that Export's `useFileDrop` overrides. Another option is to have the Library catch the drop and route to `/export` with the files, so the old gesture still works.
- This also protects Record, Editor and Settings, which were already exposed before this PR.
````

</details>

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:17 by pullfrog[bot]

`recentCopies` keeps every MP4 that has an `export` sidecar, editor exports included. Each one then gets a destination from `destinationOfPreset`. An edited export at the default Balanced preset therefore shows up as "Slack · Discord ✓ Ready". The running row (line 50) makes the same fallback for editor jobs. `MasterCopiesPanel.destinationPresetOf` already handles this correctly by requiring `fingerprint === WHOLE_RECORDING_FINGERPRINT`.

<details><summary>Technical details</summary>

````markdown
# Recent exports mislabels editor exports as destination copies

## Affected sites
- apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:17 — filter does not check `export.fingerprint`
- apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:50 — `running.destination ?? destinationOfPreset(running.presetId)` gives editor jobs (no `destination`, `wholeRecording` falsy) a destination logo
- apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 — destination name derived from preset for every row

## Required outcome
- Only whole-recording copies (`export.fingerprint === WHOLE_RECORDING_FINGERPRINT`) are named after a destination. Editor exports either stay out of the list or show their own title and a generic icon, as `MasterCopiesPanel` does.
- The running row names a destination only when `job.destination` or `job.wholeRecording` says it is a destination copy.
````

</details>

