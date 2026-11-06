# Wachiman review of branch `bench/pr-184` of pr-184 against origin/replay/pr-184/base (merge-base 06388e6), at 2c33d5b

All 7 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

5 finding(s): 3 to fix, 2 to consider

## Findings

### 🟠🐛 **Fix · bug: Hit-test still sizes text from `text.length` and one line height (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:488`

The selection outline now uses `textBoxPx` (overlay-shapes.tsx:116,144-145), and its comment says the old sizing left half the label unselectable. But `hitTest` still computes `w = o.text.length * fs * 0.55` and `h = fs * 1.3` (lines 488-489). On a multi-line label, a click or double-click on the second line or any line below it lands outside the hit box. The user can't select or move the label from there, and can't reopen it with the new double-click either. The hit area also stays far wider than the text, because `length` counts every line plus the newline characters. Fix: use `textBoxPx(o.text, fs)` for `w`/`h` here, the same way the outline does.

### 🟠🐛 **Fix · bug: A reopened multi-line label shows only its first line in the editor (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:170`

The textarea has `rows={1}` and `overflow: hidden` (lines 406, 421), and it only grows in `onInput` (lines 424-429). Setting `defaultValue` doesn't fire `input`, so when a multi-line label is reopened by double-click, only its first line is visible. The rest is hidden until the user types. The screenshot layer handles this in its open effect: it sizes the box to `scrollHeight` and moves the caret to the end (annotation-layer.tsx:115-121). This effect (lines 160-170) only focuses. Fix: run the same auto-size (and `setSelectionRange`) here.

### 🟠🐛 **Fix · bug: Re-edit box uses the current tool's colour and size, not the label's (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:415`

On re-edit, the textarea is still styled from `toolState.color` and `TEXT_PX[toolState.textSize]` (lines 415-417), and `editingText` doesn't store the label's own colour or size (lines 186, 131-136). Say a label is size L and red, and the toolbar is set to XS and pink. The editor then shows the text in a different size and colour from the label, and where the lines break no longer matches the rendered label. The screenshot layer stores `color`/`size` on double-click and uses `editing.color ?? tools.color` and `editing.size ?? tools.textSize` (annotation-layer.tsx:147-148, 374-376). Fix: do the same here.

### 🟡🐛 **Consider · bug: The label being re-edited is still drawn under the textarea (confidence high)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:387`

The SVG keeps rendering every visible overlay (lines 382-397), including the one with `id === editingText.id`. While the user edits, the original text shows under the textarea's live text, so both copies overprint each other. The screenshot layer hides the label it is editing (annotation-layer.tsx:351-352). Skip `o.id === editingText?.id` in this map.

### 🟡🧪 **Consider · tests: No test opens a multi-line label or hit-tests below its first line (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.test.tsx:315`

The new tests reopen only a one-line `"hello"` label by double-clicking at a single point. None of them double-clicks the second line of a multi-line label or reopens one, which are the cases the hit-test and auto-size bugs above break. Add a fixture with `text: "a\nb"` and double-click below the first line.

## Summary

The PR adds double-click re-editing and multi-line text to the video editor's text labels, and the export now keeps line breaks. The export side and the outline sizing are correct. Re-editing doesn't yet match the screenshot editor it copies:
- **Hit-test (fix):** clicks are still sized from `text.length` and one line height, so the lower lines of a multi-line label can't be selected, moved or reopened.
- **Editor height (fix):** a reopened multi-line label shows only its first line until the user types.
- **Editor style (fix):** the re-edit box takes the toolbar's colour and size instead of the label's.
- **Doubled text (consider):** the original label is still drawn under the edit box.
- **Tests (consider):** none of the new tests use a multi-line label.

