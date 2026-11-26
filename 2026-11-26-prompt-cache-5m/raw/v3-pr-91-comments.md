# kaipu-bench-wachi-v3#91 [replay r3] feat(desktop): Export screen with its own rail entry (replaces Prepare) - bot inline comments

## apps/kaipu-record/src/renderer/src/pages/export/export-page.tsx:352 · github-actions[bot] · 2026-11-26T17:04:37Z

| 👮 **Wachiman** | destinationStep's docstring says a held key is ignored, but the code never checks event.repeat |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The docstring says `destinationStep` returns null for "a held key". The body (lines 356-366) never checks `event.repeat`, unlike `isPrimaryEnter` at line 376. Holding → or ← therefore keeps moving the selection along the row. Either add `event.repeat` to the early return at line 358 or remove "a held key" from the comment, whichever behaviour you want.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:53 · github-actions[bot] · 2026-11-26T17:04:37Z

| 👮 **Wachiman** | Dropping a file on the Library now falls through to Chromium's default navigation |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The Library no longer mounts `useFileDrop`. That hook was the only thing calling `preventDefault` on window `dragover`/`drop` (`features/library/hooks/use-file-drop.ts:29-51`). I searched `src/` and found nothing else that handles those events, and the main window has no `will-navigate` guard (`main/index.ts:400-411` only sets `setWindowOpenHandler`). So when a user drops an MP4 on the Library, Electron's default most likely navigates the main window to the `file://` URL of the video. That replaces the app UI until the user reloads. The PR's test step 12 says this "does nothing", which I don't think is what happens. A fix: keep a window-level `dragover`/`drop` `preventDefault` on screens that don't import (for example in the shell), or block file navigations in `will-navigate` in main. Either way, test it in Electron, because the PR says the app was not run there.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80 · github-actions[bot] · 2026-11-26T17:04:37Z

| 👮 **Wachiman** | Library no longer handles window drops, so a file dropped there falls through to Electron's default navigation; the test only checks that no import happens |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟠 Fix |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

Before this change Library mounted the window-wide drop handler (the removed test "imports a video dropped anywhere on the window"). The change removes it, and the only remaining caller of `useFileDrop` is Export (`features/prepare/use-prepare-import.ts:55`, used only from `pages/export/export-page.tsx:85`). Nothing else in `src` handles `drop` or `dragover`, and main registers no `will-navigate` guard (I searched `src` and found none).

The repo's own comment at `features/library/hooks/use-file-drop.ts:10-11` says what happens next: "a file dropped where nothing handles it makes Electron navigate the window to that file." The renderer is replaced by the video file. A background export runs in that renderer (`main/index.ts:338-340`), so it would be destroyed and leave its `.part` behind, with no confirmation dialog because the close guard does not fire on a navigation.

This test asserts only that `importVideoFiles` is not called. It ignores `fireEvent.drop`'s return value, which is `true` here because nobody called `preventDefault` (see the helper comment at `export-page.test.tsx:414-416`). So the test passes while the navigation it should catch goes through. The same holds for every screen other than Export.

Fix: keep a window-level guard that calls `preventDefault` on `dragover`/`drop` for files and does not import, either app-wide in the shell or with `will-navigate` prevented in main. Then assert `expect(fireEvent.drop(document.body, …)).toBe(false)` here.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39 · github-actions[bot] · 2026-11-26T17:04:37Z

| 👮 **Wachiman** | "active with and without a video" only checks the case with a video |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The test is named for both `/export` and `/export/:assetId`, but it only renders `/export/asset-1` (line 40). The bare `/export` case is the one that depends on the NavLink not using `end` (`sidebar.tsx:53`), and nothing here checks it. Add `renderAt("/export")` with the same `aria-current` assertion, or rename the test.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/export/export-drop-zone.module.css:10 · github-actions[bot] · 2026-11-26T17:04:37Z

| 👮 **Wachiman** | Dropping the scroll box means the no-video drop zone can overflow onto Recent exports in a short window |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`.wrap` is now `flex: 1; min-height: 0` with no `overflow`, inside `.screen`, which is `overflow: hidden` (`export-page.module.css:15`). `RecentExports` comes right after it (`export-page.tsx:105-112`). When the window is shorter than the zone's content (36px padding, heading, body, actions), `.wrap` shrinks to its min-height of 0, the zone spills out of it and gets painted over the Recent exports list. Nothing scrolls, which goes against the page comment that the content scrolls when there isn't enough room. The old rule had `overflow-y: auto`. The comment gives a reason for dropping it: the picker panel (`video-picker.module.css:6-12`, absolutely positioned) must not be clipped. Another option is to keep the scroll box and let the panel escape it, for example with a portal or `position: fixed`, or to give `.wrap` a min-height that fits the zone.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108 · github-actions[bot] · 2026-11-26T17:04:37Z

| 👮 **Wachiman** | Orphaned comment for the removed import strip |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧹 cleanup |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The PR removes `.importZone`, but the comment above it ("NIW2-579: the 'Drop a video here' strip, between the header and the toolbar.") is still there. It now sits right on top of the sticky toolbar's comment and describes a strip the Library no longer has. Delete it along with the rule.

<!-- wachi:finding -->
