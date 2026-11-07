# Wachiman on Martian's Code Review Bench, first blind run

- **Date:** 2026-11-07
- **What ran:** Wachiman v1.9.0 as released, `claude-opus-5-5`, effort `high`, `wachiman local`, one run
  over all 50 pull requests of [Martian's offline Code Review Bench](https://github.com/withmartian/code-review-benchmark)
  (MIT; 5 repositories, 173 human-curated golden comments, 66 of them High or Critical).
- **Judge:** Martian's own dedup and judge steps, unmodified, with Claude Opus 4.5 (the judge of
  Martian's stored evaluations), reached through the Claude Code CLI on a subscription. See
  [Calibration](#calibration-our-judge-route-is-stricter).
- **Blind:** nobody read the golden comments' contents before or during the run. The harness reads
  only their structure and severity.
- **Plan and rules:** [PLAN.md](PLAN.md). **Raw data:** [data/](data/). **Scripts:** [scripts/](scripts/).

## In one minute

Same judge for every row, 50 PRs, Martian's "All" profile and counting:

| # | Tool | High+Critical found | Recall | Precision | F1 | TP | FP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | qodo-extended-v2 | 44/66 | 56.1% | 63.0% | 59.3% | 97 | 57 |
| 2 | augment | 46/66 | 59.0% | 57.0% | 58.0% | 102 | 77 |
| 3 | **wachiman 1.9.0 · Opus 5.5** | **47/66** | **63.6%** | 38.7% | 48.1% | 110 | 174 |
| 4 | claude-code | 29/66 | 44.5% | 45.8% | 45.2% | 77 | 91 |

- **Wachiman finds the most.** Highest recall and the most High/Critical goldens of the four.
- **Wachiman is loud.** Precision is the lowest of the four: 174 false positives against 57 to 91.
  That is what puts it third on F1.
- **Where it would sit on Martian's published table** is an estimate, not a measurement: our judge
  route scores the three reference tools 3.5 to 5.1 F1 points below Martian's stored scores. Shifted
  by that much, Wachiman's F1 would be about 51 to 53, between bugbot (50.8) and macroscope (53.5) on
  the stored table below, about 6th of the leading eleven, and near the top on High/Critical recall. Only Martian running the pipeline itself would settle it.

## Martian's stored table, for reference

Martian's own stored Opus 4.5 evaluations, scored with the same script (`scripts/score.py`), 50 PRs.
These rows use Martian's judge route, not ours, so Wachiman is **not** in this table. The script
reproduces the numbers crysk quotes for these rows exactly (for example augment 49/66, 62.4%, 60.7%,
61.5%), which checks that the counting matches Martian's.

| # | Tool | High+Critical found | Recall | Precision | F1 | TP | FP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | qodo-extended-v2 | 49/66 | 61.3% | 67.9% | 64.4% | 106 | 50 |
| 2 | cubic-v2 | 48/66 | 62.4% | 62.4% | 62.4% | 108 | 65 |
| 3 | augment | 49/66 | 62.4% | 60.7% | 61.5% | 108 | 70 |
| 4 | qodo-v2 | 47/66 | 59.0% | 56.4% | 57.6% | 102 | 79 |
| 5 | macroscope | 42/66 | 46.8% | 62.3% | 53.5% | 81 | 49 |
| 6 | bugbot | 40/66 | 45.1% | 58.2% | 50.8% | 78 | 56 |
| 7 | copilot-v2 | 47/66 | 66.5% | 40.6% | 50.4% | 115 | 168 |
| 8 | claude-code | 35/66 | 48.6% | 48.8% | 48.7% | 84 | 88 |
| 9 | sourcery | 40/66 | 54.9% | 43.2% | 48.3% | 95 | 125 |
| 10 | coderabbit | 42/66 | 59.5% | 34.7% | 43.8% | 103 | 194 |
| 11 | greptile-v5 | 44/66 | 45.1% | 40.2% | 42.5% | 78 | 116 |

crysk reports 52/66, 28.8% precision and F1 39.7 on the same 50 PRs from one unreplicated run of its
own (its `benchmarks/martian/README.md`); its judge route and raw data are not public, so it is not
placed in either table.

## Cal.com: nine tools, same judge

The pilot slice (10 PRs, 41 goldens, 19 High/Critical), with eight leading tools re-judged through
our route:

| # | Tool | High+Critical found | Recall | Precision | F1 | TP | FP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | copilot-v2 | 15/19 | 75.6% | 52.5% | 62.0% | 31 | 28 |
| 2 | augment | 15/19 | 68.3% | 54.9% | 60.9% | 28 | 23 |
| 3 | **wachiman** | 16/19 | 70.7% | 48.3% | 57.4% | 29 | 31 |
| 4 | qodo-extended-v2 | 12/19 | 51.2% | 56.8% | 53.8% | 21 | 16 |
| 5 | macroscope | 13/19 | 43.9% | 51.4% | 47.4% | 18 | 17 |
| 6 | bugbot | 12/19 | 43.9% | 51.4% | 47.4% | 18 | 17 |
| 7 | claude-code | 10/19 | 43.9% | 50.0% | 46.8% | 18 | 18 |
| 8 | coderabbit | 18/19 | 78.0% | 33.3% | 46.7% | 32 | 64 |
| 9 | cubic-v2 | 11/19 | 43.9% | 45.0% | 44.4% | 18 | 22 |

## Where Wachiman's score comes from

By repository (same judge):

| Repository | Language | Precision | Recall | F1 | TP | FP | FN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cal.com | TypeScript | 48% | 71% | 57% | 29 | 31 | 12 |
| Discourse | Ruby | 41% | 66% | 50% | 27 | 39 | 14 |
| Grafana | Go | 39% | 68% | 49% | 17 | 27 | 8 |
| Sentry | Python | 33% | 75% | 46% | 27 | 54 | 9 |
| Keycloak | Java | 30% | 33% | 32% | 10 | 23 | 20 |

By Wachiman's own severity label (a true positive is counted per golden matched, so a finding that
matches two goldens counts twice):

| Severity | Matched a golden | False positives | Precision (approx.) |
| --- | --- | --- | --- |
| blocker | 16 | 5 | 76% |
| fix | 51 | 59 | 46% |
| consider | 43 | 109 | 28% |
| info | 0 | 1 | — |

Two readings, both hypotheses until tested on held-out repositories (PLAN.md, rule 5):

- The severity label carries signal: blockers are rarely wrong. Dropping `consider` findings would
  not help F1, because they hold 43 of the 110 matches.
- Keycloak is the weak spot on both axes: it finds a third of the goldens and is wrong 70% of the time.

## Calibration: our judge route is stricter

Martian's judge calls an OpenAI-compatible gateway (`MARTIAN_API_KEY`). We have no account there, so
`scripts/judge_shim.py` serves the same API locally and forwards each call to `claude -p` with the
same model, system prompt and user prompt, and no tools.

| Check | Result |
| --- | --- |
| claude-code on Cal.com, Martian's stored judgment vs ours, same candidates and dedup | 22 vs 17 matches; 7 of 10 PRs identical; every difference is a match Martian's judge accepted and ours rejected |
| claude-code on Cal.com, our route twice | 17 vs 18 matches; 1 of 41 goldens differs |
| Three reference tools, all 50 PRs, stored vs ours | F1 −3.5 (augment), −5.1 (qodo-extended-v2), −3.5 (claude-code) |

So the route is stable but systematically stricter, probably because the CLI cannot send
`temperature: 0`, or because of the CLI's own framing. That is why the headline table re-judges
the reference tools instead of comparing Wachiman with Martian's stored scores.

## Deviations from Martian's pipeline

| Deviation | Why | Expected effect |
| --- | --- | --- |
| Judge through `claude -p` (Claude Code 2.1.319) on a subscription, not Martian's gateway | No Martian account | Stricter judging; measured above, and applied equally to every row of the headline table |
| Candidates come from Wachiman's JSON, one per finding (title and body), not extracted from posted GitHub comments | `local` posts nothing | Other tools' summary comments pass through an LLM extractor; ours do not. Every finding counts, because the Action posts every finding |
| 25 of 50 PRs reviewed as one commit: the head's exact tree on top of the true merge base (from GitHub's compare API), message = PR title | A shallow fetch did not reach the merge base | Same diff as the pull request; the individual commit messages are not shown to the reviewer |
| `--max-depth 1000` instead of 50 | Some PR branches carry merges from main (97 and 155 commits) | None on what is reviewed |
| `AGENT_REVIEW_BUDGET_USD=10` instead of 3 | Avoid a cut-short Opus review on large PRs | No review was partial; the most expensive was $2.31 |
| `TMPDIR` on a RAM disk, and reviews retried after a timeout | Wachiman's snapshot step timed out on this machine (see below) | None on the review; a failed attempt produced no output |

