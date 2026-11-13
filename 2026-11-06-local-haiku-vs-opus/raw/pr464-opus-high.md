# Wachiman review of branch `bench/pr-464` of pr-464 against origin/replay/pr-464/base (merge-base 13b7ff5), at e45c845

All 31 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

2 finding(s): 1 to fix, 1 to consider

## Findings

### 🟠🐛 **Fix · bug: Show in Finder / drag on the Library ready card don't mark the copy seen (confidence high)**

`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`

The ready status card does the same two actions, and both call `markCopySeen(recording.assetId)` before the IPC call (export-status-cards.tsx:280 and :293). The ready-copies contract says the same thing: a copy stays unseen until the user opens it "or acts on its ready card (Show in Finder, drag it out)" (ready-copies.ts:10-11). The new Library card calls `revealLocalRecording` (line 80) and `startFileDrag` (line 93) without it. So when the user reveals the file or drags it into YouTube Studio from this card, the "Ready to upload" card stays, the "1 copy ready" chip keeps counting it, and the regular card keeps its outline after the card retires. Fix: call `markCopySeen(video.assetId)` in both handlers (or pass an `onActed` callback from library-page, the way `onOpen` already does), and add an assertion to the existing "Show in Finder reveals the file" test.

### 🟡🧹 **Consider · cleanup: File name's extension is guessed from the kind, not taken from the file (confidence medium)**

`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:38`

`ExportReadyCard` takes the extension from the real file path (`recording.filePath.match(/\.[a-z0-9]+$/i)`, export-status-cards.tsx:243). This card hardcodes `.mp4`/`.gif` from `video.kind`. If a recording copy is ever saved under a different container (for example .mov or .webm), the visible name and the drag button's label would name a file that doesn't exist. Consider deriving it from `video.filePath`, if `LibraryVideo` has it.

## Summary

**Batch 1 of 2.** Part 1: one fix-level finding. On the new Library \"Ready to upload\" card, Show in Finder and the drag don't call markCopySeen, while the ready status card's same actions do (export-status-cards.tsx:280 and :293). After acting, the copy keeps its card, its chip count and its outline. There is also a minor suggestion about the hardcoded file extension. The widget's sessionStorage handling, the sidebar's card retirement and copyPresetOf's fingerprint parsing check out.

**Batch 2 of 2.** Part 2 (stylesheets, backlog docs and i18n messages): no findings. I checked the backlog doc's claims against the code and they hold: retireReadyCards is called from the sidebar's route hook, the minimized state lives in sessionStorage, the widget minimizes with a − icon, and progressHidden/hideExportProgress are gone. The renderer no longer uses the removed keys `hide` and `readyDragToUpload`, and en and es have the same keys. The destination tag colours match destination-logo.module.css. The two-column ready card fits because the Library grid always has three columns.

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Show in Finder and native drag on the Library "Ready to upload" card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — After acting, the ready card, the unseen chip and the outline all stay until the user opens the copy or leaves the Library. If it fails: revealLocalRecording is fired with `void`, the same as the sibling, so a rejection is silent. startFileDrag is a send and gets no reply. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:280`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:293`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:10-11`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:93`.
- The minimized state of the export widget is read from and written to sessionStorage (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10`) — The widget opens expanded when storage can't be read. If it fails: Treating an unreadable value as empty does no harm: nothing writes the default back, and the only write follows a user action, so no stored value is overwritten. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-18`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:25-35`.
- Leaving the Library route retires every Ready to upload card (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102`) — The next visit to the Library opens on the plain grid. Cards for copies hidden by filters are retired too. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:95-104`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:97-100`.
- Export widget and ready toast render in a new fixed bottom-right stack instead of the top-right page stack (`apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19`) — The progress widget, its pill and the ready toast show bottom right on every screen because the provider is mounted at the app root; the pill turns pointer-events back on (export-status-cards.module.css:77). Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.tsx:24-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:2-12`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:76-93`.
- Ready to upload card spans two grid columns at the head of the Library grid (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:4`) — The card takes two of the three columns, and the meta line wraps (overflow-wrap: anywhere) at narrow widths. Evidence: `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:366-369`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:106-115`.
- i18n keys `hide` and `readyDragToUpload` removed; new keys `minimize`, `expand`, `pill`, `dragTo`, `destinationTag`, `readyToUpload`, `fromOriginal`, `readyCar… (`packages/i18n/messages/en.json:1413`) — The widget title reads "Exporting for …", the pill reads "<Destination> copy · N%", and the drag button reads "Drag to <destination>". Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:153`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:223`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:298`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:97`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.tsx:19`, `packages/i18n/messages/es.json:1413-1435`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 6 | $0.48 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 16 | $0.47 |

Cost: $0.96, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 2 call(s), 22 turn(s), 2 min 1 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of e45c845 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80 · 🟠🐛 Fix · bug: Show in Finder / drag on the Library ready card don't mark the copy seen (confidence high)
   The ready status card does the same two actions, and both call `markCopySeen(recording.assetId)` before the IPC call (export-status-cards.tsx:280 and :293). The ready-copies contract says the same thing: a copy stays unseen until the user opens it "or acts on its ready card (Show in Finder, drag it out)" (ready-copies.ts:10-11). The new Library card calls `revealLocalRecording` (line 80) and `startFileDrag` (line 93) without it. So when the user reveals the file or drags it into YouTube Studio from this card, the "Ready to upload" card stays, the "1 copy ready" chip keeps counting it, and the regular card keeps its outline after the card retires. Fix: call `markCopySeen(video.assetId)` in both handlers (or pass an `onActed` callback from library-page, the way `onOpen` already does), and add an assertion to the existing "Show in Finder reveals the file" test.
2. apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:38 · 🟡🧹 Consider · cleanup: File name's extension is guessed from the kind, not taken from the file (confidence medium)
   `ExportReadyCard` takes the extension from the real file path (`recording.filePath.match(/\.[a-z0-9]+$/i)`, export-status-cards.tsx:243). This card hardcodes `.mp4`/`.gif` from `video.kind`. If a recording copy is ever saved under a different container (for example .mov or .webm), the visible name and the drag button's label would name a file that doesn't exist. Consider deriving it from `video.filePath`, if `LibraryVideo` has it.
```
