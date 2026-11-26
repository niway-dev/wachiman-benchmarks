# Credential probe: labels of 21 reviews of kaipu-record #465

What was labelled: the 21 final texts in `reviews/*.md` (one plain `claude -p` call each, asked to
"list each real bug: file and line, what goes wrong, and why"), all reviewing kaipu-record #465
(head `dac8318`, base `13b7ff5`).

Key: [`../2026-11-26-release-bisect/prs/pr-465.md`](../2026-11-26-release-bisect/prs/pr-465.md):
"Expected issues", "Baseline additional findings", "New findings" and "Judgement calls".

Labelled by: Claude Sonnet 5.5, effort high, told to judge each finding on its text against the
key. The labelling is not blind: each file name and first line show the set, turns and cost.

Rules (as in the key):

- `yes`: the finding names the same mechanism at the same place (a line number that differs from
  the key's but points at the same code, or no line number but the same file and mechanism, counts).
- `partial`: it names the place but a weaker or different mechanism.
- `no`: otherwise.
- An item a review raises with its own bullet counts even when the review calls it "minor" or "not
  a bug", as long as it names the discrepancy as a concern. An item the review explicitly closes as
  "matches the code / intended" does not count. A finding is counted once per review.
- A finding that matches no row is "other" (O1, O2, ...), checked against the code at `dac8318`
  with `git show`, and given a verdict: valid, partly valid, invalid.

Mapping of ids. The key has only three expected issues (E1, E2, E3), not nine. Its baseline table
holds A1 to A5 and the N rows (N1 to N6); N7 to N9 are in "New findings". So:

- "Known" columns are E1 to E3 plus A1 to A5 (the rows of the key that are not N rows). "Known
  found" counts their `yes`, "Known partial" their `partial`.
- "N matched" lists the N rows (N1 to N9) matched; `(p)` marks a partial.
- A2 ("Panels flip when the first copy finishes") was `no` in every earlier run; it is found here by
  many reviews, so it is labelled like any other row.
- No review matched E1, A3, A5, N1, N2, N3, N6, N7 or N8, and none was partial on a known row, so
  those columns are all `no` and "Known partial" is 0 everywhere.

## Table 1: labels per review

| Review | E1 | E2 | E3 | A1 | A2 | A3 | A4 | A5 | Known found | Known partial | N matched | Other valid | Other invalid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cap-0.75--api-key-1 | no | no | yes | no | no | no | no | no | 1 | 0 | - | O1 | - |
| cap-0.75--api-key-2 | no | no | yes | yes | no | no | no | no | 2 | 0 | - | O1 | - |
| cap-0.75--api-key-3 | no | no | yes | yes | yes | no | no | no | 3 | 0 | - | - | - |
| cap-0.75--oauth-token-1 | no | yes | no | no | no | no | no | no | 1 | 0 | - | O1 | - |
| cap-0.75--oauth-token-2 | no | yes | no | no | no | no | no | no | 1 | 0 | - | O1 | - |
| cap-0.75--oauth-token-3 | no | no | no | no | no | no | no | no | 0 | 0 | N4, N9, N5 (p) | - | O5 |
| cap-3--api-key-1 | no | no | no | yes | yes | no | no | no | 2 | 0 | N9 | O7 | - |
| cap-3--api-key-2 | no | no | no | yes | no | no | yes | no | 2 | 0 | - | - | - |
| cap-3--api-key-3 | no | no | yes | yes | yes | no | no | no | 3 | 0 | - | - | - |
| cap-3--oauth-token-1 | no | no | yes | yes | yes | no | no | no | 3 | 0 | - | - | O2 |
| cap-3--oauth-token-2 | no | no | no | yes | yes | no | no | no | 2 | 0 | - | - | - |
| cap-3--oauth-token-3 | no | yes | no | yes | yes | no | no | no | 3 | 0 | - | - | - |
| token-cap-0.75-ttl-5m--oauth-token-1 | no | no | no | yes | yes | no | no | no | 2 | 0 | - | - | O3 |
| token-cap-0.75-ttl-5m--oauth-token-2 | no | yes | yes | yes | no | no | no | no | 3 | 0 | - | O1 | O3, O6 |
| token-cap-0.75-ttl-5m--oauth-token-3 | no | no | yes | yes | no | no | no | no | 2 | 0 | N9 | O1 | O4 |
| token-nocap-ttl-1h--oauth-token-1 | no | no | no | yes | no | no | yes | no | 2 | 0 | N9 | - | - |
| token-nocap-ttl-1h--oauth-token-2 | no | no | yes | yes | no | no | no | no | 2 | 0 | - | - | O2 |
| token-nocap-ttl-1h--oauth-token-3 | no | no | yes | yes | no | no | no | no | 2 | 0 | - | - | - |
| token-nocap-ttl-5m--oauth-token-1 | no | no | no | yes | no | no | no | no | 1 | 0 | N9 | - | - |
| token-nocap-ttl-5m--oauth-token-2 | no | no | no | no | yes | no | no | no | 1 | 0 | - | O1 | O2 |
| token-nocap-ttl-5m--oauth-token-3 | no | no | yes | yes | yes | no | no | no | 3 | 0 | - | - | - |

## Table 2: "other" issues

Code checked with `git show dac8318:<path>` in `/tmp/kaipu-mine/repo`. Paths are under
`apps/kaipu-record/src/renderer/src/` unless stated. Raised by: O1 in 7 reviews, O2 in 3, O3 in 2,
O4 in 1, O5 in 1, O6 in 1, O7 in 1.

| ID | Issue | Verdict | Why | file:line |
|---|---|---|---|---|
| O1 | "Not now" on "Where is it going?" is stored by `assetId` in component state, so it outlives the visit: go from recording A to another `/library/:id` page and back, and A's panel stays hidden. The code comment says "until the page is left" and the backlog doc says "for that visit". | valid (low) | `destinationsDismissedFor` is keyed by `video.assetId` and the route `<LibraryDetailPage />` has no `key`, so React Router reuses the instance when only `:assetId` changes; the "Saved" notice and the card are keyed by `location.key`, this one is not. Narrow to reach (needs a detail-to-detail hop with no copies), but it contradicts the doc line. | `pages/library-detail/library-detail-page.tsx:138-139, 190-191`; `app/router.tsx:67`; doc `apps/documentation/src/content/docs/backlog/prepare-screen.md:101` |
| O2 | A long title overflows over the master tag instead of ending in an ellipsis, because the `<h1>` keeps `min-width: auto`. | invalid | The `<h1>` has `overflow: hidden`, and a flex item with a non-visible overflow gets an automatic minimum size of 0, so it can shrink; its row is a block-level flex box inside the wrapper that has `min-width: 0`, so the ellipsis applies as the PR intends. | `features/library/components/recording-title.module.css:8-15`; `pages/library-detail/library-detail-page.module.css:61-64` |
| O3 | The player width cap `calc((100vh - 300px) * 16 / 9)` assumes 16:9, so a portrait recording renders over 1100 px tall and pushes the actions off screen. | invalid | The player box is `aspect-ratio: 16 / 9` and the `<video>` is `object-fit: contain`, so a portrait file is letterboxed inside a 16:9 box whose width is the capped one; the height never exceeds the cap. | `features/library/components/recording-player.module.css:3`; `pages/library-detail/library-detail-page.module.css:201-205` |
| O4 | Copy rows' "W x H" is recomputed from the page's probe and the preset (copies of a copy, or a Fill copy, get the wrong size). | invalid | The rows listed are `exportsOf(this video)`, so this page's file is their direct source; a canvas preset's width and height are fixed (`preset.canvas`) whatever the framing, so omitting `framing` changes nothing in the label. | `features/prepare/components/master-copies-panel.tsx:104-110`; `features/video-editor/export/export-presets.ts:485` |
| O5 | Reels and LinkedIn card estimates may differ from Prepare because the panel calls `planCopy` with no `framing`. | invalid | `estimateBytes` comes from the canvas size and fps, not from the framing (framing only changes `pictureChange` edges), and Prepare starts from each preset's default framing, which is what `framing: null` resolves to. The reviewer itself says it did not check. | `features/prepare/components/destinations-panel.tsx:44-50`; `features/prepare/destinations.ts:179-190`; `export-presets.ts:481-485` |
| O6 | Copy rows can show a picture size from the previous page's file for a moment after navigating. | invalid | `useSourceProbe` returns `{ status: "loading", probe: null }` whenever `state.id !== videoId`, so a stale probe is never passed down; the review concedes the numbers "can't stick". | `features/prepare/use-prepare-copy.ts:64-66` |
| O7 | The Archive card shows the file size with `formatMB` ("1500 MB") while the details line uses `formatSize` ("1.5 GB"), so a 1.5 GB recording reads two ways on one page. | valid (cosmetic) | `formatMB` never switches to GB (`mb < 10 ? toFixed(1) : round`), `formatSize` does; both render on the page for the same `fileSizeBytes`. Only visible for files of 1 GB or more. | `features/prepare/components/destinations-panel.tsx:42`; `features/video-editor/export/export-size.ts:15-18`; `features/library/format.ts:17-28`; `pages/library-detail/library-detail-page.tsx:300` |

## Judgement calls

- Known list. The key defines E1 to E3 only, so "Known" here also includes the baseline A rows
  (A1 to A5). If only E1 to E3 count as known, "Known found" is the number of `yes` in the E1 to E3
  columns alone (0 to 2 per review; 8 reviews have none).
- cap-0.75--oauth-token-1: the E2 (unrestored `startFileDrag`) and the O1 items sit under "Minor
  points, not bugs". Counted as raised: each has its own bullet with the mechanism and the line.
  The review itself says O1 "almost never shows".
- cap-0.75--oauth-token-3: its note that "Not now" is stored by recording id "matches what was
  written" is closed as intended, so O1 is not counted for it.
- cap-0.75--oauth-token-3: N5 is `partial`. The finding is the N9 behaviour and ends with "no test
  covers this case"; it names the gap but not the test file.
- N9 `yes` for token-cap-0.75-ttl-5m--oauth-token-3, although it sits under "Smaller points (not
  bugs)" and says "seems intended": it still names the doc mismatch ("the updated doc only mentions
  the banner for a heavy copy, or a heavy master with copies"), which is the row. Three reviews close
  the same behaviour as matching the doc (cap-0.75--oauth-token-1, cap-3--api-key-2,
  cap-3--oauth-token-2); they are `no`.
