<!-- cap-0.75, oauth-token-1: 10 turns, $0.65 -->

I found no clear bugs in this PR. I read the diff and the code it calls: `destinations.ts` (`planCopy`, `presetForDestination`, `groupOf`), `resolveExportTarget`, `asPreparable`/`useSourceProbe`, `isMaster`, `MasterTag`, and the `startFileDrag` path through preload and main. I didn't run the tests.

**What I checked and found correct:**
- **Hooks:** the new `useState` calls (`library-detail-page.tsx:136`, `:139`) and the probe that now always runs (`:142`) come before the early returns at `:157` and `:161`, so hook order stays the same.
- **Function calls:**
  - `planCopy`, `presetForDestination` and `resolveExportTarget(preset, probe, probe.durationSec)` match their signatures.
  - The archive destination is in the `"keep"` group, so `data-tone="light"` is right for it.
  - `startFileDrag(copy.id!, copy.title)` matches `startFileDrag(id, name?)` and the existing call in `export-status-cards.tsx:235`.
  - Calling `e.preventDefault()` on drag start is the same pattern the ready card already uses.
- **Removed i18n keys:** nothing still uses `where*`, `copiesEmpty` or `copyProgress*`. `sendTo` is kept and is still used by `video-card.tsx` and `video-row.tsx`. Both locale files (en, es) got the same keys.
- **Progress text:** `etaMinutes` is `"{minutes} min"`, so `copyExporting` adding " left" gives "2 min left", as the test expects, with no doubled word.
- **Saved notice:** the notice (`master && showSavedNotice`) and the master note (`master && !showSavedNotice`) are exact opposites, so one never hides the other by mistake.
- **Heavy banner:** it moved from `heavy && !master` to `heavy && !showDestinations`. That matches the docs: a heavy master with copies, or one where the user pressed "Not now", now gets the banner.

**Minor points, not bugs:**
1. **Test cleanup:** `master-copies-panel.test.tsx:99-100` sets `window.electronAPI.startFileDrag = vi.fn()` and never restores it. The ready-card test uses `vi.spyOn(...)` with `mockRestore()`. If `test/setup.ts` builds `window.electronAPI` once rather than per test, the mock leaks into later tests in the same file.
2. **"Not now" reset:** the comment at `library-detail-page.tsx:138` says the panel stays hidden "until the page is left". The state is actually keyed by `assetId` on a component that stays mounted across `/library/:id` changes, so it only resets on leaving the detail route. In practice this almost never shows: a master with no copies has no copy pages to bounce to and back from.
