# Cross-run analysis of the three Martian runs (2026-11-11)

What the stored data of the three Martian runs says about recall and precision,
computed without any new review or judge call. Input for the design of the next
arms; it makes no product decision.

Sources: `martian/runs/*/data/evaluations/wachiman.json`, the review JSONs,
`martian/reference/evaluations/*`, all on branch `feat/martian-v1-10-0`.
Scripts: `scripts/digest/` (run table, misses, unions, labels) and
`scripts/counterfactuals/` (filters, caps, agreement, Keycloak check). They are
the scratch scripts as run, with absolute paths to the analyst's machine; edit
the paths before re-running.

## Status of each claim

- **[computed]**: recomputed here from the stored JSON.
- **[README]**: taken from a run's README or `history.md`.
- **[external]**: another project's own figure, not re-judged by us.
- Every counterfactual row is a filter applied to the stored Opus run. The
  stored data keeps only each golden's best-matching candidate, so recall under
  a filter is a **lower bound**. Rules chosen by search are **fitted to this
  data** and need a fresh run to confirm.
- Each configuration was run **once**. No replicates exist.

## Blindness note

To classify misses, the analyst read the text of 21 missed goldens in Cal.com
and Sentry only (the repos `PLAN.md` allows tuning on). Grafana, Keycloak and
Discourse goldens remain unread. Tune on Cal.com and Sentry; report on the other
three.

## 1. Runs and re-judged competitors (50 PRs, 173 goldens, 66 High+Critical)

| Run | Reviewer / verifier | Findings (per PR) | TP | FP | R | P | F1 | Core F2 | H+C /66 | Cost total, median per PR |
|---|---|---|---|---|---|---|---|---|---|---|
| v1.9.0 | Opus 5.5 high / none | 273 (5.5) | 110 | 174 | 63.6 | 38.7 | 48.1 | 55.7 | 47 | $25.01, $0.48 |
| arm 1 | Haiku 5.5 high / none | 421 (8.4) | 111 | 314 | 64.2 | 26.1 | 37.1 | 49.1 | 47 | $8.98, $0.10 |
| v1.10.0 | Haiku 5.5 high / Opus 5.5 high | 406 (8.1) | 106 | 302 | 61.3 | 26.0 | 36.5 | 47.0 | 45 | $28.62, $0.55 |

No run combines an Opus reviewer with a second model. [README + computed]

Competitors, same judge route as ours [computed]:

| Tool | Findings (per PR) | TP | FP | R | P | F1 | F2 | H+C /66 |
|---|---|---|---|---|---|---|---|---|
| qodo-extended-v2 | 152 (3.0) | 97 | 57 | 56.1 | 63.0 | 59.3 | 60.0 | 44 |
| augment | 178 (3.6) | 102 | 77 | 59.0 | 57.0 | 58.0 | 60.2 | 46 |
| claude-code | 173 (3.5) | 77 | 91 | 44.5 | 45.8 | 45.2 | 44.1 | 29 |

Cal.com only (10 PRs, 41 goldens, 19 H+C) [README `reference/README.md`]:

| Tool | R | P | F1 | H+C /19 |
|---|---|---|---|---|
| copilot-v2 | 75.6 | 52.5 | 62.0 | 15 |
| coderabbit | 78.0 | 33.3 | 46.7 | 18 |
| bugbot | 43.9 | 51.4 | 47.4 | 12 |
| macroscope | 43.9 | 51.4 | 47.4 | 13 |
| cubic-v2 | 43.9 | 45.0 | 44.4 | 11 |
| wachiman Opus [computed] | 70.7 | 48.3 | 57.4 | — |

crysk, its own run and its own judge, not re-judged by us [external]:
52/66 H+C, precision 28.8%, F1 39.7, 275 FP. Recall derived from F1 and
precision: about 63.9% (about 110 goldens). Not directly comparable with the
rows above: our judge route scores 3.5 to 5.1 F1 lower than Martian's stored
judgments for the same comments.

## 2. Noise

- Judge replicate: claude-code on Cal.com judged twice, 17 vs 18 matches. [README]
- Our judge matches fewer goldens than Martian's stored judgments: claude-code
  77 vs 84, qodo 97 vs 106, augment 102 vs 108. [computed]
- Haiku quasi-replicate (arm 1 vs the v1.10.0 reviewer, different engine
  version): 97 goldens in both, 14 only arm 1, 10 only v1.10.0. [computed]

Bootstrap over PRs, 2,000 resamples, sampling noise only [computed]:

