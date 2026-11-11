# Did other tools raise the findings the benchmark counts against us? (2026-11-11)

Question: the 85 audited Opus findings the judge matched to no golden (Cal.com, Sentry): did other reviewers find
them too, or do they skip them?

## Answer

**Other tools raise most of our unlisted real defects and about half of our minor findings; the best-ranked tools
raise the defects and almost none of the minor ones. [measured by text matching, one model pass, 8 matches read by
hand and all 8 correct]**

| Auditor verdict on our finding | findings | raised by at least one of ten other tools | by three or more | by none |
|---|---|---|---|---|
| real-defect | 34 | 25 | 15 | 9 |
| real-minor | 47 | 24 | 8 | 23 |
| wrong or unverifiable | 4 | 0 | 0 | 4 |

- The golden set misses real defects that several tools find independently: 15 of our 34 were raised by three or more
  other tools. Those comments count as false positives for them as well.
- The top of the leaderboard filters minor findings. `qodo-extended-v2` (best F1, 50 FP on 50 PRs) raised 11 of our 34
  real defects and 2 of our 47 minor ones; `augment` 9 and 3. `coderabbit` and `copilot-v2` (194 and 168 FP) raised 12
  minor ones each.
- Published totals on the 50 PRs, from Martian's results (judge Opus 4.5): qodo-extended-v2 106 goldens and 50 FP,
  cubic-v2 108 and 65, augment 108 and 70. Wachiman on Opus 5.5 high: 117 goldens and 177 FP. We find more known bugs
  than any of them and write about three times as many comments outside the golden set.
- Martian's methodology says the same about its limits: "The gold set might be incomplete", it "has sparse coverage of
  style issues", and a real issue outside it "is scored as a false positive"
  ([methodology/full.md](https://github.com/withmartian/code-review-benchmark/blob/main/methodology/full.md)).

Reading: the gap to the best tools' precision is mostly the minor findings we post and they do not, plus unlisted real
defects that every tool is charged for. If the audited shares held on all 177 FP (40% real defects, 55% minor), not
posting the minor ones in the main list would leave about 80 FP, near the top tools. That projection is not measured.

Tables: [tables.md](tables.md). Inputs and matches: `input-<repo>.json`, `matches-<repo>.json`.
Reproduce: `scripts/others_inputs.py`, one matching worker per repository, `scripts/others_tables.py`.

## Limits

- Matching is by comment text, done by one model (Sonnet 5.5) in one pass; "same issue" is a judgment. Eight random
  matches were read by hand and were correct; missed matches were not checked, so "raised by none" is an upper bound.
- Ten tools of the 49 in Martian's results, chosen as the best-ranked versions plus CodeRabbit, Copilot and Claude Code.
- Whether a top tool did not find a minor issue or found it and withheld it cannot be told from published comments.
- Two repositories of five; the other tools' numbers come from Martian's judge runs, not from ours.
