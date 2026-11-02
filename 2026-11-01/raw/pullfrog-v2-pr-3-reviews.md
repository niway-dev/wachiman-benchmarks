## review by pullfrog[bot] at 2026-11-01T23:34:27Z

> ℹ️ No critical issues. Three rough edges are noted inline.

**Reviewed changes**

This is the initial review of the full PR. It covers the Library's "Ready to upload" card, destination tags, the fingerprint revision fix, and the minimizable bottom-right export widget.

- **Ready to upload card**: `ReadyCopyCard` leads the grid for each finished copy, newest first. It only appears for copies the current filters show, and it replaces the copy's regular `VideoCard`.
- **`ready-copies` store**: `ReadyCopy` now carries `card`, `destination`, `width` and `height`. The new `dismissReadyCard`, `retireReadyCards` and `readyCards` manage the card's lifecycle.
- **Retire on leaving the Library**: `useLibraryBadge` tracks `wasOnLibrary` through a ref. `Sidebar` lives in `AppShell`, which hosts every route, so the hook sees every route change.
- **Destination tags**: `VideoCard` swaps the kind badge for a new `DestinationTag` on copies. The original keeps its master tag.
- **Fingerprint revision fix**: `copyPresetOf` / `copyDestinationOf` compare only the part of the fingerprint before `#`. `MasterCopiesPanel` now uses them, so YouTube/GitHub/chat copies are named by their destination.
- **Export widget**: the runner's `progressHidden` / `hideExportProgress` are replaced by a session-wide minimized state kept in `sessionStorage`. There is a new `ExportProgressPill` with a progress ring, errors always show in full, and the export cards move to a bottom-right `.exportStack`.
- **i18n**: the `backgroundCopy` wording is rewritten in `en` and `es`.

<!--
Pullfrog review metadata. These findings were written against e45c845;
if commits have landed on replay/pr-464/head since, treat every specific bug, file, or
line callout as POTENTIALLY STALE and re-diff before acting on it.

- Mode: Review (initial)
- Files reviewed: 31
- Commits reviewed: 3
- Base: replay/pr-464/base (13b7ff5)
- Head: replay/pr-464/head (e45c845)
- Reviewed commits:
  - ddcbe059 — fix(desktop): read a copy's destination through its encode revision
  - 3d1ae697 — feat(desktop): ready copy shows up in the Library; minimizable export widget
  - e45c8451 — docs(backlog): ready copy in the Library and the minimizable export widget
- Prior pullfrog review: none
-->

### ℹ️ The description's email wording is not in this diff

The description says email is its own destination, with "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag. But `DESTINATION_IDS` in `features/prepare/destinations.ts` has no `email`, and none of the new ICU `select` messages has an `email` branch. Either the description belongs to a different stack state, or that part of the change is missing. The `destinationTag` comment inline explains why this matters once `email` lands.

<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [Fix all ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog-v2/3?action=fix&review_id=5730800570) ｜ [Fix 👍s ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog-v2/3?action=fix-approved&review_id=5730800570) ｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog-v2/actions/runs/41362549508/job/125015816691) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

