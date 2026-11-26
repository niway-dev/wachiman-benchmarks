<!-- cap-0.75, api-key-1: 15 turns, $0.61 -->

I found two real bugs, both minor, in `master-copies-panel.tsx` and `library-detail-page.tsx`. The rest of the change checks out against the code it calls. I didn't run the tests or modify any files.

### 1. Dragging a copy from "Copies from this original" doesn't mark it as seen
**`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:834-838`**

The new Drag handle's `onDragStart` only calls `preventDefault()` and `window.electronAPI.startFileDrag(copy.id!, copy.title)`. The Drag button on the "copy ready" card does the same thing over the same IPC, but it also calls `markCopySeen(recording.assetId)` first (`features/status-cards/export-status-cards.tsx:231-235`, and the same for its Reveal button at line 221).

Apart from those two buttons, a copy is only marked seen when its own detail page opens (`shell/sidebar.tsx:95`). So if the user drags a copy straight into Finder or Slack from the master's page, the copy never gets marked seen. NIW2-586's Library badge then keeps pointing at that copy as unseen. The doc says this handle "starts a native file drag through the same IPC as the ready card", so the two should behave the same.

**Fix:** call `markCopySeen(copy.assetId)` in this `onDragStart` handler.

### 2. "Not now" stays in effect after the user leaves the page
**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139` and `190-191`**

The comment says "hidden for this recording until the page is left", and the doc says "hides the panel for that visit". But `destinationsDismissedFor` is keyed by `video.assetId` and stored in component state.

Moving between detail pages (master → a copy through its link → back through the "Source" link, or Library-row navigation between `/library/:assetId` URLs) keeps the same `LibraryDetailPage` instance mounted. So the master's "Where is it going?" panel stays hidden when the user comes back. Only routes that unmount the page, like `/library` or `/prepare/…`, reset it.

The saved notice right next to it is keyed by `location.key` (line 137) and does reset on each arrival. The panel should be keyed the same way, for example `destinationsDismissedFor !== location.key`.

### Checked and fine
- **Called functions:** the calls to `planCopy`, `presetForDestination`, `resolveExportTarget` and `groupOf` match their signatures. The tones are right: `send-more` is amber, while `keep-light` and `keep` (archive) are teal.
- **Probe guard:** `useSourceProbe` only returns a probe that passes `isUsableProbe`, so the new "W × H" metadata and the size estimates can't show 0 × 0 or a zero-duration estimate.
- **Drag file names:** `startFileDrag(id, title)` keeps the vault file's extension (`friendlyDragName(name, extname(file))` in `main/library/index.ts:171`), so a dragged GIF copy isn't renamed to a video file.
- **Removed i18n keys:** `where*`, `copiesEmpty` and `copyProgress*` are no longer used anywhere outside the deleted strip and the rewritten panel. Only `en` and `es` locales exist, and both were updated.
- **Panel usage:** `MasterCopiesPanel` is only used on the detail page, so dropping its empty state doesn't affect any other caller.
