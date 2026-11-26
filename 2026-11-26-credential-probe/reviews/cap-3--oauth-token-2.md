<!-- cap-3, oauth-token-2: 26 turns, $1.27 -->

I found two real bugs. Neither one is a crash: both make the recording page show the wrong state. I didn't modify any file and didn't run the test suites.

**1. The "Where is it going?" panel flashes back when the first copy finishes** — `library-detail-page.tsx:189-191`

- **What goes wrong:** When a master's first background copy completes, the page briefly drops "Copies from this original" and the "Export a copy" button, shows the destinations panel again, then swaps back once the Library list reloads.
- **Why:** `showDestinations` now depends on `hasCopies = exports.length > 0 || running !== null`. When the export completes, the runner switches to idle in one step (`export-runner.ts:462`, `set({ ...IDLE, ready: { job, recording } })`), so `runningCopyOf` returns null at once. The new copy only appears in `exports` after `refresh()` finishes, and that call is async: the effect at `library-detail-page.tsx:146-148` fires on `readyId` and has to wait for `listLibraryItems`. In between, `hasCopies` is false. Before this PR the strip and copies panel were always shown on a master, so this gap couldn't be seen. If the refresh fails, the page stays in the "no copies" state.

**2. If the file can't be read, the destination cards show "…" forever** — `destinations-panel.tsx:43` and `:91`

- **What goes wrong:** For a recording whose file can't be read, five of the six cards say "…" for good, which looks like they are still loading.
- **Why:** `estimate()` returns `null` whenever `probe` is null, and the card shows `size ?? "…"`. The page now reads every local recording's file (`library-detail-page.tsx:142`), and `useSourceProbe` returns `probe: null` both while loading and after a failed or unusable read (`status: "error"`). The panel only receives `probe`, not the status, so it can't tell the two apart. Only the archive card, which uses the file size, ever shows a number. Passing the probe status, or showing nothing or a "no estimate" line on error, would fix it.

Everything else I checked holds up:
- The six cards come from `DESTINATION_IDS` and go to `preparePath(assetId, destination)`, matching the `?to=` values the tests expect.
- With no framing passed, `planCopy` uses the same defaults Prepare starts with (vertical "fill", square "fit"), so the card estimates match Prepare's.
- `startFileDrag(copy.id, copy.title)` matches the preload and main handler signatures, and main adds the file extension.
- The new i18n keys exist in both `en.json` and `es.json`, and the removed keys aren't used anywhere. `sendTo` is still used by `video-row.tsx` and `video-card.tsx`, so keeping it is correct.
- The heavy-to-send banner switching from `!master` to `!showDestinations` matches the updated backlog doc: the banner shows on a heavy copy, on a heavy master with copies, or after "Not now".
