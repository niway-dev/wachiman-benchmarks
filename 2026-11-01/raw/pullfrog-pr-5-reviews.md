=== REVIEW 5730239001 2026-11-01T20:59:23Z commit=b12d760
> [!IMPORTANT]
> Removing the Library's window drop handling means a file dropped on the Library is no longer `preventDefault`ed, so Electron navigates the window to the file instead of "doing nothing".

**Reviewed changes**

This is the initial review of the full PR. It replaces the Prepare screen with a dedicated Export screen and rail entry.

- **Export routes and legacy redirect.** Adds `/export/:assetId` and `/export`. `/prepare*` now redirects there and keeps `?to=`. `preparePath`/`prepareNewPath` now return Export URLs.
- **Export screen.** Adds a fixed header, a stage and a row of seven destination cards. A document-level keydown handler maps Enter to the primary action and ←/→ to the selection.
- **No-video state.** Adds a drop zone, a Library picker, Browse files and Recent exports, all built on the existing `usePrepareImport` window drop.
- **Email destination.** Adds a new `email` `DestinationId` over the `balanced` preset. `usePrepareCopy` takes a `destination` override so the progress and ready cards can name it.
- **Rail badge.** The badge moves from LIBRARY to EXPORT and now also counts the running export.
- **Library cleanup.** Removes the drop strip, the Prepare and Import buttons, the `useFileDrop` wiring and `ImportDropZone`.

<!--
Pullfrog review metadata. These findings were written against b12d760;
if commits have landed on replay/pr-467/head since, treat every specific bug, file, or
line callout as POTENTIALLY STALE and re-diff before acting on it.

- Mode: Review (initial)
- Files reviewed: 47
- Commits reviewed: 2
- Base: replay/pr-467/base (13b7ff5)
- Head: replay/pr-467/head (b12d760)
- Reviewed commits:
  - 36646c14 — feat(desktop): Export screen with its own rail entry (replaces Prepare)
  - b12d760b — docs(desktop): backlog page for the Export screen
- Prior pullfrog review: none
-->

### ℹ️ Leftover references to the removed Library import

The diff deletes these pieces but leaves references to them behind. Nothing breaks at runtime.

<details><summary>Technical details</summary>

````markdown
# Leftover references to the removed Library import

## Affected sites
- `apps/documentation/src/content/docs/backlog/import-video.md:112`: still lists `.../features/library/components/import-drop-zone.tsx`, which this PR deletes.
- `packages/i18n/messages/en.json:1487` and `es.json:1487`: `backgroundCopy.libraryBadge` has no callers now that the sidebar uses `export.railBadge`.

## Required outcome
- No docs pointing at deleted files, and no orphaned catalog keys.
````

</details>

<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [Fix all ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog/5?action=fix&review_id=5730239001) ｜ [Fix 👍s ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog/5?action=fix-approved&review_id=5730239001) ｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog/actions/runs/41349393299/job/124976089608) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

