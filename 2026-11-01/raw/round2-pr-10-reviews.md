=== REVIEW 5730207168 2026-11-01T20:50:22Z commit=b12d760
👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

4 finding(s): 2 to fix, 2 to consider; 4 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 6.** I found nothing to flag in the 13 files of part 1.

- **Routing and paths:** the old `/prepare` URLs now redirect to Export and keep their `?to=` query. `preparePath` and `prepareNewPath` now return Export URLs.
- **Email destination:** it is wired into all the per-destination tables (icons, copy keys, groups and presets). It shares chat's `balanced` preset. Because chat comes before email in `DESTINATION_IDS`, `destinationOfPreset("balanced")` still returns "chat", as the comment says. The new `destination` input on `usePrepareCopy` makes the progress and ready cards name the destination that was actually picked.
- **Keyboard handling on Export:** I read `video-picker.tsx` to check it. Enter does not trigger an export when focus is on a regular button or a field. The Library picker is a dialog whose items are buttons, so Enter inside it doesn't trigger an export either. The arrow keys leave the dialog and the other radio groups alone.

**Batch 2 of 6.** Part 2 covers the new Export stage, Recent exports and video picker, the Library page losing its import controls, and the removal of the Prepare destination detail. The code follows the existing Prepare patterns, and the Library page no longer has unused imports or handlers. One finding (consider): in Recent exports, an email copy is labelled as email while it runs and as chat once it finishes, because the label comes from a preset that both destinations use.

**Batch 3 of 6.** Part 3: I found nothing to flag. Prepare's removed files (destination-list, prepare-drop-zone, prepare-page) leave no references behind; `isPrimaryEnter` and `usePrepareImport` now live in or are used by `pages/export/export-page.tsx`. The sidebar adds an Export rail item using `ROUTES.exportNew`, which is not `end`, so it matches both /export and /export/:assetId as its comment says. Its badge counts the export in progress plus unannounced finished copies, and opening Export or the Library clears the finished ones; the new `railBadge` key exists in en.json and es.json. The `import-drop-zone` test moved to `use-file-drop.test.tsx`, which keeps the hook's coverage. The two tests that went with the deleted component (click opens the dialog, disabled while importing) have counterparts in export-page.test.tsx, which renders the export drop zone. The destinations test changes match email sharing chat's balanced preset.

**Batch 4 of 6.** I reviewed the three test files in this part. The new Export page tests and the `/prepare` → `/export` route updates in the Library detail tests match the new routes. There is one problem. In `library-page.test.tsx`, the test meant to show that Library no longer accepts window drops passes no matter what Library does. The test keeps the global mock where `pathForFile` returns an empty string, so the import hook skips the dropped `.mp4` before `importVideoFiles` would be called. Stubbing `pathForFile` in that test fixes it. I only read the code; I didn't run the tests.

**Batch 5 of 6.** I reviewed all 8 files in this part: the deleted Prepare test and drop-zone stylesheet, the sidebar test, and the Export stylesheets. I found one thing to consider and nothing that blocks the merge.

- **Sidebar test (to consider):** the test named "is active on Export with and without a video" only checks the URL with a video (`/export/asset-1`), never the plain `/export` route. Adding a render of `/export` with the same assertion would make it test what its name says.
- **Stylesheets:** every class used by the Export components is defined. The CSS variables they use exist, either in `packages/tokens/css/tokens.css` or in the app's `base.css`.
- **Deleted Prepare tests:** the coverage was not lost. The drag-and-drop import, "screenshots/only recordings" and "2 more videos" toast cases now live in `export-page.test.tsx`.

**Batch 6 of 6.** Part 6 is in good shape. I read all 11 files and found one small issue: in `library-page.module.css`, the `.importZone` rule was removed but its comment was left behind at line 108. It now sits above the sticky toolbar and reads as if it describes that bar, so it should be deleted.\n\nWhat I checked and found correct:\n- **Routes:** the new `export` and `exportNew` routes and the legacy `prepare` comments match how the router uses them.\n- **Window-size test:** it now covers both Export paths.\n- **New i18n keys:** I spot-checked them against the code (stage, page, rail badge, destination copy), and each one is used. English and Spanish have the same keys.\n- **Removed Library keys:** `importVideo`, `importing`, `importDrop*` and `prepareAVideo` are no longer referenced anywhere in the app.\n- **Backlog doc and index row:** they follow the repository's status-banner and index-row convention.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 4 | $0.21 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 9 | $0.28 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 9 | $0.26 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 6 | $0.25 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 8 | $0.26 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 7 | $0.23 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 6 batches · $1.48</sub>

<!-- wachi:review -->

<!-- agent-review sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=3b8d609e-bf27-4a9f-a922-ec261e8449f1 -->

