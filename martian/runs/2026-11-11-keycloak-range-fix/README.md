# Keycloak range fix: two PRs re-run on the Opus 5.5 baseline

- **Date:** 2026-11-11
- **What ran:** only Keycloak PRs 37634 and 36880, with the baseline's configuration: Wachiman v1.9.0
  (pinned with `WACHIMAN_DIR`, a `git archive v1.9.0` export), `claude-opus-5-5`, effort `high`, no verifier,
  `--profile isolated:personal`, one review at a time. Judged by the same route as the stored runs
  (Martian's dedup and judge steps, Claude Opus 4.5, through `scripts/judge_shim.py`).
- **Stored data of the original runs is untouched.** This directory holds the new reviews
  ([data/reviews/keycloak/](data/reviews/keycloak/)), judgments ([data/evaluations/](data/evaluations/)),
  [metrics.json](metrics.json) (the two re-runs only), [totals.json](totals.json) (the replaced 50-PR totals)
  and `run.log`. No golden comment text was read or printed; counts and ids only.

## What was wrong

`worklist.tsv` reviewed the wrong commits for these two PRs, in all three stored runs:

| PR | Stored head | What that commit is | Goldens matched |
| --- | --- | --- | --- |
| 37634 "Implement access token context encoding framework" | `eafbc4e` | "Bump cypress-io/github-action from 6 to 7", 1 file, +1/-1 | 0 of 4 |
| 36880 "Add Client resource type and scopes to authorization schema" | `f09d73d` | "Bump manusa/actions-setup-minikube from 2.13.1 to 2.16.1", 1 file, +3/-3 | 0 of 5 |

## Root cause

`fetch.sh` assumed that PR #1 of every benchmark fork is the reviewed pull request. That holds for all
forks except the `claude-code` forks of these two PRs: Dependabot opened its own PR #1 there on
2026-03-11, minutes after the fork was created, and the benchmark's PR was never created in them (they hold
only Dependabot PRs). The script took Dependabot's base and head SHAs without checking the title or the
size, and the review ran on a one-line workflow change. The other seven `claude-code` Keycloak forks, and
every other fork, have the benchmark PR as #1. The same two PRs exist correctly in the other tools' forks
(`keycloak__keycloak__augment__PR<n>__20260122`: PR #1, same base, same head as the original PR).

## Correction

| PR | Base | Head | Fork | Range reviewed |
| --- | --- | --- | --- | --- |
| 37634 | `c22f76867f59` (also the merge base) | `daffb05b5ad0` | `keycloak__keycloak__augment__PR37634__20260122` | 28 files, +722/-26 |
| 36880 | `b7b84d75d16e` (merge base, from GitHub's compare API) | `95d5490bb0cc` (one commit: tree of `1950a511026d` on the merge base, message = PR title) | `keycloak__keycloak__augment__PR36880__20260122` | 10 files, +866/-138 |

Verification against `keycloak/keycloak` #37634 and #36880 (read-only `gh api`): the original PRs have the
same head SHAs as those forks' PR #1 (36880's reviewed head is a flattened commit with that head's tree), the
same file list, and the same
additions and deletions. `scripts/check_worklist.py` runs this test on every row: the stored range's files
and line counts against the original PR, and the fork's PR #1 title against the original's. Result on
the old worklist: 48 of 50 rows match, exactly these two fail. On the new worklist: 50 of 50 match.

Also changed: `scripts/fetch.sh` now skips a fork whose PR #1 does not have the original PR's title and file
count; `scripts/run-weekly.sh` gained `ONLY` (run a subset of rows) and documents `WACHIMAN_DIR` (pin a version);
`reference/shas/keycloak*.shas` carry the corrected rows.

## Results of the re-run

| PR | Findings | Goldens matched | High/Critical matched | False positives | Cost (estimate) |
| --- | --- | --- | --- | --- | --- |
| 37634 | 5 (3 fix, 2 consider) | 4/4 | 2/2 | 1 | $0.57 |
| 36880 | 5 (2 fix, 3 consider) | 3/5 | 2/4 | 2 | $0.91 |
| **Both** | 10 | **7/9** | **4/6** | **3** | **$1.47** (original runs: 0 findings, $0.22) |

Judging cost: 47 calls, about $0.81 (all on the subscription, $0 in cash). No judge errors, no partial review.
Reviews took 1.4 min each.

## Totals for the 50 PRs, Opus 5.5 v1.9.0 baseline, with these two PRs replaced

Martian's "All" profile, our judge route:

| | Recall | Precision | F1 | High+Critical | TP | FP | FN | Core F2 | Reviews total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Original | 63.6% | 38.7% | 48.1% | 47/66 | 110 | 174 | 63 | 55.7% | $25.01 |
| Replaced | 67.6% | 39.8% | 50.1% | 51/66 | 117 | 177 | 56 | 58.4% | $26.26 |

Keycloak (including keycloak-greptile) goes from TP 10, FP 23, FN 20 to TP 17, FP 26, FN 13: the
"Keycloak is the weak spot" reading in the original report was partly this defect.

## Limits

- One re-run of two PRs; run-to-run variance is 1 to 3 High/Critical goldens, so the +4 is not
  all signal. The 0 of 9 before was certain (the reviewer saw a different change), the 7 of 9 now is one sample.
- The Claude Code CLI was 2.1.321 here and 2.1.319 in the original review (same Wachiman v1.9.0, model and effort).
- The Haiku arm (2026-11-07) and the v1.10.0 Haiku+Opus verifier run (2026-11-10) used the same worklist and
  have the same two zero rows. They are not re-scored here; their totals are understated the same way.
