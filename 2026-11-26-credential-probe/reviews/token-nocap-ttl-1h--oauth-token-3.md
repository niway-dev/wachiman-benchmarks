<!-- token-nocap-ttl-1h, oauth-token-3: 26 turns, $1.08 -->

I found two real bugs in the PR. Neither is a crash; both are wrong behaviour. I didn't run the tests and didn't modify any file.

### 1. The destination cards can show "…" forever
**Where:** `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263` and `:311`. The cause is upstream at `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`.

**What goes wrong:** If the file can't be read, five of the six cards in "Where is it going?" (all but Archive) show "…" for good. It looks like they are still loading.

**Why:**
- The page passes the panel only `useSourceProbe(...).probe`. That hook returns `probe: null` both while loading and when it fails (`status: "error"`). It fails whenever `probeSource` returns nothing usable, including when the width, height or duration is 0 (`isUsableProbe` in `use-prepare-copy.ts:29-31`).
- The panel maps any `null` to "…", so it can't tell "still reading" from "gave up".
- This PR makes the page read every local recording, not just heavy ones, so every recording that can't be read now hits this. Before, the only consumer was the heavy hint, which had its own "no estimate" wording (`heavyBannerBodyNoEstimate`).
- **Fix:** pass the probe status, or a "failed" flag, to the panel and show nothing or a "no estimate" text on error.

### 2. Dragging a copy out from "Copies from this original" doesn't mark it as seen
**Where:** `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`

**What goes wrong:** Suppose a copy has just finished and you drag it out from this panel. The Library still shows it as "copy ready", outlines it and counts it in its chip. Dragging the same file from the ready card clears all that.

**Why:**
- The docs say this Drag goes "through the same IPC as the ready card", and the ready card does two things on drag: it calls `markCopySeen(recording.assetId)`, then `startFileDrag` (`export-status-cards.tsx:231-236`).
- `ready-copies.ts:9-10` defines a copy as unseen until the user "opens it … or acts on its ready card (Show in Finder, drag it out)".
- The new handler only calls `startFileDrag(copy.id!, copy.title)`. Opening the copy's own page clears it (`sidebar.tsx:95`), but dragging it from the original's page doesn't.
- **Fix:** call `markCopySeen(copy.assetId)` in that `onDragStart`.

### Checked and fine
- **Translation keys:** the removed ones (`where*`, `copiesEmpty`, `copyProgress*`) aren't used anywhere else. `sendTo` is kept for `video-card.tsx` and `video-row.tsx`. Only `en` and `es` exist, and both have every new key.
- **Progress text:** `copyExporting` with `etaMinutes` reads "Exporting · 38% · 2 min left", with no doubled "left".
- **Size estimates:** the cards use the same `planCopy`, preset and default framing as the Prepare page, so the two agree. A copy row's picture size comes from `resolveExportTarget` on the recording's probe and the copy's preset.
- **Title row:** the title truncates with an ellipsis inside the row (`.title { flex: 1; min-width: 0 }` plus the `h1`'s `overflow: hidden`).
- **Heavy hint:** it shows inside the panel when the panel is up, and as the banner otherwise.
- **Tests:** `cleanup` is imported in the page test.
