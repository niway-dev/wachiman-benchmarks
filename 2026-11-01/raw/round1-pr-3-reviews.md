=== REVIEW 5730176711 2026-11-01T20:42:30Z commit=dac8318
👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

2 finding(s): 2 to consider; 2 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 has no bugs, only two small test suggestions. I read all five files in this part:

- **`destinations-panel.tsx` (new component):** I found no problems.
- **`master-copies-panel.tsx`:** I found no problems with the picture-size facts or the Drag handle. The Drag handle uses the existing `startFileDrag` call from the preload, so the Electron boundary is no wider than before.
- **`library-detail-page.tsx`:** I found no problems with the page layout or with the new conditions for when the "Where is it going?" panel, the copies panel and the heavy-to-send banner appear.
- **`where-is-this-going-strip.tsx`:** this file is deleted, and I found no problems with removing it.

The two suggestions are both in `master-copies-panel.test.tsx` and are optional:

1. **Shared mock left replaced:** the Drag test overwrites the shared `electronAPI.startFileDrag` mock and never puts it back. The existing drag test in `export-status-cards.test.tsx` uses a spy and restores it afterwards.
2. **Half-tested case:** the "Open in Export" test only checks that the button appears and works. It never checks that the button is hidden when no handler is passed, even though the test's name promises that.

**Batch 2 of 2.** Part 2 has no findings. I checked the tests in this part against `library-detail-page.tsx` and `destinations-panel.tsx`:
- **Destinations panel:** it shows only before the first copy and hides after "Not now" until the page is left. "Export a copy" is gated on the panel being hidden. The archive card shows the recording's own size, and the colour of each size follows the destination's group. The heavy-to-send hint sits inside the panel.
- **Master tag:** it appears twice, once by the title and once over the player.
- **Saved notice:** while it shows, the standing master note is hidden.

The backlog doc describes this behaviour accurately. That includes reading the file on every local recording, which is why the `probe not called` assertion was dropped. In the message files, the keys that were removed are no longer referenced. The keys that were kept or added (`sendTo`, `sendToHint`, `copiesHeadingCopy`, `copyExporting*`, `copyDragLabel`, `metaDimensions`, `metaCopies`) are all used by the renderer, and `en.json` and `es.json` stay in sync.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 6 | $0.24 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 7 | $0.28 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 2 batches · $0.52</sub>

<!-- wachi:review -->

<!-- agent-review sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=b96c962e-9faf-49b5-a288-21989c6feb3b -->

