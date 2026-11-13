# Wachiman review of branch `bench/pr-184` of pr-184 against origin/replay/pr-184/base (merge-base 06388e6), at 2c33d5b

All 7 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

6 finding(s): 3 to fix, 3 to consider

## Findings

### 🟠🐛 **Fix · bug: Video text hit-test still sizes multi-line labels from text.length and one line of height (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:488`

The PR fixes the selection outline in overlay-shapes.tsx (now `textBoxPx`, lines 116 and 144-145), but `hitTest` for text kept the old arithmetic: `w = o.text.length * fs * 0.55` and `h = fs * 1.3` (lines 488-489). Two consequences for a label with a line break:
- The height is one line, so the lower line(s) are outside the hit box. Clicking them does not select the label, does not start a move, and a double-click on them does not reopen the editor (`onDoubleClick` relies on this same `hitTest`, line 182). A click there falls through to empty space and fires `onBackgroundClick`.
- The width counts the `\n` characters, so clicks to the right of a short line, within the total character count, select the label and swallow the background click.

The comment at lines 482-484 says the hit box matches the rendered bounds in overlay-shapes.tsx, which is no longer true. The commit message for overlay-shapes calls this exact defect ("half of it was not selectable"), and the same defect remains here.

Fix: derive the box from the shared helper, as overlay-shapes and handles.ts (`annotationBox`) already do: `const box = textBoxPx(o.text, fs); const w = box.w / (size.w || 1); const h = box.h / (size.h || 1);`, keeping the padding.

### 🟠🐛 **Fix · bug: Re-editing a multi-line label opens a textarea showing only its first line (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:402`

The textarea is rendered with `rows={1}` and `defaultValue={editingText.initialText}` (lines 402-408). Nothing sets its height on mount: the inline style has no `height` (lines 412-422), the CSS module's `.textInput` sets none either (video-annotation-layer.module.css:33-43, `overflow` is not set to visible), and the only autosize is `onInput` (lines 424-429), which runs only when the user types.

So double-clicking a label such as "first\nsecond" opens the editor with the second line clipped. The user cannot see what they are editing until they type a key. Committing without typing still saves the full value, so this is a visibility defect, not data loss.

Fix: size the textarea once it mounts, e.g. in the effect at lines 160-170, set `textInputRef.current.style.height = `${textInputRef.current.scrollHeight}px`` alongside the focus call, or pass `rows` equal to the initial line count.

### 🟠🐛 **Fix · bug: Re-edit editor uses the toolbar's size and colour, not the label's own (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:417`

`onDoubleClick` stores only `{x, y, id, initialText}` in `editingText` (line 186). The textarea then takes `color: toolState.color` and `fontSize: TEXT_PX[toolState.textSize]` (lines 415 and 417), not the overlay's own `o.color` and `o.size`.

Reopening a label whose colour or size differs from the current toolbar setting shows it in the wrong size and colour while editing. The label keeps rendering with its real style underneath (its SVG is still drawn, and the CSS background is only `rgba(0,0,0,0.04)`, so both show). After commit only `text` changes (line 342), so the label then jumps to its real size and colour. The user sees a mismatch, and the editor never shows what they will get.

Fix: carry `size` and `color` from the hit overlay into `editingText` on re-edit (line 186), and use them at lines 415 and 417. Fresh labels keep `toolState`.

### 🟡🐛 **Consider · bug: Clearing a label while re-editing reverts it instead of removing it, unlike the screenshot editor (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:337`

`commitText` only acts when `text` is non-empty (line 337). Clearing a label and pressing Enter therefore closes the editor and leaves the old text in place. The screenshot editor, which this change says it mirrors (see the comment at line 177), deletes the annotation in this case (annotation-layer.tsx:302-310: "or delete it if the user cleared the text (Excalidraw-style)").

The user sees their clear undone, with no error. They can still delete the overlay with Delete/Backspace. Whether the video editor should match the screenshot editor is a product decision. If it should, the re-edit branch needs an `else` that removes the overlay as one undoable change.

### 🟡🐛 **Consider · bug: Double-clicking inside the open editor can retarget the edit to another label (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:179`

`onDoubleClick` on the layer has no check on its target and does not check `editingText`. The open textarea is a DOM child of the layer, and its `onPointerDown` stops propagation (line 423) but its double-click does not. So a double-click inside the editor (e.g. to select a word) reaches this handler. When the tool is `select` (the re-edit case; the text tool returns early at line 180), `hitTest` runs at that point. If a different visible label overlaps and is topmost, `setEditingText` switches the target to that label, with its id and text. The typed text, still in the textarea, is then committed onto the other label (lines 338-344), and the label being edited keeps its old text.

The overlap needs to be present, so I rate this medium. Fix: return early when an edit is already open, e.g. `if (editingText || tool !== "select") return;`.

### 🟡🧪 **Consider · tests: No test covers the video overlay's hit-test or selection box for a multi-line label (confidence high)**

`apps/kaipu-record/src/renderer/src/features/screenshots/annotations/tools.test.ts:52`

