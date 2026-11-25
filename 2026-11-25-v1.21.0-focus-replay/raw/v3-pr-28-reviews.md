# kaipu-bench-wachi-v3#28 [replay r3] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:00:10Z · commit e45c845

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 2 questions for you · 2 to consider · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 2 to consider · ⚪ 1 for your information (4) · 3 Should · 1 FYI |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Needs a person** | 1 direction, in `sidebar.tsx:102` |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`ready-copy-card.module.css:4`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css#L4) | Two or more Ready cards leave an empty cell at the top right of the Library grid |

### To consider (2)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Show in Finder and drag on the Library card don't mark the copy as seen, but the toast's buttons do |
| 🟡 Consider · Should · 📝 docs | [`en.json:1413`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1413) | The PR body promises email wording that does not exist at this head |

### Questions for you (2)

- [`sidebar.tsx:102`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L102) · direction — Retiring the cards depends on the rail's route watch instead of the page, so it holds only while the Sidebar stays mounted across routes. Someone should decide whether that coupling is acceptable.
- [`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L102) · open question — Retire the ready cards when the route leaves the Library: Is every route (the editor included) rendered under AppShell, so the Sidebar never remounts? Files that would answer it: `apps/kaipu-record/src/renderer/src/app.tsx`, `apps/kaipu-record/src/renderer/src/routes.tsx`.

<details><summary>For your information (1)</summary>

| | Where | Finding |
| --- | --- | --- |
| ⚪ Info · FYI · 📝 docs | [`destination-tag.tsx:19`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.tsx#L19) | The PR body's Email wording isn't in this head |

</details>

<details><summary>What the change connects to (5 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Retire the ready cards when the route leaves the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102`) — Is every route (the editor included) rendered under AppShell, so the Sidebar never remounts? Files that would answer it: `apps/kaipu-record/src/renderer/src/app.tsx`, `apps/kaipu-record/src/renderer/src/routes.tsx`.

**Closed, with the lines they rest on**

- Show in Finder / drag out from the Library's Ready to upload card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — After the user acts on the copy, its chip and outline stay in the Library. If it fails: revealLocalRecording is fire-and-forget (void), the same as the sibling; a rejection is not shown to the user, as in the existing path. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:278-295`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:9-13`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:76-79`.
- Read and write the minimized widget state in sessionStorage (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10`) — The widget opens as a pill or in full. If it fails: Falling back to expanded only affects UI state; no user data is written back from the empty default. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`.
- The export widget and its ready toast move into a new fixed bottom-right stack that lets clicks pass through it (`apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19`) — The progress widget, the pill and the ready toast show 40 px above the bottom on every screen and stay clickable. The page underneath still gets clicks everywhere else. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.tsx:24-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:2-12`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-card.module.css:5`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:77`.
- i18n keys removed (`hide`, `readyDragToUpload`) and added (`progressNote`, `minimize`, `expand`, `pill`, `dragTo`, `destinationTag`, `readyToUpload`, `fromOrig… (`packages/i18n/messages/en.json:1413`) — The widget, pill, toast, ready card and tags show the new wording in English and Spanish. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:141`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:223`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:298`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:97`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.tsx:19`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-44`.
- The Ready to upload card spans two columns at the top of the Library grid (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css:4`) — One card lays out cleanly. With two or more, each card after the first leaves an empty cell in column 3 of the row above it. Evidence: `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:408-425`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:366-369`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 has no blocking defects. The new Library "Ready to upload" card reveals and drags the file without marking the copy as seen. The toast's matching buttons and the ready-copies contract both do mark it, so the chip and outline stay after the user has already used the copy. The PR body's Email wording is not present in this head.

**Batch 2 of 2.** I reviewed part 2: the four stylesheets, the two backlog docs and their index row, and the en/es messages. I found two things.

- **Grid gaps (fix):** the two-column Ready card leaves an empty cell at the top right of the Library grid once two or more copies are ready. The grid always has 3 columns and fills cells in order, so a second two-column card can't fit beside the first and drops to the next row. This is exactly the doc's validation step 7. Adding `grid-auto-flow: row dense` to `.grid` would let the first regular card fill the gap.
- **PR description (consider):** the body promises email wording ("Exporting for email", FOR EMAIL…). Neither locale has those strings, and the destination list at this head has no `email`. The new doc also names a different stack base (#459) than the body (#466).

Nothing else turned up:

- The new bottom-right export stack lets clicks through to the page, and its cards and pill still take clicks.
- No code still uses the removed i18n keys, and every new key has a caller.
- The doc's claims about session-only minimizing, retiring cards from the rail and keeping copies unseen after ✕ match the code.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 10 | $0.64 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 23 | $0.65 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**The PR body's Email wording isn't in this head (confidence high)** ([`destination-tag.tsx:19`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.tsx#L19))

The description says Email gets "Exporting for email", "Drag to an email" and a FOR EMAIL tag. At this head, `DESTINATION_IDS` has no `email` (destinations.ts:36-43), and the `destinationTag`, `dragTo` and `pill` messages have no email branch. Archive falls through to `other {Archive copy}`. Either the Email part comes from a stacked branch that isn't merged here, or the description is ahead of the code.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 38 in / 15k out / 787k cache read / 106k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.30</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6IjBlZmYxMGRlLTFmNjYtNDc2Ni05MmE2LTE0OWQxMDBlMGNkYiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MiwiaW5mbyI6MX0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjEsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=0eff10de-1f66-4766-92a6-149d100e0cdb -->
