<!-- cap-0.75, api-key-2: 17 turns, $0.6 -->

I found two real bugs and one smaller inconsistency. I read the diff and the code it calls (`destinations.ts`, `resolveExportTarget`, `useSourceProbe`, `asPreparable`, `MasterTag`, the router and the existing `startFileDrag` callers). I didn't run the tests or change any files.

### 1. Destination cards show "…" forever when the file can't be read
**`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`** (and line 311 in the diff, `{size ?? "…"}`)

- **What goes wrong:** `estimate()` returns `null` whenever `probe` is null, and the card then shows "…" as a loading placeholder. But `useSourceProbe` also returns `probe: null` when the read fails (`{ status: "error", probe: null }`, `use-prepare-copy.ts:55-57`). It does the same when the probe isn't usable, for example a duration of 0.
- **Why it matters:** if the file is corrupt or the probe fails, the YouTube, Reels, LinkedIn, GitHub and Slack cards show "…" permanently, as if still loading. The panel only receives `.probe` (the page passes `useSourceProbe(...).probe`), so it can't tell "loading" from "failed".
- **Why it's new:** before this PR, the page only read the file for heavy recordings or the post-recording card, and no UI showed a pending state for it.
- **Fix:** pass the probe `status` down and show nothing (or "—") on `error`.

### 2. "Not now" survives leaving the page
**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139` and `:191-192`**

- **What goes wrong:** `destinationsDismissedFor` is keyed by `video.assetId` and lives in component state. In `app/router.tsx:67`, `<LibraryDetailPage />` has no `key`, so moving from one `/library/:assetId` to another keeps the same component instance and its state.
- **Example:** dismiss the panel on master A, open a copy's page (or any other detail page by link), then follow "Source" back to A. A still matches the stored id, so the panel stays hidden.
- **Why it's a bug:** the code comment says "hidden for this recording until the page is left" and the doc says "for that visit".
- **Fix:** key the dismissal by `location.key`, as the saved notice (`noticeDismissedFor`) and the card (`cardDismissedFor`) already do.

### 3. (Minor) Dragging a copy from the panel doesn't mark it as seen
**`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`**

- **What goes wrong:** the new Drag handle calls `startFileDrag(copy.id!, copy.title)` but not `markCopySeen(copy.assetId)`.
- **Why it matters:** the ready card's drag, which the doc says this one mirrors ("the same IPC as the ready card"), does both (`export-status-cards.tsx:233-235`), and its test asserts that dragging "counts as seen". After a drag from the recording page, the NIW2-586 "unseen copy" badge or toast can keep pointing at a copy the user has already dragged into another app.

### Checked and fine
- `startFileDrag(id, name)` matches the preload and main signatures. Calling `preventDefault()` before the native drag follows the existing GIF viewer and ready-card pattern.
- `resolveExportTarget(preset, probe, probe.durationSec)` and the `planCopy`/`presetForDestination` arguments match their signatures.
- The archive card is in the `keep` group, so it gets the teal "light" tone, as the test expects.
- `MasterTag` accepts `size="sm"`.
- All the i18n keys used (`sizeAbout`, `sizeUpTo`, `sizeFull`, `etaSeconds`, `etaMinutes`, the `dest*`/`line*` keys and the new library keys) exist. `en` and `es` are the only locales, and both were updated.
- Probing every local recording, not just heavy ones, is an intentional change and its test was updated to match.
