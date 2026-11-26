# kaipu-bench-wachi-v3#18 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:55:28Z · commit e45c845

👮 **Wachiman** · 🟡 **Nothing to fix · 4 to consider** · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 4 to consider · ⚪ 1 for your information (5) · 4 Could · 1 FYI |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · ❓ question | [`copy-destination.ts:16`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts#L16) | Do Share copies get tagged with a Prepare destination? |
| 🟡 Consider · Could · 🧹 cleanup | [`ready-copy-card.tsx:97`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L97) | Fallback for an editor export differs from the toast's |
| 🟡 Consider · Could · 🐛 bug | [`export-status-cards.tsx:216`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx#L216) | The pill's progressbar is inside a button, so screen readers hide it |
| 🟡 Consider · Could · 📝 docs | [`ready-copy-in-library.md:8`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/documentation/src/content/docs/backlog/ready-copy-in-library.md#L8) | Status banner names a different stack base than the PR |

<details><summary>For your information (1)</summary>

| | Where | Finding |
| --- | --- | --- |
| ⚪ Info · FYI · ❓ question | [`en.json:1431`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1431) | The PR description's "Email wording" is not in this diff |

</details>

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Drag button on the Ready to upload card starts a native file drag (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:90`) — The OS drag carries the real file; Show in Finder calls revealLocalRecording(id). If it fails: startFileDrag is fire-and-forget (ipcRenderer.send), so a failure is silent, the same as in the existing call sites. Evidence: `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:74-98`, `apps/kaipu-record/src/renderer/src/features/library/components/gif-viewer.tsx:25-28`.
- The minimized state of the export widget is read from sessionStorage and written back (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10`) — The widget renders as the pill or the full card. If it fails: If storage is unavailable, the choice stays in memory only. The value written back is the user's choice, never one derived from a failed read, so nothing is overwritten. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`.
- Leaving the Library route retires the Ready to upload cards (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102`) — On Back or a return visit, the Library opens on the plain grid with an outline on unseen copies. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:95-104`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:97-100`.
- Click the minimize (−) button on the export widget, or click the pill to bring the widget back (`apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:76`) — ExportStatusCards shows ExportProgressPill while minimized and exporting. An error always shows the full card. The pill sets pointer-events: auto inside the exportStack container, which has pointer-events: none, so it stays clickable. If it fails: If sessionStorage throws, read() returns false and setExportWidgetMinimized keeps the choice in memory only, so nothing is lost for the session. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:34-55`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:198-204`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:76-77`.
- Show the Ready to upload card spanning two grid columns (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:4`) — The card leads the grid at two-thirds width. Cards are retired when the route leaves /library (sidebar route hook). Evidence: `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:366-371`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-104`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 looks sound. The ready-copy store, the route-based card retirement, the export widget's session state and the fingerprint fix all match what the PR describes. Three minor points: Share exports may get a Prepare destination tag through `copyPresetOf`; the Library card and the toast use different fallbacks for an editor export; and the pill's progressbar sits inside a button, so screen readers do not announce the percent.

**Batch 2 of 2.** Part 2 covers the stylesheets, the docs and the i18n messages. The new CSS is consistent with the components that use it. The destination tag colours match destination-logo.module.css. The two-column span fits the fixed 3-column Library grid. The bottom-right export stack keeps pointer-events off except on its cards and the pill. The i18n keys line up with their call sites, and the removed keys (`hide`, `readyDragToUpload`) have no remaining references. Two notes: the PR description claims email-destination wording that does not exist at this head, and the backlog doc and index row name #459 as the stack base while the description says #466.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 8 | $0.56 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 20 | $0.58 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**The PR description's "Email wording" is not in this diff (confidence high)** ([`en.json:1431`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1431))

The description says email is now its own destination, with "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag. None of the new ICU selects (`progressTitle`, `readyTitle`, `pill`, `dragTo`, `destinationTag`) in en.json or es.json has an `email` branch. The destination list at this head (`features/prepare/destinations.ts:37-42`) is youtube, vertical, square, github, chat and archive, with no email. That part of the description seems to come from a later merge, not from this commit.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 32 in / 12k out / 632k cache read / 96k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.14</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6IjcwOWZiMDY4LTJlNmEtNDlhNS04YmFmLWNjMzBlNWEzMzNjMyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NSwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NCwiaW5mbyI6MX0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjEsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=709fb068-2e6a-49a5-8baf-cc30e5a333c3 -->
