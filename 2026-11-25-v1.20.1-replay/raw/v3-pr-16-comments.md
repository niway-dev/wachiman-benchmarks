# kaipu-bench-wachi-v3#16 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:98 · github-actions[bot] · 2026-11-25T21:55:23Z

| 👮 **Wachiman** | Unreadable-file redirect drops the destination picked on this screen |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The probe-error effect sends the user back to `exportNewPath(urlDestination)`. It ignores `chosen.current`, but every other exit from this screen goes through `current()`: `openVideo` at line 87 and the drop import via `usePrepareImport` at line 85. Say a user opens a video with no `?to=`, picks a card and Change video lands on a file that can't be read. The stored pick never reaches that path, since `openVideo` already put it in `?to=`. The gap is the other case: a video whose probe fails after a card was picked on the same mount. There the redirect loses the pick. Using `current()` here, and adding it to the deps, would make the redirect behave like the other exits.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/destination-row.tsx:13 · github-actions[bot] · 2026-11-25T21:55:23Z

| 👮 **Wachiman** | \`DestinationSizes.sizeText\` doc promises an "up to" form the row never gets |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The doc says `sizeText` returns "~570 MB", "up to ~570 MB" or "Full size". But `ExportScreen` passes `sizeText: estimateText` (export-page.tsx:337), and `estimateText` (export-page.tsx:241-244) never returns the "up to" form. Only the stage's `sizeText` (export-page.tsx:245-248) does. Either fix the comment or pass the same formatter, so nobody later expects the cards to say "up to".

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-25T21:55:23Z

| 👮 **Wachiman** | A file dropped on the Library now sends the whole window to that file |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The Library no longer calls `useFileDrop`, and nothing else handles window drops while it is open. The hook's own doc says why it covers the whole window: "a file dropped where nothing handles it makes Electron navigate the window to that file" (`features/library/hooks/use-file-drop.ts:9-11`). The main process does not guard against this either. `main/index.ts:400-411` sets only `setWindowOpenHandler`, and the repository has no `will-navigate` handler. So step 12 of the PR body ("dropping a file there does nothing") is not what happens: dropping an MP4 on the Library replaces the app with Chromium's file viewer. That also throws away renderer state, including an export the renderer owns (`main/index.ts:396`). The fix is to keep a no-op drop guard on the Library, for example `useFileDrop(() => {})`, or better, one guard for the whole app: `preventDefault` on `dragover`/`drop` at the root, or a `will-navigate` handler in main. Then only Export imports, and no screen can navigate away.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-stage.tsx:228 · github-actions[bot] · 2026-11-25T21:55:23Z

| 👮 **Wachiman** | Fill / Fit lost its preview, and the frame-rate cap and sound changes are no longer shown |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The deleted `ShapeCard` (`destination-detail.tsx`) rendered `FramingPreview` with the recording's thumbnail for each framing, so the user could see that Fill crops the edges. The new framing radios have only a `title` tooltip. The deleted `ChangesCard` also showed when smoothness was capped (`smoothCapped`) and how the sound changes. `DestinationStage` reads neither `plan.smoothness` nor `plan.sound`. The PR describes the change as "restyled, not rewritten", but this information is gone from the screen. If the design file drops these on purpose, say so in the backlog doc. Otherwise, bring back at least the framing preview for TikTok · Reels and LinkedIn · Feeds.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:122 · github-actions[bot] · 2026-11-25T21:55:23Z

| 👮 **Wachiman** | Badge moved to Export, but the old Library vocabulary stays behind |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The badge now sits on the Export item. Several names and strings still describe it as the Library's:
- `backgroundCopy.libraryBadge` (en.json/es.json:1487) has no caller left in `src/`. This line was its only reader.
- `libraryBadgeCount` (ready-copies.ts:70) now feeds the Export badge.
- The ready-copies.ts module doc (lines 5-12) still says "the Library rail item then carries a count" and "ANNOUNCED once the Library page has been open". Opening Export now announces them too (sidebar.tsx:117-119).

Suggested fix: delete the dead key, and rename the function or update its doc so the next reader isn't misled.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-25T21:55:23Z

| 👮 **Wachiman** | "Does not take a dropped video" does not check that the window stops the drop, so Electron can still open the file in the app window |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The new test only checks that `importVideoFiles` is never called. It does not check whether anything stopped the drop. The Export test checks exactly that with `!fireEvent.drop(...)` (export-page.test.tsx:414-416), and its comment says why: "Electron does not navigate the window to the file". Library no longer mounts the window-wide `useFileDrop` listener, which was the code that called `preventDefault` on `dragover`/`drop` (use-file-drop.ts:31,49-51). The main process has no `will-navigate` guard either: a search of `src/` finds none. So a file dropped on the Library now likely makes the BrowserWindow load `file://…/Zoom Meeting.mp4` and replace the app, which is the opposite of the PR's claim that "dropping a file there does nothing". This test passes either way. Assert what the user would see: make `fireEvent.drop` return false (some listener prevented the default) while `importVideoFiles` is still not called. Then add a window-level `dragover`/`drop` `preventDefault` for screens that don't take drops, either in the shell or as a main-process `will-navigate` guard.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-25T21:55:23Z

| 👮 **Wachiman** | "with and without a video" only renders the with-video URL |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named "is active on Export with and without a video", but it only renders `/export/asset-1`. The bare `/export` route (`ROUTES.exportNew`, the link's own target) is never checked for `aria-current`. Lighting the item on `/export/:assetId` relies on `isActive` matching with `end: false` (`sidebar.tsx:68-69`, `sidebar.tsx:53`). Adding `renderAt(ROUTES.exportNew)` with the same assertion would make the test cover what its name says.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-25T21:55:23Z

| 👮 **Wachiman** | Orphaned comment for the removed import strip |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The `.importZone` rule was removed, but its comment ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still here. It now sits directly above the sticky toolbar's comment, so it reads as if it described the toolbar. Remove it along with the rule.

<!-- wachi:finding -->
