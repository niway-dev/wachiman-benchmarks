# kaipu-bench-wachi-v3#94 [replay] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T17:30:29Z · commit dac8318

👮 **Wachiman** · 🟡 **Nothing to fix · 4 to consider** · whole PR at `dac8318`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 4 to consider · ⚪ 0 for your information (4) · 1 Should · 3 Could |
| **Risk** | Low: no risk facts reported, no risky paths |
| **Coverage** | 14 of 14 files reviewed, whole pull request |
| **Read first** | `library-detail-page.tsx`, `master-copies-panel.tsx`, `destinations-panel.tsx`, `where-is-this-going-strip.tsx`, `library-detail-page.test.tsx` |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🐛 bug | [`master-copies-panel.tsx:174`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx#L174) | Drag from the copies panel doesn't mark the copy as seen |
| 🟡 Consider · Could · 🐛 bug | [`destinations-panel.tsx:91`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx#L91) | Size shows "…" forever when the file can't be read |
| 🟡 Consider · Should · 🧪 tests | [`master-copies-panel.test.tsx:140`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L140) | "shows only where there is an export screen" test never checks the absent case |
| 🟡 Consider · Could · 🧪 tests | [`master-copies-panel.test.tsx:100`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/dac8318b631e64780f65ce94b4aaa57261d7d63d/apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx#L100) | Test overwrites the global \`window.electronAPI.startFileDrag\` and never restores it |

<details><summary>What the change connects to (3 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Drag handle on a ready copy row hands the real file to main for a native drag (`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:164`) — The OS drag starts through main. The renderer never names a path. The copy stays flagged unseen in ready-copies, so the Library chip and outline remain after the drag. If it fails: If main fails (missing poster, vault error) it only logs `file drag failed` and nothing is shown to the user. The same silent failure applies to the existing call sites, so it is not new. The handle… Evidence: `apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:231-236`, `apps/kaipu-record/src/main/library/index.ts:161-175`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:8-10`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/ready-copies.ts:55-58`, `apps/kaipu-record/src/renderer/src/shell/sidebar.tsx:95`.
- The page now probes every preparable recording's file on open (was only when heavy or when the card showed) (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142`) — The dimensions appear in the metadata line, the destination cards show sizes, and copy rows show picture sizes. While loading or after an error, the dimensions are omitted and the cards show "…". If it fails: A failed probe is silent: the cards show "…" forever and no dimensions appear (reported as a finding). The extra read is cheap, so it is not a perf finding. Evidence: `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:42-67`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:21-47`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:282-289`, `apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:41-56`.
- "Where is it going?" panel: a card opens Prepare on a destination, "Not now" hides it (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489`) — Once the first copy is running or exists, the panel is replaced by the copies list. After "Not now", the 'Export a copy' button and the heavy banner appear. The dismissal is kept in component state keyed by assetId and is lost when the page is left. If it fails: A master that is not preparable (no local id) with no copies now shows neither panel, where it used to show 'No copies yet'. The remaining actions still render, so this is acceptable. Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:187-191`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:436-441`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:489-523`, `apps/kaipu-record/src/renderer/src/features/prepare/components/where-is-this-going-strip.tsx:1-63`. ⚠️ A citation did not resolve in the head.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** The page restructure and the new DestinationsPanel and MasterCopiesPanel code are mostly consistent: the panel and banner conditions are mutually exclusive, and the picture-size math reuses `resolveExportTarget`. I found no blocker or bug that loses data. Four small issues, all "consider". The drag handle skips the `markCopySeen` call its sibling ready card makes. The destination cards show \"…\" forever if the file probe fails. One test named \"shows only where…\" never checks the absent case. One test leaves the global `window.electronAPI.startFileDrag` overwritten.

**Batch 2 of 2.** I found nothing to flag in these nine files (tests, stylesheets, docs and messages). I checked them against the page, the two panel components and `destinations.ts`, and only read the code; none of it was run.

- **Tests:** the new assertions match the page code. The six destination cards match `DESTINATION_IDS`. "Not now" and the "Saved" notice are driven by `location.key`/`assetId` as the tests expect. Dropping the "file isn't read" assertion matches the page now probing every local recording.
- **Stylesheets:** every class the components use is defined, and every CSS variable used is defined in the tokens CSS. Nothing still references the deleted `where-is-this-going-strip` module or the removed `.bar`, `.titleBlock` and `.masterRow` classes.
- **Messages:** the old strip keys are gone and the new keys are in both locales. `sendTo` is still used by the Library card and row, and `sendToHint` by the page.
- **Docs:** `prepare-screen.md` says the code has six destinations against the design's seven, which matches `DESTINATION_IDS`. The backlog row in `backlog/index.mdx` was updated along with it. The only remaining "Send to…" mentions describe the Library card and row, which still use it.

I did not check the drag handle or the exporting row in the page test. They belong to the other part's files, and I did not review that part's panel test.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 5 | 852 | 4 | reviewed | 16 | $0.39 |
| Batch 2 of 2 | 9 | 763 | 2 | reviewed | 19 | $0.36 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 30 in / 16k out / 754k cache read / 129k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.75</sub>

<!-- wachi:review -->

<!-- wachiman sha=dac8318b631e64780f65ce94b4aaa57261d7d63d -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjEuMCIsImhlYWQiOiJkYWM4MzE4YjYzMWU2NDc4MGY2NWNlOTRiNGFhYTU3MjYxZDdkNjNkIiwiYXR0ZW1wdCI6ImY1NjM0ODEzLTg3NWYtNDNkMi05NWYwLTgzODcwZGZiYjBlOSIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=f5634813-875f-43d2-95f0-83870dfbb0e9 -->
