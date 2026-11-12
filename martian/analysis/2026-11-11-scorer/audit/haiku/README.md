# Haiku as the reviewer: are its extra findings noise? (Cal.com, 2026-11-11)

Question: the Haiku reviewer (Wachiman v1.9.0, Haiku 5.5 high, no verifier) has 331 judge FP on 50 PRs against 177
for Opus. Are those wrong, minor, or real? Scope: Cal.com only, 10 PRs, the 67 Haiku findings the judge matched to no
golden. Same auditor and [brief](../brief.md) as the Opus audit.

## Answer

**Haiku's extra findings are not hallucinations: 1 of 67 is wrong. 27 are real defects the golden set lacks, 37 are
true but minor. [measured, one model auditor, one repository, no human check]**

| Reviewer, Cal.com, 10 PRs | findings | matched a golden | FP: real-defect | FP: real-minor | FP: wrong | FP: unverifiable |
|---|---|---|---|---|---|---|
| Opus 5.5 high | 58 | 27 | 17 | 14 | 0 | 0 |
| Haiku 5.5 high | 96 | 29 | 27 | 37 | 1 | 2 |

- Goldens found: Opus 29 of 41 (16 High+Critical), Haiku 28 of 41 (15 High+Critical).
- Serious findings (matched a golden, or audited real-defect): Opus 44 of 58 (76%), Haiku 56 of 96 (58%).
- Minor, wrong or unverifiable: Opus 14, Haiku 40. Haiku writes about three times as many of these.
- Of Haiku's 27 real defects, 14 are not within 10 lines of any Opus finding. Of Opus's 17, 4 are not near any Haiku
  finding. Neither reviewer contains the other.
- Haiku's own severity separates them: blocker or fix is 18 real-defect, 6 real-minor, 1 wrong; consider is
  9 real-defect, 31 real-minor, 2 unverifiable.

Reading: on this repository Haiku finds as many known bugs as Opus and more unlisted real defects, at about one fifth
of the review cost (median $0.10 against $0.48 per PR over the 50 PRs). Its cost is volume: 40 minor comments on 10
PRs against 14. With a scorer that orders or sections minor findings, Haiku as the main reviewer is a candidate
again. This is one repository; it is not a decision.

Tables: [tables.md](tables.md). Per-finding rows: [audit.csv](audit.csv). Verdicts with evidence: `outputs/`.
Reproduce: `scripts/audit_inputs.py cal.com haiku`, then the auditor per PR, then `scripts/audit_haiku.py`.

## Limits

- One auditor (`gpt-6.1-sol`, reasoning effort high), one pass, no human read the evidence.
- One repository, and the one where both reviewers do best. Sentry was harder for Opus (17 real-defect of 54 FP).
- "Real defect" counts findings, not distinct bugs: the auditor marked 2 of 67 as duplicates of another finding, and
  "near" is a line-distance proxy for "same bug".
- Goldens were not audited; they count as serious whatever their severity.
- The scorer was never run on Haiku findings, so nothing here measures how well a score would order them.
- The safety-net idea (Haiku reviews, a second pass catches what it misses) is not tested here.
