# 2026-11-10: day summary

The day holds 186 merged PRs in pingdotgg/t3code, annotated as 8 chunks (chunks 01 to 07 hold 25
each, chunk 08 holds the last 11).

Chunks 06 and 07 are fixes to the unmerged redesign stack (#28839-#28845). Macroscope skipped
#28845 for its cost limit, so every fix whose introducing PR is #28845 counts as did not run.

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
| [01](chunk-01.md) | 25 | 56 (34 / 22) | 23 | 8 of 17 | 0 | 5 | 1 | 2 |
| [02](chunk-02.md) | 25 | 13 (7 / 6) | 6 | 11 of 20 | 1 | 8 | 2 | 0 |
| [03](chunk-03.md) | 25 | 29 (15 / 14) | 8 | 11 of 18 | 0 | 6 | 5 | 0 |
| [04](chunk-04.md) | 25 | 10 (9 / 1) | 1 | 12 of 21 | 0 | 8 | 1 | 3 |
| [05](chunk-05.md) | 25 | 22 (17 / 5) | 1 | 10 of 25 | 0 | 9 | 0 | 1 |
| [06](chunk-06.md) | 25 | 10 (0 / 10) | 1 | 8 of 24 | 0 | 5 | 0 | 3 |
| [07](chunk-07.md) | 25 | 28 (0 / 28) | 3 | 19 of 25 | 0 | 4 | 12 | 3 |
| [08](chunk-08.md) | 11 | 41 (29 / 12) | 5 | 6 of 11 | 1 | 4 | 1 | 0 |
| **Total** | **186** | **209 (111 / 98)** | **48** | **85 of 161** | **2** | **49** | **22** | **12** |

## Notes on the counts

- **Caught is strict.** A bot comment on a neighbouring defect in the same file does not count.
  The two caught rows are chunk 02 `#33741` and chunk 08 `#26630` (both "caught-and-ignored").
- **Counted from the table rows, not the chunk tallies.** Chunk 02 header says 13 SZZ runs, but 2
  of them found no target (`#33768`, `#33820`), so 11 are traced. Chunk 03 says 13 traced, of
  which 2 are "n/a" (`#33629`, `#33626`), so 11. Chunk 05 says missed 9 plus ran-silent 1; here
  `#32815` ("ran silent": reviews exist, no inline comment) counts as missed, and `#32605`
  (low-confidence target, not checked) counts as not checked. Chunk 06 tallies missed 6; the table
  gives 5, with `#31624` ("partial": bots commented on other defects) counted as missed.
- **Not traced despite a named PR.** Chunk 07 `#31433` (1 line in `#31585`, then `#28845`, bots
  "n/a") and chunk 08 `#27791` (blame is the `#2829` import, closest PR only) and `#27677`
  (pure addition) are not traced.
- **Ranges are not ordered by PR number in chunk 08.** Low numbers such as `#13809` merged on
  this day.
- **Missing fields in the catalogue.** Severity and diff are copied from the Track B row only when
  that row's introducing PR matches the candidate's. Class is "-" everywhere. Track A candidates
  fixed before merge list the same PR as fix and intro. Chunk 05 `cancel-queued-wake-...` covers
  two escapes, so its fix, intro, caught-by, base and head cells carry (a) and (b).
- **Replay caveats.** Chunk 01 and chunk 02 heads are the PR's last commit, which already contains
  the fixes. The `#34007` stale-branch row has no recoverable head.

## Chunks

- [chunk-01.md](chunk-01.md): PRs #34106 to #33867
- [chunk-02.md](chunk-02.md): PRs #33820 to #33655
- [chunk-03.md](chunk-03.md): PRs #33647 to #33534
- [chunk-04.md](chunk-04.md): PRs #33529 to #32899
- [chunk-05.md](chunk-05.md): PRs #32861 to #31827
- [chunk-06.md](chunk-06.md): PRs #31823 to #31537
- [chunk-07.md](chunk-07.md): PRs #31535 to #31262
- [chunk-08.md](chunk-08.md): PRs #28353 to #13809

The cross-batch catalogue is at [catalogue.md](../../catalogue.md). This day contributes 41 rows.