- N4 `yes` for cap-0.75--oauth-token-3 only: it asks the row's question (every local recording is now
  read; is the cost acceptable) as its own item. Reviews that mention the per-visit read only as
  context for A1 are A1, not N4.
- E2 `yes` for cap-3--oauth-token-3: no line number, but it names the file, the unrestored
  `startFileDrag` assignment and the `vi.spyOn` plus `mockRestore()` fix; it says "not a product bug".
  Same for token-cap-0.75-ttl-5m--oauth-token-2 (cites `:635`, a diff line, for the same test).
- A4 `yes` for cap-3--api-key-2 (`prepare-screen.md:179`) and token-nocap-ttl-1h--oauth-token-1
  (no line): the key cites `:184`; the QA step "Drag the copy's row ..." is at `:183-184` at the head
  commit, so it is the same step.
- A2 is `yes` for nine reviews even though it was `no` in all earlier runs: they all give the key's
  mechanism (`running` becomes null at once, the new copy reaches `exports` only after `refresh()`).
  token-nocap-ttl-5m--oauth-token-2 labels it "likely, minor, inferred"; counted, since it names the
  mechanism and the place.
- O1 verdict "valid (low)" rather than "partly valid": the behaviour is real and contradicts the doc
  and the comment; only its reach is narrow.
