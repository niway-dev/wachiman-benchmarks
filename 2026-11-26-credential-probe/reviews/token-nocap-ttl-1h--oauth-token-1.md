<!-- token-nocap-ttl-1h, oauth-token-1: 39 turns, $1.52 -->

I found one real bug. Two smaller points are below it, as judgement calls rather than defects. I didn't run the tests or change any file.

### Bug

**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142` together with `features/prepare/components/destinations-panel.tsx:263` and `:311`: if the file can't be read, every card except Archive shows "…" forever.**

- **What happens:** the page keeps only `useSourceProbe(...).probe` and throws away `status`. `useSourceProbe` (`use-prepare-copy.ts:51-58`) returns `{ status: "error", probe: null }` whenever `probeSource` fails or the result isn't usable. That includes a zero width, height or duration, which an imported `.webm`/`.mov` without duration metadata can produce.
- **Why it's wrong:** `DestinationsPanel.estimate()` returns `null` whenever `probe` is null, and the card renders `size ?? "…"`. "Still loading" and "failed" therefore look the same, so YouTube, Reels, LinkedIn, GitHub and Chat show a loading ellipsis that never resolves. The panel's own doc comment says the cards "show no estimate until it is [read]", which assumes the read always finishes.
- **Why it's new:** before this PR the page read the file only for heavy recordings or the post-recording card, and nothing on the page showed a pending placeholder for it. Now every local recording is read, and the "Where is it going?" panel is the first view of every recording that has no copies yet.
- **Fix:** pass the probe `status` (or a `failed` flag) into the panel, and show nothing (or the plain destination line) instead of "…" on `"error"`. The heavy-note text already handles this case through `heavyBannerBodyNoEstimate`.

### Lower-severity behaviour worth a look

- **`library-detail-page.tsx:517`, banner after "Not now":** the condition changed from `heavy && !master` to `heavy && !showDestinations`. On a heavy master with no copies, pressing "Not now" removes the panel and immediately shows the full banner with "Prepare a light copy →". So turning down one prompt makes a new one appear. The backlog doc describes the banner for "a heavy master with copies", not for a dismissed panel. Keep it only if that's what the design intends.
- **Docs, `prepare-screen.md` manual test ("Drag the copy's row out of the page into Finder"):** only the separate **Drag** button starts the native file drag. The rest of the row is a `<Link>`, and dragging it drags the `/library/<id>` URL, not the file. The test step should say "Drag button", or the whole row should be made the drag source.

### Checked and fine

- The new card size estimates agree with the Prepare screen: no framing falls back to `defaultFraming`, and the YouTube default is the same.
- `resolveExportTarget` gives correct copy picture sizes.
- `startFileDrag` is called with the right id and name and only when there is a local file.
- The `?to=` paths are valid for all six destinations, including archive.
- No orphaned i18n keys are left by deleting the strip, and `sendTo` is still used by the Library card and row.
- Title truncation works: the `<h1>` has `overflow: hidden`, so it can shrink and ellipsize inside the flex row.