| Quantity | 95% interval |
|---|---|
| Opus recall | 54 to 73 |
| Opus F1 | 41 to 55 |
| Opus minus Haiku F1 | +5 to +16 |
| Opus minus qodo recall | -2 to +17 |
| Opus minus qodo precision | -33 to -17 |

McNemar on goldens found [computed]:

| Pair | Discordant goldens | p |
|---|---|---|
| Opus vs Haiku | 14 vs 15 | 1.0 |
| Opus vs v1.10.0 | 20 vs 16 | 0.62 |
| Opus vs qodo | 30 vs 17 | 0.08 |
| Opus vs augment | 26 vs 18 | 0.29 |

## 3. What Opus missed (63 goldens, 19 H+C) [computed]

| Cut | Counts |
|---|---|
| Severity | Critical 5, High 14, Medium 21, Low 23 |
| Repo | Keycloak 20, Discourse 14, Cal.com 12, Sentry 9, Grafana 8 |
| Martian category | bug 32, doc_defect 6, security 6, style 5, other 14 |
| Found by Haiku / v1.10.0 / either | 15 / 16 / 19 |
| Found by qodo / augment / claude-code / any | 17 / 18 / 11 / 31 |
| Found by any of those five sources | 38 |
| Found by none of them | 25 (12 Low, 8 Medium, 3 High, 2 Critical) |

Of the 19 H+C misses: Haiku found 6, v1.10.0 found 5, competitors 12, nobody 5.

Analyst's classification of the 21 Cal.com and Sentry misses: 7 visible defects
in the changed lines, 6 needing context outside the diff (other implementers,
callers, a framework contract), 8 nits, style, docs or speculative.

## 4. Union of sources [computed]

| Combination | Goldens /173 | H+C /66 |
|---|---|---|
| Opus alone | 110 | 47 |
| Opus ∪ Haiku | 125 (96 both, 14 only Opus, 15 only Haiku) | 53 |
| Opus ∪ v1.10.0 | 126 | 52 |
| All three runs | 129 | 53 |
| Opus ∪ augment | 128 | 57 |
| Opus ∪ three competitors | 141 | 59 |
| All six sources | 148 | 61 |

Opus ∪ Haiku posted as is: 694 findings, precision about 18 to 20%.

## 5. Opus findings by label [computed]

| Severity | Findings | FP | Goldens matched |
|---|---|---|---|
| blocker | 20 | 5 | 16 |
| fix | 103 | 59 | 51 |
| consider | 149 | 109 | 43 |
| info | 1 | 1 | 0 |

| Confidence | Findings | FP | Goldens matched |
|---|---|---|---|
| high | 179 | 101 | 88 |
| medium | 87 | 67 | 22 |
| low | 7 | 6 | 0 |

FP by topic: tests 37 of 45 findings, docs 10 of 12, perf 10 of 13, bug 89 of 155.
FP by repo: Sentry 54 of 78 findings, Keycloak 23 of 33.
PRs with 10 or more findings: 19% precision. PRs with 3 or fewer: 58%.

## 6. Counterfactual filters on the Opus run [computed, recall is a lower bound]

F2 here is over all goldens (56.4 at baseline), not the Core profile (55.7).

