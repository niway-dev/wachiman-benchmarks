# kaipu-bench-wachi-v3#115 [replay r2] feat(desktop): float "Your video is ready" outside the app window - bot reviews

## github-actions[bot] · COMMENTED · 2026-11-26T20:07:48Z · commit b2705a9

👮 **Wachiman** · 🟣 **3 questions for you** · 6 to consider · whole PR at `b2705a9`

| At a glance | |
| --- | --- |
| **Findings** | 🔴 0 blockers · 🟠 0 to fix · 🟡 6 to consider · ⚪ 0 for your information (6) · 6 Could |
| **Risk** | High: risky path `preload/index.ts`, see Risk facts |
| **Needs a person** | 1 trade-off, in `recording-ready-window.ts:219` |
| **Coverage** | 28 of 28 files reviewed, whole pull request |
| **Read first** | `preload/index.ts`, `recording-ready.ts`, `electron-api.ts`, `ipc.ts`, `recording-ready-window.ts` |

### To consider (6)

| | Where | Finding |
| --- | --- | --- |
| 🟡 Consider · Could · 🔐 security | [`recording-ready-window.ts:104`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L104) | \`recording-ready:show\` handler does not check who is asking |
| 🟡 Consider · Could · ❓ question | [`main/index.ts:899`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/index.ts#L899) | Hand-off brings the main window forward without \`app.focus({ steal: true })\` |
| 🟡 Consider · Could · 🐛 bug | [`recording-ready-window.ts:219`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L219) | Re-showing a hidden card can flash the previous recording's card |
| 🟡 Consider · Could · 🐛 bug | [`recording-ready-card.module.css:1`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.module.css#L1) | 16 px window padding is smaller than the card's shadow, so the shadow will be cut at the window edge |
| 🟡 Consider · Could · 🐛 bug | [`use-floating-ready-card.ts:18`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts#L18) | "Once per arrival" does not survive a remount, so Back re-floats the card |
| 🟡 Consider · Could · 📝 docs | [`floating-ready-window.md:30`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/documentation/src/content/docs/backlog/floating-ready-window.md#L30) | "Every action closes the window, then shows and focuses the main window" is not true of ✕ and Escape |

### Questions for you (3)

- [`recording-ready-window.ts:219`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L219) · trade-off — If the card window is created but its renderer never loads, `show` has already answered true, so there is no in-app fallback and the user gets nothing. The doc lists this as accepted. A person has to decide whether that is acceptable or whether to add a load-failure fallback.
- [`apps/kaipu-record/src/main/recording/recording-ready-window.ts:166`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/main/recording/recording-ready-window.ts#L166) · open question — A card press (pick/edit/open/dismiss) becomes a hand-off to the main window: Does the main window come to the front of another app after a press, given the panel never activates the app? Files that would answer it: `apps/kaipu-record/src/main/index.ts`.
- [`apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28`](https://github.com/niway-dev/kaipu-bench-wachi-v3/blob/b2705a9ce2593b29ae50235312a4226955bbbb36/apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts#L28) · open question — The floating card's actions (pick, edit, open, dismiss) reach main, and main hands off to the main window, which navigates through pathForHandOff: Does main validate the card's action payload and check the sender before it emits a hand-off, and does it send the hand-off only after the main window's AppRoot has mounted? Files that would answer it: `apps/kaipu-record/src/main/recording/recording-ready-window.ts`, `apps/kaipu-record/src/shared/types/recording-ready.ts`, `apps/kaipu-record/src/preload/index.ts`.

### Risk facts

- `preload/index.ts` — a process boundary
- `electron-api.ts` — a contract more than one side imports
- `ipc.ts` — a contract more than one side imports
- `recording-ready.ts` — a contract more than one side imports

<details><summary>What the change connects to (5 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**

- A card press (pick/edit/open/dismiss) becomes a hand-off to the main window (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:166`) — Does the main window come to the front of another app after a press, given the panel never activates the app? Files that would answer it: `apps/kaipu-record/src/main/index.ts`.
- The floating card's actions (pick, edit, open, dismiss) reach main, and main hands off to the main window, which navigates through pathForHandOff (`apps/kaipu-record/src/renderer/src/features/recording-ready/use-recording-ready-hand-offs.ts:28`) — Does main validate the card's action payload and check the sender before it emits a hand-off, and does it send the hand-off only after the main window's AppRoot has mounted? Files that would answer it: `apps/kaipu-record/src/main/recording/recording-ready-window.ts`, `apps/kaipu-record/src/shared/types/recording-ready.ts`, `apps/kaipu-record/src/preload/index.ts`.

**Closed, with the lines they rest on**

