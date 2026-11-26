<!-- token-cap-0.75-ttl-5m, oauth-token-3: 14 turns, $0.61 -->

I found four real bugs. None of them breaks the main flows the tests cover. I read the diff and the helpers it calls (`destinations.ts`, `resolveExportTarget`, `useSourceProbe`, `MasterTag`, the drag IPC, `markCopySeen` and the i18n files). I didn't run the test suite and didn't change any file.

### 1. Destination cards show "…" forever when the file can't be read
`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263` and `:311`

- **What goes wrong:** if the file can't be read, every card except Archive shows "…" permanently. Nothing distinguishes "still reading" from "gave up."
- **Why:** `useSourceProbe` returns `probe: null` in both the `"loading"` and `"error"` states. This happens when `probeSource` fails or returns something `isUsableProbe` rejects. The page passes only `.probe` (`library-detail-page.tsx:142`), so the panel can't tell the two states apart.
- **Fix:** pass the probe status down and show nothing, or a fallback, on `"error"`.

### 2. Dragging a copy from "Copies from this original" doesn't mark it as seen
`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:834-838`

- **What goes wrong:** after the user drags a ready copy out from the master's page, the Library still flags it as unseen ("copy ready").
- **Why:** this handler copies the ready card's native drag (`export-status-cards.tsx:231-236`) but leaves out its `markCopySeen(recording.assetId)` call. Today a copy is only marked seen when its own page is opened (`sidebar.tsx:95`) or when the ready card's Show/Drag buttons are used.
- **Fix:** call `markCopySeen(copy.assetId)` in `onDragStart`.

### 3. "Not now" can stay in effect after the user leaves the page
`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139,191,2044`

- **What goes wrong:** the comment says the panel is hidden "until the page is left." But the dismissal is keyed by `video.assetId` in component state. If the page stays mounted while the user moves between `/library/:assetId` routes (A → B → A, which React Router does when only the parameter changes), recording A's panel stays hidden on return.
- **Why:** the other two one-off dismissals on this page (`cardDismissedFor`, `noticeDismissedFor`) are keyed by `location.key`, so they reset on each arrival. This one doesn't.
- **Fix:** key it by `location.key` like the other two.

### 4. Copy rows show wrong dimensions for some copies
`master-copies-panel.tsx:756-766`

- **What goes wrong:** a copy row's "W × H" isn't read from the copy. It's recomputed from the current page's probe and the copy's preset. Two cases go wrong:
  - **Copies of a copy:** with `source="copy"`, `probe` belongs to the copy whose page this is, not to the file each listed copy was made from. The numbers are only right when that file is the direct source.
  - **Reels/feeds copies:** `resolveExportTarget` is called without the copy's `framing`. A copy made with Fill is labelled with the default framing's size. That only matters for presets whose canvas size depends on the framing.
- **Severity:** labels only, nothing breaks.

### Smaller points (not bugs)
- **Heavy-to-send banner after "Not now":** on a heavy master with no copies, "Not now" now brings up the full banner (`heavy && !showDestinations`, line 2068). That seems intended, since the hint has to live somewhere, but the updated doc only mentions the banner for "a heavy copy, or a heavy master with copies."
- **Possibly dead i18n key:** `sendTo` is kept but moved to the end of the `library` block in en/es. It's still used by `video-card.tsx` and `video-row.tsx`, so that's fine. The removed `where*`, `copiesEmpty` and `copyProgress*` keys have no remaining callers. The two `etaSeconds`/`etaMinutes` strings combine correctly into "Exporting · 38% · 2 min left".
