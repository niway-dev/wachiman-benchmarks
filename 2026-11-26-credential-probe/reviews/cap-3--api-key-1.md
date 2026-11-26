<!-- cap-3, api-key-1: 38 turns, $1.31 -->

I found no serious bugs: nothing that crashes, sends the user to the wrong place, or corrupts data. There are two real but small bugs, plus two judgment calls for the author. I checked every changed file and what it calls: `destinations.ts` (`planCopy`, `presetForDestination`, `groupOf`), `resolveExportTarget`, `useSourceProbe`, the export runner's finish step, `useLocalLibrary.refresh`, the `startFileDrag` IPC in preload and main, `RecordingTitle`, and the i18n keys. I didn't run the tests.

## Bugs

### 1. "Where is it going?" flashes when the first copy finishes
`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189-191`

```ts
const hasCopies = exports.length > 0 || running !== null;
const showDestinations = master && preparable !== null && !hasCopies && ...;
```

When a master's first copy finishes, the runner resets to idle and records the finished copy in one step (`export-runner.ts:462`, `set({ ...IDLE, ready: { job, recording } })`). That makes `running` null straight away. But the new copy only reaches `exports` after the page reloads the library list. That reload starts in a `useEffect` (`library-detail-page.tsx:146-148`), which runs after the page has already been drawn.

So for one drawn frame, `exports` is empty and `running` is null. The page shows:
- the "Where is it going?" panel again,
- no "Export a copy" button,
- no copies panel.

Then the reload turns on the loading state and the page settles on the copies view. Before this PR, a master always showed the same panel whether a copy was running or done, so this didn't happen. A fix: also count `runner.ready?.job.sourceAssetId === video.assetId` as having copies.

### 2. Destination cards show "…" forever if the file can't be read
`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263, 311`

`useSourceProbe` returns `probe: null` both while it is reading the file and when reading fails (`use-prepare-copy.ts:57`, `{ status: "error", probe: null }`). The page only passes `.probe` down (`library-detail-page.tsx:142`), so the panel can't tell the two apart. If the file can't be read (unreadable file, zero duration), every card except Archive stays on "…", which looks like it is still loading, with no way out.

Before this PR, the only things that read the file showed a proper fallback (`heavyBannerBodyNoEstimate`). Pass the probe status down and show nothing, or "—", when it fails.

## Judgment calls for the author

- **The heavy-to-send banner comes back after "Not now"** (`library-detail-page.tsx:517`). The condition changed from `heavy && !master` to `heavy && !showDestinations`. On a heavy master with no copies, clicking "Not now" hides the panel and then shows the same "heavy to send" text as a separate banner with its own "Prepare a light copy →" button. The docs list a banner only for "a heavy copy, or a heavy master with copies", so this case looks unplanned. Someone who just declined is asked again right away.
- **The Archive card and the details line can show the same size differently.** The card uses `formatMB(sizeBytes)` (`destinations-panel.tsx:262`), which never switches to GB. The details line uses `formatSize`. A 1.5 GB recording shows "1.5 GB" in the details line and "1500 MB" on the Archive card. The heavy banner already does the same, so this is cosmetic.

## Checked and fine
- The Drag button calls `startFileDrag(id, title)` exactly as the ready card does, and the main process checks the id and adds the file extension.
- The picture size on copy rows comes from `resolveExportTarget(preset, probe, …)`. Fixed-size presets ignore Fit/Fill for width and height, so passing no framing is correct.
- The removed i18n keys (`where*`, `copiesEmpty`, `copyProgress*`) are no longer used anywhere. `sendTo` is still used by the Library card and row, and the PR keeps it.
- The title can no longer overflow its row: the `h1` has `overflow: hidden`, so it is allowed to shrink inside the row.
- `useSourceProbe` ignores a result that belongs to a different recording, so reading the file for every local recording can't show the wrong resolution.
