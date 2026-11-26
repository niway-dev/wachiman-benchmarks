# kaipu-bench-wachi-v3#38 [replay r2] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T23:56:05Z · commit e45c845

👮 **Wachiman** · 🟠 **1 to fix in this PR** · 4 to consider · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 4 to consider · ⚪ 1 for your information (6) · 4 Should · 1 Could · 1 FYI |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Show in Finder and the drag on the Library ready card never mark the copy seen |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`ready-copy-card.tsx:93`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L93) | The drag passes the raw title while the label uses the "Untitled" fallback |
| 🟡 Consider · Should · 🧪 tests | [`library-page.test.tsx:225`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx#L225) | "opening the copy goes to its page and forgets it" never checks the forgetting |
| 🟡 Consider · Should · 📝 docs | [`ready-copy-in-library.md:77`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/documentation/src/content/docs/backlog/ready-copy-in-library.md#L77) | Validation step 7 lists the cards oldest first |
| 🟡 Consider · Should · 📝 docs | [`en.json:1431`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1431) | The vertical destination gets three different names |

<details><summary>For your information (1)</summary>

| | Where | Finding |
| --- | --- | --- |
| ⚪ Info · FYI · ❓ question | [`en.json:1413`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1413) | The PR body's "Email wording" section is not in this diff |

</details>

<details><summary>What the change connects to (5 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Show in Finder / Drag on the Library Ready to upload card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — The copy stays unseen: after the card retires, the regular card has the outline and the chip counts it, even though the user already acted on the file. If it fails: revealLocalRecording's promise is voided, as in the sibling and in use-local-library, so a rejection is silent in both places. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-295`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:9-13`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:76-79`.
- Minimize the export widget (session-wide, stored in sessionStorage) (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:25`) — The pill renders while status is exporting and the widget is minimized. The full card renders on error or while expanded. If it fails: If storage is unavailable, the read falls back to false and the write is skipped; the choice stays in memory. Nothing reads data and writes it back, so nothing is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:34-55`.
- Retire the ready cards when the route leaves the Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:102`) — The next visit shows the plain grid with outlined copies. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:92-106`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:97-100`.
- Destination tag and the ready card / widget strings choose their text with an ICU select on the destination id (`packages/i18n/messages/en.json:1431`) — DestinationTag renders t("destinationTag") on the poster with data-destination colours. Every DESTINATION_IDS member has a branch; archive falls to `other` ("Archive copy") on the default #2a2a30 background. Editor exports pass "export", or "other" in ready-copy-card, and that f… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.tsx:18-20`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:62-64`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:97`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.module.css:3-46`.
- Export cards move to a fixed bottom-right stack above the status bar; the ready card spans two grid columns (`apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19`) — The status bar is 28px tall, so the 40px bottom offset clears it. The library grid is a fixed 3 columns, so `grid-column: span 2` never creates an implicit column. Evidence: `apps/kaipu-record/src/renderer/src/shell/app-shell.module.css:24-27`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:366-371`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.tsx:27`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:76-77`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** Part 1 has one bug. On the new Library "Ready to upload" card, Show in Finder and the drag call the same IPCs as the export toast's ready card but skip the toast's `markCopySeen` step. A copy the user already revealed or dragged out therefore stays outlined as unseen and counted in the "1 copy ready" chip. Two smaller points: the drag passes the raw title while the label uses the "Untitled" fallback, and one library test does not check the forgetting its name claims. The fingerprint fix in `copyPresetOf`, the session-wide minimized widget, and retiring cards from the route watch all read correctly.

**Batch 2 of 2.** I reviewed the nine files in part 2 (stylesheets, backlog docs and both message files) and found no defects.

Three findings, none blocking:

- **Doc order (consider):** validation step 7 in `ready-copy-in-library.md` lists the ready cards oldest first (FOR GITHUB before FOR CHAT). `readyCards` puts the newest first, so a tester following the doc would expect the wrong order.
- **Naming (consider):** the vertical destination is called three different things across the new strings: "Reels and TikTok", "Vertical copy" and "For Reels".
- **PR body (info):** the "Email wording" section describes text that is not in this diff, and there is no email destination at this head.

Every message key the new code calls exists in `en.json` and `es.json`. The removed keys (`hide`, `readyDragToUpload`) have no remaining callers in the renderer. Every destination id has a branch in the new ICU selects or falls through to `other`. The CSS offsets match the 28px status bar and the fixed 3-column Library grid.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 5 | $0.48 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 17 | $0.53 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**The PR body's "Email wording" section is not in this diff (confidence high)** ([`en.json:1413`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1413))

The PR body says email is its own destination and gets "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag. None of the new `select` messages here has an `email` branch, and `DESTINATION_IDS` at this head has no `email` (`destinations.ts:36-43`). Nothing breaks: there is no email destination to fall through to `other`. But the description claims wording the change does not contain.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 24 in / 11k out / 417k cache read / 89k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.01</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6ImVlNDlmMTFkLWRhZWUtNDczMy05YzYxLTU3ZWZjMzQzZDU0NyIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6NCwiaW5mbyI6MX0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjUsImJvZHkiOjEsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=ee49f11d-daee-4733-9c61-57efc343d547 -->