| Rule | Kept | TP | FP | R | P | F1 | F2 | H+C /66 |
|---|---|---|---|---|---|---|---|---|
| baseline | 273 | 110 | 174 | 63.6 | 38.7 | 48.1 | 56.4 | 47 |
| confidence at least medium | — | — | — | 63.6 | 39.6 | 48.8 | — | 47 |
| confidence high only | — | — | — | 50.9 | 46.6 | 48.6 | — | 39 |
| severity at least fix | 123 | 67 | 64 | 38.7 | 51.1 | 44.1 | 40.7 | 33 |
| severity at least fix and confidence high | — | — | — | 32.9 | 61.3 | 42.9 | — | 29 |
| topic bug, security or perf only | — | — | — | 49.1 | 44.3 | 46.6 | — | 43 |
| drop tests | 228 | 100 | 137 | 57.8 | 42.2 | 48.8 | 53.8 | 46 |
| drop docs | 261 | 108 | 164 | 62.4 | 39.7 | 48.5 | 56.0 | 46 |
| drop tests+docs | 216 | 98 | 127 | 56.6 | 43.6 | 49.2 | 53.4 | 45 |
| drop tests+docs, only consider/info | 228 | 102 | 135 | 59.0 | 43.0 | 49.8 | 54.9 | 45 |
| drop cleanup | 249 | 99 | 160 | 57.2 | 38.2 | 45.8 | 52.1 | 45 |
| drop question | 265 | 108 | 169 | 62.4 | 39.0 | 48.0 | 55.7 | 47 |
| best-F1 topic×severity cells (fitted) | 214 | 101 | 123 | 58.4 | 45.1 | 50.9 | 55.1 | 45 |
| top 3 per PR | 134 | 75 | 66 | 43.4 | 53.2 | 47.8 | 45.0 | 37 |
| top 4 per PR | 170 | 91 | 89 | 52.6 | 50.6 | 51.6 | 52.2 | 41 |
| top 5 per PR | 201 | 98 | 114 | 56.6 | 46.2 | 50.9 | 54.2 | 43 |
| top 6 per PR | 222 | 106 | 127 | 61.3 | 45.5 | 52.2 | 57.3 | 46 |
| top 8 per PR | 251 | 110 | 152 | 63.6 | 42.0 | 50.6 | 57.7 | 47 |
| top 10 per PR | 260 | 110 | 161 | 63.6 | 40.6 | 49.5 | 57.1 | 47 |
| blocker+fix, no consider | 123 | 67 | 64 | 38.7 | 51.1 | 44.1 | 40.7 | 33 |
| blocker+fix, 1 consider per PR | 169 | 85 | 92 | 49.1 | 48.0 | 48.6 | 48.9 | 39 |
| blocker+fix, 2 consider per PR | 208 | 98 | 121 | 56.6 | 44.7 | 50.0 | 53.8 | 46 |
| blocker+fix, 3 consider per PR | 234 | 105 | 141 | 60.7 | 42.7 | 50.1 | 56.0 | 46 |
| blocker+fix, 5 consider per PR | 258 | 109 | 160 | 63.0 | 40.5 | 49.3 | 56.7 | 47 |
| Haiku echo ±5 lines | 194 | 97 | 107 | 56.1 | 47.5 | 51.5 | 54.1 | 41 |
| Haiku echo ±10 lines | 213 | 104 | 120 | 60.1 | 46.4 | 52.4 | 56.8 | 45 |
| Haiku echo, same file | 248 | 105 | 153 | 60.7 | 40.7 | 48.7 | 55.3 | 46 |
| blocker/fix kept, consider/info need echo ±10 | 229 | 106 | 134 | 61.3 | 44.2 | 51.3 | 56.9 | 46 |
| echo ±10 + top 6 | 183 | 100 | 94 | 57.8 | 51.5 | 54.5 | 56.4 | 44 |
| echo ±10 + top 8 | 201 | 104 | 108 | 60.1 | 49.1 | 54.0 | 57.5 | 45 |
| consider needs echo ±10 + top 6 | 197 | 102 | 106 | 59.0 | 49.0 | 53.5 | 56.7 | 45 |
| echo ±10 + 3 consider per PR | 187 | 99 | 99 | 57.2 | 50.0 | 53.4 | 55.6 | 44 |

"Top N" ranks by severity, then confidence, then original order. "Echo" keeps an
Opus finding only if the Haiku arm-1 run has a finding in the same PR and file
within the given distance. No label threshold alone lifts F1 above 48.8.

Split sample (A = Cal.com + Sentry, 77 goldens; B = Grafana + Discourse +
Keycloak, 96 goldens):

| Rule | A: kept / TP / FP | A: R / P / F1 | B: kept / TP / FP | B: R / P / F1 |
|---|---|---|---|---|
| baseline | 136 / 56 / 85 | 72.7 / 39.7 / 51.4 | 137 / 54 / 89 | 56.2 / 37.8 / 45.2 |
| echo ±10 + top 6 | 83 / 49 / 39 | 63.6 / 55.7 / 59.4 | 100 / 51 / 55 | 53.1 / 48.1 / 50.5 |
| echo ±10 + top 8 | 95 / 51 / 49 | 66.2 / 51.0 / 57.6 | 106 / 53 / 59 | 55.2 / 47.3 / 51.0 |
| consider needs echo + top 6 | 91 / 50 / 46 | 64.9 / 52.1 / 57.8 | 106 / 52 / 60 | 54.2 / 46.4 / 50.0 |
| echo ±10 alone | 102 / 51 / 56 | 66.2 / 47.7 / 55.4 | 111 / 53 / 64 | 55.2 / 45.3 / 49.8 |
| top 6 alone | 101 / 54 / 52 | 70.1 / 50.9 / 59.0 | 121 / 52 / 75 | 54.2 / 40.9 / 46.6 |
| fitted cells | 109 / 52 / 62 | 67.5 / 45.6 / 54.5 | 105 / 49 / 61 | 51.0 / 44.5 / 47.6 |