## Product defects this run found

- **`wachiman local` fails on large repositories when the disk is slow or busy.** The snapshot step
  (`src/connectors/local-git.ts`) runs `tar -xf` and `git add -A -f` with a fixed 60-second timeout
  (`TIMEOUT_MS`). Extracting Grafana's 241 MB head took 85 s on this machine's disk and 4.4 s on a RAM
  disk; `git add -A -f` of Keycloak took 14 s alone and over 60 s with three reviews running. The
  review fails with `spawnSync tar ETIMEDOUT` or `spawnSync git ETIMEDOUT` and nothing is reviewed.
- **The depth cap blocks ordinary PR branches.** A branch that merged main has more commits than the
  default `--max-depth 50` even when the diff is small.

## Cost and time

| | Reviews | Judge |
| --- | --- | --- |
| Calls | 54 provider calls for 50 reviews | 5,211 calls (Wachiman, the calibration, and re-judging eight tools on Cal.com and three on all 50 PRs) |
| API-equivalent estimate | $25.01 total, $0.50 a PR, $2.31 at most | about $124 |
| Paid in cash | $0: Claude subscription | $0: Claude subscription |
| Time | median 1.4 min a PR, 4.4 min at most | median 12 s a call |

273 findings: 20 blocker, 103 fix, 149 consider, 1 info; no review was partial.

