# 2026-11-09: day summary

The day holds 123 merged PRs in pingdotgg/t3code, annotated as 5 chunks (chunks 01 to 04 hold 25
each, chunk 05 holds the last 23).

Columns:

- **Bot threads**: CodeRabbit and Macroscope threads on the chunk's PRs (from the chunk header).
- **Real-bug threads**: threads with verdict `real-bug` (from the chunk header).
- **Fix PRs traced**: Track B rows where the trace found one introducing PR, out of all Track B
  table rows. Rows with no usable target (pure addition, refactor only, trivial, or several
  candidate PRs) are not traced.
- **Caught / missed / did not run / not checked**: what the bots did on the introducing PR for
  each traced row. Counted from the "bots at intro" column of the Track B tables.
  - *caught*: a bot flagged the defect itself on that PR.
  - *missed*: the bots commented on that PR, but not on the defect.
  - *did not run*: the PR had no bot comments at all.
  - *not checked*: the chunk did not check the PR.

| Chunk | PRs | Bot threads (CodeRabbit / Macroscope) | Real-bug threads | Fix PRs traced | Caught | Missed | Did not run | Not checked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [01](chunk-01.md) | 25 | 12 (5 / 7) | 4 | 8 of 10 | 2 | 6 | 0 | 0 |
| [02](chunk-02.md) | 25 | 42 (21 / 21) | 4 | 6 of 6 | 0 | 6 | 0 | 0 |
| [03](chunk-03.md) | 25 | 66 (41 / 25) | 13 | 5 of 11 | 0 | 4 | 1 | 0 |
| [04](chunk-04.md) | 25 | 25 (22 / 3) | 7 | 8 of 9 | 2 | 6 | 0 | 0 |
| [05](chunk-05.md) | 23 | 60 (46 / 14) | 10 | 11 of 17 | 0 | 8 | 2 | 1 |
| **Total** | **123** | **205 (135 / 70)** | **38** | **38 of 53** | **4** | **30** | **3** | **1** |

## Notes on the counts

- **Counted from the table rows, not the chunk headers.** Chunk 01 header says 10 traced; 2 rows
  have no target (`#33518`, `#33538`), so 8. Chunk 02 header says 12 fix PRs and SZZ on 6; the
  table has 6 rows. Chunk 03 header says 7 SZZ runs, 5 meaningful traces; `#31739` ("none clean",
  closest `#1371`) is not traced. Chunk 04 header says 9 resolved; `#29832` (blame is `#29164`,
  which only added a branch, bots had 0 comments) is not traced, so 8. Chunk 05 header says 10
  traced; the table gives 11 rows with a named PR, 1 of them not checked (`#21163`).
- **Caught counts the row label.** Chunk 01 `#33598` is "caught-and-ignored" but the bots
  predicted the timer problem, not the latency, so it is a loose catch. Chunk 01 `#33501` and
  chunk 04 `#30370` and `#29308` are "caught-and-ignored". Chunk 01 tallies 2 caught, chunk 04
  tallies 2 caught: same as here.
- **Judgement calls.** Chunk 04 `#31337` counted missed (bots missed it on `#18505`; a related
  comment on `#10054` is not the same defect). Chunk 05 `#24933` ("partly") counted missed.
  Chunk 05 `#24079` (two introducing PRs, bots "too diluted to judge") and `#25828` ("not
  checked", no single target) are not traced. Chunk 05 `#25835` is traced from the PR body
  (SZZ found a pure addition).
- **Ranges are not ordered by PR number.** Chunks 04 and 05 list PRs by merge time, so low
  numbers merged on this day.
- **Missing fields in the catalogue.** Severity and diff are copied from the Track B row only when
  that row's introducing PR matches the candidate's. Class is "-" everywhere. Track A candidates
  fixed before merge list the same PR as fix and intro. Base and head cells keep the chunk's
  parenthetical notes where the chunk wrote them.
- **Replay caveats.** Chunk 03 bases for `#33093` and `#33092` are the PR base, not its first
  commit. Chunk 02 `codex-goal-command-notice-queued` uses the base and last commit of `#29909`;
  a diff-only reviewer is unlikely to reach it. Chunk 05 Track A heads are the commit the bot
  commented on, not the PR's last commit.

## Chunks

- [chunk-01.md](chunk-01.md): PRs #33600 to #33291
- [chunk-02.md](chunk-02.md): PRs #33268 to #33143
- [chunk-03.md](chunk-03.md): PRs #33142 to #31739
- [chunk-04.md](chunk-04.md): PRs #31337 to #29025
- [chunk-05.md](chunk-05.md): PRs #29018 to #19064

The cross-batch catalogue is at [catalogue.md](../../catalogue.md). This day contributes 35 rows.
