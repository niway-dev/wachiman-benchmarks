=== REVIEW 5730212748 2026-11-01T20:51:42Z commit=b12d760
👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

7 finding(s): 3 to fix, 4 to consider; 7 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 6.** I reviewed all 13 files in part 1 and found no defects. These files rename Prepare to Export, add redirects from the old routes, add Email as a destination that shares chat's `balanced` preset, and build the new Export screen out of a header, a drop zone, a destination row and keyboard handling.

What I confirmed:
- **Email destination:** `destinationOfPreset("balanced")` still returns `chat`, because it picks the first match in the `DESTINATION_IDS` order. `usePrepareCopy` now takes an explicit `destination`, so the progress card says Email when Email was picked. The new i18n keys exist in `en.json`.
- **Old URLs:** `/prepare` links redirect to `/export` and keep the `?to=` query.
- **Keyboard handling:** Enter and the arrow keys skip text fields, ordinary buttons and the video picker's dialog. The picker's list items are plain buttons, so Enter on them selects the video as expected.

My only finding is a suggestion: the "Pick from Library" button stays clickable while an imported file is still loading. If someone picks a video during that time, the finished import navigates to the imported file and replaces their pick.

**Batch 2 of 6.** Part 2 has no blockers and nothing that needs a fix. There are two optional suggestions:\n\n- **Recent exports:** a finished Email export is labelled Chat, because Email and chat share the `balanced` preset.\n- **GitHub size bar:** the card is marked as an image, so screen readers only hear the label and never the fits/over-limit result.\n\nWhat I checked and found fine:\n\n- **Enter key:** the screen-wide Enter shortcut correctly ignores Enter inside the video picker's dialog and on its buttons (`isPrimaryEnter`).\n- **Library page:** removing the import controls left no unused imports and no stale import copy.\n- **Removed Prepare component:** its replacement (`export-stage.tsx`) covers what it did.

**Batch 3 of 6.** I found nothing to flag in the 7 files of this part.

- **Deleted Prepare files:** nothing in `apps/kaipu-record/src` still imports `destination-list`, `prepare-drop-zone` or `prepare-page`. `isPrimaryEnter` now lives in `pages/export/export-page.tsx`.
- **Sidebar:** the badge moves from Library to Export. It counts the copy being made (`status === "exporting"`) plus unseen finished copies. Opening `/export`, `/export/:assetId` or `/library` clears the finished ones, as the doc comment says. The `export.railBadge` message exists in `en.json` (line 946). The running-copy count also includes exports started from the editor, since they share one export runner. That fits the label "copies in progress or ready".
- **`useFileDrop` tests:** the new `use-file-drop.test.tsx` keeps every hook check from the deleted `import-drop-zone.test.tsx`. Only the two checks of the deleted component itself go away.
- **Destinations test:** the updated test matches email reusing chat's `balanced` preset. A `Set` removes the duplicate preset, and `balanced` still maps back to chat.

**Batch 4 of 6.** Part 4 covers the new Export page tests and the Library and Library-detail test updates. The Library-detail changes only swap `/prepare/` for `/export/` in the expected paths. The Export page test covers destinations, the keyboard, redirects from old Prepare URLs, and import by drop. There is one finding: the Library test meant to prove the page no longer takes dropped files would pass even if it still did. The test's `pathForFile` stub returns an empty path, so the import is skipped before `importVideoFiles` is ever called.

**Batch 5 of 6.** I found no defects in this part and have one test suggestion.

- **Stylesheets:** every CSS variable the new files use is defined in `packages/tokens/css/tokens.css` or `assets/base.css`. Every class in the new modules is used by its component.
- **Badge text:** the expected text in the sidebar test matches the `export.railBadge` message in `en.json`.
- **Removed Prepare tests:** `prepare-page.test.tsx` is deleted along with `PreparePage`; `export-page.test.tsx` (another part of this review) covers the new page.
- **Suggestion:** the sidebar test that says Export is active "with and without a video" only renders the URL with a video. It should also check `/export` with no video.

**Batch 6 of 6.** Part 6 (routes, the window-size test, the Export stylesheets, the deleted Prepare/Library styles, the backlog docs and the en/es messages). Checks that came back clean:
- The removed `library.import*` and `prepare.prepareAVideo` keys have no remaining callers.
- Every class the new stylesheets define is used by its component.
- The `data-tone` values match what `SizeBarCard` emits.
- The en and es `export` namespaces have the same keys.
- The backlog doc's claims about the rail badge and Recent exports match `sidebar.tsx` and `recent-exports.tsx`: opening Export or the Library clears finished copies, and Recent exports shows three items.

Two small fixes: an orphaned comment left in `library-page.module.css` after `.importZone` was deleted, and a CSS comment that calls the minimum window size the default.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 8 | $0.28 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 9 | $0.33 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 9 | $0.24 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 9 | $0.26 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 12 | $0.31 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 15 | $0.42 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 6 batches · $1.84</sub>

<!-- wachi:review -->

<!-- agent-review sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=f0f0b124-c5ec-4156-933b-d45d1fb11be1 -->

