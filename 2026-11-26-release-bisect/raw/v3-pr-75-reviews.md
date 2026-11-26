# kaipu-bench-wachi-v3#75 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:03:21Z · commit b12d760

👮 **Wachiman** · review of the whole pull request, at `b12d760`: all 47 files reviewed.

8 finding(s): 2 to fix, 6 to consider; 8 on their lines. Reply in a comment's thread to answer it.

### Risk map

**Medium.**

- `public-contract` · `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts:13` — `preparePath`/`prepareNewPath` keep their names but now return `/export` URLs, so every caller, including sibling branches, lands on the new screen.

**Needs a person:**

- `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:71` (`tradeoff`) — Email shares chat's Balanced preset, so one copy shows "Ready" on both cards and `destinationOfPreset` answers "chat". The status cards also have no email branch, so they say "your export" for an Email copy.

**Read first:** `apps/kaipu-record/src/renderer/src/features/prepare/prepare-path.ts`, `apps/kaipu-record/src/renderer/src/pages/prepare/destination-detail.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx`.

### Summary

**Batch 1 of 6.** I read every file in part 1. I found no blockers, and two considers in the new Export screen. First, the window-wide Enter handler skips dialogs for the arrow keys but not for Enter, so Enter can start an export behind an open \"Change video\" list. Second, \"Pick from Library\" stays enabled during an import, while \"Browse files…\" is disabled. One question is left open: I did not read the body of `useSourceProbe`, so I could not confirm what bounds the \"Reading…\" wait if the probe never settles.

**Batch 2 of 6.** I found one fix and one consider in this part. The fix is in `library-page.tsx:53`: the Library no longer mounts `useFileDrop`, and nothing else in the app stops a file dropped on the window. Main has no `will-navigate` guard. So dragging a video from Finder onto the Library makes Electron load that file in the app window and replaces the app, with no error shown. The PR says the drop "does nothing" there. I rate this medium confidence because I could not run Electron to watch it happen. The consider is in `export-stage.tsx:201`: the 1440p / 4K and Fill / Fit radio groups don't respond to arrow keys, and the screen's own arrow handler skips them because its comment assumes they handle arrows themselves. I found nothing to flag in `recent-exports.tsx`, `video-picker.tsx` or the deleted `destination-detail.tsx`.

**Batch 3 of 6.** Part 3 covers the deleted Prepare page files, the sidebar's new EXPORT item and badge, the move of the drop-zone tests to `use-file-drop.test.tsx`, and the destination tests for Email. The deleted Prepare components are not referenced anywhere else in the code. `isPrimaryEnter` is re-implemented in `export-page.tsx`. The rewritten hook test keeps the four `useFileDrop` behaviours, and the two dropped tests covered only the deleted component. The destination tests match the "Email shares Balanced, `destinationOfPreset(\"balanced\")` is `chat`" decision in the description. One "consider" finding: the badge's new running-export term counts an export whose progress card is on screen, unlike the existing rule that leaves out a copy whose ready card is visible. Editor exports also light the EXPORT badge.

**Batch 4 of 6.** I reviewed the three test files in part 4 and found one problem. The new Library test, "does not take a video dropped on the window", only asserts that no import ran. It does not check that the drop's default action was prevented. Nothing on the Library prevents that default now, and main has no will-navigate guard, so a file dropped on the Library likely makes Electron load the file in place of the app. The Export test already checks this with the return value of `fireEvent.drop`, and the Library test should do the same. The library-detail test edits are mechanical `/prepare` → `/export` path updates. In the Export test I found nothing wrong.

**Batch 5 of 6.** I found no defects in this part, only one small test gap.

**Test gap (consider):** in `sidebar.test.tsx:39`, the test "is active on Export with and without a video" only renders `/export/asset-1`. The case with no video, plain `/export`, is never checked. Either add that case or rename the test.

**Checked and correct:**
- **Sidebar badge tests:** they match `useExportBadge` in `sidebar.tsx` and the `export.railBadge` plural message in `en.json`.
- **Stylesheets:**
  - Every class the new CSS defines is used by its component.
  - Every CSS variable it uses is defined in `packages/tokens` or `base.css`.
  - The `data-tone` and `data-group` values match what `destination-row.tsx` and `destinations.ts` produce.
  - The new `email` logo colour matches the new `email` destination.
- **Deleted files:** nothing in the app still imports the deleted `import-drop-zone.module.css`. The removed Prepare test file has a replacement in `export-page.test.tsx`, which also covers the redirects from the old `/prepare` routes.

**Batch 6 of 6.** This part covers the route constants, the stylesheets, the backlog doc and the i18n messages. `routes.ts` still holds only literals, so the preload rule holds. The i18n keys removed from the `library` namespace (importVideo, importDropTitle and the rest) and from `prepare` (`prepareAVideo`) are no longer referenced anywhere in kaipu-record. The en and es namespaces match key for key. Every class name `export-stage.tsx` uses has a rule, and the new `data-tone` values match the selectors. The backlog doc's claim that the badge is cleared on Export or the Library matches the sidebar code. The only finding is a stale comment left in the library stylesheet.

