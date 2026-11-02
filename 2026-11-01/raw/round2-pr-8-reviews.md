=== REVIEW 5730200407 2026-11-01T20:48:30Z commit=dac8318
👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

3 finding(s): 3 to consider; 3 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 replaces the \"Where is this going?\" strip with a DestinationsPanel, which shows until the first copy exists and can be closed with \"Not now\". It also reworks MasterCopiesPanel into a grid with picture sizes, a Drag handle and \"Open in Export\", and moves the title and metadata on the recording page above the player. Nothing blocks the merge. One UX gap: when the file can't be read, the size on every destination card except Archive stays at \"…\" indefinitely. Two small test gaps: the drag test leaves its mock on the shared stub, and the \"Open in Export\" test never checks that the button is missing without a callback.

**Batch 2 of 2.** I found nothing to flag in the nine files of part 2.

- **Tests:** the updated tests match how the page behaves. The "Where is it going?" panel appears only on an original that has no copies and has not been dismissed (`library-detail-page.tsx:190`). The "Export a copy" button stays hidden while the panel shows (line 436). The saved notice and the "This is your original. It never changes." note never show at the same time (lines 341 and 394).
- **Backlog doc:** it agrees with the code. The panel lists what `DESTINATION_IDS` lists, a card opens Prepare through `preparePath`, and "Not now" hides the panel until the page is left. The doc also says the page now reads the file on every local recording, which is why the old test that checked the file was not read was dropped.
- **Messages:** the strings removed from en/es are no longer used anywhere. `sendTo` stays because the Library's cards and rows still use it, and the new strings exist in both languages.
- **Stylesheets:** the old strip's stylesheet is deleted together with its component.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 7 | $0.25 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 6 | $0.25 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 2 batches · $0.50</sub>

<!-- wachi:review -->

<!-- agent-review sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=64ec1beb-9588-4759-8f98-c5e86c09e22c -->

