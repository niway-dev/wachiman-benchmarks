<!-- token-cap-0.75-ttl-5m, oauth-token-2: 13 turns, $0.59 -->

I found five real bugs. None of them crash the page; they are behaviour and display problems. I read the diff and the code it calls but did not run the tests.

### 1. The destination cards show "…" forever when the file can't be read
`apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:263` and `:311`

- **What goes wrong:** if reading the file fails, every card except Archive shows "…" permanently. It looks like it's still loading.
- **Why:** the page passes only `useSourceProbe(...).probe` (`library-detail-page.tsx:142`), so a failure and a load in progress both arrive as `probe: null`. The panel can't tell them apart. `useSourceProbe` does have an `"error"` status, but it is dropped before it reaches the panel. A failed read should show nothing, or a "size unknown" message, instead of "…".

### 2. "Drag" on a copy doesn't mark that copy as seen
`apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:834-838`

- **What goes wrong:** you can drag a finished copy into another app from the recording page, and the Library still flags it as an unseen copy afterwards.
- **Why:** the doc says this button uses "the same IPC as the ready card", but the ready card does two things when a drag starts: it calls `markCopySeen(recording.assetId)` and then `startFileDrag` (`export-status-cards.tsx:233-235`). The new button only calls `startFileDrag`. Elsewhere a copy is only marked seen when its own page is opened (`shell/sidebar.tsx:95`), and dragging from the original's page never opens it.

### 3. "Not now" lasts longer than "this visit"
`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:139` and `:191`, `:2044` in the diff

- **What goes wrong:** say you dismiss "Where is it going?" on recording A. Then you follow a link to a copy or source page and come back to A, by link or with Back. The panel stays hidden. The doc and the code comment both say it's hidden only "for that visit" / "until the page is left".
- **Why:** the dismissal is stored by `video.assetId`. Moving from one `/library/:id` page to another reuses the same page component, so that stored value survives. The "Saved" notice and the "ready" card key on `location.key` instead, which is why they reset correctly. The panel should do the same.

### 4. Copy sizes can be wrong for a moment when you open a copy from the original
`master-copies-panel.tsx:756-766`, using the `probe` passed at `library-detail-page.tsx:2062`

- **What goes wrong:** this window opens when you go from a copy's page to its original. For a moment, the copy rows can show a picture size worked out from the previous page's file.
- **Why:** this one is mostly harmless. `useSourceProbe` reports the old result as "loading" once the id changes (`use-prepare-copy.ts:66`), so the wrong numbers can't stick. In practice it shows up as a brief blank: only the file size shows until the new read finishes. I'd treat it as a minor glitch, not a correctness bug.

### 5. The player-height cap assumes a 16:9 video
`apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.module.css:1212`

- **What goes wrong:** for a portrait or square recording, the player can be much taller than the window. That pushes the action buttons and the panels off screen at the default 900 × 670, which is exactly what the change says it prevents.
- **Why:** `width: min(100%, max(420px, calc((100vh - 300px) * 16 / 9)))` turns the height limit into a width using a fixed 16:9 ratio. For example, a 9:16 video at about 658 px wide is roughly 1170 px tall.

### Minor: a test change leaks into other tests
`master-copies-panel.test.tsx:635` replaces `window.electronAPI.startFileDrag` with a mock and never puts the original back. Every test that runs after it in the same environment sees the mock.
