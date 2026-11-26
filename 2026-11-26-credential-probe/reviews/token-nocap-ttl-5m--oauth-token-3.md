<!-- token-nocap-ttl-5m, oauth-token-3: 34 turns, $1.11 -->

I found three real bugs in the PR, none of which breaks a feature outright. Each one either leaves the page showing something wrong, or shows the wrong thing for a moment. I didn't modify any file and didn't run the tests.

### 1. The page flickers back to "before the first copy" when the first copy finishes
**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189-191`** (and how it's used at 436, 489, 507, 517)

```ts
const hasCopies = exports.length > 0 || running !== null;
const showDestinations = master && preparable !== null && !hasCopies && ...;
```

When the background export finishes, `export-runner.ts:462` switches the runner straight to idle (`set({ ...IDLE, ready: { job, recording } })`). That makes `running` null at once. The new copy only shows up in `exports` after the Library list is reloaded, and that reload is async: the `useEffect` on `readyId` (line 146) calls `refresh()` only after the render that already has `running === null`. For at least one render cycle, until the reload comes back, the master looks as if it has no copies:
- the copy's row and the "Copies from this original" panel disappear;
- "Where is it going?" comes back and the "Export a copy" button disappears;
- on a heavy master, the heavy-to-send banner turns back into the in-panel note.

Then everything flips back once the list arrives. If the reload is slow or fails, the page stays in the wrong state. Before this PR the copies panel always rendered for a master, so the worst case was a brief "No copies yet". Now the whole layout swaps. A fix is to count `runner.ready` as a copy when `runner.ready.job.sourceAssetId === video.assetId` and that copy isn't in `exports` yet.

### 2. Dragging a copy out of the copies panel doesn't mark it as seen
**`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`**

```ts
onDragStart={(e) => {
  e.preventDefault();
  window.electronAPI.startFileDrag(copy.id!, copy.title);
}}
```

The docs say this handle uses "the same IPC as the ready card". But the ready card's drag (`export-status-cards.tsx:234`) also calls `markCopySeen(recording.assetId)`. The rule in `ready-copies.ts:9-10` is that a copy stays unseen until the user opens it or acts on it, and dragging it out counts as acting on it. So after dragging a just-finished copy into Finder or Slack from here, the Library keeps outlining it and its "1 copy ready" chip keeps counting it. Fix: call `markCopySeen(copy.assetId)` in this handler.

### 3. Destination cards show "…" forever when the file can't be read
**`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263, 311`**, fed by **`library-detail-page.tsx:142`**

The page keeps only `useSourceProbe(...).probe` and drops `status`. When the probe fails, `useSourceProbe` returns `{ status: "error", probe: null }`. That can happen with a corrupt or unusual file, a zero duration, or a picture size it can't read. The panel can't tell this from "still loading": `estimate()` returns null and every card except Archive shows "…" with no end. Passing the status through and showing no size, or a "size unknown" text, on error would fix it.
