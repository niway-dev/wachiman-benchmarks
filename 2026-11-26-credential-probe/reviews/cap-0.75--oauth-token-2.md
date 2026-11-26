<!-- cap-0.75, oauth-token-2: 12 turns, $0.69 -->

I found one real bug in this PR, plus one smaller test issue. I read the diff and the code it calls (`destinations.ts`, `useSourceProbe`/`asPreparable`, `resolveExportTarget`, `isMaster`, the `startFileDrag` path through preload and main, the formatters, and the i18n keys). I didn't run the tests or modify any file.

### Bug

**`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139` and `:190-191` — "Not now" stays in effect after you leave the page**

- **What goes wrong:** "Not now" stores `video.assetId` in `destinationsDismissedFor`, and `showDestinations` checks `destinationsDismissedFor !== video.assetId`. Suppose you press "Not now" on recording A, open a copy or another recording (`/library/B`), then come back to A through the source link. The "Where is it going?" panel stays hidden. The only way to get it back is to unmount the page, for example by going to the Library list.
- **Why:** `/library/:assetId` keeps the same `LibraryDetailPage` instance when only the param changes, so the state survives the round trip. The code comment says "hidden for this recording until the page is left", and the backlog doc says "hides the panel for that visit". Neither is what happens.
- **The same file already does this correctly:** the "Your video is ready" card and the new "Saved" notice key their dismissal on `location.key` (`:128-137`). Keying "Not now" on `location.key` too (or on `location.key` plus `assetId`) would make it last one visit.
- **A related side effect:** while the panel is dismissed on a heavy master, `heavy && !showDestinations` shows `HeavyToSendBanner`. So the stale dismissal also swaps the in-panel hint for the banner on later visits.

### Test issue

**`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:99-100` — a mock leaks into later tests**

- The test runs `window.electronAPI.startFileDrag = vi.fn()` and never restores the original. Every later test in the run gets the mock.
- The existing test for the same feature (`export-status-cards.test.tsx:143-152`) uses `vi.spyOn(...)` and `mockRestore()` instead.

### Checked and fine

- The Drag handle's `startFileDrag(copy.id!, copy.title)` matches the API signature and the IPC handler in main.
- Every i18n key the PR removes has no remaining use. `sendTo` is still defined because the Library card and row still use it.
- `useSourceProbe` drops a stale probe when the id changes, so the new resolution shown in the metadata line can't show the previous recording's numbers.
