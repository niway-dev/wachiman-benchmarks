# Plan: Wachiman on Martian's Code Review Bench

A working document, started 2026-11-07. The pull request that ships the replicated result (three
runs of all 50 PRs) deletes it.

**Status (2026-11-07):** the pilot and the first blind run of all 50 PRs are done; results and the
deviations actually applied are in [the run's report](runs/2026-11-07-v1.9.0-opus-5-5/README.md), which supersedes the deviation table below.
Replicates, the Action path and the arms are not started.

## Goal

Find where Wachiman stands against the tools already scored on
[Martian's offline Code Review Bench](https://github.com/withmartian/code-review-benchmark)
(50 public PRs, 5 repositories, human-curated golden comments, LLM judge). Do it in a way anyone can
check: method, deviations, and raw data are in this directory.

## Rules

1. **Blind.** Nobody who tunes Wachiman reads the golden comments' contents. The harness reads only
   their structure. The first number is v1.9.0 as released, not a version tuned on this benchmark.
2. **Same inputs as the other tools.** Each PR is reviewed at the head commit of Martian's own fork
   (`code-review-benchmark/<repo>/pull/1`), against that pull request's base commit.
3. **Same judge as the published table.** Martian's `step3_judge_comments.py`, unmodified, with
   `MARTIAN_MODEL=anthropic/claude-opus-4-5-20251101`, the judge of their stored evaluations.
4. **Every deviation is written down** (below), with its expected effect.
5. **Later tuning is held out.** If a change is tuned on this benchmark, it is tuned on Cal.com and
   Sentry only and reported on Grafana, Keycloak and Discourse.

## Steps

| # | Step | Output |
| --- | --- | --- |
| 1 | Fetch each PR's base and head from Martian's fork (shallow) | `shas/*.tsv` |
| 2 | Calibrate the judge: re-judge one stored tool (`claude-code`, Cal.com) through our judge route; compare TP/FP/FN with Martian's stored Opus 4.5 evaluations | `calibration.md` |
| 3 | Review each PR: `wachiman local --base <base> --format json --profile isolated:personal`, `AGENT_REVIEW_MODEL=claude-opus-5-5` | `reviews/<repo>/<pr>.json` |
| 4 | Map every finding to one Martian candidate (`text`, `path`, `line`) | `candidates-wachiman.json` |
| 5 | Run Martian's step 2.5 (dedup) and step 3 (judge) for tool `wachiman` | `evaluations-wachiman.json` |
| 6 | Score with the same profiles as the published table; place next to the stored rows | `README.md` |

Pilot: Cal.com, 10 PRs, 1 run. Then the other 40 PRs. Then two more runs of all 50 (replicates).
Later: the GitHub Actions path on forked PRs (Martian's official step 0).

## Planned arms (test measures)

Agreed with the owner on 2026-11-07: every arm runs, one at a time, each as its own row in
[history.md](history.md). One variable per arm. The baseline is the 2026-11-07 run (v1.9.0,
Opus 5.5, high).

| # | Arm | Variable | Built from | Question it answers | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Haiku 5.5 high alone | the review model | the product as released: `run-weekly.sh <label> claude-haiku-5-5 high` | How much recall and cost does a cheaper model give on public PRs? | done 2026-11-07: [report](runs/2026-11-07-v1.9.0-haiku-5-5-high/README.md) |
| 2 | Opus 5.5 + a findings falsifier on `fix` and `consider` | a verification pass | a prototype outside the product, over this bench's candidates | Does trying to disprove each finding cut false positives without losing real bugs? | superseded: v1.10.0 ships a verifier; measure it with Opus as reviewer before designing another |
| 3 | Haiku 5.5 high + the same falsifier | the proposer model, falsifier fixed | arms 1 and 2 | Is cheap proposer plus verifier as good as Opus, for less? | **done 2026-11-10 as v1.10.0's default, a clear failure**: [report](runs/2026-11-10-v1.10.0-haiku-5-5-high-opus-verifier/README.md). The verifier dropped 14 of 415 findings; precision stayed at 26%, cost rose to $0.55/PR, above Opus alone |
| 4 | Feature-guarantee falsifier | a review mode for critical features | a design to come | Does stating a documented guarantee and trying to break it find bugs others miss? | measured on kaipu-record, not here: these PRs carry no written guarantees |

### Next arms, agreed 2026-11-11 after the v1.10.0 failure

The reviewer stays Opus 5.5 high: every good number so far is at high, and recall is the
strength to protect. Its 174 false positives are the verifier's job. One variable per arm:

| # | Reviewer | Verifier | Needs first |
| --- | --- | --- | --- |
| 5 | Opus 5.5 high | Haiku 5.5 high | the verifier may drop a finding it finds no supporting evidence for, not only one it disproves |
| 6 | Opus 5.5 high | Sonnet 5.5 medium | the same rule, and a configurable verifier effort (today it is always `high`) |
| 7 | Opus 5.5 medium | the better of 5 and 6 | nothing: measures what medium saves and what recall it costs |

Arms 5 and 6 can reuse the baseline's saved Opus findings instead of reviewing again, so they
compare verifiers without a second generation. The deciding numbers: real bugs dropped by
mistake, false positives removed, verifier cost and time.

Decision rules for every arm, fixed before it runs:

- **Same judge route as the baseline**, and only rows judged that way are compared.
- **A High/Critical difference of 3 or fewer is noise** for a single run; a claim needs replicates.
- **Tuning is held out:** anything adjusted after seeing results is adjusted on Cal.com and Sentry
  only and judged on Grafana, Keycloak and Discourse.
- **Cost is reported with quality:** `$/PR median`, `$/golden found` and `$/High+Critical found`.
- **The falsifier must show its evidence:** the claim, the paths it checked with lines, and the
  counterexample or the disproof. A bare "refuted" or "corroborated" is not accepted. A finding it
  cannot disprove is kept.

## Deviations from Martian's pipeline

| Deviation | Why | Expected effect |
| --- | --- | --- |
| The judge is reached through a local OpenAI-compatible shim that runs `claude -p` (Claude Code 2.1.319) with the same model, the same system and user prompt, no tools, on a Claude subscription. Martian calls its own gateway with `MARTIAN_API_KEY` | No Martian account; the owner's subscription pays | No `temperature: 0` (the CLI has no such option): small judge variance. Measured by step 2 |
| Our candidates come straight from Wachiman's JSON, one per finding, not extracted from posted GitHub comments (step 2) | `local` posts nothing | Other tools' summary comments go through an LLM extractor; ours do not. crysk saw extraction add 17% candidates to its own run |
| Reviews run locally, not as a GitHub App on the forks | Martian's official path needs an installed app per fork; the Action path is a later run | None on the code reviewed: same commits |
| `AGENT_REVIEW_BUDGET_USD=10` instead of the default `3` | Opus on a 40-file PR can exhaust a $3 estimate and leave files unreviewed | Fewer partial reviews; any partial review is listed |

## Not claimed

- A place on Martian's public leaderboard: it requires about 600 to 1,000 reviewed public PRs and a
  run by Martian itself.
- Anything from one run beyond what one run shows. Run-to-run variance on this benchmark is 1 to 3
  High/Critical goldens (crysk's own measurement).
