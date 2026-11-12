# Sonnet as the reviewer: are its unlisted findings invented? (Cal.com and Sentry, 2026-11-12)

Question: Sonnet 5.5 high finds as many goldens as Opus 5.5 high for about 25% less, with 190 judge false
positives on 50 PRs against 177. Before it becomes the default reviewer: are those findings wrong, minor or real?
Scope: Cal.com and Sentry, 20 PRs, the 97 Sonnet findings the judge matched to no golden, from the run
`runs/2026-11-11-v1.9.0-sonnet-5-5-high`. Same auditor (GPT-6.1 Sol, effort high) and [brief](../brief.md) as the
Opus audit; eight audit tasks in parallel, each blind to the judge and to the other audits.

## Answer

**Sonnet does not invent more than Opus: 2 of 97 are wrong, the same count as Opus (2 of 85). 30 are real defects
the golden set lacks and 60 are true but minor. [measured, one model auditor, one pass, two repositories, no human
check]**

| Reviewer, Cal.com + Sentry, 20 PRs | findings | matched a golden | FP: real-defect | FP: real-minor | FP: wrong | FP: unverifiable | serious (golden + real-defect) |
|---|---|---|---|---|---|---|---|
| Opus 5.5 high | 136 | 49 | 34 | 47 | 2 | 2 | 83 (61%) |
| Sonnet 5.5 high | 150 | 52 | 30 | 60 | 2 | 5 | 82 (55%) |

- Goldens found on these PRs: Sonnet 57, Opus 56 (a finding can match more than one golden).
- By repository, Sonnet: Cal.com 18 real-defect, 22 real-minor, 1 wrong; Sentry 12 real-defect, 38 real-minor,
  1 wrong, 5 unverifiable.
- The difference is minor comments: 60 against 47. Sonnet writes about a quarter more of them.
- Sonnet's own severity separates less sharply than Opus's. Blocker or fix: 18 real-defect, 10 real-minor,
  1 wrong, 2 unverifiable (Opus: 27, 5, 0, 1). Consider: 12 real-defect, 50 real-minor, 1 wrong, 3 unverifiable
  (Opus: 7, 41, 2, 1). So 12 of Sonnet's 30 unlisted real defects sit under `consider`, against 7 of 34 for Opus.

Reading: the risk checked here, that the cheaper model pays for its price with invented findings, did not appear.
What Sonnet adds is volume of minor comments and a weaker severity label, which is the case for a scoring step
after the review rather than against the model.

Not checked: Discourse, Grafana and Keycloak; whether the Haiku scorer separates Sonnet's findings as it does
Opus's (it was measured on Opus findings only); a second auditor or a human on the verdicts.

Per-finding rows: [audit.csv](audit.csv). Verdicts with evidence: `outputs/`. Inputs: `inputs/`
(built by `scripts/audit_inputs.py <repo> sonnet`).
