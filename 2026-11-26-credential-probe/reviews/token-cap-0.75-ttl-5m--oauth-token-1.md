<!-- token-cap-0.75-ttl-5m, oauth-token-1: 14 turns, $0.57 -->

I found two real bugs and one smaller layout issue. I didn't run the tests or the app; all of this comes from reading the diff and the code it calls.

### 1. The "Where is it going?" panel flashes back when a copy finishes
**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189-191`** (and the `hasCopies &&` gate at :507)

```ts
const hasCopies = exports.length > 0 || running !== null;
const showDestinations = master && preparable !== null && !hasCopies && …;
```

- **What goes wrong:** On a recording with no copies yet, the user starts a copy and comes back while it encodes. The progress row shows correctly, but when the export ends it disappears, "Where is it going?" pops back up with "Export a copy" hidden, and then everything swaps again once the list is refreshed.
- **Why:** `running` only counts while the runner's status is `"exporting"` (`runningCopyOf`, `master-copies-panel.tsx:35`). When the export ends, `running` becomes `null` straight away. The new copy only reaches `exports` after `refresh()` finishes, and that call starts in an effect after `readyId` changes (:146-148).
- **What's new here:** The old page kept the copies panel mounted for any master (`showCopies = master || …`), so this gap never showed. Now `hasCopies` switches the page between two different layouts.
- **Same cause, uncertain:** if the runner has any state before or after `"exporting"` that still means a copy is in progress, the panel shows there too, offering to start a second export. I didn't check whether such a state exists.

### 2. Destination cards show "…" forever if the file can't be read
**`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263` and `:311`**

- **What goes wrong:** If the probe fails (the file is unreadable, or zero width, height or duration), every card except Archive shows "…" indefinitely, as if still loading.
- **Why:** `useSourceProbe` has a separate `"error"` state, but the page keeps only `.probe` (`library-detail-page.tsx:142`), which is `null` for both loading and error. So `estimate()` returns `null` and the card falls back to `"…"`.
- **What's new here:** This PR now reads the file for every local recording, not just heavy ones, so far more pages can hit the failure case. The panel needs the probe's status, so it can show no estimate (or the full size) on error.

### 3. Smaller: the player size cap assumes a 16:9 video
**`library-detail-page.module.css`, `.player`**

- **What goes wrong:** The width is `min(100%, max(420px, calc((100vh - 300px) * 16 / 9)))`, which caps only the width. A portrait recording (for example 1080 × 1920) gets about 658 px of width at 900 × 670, so it renders over 1100 px tall. That pushes the actions and the panel far below the fold, the opposite of what the comment intends.
- **Fix:** Cap the height (for example `max-height` on the video) rather than deriving the width from a fixed aspect ratio.

The new i18n keys are present in both `en.json` and `es.json`, and nothing else uses the keys the PR removes. The planning calls in `DestinationsPanel` match `destinations.ts`.
