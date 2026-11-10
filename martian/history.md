# History: Wachiman on Martian's 50 PRs

One row per run, newest first. Quality uses our judge route for every row, so rows compare with each
other and with the [reference tools](reference/README.md#same-judge-scores), not with Martian's
stored numbers. Cost is the product's own cost (the reviews), at API list prices; the judge's cost
is in each run's `metrics.json`, under `judge_cost`.

## Quality and product cost

| Run | PRs | High+Critical | Recall | Precision | F1 (All) | F2 (Core) | False positives | Reviews total | $/PR median | $/PR p90 | $/1k changed lines | $/golden found | $/High+Critical found | Partial reviews |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [2026-11-10 · v1.10.0 · Haiku 5.5 high + Opus 5.5 verifier (default)](runs/2026-11-10-v1.10.0-haiku-5-5-high-opus-verifier/README.md) | 50 | 45/66 | 61.3% | 26.0% | 36.5% | 47.0% | 302 | $28.62 | $0.55 | $0.91 | $1.48 | $0.27 | $0.64 | 0 |
| [2026-11-07 · v1.9.0 · Haiku 5.5 · high · arm 1](runs/2026-11-07-v1.9.0-haiku-5-5-high/README.md) | 50 | 47/66 | 64.2% | 26.1% | 37.1% | 49.1% | 314 | $8.98 | $0.10 | $0.35 | $0.46 | $0.08 | $0.19 | 0 |
| [2026-11-07 · v1.9.0 · Opus 5.5 · high](runs/2026-11-07-v1.9.0-opus-5-5/README.md) | 50 | 47/66 | 63.6% | 38.7% | 48.1% | 55.7% | 174 | $25.01 | $0.48 | $0.61 | $1.29 | $0.23 | $0.53 | 0 |

Reference tools, same judge, same 50 PRs (do not change between runs unless the judge route does):

| Tool | High+Critical | Recall | Precision | F1 (All) | F2 (Core) |
| --- | --- | --- | --- | --- | --- |
| qodo-extended-v2 | 44/66 | 56.1% | 63.0% | 59.3% | 60.0% |
| augment | 46/66 | 59.0% | 57.0% | 58.0% | 60.2% |
| claude-code | 29/66 | 44.5% | 45.8% | 45.2% | 44.1% |

Arm 1 (Haiku 5.5 high alone) is done. Planned next rows, one at a time: arm 2 (Opus 5.5 + a findings
falsifier on `fix`/`consider`), arm 3 (Haiku 5.5 high + the same falsifier). Arm 4 (feature-guarantee
falsifier) is measured on kaipu-record. Details and decision rules: [PLAN.md](PLAN.md#planned-arms-test-measures).

## Questions each row answers

- **Did a change help?** Compare F1, F2 and High/Critical with the previous row of the same model.
  A difference of 1 to 3 High/Critical goldens is within one run's variance.
- **Did it get cheaper or dearer?** `$/PR median` and `$/1k changed lines` (the PRs do not change).
- **Is the money buying bugs?** `$/golden found` and `$/High+Critical found`.
- **Is anything cut short?** `Partial reviews` should stay 0; a partial review means the budget ran out.

## What it would cost a person to use Wachiman

An estimate built from two measurements, labelled as such:

| Input | Value | Source |
| --- | --- | --- |
| First review of a PR, typical size | about $0.48 (median), $0.61 at p90 | this bench, v1.9.0, Opus 5.5; PRs average 387 changed lines |
| Per 1,000 changed lines | about $1.29 | this bench |
| Share of a PR's cost spent on re-reviews after pushes | 49% (so about 2× the first review) | [field run](../2026-11-02-field/README.md), kaipu-record, mostly v1.3.0 |

So, at API list prices with Opus 5.5 (an estimate, not a bill):

| Who | Assumption | About |
| --- | --- | --- |
| One PR of ~400 lines, reviewed on every push | first review × 2 | **$1** |
| A developer, 20 such PRs a month | 20 × $1 | **$20 a month** |
| A large feature PR of ~3,500 lines | first review 3.5 × $1.29 | **$4.50** for the first review alone: above the default $3 budget per review (`budget_usd`), so it would end partial unless the budget is raised |
| `wachiman local` on the developer's own Claude subscription | | **$0 in cash**; it uses the subscription's quota |

Not measured yet: re-review cost with v1.9.0 (the 49% is from older versions), Sonnet 5.5 (the
engine's default model) on this bench, and the GitHub Action path.
