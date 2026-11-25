# kaipu-bench-wachi-v3#10 [replay r2] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-25T21:54:09Z · commit b2705a9

👮 **Wachiman** · 🟣 **1 question for you** · 4 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 4 to consider · ⚪ 0 for your information (4) · 2 Should · 2 Could |
| **Risk** | High: top fact `public-contract` at `ipc.ts:532`, see Risk facts |
| **Needs a person** | 1 trade-off, in `recording-ready-window.ts:146` |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `ipc.ts`, `index.ts`, `recording-ready.ts`, `electron-api.ts`, `recording-ready-window.ts` |

### To consider (4)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Should · 🐛 bug | [`recording-ready-window.ts:146`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L146) | \`show()\` answers true before the card window has loaded, so a renderer that never loads loses the card with no fallback |
| 🟡 Consider · Could · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` accepts an invoke from any renderer |
| 🟡 Consider · Should · 📝 docs | [`post-recording-card.tsx:48`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx#L48) | Docstring still says the card goes away when the user leaves the page |
| 🟡 Consider · Could · 🐛 bug | [`library-detail-page.tsx:141`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx#L141) | Floating card outlives the page and the recording it points to |

### Questions for you (1)

- [`recording-ready-window.ts:146`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L146) · trade-off — Answering true before the card has loaded keeps the main window's in-app card from ever showing twice. The cost is that a failed load loses the prompt for that take. Someone needs to decide whether to wait for `card-ready`, with a timeout, before answering.

### Risk facts

- `public-contract` · [`ipc.ts:532`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/shared/types/ipc.ts#L532) — Adds six new IPC channels between the main window, main and the new card window, and exposes them on `window.electronAPI` in every renderer.
- `index.ts` — a process boundary
- `electron-api.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (6 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**

- Main window asks main to float the card (`showRecordingReady` → `recording-ready:show`) (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — After `card-ready`, `present()` sets bounds, sends the payload and calls `showInactive`. The card shows at the top-right of the recorded display. If it fails: If creation throws, it answers false and the page shows the in-app card. If the renderer load fails or ready never comes, it answers true and nothing is shown: the card is silently lost for that take… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:218-226`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:258-269`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:148-160`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:21-31`.
- An action on the floating card hands off to the main window (`openInMain`) (`apps/kaipu-record/src/main/index.ts:899`) — The main window comes forward, and `useRecordingReadyHandOffs` navigates to Prepare, the editor or the detail page. If it fails: If the main window was destroyed, `createWindow` runs and the send is queued in `pendingRendererSends`, so the hand-off is not lost. Evidence: `apps/kaipu-record/src/main/index.ts:145-150`, `apps/kaipu-record/src/main/index.ts:449-457`, `apps/kaipu-record/src/main/index.ts:683-695`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28-34`.
- Hub remembers the display of the latest take (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — The ready window opens on that display's work area, or under the cursor when it is null or unknown. If it fails: A window source, or a stop before the lookup resolves, leaves it null or at the region's display. The card then falls back to the cursor display, which is still visible. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:646`, `apps/kaipu-record/src/main/recording/recording-hub.ts:666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:710-713`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- Recording page asks main to float the ready card once per arrival, after the probe settles (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — The card shows in its own desktop window (main.tsx:66-71 renders RecordingReadyCard). The in-app card shows only as the fallback. If it fails: If the IPC rejects or main returns false, the hook sets fallbackFor and the in-app card shows. If the window is created but its renderer never loads, nothing shows and there is no fallback (the doc s… Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-32`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:33-66`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`, `apps/documentation/src/content/docs/backlog/floating-ready-window.md:55-56`.
- New render target ?window=recording-ready (`apps/kaipu-record/src/renderer/src/main.tsx:66`) — Only the card paints. main.css gives 16 px padding, which matches READY_WINDOW_PADDING, and main adds 2*padding to the reported height. If it fails: A load failure shows nothing (documented). Evidence: `apps/kaipu-record/src/renderer/src/main.tsx:60-71`, `apps/kaipu-record/src/renderer/src/assets/main.css:85-93`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:18-19`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:71-73`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:258-268`.
- Main-window listener that routes floating-card hand-offs (`apps/kaipu-record/src/renderer/src/shell/app-root.tsx:31`) — The main window moves to Prepare, the editor or the detail page. If it fails: If a hand-off arrives before the listener mounts, it is dropped (main side, not verified here). Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28-34`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:166-172`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I read all 15 files in part 1 and found nothing that blocks the merge. The floating-window manager follows the capture toast's pattern closely. That covers its non-activating panel, `showInactive`, content protection, joining every Space only while shown, ignoring messages from other windows, recreating a closed window, and refusing to show after quit. The IPC contract has no value imports, as the CLAUDE.md preload rule requires. All three findings are at "consider":

- **Lost card on load failure:** `show()` answers true as soon as the window exists. If the card window then fails to load, the card is lost with no in-app fallback and nothing logged. The PR body acknowledges this.
- **Unchecked sender:** `recording-ready:show` does not check which window sent it, so any renderer can float a card.
- **Stale docstring:** `PostRecordingCard`'s docstring still says the card goes away when the user leaves the page, which the floating window does not do.

The hand-off into the main window queues correctly when that window has to be recreated. The display remembered for the take is reset on every start.

**Batch 2 of 2.** I found one issue in part 2, at "consider" severity and medium confidence. Once main confirms the floating "Your video is ready" card, the recording page no longer controls it. The card stays up after the user leaves the page, and after they delete the recording from that page. If they then press a chip, Edit first or Open, the main window goes to an asset that no longer exists.

Everything else I checked matches the code:

- The request is sent once per arrival, after the file has been read. The in-app card comes back when the window can't open or the IPC call fails.
- The 16 px padding in main.css matches what the main process uses to size the window.
- The new render target is set up the same way as the capture toast.
- The hand-off paths go where the tests expect.
- The en/es strings were added to both files.
- The backlog doc's claims match the code: window flags, content protection, when it answers false, and `lastTakeDisplayId`. Its sidebar entry and backlog row are in place.

The tests assert what their names say.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 5 | $0.55 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 12 | $0.49 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 16 in / 14k out / 245k cache read / 89k cache write · Claude subscription: API-equivalent estimate, not a bill · $1.04</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjAuMSIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6IjZkYzBlOTUxLTY2MGQtNDg2MC1iNzhjLWI0ZWFhNjA3NzE0MiIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NCwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NCwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjQsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=6dc0e951-660d-4860-b78c-b4eaa6077142 -->
