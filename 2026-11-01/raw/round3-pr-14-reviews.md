=== REVIEW 5730204359 2026-11-01T20:49:33Z commit=b2705a9
👮 **Wachiman** · review of the whole pull request, at `b2705a9`: all 28 files reviewed.

2 finding(s): 2 to consider; 2 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 adds the floating "Your video is ready" window, and nothing in it blocks the merge. The new IPC follows the capture toast's pattern. Card → main messages are checked against the window's own `webContents` and parsed before use, and the show request's payload is validated too. `shared/recording-ready.ts` keeps its value-free contract (no value imports from workspace packages). I left two "consider" findings. First, a reused window may show the previous take's card for a frame when it reappears. Second, a doc comment in `post-recording-card.tsx` still describes only the in-app behaviour.

**Batch 2 of 2.** I found nothing to flag in the 13 files of part 2.

- **Recording page:** it asks main for the floating card only after the probe has finished reading the file, whether it succeeded or failed. `probeSource` catches its own errors, so the probe always finishes and the request always goes out. A ref in `useFloatingReadyCard` makes sure it asks only once per arrival. The in-app card shows only when main answers false or the call fails. Its size, duration and dimensions come from the same sources as the floating payload.
- **Hand-offs and window root:** these follow the capture toast's pattern. `pathForHandOff` builds its paths with the existing `preparePath`, `editorPathFor` and `ROUTES.libraryDetail` helpers.
- **Sizing:** the 16 px body padding in `main.css` matches `READY_WINDOW_PADDING` in main. Main adds twice the padding to the frame height the card reports.
- **Tests:** the test stubs and the new tests check what their names say.
- **Docs and messages:** the backlog doc and its index row match the code and follow the status-banner rules. The new `openFloatingHint` string exists in both English and Spanish, and `PostRecordingCard` uses it.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 15 | 998 | 8 | reviewed | 6 | $0.29 |
| Batch 2 of 2 | 13 | 297 | 4 | reviewed | 12 | $0.30 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 2 batches · $0.59</sub>

<!-- wachi:review -->

<!-- agent-review sha=b2705a9ce2593b29ae50235312a4226955bbbb36 -->

<!-- wachi:attempt id=06904ddd-11fd-47ed-84d3-dc08b43ca335 -->

