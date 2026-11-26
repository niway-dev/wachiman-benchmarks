# kaipu-bench-wachi-v3#70 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T01:43:57Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

3 finding(s): 3 to consider; 3 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 replaces the \"Where is this going?\" strip with a full destinations panel, moves the title into its own top row, and redesigns \"Copies from this original\" with dimensions, a progress bar, Drag and \"Open in Export\". The new panels reuse the same Prepare navigation and the same probe and estimate math as the rest of Prepare. I found three things worth a look, none of them blocking:

- **Drag doesn't mark the copy as seen.** The new Drag handle skips the `markCopySeen` call that the ready card's Drag makes, so a copy dragged out from this page stays outlined as unseen in the Library.
- **Cards wait forever on an unreadable file.** The destinations panel only gets `probe`, so when the file can't be read every card except Archive shows \"…\" for good.
- **One test checks only half of what its name says.** The \"Open in Export\" test never checks that the button is hidden when there is no export screen.

The pull request description is wrong about one thing: it says there are seven destinations, with Email as its own card. `DESTINATION_IDS` lists six, with Email still inside the chat card (`destinations.ts:36-43`), and the description's own test steps name six cards.

**Batch 2 of 2.** I found nothing to flag in part 2.

**Files checked.** I read the full test file, the three stylesheets, the backlog doc and its index row, and both message files. I checked them against `library-detail-page.tsx`, `destinations-panel.tsx`, `master-copies-panel.tsx` and `destinations.ts`.

- **Messages.** Every new `library.*` key is used and appears in both `en.json` and `es.json`. Nothing still reads the removed keys (the `where*` set, `copiesEmpty`, `copyProgress*`). `sendTo` is still used by `video-row.tsx` and `video-card.tsx`.
- **Styles.** Each class the components use exists in its stylesheet.
- **Tests.** The tests' names match what they assert. The dropped "file isn't read" assertion matches the change: the page now reads the file for every local recording.

**One false claim in the PR body.** It says there are "Seven destinations, as in the design. Since the export-screen merge, Email is its own card." That is not what the code does: `DESTINATION_IDS` (`destinations.ts:36-43`) lists six destinations, with email folded into the chat card. The tests (`library-detail-page.test.tsx:253-260`) and the backlog doc (`prepare-screen.md:114`, "the code has six") both match the code, so only the PR description is wrong. Fix it there, or add the seventh card if it was meant to be included.

<details><summary>What the change connects to (8 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171-175`) — The file is dragged out under the copy's title. The Library's unseen-copy outline and "copy ready" chip stay put. If it fails: startFileDrag is fire-and-forget, the same as the siblings. A copy without a local id gets no handle. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-236`, `apps/kaipu-record/src/renderer/src/features/library/components/gif-viewer.tsx:25-28`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:8-13`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-58`.
- Destination card click opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`) — Navigates to Prepare with the destination preselected. If it fails: On a probe error the cards show '…' indefinitely, because the panel only receives the probe and not its status. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`.
- Probe now runs for every local recording (dimensions in the metadata line, estimates, copy dimensions) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The resolution shows in the metadata line once the file is read. Copy rows show the dimensions computed by resolveExportTarget. Canvas presets have a fixed size, so framing doesn't change them. If it fails: On error the probe is null: no resolution in the metadata, copy rows show only the file size, destination cards show '…'. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:47-66`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:478-504`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:104-114`.
- Switch from destinations panel to copies panel when a background export finishes (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189-191`) — One frame of the destinations panel, then the loading state, then the copies panel. If it fails: If the export fails, the runner sets status error, running becomes null and the destinations panel returns. That is the correct state. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-runner.ts:462-465`, `apps/kaipu-record/src/renderer/src/features/library/hooks/use-local-library.ts:41-44`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:146-148`.
- 'Saved to your Library' notice dismissal and 'Not now' on the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`) — On Back from Prepare the page remounts under the same history entry, which still carries fromRecording, so the notice and the post-recording card show again. This matches the existing card's behaviour. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-137`.
- Green "Saved to your Library" notice on a fresh recording, dismissed with ✕ (keyed to location.key) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:137`) — role=status notice above the player; ✕ hides it and brings back "This is your original. It never changes." (test at library-detail-page.test.tsx:868-881). If it fails: No async work. Prepare returns to the recording with navigate(recordingPath), a new entry with no fromRecording state, so the notice does not come back; only a history Back to the original arrival en… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:129-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341-346`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`, `apps/kaipu-record/src/renderer/src/pages/prepare/prepare-page.tsx:152-153`.
- Destination card in "Where is it going?" opens Prepare on that destination; "Not now" hides the panel (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — Navigation to Prepare with the destination preselected; the card sizes come from planCopy once the probe arrives ("…" before). If it fails: The probe never arriving leaves non-archive cards at "…" but clickable; the dismiss lives only in component state, so it resets on unmount. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-96`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-505`.
- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — The OS drags the copy's real file. If it fails: Fire-and-forget ipcRenderer.send; main validates the id in its handler, as for the existing callers. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 18 | $0.69 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 14 | $0.54 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 38 in / 18k out / 1.0M cache read / 135k cache write · $1.24</sub>

<!-- wachi:review -->

<!-- agent-review sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=e78bddd5-3410-4f63-8cfe-0582130d68ae -->
