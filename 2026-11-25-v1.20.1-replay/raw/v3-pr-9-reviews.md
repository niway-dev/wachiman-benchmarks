# kaipu-bench-wachi-v3#9 [replay r2] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:53:39Z · commit dac8318

👮 **Wachiman** · 🟡 **Nothing to fix · 3 to consider** · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 3 to consider · ⚪ 0 for your information (3) · 3 Should |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (3)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`destinations-panel.tsx:91`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx#L91) | If the file can't be read, the destination cards show "…" forever |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | The test replaces the shared \`startFileDrag\` stub and never puts it back |
| 🟡 Consider · Should · 🧹 cleanup | [`en.json:791`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/packages/i18n/messages/en.json#L791) | "Send to…" survives only on the Library cards, so the same action now has two names |

<details><summary>What the change connects to (7 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Drag handle on a ready copy starts a native file drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:171`) — Main starts a native drag of the copy's file, named after its title. If it fails: startFileDrag is a fire-and-forget ipc send (preload/index.ts:87). If main refuses, nothing happens and the user sees no error, same as the sibling. The handle is hidden when there is no local id. Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-236`, `apps/kaipu-record/src/preload/index.ts:87`, `apps/kaipu-record/src/main/library/index.ts:161`.
- Probe the source file for every local recording instead of only heavy ones or the card (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — Shows the resolution in the metadata line, the destination estimates and each copy's picture size. If it fails: A failed probe gives probe null with status error. The page drops the status, so the destination cards show "…" indefinitely (reported as a finding). Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`.
- Copy row picture size from resolveExportTarget(preset, probe) without framing (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:109`) — "2560 × 1440 · 22 MB" on the copy row. If it fails: When there is no probe, the row shows only the file size. Evidence: `apps/kaipu-record/src/renderer/src/features/video-editor/export/export-presets.ts:478-503`.
- "Saved to your Library" notice shown on fromRecording, dismissed per location.key (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:137`) — A green notice above the player that replaces the masterNote line. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:128-137`.
- "Not now" on the Where is it going? panel hides it and brings back Export a copy (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`) — The panel unmounts and the primary Export a copy button renders, because showDestinations becomes false (library-detail-page.tsx:436,489). If it fails: No async work. Going Back or leaving the page remounts the component, so the panel comes back. Navigating to another asset inside the same mounted page compares the stored id to the new assetId, so t… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:494`, `apps/documentation/src/content/docs/backlog/prepare-screen.md:101-102`.
- A destination card opens Prepare on that destination (`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:82`) — Navigates to /prepare/:assetId?to=<id> (library-detail-page.tsx:149-151). If it fails: Synchronous navigation. Size estimates show "…" until the probe resolves (destinations-panel.tsx:43,91). If the probe never resolves, the estimates stay "…" but the cards still work. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:73-93`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:149-151`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.test.tsx:253-266`.
- The Saved to your Library notice on a fresh recording, dismissable with ✕ (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394`) — A green status box above the player. The test pins its text and the note's return after ✕ (test:868-881). If it fails: Router Back to the same history entry restores location.state.fromRecording with the same key. The component state resets on remount, so the notice shows again on Back. This matches how the ready car… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:101`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:136-137`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:341`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:394-412`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** This part of the redesign holds up: I found no blockers and two small issues worth fixing. The new destinations panel, the reworked copies panel and the rearranged detail page match the pull request's description. Drag uses the existing `startFileDrag` IPC with the same `preventDefault` guard as its sibling, and a copy's picture size is worked out correctly, since the size of a fixed-canvas preset doesn't depend on framing. The two issues: if the file can't be read, the destination cards show a permanent "…" because the probe's error status is dropped; and a test replaces the shared `startFileDrag` stub without restoring it.

**Batch 2 of 2.** I found nothing that should block the merge; the only finding is a minor naming inconsistency.

**What I checked:**

- **Tests:** they match the new page in `library-detail-page.tsx`. That covers the title row, the "Where is it going?" panel and its six cards, "Not now", the "Saved to your Library" notice, the copies count, and the heavy hint now living inside the panel.
- **Stylesheet:** `where-is-this-going-strip.module.css` is deleted, and nothing in the app still references it.
- **Messages:** the keys this change removes (`where*`, `copyProgress*`, `copiesEmpty`) are no longer used in the app. `en.json` and `es.json` stay in step.
- **Docs:** `prepare-screen.md` describes the code accurately. That includes reading the file on every local recording, which is why the "up to 25 MB" test no longer asserts that the file is left unread.

**Finding (consider):** the same action now has two names. The recording page says "Export a copy", while the Library's card and row buttons (`video-row.tsx` and `video-card.tsx`) still say "Send to…".

I recorded three closed contract entries: "Not now", the destination cards, and the saved notice.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 11 | $0.51 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 5 | $0.45 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 20 in / 10k out / 354k cache read / 87k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.97</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6IjEyNjQ2YThhLTE1YTUtNDEwNy1hMjYzLTFjOTcyYTMwNjhlNiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6MywiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6MywiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjMsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=12646a8a-15a5-4107-a263-1c972a3068e6 -->
