<!-- cap-3, oauth-token-3: 28 turns, $1.28 -->

I found two real bugs, both low severity. Neither breaks a main flow, but both are regressions this PR introduces. I only read the code; I didn't run the tests.

### 1. The destination cards show "…" forever when the file can't be read
**`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263` and `:311`**

- **What goes wrong:** `estimate()` returns `null` whenever `probe` is null. The card then shows `size ?? "…"`.
- **Why:** The page passes `useSourceProbe(...).probe` (`library-detail-page.tsx:142`). That is `null` both while the file is loading and after a failed read (`useSourceProbe` returns `{ status: "error", probe: null }` when `isUsableProbe` fails, e.g. `durationSec` is 0 or the size is unreadable). The panel can't tell the two apart.
- **Result:** On a recording whose probe fails, five of the six cards (all but Archive) show "…" for good, which looks like they're still loading.
- **Why it matters more now:** This PR runs the probe on every local recording, not only heavy ones. So any unreadable recording hits this.
- **Fix:** Pass the probe status in as well, and show nothing or the "Full size" wording once the status is `error`.

### 2. When a background copy finishes, the page briefly shows "Where is it going?" again
**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:188-191` (and `:2057` in the diff)**

- **What goes wrong:** When the export finishes, `export-runner.ts:462` sets `{ ...IDLE, ready }`. So `runningCopyOf` returns `null` right away.
- **Why:** The new copy isn't in `videos` until the `readyId` effect's `refresh()` finishes listing the library. In between, a master's first copy gives `hasCopies === false` and `showDestinations === true`.
- **Result:** The "Copies from this original" panel and its running row vanish. The "Where is it going?" panel comes back, and "Export a copy" is hidden. Then `refresh()` flips `isLoading` and the page switches to the copies layout.
- **Before this PR:** `showCopies` included `master`, so the copies panel stayed on screen across this gap.
- **Fix:** Also count `runner.ready?.job.sourceAssetId === video.assetId` as having copies.

Everything else I checked matches the code it calls:
- the `startFileDrag(id, name)` signature and its IPC;
- `planCopy`, `presetForDestination` and `resolveExportTarget` inputs;
- `groupOf` for the card colours;
- every i18n key used (`sizeAbout`, `sizeUpTo`, `sizeFull`, `etaMinutes`, `metaCopies` plural), in both `en.json` and `es.json`;
- the removed `where*`, `copiesEmpty` and `copyProgress*` keys, which nothing else uses (`sendTo` is still used by the Library card and row, and is kept);
- the CSS variables;
- the title row ellipsis: the `h1` has `overflow: hidden`, so it can shrink inside its flex row.

Not a product bug: `master-copies-panel.test.tsx` sets `window.electronAPI.startFileDrag = vi.fn()` and never restores it. Using `vi.spyOn` with `mockRestore()`, as `export-status-cards.test.tsx` does, would avoid leaking it into later tests.
