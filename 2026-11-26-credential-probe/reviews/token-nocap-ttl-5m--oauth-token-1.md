<!-- token-nocap-ttl-5m, oauth-token-1: 26 turns, $0.77 -->

I found two real bugs, both small. Neither breaks the main flows (cards opening Prepare, the copies grid, Drag, the title row). I didn't run the tests.

### 1. The size on each "Where is it going?" card stays at "…" forever when the file can't be read
`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263` and `:311`, fed by `library-detail-page.tsx:142`

- **What goes wrong:** if the recording's file can't be read, the five non-archive cards show "…" for good, as if still loading.
- **Why:** `useSourceProbe` (`use-prepare-copy.ts:42-67`) has distinct `loading` and `error` states. In both, `probe` is `null`, and it is also `null` when the file reads but has no width, height or duration (`isUsableProbe`). The page keeps only `.probe`, so the panel can't tell "still reading" from "failed". `estimate()` returns `null` and the card renders `size ?? "…"`.
- **Contradiction:** the panel's own doc comment says "the cards show no estimate until it is [read]", but on failure it never is read.
- **Who it affects:** before this PR the page only read the file when it was heavy or the post-recording card was showing. Now every local recording's page reads it, so any file that can't be read hits this.
- **Fix:** pass the probe's `status` down and render nothing (or a neutral label) on `"error"`.

### 2. "Not now" on a heavy master with no copies makes the heavy-to-send banner appear
`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:517` (`heavy && !showDestinations`)

- **What goes wrong:** the banner's condition changed from `heavy && !master` to `heavy && !showDestinations`. `showDestinations` becomes `false` as soon as the user clicks "Not now".
- **Result:** on a master over 25 MB with no copies, dismissing the panel immediately adds a "119 MB is heavy to send … Prepare a light copy →" banner at the bottom. The user just declined to make a copy, and the page nags with another prompt to make one.
- **Contradiction:** the PR's own docs (`prepare-screen.md`) say the banner stays only for "a heavy copy, or a heavy master with copies".
- **Fix:** gate it on `heavy && (!master || hasCopies)`. That keeps the hint inside the panel while it shows, and drops it once the panel is dismissed.

### Checked and fine
- **Drag:** `startFileDrag(copy.id, copy.title)` matches the preload/main signature and the ready card's pattern (`export-status-cards.tsx:231-235`).
- **Picture sizes:** `resolveExportTarget(preset, probe, …)` in `factsOf` gives the right size for fixed-canvas presets and for the quality tiers.
- **Destination links:** every `?to=` value the cards produce, including `archive`, is a valid `DestinationId`.
- **Card estimates:** they match the Prepare page's `planCopy` call (same preset choice and duration), so the two screens agree.
- **Removed translation keys:** none of the `where*`, `copiesEmpty` or `copyProgress*` keys is used anywhere else. `sendTo` is kept, and the Library card and row still use it.
- **`MasterTag size="sm"`:** it exists. In the title row, the title's ellipsis still works because its wrapper has `min-width: 0`.