<details><summary>What the change connects to (3 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Double-click a text label with the select tool to reopen it for editing (`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:179`) — The textarea opens prefilled. Its font and colour come from the toolbar, and a multi-line label shows only one line. The original label stays visible underneath. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:179-187`, `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:160-170`, `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:412-418`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/annotation-layer.tsx:115-121`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/annotation-layer.tsx:142-150`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/annotation-layer.tsx:351-352`.
- Commit re-edited text in place (`apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:338`) — onCommit gets the overlays with the text replaced. Start and end are kept. If it fails: If the text is cleared, the edit is dropped without a message and the old label stays. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:332-363`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/annotation-layer.tsx:302-312`.
- Render and export multi-line text as one tspan per line (`apps/kaipu-record/src/renderer/src/features/video-editor/export/overlay-raster.ts:97`) — Line breaks are kept in the preview and in the exported video. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/overlay-raster.ts:89-103`, `apps/kaipu-record/src/renderer/src/features/screenshots/annotations/tools.ts:69-78`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 1 | 7 | 262 | 4 | reviewed | 9 | $0.49 |

Cost: $0.49, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 1 call(s), 9 turn(s), 51 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of 2c33d5b below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:488 · 🟠🐛 Fix · bug: Hit-test still sizes text from `text.length` and one line height (confidence high)
   The selection outline now uses `textBoxPx` (overlay-shapes.tsx:116,144-145), and its comment says the old sizing left half the label unselectable. But `hitTest` still computes `w = o.text.length * fs * 0.55` and `h = fs * 1.3` (lines 488-489). On a multi-line label, a click or double-click on the second line or any line below it lands outside the hit box. The user can't select or move the label from there, and can't reopen it with the new double-click either. The hit area also stays far wider than the text, because `length` counts every line plus the newline characters. Fix: use `textBoxPx(o.text, fs)` for `w`/`h` here, the same way the outline does.
2. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:170 · 🟠🐛 Fix · bug: A reopened multi-line label shows only its first line in the editor (confidence high)
   The textarea has `rows={1}` and `overflow: hidden` (lines 406, 421), and it only grows in `onInput` (lines 424-429). Setting `defaultValue` doesn't fire `input`, so when a multi-line label is reopened by double-click, only its first line is visible. The rest is hidden until the user types. The screenshot layer handles this in its open effect: it sizes the box to `scrollHeight` and moves the caret to the end (annotation-layer.tsx:115-121). This effect (lines 160-170) only focuses. Fix: run the same auto-size (and `setSelectionRange`) here.
3. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:415 · 🟠🐛 Fix · bug: Re-edit box uses the current tool's colour and size, not the label's (confidence high)
   On re-edit, the textarea is still styled from `toolState.color` and `TEXT_PX[toolState.textSize]` (lines 415-417), and `editingText` doesn't store the label's own colour or size (lines 186, 131-136). Say a label is size L and red, and the toolbar is set to XS and pink. The editor then shows the text in a different size and colour from the label, and where the lines break no longer matches the rendered label. The screenshot layer stores `color`/`size` on double-click and uses `editing.color ?? tools.color` and `editing.size ?? tools.textSize` (annotation-layer.tsx:147-148, 374-376). Fix: do the same here.
4. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.tsx:387 · 🟡🐛 Consider · bug: The label being re-edited is still drawn under the textarea (confidence high)
   The SVG keeps rendering every visible overlay (lines 382-397), including the one with `id === editingText.id`. While the user edits, the original text shows under the textarea's live text, so both copies overprint each other. The screenshot layer hides the label it is editing (annotation-layer.tsx:351-352). Skip `o.id === editingText?.id` in this map.
5. apps/kaipu-record/src/renderer/src/features/video-editor/annotations/video-annotation-layer.test.tsx:315 · 🟡🧪 Consider · tests: No test opens a multi-line label or hit-tests below its first line (confidence medium)
   The new tests reopen only a one-line `"hello"` label by double-clicking at a single point. None of them double-clicks the second line of a multi-line label or reopens one, which are the cases the hit-test and auto-size bugs above break. Add a fixture with `text: "a\nb"` and double-click below the first line.
```
