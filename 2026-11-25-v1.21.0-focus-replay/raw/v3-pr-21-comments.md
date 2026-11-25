# kaipu-bench-wachi-v3#21 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:375 · github-actions[bot] · 2026-11-25T22:56:19Z

| 👮 **Wachiman** | Enter can still start an export while the Change video picker is open |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`destinationStep` skips arrow keys pressed inside `[role='dialog']` (line 364), but `isPrimaryEnter` has no matching check. `VideoPicker` renders its panel as `role="dialog"` and never moves focus into it (video-picker.tsx:68-75). If the user opens it and then clicks the panel's empty area or the "no videos" text, focus drops to `body`. Line 381 then returns true, so pressing Enter starts an encode behind the open picker. Adding the same `closest("[role='dialog']")` guard here would make Enter behave like the arrows.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.tsx:40 · github-actions[bot] · 2026-11-25T22:56:19Z

| 👮 **Wachiman** | Pick from Library stays enabled while an import is running |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

"Browse files…" is disabled while `importing` (line 51), but the `VideoPicker` trigger is not. Say the user picks a Library video during an import. When the import finishes, `usePrepareImport` calls `navigate(preparePath(first.assetId, …))` (use-prepare-import.ts:48), and that replaces the screen they just opened with the imported video. Disabling the trigger while `importing` would prevent this.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:55 · github-actions[bot] · 2026-11-25T22:56:19Z

| 👮 **Wachiman** | Comment says \`usePrepareCopy\` is reused unchanged, but it was changed |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The doc comment says Export reuses "`usePrepareCopy` and the background export runner" as is, and the PR body says "reused unchanged". This PR adds a `destination` override to `PrepareCopyInput` (use-prepare-copy.ts:77,119) so Email copies are not labelled as chat. The comment could mention that change.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T22:56:19Z

| 👮 **Wachiman** | Dropping a file on the Library now falls through to Electron's default: the window navigates to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The PR removes `useFileDrop` from the Library, and the PR body says "dropping a file there does nothing". `useFileDrop` was the only thing on this screen that called `preventDefault` on `dragover`/`drop` (`features/library/hooks/use-file-drop.ts:29-47`). The main process has no `will-navigate` guard: `src/main/index.ts` only sets `setWindowOpenHandler` (line 400), and a search of `src/main` finds no `will-navigate`. With nothing intercepting the drop, Electron's default for a file dropped on a BrowserWindow is to load that file in the window. The app's UI is then replaced by the video, and the user is left with no way back. Before this PR the Library intercepted the drop. To make "does nothing" true, either keep a passive window-level `dragover`/`drop` `preventDefault` on the Library (or app-wide in the shell), or block file navigation in main with `webContents.on('will-navigate', e => e.preventDefault())` for non-app URLs. I could not run the app to confirm, which is why confidence is medium.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-25T22:56:19Z

| 👮 **Wachiman** | An Email export changes from "Email" to "Slack · Discord" in Recent exports once it finishes |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The running row's logo comes from `running.destination` (`export-runner.ts:59`), so an Email export in progress shows the Email logo. A finished row comes from `destinationOfPreset(copy.export!.preset)`. The sidecar only stores `{ preset, fingerprint }` (`shared/types/library-storage.ts:49`), and `destinationOfPreset("balanced")` returns `"chat"` (`features/prepare/destinations.ts:102-107`). So the same row flips from the Email logo to Slack · Discord's logo and name as soon as it finishes. The PR lists "balanced → chat" as a known decision, but this strip shows the change happen live. You could either show a neutral label for presets several destinations share, or persist the destination with the export.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:117 · github-actions[bot] · 2026-11-25T22:56:19Z

| 👮 **Wachiman** | The badge clears on /export/:assetId, a screen that doesn't show the finished copies |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`matchPath({ path: ROUTES.exportNew, end: false }, …)` matches `/export/:assetId` as well as `/export`, so `announceReadyCopies()` runs on every Export screen. Only the no-video branch renders `RecentExports` (`pages/export/export-page.tsx:101-115`). The recording branch shows nothing that points at the finished copies, so the doc comment's "both point at the copies" (line 107) is not true for it.

What goes wrong:
- A user opens Export on a recording from a Library card or the "Prepare for…" chips. Every copy that finished earlier (with its ready card hidden or closed) is marked announced, and the rail badge drops to 0 without the user being shown those copies.
- Export now stays on screen after an export starts. The effect re-runs on `copies` (line 120), so a copy that finishes while the user is on `/export/:assetId` is announced at once. If the user then closes its ready card, nothing on the rail says a copy is waiting. Under Prepare, the screen navigated back to the recording, so the badge did count it.

The fix: announce only on the exact `/export` route (`end: true`), the screen that lists recent exports, as the Library match on line 118 already does. Note that `RecentExports` shows only the newest three, so even `/export` can clear a fourth unseen copy that it doesn't list.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-25T22:56:20Z

| 👮 **Wachiman** | Library no longer handles file drops, so a video dropped there navigates the Electron window to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This test checks that Library does not import a dropped video. It does not check what the window does with the drop. Before this PR, Library mounted the window-wide drop handler. `useFileDrop` is now mounted only through `usePrepareImport` (`features/prepare/use-prepare-import.ts:55`), and only `ExportPage` calls that (`pages/export/export-page.tsx:85`). The hook's own comment says why it listens on the whole window: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:10-11`). Main has no `will-navigate` guard either; only `setWindowOpenHandler` is set (`main/index.ts:400-403`).

So a user who drops a video on Library, as they could before this PR, now sees the whole app window replaced by the video file. No error or toast explains it. The Export tests guard this case with `!fireEvent.drop(...)` (`export-page.test.tsx:414-416`). This test should assert the same, and the app should refuse the drop outside Export. Two ways to do that: a shell-level `dragover`/`drop` `preventDefault`, or a `will-navigate` guard in main.

<!-- wachi:finding -->
