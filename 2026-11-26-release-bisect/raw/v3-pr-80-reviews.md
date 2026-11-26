# kaipu-bench-wachi-v3#80 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:27:22Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

4 finding(s): 1 to fix, 3 to consider; 4 on their lines. Reply in a comment's thread to answer it.

**Risk map:** low — no risk facts in this change.
**Read first:** `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/where-is-this-going-strip.tsx`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx`.

### Summary

**Batch 1 of 2.** Part 1 replaces the \"Where is this going?\" strip with a destinations panel, moves the title row and actions on the recording page, and adds picture size, progress bars, Drag and \"Open in Export\" to the copies panel. Every card and button reaches Prepare through the existing `openPrepare` → `preparePath`. Nothing in the repository still references the removed strip, `copiesEmpty` or `copyProgress*`. Copy dimensions match what `resolveExportTarget` produces whatever the framing.

Findings:
- **Drag handle (fix):** it skips the `markCopySeen` call that the ready card's drag makes, so a copy dragged out stays \"unseen\" in the Library.
- **Destination cards (consider):** if the file read fails, they show \"…\" forever.
- **Open in Export test (consider):** its name says the button shows only when there is an export screen, but it never checks the case without one.

The description says \"seven destinations… Email is its own card\". `DESTINATION_IDS` in `features/prepare/destinations.ts` has six, with Email inside the chat card, and the test's \"Slack · Discord · Email\" label agrees with six. The description is wrong on this point.

**Batch 2 of 2.** I found nothing in this part that needs fixing; there is one optional test suggestion.

- **CSS:** every class the new and reworked components use exists in their stylesheets, and every custom property they reference is defined. Those are in `packages/tokens/css/tokens.css` or the renderer's `base.css`.
- **Removed i18n keys:** nothing in the app still uses them. `sendTo` stays because the Library card and row still use it. The en and es files change in step.
- **Tests:** the changed assertions match the page. It now reads the file for every local recording, the panel has six cards, and the copy facts are worked out from the master's probe.
- **Backlog doc:** it says the code has six destinations against the design's seven. That matches `DESTINATION_IDS`, and it contradicts the PR body's "Seven destinations… Email is its own card". The body is wrong; the doc is right.

The one finding is a "consider" on tests. No page test covers a master whose first copy is still exporting, the case where the copies panel replaces the destinations panel.

<details><summary>What the change connects to (8 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Clicking a "Where is it going?" card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The Prepare route opens with the destination preselected. If it fails: Synchronous navigation only; no async call. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:521`.
- The Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The file is dragged into another app, but the Library keeps outlining the copy as unseen. If it fails: startFileDrag returns void (fire-and-forget IPC), so a failed drag gives the user no signal; preventDefault stops the browser's own drag. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-235`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:9-10`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-58`, `apps/kaipu-record/src/shared/types/electron-api.ts:259`.
- The page reads the file for every local recording (it used to read it only for heavy recordings or when the card showed) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution in the metadata line, the estimate on each destination card and the picture size on each copy row. While the probe is null, the cards show "…" and the rows show only the file size. If it fails: On error the page drops the status, so the destination cards stay at "…" with no message (finding). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- A copy row's picture size is worked out from the source's probe and the copy's preset (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`) — "2560 × 1440 · 22 MB". If it fails: No async work; with no probe the row shows the size only. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:450-464`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:478-503`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:539-543`.
- The "Saved to your Library" notice and the "Not now" dismissal (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`) — The notice can show again after the user returns from Prepare with Back, even once a copy exists. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-133`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`.
- Clicking a "Where is it going?" destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router moves to /prepare/:assetId?to=<destination>. The test at library-detail-page.test.tsx:253-266 checks all six search strings. If it fails: This is plain navigation: no async call and no IPC. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-83`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- "Not now" hides the destinations panel and brings back "Export a copy" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts and the primary "Export a copy" button shows (`!showDestinations`). The doc says the panel stays hidden "for that visit". If it fails: Nothing is persisted, so nothing can be lost. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:101-103`.
- Green "Saved to your Library" notice after a fresh recording, dismissable with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A role=status notice appears above the player. After ✕, the line "This is your original. It never changes." appears (test at :868-881). If it fails: Browser Back to the same entry remounts the page with the history state still set, so the notice shows again. The card behaves the same way, so this is consistent. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 16 | $0.66 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 15 | $0.60 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 38 in / 19k out / 1.0M cache read / 135k cache write · $1.25</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=3e6023c8-e887-4ff3-a419-c2455b7d41db -->
