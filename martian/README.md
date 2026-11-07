# Martian's Code Review Bench: Wachiman, run after run

This section tracks Wachiman on [Martian's offline Code Review Bench](https://github.com/withmartian/code-review-benchmark)
(MIT): 50 public pull requests from five repositories, 173 human-curated golden comments, 66 of
them High or Critical. One run is one row in [history.md](history.md); every run keeps its raw data.

| Page | What it holds |
| --- | --- |
| [history.md](history.md) | One row per run: quality, product cost, cost per bug. Start here |
| [reference/](reference/README.md) | The yardstick: the judge route, its calibration, and competitors re-judged through it |
| [runs/](runs/) | One directory per run: report, metrics, every review, every judgment |
| [PLAN.md](PLAN.md) | The plan and its rules (blind first run, held-out tuning) |
| [scripts/](scripts/) | Everything needed to run and score |

## How a run is measured

1. **Inputs are fixed.** [worklist.tsv](worklist.tsv) pins each PR's base and head commit (Martian's
   own fork of the PR). 25 PRs are a single commit with the head's exact tree on its true merge base,
   because a shallow fetch does not reach the base; the diff is the pull request's.
2. **Wachiman reviews locally:** `wachiman local --format json`, the owner's Claude subscription,
   `AGENT_REVIEW_BUDGET_USD=10`, `--max-depth 1000`, snapshots on a RAM disk.
3. **Every finding is one candidate** (title and body), because the Action posts every finding.
4. **Martian's own dedup and judge steps score it**, with Claude Opus 4.5, through
   [`judge_shim.py`](scripts/judge_shim.py) (the Claude Code CLI instead of Martian's paid gateway).
5. **Two views of quality:**
   - **All profile, F1** (precision and recall weighted equally) and High/Critical goldens found.
   - **Core profile, F2** (recall weighted four times precision): the metric
     [Martian's site](https://codereview.withmartian.com/) ranks by.
6. **Only same-judge comparisons are claims.** Our judge route is stricter than Martian's stored
   judgments (see [reference/](reference/README.md)), so Wachiman is compared with the reference
   tools re-judged through the same route, never with Martian's stored numbers directly.

## Rules

- **Blind.** Whoever tunes Wachiman does not read golden contents. Scripts read structure,
  severity and category only.
- **Held out.** A change tuned on this bench is tuned on Cal.com and Sentry only; the claim is what
  it does on Grafana, Keycloak and Discourse.
- **One variable per arm.** A model mix, a falsifier or a prompt change is its own labelled run.
- **One run is not a rank.** Run-to-run variance is 1 to 3 High/Critical goldens; a rank needs
  three runs of the same configuration.
- **Not on Martian's leaderboard.** Listing needs about 600 to 1,000 reviewed public PRs and a run by
  Martian itself.

## Weekly run

```sh
# from this directory, on the owner's laptop, signed in to ~/.wachiman/claude-personal
caffeinate -i scripts/run-weekly.sh 2026-11-14-v1.10.0-opus-5-5            # model and effort optional
EXTRA_ENV="AGENT_REVIEW_X=1" caffeinate -i scripts/run-weekly.sh <label>    # an arm
```

It runs two review queues at a time (two Opus sessions) and at most eight judge calls in flight,
then writes `runs/<label>/` and prints the row for [history.md](history.md). About 1.5 hours.
First used end to end for arm 1 on 2026-11-07: 50 of 50 reviews on the first attempt, no judge errors, about 3 h 10 min with Haiku.

**Bootstrap the cache** (`~/.cache/wachiman-martian`, once per machine): clone Martian's benchmark
into `martian-upstream/`, create `venv/` with `openai tqdm aiohttp requests`, then
`scripts/fetch.sh` and `scripts/flatten.sh` per repository into `repos/` (lists in
[reference/shas/](reference/shas/)).

## What a run costs

| Cost | Paid by | 2026-11-07 run, API-list-price estimate |
| --- | --- | --- |
| **Product**: Wachiman's reviews | what a user would pay | $25.01 for 50 PRs |
| **Measurement**: judging Wachiman's findings | only us | about $27 |
| **Measurement**: re-judging competitors | only us, once per judge route | about $94, done |

All of it came out of the owner's Claude subscription: $0 in cash. The estimate is the CLI's
`total_cost_usd` at API list prices. The judge is expensive because each CLI call carries about
6,300 tokens of the CLI's own prefix for a 670-token prompt; calling the API directly would cost an
estimated $7 for judging Wachiman, not $27.