The describe block at lines 52-68 is titled "textBoxPx, as the video overlay's box", but it only checks the shared helper's arithmetic. Nothing exercises the video overlay: not `hitTest` (video-annotation-layer.tsx:482-489), which still has the defect described in the hitTest finding, and not the selection rect in overlay-shapes.tsx. A test that clicks the lower line of a two-line label, or double-clicks it to reopen the editor, would have failed on this branch.

The Shift+Enter test (video-annotation-layer.test.tsx:329-333) asserts only that `onCommit` is not called. jsdom does not insert the newline, so the test would pass even if the key were swallowed. Its name, "does not commit on Shift+Enter", is accurate, but it does not check the line break itself. The prefilled-height problem (video-annotation-layer.tsx:402) is also untested, because `fireEvent.change` does not fire React's `onInput`.

## Summary

Reviewed all 7 files in this part. Export and rendering are consistent with the screenshot compositor, and the keyboard handling is safe. The main defects are in the video editor's text handling: (1) hitTest for text still uses the old one-line, character-count box, so multi-line labels cannot be selected or double-clicked on their lower lines (the same bug the PR says it fixed in the outline); (2) a prefilled multi-line label opens with only its first line visible; (3) the re-edit editor uses the toolbar's size and colour rather than the label's. Behaviour gap: clearing a label while re-editing reverts it, where the screenshot editor deletes it. The tests do not cover the hit-test or the multi-line selection path. Nothing was built or run, per the review instructions.

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Double-click on a text label reopens it in place (select tool) (`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:177-187`) — A textarea opens over the label, prefilled with its text, and Enter/blur commits the change as one onCommit with the same id, start and end. If it fails: A multi-line label opens with its second line clipped (video-annotation-layer.tsx:402). The editor uses the toolbar's size and colour, not the label's (line 417). Clearing the text reverts instead of… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:177-187`, `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:332-363`, `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:402-449`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/annotation-layer.tsx:136-142`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/annotation-layer.tsx:302-310`, `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.module.css:33-43`.
- Textarea onBlur and Enter commit the re-edit (commitText, re-edit branch) (`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:332-363`) — The label's text changes in place, and the label keeps its timeline window. Undo reverts it in one step. If it fails: Empty text reverts silently (no error, the old text stays). The screenshot editor deletes it, so the two editors differ. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:332-363`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/annotation-layer.tsx:295-312`.
- Shift/Alt+Enter inserts a newline in the textarea; plain Enter commits (`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:430-441`) — The caret moves to a new line and the textarea grows through onInput (line 424-429). If it fails: The window keydown in the video editor returns early for TEXTAREA targets (video-editor-page.tsx:164 and 833), so Space, Delete, Backspace and S do not fire editor shortcuts while typing. This was ch… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:424-441`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/annotation-layer.tsx:387-393`, `apps/kaipu-record/src/renderer/src/pages/video-editor/video-editor-page.tsx:164`, `apps/kaipu-record/src/renderer/src/pages/video-editor/video-editor-page.tsx:833-836`.
- Export rasterizes a text overlay with one tspan per line (`apps/kaipu-record/src/renderer/src/features/video-editor/export/overlay-raster.ts:91-103`) — The exported frame shows each line of the label at the same vertical spacing as the preview. If it fails: If rasterize rejects (SVG load error, lines 135-138), rasterizeOverlays rejects through Promise.all, so the export fails. This predates the PR and is not changed by it. A line break survives as a tsp… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/overlay-raster.ts:91-103`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/overlay-raster.ts:117-141`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/compositor.ts:184-191`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/tools.ts:76-78`.
- Selected text label shows its outline from textBoxPx (overlay-shapes) (`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/overlay-shapes.tsx:113-146`) — The outline wraps all lines (height from the line count, width from the longest line). If it fails: The outline is correct, but clicks on it are not: the hit test still uses the old arithmetic (video-annotation-layer.tsx:488-489). A click on the lower lines of the outline does not select the label.… Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/overlay-shapes.tsx:113-146`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/handles.ts:76-85`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/tools.ts:114-126`, `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:482-489`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 1 | 7 | 262 | 4 | reviewed | 18 | $0.04 |

Cost: $0.04, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 1 call(s), 18 turn(s), 2 min 31 s.

stop: complete

Claude Haiku 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of 2c33d5b below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:488 · 🟠🐛 Fix · bug: Video text hit-test still sizes multi-line labels from text.length and one line of height (confidence high)
   The PR fixes the selection outline in overlay-shapes.tsx (now `textBoxPx`, lines 116 and 144-145), but `hitTest` for text kept the old arithmetic: `w = o.text.length * fs * 0.55` and `h = fs * 1.3` (lines 488-489). Two consequences for a label with a line break:
   - The height is one line, so the lower line(s) are outside the hit box. Clicking them does not select the label, does not start a move, and a double-click on them does not reopen the editor (`onDoubleClick` relies on this same `hitTest`, line 182). A click there falls through to empty space and fires `onBackgroundClick`.
   - The width counts the `\n` characters, so clicks to the right of a short line, within the total character count, select the label and swallow the background click.

   The comment at lines 482-484 says the hit box matches the rendered bounds in overlay-shapes.tsx, which is no longer true. The commit message for overlay-shapes calls this exact defect ("half of it was not selectable"), and the same defect remains here.

   Fix: derive the box from the shared helper, as overlay-shapes and handles.ts (`annotationBox`) already do: `const box = textBoxPx(o.text, fs); const w = box.w / (size.w || 1); const h = box.h / (size.h || 1);`, keeping the padding.
2. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:402 · 🟠🐛 Fix · bug: Re-editing a multi-line label opens a textarea showing only its first line (confidence high)
   The textarea is rendered with `rows={1}` and `defaultValue={editingText.initialText}` (lines 402-408). Nothing sets its height on mount: the inline style has no `height` (lines 412-422), the CSS module's `.textInput` sets none either (video-annotation-layer.module.css:33-43, `overflow` is not set to visible), and the only autosize is `onInput` (lines 424-429), which runs only when the user types.

   So double-clicking a label such as "first\nsecond" opens the editor with the second line clipped. The user cannot see what they are editing until they type a key. Committing without typing still saves the full value, so this is a visibility defect, not data loss.

   Fix: size the textarea once it mounts, e.g. in the effect at lines 160-170, set `textInputRef.current.style.height = `${textInputRef.current.scrollHeight}px`` alongside the focus call, or pass `rows` equal to the initial line count.
3. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:417 · 🟠🐛 Fix · bug: Re-edit editor uses the toolbar's size and colour, not the label's own (confidence high)
   `onDoubleClick` stores only `{x, y, id, initialText}` in `editingText` (line 186). The textarea then takes `color: toolState.color` and `fontSize: TEXT_PX[toolState.textSize]` (lines 415 and 417), not the overlay's own `o.color` and `o.size`.

   Reopening a label whose colour or size differs from the current toolbar setting shows it in the wrong size and colour while editing. The label keeps rendering with its real style underneath (its SVG is still drawn, and the CSS background is only `rgba(0,0,0,0.04)`, so both show). After commit only `text` changes (line 342), so the label then jumps to its real size and colour. The user sees a mismatch, and the editor never shows what they will get.

   Fix: carry `size` and `color` from the hit overlay into `editingText` on re-edit (line 186), and use them at lines 415 and 417. Fresh labels keep `toolState`.
4. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:337 · 🟡🐛 Consider · bug: Clearing a label while re-editing reverts it instead of removing it, unlike the screenshot editor (confidence high)
   `commitText` only acts when `text` is non-empty (line 337). Clearing a label and pressing Enter therefore closes the editor and leaves the old text in place. The screenshot editor, which this change says it mirrors (see the comment at line 177), deletes the annotation in this case (annotation-layer.tsx:302-310: "or delete it if the user cleared the text (Excalidraw-style)").

   The user sees their clear undone, with no error. They can still delete the overlay with Delete/Backspace. Whether the video editor should match the screenshot editor is a product decision. If it should, the re-edit branch needs an `else` that removes the overlay as one undoable change.
5. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:179 · 🟡🐛 Consider · bug: Double-clicking inside the open editor can retarget the edit to another label (confidence medium)
   `onDoubleClick` on the layer has no check on its target and does not check `editingText`. The open textarea is a DOM child of the layer, and its `onPointerDown` stops propagation (line 423) but its double-click does not. So a double-click inside the editor (e.g. to select a word) reaches this handler. When the tool is `select` (the re-edit case; the text tool returns early at line 180), `hitTest` runs at that point. If a different visible label overlaps and is topmost, `setEditingText` switches the target to that label, with its id and text. The typed text, still in the textarea, is then committed onto the other label (lines 338-344), and the label being edited keeps its old text.

   The overlap needs to be present, so I rate this medium. Fix: return early when an edit is already open, e.g. `if (editingText || tool !== "select") return;`.
6. apps/kaipu-record/src/renderer/src/features/screenshots/annotations/tools.test.ts:52 · 🟡🧪 Consider · tests: No test covers the video overlay's hit-test or selection box for a multi-line label (confidence high)
   The describe block at lines 52-68 is titled "textBoxPx, as the video overlay's box", but it only checks the shared helper's arithmetic. Nothing exercises the video overlay: not `hitTest` (video-annotation-layer.tsx:482-489), which still has the defect described in the hitTest finding, and not the selection rect in overlay-shapes.tsx. A test that clicks the lower line of a two-line label, or double-clicks it to reopen the editor, would have failed on this branch.

   The Shift+Enter test (video-annotation-layer.test.tsx:329-333) asserts only that `onCommit` is not called. jsdom does not insert the newline, so the test would pass even if the key were swallowed. Its name, "does not commit on Shift+Enter", is accurate, but it does not check the line break itself. The prefilled-height problem (video-annotation-layer.tsx:402) is also untested, because `fireEvent.change` does not fire React's `onInput`.
```
