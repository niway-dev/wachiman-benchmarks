=== REVIEW 5730200517 2026-11-01T20:48:32Z commit=e45c845
👮 **Wachiman** · review of the whole pull request, at `e45c845`: all 31 files reviewed.

2 finding(s): 2 to consider; 2 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 has no defects that need fixing; two optional suggestions. The Ready-to-upload card store (`ready-copies.ts`), reading the destination through the `#revision` fingerprint suffix, the minimized widget state and how the sidebar retires cards are consistent with each other and with the tests. The ICU selects for `dragTo` and `pill` cover every destination. One Library test claims more than it asserts. While the ready card shows, a copy loses its grid actions (delete, tags, prepare, edit).

**Batch 2 of 2.** Part 2 (stylesheets, docs, i18n messages) has no findings. Nothing in the renderer still uses the removed keys (`hide`, `readyDragToUpload`). The new keys (`minimize`, `expand`, `pill`, `progressNote`, `dragTo`, `destinationTag`, `readyToUpload`, `fromOriginal`, `readyCardLabel`, `readyCardClose`) are used by `export-status-cards.tsx`, `ready-copy-card.tsx` and `destination-tag.tsx`. en and es contain the same keys. The CSS variables these styles use (`--tone-saving`, `--accent-primary-ring`) are defined in or already used across the renderer. The destination-tag colours match `destination-logo.module.css`, as its comment says. The Library grid has a fixed 3 columns (`library-page.module.css:368`), so `grid-column: span 2` always fits. The new backlog doc has a status banner and a row in `backlog/index.mdx`, and its text matches the messages.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 4 | $0.26 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 9 | $0.23 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 2 batches · $0.49</sub>

<!-- wachi:review -->

<!-- agent-review sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:attempt id=71141bb3-e714-4ded-a0b5-11bc8b4f902b -->

