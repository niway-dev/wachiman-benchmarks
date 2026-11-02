=== REVIEW 5730202871 2026-11-01T20:49:10Z commit=e45c845
👮 **Wachiman** · review of the whole pull request, at `e45c845`: all 31 files reviewed.

1 finding(s): 1 to consider; 1 on their lines. Reply in a comment's thread to answer it.

### Summary

**Batch 1 of 2.** Part 1 looks sound. The changes covered are the export widget minimizing to a pill (with the choice kept in sessionStorage), the Library's \"Ready to upload\" cards, and reading the destination tag from the sidecar fingerprint through the `#revision` suffix. The ICU fallbacks behave: `destinationArg`'s \"export\" and the ready card's \"other\" both land on the `other` branch. Moving card retirement from the page's unmount to the sidebar's route watch is consistent with the tests. One accessibility point to consider: the pill's aria-label hides its progress from screen readers.

**Batch 2 of 2.** Part 2 (stylesheets, backlog docs, i18n messages): no findings. I checked the CSS variables these files use. All of them are defined in packages/tokens or the renderer's base.css, and the one that isn't, `--bg-hover`, has a fallback. The i18n keys that were removed (`hide`, `readyDragToUpload`) are no longer used anywhere in the renderer. Every key that was added (`pill`, `dragTo`, `destinationTag`, `minimize`, `expand`, `readyToUpload`, `fromOriginal`, `readyCardLabel`, `readyCardClose`, `progressNote`) is used by the new components, and every `select` covers every `DestinationId`. The new backlog doc matches the code: the minimized state is stored in sessionStorage, `retireReadyCards`/`dismissReadyCard` behave as described, ready cards are listed newest first, and `copyDestinationOf` compares only the part of the fingerprint before `#`. The doc has a status banner and a 🟡 row in backlog/index.mdx, as the docs rules require.

<details><summary>Coverage by batch</summary>

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 2 | 22 | 835 | 4 | reviewed | 4 | $0.26 |
| Batch 2 of 2 | 9 | 427 | 1 | reviewed | 13 | $0.28 |

</details>

<sub>Claude Opus 5.5 via Claude Code 2.1.304 · 2 batches · $0.54</sub>

<!-- wachi:review -->

<!-- agent-review sha=e45c845143ba72f35fea4fac2f9d62a186dff986 -->

<!-- wachi:attempt id=413dd5ca-61d3-47ea-bae0-7ee3c624c07d -->

