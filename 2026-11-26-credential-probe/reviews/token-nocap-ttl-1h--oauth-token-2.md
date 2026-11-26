<!-- token-nocap-ttl-1h, oauth-token-2: 28 turns, $1.3 -->

I found one clear bug and two smaller ones. I read the diff, the changed components, and the code they call (`destinations.ts`, `export-presets.ts`, `use-prepare-copy.ts`, `recording-title.*`, `export-status-cards.tsx`, the main-process `startFileDrag` handler and the tokens). I didn't run the tests or modify any file.

### 1. A long title still won't get an ellipsis, and it runs over the master tag
**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.module.css:61-64`, with `library-detail-page.tsx:256-268`**

- **What the PR intended:** The main point of the PR is that the title fills the space the row leaves and gets an ellipsis only at that edge. To do that, `.title` (the wrapper) gets `flex: 1; min-width: 0`.
- **What goes wrong:** That wrapper isn't the element that needs to shrink. Inside it, `RecordingTitle` renders its own flex row (`recording-title.module.css:1-6`), and the `<h1>` is a flex item in that row.
- **Why the ellipsis never happens:** The `<h1>` has `white-space: nowrap; overflow: hidden; text-overflow: ellipsis` but keeps the default `min-width: auto`. Nothing in `base.css` resets it. So the `<h1>` won't shrink below the full width of its text.
- **Result:** The `<h1>` overflows the wrapper, which has visible overflow. A long title paints over the "MASTER · FULL QUALITY" tag and pushes the rename pencil out of place.
- **Fix:** Add `min-width: 0` to the `<h1>`, or to `.title h1` and the inner row. Alternatively, make the wrapper `display: flex` and clip it.
- **Tests:** The new test only checks which elements are in the row, not how it lays out, so it can't catch this.

### 2. Destination cards show "…" forever when the file can't be read
**`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263, 311`**

- `estimate()` returns `null` whenever `probe` is null, and the card then shows `"…"`.
- The page passes `useSourceProbe(...).probe`, which is also null when the probe fails (`use-prepare-copy.ts:55-57`, `status: "error"`).
- The page now reads the file for every local recording. Any file it can't read (an old import, a codec it can't parse) shows "…" on five of the six cards permanently, which looks like it is still loading.
- The panel only gets `probe`, not the status, so it can't tell failure from loading. It should get the status and fall back to no size, or a "size unknown" label, on error.

### 3. Dragging from "Copies from this original" doesn't mark the copy as seen
**`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`**

- The new Drag handle copies the ready card's drag (`export-status-cards.tsx:231-235`, "the same IPC as the ready card") but leaves out the ready card's `markCopySeen(recording.assetId)` call.
- Copies are otherwise only marked seen when their own detail page is opened (`sidebar.tsx:95`).
- So a user can drag a new copy straight off the master's page into Slack or Finder, and the Library badge still points at it as unseen.
- **Fix:** Call `markCopySeen(copy.assetId)` in `onDragStart`.

The rest of what I checked looks correct: the `planCopy` and `presetForDestination` inputs, `resolveExportTarget` for each copy's picture size, `groupOf` → tone mapping (archive is in the "keep" group and shows teal), `?to=` paths for all six destinations, the i18n keys in both locales (the remaining `sendTo` is still used by `video-row` and `video-card`), and the heavy-banner and destinations-panel conditions.
