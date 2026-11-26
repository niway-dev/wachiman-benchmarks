# kaipu-bench-wachi-v3#103 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:35:32Z · commit e45c845

👮 **Wachiman** · 🟡 **Nothing to fix · 3 to consider** · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 1 Should · 2 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Library ready card's Show in Finder / drag don't mark the copy seen, unlike the toast's |
| 🟡 Consider · Could · 🐛 bug | [`export-status-cards.tsx:216`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx#L216) | progressbar nested inside the pill's button is not exposed to assistive tech |
| 🟡 Consider · Should · 📝 docs | [`background-copy-toasts.md:60`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/documentation/src/content/docs/backlog/background-copy-toasts.md#L60) | Validation steps quote strings this PR removes |

<details><summary>What the change connects to (8 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Show in Finder and native drag from the Library's Ready to upload card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — The file is revealed or dragged out. The chip and outline remain until the copy is opened. If it fails: revealLocalRecording is fire-and-forget with `void` and no catch, the same as use-local-library.ts:98, so a rejection is silent. This is the existing convention. Evidence: `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:74-99`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-299`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:97-99`.
- Retire Ready to upload cards when the route leaves the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-105`) — On return to the Library the plain grid shows. The copy keeps its outline and chip until it is opened. If it fails: A remount of the Sidebar, which only happens leaving AppShell for sign-in, would reset the ref and skip the retire. That is unlikely and harmless. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-105`, `apps/kaipu-record/src/renderer/src/shell/app-shell.tsx:46-53`, `apps/kaipu-record/src/renderer/src/app/router.tsx:59-63`, `apps/kaipu-record/src/renderer/src/app/router.tsx:106`.
- Export widget minimized state kept in module memory and sessionStorage (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`) — Later exports open as the pill. An error always shows in full (status === "error" renders the card regardless). If it fails: If storage throws, both the read and the write fall back to memory silently. That costs only persistence across a reload. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:34-55`.
- Read a copy's destination back from the sidecar fingerprint (copyPresetOf / copyDestinationOf) (`apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:13-30`) — The Library grid tags copies For YouTube, For GitHub and so on, and the Copies panel names them by destination. If it fails: No failure path: pure and synchronous. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:13-30`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-reuse.ts:18`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:440`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:185`.
- Minimize the export progress widget to a pill (− button) and expand it again by clicking the pill (`apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:152`) — With the flag set and status "exporting", `ExportStatusCards` renders the pill (ring plus "YouTube copy · 38%"). Clicking it sets the flag false and the full card returns. A status of "error" always renders the full card, whatever the flag says. If it fails: If sessionStorage throws, the choice holds in memory only and the widget still works. A minimized widget with no way to cancel is not reachable: expanding the pill brings back Cancel, and an error ig… Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:8-44`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:40-51`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:152-154`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:199-204`.
- Ready to upload card in the Library grid: Show in Finder, native drag of the file, open (poster or file name), dismiss (✕) (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:74`) — The card leads the grid in place of the regular card. Dismissing it returns the regular card, still outlined, as ready-copies.ts `dismissReadyCard` sets `card: false` and keeps the entry. If it fails: The actions render only when `video.id` is non-null; a cloud-only item gets the poster and file name but no actions. `revealLocalRecording` is called with `void` and no catch, so a rejection is silen… Evidence: `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:74-100`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:409-421`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:87-100`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-299`.
- Leaving the Library retires the ready cards (route watch in the rail hook); a Back navigation to the Library lands on the plain grid (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102`) — On the next visit the copy's regular card shows with the unseen outline. Opening a copy's detail page counts as leaving, so the cards retire as well. If it fails: A copy that finishes while the user is on the Library gets its card immediately and keeps it until they leave. If the Library is open when the toast's Show in Finder runs, the copy is marked seen and… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-106`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:93-100`.
- New destination-tag and ICU select messages (`destinationTag`, `dragTo`, `pill`, titles) for every destination id (`packages/i18n/messages/en.json:1413`) — Titles, pill text, drag labels and tags read correctly in both locales. If it fails: None found. Evidence: `packages/i18n/messages/en.json:1413-1435`, `packages/i18n/messages/es.json:1413-1435`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-44`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:62-64`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found two minor issues in this part and no blockers. The Library's Ready to upload card doesn't mark the copy seen, which the toast's card does. The minimized pill nests a progressbar inside a button. The leave-the-Library retirement works: the Sidebar sits in AppShell, which hosts every route except sign-in. The sidecar fix for fingerprints like \"whole#…\" is sound, and the tests cover it. The PR body's \"Email wording\" bullet describes an email destination that isn't in this diff. `DESTINATION_IDS` has no email entry and the `en.json` selects have no email branch, so that text was not checked. It presumably lives in the stacked branch #467. I read only the English messages for the keys these components use, and `es.json` was not checked.

**Batch 2 of 2.** The styles, messages and docs in this part match the code. I found no defect, only one docs mismatch. The older `background-copy-toasts.md` still quotes strings and a \"Drag to upload\" button that this PR removes from `en.json`, so its validation steps no longer match the UI. The new CSS tokens exist; `--bg-hover` has a fallback. The Library grid is a fixed three columns, so the card's `span 2` is safe. en.json and es.json are in sync, and the removed message keys have no remaining references. Nothing here is dangerous to ship: no migration, auth or install-script change.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 17 | $0.45 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 28 | $0.42 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**Validation steps quote strings this PR removes (confidence high)** ([`background-copy-toasts.md:60`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/documentation/src/content/docs/backlog/background-copy-toasts.md#L60))

The "How to validate" steps (lines 60 and 67, and the bullets at 29–37) still quote "Preparing your YouTube copy…", "Preparing your export…", "Your export is ready" and the "Drag to upload" button. This PR rewrites `backgroundCopy.progressTitle` and `readyTitle`, and drops `hide` and `readyDragToUpload` (en.json 1413–1418). The progress title is now "Exporting for YouTube", the ready title "YouTube copy ready", and the drag label "Drag to YouTube Studio". The new "Update" banner at line 16 says the cards moved, but the steps themselves can no longer be followed word for word. Either update the quoted strings or mark these steps as superseded by `ready-copy-in-library`.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 38 in / 21k out / 987k cache read / 139k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.86</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6Ijk4NTA1MWZjLTFhMzctNGZjNS04ZTEzLTEwNzU1ZGFmZjg4ZiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjIsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MX0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=985051fc-1a37-4fc5-8e13-10755daff88f -->
