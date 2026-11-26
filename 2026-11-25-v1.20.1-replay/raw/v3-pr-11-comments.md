# kaipu-bench-wachi-v3#11 [replay r2] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:212 · github-actions[bot] · 2026-11-25T21:54:20Z

| 👮 **Wachiman** | A destination picked on screen is not in the URL, so Back loses it |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`selected` starts from `initialDestination` (the `?to=` query) and lives only in component state plus the `chosen` ref (lines 77-84). Picking a card does not update the URL. If the user goes to the Library from Export (for example through `onOpenExisting`, line 162) and then presses Back, the screen remounts under the same history entry and opens on the old `?to=` value, or on "Where is it going?". Their choice, YouTube resolution and framing are gone. Writing the pick back with `setSearchParams({ to: d }, { replace: true })` in `select` would keep it, and it would also let the probe-error redirect (line 98) carry the current choice.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T21:54:20Z

| 👮 **Wachiman** | Dropping a file on the Library now hits Electron's default and navigates the window to the file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Before this change, `useFileDrop` was mounted on the Library. It called `preventDefault` on `dragover` and `drop` for file drags (`features/library/hooks/use-file-drop.ts:29-47`). With the hook removed, no renderer listener handles a file drop on the Library. The main process doesn't guard navigation either: `main/index.ts:400` only sets `setWindowOpenHandler`, and there is no `will-navigate` handler. In Chromium/Electron, a file drop nobody prevents navigates the page to `file:///…/video.mp4`. The main window swaps the app for a bare video player, and any in-progress renderer state, such as the export runner's job, is lost.

The PR body says "dropping a file there does nothing", but the code says it navigates away. Two ways to fix it:
- keep a window-level `dragover`/`drop` `preventDefault` on the Library (or app-wide in the shell);
- add a `will-navigate` guard in main.

The gap probably already exists on the other pages without `useFileDrop`. The Library is where users were just taught to drop files, though, so this is where they will try it.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-25T21:54:20Z

| 👮 **Wachiman** | "does not take a video dropped on the window" passes even if Library still imports drops |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This test does not set `window.electronAPI.pathForFile`, so it uses the default stub from `src/renderer/src/test/setup.ts:156`, which returns `""`. In `importDropped` (`features/library/hooks/use-import-videos.ts:102-111`), a file whose path is empty is treated as skipped, and the function returns before `importVideoFiles` is called. So the assertion `expect(importVideoFiles).not.toHaveBeenCalled()` at line 86 holds whether or not LibraryPage still mounts `useFileDrop`: a regression that brings the drop handler back would still pass. The test that was removed set `pathForFile` (`/Users/me/Movies/${f.name}`) for exactly this reason. Fix: set `pathForFile` to return a real path, as `export-page.test.tsx:421` does. Also assert that the drop is not consumed (`fireEvent.drop(...)` returns true) and that no toast appears, so the test checks that the page ignores the drop.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-25T21:54:20Z

| 👮 **Wachiman** | "with and without a video" only checks the with-video URL |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named for both `/export` and `/export/:assetId`, but it only renders `/export/asset-1`. The case that depends on the non-`end` match at `sidebar.tsx:53` (`ROUTES.exportNew` with no `end`) is the bare `/export` URL plus the deeper one; checking only one of them leaves the other unpinned. Add `renderAt(ROUTES.exportNew)` with the same `aria-current` assertion, or rename the test.

<!-- wachi:finding -->
