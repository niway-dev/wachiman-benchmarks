=== REVIEW 5730176663 2026-11-01T20:42:29Z commit=e45c845
👮 **Wachiman** · review of the whole pull request, at `e45c845`: all 31 files reviewed.

1 finding(s): 1 to consider; 1 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** I reviewed all 22 files in part 1 and found one optional issue, at "consider" level. Nothing needs fixing before merge.

- **The ready-copy flow looks consistent.** When the Library shows a copy's "Ready to upload" card, the copy's regular card steps aside. Closing the card, opening the copy, or leaving the Library removes the card, and leaving is handled by watching the route in `sidebar.tsx`.
- **`copyPresetOf` now handles fingerprints with a "#" suffix.** I checked `encodeFingerprint` and `WHOLE_RECORDING_FINGERPRINT = "whole"`, so splitting on "#" fixes the master-copies panel for real YouTube copies.
- **Replacing `progressHidden` with the minimized state works.** The new state lives in `export-widget-state.ts`, is kept for the session, and errors still show in full while the widget is minimized. The tests cover this.

**The finding:** in the minimized pill (`export-status-cards.tsx:216`), the progress bar sits inside a button whose label overrides its content. Screen readers announce only "Show the export's progress" and never the percent.

**Batch 2 of 2.** No findings in this part. Checks made:
- **Removed i18n keys:** nothing under apps/ still uses the removed `backgroundCopy.hide` and `backgroundCopy.readyDragToUpload` keys.
- **Matching translations:** en.json and es.json add the same new keys with the same ICU select branches.
- **CSS variables:** the new stylesheets only use variables that are defined. `--bg-modal` and `--accent-primary-ring` come from packages/tokens, `--tone-saving` from base.css, and `--bg-hover` has a fallback.
- **Destination colours:** destination-tag.module.css uses the same colours as destination-logo.module.css, as its comment says.
- **Docs:** the backlog doc has the status banner and an index row, as CLAUDE.md requires. Its "Drag to …" labels match the `dragTo` messages.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 4 | $0.30 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 8 | $0.20 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 2 batches · $0.51</sub>

<!-- wachi:review -->

<!-- agent-review sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:attempt id=1eb32221-3802-40ba-93b9-86e8ee9b87df -->

