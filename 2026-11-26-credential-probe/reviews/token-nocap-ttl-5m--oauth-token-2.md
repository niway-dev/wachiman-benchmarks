<!-- token-nocap-ttl-5m, oauth-token-2: 30 turns, $0.95 -->

I found one real bug and two smaller issues. I only read the code; I didn't run the tests or the app, and I changed no files.

### 1. A long title doesn't get an ellipsis; it spills over the master tag
**Where:** `apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.module.css:61` (`.title`), with `features/library/components/recording-title.module.css:1-15`

**What goes wrong:** The PR's stated goal is a title that takes the space the row leaves and gets an ellipsis at that edge, so it never collides with the tag. That doesn't happen:
- The page wrapper `.title` (`flex: 1; min-width: 0`) can shrink.
- But inside it, `RecordingTitle` renders its own flex row (`display: flex`). The `<h1>` in that row is a flex item with the default `min-width: auto`.
- With `white-space: nowrap`, that minimum is the full width of the text. So the `<h1>` never shrinks, and its `overflow: hidden; text-overflow: ellipsis` never applies.

**Why it matters:** With a long title, the `<h1>` and the rename pencil overflow the wrapper. Nothing clips that overflow, so they paint over the "MASTER · FULL QUALITY" tag beside them instead of being cut off. This is exactly the problem the owner reported, and it fails the doc's QA step "At 900 × 670 the title, tag and actions never truncate each other". jsdom doesn't do layout, so the tests can't catch it.

**Fix:** Add `min-width: 0` to the `<h1>` (or `.titleRow > .title`), or `overflow: hidden` on the page's `.title` wrapper.

### 2. (Likely, minor) The panels flicker when a background copy finishes
**Where:** `library-detail-page.tsx:189-191` (`hasCopies` / `showDestinations`), and `export-runner.ts:462`

**What goes wrong:** When the export finishes, the runner goes to idle and sets `ready` in one step, so `running` becomes `null` right away. But `exports` only gains the new copy once the library list comes back from `refresh()` or `onLibraryChanged`, which is asynchronous. In between, `hasCopies` is false. So the page briefly:
- swaps "Copies from this original" back to "Where is it going?",
- hides the "Export a copy" button,
- moves the heavy-to-send banner,
- then swaps everything back.

The old layout always showed the copies panel on a master, so it only flashed one line. Here two whole panels swap. I'm inferring this from the order of the state updates; I haven't seen it happen.

### 3. (Minor) "Not now" is remembered per recording, not per visit
**Where:** `library-detail-page.tsx:139` and the `onDismiss` handler that calls `setDestinationsDismissedFor(video.assetId)`

**What goes wrong:** The doc says "Not now" hides the panel "for that visit", and the code comment says "until the page is left". But the dismissal is keyed by `assetId`, and `/library/:assetId` keeps the same component mounted when only the asset changes. So going from recording A to another recording's page (for example through a ready-card link) and back to A leaves the panel hidden. The saved notice and the ready card next to it are keyed by `location.key`; keying this one the same way would make it last one visit.

### Checked and fine
- The `startFileDrag(id, name)` call matches the ready card and the preload signature.
- Every new i18n key exists in both `en.json` and `es.json`. The removed `where*`, `copiesEmpty` and `copyProgress*` keys are no longer used anywhere, and `sendTo` stays for the Library card and row.
- `?to=archive`, `?to=vertical`, `?to=square` and `?to=chat` are valid `DestinationId`s.
- The size estimates match `planCopy` and `resolveExportTarget`.
