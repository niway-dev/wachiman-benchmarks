=== REVIEW 5730236131 2026-11-01T20:58:30Z commit=dac8318
> ℹ️ No critical issues. One rough edge inline, plus a note on the description.

**Reviewed changes**

I reviewed the whole relayout of the recording detail page after Export v3: the new title row, the destinations panel, the copies grid with Drag, and the i18n and backlog doc updates.

- **Title row**: `← Library`, the renamable title and the master tag now share the top row. The title wrapper is `flex: 1; min-width: 0`, so the h1's existing ellipsis kicks in only at the tag.
- **Metadata and actions**: the meta line adds the probed resolution and an "N copies" count. The action row holds only buttons and wraps. "Export a copy" replaces "Send to…".
- **Probe on every local recording**: `useSourceProbe` no longer depends on `heavy || showCard`.
- **"Saved to your Library" notice**: it shows only for `fromRecording` and is dismissed per `location.key`. `masterNote` waits until it is gone.
- **`DestinationsPanel`** (new): one equal card per `DESTINATION_IDS` entry, with a `planCopy` estimate and an upload/light tone. It opens Prepare via `preparePath`. "Not now" hides it for this visit. It replaces `WhereIsThisGoingStrip`, which is deleted.
- **`MasterCopiesPanel`**: copies are two to a row. A copy's picture size is derived from the source probe and its preset. The running row gets a progress bar, and the header gets "Open in Export →". A Drag handle reuses `startFileDrag`, the same way `export-status-cards.tsx` does. The empty state is gone because the caller only renders the panel when there is something to list.
- **Heavy banner**: it now shows whenever the destinations panel doesn't, including a heavy master that has copies.

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

### ℹ️ The description says seven destinations, but the code and the doc say six

Under "Notes for review", the PR description says "Seven destinations, as in the design. Since the export-screen merge, Email is its own card". But `DESTINATION_IDS` in `features/prepare/destinations.ts` has six entries (`youtube`, `vertical`, `square`, `github`, `chat`, `archive`). The tests only exercise those six, with Email folded into "Slack · Discord · Email", and the updated `prepare-screen.md` says "the code has six". QA following the description will look for a seventh card that isn't there.

<details><summary>Technical details</summary>

````markdown
# PR description disagrees with `DESTINATION_IDS`

## Affected sites
- PR description, "Notes for review": the first bullet claims seven destinations, with Email as its own card
- apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36: `DESTINATION_IDS` has six ids
- apps/documentation/src/content/docs/backlog/prepare-screen.md:114: says "the code has six" (consistent with the code)

## Required outcome
- The description and the backlog doc agree with what `DESTINATION_IDS` actually lists
````

</details>

<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [Fix all ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog/3?action=fix&review_id=5730236131) ｜ [Fix 👍s ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog/3?action=fix-approved&review_id=5730236131) ｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog/actions/runs/41349377800/job/124976040942) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