<details><summary>What the change connects to (13 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Wait on the source probe before the screen renders (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:144`) — Does `probeSource` have a timeout, or can it hang forever on a stalled file? Files that would answer it: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts`.

**Closed, with the lines they rest on**
- Enter on the Export screen runs the primary action: it opens an existing copy or starts a new one (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:277`) — The export starts in the background and the progress card shows it, or the Library page of the existing copy opens. If it fails: With the VideoPicker dialog open and focus off a button, Enter starts an export behind the list. If an export is already running, `copy.start` shows the busy toast. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:356-386`, `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:68-75`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:99-101`.
- Change video, or Pick from Library, navigates to another asset and carries over the chosen destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:86`) — Export opens on the new video with the same card selected. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:73-88`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:150-158`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:42-52`.
- Legacy /prepare URLs redirect to /export with the query kept (`apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:168`) — The Export screen opens with `?to=` kept. Evidence: `apps/kaipu-record/src/renderer/src/app/router.tsx:72-74`, `apps/kaipu-record/src/shared/routes.ts:17-24`.
- Library stops handling window file drops (useImportVideos/useFileDrop removed) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53`) — Electron's default runs: the window navigates to the dropped file and the app UI is replaced. If it fails: Silent: there is no toast and no error. The user has to reload the app. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-11`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:48-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:400`.
- VideoPicker adds document mousedown/keydown listeners while open (`apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`) — Escape or a click outside closes the list. Enter and the arrows inside the dialog are skipped by the screen handlers (button and dialog checks). Evidence: `apps/kaipu-record/src/renderer/src/pages/export/video-picker.tsx:45-59`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:364`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:384`.
- SizeBarCard tone and GitHub limit bar (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:295-307`) — The CSS styles the tones lighter/fits/not-lighter/over. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:202-203`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:219-227`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:262-268`.
- Rail EXPORT badge = running export + unannounced finished copies (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`) — A number on the EXPORT rail item with the aria label export.railBadge (en.json:946). If it fails: When the runner goes to "error", running drops to 0 and the progress card comes back with the error (export-runner.ts:337-341). Nothing is lost. The store lives in memory, so a relaunch clears it (re… Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:66-75`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:26`, `packages/i18n/messages/en.json:946`.
- Opening /export or /export/:assetId announces ready copies (clears the badge's finished part) (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117-119`) — The badge's finished-copy count goes to 0 while on Export. The Library chip and outline remain until the copy is opened. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:114-120`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-64`, `apps/kaipu-record/src/shared/routes.ts:18-20`.
- A file dropped on the window while the Library is shown (the Library no longer mounts the drop hook) (`apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80`) — With no handler, Chromium/Electron treats the drop as a navigation to the file, which replaces the app's renderer. If it fails: Main has no will-navigate guard, so the window loads the file and the app UI disappears until it is reloaded. Evidence: `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:8-12`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-file-drop.ts:40-51`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-import.ts:55`, `apps/kaipu-record/src/main/index.ts:400-403`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:414-416`.
- The Export test mocks useVideoExport and asserts the start() arguments for each destination (`apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:13-22`) — The screen stays on /export/:assetId after the export starts (test line 209), which matches the PR's stated decision. If it fails: The busy path is covered by mocking isVideoExportBusy (test lines 24-28, 319-327). Real worker failures are left to use-video-export.test.ts, as the comment at line 11 says. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:252-266`, `apps/kaipu-record/src/renderer/src/pages/export/export-page.test.tsx:187-213`.
- Sidebar Export entry carries the copy badge, cleared on Export or Library (`apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44`) — Export link shows a count, with aria label '# copy/copies in progress or ready' from export.railBadge. Evidence: `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:79-81`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:111-123`, `packages/i18n/messages/en.json:946`, `apps/kaipu-record/src/shared/routes.ts:18-20`.
- New `export`/`exportNew` routes added to ROUTES, with the `prepare`/`prepareNew` entries kept as legacy redirects (`apps/kaipu-record/src/shared/routes.ts:17-24`) — The sidebar entry points to ROUTES.exportNew (sidebar.tsx:53), and the badge-clearing logic matches the exportNew prefix (sidebar.tsx:117). Evidence: `apps/kaipu-record/src/shared/routes.ts:13-42`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:53`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117`, `apps/kaipu-record/src/shared/window-size.test.ts:21-22`.
- Size bar tone switched from `data-direction` to `data-tone`, with new fits/over values (`apps/kaipu-record/src/renderer/src/pages/export/export-stage.module.css:262-291`) — The tag colour and bar fill colour follow the tone. Evidence: `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:307`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:320`, `apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:329`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 6 | 13 | 777 | 4 | reviewed | 7 | $0.53 |
| Batch 2 of 6 | 5 | 987 | 4 | reviewed | 11 | $0.53 |
| Batch 3 of 6 | 7 | 789 | 4 | reviewed | 8 | $0.42 |
| Batch 4 of 6 | 3 | 603 | 2 | reviewed | 8 | $0.46 |
| Batch 5 of 6 | 8 | 854 | 2 | reviewed | 14 | $0.52 |
| Batch 6 of 6 | 11 | 843 | 4 | reviewed | 10 | $0.45 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 6 batches · 64 in / 28k out / 1.1M cache read / 265k cache write · Claude subscription: API-equivalent estimate, not a bill · $2.90</sub>

<!-- wachi:review -->

<!-- wachiman sha=b12d760bd90b1e9619bab115f500f9c1a30cccf3 -->

<!-- wachi:attempt id=9ee51489-2449-4948-a11c-0cf9950aba66 -->
