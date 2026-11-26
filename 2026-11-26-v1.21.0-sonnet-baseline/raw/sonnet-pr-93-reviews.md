# kaipu-bench-wachi-v3#93 [replay] feat(desktop): ready copy shows up in the Library; minimizable export widget - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:30:39Z · commit e45c845

👮 **Wachiman** · 🟣 **2 questions for you** · 7 to consider · whole PR at `e45c845`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 7 to consider · ⚪ 0 for your information (7) · 1 Should · 6 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Needs a person** | 1 trade-off, in `sidebar.tsx:102` |
| **Coverage** | 31 of 31 files reviewed, whole pull request |
| **Read first** | `ready-copy-card.tsx`, `export-status-cards.tsx`, `library-page.tsx`, `export-widget-state.ts`, `ready-copies.ts` |

### To consider (7)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`ready-copy-card.tsx:80`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L80) | Library ready card's Show in Finder / drag do not mark the copy seen, unlike the ready toast |
| 🟡 Consider · Could · 🐛 bug | [`sidebar.tsx:102`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L102) | Cards are retired on leaving the Library even if they were never rendered |
| 🟡 Consider · Could · 🐛 bug | [`export-status-cards.tsx:202`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx#L202) | Pill's aria-label hides its own progress text from assistive tech |
| 🟡 Consider · Should · 📝 docs | [`background-copy-toasts.md:60`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/documentation/src/content/docs/backlog/background-copy-toasts.md#L60) | Validation steps and user-facing text of this doc now contradict the shipped UI |
| 🟡 Consider · Could · 📝 docs | [`ready-copy-in-library.md:8`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/documentation/src/content/docs/backlog/ready-copy-in-library.md#L8) | Doc and PR description disagree on the stack base and on email wording |
| 🟡 Consider · Could · ❓ question | [`en.json:1431`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/packages/i18n/messages/en.json#L1431) | PR description promises an email destination's wording, but no message has an email branch |
| 🟡 Consider · Could · 🐛 bug | [`export-status-cards.tsx:199`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx#L199) | Minimized pill: the button's aria-label hides the percent and the nested progressbar |

### Questions for you (2)

- [`sidebar.tsx:102`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/shell/sidebar.tsx#L102) · trade-off — Retiring cards on route-away is a product decision: a card the user may never have seen is lost on leaving (list view, filtered out, library not yet rescanned), and the copy only returns as an outlined card. A person has to decide whether 'seen' means rendered or just 'Library was open'.
- [`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:85`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx#L85) · open question — Drag the finished copy out of the Library's Ready to upload card: Does main's `startFileDrag` handler validate its `id` argument and report a failure? Does dragging from the Library card need to clear the copy's unseen state the way the toast's drag does through `markCopySeen`? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts`.

<details><summary>What the change connects to (5 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- Drag the finished copy out of the Library's Ready to upload card (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:85`) — Does main's `startFileDrag` handler validate its `id` argument and report a failure? Does dragging from the Library card need to clear the copy's unseen state the way the toast's drag does through `markCopySeen`? Files that would answer it: `apps/kaipu-record/src/main/index.ts`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts`.

**Closed, with the lines they rest on**

- Library 'Ready to upload' card: Show in Finder and native drag of the finished copy (`apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`) — The file is revealed or dragged out, but the 'N copies ready' chip and the just-ready outline stay. If it fails: revealLocalRecording is fire-and-forget with `void`, so a rejection is silent. This is the same as the existing toast and the use-local-library reveal. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:280-281`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:293-294`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:80`, `apps/kaipu-record/src/renderer/src/features/library/components/ready-copy-card.tsx:93`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:9-11`.
- Leaving the Library retires all ready cards; Library-page card lifecycle across route changes (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:96-104`) — On the next Library visit the copy is a regular outlined card; the leading card is gone. A copy that finishes while away gets its card on the next visit. If it fails: State is in memory only. Cards are retired even if they were never rendered (list view, filtered out, copy not yet in `videos`). See the finding on sidebar.tsx. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:95-104`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:93-100`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:126-132`, `apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:408-421`.
- Minimized export widget state persisted in sessionStorage and shared across exports (`apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:8-35`) — The pill replaces the card for every later export in the session. A reload keeps the choice and a relaunch resets it. If it fails: If sessionStorage throws, `read()` returns false and set() ignores the error, so the choice lives in memory only. Nothing is written back from a failed read, so no data is lost. The cancel button is… Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:34-55`.
- Destination of a library copy read back from the sidecar fingerprint (`apps/kaipu-record/src/renderer/src/features/prepare/copy-destination.ts:13-17`) — Library cards and Prepare's copy list tag the copy 'For YouTube' and so on. Editor exports, GIFs, originals and files with a null fingerprint get no tag. If it fails: Fails closed: an unknown or missing fingerprint gives null and the regular kind badge. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:185-188`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-reuse.ts:18`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:439-441`, `apps/kaipu-record/src/shared/types/library-storage.ts:49`.
- Minimize the export progress widget to a pill (− button) and reopen it by clicking the pill (`apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:152`) — `ExportStatusCards` (export-status-cards.tsx:40-51) renders the pill when `status === "exporting" && minimized`. It renders the full card when `status === "error"` regardless of the flag, or when exporting and not minimized. The flag survives a reload through sessionStorage and… If it fails: If sessionStorage throws, both the read (10-16) and the write (28-33) swallow the error and the choice stays in memory only. Nothing is lost for the session. Cancel exists only on the expanded card,… Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-widget-state.ts:10-35`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:40-51`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:152-154`, `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:203`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The change replaces the per-export progress-hidden flag with a session-wide minimize pill, adds a Library 'Ready to upload' card, and fixes the destination lookup to ignore the '#revision' suffix on sidecar fingerprints. I read every file in this part and found no blocker. I found three points the author may want to change. The Library card's Show in Finder and drag actions don't mark the copy seen, unlike the ready toast. Leaving the Library retires cards that may never have been rendered. The minimized pill's aria-label hides its percent text from screen readers. I did not check the new CSS modules, the docs and the other files that belong to part 2. The en and es message keys match and the new select keys have `other` fallbacks.

**Batch 2 of 2.** This part (CSS modules, backlog docs, en/es messages) is mostly sound. The CSS variables all exist in `packages/tokens/css/tokens.css` or `base.css`. The removed message keys (`hide`, `readyDragToUpload`) have no remaining users. The en and es files have matching keys and ICU structure. Four things to address, none blocking:\n- `background-copy-toasts.md` still tells people to validate behaviour and strings that this PR removed.\n- The PR description and doc disagree on the stack base, and the description promises email-specific wording that this head does not contain.\n- The minimized pill's aria-label hides the percent from screen readers.\n- One contract stays open: I did not read main's `startFileDrag` handler or check whether the Library card's drag should call `markCopySeen`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 16 | $0.47 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 25 | $0.39 |

</details>

<details><summary>Details of findings with no thread (1)</summary>

**Validation steps and user-facing text of this doc now contradict the shipped UI (confidence high)** ([`background-copy-toasts.md:60`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/e45c845143ba72f35fea4fac2f9d62a186dff986/apps/documentation/src/content/docs/backlog/background-copy-toasts.md#L60))

The new "Update" banner (lines 16-18) is the only correction. "What the user sees" (29-38) and "How to validate" (60-69) still describe strings and behaviour this PR removes. Examples: "Preparing your YouTube copy…", "Your YouTube copy is ready", "Drag to upload", and "Click ✕: the card goes away". The ✕ is now a minimize to a pill, and the strings were rewritten in `backgroundCopy.progressTitle`, `readyTitle` and `dragTo`. The front-matter `description` (line 3) quotes the old strings too. Someone following steps 1, 2 and 6 will not see what they describe. Update the strings and steps, or mark those sections as superseded by `ready-copy-in-library`.

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 38 in / 21k out / 983k cache read / 141k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.87</sub>

<!-- wachi:review -->

<!-- wachiman sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJlNDVjODQ1MTQzYmE3MmYzNWZlYTRmYWMyZjlkNjJhMTg2ZGZmOTg2IiwiYXR0ZW1wdCI6IjNkNDJiZWIyLTA3NDMtNGM0MS04ODIzLWM0ZTEzODViODA2NiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjYsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MX0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=3d42beb2-0743-4c41-8823-c4e1385b8066 -->
