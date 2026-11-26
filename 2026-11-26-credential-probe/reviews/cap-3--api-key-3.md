<!-- cap-3, api-key-3: 28 turns, $0.96 -->

I found three real bugs, all minor UX problems. None of them crashes anything or corrupts data. I read the diff and the code it calls; I did not run the tests or the app, and I changed no files.

### 1. "Where is it going?" flashes back when the first copy finishes
**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189-191`**, with `features/video-editor/export/export-runner.ts:462`

- **What goes wrong:** when the first background copy finishes, the copies list disappears for a moment. In its place the destinations panel comes back, and the "Export a copy" button is hidden. Then the list returns.
- **Why:**
  - Whether the panel shows depends on `hasCopies = exports.length > 0 || running !== null`.
  - When the export ends, the runner sets `{ ...IDLE, ready: { job, recording } }`, so `runningCopyOf` returns `null` at once.
  - The new copy only reaches `exports` after the `refresh()` in the `readyId` effect. That effect runs after the render and is async.
  - For one or more renders, both conditions are false, so `showDestinations` turns true and the page swaps panels twice.
  - The old code didn't do this: it showed the copies section whenever the page was a master (`showCopies = master || …`).
- **Possible fix:** treat `runner.ready?.job.sourceAssetId === video.assetId` as "has copies" until the list refresh lands.

### 2. Dragging a copy out doesn't mark it as seen
**`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:169-175`**

- **What goes wrong:** after the user drags a finished copy into Finder or Slack from this page, the Library badge and the "unseen copy" pointer from NIW2-586 still point at it.
- **Why:**
  - The new Drag handler only calls `e.preventDefault()` and `window.electronAPI.startFileDrag(...)`.
  - The ready card's drag, which the docs say this one mirrors, also calls `markCopySeen(recording.assetId)` (`features/status-cards/export-status-cards.tsx:234`).
  - Otherwise a copy is only marked seen when its own page opens (`shell/sidebar.tsx:95`). Dragging from the master's page never opens that page.

### 3. Destination cards show "…" forever if the file can't be read
**`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43` and `:91`**

- **What goes wrong:** for a recording whose probe fails, every card except Archive shows "…" for as long as the page is open. It looks like it's still loading.
- **Why:**
  - `estimate()` returns `null` whenever `probe` is null, and the card then shows `size ?? "…"`.
  - `useSourceProbe` returns `probe: null` both while loading and on `status: "error"`. That covers an unreadable file, or one with no readable duration (`isUsableProbe` requires `durationSec > 0`).
  - The page only passes `.probe`, so the panel can't tell "still reading" from "failed".
  - Older recordings with no duration are exactly the files that fail this check.
- **Possible fix:** pass the probe status down, and hide the estimate (or show a fallback) on error.

Things I checked that look correct:
- All the i18n keys used exist in both `en.json` and `es.json`, which are the only locale files.
- `MasterTag` accepts `size="sm"`, and the `startFileDrag(id, name)` signature matches.
- The new state hooks are declared before the early returns.
- Prepare's `onStarted` pushes a new history entry without `fromRecording`, so the "Saved" notice doesn't come back after a copy starts.
- The title can still shrink to an ellipsis, because the `h1` has `overflow: hidden`.
