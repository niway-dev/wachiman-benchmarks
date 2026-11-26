# kaipu-bench-wachi-v3#36 [replay] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:212 · github-actions[bot] · 2026-11-25T23:53:37Z

| 👮 **Wachiman** | The picked destination is lost on Back from an opened copy |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`selected` starts from `?to=` (line 212), and a pick only updates local state and the `chosen` ref (lines 213-216, 81-83). Nothing writes it back to the URL. Say a user opens `/export/:id` with no `?to=`, picks Email, and the card says Ready. Enter (`primary`, line 264) then navigates to `/library/:existingId`. When they press Back, the screen remounts under the same history entry with no `?to=`, so it shows "Where is it going?" again and their pick is gone. You could replace the history entry with `exportPath(video.assetId, d)` inside `select`, which keeps the pick across Back and remounts.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:17 · github-actions[bot] · 2026-11-25T23:53:37Z

| 👮 **Wachiman** | Recent exports labels editor exports (cuts) and their running jobs as destination copies |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`recentCopies` keeps every recording that has an `export` record, and the row is then named after `destinationOfPreset(copy.export!.preset)` (line 65). The sibling `MasterCopiesPanel` only treats a copy as a destination copy when `copy.export.fingerprint === WHOLE_RECORDING_FINGERPRINT` (`features/prepare/components/master-copies-panel.tsx:133-136`). For the running job it checks `running.wholeRecording` and otherwise shows "edited" (lines 101-103). Here, an Editor export of a trimmed cut with a YouTube or Balanced preset appears as "YouTube" or "Slack · Discord" with a Ready badge. The in-progress row (line 50) also shows such a job under a destination logo. Filter on the whole-recording fingerprint (and `wholeRecording` for the running job), or label those rows the way the panel does.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T23:53:37Z

| 👮 **Wachiman** | What happens now when a file is dropped on the Library? |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟠 Fix |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

The Library no longer mounts `useFileDrop`, which called `preventDefault` on window `dragover` and `drop` (`features/library/hooks/use-file-drop.ts:31-56`). I found no `will-navigate` guard in `src/main`: only `setWindowOpenHandler` at `main/index.ts:400`. Chromium's default for a file dropped on a page that doesn't handle it is to navigate to the file. Does dropping an MP4 on the Library now replace the app's UI with the file, rather than "doing nothing" as the PR says? If so, the window needs a navigation guard or a window-level `preventDefault` outside Export.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:297 · github-actions[bot] · 2026-11-25T23:53:37Z

| 👮 **Wachiman** | GitHub bar is drawn against 10 MB but labelled with the original's size |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

For GitHub, `scale` is `max(copyBytes, 10 MB)`. The labels above the bar are still "Original {size}" on the left and the copy on the right, and the `aria-label` reads "Your recording X, the copy Y". So a 40 MB recording with a 6 MB copy shows a 60% bar under "Original 40 MB", which suggests the copy is 60% of the original. Prepare's version (the removed `destination-detail.tsx`) also kept the "N% lighter" tag next to the limit; this one drops it for GitHub. Consider labelling the right edge as the 10 MB limit when `limited` is true.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-25T23:53:37Z

| 👮 **Wachiman** | "does not take a video dropped on the window" passes even if the Library still handled drops |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

This test no longer sets `window.electronAPI.pathForFile`, so it uses the default from the test setup, which returns `""` (`src/renderer/src/test/setup.ts:156`). `importDropped` treats a file with an empty path as skipped and returns before it calls `importVideoFiles` (`features/library/hooks/use-import-videos.ts:102-111`). So `importVideoFiles` stays uncalled whether or not the Library still listens for window drops, and the test can't catch a regression. The deleted test set `pathForFile` for exactly this reason.

Fix: set `window.electronAPI.pathForFile = vi.fn((f) => \`/Users/me/Movies/${f.name}\`)` here, as `export-page.test.tsx:421` does. Also assert that no toast was raised, or that the `drop` event was not `preventDefault`ed, so a handler that only skips the file also fails the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-25T23:53:37Z

| 👮 **Wachiman** | "with and without a video" only checks the with-video URL |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test renders only `/export/asset-1`. The comment at `sidebar.tsx:52` says the Export item is lit on both `/export` and `/export/:assetId`, but no test checks the bare `ROUTES.exportNew` path. Add `renderAt(ROUTES.exportNew)` with the same `aria-current` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-25T23:53:37Z

| 👮 **Wachiman** | Orphaned comment for the removed import strip |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

`.importZone` was removed, but its comment ("NIW2-579: the \"Drop a video here\" strip, between the header and the toolbar.") still sits right above the `.stickyBar` comment. It now describes nothing, and it reads as if it were about the sticky bar. Delete it along with the rule.

<!-- wachi:finding -->

## packages/i18n/messages/en.json:921 · github-actions[bot] · 2026-11-25T23:53:37Z

| 👮 **Wachiman** | GitHub limit is hardcoded as "10 MB" in the strings, separate from the constant that draws the bar |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`barFitsLimit` and `barOverLimit` (and their es.json counterparts at the same lines) spell out "10 MB". The bar itself is scaled by `GITHUB_FREE_LIMIT_BYTES` (`export-stage.tsx:297`), and the tone comes from `plan.underGithubFreeLimit` (`export-stage.tsx:300-307`). If that limit changes, the bar and the fits/over verdict follow it but the text does not. Consider passing the limit as an ICU argument, e.g. `{limit}`, formatted from the same constant.

<!-- wachi:finding -->
