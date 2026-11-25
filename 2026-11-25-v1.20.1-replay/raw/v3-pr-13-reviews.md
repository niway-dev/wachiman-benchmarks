# kaipu-bench-wachi-v3#13 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:54:16Z · commit e45c845

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 1 to consider · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 1 to consider · ⚪ 0 for your information (2) · 1 Should · 1 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Show in Finder / drag on the Library ready card don't mark the copy seen |

### To consider (1)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`ready-copy-card.module.css:180`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css#L180) | \`--bg-hover\` is not defined anywhere, so the ✕ hover always uses a white-tint fallback |

<details><summary>What the change connects to (4 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Show in Finder / native drag from the Library's Ready to upload card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — The copy stays unseen: the card, the chip count and the outline stay after the user has acted on it. If it fails: revealLocalRecording's promise is voided, the same as in the sibling; a rejection fails silently in both. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-295`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:9-13`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:76-98`.
- Minimized export widget state persisted in sessionStorage (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10`) — The widget opens as a pill or in full; an error always shows in full (export-status-cards.tsx:40-43). If it fails: When storage is unavailable, the state holds in memory only. The value is a UI preference, so a fallback to expanded loses no data. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:36-53`.
- Minimize the export widget to a pill (− button), and reopen it from the pill (`apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:76`) — The pill shows a ring plus "<Destination> copy · N%" (en/es `pill` key) and sits in the fixed bottom-right exportStack. If it fails: sessionStorage access is wrapped. A reload keeps the flag, and a relaunch clears it. No async calls. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:40-51`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:152-154`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:199-224`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:12`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:29-30`, `packages/i18n/messages/en.json:1427-1429`.
- Ready to upload card spanning two grid columns, with a destination tag and Drag to <destination> (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:4`) — `grid-column: span 2` works in the Library's fixed 3-column grid, since there is no media query that drops to one column. The tag colours match destination-logo.module.css. If it fails: revealLocalRecording is fire-and-forget (`void`). A rejection goes unseen, which is the toast's existing behaviour. Evidence: `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:76-98`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-299`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:366-371`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-logo.module.css:11-28`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 has one finding, a fix. The Library's new \"Ready to upload\" card skips the `markCopySeen` step that the ready toast's identical Show in Finder and drag buttons take. As a result, a copy the user has already revealed or dragged out stays marked unseen. The rest looks consistent: the copy-destination fingerprint fix, the destination tags, the session-wide minimized widget, and retiring the cards on route change. Separately, the PR body describes email wording and a FOR EMAIL tag, but at this head `DestinationId` and the en.json selects have no email case; the wording probably arrives with the stacked branch.

**Batch 2 of 2.** I found one optional issue and nothing that blocks part 2 (stylesheets, backlog docs, en/es messages).

- **Undefined hover token:** `ready-copy-card.module.css:180` uses `--bg-hover`, which no stylesheet defines. The fallback is a faint white tint, so the ✕ button's hover background can't be seen on the light theme's white card. Logged as "consider".

The rest checks out:

- **Messages:** nothing in the app still references the removed `hide` and `readyDragToUpload` keys. The new keys exist in both languages with the same ICU select branches. In `destinationTag`, the archive case falls to `other`, which reads "Archive copy".
- **Docs:** the claims I checked match the code: the sessionStorage minimize state, `retireReadyCards` called from the sidebar, the toast's "Drag to …" text and errors always showing in full. The new backlog row's 🟡 status is right for a branch that hasn't been QA'd yet.
- **Styles:** the destination tag colours match `destination-logo.module.css`. The other tokens the new CSS uses are defined.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 7 | $0.49 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 13 | $0.45 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 24 in / 9.9k out / 389k cache read / 83k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.94</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6ImQ5YWNlNzBiLTFhNjctNGE2MC1iZDMxLTY0NDJmYWEyZjc5ZSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MSwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjIsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=d9ace70b-1a67-4a60-bd31-6442faa2f79e -->
