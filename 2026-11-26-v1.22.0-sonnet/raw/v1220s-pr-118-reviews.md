# kaipu-bench-wachi-v3#118 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:08:13Z · commit e45c845

👮 **Wachiman** · 🟡 **Nothing to fix · 4 to consider** · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 4 to consider · ⚪ 0 for your information (4) · 2 Should · 2 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Acting on the Library ready card does not mark the copy seen, unlike the toast card |
| 🟡 Consider · Should · 🧪 tests | [`library-page.test.tsx:225`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L225) | "opening the copy ... forgets it" never asserts that the copy was forgotten |
| 🟡 Consider · Should · 📝 docs | [`en.json:1431`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1431) | PR body describes email wording that this head does not contain |
| 🟡 Consider · Could · 🐛 bug | [`export-status-cards.module.css:99`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css#L99) | Minimized pill hides the percentage from screen readers |

<details><summary>What the change connects to (4 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Library leads the grid with a ReadyCopyCard for each finished copy; Show in Finder and drag-out use existing IPC (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:409`) — The card appears as a two-column lead card in grid view only. It is replaced by the regular card once closed, opened or retired. The unseen chip and outline persist after a reveal or drag. If it fails: revealLocalRecording and startFileDrag are fire-and-forget, so a rejection from main is silent. The toast and the Library hook (use-local-library.ts:98) behave the same way. Evidence: `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:74-100`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-299`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:98`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:75-79`.
- Cards are retired when the route leaves the Library (sidebar route watch with a ref) (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-105`) — Leaving the Library and returning shows the plain grid, with the outline kept for unseen copies. If it fails: None found. The state is in memory, and nothing is persisted or fails asynchronously. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-105`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:93-100`.
- The export widget minimize state is read from and written to sessionStorage (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`) — The pill or the card, driven by useSyncExternalStore. If it fails: Storage unavailable only means the choice is not persisted across a renderer reload. An error always shows in full (export-status-cards.tsx:43). Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:34-55`.
- copyPresetOf now compares only the content part of the sidecar fingerprint before "#" (`apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:13-17`) — Copies show the destination in the panel and on the Library tags. If it fails: None found. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:13-17`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:440`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-reuse.ts:18`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-reuse.ts:74`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The change holds together: store, Library card, sidebar retirement and widget state are consistent, and the i18n keys the new components use exist in both locales. I found two minor items. The Library ready card's Show in Finder and drag do not mark the copy seen, unlike the toast card, so the unseen chip and outline linger. One test is named \"forgets it\" but never asserts that. The PR body also says Email gets its own wording and tag. No `email` destination exists in `destinations.ts`, and the new `dragTo`, `destinationTag`, `pill` and `progressTitle` messages have no email case, so that claim does not match this head. I did not read the CSS modules or the backlog doc, which belong to part 2.

**Batch 2 of 2.** The nine files in this part are mostly CSS, docs and messages, and I found only two minor issues. CSS tokens resolve (`--bg-hover` has a fallback). The `grid-column: span 2` card is safe because the Library grid is a fixed three columns. The removed i18n keys `hide` and `readyDragToUpload` are no longer referenced, and `status-stack.tsx` wires the new `.exportStack`. The PR body claims email-specific wording from #467 that is absent from this head's destinations and messages, and the minimized pill's accessible name drops the percent. I did not build or run anything.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 16 | $0.34 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 24 | $0.25 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 30 in / 19k out / 705k cache read / 133k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.59</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6ImJmNWM2MTg3LWZhMTItNDY1ZC1hODVmLWQ1MTQ5ZGI4YmNjNiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=bf5c6187-fa12-465d-a85f-d5149db8bcc6 -->
