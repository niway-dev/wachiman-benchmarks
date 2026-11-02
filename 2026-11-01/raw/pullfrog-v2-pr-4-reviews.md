## review by pullfrog[bot] at 2026-11-01T23:34:27Z

> ℹ️ No critical issues — one rough edge inline.

**Reviewed changes**

Reviewed the full diff of the recording detail page relayout (one commit, 14 files).

- **Title row** — `← Library`, `RecordingTitle` and the small `MasterTag` now share the top row. The h1's `overflow: hidden` lets it shrink and ellipsize inside the `flex: 1; min-width: 0` wrapper.
- **Details block** — the metadata line gains the probed resolution and an `N copies` count. The master note hides while the new "Saved to your Library" notice is showing.
- **`DestinationsPanel`** — replaces `WhereIsThisGoingStrip`. It shows one card per `DESTINATION_IDS` entry with a `planCopy` size estimate, and its "Not now" brings back the "Export a copy" action.
- **`MasterCopiesPanel`** — rewritten as a two-column grid with an "Open in Export →" header, a `W × H · size` facts line, a progress bar and a Drag button. The Drag button uses the same `startFileDrag` pattern as `export-status-cards.tsx`. The empty state is gone; the page renders the panel only when `hasCopies`.
- **Probe and banner** — `useSourceProbe` now runs for every local recording. `HeavyToSendBanner` shows whenever the destinations panel doesn't.
- **i18n / docs** — removed the `where*`, `copiesEmpty` and `copyProgress*` keys (no remaining references), added the new keys in `en` and `es`, and updated the backlog docs.

The PR description says "Seven destinations", but `DESTINATION_IDS` and the backlog doc both list six. The code and docs agree with each other, so only the description needs fixing.

<!--
Pullfrog review metadata. These findings were written against dac8318;
if commits have landed on replay/pr-465/head since, treat every specific bug, file, or
line callout as POTENTIALLY STALE and re-diff before acting on it.

- Mode: Review (initial)
- Files reviewed: 14
- Commits reviewed: 1
- Base: replay/pr-465/base (13b7ff5)
- Head: replay/pr-465/head (dac8318)
- Reviewed commits:
  - dac8318 — feat(desktop): recording detail — title on top, destinations, copies from this original
- Prior pullfrog review: none
-->


<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [Fix all ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog-v2/4?action=fix&review_id=5730800567) ｜ [Fix 👍s ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog-v2/4?action=fix-approved&review_id=5730800567) ｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog-v2/actions/runs/41362558494/job/125015843765) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

