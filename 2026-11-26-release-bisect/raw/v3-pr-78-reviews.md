# kaipu-bench-wachi-v3#78 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T06:00:51Z · commit dac8318

👮 **Wachiman** · review of the whole pull request, at `dac8318`: all 14 files reviewed.

2 finding(s): 2 to consider; 2 on their lines. Reply in a comment's thread to answer it.

**Risk map:** low — no risk facts in this change.
**Read first:** `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx`, `apps/kaipu-record/src/renderer/src/features/prepare/components/where-is-this-going-strip.tsx`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx`.

### Summary

**Batch 1 of 2.** I found two minor issues in part 1, both at "consider". I found nothing that blocks the merge.

1. **Failed file read looks like loading.** The page now reads the file for every local recording but drops the read's status. If the read fails, every destination card except Archive shows "…" for as long as the page is open, which looks the same as still loading (`library-detail-page.tsx:142`).
2. **Test checks only half its name.** The "Open in Export →" test promises the button appears "only where there is an export screen to open", but it never checks that the button is absent without one (`master-copies-panel.test.tsx:140`).

The rest checks out:
- **Drag handle:** it matches the existing drag in the export status cards: same `startFileDrag(id, title)` call, plus a guard for copies with no local file.
- **Destination cards:** they reuse the page's existing way of opening Prepare on a destination.
- **"Saved" notice and "Not now":** both are held only in page state, like the existing post-recording card. Coming Back from Prepare shows the notice again and resets "Not now"; that matches the PR's "until you leave the page".

I could not cover the copies' picture sizes fully. They are computed from the original's file without the framing chosen at export. I read only part of the sizing code: it says framing applies only to fixed-size presets, but I did not confirm it never changes the output size. If it can, a copy row could show the wrong "2560 × 1440".

**Batch 2 of 2.** I found no problems in part 2. The tests, stylesheets, backlog docs and both message files all match the head implementation:

- **Stylesheets.** Every class the page and panels reference exists in its stylesheet, and the new tokens (`--accent-green`, `--bg-input`, `--font-mono`) are defined in `packages/tokens/css/tokens.css`.
- **Removed keys.** The `library.*` keys the PR removes have no remaining renderer users. `sendTo` stays, because the Library card and row still use it.
- **Tests.** They assert the new labels, the six `?to=` destinations, the size tones (`groupOf` sorts the archive card into the teal "light" tone) and the panel/copies switch.
- **Docs.** `backlog/prepare-screen.md` correctly says the code has six destinations from `DESTINATION_IDS`. The PR body is wrong on this point: it says seven, with Email as its own card, but `destinations.ts` lists six. Only the PR description is wrong; no file in this part is.

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- Drag handle on a ready copy starts a native file drag via startFileDrag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — The OS drag carries the real file, named after the copy's title. If it fails: startFileDrag is fire-and-forget (void). A failure in main is not visible here, as with the existing siblings. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:235`, `apps/kaipu-record/src/shared/types/electron-api.ts:259`, `apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164-180`.
- Destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:493`) — Navigates to Prepare with the destination preselected. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:384-387`.
- Probe the source file for every local recording (was: only heavy or with the post-recording card) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Resolution in the metadata line, card estimates, and copy picture sizes appear once the probe resolves. If it fails: On error the status is dropped, so the cards show "…" indefinitely and the resolution and copy dims are silently omitted. A rejection of probeSource is unhandled inside the hook (`void ...then`), whi… Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91`.
- Saved notice and "Not now" dismissals held in component state (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-139`) — On remount (Back from Prepare), the history entry still carries `fromRecording`, so the notice shows again, just as the card does. "Not now" resets too, which matches the PR's "until you leave the page". Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-137`.
- A destination card in "Where is it going?" opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — Navigation to /prepare/:assetId?to=<id>, which the tests assert for all six ids. If it fails: The click only navigates; there is no async call that can fail. The size estimates show "…" until the probe resolves. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-93`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-494`, `apps/kaipu-record/src/renderer/src/features/prepare/destinations.ts:36-43`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- The "Saved to your Library" notice is dismissed with ✕, and "Not now" hides the destinations panel (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:137`) — The notice and the panel reappear after the user returns to the page; nothing is stored. The PR body says as much. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 8 | $0.56 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 11 | $0.56 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 26 in / 10k out / 548k cache read / 100k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.12</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:attempt id=513c6718-be33-4611-8948-2080f1aeea87 -->
