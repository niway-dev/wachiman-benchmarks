# How the first batch was mined (2026-11-26)

Read-only: `gh` reads and git fetches of `refs/pull/<n>/head` into a local clone. A Sonnet 5.5 medium worker ran the
mining, and a Sonnet 5.5 high worker verified the 27 rows Wachiman did not catch. The scripts are in
[`scripts/mining/`](scripts/mining/); they are throwaway and expect `AO_CLONE` and a scratch directory.

Funnel
- 200 merged PRs listed (newest first, back to PR ~8700). Kept: base main, changedFiles <= 40, additions <= 3000, minus #9068 -> 181 scanned.
  Dropped: 11 non-main base, 11 over size limits (some overlap), #9068 excluded.
- 107 of 181 had at least one top-level inline CodeRabbit comment (322 comments: 274 Minor, 48 Major; the inline severity labels are only Minor/Major).
- 77 PRs had at least one comment with "Addressed in commit"; 43 had >= 2 (the analysis pool).
- Of the 43: 4 dropped as unreachable (8716, 8776, 8889, 9039): every commit CodeRabbit reviewed is absent from refs/pull/<n>/head (history rewritten).
  The shas can still be fetched by hash from GitHub (tested on 8716), so they are recoverable but fragile. 8716 had 10 of 10 comments addressed; worth a second look.
- 39 PRs analysed with a reachable head; 29 have >= 2 admitted owner-accepted findings (candidates.tsv, n_admitted).
- Not admitted: comments created on later commits whose line was already changed relative to the PR's earliest reviewed head ("line changed between head and reviewed commit"),
  or lines not among added lines (omissions, not judged except as noted). This removed most findings from 8732, 8734, 8875, 8874, 9073.

Method notes
- head = earliest commit among CodeRabbit comments' original_commit_id and review commit_ids that is an ancestor of all the others.
- base = merge-base(first parent of the merge commit, head); all diffs sane, base is an ancestor of head, shortstat close to the PR's own diff at that point.
- Admission: comment line (original_line on original commit) mapped to head with diff -U0, then required to be in the added lines of base..head.
- Owner-accepted = "Addressed in commit" marker (fix sha verified to be an ancestor of the PR head), OR a later PR commit changed that exact line.
  The second kind (marked "later" in cases.tsv note) I read for the 7 chosen PRs only; n_admitted in candidates.tsv counts them WITHOUT reading, for the other PRs treat as upper bound.
- Fix sha for "later" rows = oldest commit in head..PR head whose diff changes the removed line text (git log -S); read for correctness, but it is a heuristic.

Surprises / limits
- Only 3 pure-Go PRs reach >= 2 admitted owner-accepted findings (9086, 8720, 9076). Fourth go slot filled by mixed PRs whose findings are Go (9095, 8832).
- Nitpicks and "Outside diff range" items live in review bodies (30 such review bodies in 24 PRs). I did not mine them: no thread URL, no "Addressed" marker. Gap.
- Several PRs merge main into the branch mid-review (8732, 8734); those findings after the merge are not admitted against the earliest head.
- additions/files in the tables are the PR totals from the PR list; the diff at head is smaller (one to two commits in the chosen PRs).
- Not verified: no reviewer was run; golden_cause text is based on reading the code at head and the CodeRabbit text, not on executing anything.

## Verification pass

- 27 rows read at head: 26 real, 1 not (ao-9095-C3: the bot's claim about Claude Code skill naming was wrong, and CodeRabbit withdrew it).
- All 27 defect lines are added lines of base..head.
- Fix sha corrected for ao-9036-C2, ao-9036-C3, ao-9036-C4 (`dbb1c5ff`) and ao-9055-C1 (`dc51ca76`): the heuristic had picked a nearby commit that does not touch the site.
- ao-9086-C1's cause was narrowed: the owned record stays, only the parked record is missing.
