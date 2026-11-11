# 2026-11-07: day summary

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
| [01](chunk-01.md) | 25 | 8 (6 / 2) | 3 | 8 of 17 | 0 | 7 | 1 | 0 |
| [02](chunk-02.md) | 25 | 26 (23 / 3) | 2 | 11 of 14 | 0 | 8 | 1 | 2 |
| [03](chunk-03.md) | 6 | 16 (14 / 2) | 0 | 4 of 5 | 0 | 4 | 0 | 0 |
| **Total** | **56** | **50 (43 / 7)** | **5** | **23 of 36** | **0** | **19** | **2** | **2** |

## Notes on the counts

- **Counted from the table rows, not the chunk headers.** Chunk 01 header says 22 fix PRs and SZZ
  on 16; the table has 17 rows. Of those, `#32249` and `#32248` land on the unmerged stack PR
  `#28842` (not traced), and 7 rows have no usable target (pure additions `#32666`, `#32391`,
  `#32252`; noise `#32409`, `#32408`, `#32389`, `#32231`), so 8 traced. Chunk 02 header says 12
  introducing PRs (0 caught, 10 missed, 1 no bot comments, 1 not checked); the table has 14 rows,
  11 with one introducing PR: 8 missed, 1 did not run (`#31292`), 2 not checked (`#30230`,
  `#31168`), which matches the chunk's own bottom-line count. `#31825` has no single origin and
  `#31489`, `#31794` are pure additions. Chunk 03 header says missed 5 of 5; the table has 5 rows,
  but `#19659` has no clean origin (`#2829` / `#9348`), so 4 traced.
- **Judgement calls.** Chunk 01 `#32315` counted did not run (no bot review on `#31114`). Chunk 01
  `#32401` and `#32400` are counted traced (found by `git log -S`, low and medium confidence).
  Chunk 02 `#29586` and `#26324` counted traced despite low or medium confidence.
- **No bot caught any traced defect on this day.**
- **Missing fields in the catalogue.** Severity and diff are copied from the Track B row only when
  that row's introducing PR matches the candidate's. Class is "-" everywhere. Track A candidates
  fixed before merge list the same PR as fix and intro. Chunk 02 `cloud-dictation-reenabled-after-local-choice`
  and `voice-setup-cancelled-download-advances-wrong-model` are Track A; the second also has a
  Track B row on `#32035` with a different introducing PR (`#30623`), catalogued separately.
- **Replay caveats.** Chunk 01 `settings-read-failure-silent-defaults` head is the stack PR's last
  commit, and whether it lacked the gate then is unverified; the introducing PR `#28842` is still
  open. Chunk 02 `cloud-dictation-reenabled-after-local-choice` and
  `voice-setup-cancelled-download-advances-wrong-model` heads are the commits the bot commented on,
  and `android-review-diff-blank-after-section-switch` attribution is medium confidence. Chunk 03
  `service-install-overwrites-other-base-dir` origin confidence is low-medium; the fix PR `#23878`
  (base 006d7e38f0485431c314a1afcc39fa823f379092) is a cleaner replay of the same bug.
  `acp-raw-notification-unbounded-bytes` has low origin confidence and low replay value. Chunk 03
  `#19659` T1 (`__proto__` dropped) is severity 2 and not catalogued.

## Chunks

- [chunk-01.md](chunk-01.md): PRs #32666 to #32197
- [chunk-02.md](chunk-02.md): PRs #32194 to #26324
- [chunk-03.md](chunk-03.md): PRs #24202 to #19585

The cross-batch catalogue is at [catalogue.md](../../catalogue.md). This day contributes 12 rows.
