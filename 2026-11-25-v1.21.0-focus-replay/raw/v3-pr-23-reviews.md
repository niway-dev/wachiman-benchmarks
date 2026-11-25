# kaipu-bench-wachi-v3#23 [replay r2] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T22:58:55Z · commit e45c845

👮 **Wachiman** · 🟠 **1 to fix in this PR** · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 1 to fix · 🟡 0 to consider · ⚪ 1 for your information (2) · 1 Should · 1 FYI |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To fix (1)

| | Where | Finding |
| --- | --- | --- |
| 🟠 Fix · Should · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Show in Finder and drag on the Library ready card never mark the copy seen |

<details><summary>For your information (1)</summary>

| | Where | Finding |
| --- | --- | --- |
| ⚪ Info · FYI · 📝 docs | [`en.json:1413`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1413) | PR body claims email wording that is not in this head |

</details>

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Show in Finder on the Library ready card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — Finder opens on the file. The card and the unseen outline/chip stay. If it fails: A rejected promise is dropped with `void`, the same as the toast does: nothing shows the user. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:277-281`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:10-11`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:76-79`.
- Native drag out of the Library ready card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:90-94`) — The main process starts a native file drag. The card stays. If it fails: startFileDrag is fire-and-forget (ipcRenderer.send), so a failure shows nothing, as in the toast. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:290-294`.
- The minimized state of the export widget is read from and written to sessionStorage (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:11-35`) — The widget opens expanded when storage can't be read. If it fails: If storage is unavailable, the choice holds in memory only. Nothing is lost. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-16`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:25-35`.
- Leaving the Library route retires the ready cards (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:99-103`) — The next Library visit shows the plain grid, with the unseen outlines still there. If it fails: The Sidebar persists in the shell, so the ref survives page remounts. A Back/remount of the Library page doesn't reset it. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:97-100`.
- New ICU select messages (`progressTitle`, `readyTitle`, `pill`, `dragTo`, `destinationTag`) take a `destination` argument from the renderer (`packages/i18n/messages/en.json:1413`) — ExportProgressCard title, pill label, ready toast title and Drag button, the ReadyCopyCard drag button, and DestinationTag text. If it fails: Every DestinationId (youtube, vertical, square, github, chat, archive) has an explicit case, or falls to `other` for `destinationTag`'s archive. A null destination is passed as "other" (ready-copy-ca… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-44`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:97`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:141`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:223`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:298`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destination-tag.tsx:19`.
- The export cards are moved into a fixed bottom-right `.exportStack` with `pointer-events: none` (`apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.module.css:19`) — The widget and pill stay clickable: `.card` in status-card.module.css sets `pointer-events: auto`, and so does `.pill` in export-status-cards.module.css. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/status-stack.tsx:24-29`, `apps/kaipu-record/src/renderer/src/features/status-cards/status-card.module.css:5`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.module.css:77`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found one bug in part 1. The Library's new "Ready to upload" card calls Show in Finder and the native drag (`ready-copy-card.tsx:80` and `:93`) without `markCopySeen`. The toast's ready card does call it, and the store's documented contract requires it. As a result, a copy the user has already revealed or dragged out stays shown as an unseen, ready card.

The rest of what I read holds up:

- `copyPresetOf` correctly compares only the part of the fingerprint before the revision.
- The sessionStorage widget state never writes back a value it failed to read.
- Retiring cards on route change works across page remounts.

One more thing: the PR body describes Email-specific wording and a FOR EMAIL tag. I found no email key in the current `en.json` select messages, and none in `DESTINATION_IDS`. I'm only noting this, not posting it as a finding, because the messages file is in part 2.

**Batch 2 of 2.** I found nothing to fix in part 2's stylesheets, docs and messages.

- **Styles:** the destination tag colours match `destination-logo.module.css`. The new bottom-right export stack stays clickable: the stack itself ignores clicks, but the status card and the pill accept them.
- **Messages:** the new select messages in both `en.json` and `es.json` cover every destination id. The two removed keys, `hide` and `readyDragToUpload`, have no callers left.
- **Docs:** the backlog doc and its index row agree with the code as built.

The one note is info only: the PR body describes email wording ("Exporting for email", a FOR EMAIL tag) that isn't in this head. No `email` destination exists here, so nothing breaks; the description is just ahead of the code.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 7 | $0.53 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 13 | $0.44 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**PR body claims email wording that is not in this head (confidence high)** ([`en.json:1413`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1413))

The PR body's first bullet says Email is now its own destination with "Exporting for email", "Email copy ready", "Drag to an email" and a FOR EMAIL tag. At this head `DESTINATION_IDS` has no `email` (apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43), and none of the new `backgroundCopy` select messages (`progressTitle`, `readyTitle`, `pill`, `dragTo`, `destinationTag`) has an `email` case. Nothing breaks, because no caller can pass `email`. The description is just ahead of the code, so the claim can't be checked here.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 22 in / 9.8k out / 395k cache read / 87k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.97</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6ImRlZDg5OWNiLTQ3MjEtNDdhNy04Mjc5LTQwNmE0OTRjMjRlZSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjoxLCJjb25zaWRlciI6MCwiaW5mbyI6MX0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjEsImJvZHkiOjEsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=ded899cb-4721-47a7-8279-406a494c24ee -->
