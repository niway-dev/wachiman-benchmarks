# Audit of the judge's false positives on Cal.com and Sentry (2026-11-11)

Question: are the Opus findings that the judge matched to no golden ("FP") wrong, or true observations the golden
set does not contain? Scope: Cal.com (31 FP on 9 PRs) and Sentry, both sets (54 FP on 9 PRs): 85 of the 177 FP.

## Answer

**The FP are almost never false claims; about 40% are real defects the golden set lacks, and most of the rest are
true but minor. [measured, one model auditor, no human check]**

| Repository | audited FP | real-defect | real-minor | wrong | unverifiable |
|---|---|---|---|---|---|
| Cal.com | 31 | 17 | 14 | 0 | 0 |
| Sentry | 54 | 17 | 33 | 2 | 2 |
| Both | 85 | 34 (40%) | 47 (55%) | 2 (2%) | 2 (2%) |

What follows for the next iterations:

1. **Martian's precision is a floor.** On these two repositories the benchmark counts 49 of 134 Opus findings as
   right (37%). Adding the 34 audited real defects gives 83 of 134 (62%). The benchmark stays useful as a list of
   known bugs to measure recall against; its FP count is not a count of wrong comments.
2. **The noise is minor comments, not hallucinations.** 2 of 85 audited FP were wrong. 47 were true and minor (style,
   docs, test gaps, unlikely edge cases). The work is ordering and sectioning those, not making the reviewer more
   cautious.
3. **A score separates serious from minor better than line proximity to a Haiku review.** With "serious" = matched a
   golden or audited real-defect (83) and "not serious" = the other audited FP (51): AUC 0.83 for the Opus scorer,
   0.83 for the Haiku scorer, 0.78 for Wachiman's own severity, 0.63 for the Haiku echo. This reverses the reading of
   Experiment A, which scored the same signals against the judge's labels only.
4. **Haiku is enough as the scorer.** Same AUC as Opus at about one twentieth of the cost ($0.009 against $0.19 per PR).
5. **No single rule is clean.** "Severity is blocker or fix" keeps 55 serious and 6 not serious in the main section but
   sends 28 serious findings to the second section (mostly goldens Wachiman labelled `consider`). "Haiku scorer gave 5
   or more" keeps 61 and 8, sends 22. The Haiku echo keeps 71 serious but also 30 not serious.

All tables: [tables.md](tables.md). Per-finding rows: [audit.csv](audit.csv).

## Method

One `gpt-6.1-sol` child (Codex, reasoning effort high) through `delegate_task`, one to three PRs per child, following
[brief.md](brief.md): refute first, then construct the failure, verdict with file and line. It saw all findings of the
PR and the diff, on a checkout of the head commit; it was not told which findings matched a golden and was told not to
read the benchmark's reference data. Inputs come from `scripts/audit_inputs.py <repo>`, verdicts with evidence are in
`outputs/`, and `scripts/audit_tables.py` joins them with `findings-opus.csv` and `findings-haiku.csv`.

## Limits

- One auditor, one pass, no human read the evidence. 80 of 85 verdicts are "high confidence". Cal.com had no `wrong`
  at all, which may be lenient; Sentry had 2 `wrong` and 2 `unverifiable`.
- The auditor is a model from another provider than the reviewer. That reduces shared blind spots; it does not remove
  them.
- "Serious" mixes two sources: goldens were not audited and count as serious whatever their severity; audited FP count
  as serious only when the auditor traced a failing path. The AUC figures inherit that asymmetry.
- Two repositories of five (85 of 177 FP). Discourse, Grafana and Keycloak are not audited.
- Only Opus findings were audited. Nothing here says whether the Haiku reviewer's 331 FP are real defects, minor or
  wrong.
- Cost is not reported by the tool (Codex subscription).
