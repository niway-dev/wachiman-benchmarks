<!-- cap-3, api-key-2: 27 turns, $0.93 -->

I found one real bug and one inaccurate line in the docs. The rest of the change matches the code it calls. I didn't run the tests and didn't modify any file.

## Bug

**`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263` and `:311`: if the file can't be read, the size estimates show "…" forever.**

- **What goes wrong:** `estimate()` returns `null` whenever `probe` is null, and the card then shows `{size ?? "…"}`. `probe` comes from `useSourceProbe(...).probe` (`library-detail-page.tsx:142`), which is null both while loading and when reading the file fails.
- **When it fails:** `probeSource` returns `null` on any error (`probe-source.ts:42-43`). `isUsableProbe` also rejects a result with zero width, height or duration (`use-prepare-copy.ts:29-31`). In both cases `useSourceProbe` settles on `{ status: "error", probe: null }`.
- **Why it matters:** the page only passes `.probe` to the panel, so it can't tell "still reading" from "failed". For a corrupt or unsupported imported file, the YouTube, Reels, LinkedIn, GitHub and Slack cards keep a loading "…" that never resolves.
- **Why it's new:** before this PR, the file was only read when the recording was heavy or the "ready" card was showing, and nothing rendered a loading placeholder for it.
- **Fix:** pass the probe `status` (or a `failed` flag) through, and drop the size line when it is `"error"`.

## Docs inaccuracy

**`apps/documentation/src/content/docs/backlog/prepare-screen.md:179` (the QA script):** it says "Drag the copy's row out of the page into Finder". In `master-copies-panel.tsx:164-180`, only the **Drag** button is `draggable`. The row is a plain `<li>` and the copy's name is a `<Link>`, so dragging the row gives the browser's link drag, not the file. A tester following the script literally would report a failure. The line should say to drag the copy's **Drag** handle.

## Checked and fine

- **Heavy banner after "Not now":** on a heavy master with no copies, the panel hides and `HeavyToSendBanner` appears (`heavy && !showDestinations`). That matches the new doc comment ("every other page"), so I read it as intended.
- **Copy picture sizes:** `factsOf` uses this page's probe with `resolveExportTarget`. The copies all derive from this file, and the fixed-size presets come out the same whatever the framing.
- **Message keys and styles:** none of the removed keys (`where*`, `copiesEmpty`, `copyProgress*`) are used anywhere else. `sendTo` is kept and is still used by `video-card.tsx` and `video-row.tsx`. All the new keys exist in both `en.json` and `es.json`, and every CSS variable used is defined.
- **Title truncation:** the inner `<h1>` has `overflow: hidden`, so it can shrink inside the flex row and the ellipsis works as the comment says.