## What is not claimed

- **One run.** Run-to-run variance on this benchmark is 1 to 3 High/Critical goldens (crysk's own
  measurement). Two more runs are needed before quoting a rank.
- **No place on Martian's public leaderboard.** That needs about 600 to 1,000 reviewed public PRs and a
  run by Martian.
- **The Action path was not measured.** Martian's official route posts reviews on forked PRs and
  extracts candidates from the comments.
- **Golden quality is Martian's.** At least one golden is known to be wrong (Sentry PR 1, per crysk).

## Reproduce

1. Clone Martian's benchmark; copy `offline/` to a working directory.
2. `scripts/fetch.sh` for each repository (lists in `data/shas/`), then `scripts/flatten.sh` where
   the merge base is not reached.
3. `scripts/seq.sh` runs the reviews (`wachiman local … --format json --profile isolated:personal`).
4. Start `scripts/judge_shim.py`; set `MARTIAN_API_KEY` to any value, `MARTIAN_BASE_URL` to the shim,
   `MARTIAN_MODEL=anthropic/claude-opus-4-5-20251101`.
5. `scripts/to_martian.py`, then Martian's `step2_5_dedup_candidates --tool wachiman` and
   `step3_judge_comments --tool wachiman`.
6. `scripts/score.py` over the evaluation files in `data/evaluations/`.

## Next

1. Two more runs of the same configuration (replicates).
2. The two product defects above.
3. Arms, each its own row and tuned only on Cal.com and Sentry: a verifier on `fix`/`consider`
   findings to cut false positives; the Haiku-proposer/Opus-verifier design; the owner's
   guarantee-refutation review for critical features.
4. The Action path on forked PRs.
