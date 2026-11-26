# kaipu-bench-wachi-v3#33 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:51:57Z · commit e45c845

👮 **Wachiman** · 🟡 **Nothing to fix · 6 to consider** · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 6 to consider · ⚪ 0 for your information (6) · 3 Should · 3 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To consider (6)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Show in Finder / drag on the Library ready card never mark the copy seen |
| 🟡 Consider · Could · 🐛 bug | [`sidebar.tsx:102`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L102) | Leaving the Library retires cards the user never saw (list view or filtered out) |
| 🟡 Consider · Should · 🧪 tests | [`library-page.test.tsx:225`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L225) | "opening the copy … forgets it" never checks the forgetting |
| 🟡 Consider · Should · 📝 docs | [`background-copy-toasts.md:16`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/documentation/src/content/docs/backlog/background-copy-toasts.md#L16) | The update banner leaves the old wording in the doc's body and front matter |
| 🟡 Consider · Could · ❓ question | [`en.json:1413`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1413) | The PR body promises email wording, but no message has an \`email\` branch |
| 🟡 Consider · Could · 🐛 bug | [`ready-copy-card.module.css:180`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.module.css#L180) | ✕ hover background falls back to a white tint that won't show in the light theme |

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Show in Finder / drag the file from the Library's Ready to upload card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — After acting on it, the copy keeps its unseen chip and outline in the Library. If it fails: revealLocalRecording's promise is voided, as in the sibling and in use-local-library.ts:98, so a rejection is silent in both places. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:279-295`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:10-11`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80-94`.
- Retire the ready cards when the route leaves the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:99-103`) — The next visit to the Library shows the plain grid, with the outline still on unseen copies. If it fails: Cards for copies hidden by list view or filters are retired without ever being shown. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:97-100`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:126-133`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:407`.
- Minimized export widget state kept in sessionStorage (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`) — The pill or the full widget in ExportStatusCards. An error always renders in full. If it fails: When storage fails, the widget defaults to expanded. No data is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-16`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:40-43`.
- DestinationTag renders the new `backgroundCopy.destinationTag` ICU select with the destination's colour from destination-tag.module.css (`apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.tsx:18`) — FOR YOUTUBE / FOR GITHUB… uppercase tag on the ready card's poster (ready-copy-card.tsx:58-62) and the grid card. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.module.css:25-46`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-logo.module.css:11-29`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `packages/i18n/messages/en.json:1431`.
- The export widget and its pill render in a new fixed bottom-right stack with pointer-events: none (`apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19`) — Progress card, pill and ready toast bottom right, 40px above the bottom edge; the stack's empty area does not block clicks. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.tsx:24-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:76-78`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:39-54`.
- Removed i18n keys `backgroundCopy.hide` and `backgroundCopy.readyDragToUpload`; editor exports now use the `other` branches (`packages/i18n/messages/en.json:1418`) — Editor export toast title unchanged; progress title becomes "Exporting your video". Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:62-64`, `apps/kaipu-record/e2e/export.e2e.ts:44`, `packages/i18n/messages/en.json:1418`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 is generally sound. The fingerprint-revision fix in `copyPresetOf` is correct and has tests. The sessionStorage widget state degrades safely. The route-based card retirement works as described. Three consider-level findings:

- The Library ready card's Show in Finder and drag buttons skip the `markCopySeen` call that the toast's buttons make.
- Leaving the Library retires cards that were never shown (list view or filtered out).
- One test named for forgetting the copy never checks that the copy was forgotten.

Not something to fix in this part: the PR body describes an email destination ("Exporting for email", "FOR EMAIL"), but `DESTINATION_IDS` at this head has no `email`, and the `dragTo`/`destinationTag` messages have no email branch.

**Batch 2 of 2.** I found three "consider" items and nothing that blocks the merge.

1. **Stale doc.** The banner added to `background-copy-toasts.md` doesn't say the wording changed. That doc's description, body and validation steps still quote the old strings ("Preparing your YouTube copy…", "Your YouTube copy is ready", "Drag to upload").
2. **Email claim (asked as a question).** The PR body promises email wording ("Exporting for email", "Email copy ready", "Drag to an email", FOR EMAIL). No new message has an `email` branch in either locale, and the destination list at this head has no `email` destination.
3. **Light theme.** The ✕ hover background on the Ready to upload card uses `--bg-hover`, which isn't defined. It always falls back to a white tint, which won't show on the light theme's white cards.

What checked out:

- The other new stylesheets use only tokens that exist.
- The tag colours match the destination logos.
- The bottom-right stack still lets clicks reach its cards and the pill.
- No code still uses the removed `hide` and `readyDragToUpload` keys.
- The editor export's "Your export is ready" title still matches what the e2e tests look for.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 8 | $0.56 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 15 | $0.56 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 28 in / 13k out / 508k cache read / 95k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.12</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6IjdiZGRhYzgxLTlmNmYtNGFlZC05OWEyLTJhYmFlZGUyYWYwOCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NiwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjYsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=7bddac81-9f6f-4aed-99a2-2abaede2af08 -->
