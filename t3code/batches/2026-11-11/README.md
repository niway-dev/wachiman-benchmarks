# 2026-11-11: day summary

The day holds 203 merged PRs in pingdotgg/t3code, annotated as 8 chunks. Chunk 08 also
covers 3 PRs from chunk 9 (#10495, #9954, #8766), so the chunks add up to 203.

Columns:

- **Bot threads**: CodeRabbit and Macroscope threads on the chunk's PRs (from the chunk header).
- **Real-bug threads**: threads with verdict `real-bug` (from the chunk header).
- **Fix PRs traced**: Track B rows where the trace found one introducing PR, out of all Track B
  rows. Rows with no usable target (pure addition, refactor only, trivial, or several candidate
  PRs) are not traced.
- **Caught / missed / did not run / not checked**: what the bots did on the introducing PR for
  each traced row. Counted from the "bots at intro" column of the Track B tables.
  - *caught*: a bot flagged the defect itself on that PR.
  - *missed*: the bots commented on that PR, but not on the defect.
  - *did not run*: the PR had no bot comments at all.
  - *not checked*: the chunk did not check the PR.

| Chunk | PRs | Bot threads (CodeRabbit / Macroscope) | Real-bug threads | Fix PRs traced | Caught | Missed | Did not run | Not checked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [01](chunk-01.md) | 25 | 32 (24 / 8) | 5 | 7 of 9 | 0 | 7 | 0 | 0 |
| [02](chunk-02.md) | 25 | 51 (32 / 19) | 14 | 13 of 15 | 0 | 13 | 0 | 0 |
| [03](chunk-03.md) | 25 | 63 (52 / 11) | 5 | 22 of 23 | 1 | 16 | 4 | 1 |
| [04](chunk-04.md) | 25 | 24 (20 / 4) | 0 | 19 of 22 | 0 | 13 | 5 | 1 |
| [05](chunk-05.md) | 25 | 27 (25 / 2) | 0 | 20 of 24 | 1 | 15 | 2 | 2 |
| [06](chunk-06.md) | 25 | 50 (40 / 10) | 1 | 16 of 21 | 0 | 13 | 0 | 3 |
| [07](chunk-07.md) | 25 | 72 (56 / 16) | 8 | 21 of 25 | 0 | 16 | 4 | 1 |
| [08](chunk-08.md) | 28 | 52 (39 / 13) | 10 | 14 of 20 | 0 | 12 | 2 | 0 |
| **Total** | **203** | **371 (288 / 83)** | **43** | **132 of 159** | **2** | **105** | **17** | **8** |

## Notes on the counts

- **Caught is strict.** A bot comment on a neighbouring defect in the same function or file does
  not count as catching the defect. Three rows that the chunk labelled as "caught (adjacent)" or
  "adjacent only" are counted as missed: chunk 05 `#26601` and `#25978`, and chunk 06 `#24433`.
  Their counts move from caught to missed. Two rows labelled "missed" carry a "not examined"
  note, chunk 04 `#27275` and chunk 07 `#22948`. They stay in the missed count, but the chunk
  did not verify them.
- **Mixed row.** Chunk 08 `#18622` has two introducing PRs: `#20537` had no bot comments, and
  `#9507` was missed. It is counted once, as missed.
- **Chunk 02 header mismatch.** The chunk header says "15 traced, missed 15". Its Track B table
  has 13 traced rows; the other 2 (`#33783`, `#33129`) are "diffuse" and not traced. This table
  counts 13 traced and 13 missed.
- **Missing fields in the catalogue.** The chunk candidate tables carry no severity, diff or
  class columns. Severity and diff are copied from the Track B row only when that row's
  introducing PR matches the candidate's. Class is "-" everywhere.
- **Fix and intro PRs in the catalogue.** Taken from the candidate's PR text. Where the chunk
  says the bug was fixed before merge, the same PR is both the fix and the intro. Where the
  chunk names no introducing PR (chunk 08 `#19652`, `#18622`, `#15848`, `#15255`), the candidate
  PR is listed as intro, because the row's base and head are that PR's range. That is inferred,
  not confirmed. Fix is "-" where the chunk gives no fix.

## Chunks

- [chunk-01.md](chunk-01.md): PRs #34490 to #34139
- [chunk-02.md](chunk-02.md): PRs #34132 to #33058
- [chunk-03.md](chunk-03.md): PRs #32963 to #29183
- [chunk-04.md](chunk-04.md): PRs #29151 to #26963
- [chunk-05.md](chunk-05.md): PRs #26908 to #25911
- [chunk-06.md](chunk-06.md): PRs #25870 to #23001
- [chunk-07.md](chunk-07.md): PRs #22997 to #21676
- [chunk-08.md](chunk-08.md): PRs #21661 to #10895, plus chunk 9 PRs #10495, #9954, #8766

The cross-batch catalogue is at [catalogue.md](../../catalogue.md). This day contributes 57 rows.
