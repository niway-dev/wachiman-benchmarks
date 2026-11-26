<!-- cap-0.75, oauth-token-3: 12 turns, $0.67 -->

I reviewed the PR's diff and checked the code it calls. I found no definite bugs: nothing that would crash, call a missing function, or show a missing translation. There are three smaller issues worth a look, and none of them is proven.

**What I checked, which all line up:**
- `resolveExportTarget` returns `width` and `height`, so the copy rows can show the picture size.
- `planCopy`, `presetForDestination` and `groupOf` are called with the right arguments. For YouTube, both this panel and Prepare fall back to `defaultYoutubePreset(probe)` when no YouTube preset is given.
- `MasterTag` accepts `size="sm"`.
- `startFileDrag(id, name)` is called the same way as on the "copy ready" card (`export-status-cards.tsx:235`).
- The new translation keys exist in both `en.json` and `es.json`. No code still uses the removed keys (`copyProgress*`, `copiesEmpty`, `where*`). `sendTo` is still used by `video-card.tsx` and `video-row.tsx`, so keeping it is right.
- The deleted `where-is-this-going-strip` is not imported anywhere.

**Possible issues:**

1. **The Reels and LinkedIn cards may show a different size than Prepare** (`destinations-panel.tsx:44-50`). The panel calls `planCopy` without a `framing`, so it uses the default, `null`. Prepare passes `framing: framingOf(d)` (`prepare-page.tsx:218`). If the estimate depends on Fit or Fill, the "Reels · TikTok · Shorts" and "LinkedIn · Feeds" cards can show a size Prepare won't match. The new docs say the panel and the Export screen "cannot disagree", but they only share the list of destinations, not the sizes. I didn't check whether framing changes the estimate. If it doesn't, this is harmless.

2. **After "Not now", a heavy recording with no copies shows the big banner** (`library-detail-page.tsx:2068` in the diff, `heavy && !showDestinations`). Before, a master never showed this banner. Now, once the panel is dismissed, the full "Prepare a light copy →" banner appears below the actions. The docs only describe the banner for "a heavy copy, or a heavy master with copies", and no test covers this case. It may be intended, but it isn't documented.

3. **Every local recording's file is now read when its page opens** (`library-detail-page.tsx:1604`). Before, the file was read only when it was heavy or the "ready" card was showing, and a test checked that a small file was not read. That test assertion was removed. The docs say this is deliberate, so it's a performance cost rather than a bug. On a slow disk or a large file, the metadata line and the size estimates show "…" until the read finishes.

Small note: "Not now" is stored by recording ID, not by visit (`destinationsDismissedFor`). It stays hidden as long as the page stays mounted, even across moves between recordings. The comment says "until the page is left", so this matches what was written.