- Page asks main to float the 'Your video is ready' card (`recording-ready:show`, invoke) (`apps/kaipu-record/src/main/recording/recording-ready-window.ts:104`) — The card floats at the top-right of the recorded display (or the cursor display when that is unknown) and stays until ✕, Escape or an action. If it fails: Creation failure is caught and returns false, so the in-app fallback appears. A window that is created but fails to load its renderer never sends `card-ready`: `show` returns true, nothing is shown a… Evidence: `apps/kaipu-record/src/main/recording/recording-ready-window.ts:104-107`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:134-147`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:219-226`, `apps/kaipu-record/src/main/screenshots/capture-toast-window.ts:304-308`, `apps/documentation/src/content/docs/backlog/floating-ready-window.md:53-57`.
- Hub records the display of the latest take (`lastTakeDisplayId`) (`apps/kaipu-record/src/main/recording/recording-hub.ts:666`) — The floating card opens on the display that was recorded; if that is unknown it opens on the display under the pointer. If it fails: A take stopped before the source lookup resolves keeps null or the region id, so the card falls back to the cursor display. That is a harmless degradation. Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:643-666`, `apps/kaipu-record/src/main/recording/recording-hub.ts:707-714`, `apps/kaipu-record/src/main/recording/recording-ready-window.ts:237-244`.
- Main window renderer subscribes to `recording-ready:open` through the preload (`apps/kaipu-record/src/preload/index.ts:256`) — The renderer navigates when main sends a hand-off. If it fails: No new failure path beyond the existing preload listeners. The shared types import only types, so the preload bundle has no new value import. Evidence: `apps/kaipu-record/src/preload/index.ts:256-261`, `apps/kaipu-record/src/preload/index.ts:262-264`, `apps/kaipu-record/src/shared/types/recording-ready.ts:1-5`.
- The recording page asks main to float the card (showRecordingReady) once the source probe settles, and falls back to the in-app card if main answers false or t… (`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:141`) — The card is a separate always-on-top window, with the same numbers because the probe has already settled. On a false answer or a rejected IPC, the in-app card shows instead. If it fails: A rejection or a false answer triggers the in-app fallback (use-floating-ready-card.ts:25-28). A window created whose renderer never loads is silent, as the doc admits. On remount via Back, the ref r… Evidence: `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:130-155`, `apps/kaipu-record/src/renderer/src/features/recording-ready/use-floating-ready-card.ts:16-32`, `apps/kaipu-record/src/renderer/src/features/prepare/use-prepare-copy.ts:47-66`, `apps/kaipu-record/src/renderer/src/features/video-editor/export/probe-source.ts:28-42`.
- The new ?window=recording-ready renderer root subscribes with onShow and then sends ready, which makes main send the payload; the card reports its height throu… (`apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:24`) — The transparent window shows the card with its pop-in animation, and a new payload remounts the card by assetId key. If it fails: If the payload never arrives, the window stays empty and transparent with no fallback, as documented under "Not done". Evidence: `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.tsx:18-72`, `apps/kaipu-record/src/renderer/src/features/recording-ready/recording-ready-card.test.tsx:37-43`, `apps/kaipu-record/src/renderer/src/main.tsx:66-71`.

</details>

<details><summary>What the reviewer checked</summary>

**Batch 1 of 2.** I found no blockers or must-fix problems in part 1. Nothing was run, and the window has not been tested in Electron; the backlog doc says the same.

- **Boundary:** The shared contract file takes only type imports, so the preload bundle gets no new value import. Card-to-main actions are parsed and sender-checked, and `recording-ready:show` validates its payload.
- **Window setup:** It matches the capture toast pattern.
- **Display tracking:** `lastTakeDisplayId` is reset on each take, and the display lookup fills in the screen source's id.
- **Docs:** The backlog doc discloses the known gap that a window which is created but never loads shows nothing and has no fallback.

I raised three consider-level notes:

- **No sender check on `show`:** the `recording-ready:show` handler does not check who is asking, unlike the other three channels.
- **No `app.focus({ steal: true })`:** the hand-off to the main window skips it, which `bringAppToFront` and the stop path both do. I'm unsure whether the main window comes forward after a press on macOS.
- **Possible flash on re-show:** the previous recording's card may flash when the window is re-shown. I'm unsure of this one.

**Batch 2 of 2.** The renderer side of part 2 is sound. The floating ask runs once per `location.key` after the probe settles, and the in-app fallback on a false answer or a rejected IPC is correct and tested. The card, hand-off and setup tests assert what their names say. I found three things, all "consider". The card's 80 px blur shadow is likely to be clipped by the 16 px window padding. The ask-once ref resets on remount, so Back after a chip or Edit first re-floats the card. The doc overstates which actions bring up the main window. Whether main validates the card's action payload and the sender is outside this part and still needs a look in part 1.

</details>

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost (estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 18 | $0.29 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 17 | $0.22 |

</details>

<sub>Answer a finding in its thread: `Verdict: correct` or `Verdict: wrong`, and why.</sub>

<sub>Claude Sonnet 5.5 via Claude Code 2.1.304 · effort high · review · 2 batches · 32 in / 20k out / 685k cache read / 100k cache write · Claude subscription: API-equivalent estimate, not a bill · $0.51</sub>

<!-- wachi:review -->

<!-- wachiman sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:state eyJmb3JtYXQiOiJ3YWNoaW1hbi5yZXZpZXctc3RhdGUvMSIsImVuZ2luZSI6IjEuMjIuMCIsImhlYWQiOiJiMjcwNWE5Y2UyNTkzYjI5YWU1MDIzNTMxMmE0MjI2OTU1YmJiYjM2IiwiYXR0ZW1wdCI6IjMyNTkxMTBkLWRlYzMtNGIxMi04ZGM2LWI5YjdlMDBjMThlMCIsInN0YXR1cyI6ImNvbXBsZXRlIiwicmVhc29uIjpudWxsLCJmaW5kaW5ncyI6eyJ0b3RhbCI6NiwiYnlfc2V2ZXJpdHkiOnsiYmxvY2tlciI6MCwiZml4IjowLCJjb25zaWRlciI6NiwiaW5mbyI6MH0sImJ5X3BsYWNlbWVudCI6eyJpbmxpbmUiOjYsImJvZHkiOjAsIm91dHNpZGVfZGlmZiI6MH0sInVudGhyZWFkZWRfYmxvY2tpbmciOjB9fQ -->

<!-- wachi:attempt id=3259110d-dec3-4b12-8dc6-b9b7e00c18e0 -->
