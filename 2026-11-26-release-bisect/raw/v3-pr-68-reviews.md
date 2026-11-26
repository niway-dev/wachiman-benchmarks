# kaipu-bench-wachi-v3#68 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T01:43:53Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

3 finding(s): 3 to consider; 3 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 has no blockers and nothing at fix level. I read all five files in full, plus the code they call into: the destinations module, `resolveExportTarget`, `useSourceProbe`, the ready-copies store and the sibling `startFileDrag` callers. All three findings are at consider level:

- **Drag doesn't clear the copy's mark (bug):** the new Drag handle skips the `markCopySeen` call that the ready card makes before the same drag. A copy dragged out from \"Copies from this original\" stays outlined and counted in \"1 copy ready\" on the Library page.
- **Endless \"…\" (bug):** when the file can't be read, the destination cards show \"…\" forever, because the page passes only the probe value and not whether reading failed.
- **Half-tested (tests):** the \"Open in Export →\" test never checks that the button is missing when no export screen is passed.

Things I checked that hold:
- **Picture sizes:** the copy rows' sizes match the export, because canvas presets take their dimensions from the canvas whatever the framing.
- **Dismissals:** \"Not now\" and the Saved notice's ✕ use the same remount behaviour as the existing post-recording card.
- **Heavy banner:** it now shows on an original that has copies, which is what its comment says.

One note on the PR description: it says there are seven destinations with Email as its own card, but `DESTINATION_IDS` at the head lists six, and Email is still part of the chat card (\"Slack · Discord · Email\").

**Batch 2 of 2.** I found nothing to flag in this part's files.

- **Messages:** none of the removed i18n keys (`where*`, `copiesEmpty`, `copyProgress*`) is referenced anywhere in the repository. The new keys match between en.json and es.json and are used by the page and the panels.
- **Stylesheets:** every CSS token the new stylesheets use exists in packages/tokens. The stylesheet for the deleted strip is no longer referenced.
- **Tests:** the updated page tests match the new layout.
  - The archive card shows the recording's own size.
  - The other cards wait for the probe.
  - `cleanup()` was added before the second `renderDetail` call, and that is why the master-tag count went from 1 to 0.
  - The "up to 25 MB" test no longer asserts that the file is not probed. That matches the new behaviour, where every local recording is probed.
- **Docs:** the backlog doc is accurate against the code. It says the code has six destinations, and `DESTINATION_IDS` does list six.
- **PR description:** the description says something different under "Seven destinations, as in the design … Email is its own card". The code and the tests have six cards, with Email still part of Slack · Discord · Email. The description should be corrected; the files are fine.
- **Open question:** the Drag handle's IPC returns without doing anything when a file has no thumbnail. I couldn't confirm that every exported copy has one, so that contract is left open.

<details><summary>What the change connects to (8 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Drag handle on a copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — Does every destination copy written by the export runner have a thumbnail in the vault? If not, its Drag handle does nothing and gives no feedback. Files that would answer it: `apps/kaipu-record/src/main/library/index.ts`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts`.

**Closed, with the lines they rest on**
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — Main runs the native drag with the copy's title as the file name. The copy stays marked unseen on the Library page. If it fails: Fire-and-forget ipcRenderer.send, the same as the sibling. The handle only renders when the copy has a local id. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:9-10`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:95`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161`.
- Destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Navigates to Prepare with the destination preselected. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`.
- Probe the file for every local recording (estimates, resolution, copy picture sizes) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution appears in the metadata line, destination cards fill in their sizes, and copy rows gain picture sizes. If it fails: An unusable probe gives probe null: the metadata omits the resolution, copy rows show only the file size, and the destination cards show '…' indefinitely. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`.
- Copy row picture size from the original's probe and the copy's preset (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104`) — e.g. '2560 × 1440 · 22 MB'. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:482-503`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:187`.
- 'Not now' hides the destinations panel; 'Saved' notice ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel goes away and 'Export a copy' appears among the actions. The notice goes away and masterNote shows. If it fails: The state is lost on remount, so Back brings both back, the same as the existing post-recording card. This matches the PR's claim that the dismissal lasts until you leave the page. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`.
- Clicking a destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Router navigation to Prepare with that destination selected. The test covers all six cards (`?to=youtube` … `?to=archive`). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-82`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-42`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and brings back "Export a copy" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts, and showDestinations=false lets the Export a copy button and, on a heavy master, the heavy banner render. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:101-102`.
- "Saved to your Library" notice on a fresh recording, dismissed with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A green role=status notice above the player. While it shows, the masterNote line is hidden. After ✕ the masterNote line comes back (tested). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 15 | $0.60 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 19 | $0.70 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 44 in / 20k out / 1.2M cache read / 133k cache write · $1.30</sub>

<!-- wachi:review -->

<!-- agent-review sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=8934d531-ad92-452a-8212-27bd831518b1 -->
