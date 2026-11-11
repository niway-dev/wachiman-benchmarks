# 2026-11-06: day summary

The day holds 167 merged PRs in pingdotgg/t3code, annotated as 7 chunks (chunks 01 to 06 hold 25
each, chunk 07 holds the last 17).

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
| [01](chunk-01.md) | 25 | 19 (19 / 0) | 2 | 3 of 6 | 0 | 3 | 0 | 0 |
| [02](chunk-02.md) | 25 | 10 (9 / 1) | 2 | 11 of 12 | 0 | 8 | 3 | 0 |
| [03](chunk-03.md) | 25 | 27 (25 / 2) | 1 | 11 of 16 | 1 | 8 | 2 | 0 |
| [04](chunk-04.md) | 25 | 32 (28 / 4) | 9 | 8 of 15 | 0 | 7 | 0 | 1 |
| [05](chunk-05.md) | 25 | 9 (9 / 0) | 1 | 14 of 19 | 1 | 13 | 0 | 0 |
| [06](chunk-06.md) | 25 | 54 (43 / 11) | 2 | 13 of 17 | 0 | 11 | 2 | 0 |
| [07](chunk-07.md) | 17 | 43 (35 / 8) | 3 | 9 of 12 | 1 | 8 | 0 | 0 |
| **Total** | **167** | **194 (168 / 26)** | **20** | **69 of 97** | **3** | **58** | **7** | **1** |

## Notes on the counts

- **Counted from the table rows, not the chunk headers.** Chunk 01 header says 12 `fix` PRs; the
  table has 6 rows (the other 6 were skipped as trivial or non-source) and 3 are traced
  (`#31815`, `#31819`, `#31928`, all missed); `#32154`, `#31924`, `#31888` are pure additions.
  Chunk 02 header says missed 11 (3 of them with no bot comment at all); here that is 8 missed and
  3 did not run (`#31741`, `#31642`, `#31285`). `#31717` has no clear target, so 11 of 12 traced.
  Chunk 03 header says 18 `fix` PRs and 16 non-trivial; the table has 16 rows, 5 with no usable
  target (`#30910`, `#30848`, `#30762` pure additions; `#30830`, `#30719` land on the `#2829`
  import), so 11 traced. Chunk 04 header says caught 0, missed 6, partial-adjacent 1 (`#30480`),
  not checked 1 (`#30652`), no usable target 7; here `#30480` is counted missed, so 7 missed and 8
  traced of 15 rows. Chunk 05 header gives no bots-at-intro tally; the table has 19 rows, 5 with no
  target (`#30390`, `#30369`, `#30295` on `#2829`; `#30138`, `#30361` pure additions), so 14
  traced. Chunk 06 header gives no tally either; the table has 17 rows, 4 with no target
  (`#29817`, `#28625` pure additions; `#29762`, `#27691` on `#2829`), so 13 traced. Chunk 07
  header matches: 9 traced, caught 1, missed 8.
- **Judgement calls.** Chunk 03 `#30798` and `#30726` are labelled "missed" in the table but the
  row says there were no bot comments on the introducing PR, so they are counted did not run.
  Chunk 06 `#29738` is marked trivial but has a medium-confidence origin and "missed", so it is
  counted traced. Chunk 03 `#30834`, chunk 04 `#30652` and `#30563`, and several chunk 05 and 07
  rows are low confidence and still counted traced. Chunk 05 `#30139` is counted missed (the bot
  comment on `#30308` is on a different point).
- **Caught rows.** All three are "caught-and-ignored": chunk 03 `#30743` (CodeRabbit on `#30174`),
  chunk 05 `#30332` (Macroscope on `#24343`, disputed by the author), chunk 07 `#22489`
  (Macroscope on `#4849`).
- **Missing fields in the catalogue.** Severity and diff are copied from the Track B row only
  when that row's introducing PR matches the candidate's. Class is "-" everywhere. Track A
  candidates fixed before merge list the same PR as fix and intro.
- **Replay caveats.** Chunk 01 Track A heads are the commits CodeRabbit commented on; pre-merge
  commits may be missing from a squash-merged clone (unverified). Chunk 02 `#30623` base is a
  stack branch tip, not main, and the two iOS candidates share `#8614` (3001 lines, one replay
  range). Chunk 05 `ios-composer-textkit2-layoutmanager-downgrade` (`#3101`, 8k lines) and
  `antigravity-intel-mac-hardened-runtime` (`#9348`, 21k lines) have low expected catch rates.
  Chunk 06 `autocorrect-flush-uncorrected-draft-after-send` is medium confidence and a 148-file
  replay. Chunk 03 has one candidate (Track A); no Track B bug there is both severity >= 3 and
  traceable.

## Chunks

- [chunk-01.md](chunk-01.md): PRs #32162 to #31814
- [chunk-02.md](chunk-02.md): PRs #31807 to #30942
- [chunk-03.md](chunk-03.md): PRs #30910 to #30679
- [chunk-04.md](chunk-04.md): PRs #30678 to #30397
- [chunk-05.md](chunk-05.md): PRs #30391 to #30135
- [chunk-06.md](chunk-06.md): PRs #30078 to #26452
- [chunk-07.md](chunk-07.md): PRs #25988 to #15632

The cross-batch catalogue is at [catalogue.md](../../catalogue.md). This day contributes 31 rows.
