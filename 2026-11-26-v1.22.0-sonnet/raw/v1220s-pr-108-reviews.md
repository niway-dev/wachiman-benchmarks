# kaipu-bench-wachi-v3#108 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:03:27Z · commit e45c845

👮 **Wachiman** · 🟡 **Nothing to fix · 3 to consider** · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 3 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Library ready card's Show in Finder / drag do not mark the copy seen |
| 🟡 Consider · Could · 🐛 bug | [`export-status-cards.tsx:216`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx#L216) | Progress percent inside the pill is hidden from assistive tech |
| 🟡 Consider · Could · 🐛 bug | [`library-page.tsx:126`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx#L126) | Ready cards are retired on leaving the Library even if the list view hid them |

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Leaving the Library retires every 'Ready to upload' card (route watch in the sidebar) (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92`) — The lead card is replaced by the regular outlined card on the next Library visit. The sidebar test covers this flow. If it fails: The Sidebar is not remounted on route changes, so the ref survives correctly. Router Back to /library re-announces and shows only cards that are still `card:true`. A copy finished while on /library/:… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-106`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:93-100`, `apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:50-63`.
- Read the destination of a copy back from its sidecar (copyPresetOf strips the '#revision' before comparing) (`apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:13`) — The 'For YouTube' tag and the destination logos show for real copies, both in the Library grid and in the Master copies panel. The job destination is `destinationOfPreset(preset)` (use-prepare-copy.ts:114), so the live and sidecar answers agree. If it fails: A file older than fingerprints returns null, so the card has no tag and shows the plain kind badge. Nothing is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:13-17`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:177-188`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:439-440`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:112-114`.
- Minimize the export widget to a pill, persisted in sessionStorage (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10`) — A pill with a ring and percent in the bottom-right stack. Clicking it expands the widget, where Cancel is. If it fails: If sessionStorage throws, the choice is kept in memory only. The flag is read once at module load and the store notifies subscribers, so remounts and Back stay consistent. No async work is involved. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-44`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:34-53`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.test.tsx:250-267`.
- Library ready card: Show in Finder and a native drag of the file via IPC (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — The OS reveals the file, or starts a native drag. `preventDefault` stops the browser's own drag, as in the toast. If it fails: Both calls are fire-and-forget. A rejected reveal is silently dropped, as in the other call sites. The buttons render only when `video.id` is non-null. The id is the local id the main process already… Evidence: `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:74-100`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-299`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:97-99`.
- New bottom-right export stack container that hosts the export progress widget, the minimized pill and the ready card (`apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19`) — Export progress, pill and ready card sit bottom right, 40px above the bottom edge, and stay clickable. StatusCard sets `pointer-events: auto` (status-card.module.css:5) and the new `.pill` sets it too (export-status-cards.module.css:77), so every child of the stack is interactiv… If it fails: None found. The container is non-blocking, so clicks pass through the gaps to the page below. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:2-12`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.tsx:27-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-card.module.css:5`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:77`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The change is sound overall. I read the renderer code and the unchanged files it calls, and found no blockers. `copyPresetOf` now strips the '#revision' suffix before comparing, which also fixes the Master copies panel, since the old `destinationPresetOf` could never match a real file's fingerprint. There are three minor "consider" findings. The Library ready card's Show in Finder and drag do not call `markCopySeen`, unlike the toast card and the `ready-copies.ts` comment. The progress percent inside the pill button is hidden from assistive tech. A user in list view never sees the ready cards, yet leaving the Library retires them. I did not read the CSS modules, the i18n files other than en.json, or the new backlog doc, which belong to part 2.

**Batch 2 of 2.** I found nothing to change in this part. Nothing was built or run, so this rests on reading the code.

- **CSS:** The new stylesheets use the same design tokens as the sibling modules. The bottom-right stack ignores the pointer, and the status card (`status-card.module.css:5`) and the new `.pill` (`export-status-cards.module.css:77`) each turn pointer events back on, so they stay clickable.
- **Destination colours:** The tag colours match `destination-logo.module.css`. A destination with no colour rule, `archive`, shows the default dark tag. That is fine, because the tag's own i18n select already maps it to "Archive copy".
- **i18n:** `en.json` and `es.json` carry the same new `backgroundCopy` keys, and the removed keys (`hide`, `readyDragToUpload`) have no remaining references.
- **Docs:** The new backlog doc has a row in `backlog/index.mdx` and an entry in the sidebar in `astro.config.mjs`. The claims I checked match the code: `retireReadyCards` runs from the sidebar's route hook, and the minimized state is kept in `sessionStorage` through `export-widget-state.ts`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 11 | $0.26 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 20 | $0.19 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 26 in / 15k out / 490k cache read / 97k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.45</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6IjQ0Y2RhZWRlLWE4MDUtNDc0My04NmFlLTgwNjk4OWJlNjNlYiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=44cdaede-a805-4743-86ae-806989be63eb -->
