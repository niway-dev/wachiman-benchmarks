<!-- cap-3, oauth-token-1: 20 turns, $1.1 -->

I found four bugs. The first defeats the main point of this PR. I read the whole diff and the code it calls, and changed no files. I did not run the tests or the app, so everything below comes from reading the code.

### 1. A long title overflows into the master tag instead of ending in "…"
**Where:** `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.module.css:61` (`.title`), together with `features/library/components/recording-title.module.css:1-15`

**What goes wrong:** The PR says the title "ellipsizes only at that edge", and its QA step says that at 900 × 670 "the title, tag and actions never truncate each other". With a long title, the text instead runs out of the box over the "MASTER · FULL QUALITY" tag, and the rename pencil is pushed under it.

**Why:** Only the wrapper `div.title` gets `flex: 1; min-width: 0`. Inside it, `RecordingTitle` renders its own flex row (`.titleRow`, with no `min-width`). The `<h1 class="title">` in that row is a flex item with the default `min-width: auto` and `white-space: nowrap`, so it can never be narrower than its text, and `text-overflow: ellipsis` never applies. The wrapper has no `overflow: hidden` either, so the text paints past it. Fixing it needs `min-width: 0` on the `<h1>`, plus `min-width: 0` or `overflow: hidden` on the inner row.

### 2. The page flips back to "Where is it going?" for a moment when the first copy finishes
**Where:** `library-detail-page.tsx:189-191`, with `export-runner.ts:462` and `library-detail-page.tsx:146-148`

**What goes wrong:** While the first copy encodes, `running` is set, so the page shows "Copies from this original" and the "Export a copy" button. When the encode finishes, the runner sets the status back to idle (`set({ ...IDLE, ready })`), so `running` becomes `null`. But `exports` still comes from the old Library list until the `refresh()` started by the `readyId` effect comes back. For that gap, `hasCopies` is false and `showDestinations` is true: the copies panel disappears, the destinations panel and its "Not now" come back, and "Export a copy" disappears. Then it all flips again once the new list arrives.

**Why:** Before this PR the copies panel stayed on screen for any master (`showCopies = master || …`), so there was no gap. The new logic depends only on `exports` and `running`, and the hand-off between them isn't atomic.

### 3. If the file can't be read, the destination cards show "…" forever
**Where:** `library-detail-page.tsx:142` and `destinations-panel.tsx:263, 311`

**What goes wrong:** The page keeps only `useSourceProbe(...).probe`. That is `null` both while the file is being read and after reading fails (`status: "error"`). `DestinationsPanel` shows `size ?? "…"`, so on a file that can't be read, every card except the archive one looks like it is still loading, permanently.

**Why:** The probe's `status` is thrown away. Before this PR the page read the file only for the heavy banner, which had a text for this case (`heavyBannerBodyNoEstimate`). This PR reads the file for every local recording and has no fallback for a failed read.

### 4. Dragging a copy out from the recording page doesn't mark it as seen
**Where:** `master-copies-panel.tsx:171-175`

**What goes wrong:** The ready card's Drag handler (`export-status-cards.tsx:231-235`) calls `markCopySeen(recording.assetId)` before `startFileDrag`. The new Drag handle only calls `startFileDrag`. Drag a copy out from the master's page and the Library badge and "copy ready" hint (NIW2-586) still point at it as unseen, even though the user has just used it. The docs describe this handle as going "through the same IPC as the ready card", but it skips that step.

**Why:** `markCopySeen(copy.assetId)` is missing from the `onDragStart` handler.
