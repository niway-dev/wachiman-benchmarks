# kaipu-bench-wachi-v3#46 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:98 · github-actions[bot] · 2026-11-25T23:57:30Z

| 👮 **Wachiman** | An unreadable file drops the destination picked on screen |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

When the probe fails, the page goes back to `/export` with `exportNewPath(urlDestination)`. A destination the user picked on this screen lives only in `chosen.current`, and that is not used here. Every other exit (`openVideo` at line 87, the drop import through `current`) keeps the user's choice through `current()`. So after a Change video to a broken file, the user lands on the drop zone with the old `?to=`, or with none. Using `current()` here would match the other paths.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T23:57:30Z

| 👮 **Wachiman** | Dropping a file on the Library now loads that file in place of the app |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

Before this change, the Library mounted `useFileDrop`, which intercepts `dragover` and `drop` across the whole window. That hook's own comment (`features/library/hooks/use-file-drop.ts:8-11`) explains why: "a file dropped where nothing handles it makes Electron navigate the window to that file." The main process doesn't guard against this. The only navigation hook there is `setWindowOpenHandler` (`main/index.ts:400-403`), which covers new windows only, and nothing in `src` registers `will-navigate`.

With the hook removed from the Library, an MP4 dragged from Finder onto the Library replaces the renderer with the raw file. The app UI is gone until a reload, and so is the renderer-owned export runner with any export in progress. The PR body says "dropping a file there does nothing", but that isn't what happens.

Suggested fix: keep a window-level `dragover`/`drop` handler that calls `preventDefault` and drops the files without importing them. It could run app-wide in the shell, or on the Library only. Alternatively, block file navigation in main with `will-navigate`.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65 · github-actions[bot] · 2026-11-25T23:57:30Z

| 👮 **Wachiman** | A finished Email copy is listed under Slack · Discord in Recent exports |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

While it is running, the row uses `running.destination` (`export-runner.ts:83`), so an Email export shows the Email logo and name. Once it finishes, the row comes from `destinationOfPreset(copy.export!.preset)`. Per the PR body that maps `balanced` to `chat`, so the same copy then reads "Slack · Discord". The PR mentions the shared preset, but not that this strip changes the name of a copy the user just made for Email. Two ways to fix it: store the destination on the export record, or label balanced copies neutrally here.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:85 · github-actions[bot] · 2026-11-25T23:57:30Z

| 👮 **Wachiman** | Test of a drop on the Library ignores whether the window navigates to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

This test only checks that `importVideoFiles` is not called. It throws away the return value of `fireEvent.drop`. After this PR the only window-level drag handler is `useFileDrop` (`features/library/hooks/use-file-drop.ts:49-51`), and only `usePrepareImport` mounts it, from `ExportPage` (`pages/export/export-page.tsx:85`). The main process has no `will-navigate` guard either: a search of `src/` finds only `setWindowOpenHandler` at `main/index.ts:400`. So when a user drops a file on the Library, or on any screen other than Export, nothing calls preventDefault on dragover or drop. Chromium's default then loads the file into the window, and the app is replaced by the file. Before this PR the Library's drop handler covered this. The test passes in exactly that state. Assert what the Export tests assert at `export-page.test.tsx:414-416`: the drop is default-prevented (`expect(fireEvent.drop(...)).toBe(false)`). Then keep a window-level guard that prevents file drops outside Export, either app-wide in the shell or with `will-navigate` in main.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-25T23:57:30Z

| 👮 **Wachiman** | "Active with and without a video" only checks the with-a-video case |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named for both `/export` and `/export/:assetId`, but it only renders `/export/asset-1`. The no-video route `/export` (`ROUTES.exportNew`), which is where the rail link actually points, is never asserted as `aria-current="page"`. A second `renderAt(ROUTES.exportNew)` plus the same assertion would make the test match its name.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:44 · github-actions[bot] · 2026-11-25T23:57:30Z

| 👮 **Wachiman** | The badge's in-progress count is never tested |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`useExportBadge` now adds 1 while `useExportRunner().status === "exporting"` (`apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:121-122`), and the accessible label says "copy in progress or ready". Every test here only drives finished copies through `noteFinishedCopy`, so the running half of the count (the part this PR adds) has no coverage. A case that mocks the runner as exporting and expects the badge to show 1 would pin it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-25T23:57:30Z

| 👮 **Wachiman** | Stale comment for the removed "Drop a video here" strip |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This PR deletes the `.importZone` rule, but the comment above it is still there: `/* NIW2-579: the "Drop a video here" strip, between the header and the toolbar. */`. It now sits directly above the `.stickyBar` comment and describes a strip the Library no longer has. Delete line 108 along with the rule.

<!-- wachi:finding -->
