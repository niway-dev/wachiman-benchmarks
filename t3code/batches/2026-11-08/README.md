# 2026-11-08: day summary

The day holds 56 merged PRs in pingdotgg/t3code, annotated as 3 chunks (chunks 01 and 02 hold 25
each, chunk 03 holds the last 6).

Columns:

- **Bot threads**: CodeRabbit and Macroscope threads on the chunk's PRs (from the chunk header).
- **Real-bug threads**: threads with verdict `real-bug` (from the chunk header).
- **Fix PRs traced**: Track B rows where the trace found one introducing PR, out of all Track B
  table rows. Rows with no usable target (pure addition, refactor only, trivial, unresolved stack
  commits, or no clean origin) are not traced.
- **Caught / missed / did not run / not checked**: what the bots did on the introducing PR for
  each traced row. Counted from the "bots at intro" column of the Track B tables.
  - *caught*: a bot flagged the defect itself on that PR.
  - *missed*: the bots commented on that PR, but not on the defect.
  - *did not run*: the PR had no bot comments at all.
  - *not checked*: the chunk did not check the PR.

| Chunk | PRs | Bot threads (CodeRabbit / Macroscope) | Real-bug threads | Fix PRs traced | Caught | Missed | Did not run | Not checked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [01](chunk-01.md) | 25 | 10 (6 / 4) | 2 | 4 of 8 | 0 | 2 | 2 | 0 |
| [02](chunk-02.md) | 25 | 15 (11 / 4) | 3 | 13 of 15 | 0 | 12 | 0 | 1 |
| [03](chunk-03.md) | 6 | 6 (5 / 1) | 1 | 2 of 5 | 0 | 2 | 0 | 0 |
| **Total** | **56** | **31 (22 / 9)** | **6** | **19 of 28** | **0** | **16** | **2** | **1** |

## Notes on the counts

- **Counted from the table rows, not the chunk headers.** Chunk 01 header says SZZ on 8; the
  table has 8 rows, but `#32893` and `#32712` land on unmerged stack commits (PR not resolved,
  "not checked"), `#32593` is not traced, and `#32573` has no clean introducing PR (origin is the
  import `#2829`, extended by `#17696`/`#20310`), so 4 traced. Chunk 02 header says 14 bugs with
  an introducing PR (0 caught, 13 missed, 1 not checked); the table has 13 rows with one, so 12
  missed and 1 not checked (`#28255`). Chunk 02 `#32266` and `#26737` have no target. Chunk 03
  header says 5 traced; the table has 5 rows, but 3 have no SZZ target (`#22295`, `#21592`,
  `#21524`), so 2.
- **Judgement calls.** Chunk 02 `#31585` counted missed: its introducing commit sits in `#28845`,
  which is still open (unmerged stack PR). Chunk 02 `#30709` counted missed (a near miss: Macroscope
  flagged a sibling nested-link case on `#26290`, not the angle-bracket form). Chunk 01 `#33109`
  counted missed (CodeRabbit asked for the opposite behaviour).
- **No bot caught any traced defect on this day.**
- **Missing fields in the catalogue.** Severity and diff are copied from the Track B row only when
  that row's introducing PR matches the candidate's. Class is "-" everywhere. Track A candidates
  fixed before merge list the same PR as fix and intro. Chunk 01 `late-delegated-read-consumes-wake`
  has no resolved introducing PR. Chunk 03 `terminal-option-layer-dropped-on-mac` has no base sha
  (not resolved in the chunk).
- **Replay caveats.** Chunk 01 `late-delegated-read-consumes-wake` replays the fix parent, since
  the origin is pre-existing. Chunk 03 `terminal-option-layer-dropped-on-mac` head is the last
  commit of `#7485`. Chunk 02 notes `#31585` is not replayable on main.

## Chunks

- [chunk-01.md](chunk-01.md): PRs #33109 to #32498
- [chunk-02.md](chunk-02.md): PRs #32266 to #24084
- [chunk-03.md](chunk-03.md): PRs #23821 to #21524

The cross-batch catalogue is at [catalogue.md](../../catalogue.md). This day contributes 7 rows.
