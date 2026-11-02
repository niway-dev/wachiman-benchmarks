## review by pullfrog[bot] at 2026-11-01T23:35:00Z

> [!IMPORTANT]
> Removing the Library's window drop handling likely lets a dropped video navigate the whole Electron window away from the app. Recent exports also labels editor exports as destination copies.

**Reviewed changes**

I reviewed the full diff: the new Export screen and rail entry, the Prepare removal, the routing and redirects, the Email destination, the Library cleanup, and the i18n changes.

- **Export screen** — `pages/export/*` replaces `pages/prepare/*` with a fixed header, a stage that scrolls on its own, a fixed destination row, and document-level Enter / ←→ handling.
- **Routes** — adds `/export/:assetId` and `/export`. Legacy `/prepare*` URLs redirect there and keep `?to=`. `preparePath` / `prepareNewPath` now return Export URLs.
- **Email destination** — a new `DestinationId` that uses chat's `balanced` preset. `usePrepareCopy` accepts a `destination` override so the cards can name it.
- **Rail** — a new EXPORT entry sits under Editor. The copy badge moves there from Library and now also counts the export that is running.
- **Library** — the drop strip, the Import / Prepare buttons and the window-wide `useFileDrop` are removed, and `ImportDropZone` is deleted.

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


<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [Fix all ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog-v2/6?action=fix&review_id=5730802385) ｜ [Fix 👍s ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog-v2/6?action=fix-approved&review_id=5730802385) ｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog-v2/actions/runs/41362578203/job/125015904071) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

