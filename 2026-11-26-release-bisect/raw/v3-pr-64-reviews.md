# kaipu-bench-wachi-v3#64 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T01:33:47Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

6 finding(s): 5 to consider; 5 on their lines. Reply in a comment's thread to answer it.

### For your information

- ⚪📝 **Info · docs: The PR description says seven destinations; the code and this doc say six (confidence high)** (`apps/documentation/src/content/docs/backlog/prepare-screen.md:114`): The pull request body says "Seven destinations, as in the design. Since the export-screen merge, Email is its own card." `DESTINATION_IDS` lists six (`youtube, vertical, square, github, chat, archive`, `features/prepare/destinations.ts:36-43`), and email is still part of `chat` ("Slack · Discord · Email", which the test at `library-detail-page.test.tsx:258` expects). This doc's line 114 is correct. Only the PR description is wrong, so update it before QA. Otherwise step 4 of "How to test" has the reviewer looking for a seventh card.

### Summary

**Batch 1 of 2.** This part replaces the \"Where is this going?\" strip with a six-card DestinationsPanel, which shows only until the master's first copy exists. It also rebuilds the copies panel (two to a row, picture size, a Drag handle, \"Open in Export →\") and reorders the library detail page.

I found no blockers. There are four suggestions, all at \"consider\":
- **Drag doesn't mark the copy as seen.** The new Drag handle skips the `markCopySeen` call that the ready card's drag makes, so a copy dragged out from the panel stays outlined as unseen in the Library.
- **A failed probe looks like endless loading.** The page passes the probe without its status, so if the file can't be read, the destination cards show \"…\" forever.
- **One test doesn't cover what its name says.** The \"Open in Export →\" test never checks that the button is absent without `onOpenExport`.
- **One test leaves a mock behind.** The drag test overwrites the global `startFileDrag` stub and never restores it.

**Batch 2 of 2.** Part 2 (tests, stylesheets, docs, i18n): nothing blocking. The tests follow the new layout. They cover the title row, the six destination cards and their `?to=` values, Not now leading to Export a copy, the Saved notice and its interplay with the master note, the copies grid with its Drag handle, and the heavy hint folded into the panel. Removing the \"file isn't read below 25 MB\" assertion matches the new always-probe behaviour. Every CSS variable used is defined in tokens.css or base.css, and every class the components reference exists. No removed i18n key is still referenced; `sendTo` stays for the Library cards, and en and es have the same keys. The backlog doc's six-destination note is correct. The PR description's claim of seven destinations (Email as its own card) is not, and one consider-level finding covers the awkward \"Export a copy for Archive copy\" label.

<details><summary>What the change connects to (10 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- When a background copy finishes, the page switches from destinations to copies (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:144-148`) — Does the export runner go from "exporting" to a non-exporting status in the same update that sets `ready`, and how long does refresh() take? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts`.

**Closed, with the lines they rest on**
- Pick a destination card in "Where is it going?" (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — Opens the Prepare/Export screen with that destination chosen. If it fails: Synchronous navigation only; nothing async. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`.
- "Not now" dismisses the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel hides and the "Export a copy" button appears (showDestinations is false). Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`.
- The source is now probed on every preparable page (before, only when heavy or when the card showed) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Dimensions in the metadata line, card estimates and copy dimensions. If it fails: On a probe error, status is "error" with probe null. The page drops the status, so the dimensions meta is hidden (fine) but the destination cards show "…" indefinitely. If probeSource rejects, the st… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — A native drag of the copy file. The Library's unseen outline and chip are not cleared. If it fails: Fire-and-forget IPC send. Main validates the id (no slashes or ..) and silently returns on a bad one. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:232-235`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:9-10`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-58`, `apps/kaipu-record/src/main/library/index.ts:161-163`, `apps/kaipu-record/src/preload/index.ts:87`.
- Copy row facts: the picture size from resolveExportTarget(preset, probe) (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`) — "2560 × 1440 · 22 MB", or just the size when there is no probe or no preset. If it fails: No probe: only the size is shown. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:187`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:273`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:280`.
- Clicking a "Where is it going?" destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — The router goes to /prepare/:assetId?to=<id>. The test checks all six destinations. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-93`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`.
- "Not now" hides the destinations panel and brings back "Export a copy" (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel is removed. Export a copy appears because showDestinations is false, and the heavy banner shows on a heavy master. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:138-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:101-102`.
- "Saved to your Library" notice shown on a fresh recording, dismissed with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A green status row appears above the player, and while it shows the masterNote line is hidden. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:868-881`.
- The Drag handle on a copy row starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The file is dragged out to Finder or another app. If it fails: startFileDrag is fire-and-forget, as on the existing card. Nothing in the renderer shows a failed drag. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-180`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:108-109`.
- The page now reads (probes) the file for every local recording (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution appears in the metadata line, and the destination cards and copy rows get size and picture estimates. If it fails: When the probe is unusable, the state becomes error with probe null. The non-archive cards then show "…" for good, the resolution never appears, and no error is shown. This is silent but harmless. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-63`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:757-771`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 12 | $0.52 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 17 | $0.66 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · 2 batches · $1.17</sub>

<!-- wachi:review -->

<!-- agent-review sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=0ed687a1-7eb0-481c-9a8e-da998c206e90 -->
