# Wachiman vs CodeRabbit on kaipu-record, 2026-11-06

## One-minute block

- **Scope:** niway-dev/kaipu-record #538-#543 and #545-#549 (#544 is not a pull request). Both tools ran live in CI on commits pushed during the local day of 2026-11-06.
- **Pairs:** 14 commits both tools finished. **Special cases:** 22 (0 refused, 3 partial, 4 skipped, 15 unpaired). **Comparable findings:** Wachiman 18, CodeRabbit 10.
- **Verdicts on the 28 paired findings:** 6 verified by reading the code, 10 owner-accepted (the file changed after the comment; the line was not compared), 12 unverified and not scored.
- **What CodeRabbit found that Wachiman did not:** one verified defect, a failed settings save that leaves the in-memory hidden-tracks list ahead of the stored one (#542, low). Four more CodeRabbit-only findings were fixed by the owner afterwards (#543: focus ring, "Move to workspace" check, navigation order; #548: test timers). Wachiman reported nothing on those commits.
- **What Wachiman found that CodeRabbit did not:** a verified defect where a copy of a copy shows its parent as "Original" (#543, medium), and two verified low findings (#539 stale comment, #548 stale summary under a throttled drag).
- **Found by both:** the screenshot zoom-out that enlarges and crops tall images (#543, verified) and the history arrows missing pushes while unmounted (#545, owner-accepted).
- **Basis:** all rows are `live`; no laptop reruns. Wachiman version seen: v1.8.0 on every row (Claude Opus 5.5, high effort), from `pairs.csv`.
- **Judge:** claude-sonnet-5-5.

## Pairs


| PR | Commit | Wachiman version | Model · effort | Wachiman cost | Wachiman findings | coderabbit findings | Minutes apart |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #538 | `7535940` | v1.8.0 | Claude Opus 5.5 · high | $0.34 | 2 | 0 | 4 |
| #538 | `6c2ccf6` | v1.8.0 | Claude Opus 5.5 · high | $0.26 | 0 | 0 | -2 |
| #539 | `e41c267` | v1.8.0 | Claude Opus 5.5 · high | $0.54 | 1 | 0 | 4 |
| #539 | `1e34f38` | v1.8.0 | Claude Opus 5.5 · high | $0.11 | 0 | 0 | 0 |
| #541 | `6e2fe35` | v1.8.0 | Claude Opus 5.5 · high | $0.38 | 0 | 1 | 309 |
| #542 | `1e7cf17` | v1.8.0 | Claude Opus 5.5 · high | $0.38 | 0 | 1 | 12 |
| #543 | `d70421e` | v1.8.0 | Claude Opus 5.5 · high | $2.50 | 8 | 5 | 0 |
| #543 | `b579b7b` | v1.8.0 | Claude Opus 5.5 · high | $0.61 | 2 | 1 | 0 |
| #543 | `c2e1feb` | v1.8.0 | Claude Opus 5.5 · high | $0.67 | 0 | 0 | 0 |
| #543 | `4fb9bbb` | v1.8.0 | Claude Opus 5.5 · high | $0.32 | 1 | 0 | 0 |
| #543 | `b66e9ff` | v1.8.0 | Claude Opus 5.5 · high | $0.14 | 0 | 0 | 1 |
| #545 | `d728849` | v1.8.0 | Claude Opus 5.5 · high | $0.38 | 2 | 1 | 1 |
| #545 | `2b5ffdd` | v1.8.0 | Claude Opus 5.5 · high | $0.21 | 0 | 0 | 3 |
| #548 | `151d8a8` | v1.8.0 | Claude Opus 5.5 · high | $0.32 | 2 | 1 | 1 |

| PR | What Wachiman posted | What CodeRabbit posted | Verdicts |
| --- | --- | --- | --- |
| #538 | `7535940`: 2 notes (button label for assistive tech, missing rename test) | nothing | both unverified |
| #539 | `e41c267`: stale comment about stable callbacks | nothing | verified, low |
| #541 | nothing | `6e2fe35`: `setSize` vs `setContentSize` in a verify script | unverified (depends on the window's frame settings) |
| #542 | nothing | `1e7cf17`: `latest` is not reset when a save fails | verified, low |
| #543 | `d70421e`: 8 (copy-of-copy "Original", zoom-out crop, nav order, a11y, tests, dead strings); `b579b7b`: 2; `4fb9bbb`: 1 | `d70421e`: 5 (path traversal, focus ring, movability, zoom-out, nav order); `b579b7b`: 1 | 1 matched pair, see Gaps |
| #545 | `d728849`: forward arrow stale after a sign-in round trip; a test that never clicks Back | the same stale-arrow defect | matched, owner-accepted |
| #548 | `151d8a8`: throttled preview drops the trailing value; a test that only checks "not empty" | fake timers not restored | 1 verified (Wachiman), 1 accepted (CodeRabbit) |

## Gaps

Findings only CodeRabbit made, verified or accepted:

1. **#542, `use-hidden-tracks.ts:44` (verified, low, difficulty 3).** `write()` stores the new list in `latest.current` before the save finishes. If the save is rejected, the catch only reports the error, so the next toggle starts from a list the settings never stored. CodeRabbit named the fix (reset `latest` on a refused save). Wachiman posted nothing on this commit, so the gap is a miss, not a refusal.
2. **#543 `d70421e`, three accepted findings (low, difficulty 2-3):** focus indicator on menu items, "Move to workspace" offered without a movability check, navigation order not filtered by library. The owner changed those files in `b579b7b`. Wachiman's own 8 findings on that commit did not include them.
3. **#548 `151d8a8`, fake timers not restored (accepted, low).** The owner changed `inspector.test.tsx` afterwards.

Not a gap, unverified: the path-traversal finding on #543 (`index.ts` was not changed afterwards; only a test was added) and the `setSize` finding on #541.

Why CodeRabbit found them is not recorded here: `findings.csv` carries no posted commands or cited files for it, so I do not claim a reason.

## Special cases

Ordered by what was lost. No Wachiman review was refused.

1. **Partial (3):** #540 `8c060a0`, `dbdc479`, `a61a20c`. Wachiman did not review some files; the same last commit was skipped by CodeRabbit's path filters.
2. **Skipped (4), all CodeRabbit:** #540 `a61a20c` and #549 `0d43662` (path filters); #546 `6d2bf6a` and #547 `f398f90` (auto reviews are off on non-default base branches, i.e. stacked PRs).
3. **Unpaired (15):** Wachiman only, 12 commits: CodeRabbit never reviewed them (#539, #541, #542 x3, #543, #546 `55ae970` and `93a721a`, #547 `ca5cef4`, #549), or skipped them (#546 `6d2bf6a`, #547 `f398f90`, listed above as skipped). CodeRabbit only, 3 commits: the last commit of #538 (`04fc9ee`), #543 (`9513ede`) and #548 (`51b6826`). Wachiman did not review those head commits, and I did not find out why.

Full table: `pairs/special-cases.csv`.

## Cost

- Wachiman on the 14 pairs: **$7.16** (`pairs.csv`). One commit, #543 `d70421e`, is $2.50 of it.
- CodeRabbit: **not published**.
- Wachiman's cost on unpaired and partial commits is in `pairs/reviews.csv` and is not included above.

## Limits

- One day, one repository, 11 pull requests; #538-#540 overlap with the range in draft PR #12 (#534-#540).
- Single judge (claude-sonnet-5-5). "Verified" means I read the code at that commit; **owner-accepted compares files, not lines**, so an accepted finding may have been fixed for a different reason.
- 12 of 28 paired findings are unverified and not scored, including most of Wachiman's test-quality and accessibility notes.
- Several PRs were still open and updated after 05:00Z (midnight local), so pairs for #546-#549 may change.
- Difficulty and severity are my judgement. The day's severity labels from the tools are in `findings.csv`.