v1.10.0 run, same exercise:

| Keep | R | P | F1 | H+C |
|---|---|---|---|---|
| all | 61.3 | 26.0 | 36.5 | 45 |
| drop info | 57.2 | 26.3 | 36.1 | 43 |
| confidence high only | 47.4 | 30.1 | 36.9 | 31 |
| severity at least fix | 32.9 | 41.0 | 36.5 | 30 |
| Important tier only | 32.9 | 41.6 | 36.8 | 30 |
| topic bug, security or perf | 43.4 | 35.7 | 39.2 | 37 |

## 7. Per repo, recall / precision [computed]

| Repo | Opus | qodo | augment |
|---|---|---|---|
| Cal.com | 71 / 48 | 51 / 57 | 68 / 55 |
| Sentry | 75 / 33 | 56 / 69 | 58 / 58 |
| Discourse | 66 / 41 | 54 / 58 | 59 / 60 |
| Grafana | 68 / 39 | 68 / 63 | 64 / 62 |
| Keycloak | 33 / 30 | 57 / 74 | 43 / 50 |

Candidate-level precision (findings that are not FP over findings): qodo 62.5%,
augment 56.7%, Opus 36.3%.

## 8. The verifier in v1.10.0 [computed]

| Verifier outcome | Findings | FP among them |
|---|---|---|
| kept | 339 | 246 |
| moved down | 51 | 41 |
| inconclusive | 11 | 11 |
| dropped | 14 | 13 |

The Opus verifier marked 287 of the 302 FP "supported". Hypothesis, not audited:
most FP are true observations that the golden set does not contain, not false
claims, so a verifier that looks for a disproof cannot remove them.

## 9. Duplicates and concentration of FP (Opus) [computed]

- 41 of 174 FP sit in the same PR and file within ±10 lines of another Opus
  finding; 19 of those are next to a finding that matched a golden.
- 14 findings matched two goldens each. 3 candidates matched a golden but lost
  to a better candidate (inferred).
- FP per PR: 0 in 7 PRs, 1 in 6, 2 in 6, 3 in 11, 4–5 in 10, 6–9 in 8, 10+ in 2.
- The 10 noisiest PRs hold 78 of 174 FP (44.8%).
- Findings per PR vs changed lines: Pearson 0.63, Spearman 0.55.

## 10. Harness defect: two Keycloak PRs reviewed on the wrong commits [computed]

| PR | Upstream title | What Wachiman was given |
|---|---|---|
| keycloak 37634 | Implement access token context encoding framework | head `eafbc4e` "Bump cypress-io/github-action from 6 to 7" (2026-03-11), 1 file, 1 line |
| keycloak 36880 | Add Client resource type and scopes to authorization schema | head `f09d73d` "Bump manusa/actions-setup-minikube…" (2026-03-11), 1 file, 3+/3- |

The SHAs in `worklist.tsv` for these two rows point at the fork's later
Dependabot commits, not at the benchmark PR. All three runs scored 0 of their 9
goldens (6 H+C) without seeing the code. The published numbers stand as
measured; the correction is to re-run those two PRs on the right range and
report both figures. Excluding the two PRs from every row: Opus R 67.1, P 38.7,
F1 49.1, H+C 47/60; qodo R 56.1, P 61.7, F1 58.8; augment R 60.4, P 57.2,
F1 58.8.

## 11. How the scoring treats a finding [computed from `step3_judge_comments.py`]

- Each golden takes its single best-matching candidate. TP is goldens matched,
  so one finding that covers two bugs counts as 2 TP.
- FP is candidates that were never the best match of any golden. A second
  finding about the same golden usually counts as FP.
- FP is not filtered by profile: a style or test comment costs precision even
  under the Core profile.

## 12. Open items

- No replicates of any configuration.
- The two Keycloak PRs above.
- No manual audit of the FP (false claim, true but minor, duplicate, real bug
  outside the golden set).
- Planned arms in `PLAN.md`: Opus reviewer with Haiku and Sonnet verifiers,
  Opus medium.
- Product defects still open: 60 s snapshot timeout
  (`src/connectors/local-git.ts`), `--max-depth` cap.
