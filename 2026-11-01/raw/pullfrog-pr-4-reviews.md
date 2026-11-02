=== REVIEW 5730240971 2026-11-01T20:59:57Z commit=b2705a9
> ℹ️ No critical issues — one visual rough edge inline.

**Reviewed changes**

This review covers the whole PR: "Your video is ready" moves out of the main window's status stack into its own floating window, built on the capture toast's pattern.

- **Floating window manager**: `RecordingReadyWindow` creates the window and shows it with `showInactive`. It reuses the window for each new take, sizes it to the height the card reports, and turns each action into a typed hand-off to the main window.
- **Take display tracking**: `RecordingHubHandle.lastTakeDisplayId()` records the display of the area, the countdown or the screen source. The window opens there, or on the cursor's display when that is unknown.
- **IPC contract**: `shared/types/recording-ready.ts` defines the payload, actions and hand-offs, with parsers for everything that crosses IPC. It adds six `recording-ready:*` channels.
- **Renderer entry and hand-offs**: the `?window=recording-ready` root renders the same `PostRecordingCard`. `useRecordingReadyHandOffs` turns each hand-off into a route using `preparePath`, `editorPathFor` and the library detail route.
- **Ask-then-fallback on the recording page**: `useFloatingReadyCard` asks main once per `location.key`, after the probe settles. The in-app card shows only when main answers `false` or the IPC rejects.
- **`PostRecordingCard`**: adds an optional `onOpen` prop and an `openFloatingHint` string in English and Spanish.

<!--
Pullfrog review metadata. These findings were written against b2705a9;
if commits have landed on replay/pr-466/head since, treat every specific bug, file, or
line callout as POTENTIALLY STALE and re-diff before acting on it.

- Mode: Review (initial)
- Files reviewed: 28
- Commits reviewed: 2
- Base: replay/pr-466/base (13b7ff5)
- Head: replay/pr-466/head (b2705a9)
- Reviewed commits:
  - db49e4b — feat(desktop): float "Your video is ready" outside the app window
  - b2705a9 — docs(backlog): "Your video is ready" floats on the desktop
- Prior pullfrog review: none
-->


<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [Fix all ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog/4?action=fix&review_id=5730240971) ｜ [Fix 👍s ➔](https://pullfrog.com/trigger/niway-dev/kaipu-bench-pullfrog/4?action=fix-approved&review_id=5730240971) ｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog/actions/runs/41349385331/job/124976065150) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

