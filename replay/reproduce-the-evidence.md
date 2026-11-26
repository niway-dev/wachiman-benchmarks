# Reproduce the evidence: why Wachiman 1.20.x found fewer known bugs than 1.4, and why we run Sonnet 5.5 on the subscription token

This guide says how to rebuild every number of this investigation from zero. It links the
reports; it does not repeat their reasoning. Every figure below comes from those reports.

## One-minute summary

**Question.** On the same five kaipu-record pull requests (#463 to #467, 27 known bugs), Wachiman
v1.4.0 caught about 12 known bugs per run and v1.20.1 and v1.21.0 caught 9 to 11. Why? And why does
the release baseline now run Sonnet 5.5 on the subscription token?

**Answer.**

- **The $3 review budget left reviews partial.** From v1.16.0 the engine runs up to 4 batches at
  once, and each reserves its $0.75 cap first. On the biggest pull request (#467, 47 files) the
  last batches found no room and left 8 to 19 files unread. With `budget_usd: 10` no review was
  partial and v1.21.0 caught 32 of 81 known-bug chances, against 27 at $3
  ([budget report](../2026-11-25-v1.21.0-budget-replay/README.md)).
- **The credential cut the turns per batch, not a release.** The same v1.15.0 makes about 15
  turns per batch call on an API key and about 9 on a subscription token
  ([release bisect](../2026-11-26-release-bisect/README.md)). The old comparison mixed credentials:
  v1.4.0 ran on the key, v1.20.1 and v1.21.0 on the token. A plain `claude -p` call with no
  Wachiman reproduces it at the $0.75 batch cap: 15 to 17 turns on the key, 10 to 12 on the token
  ([credential probe](../2026-11-26-credential-probe/README.md)). The probe's second round points to the
  1-hour prompt cache the token uses plus the budget notice Claude Code shows under a cap. That
  cause is inferred from counts, not observed.
- **Inside Wachiman, the credential's effect on known bugs is small.** v1.15.0 found 6 of 9 (#465)
  and 12 of 30 (#467) on the key, against 4 of 9 and 10 of 30 on the token. Three runs cannot
  separate that from run-to-run spread.
- **Sonnet 5.5 on the token found the most known bugs at the lowest cost** of the sets measured:
  16, 14 and 12 per run, $5.77 a run on average, $0.41 per known bug
  ([Sonnet baseline](../2026-11-26-v1.21.0-sonnet-baseline/README.md)). Turns per batch rose to 19.3.

## Every measured set

All rows: the five kaipu-record pull requests, 3 runs per set, 27 known bugs. A run is one review
of each of the five pull requests, so **cost per review = cost per run / 5**. Cost per run is the
set's total for 15 reviews divided by 3. On the token, costs are API-equivalent estimates, not a bill.

| Set | Model, credential, budget | Runs | Known bugs per run (mean) | Cost per run | Cost per review | Cost per bug | Turns per batch | Report |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v1.4.0 | Opus 5.5, key, $3 | W4–W6 | 12, 11, 12 (11.7) | $6.96 | $1.39 | $0.60 | 13.7 | [2026-11-02](../2026-11-02/README.md) |
| v1.20.1 | Opus 5.5, token, $3, no focus file | W7–W9 | 10, 9, 11 (10.0) | $7.15 | $1.43 | $0.71 | 8.2 | [v1.20.1 replay](../2026-11-25-v1.20.1-replay/README.md) |
| v1.21.0 | Opus 5.5, token, $3 | W10–W12 | 9, 8, 10 (9.0) | $7.35 | $1.47 | $0.82 | 8.5 | [focus replay](../2026-11-25-v1.21.0-focus-replay/README.md) |
| v1.21.0 | Opus 5.5, token, $10 | W13–W15 | 12, 11, 9 (10.7) | $7.42 | $1.48 | $0.70 | 10.1 | [budget replay](../2026-11-25-v1.21.0-budget-replay/README.md) |
| v1.4.0 again | Opus 5.5, key, $3 | W16–W18 | 9, 11, 14 (11.3) | $7.16 | $1.43 | $0.63 | 14.1 | [v1.4.0 rerun](../2026-11-25-v1.4.0-rerun/README.md) |
| **v1.21.0** | **Sonnet 5.5, token, $10** | W31–W33 | 16, 14, 12 (14.0) | $5.77 ($5.74, $5.69, $5.88) | $1.15 | $0.41 | 19.3 | [Sonnet baseline](../2026-11-26-v1.21.0-sonnet-baseline/README.md) |

Two more kinds of measurement are not in that table because they use other pull requests or no
Wachiman:

| Set | What it measures | Report |
| --- | --- | --- |
| W19–W30: v1.5.0, v1.9.0, v1.15.0 on the key and on the token | Turns and known bugs on two pull requests only (#465 and #467), to find the release where turns dropped. Result: none; the credential did | [release bisect](../2026-11-26-release-bisect/README.md) |
| Credential probe: plain `claude -p` on #465, 27 calls | Turns, cost and known issues per call by credential, cap and cache lifetime. Not Wachiman | [credential probe](../2026-11-26-credential-probe/README.md) |

## Reproduce it from zero

The steps follow the order the investigation ran. Each report's Conditions table lists the exact
inputs of its sets.

### 1. Prerequisites

1. A clone of the kaipu-record repository that contains every SHA of the manifest. Use a bare
   clone, because a working checkout runs its own `pre-push` hooks on the replay push:
   `git clone --bare <your kaipu-record checkout> /tmp/kaipu-mine/repo`.
2. A GitHub account with `gh` logged in, `git` push access over SSH, `jq`, and Bash 3.2 or newer.
3. A throwaway public repository for the replays (the reports used `kaipu-bench-wachi-v3`), with
   these Actions secrets. Never paste their values into a report:
   - `CLAUDE_CODE_OAUTH_TOKEN`: a subscription token from `claude setup-token`.
   - `ANTHROPIC_API_KEY`: optional. Add it only for the sets that ran on a key
     (W4–W6, W16–W18, W19–W24, W28–W30).
4. The Wachiman GitHub App and the replay setup links that `bench.sh create` prints.

Not confirmed from the sources: `bench.sh` hardcodes the owner (`niway-dev`), the SSH alias
(`github-csdev`) and the expected `gh` login (`csdev19`) in its first lines. Anyone else has to
change those three values before it runs.

### 2. Create the replay repository and the first set

```sh
cd replay
export KAIPU_CLONE=/tmp/kaipu-mine/repo     # the bare clone
export BENCH_BRANCH_PREFIX=replay-v140      # one prefix per set of runs
export BENCH_FOCUS=as-is                    # v1.4.0 reads .github/agent-review.md itself
./bench.sh create wachi kaipu-bench-wachi-v3   # repo, main, replay branches; setup PR is #1
./bench.sh open kaipu-bench-wachi-v3           # one replay PR per manifest row, then /wachi review
./bench.sh rounds kaipu-bench-wachi-v3 2 3     # rounds 2 and 3 on the same commits
./bench.sh collect kaipu-bench-wachi-v3 out/ v140   # reviews and comments to out/v140-pr-<n>-*.md
```

- Add `--dry-run` to any command to print the `gh` and `git` commands without running them.
- For a repository that already exists, use `push` instead of `create`, with a new
  `BENCH_BRANCH_PREFIX`:
  `./bench.sh push kaipu-bench-wachi-v3`, then `open`, `rounds 2 3`, `collect`.
- The manifest defaults to [`manifest-2026-10-31.tsv`](manifest-2026-10-31.tsv). The release bisect
  used [`manifest-2026-11-26-bisect.tsv`](manifest-2026-11-26-bisect.tsv) through `BENCH_MANIFEST`.
- Round 1 is `open`. The engine does not review a head it already marked, so `rounds` pushes the
  same head under a new branch name.
- Set `BENCH_FOCUS=rename` for any engine v1.14.0 or newer. It copies `.github/agent-review.md`
  to `.github/wachiman.md` on the base, which those engines read
  (see [Review focus file](README.md#review-focus-file)).

### 3. Pin a Wachiman version and a credential in the caller workflow

The caller is the workflow on the replay repository's `main`. Its `uses:` line pins the engine by
SHA; the `with:` block sets the model, effort and budget; the `secrets:` block sets which
credential the run can use.

```yaml
uses: niway-dev/wachiman/.github/workflows/review.yml@<release SHA> # v1.21.0
with:
  model: claude-opus-5-5     # claude-sonnet-5-5 for the baseline
  effort: high
  verify: false
  budget_usd: 10             # omit for the $3 default
secrets:
  CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}   # drop this line for a key-only run
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}               # drop this line for a token-only run
```

With both secrets set, the engine uses the token. To compare releases on one credential, pass
only one. Ready-made callers in this folder:

| File | Used for |
| --- | --- |
| [`wachi-workflow-v1.4.0.yml`](wachi-workflow-v1.4.0.yml) | W16–W18: v1.4.0, key only, $3 |
| [`wachi-workflow-v1.5.0.yml`](wachi-workflow-v1.5.0.yml), [`wachi-workflow-v1.9.0.yml`](wachi-workflow-v1.9.0.yml), [`wachi-workflow-v1.15.0-api-key.yml`](wachi-workflow-v1.15.0-api-key.yml) | Bisect on the key |
| [`wachi-workflow-v1.15.0.yml`](wachi-workflow-v1.15.0.yml) | Bisect on the token |
| [`wachi-workflow.yml`](wachi-workflow.yml) | v1.21.0, Opus 5.5, token and key, `budget_usd: 10` (W13–W15 had the same inputs). Remove `budget_usd` to reproduce the $3 sets W7–W12 |
| [`wachi-workflow-sonnet.yml`](wachi-workflow-sonnet.yml) | W31–W33: Sonnet 5.5, token only, `budget_usd: 10` |

W7–W9 also ran without the focus file: use `BENCH_FOCUS=as-is` with a v1.14.0+ engine.

### 4. Put the caller on the replay repository's `main`, and restore it

`bench.sh` never installs a caller. The reports say each one was put on `main` "through the
contents API" before round 1, then `main` went back to `wachi-workflow.yml`. The workflow path
on `main` is `.github/workflows/wachi-bench.yml`. A sketch of that call (not recorded in the
sources, not tested here):

```sh
REPO=niway-dev/kaipu-bench-wachi-v3
P=.github/workflows/wachi-bench.yml
SHA=$(gh api "repos/$REPO/contents/$P" --jq .sha)
gh api -X PUT "repos/$REPO/contents/$P" \
  -f message="bench: install <caller name>" -f sha="$SHA" \
  -f content="$(base64 < replay/wachi-workflow-sonnet.yml | tr -d '\n')"
```

After the last round, repeat it with `wachi-workflow.yml`.

### 5. Label the findings against the known-bug catalogue

1. The known bugs per pull request are listed in the per-PR docs of the
   [v1.4.0 rerun](../2026-11-25-v1.4.0-rerun/prs/) (IDs such as #463 E1; "Label when found"
   rules). [`kaipu-record-bug-catalogue.md`](../kaipu-record-bug-catalogue.md) is the wider catalogue
   those five were chosen from.
2. A labeller reads each posted finding and the head code, and marks it as a known bug (full or
   in part), an extra already seen, a new finding, or invalid. These reports used one Claude
   Sonnet 5.5 pass per pull request, not blind. Its judgement calls are written in each report's
   `prs/` files.
3. Counts come from [`dataset/labelled-runs.csv`](../dataset/labelled-runs.csv) (`run_label` W4–W33).
4. Check first that every review body says the whole pull request was reviewed. A partial review
   is not comparable with a full one.

### 6. Compute cost per review and turns per batch

- **Cost per review** = cost per run / 5, where cost per run is the sum of the five reviews' costs
  in a run. Each review's cost is the last `<sub>` footer of its review
  ([`dataset/reviews.csv`](../dataset/reviews.csv)); `Cost (estimate)` marks a token run, `Cost` a key run.
- **Turns per batch call** = `turns` summed over a set's batch calls, divided by the number of
  calls. Per run log: [`dataset/run-logs.csv`](../dataset/run-logs.csv) (`calls`, `turns`),
  joined to the review through `reviews.csv` `run_id`.
- **Per-call detail for the Sonnet set** is [`batch-calls.jsonl`](../2026-11-26-v1.21.0-sonnet-baseline/batch-calls.jsonl),
  one `wachiman-cost` line per batch call (42 calls):

  ```sh
  jq -s '{calls: length, turns_per_call: (map(.turns)|add/length),
          total_usd: (map(.cost_usd)|add), costliest_call: (map(.cost_usd)|max)}' batch-calls.jsonl
  ```

  This gives 42 calls, 19.3 turns per call, $17.30 for three runs ($5.77 each) and $0.73 for the
  costliest call, as the report states.

### 7. Run the credential probe

The probe is one plain `claude -p` call on the diff of kaipu-record #465 (14 files): no Wachiman,
Claude Code 2.1.304, `claude-opus-5-5`, effort `high`, 40 turns, read-only tools, one credential.

1. Put [`credential-probe.yml`](credential-probe.yml) on the replay repository's `main` (step 4).
   It needs the replay branches of #465 on the repository (defaults `replay-v1150k/pr-465/head` and
   `.../base`) and both secrets.
2. Start it by hand from the Actions tab (`workflow_dispatch`). The inputs the reports varied:

   | Input | Values used |
   | --- | --- |
   | `credentials` | `["api-key","oauth-token"]` (default), or `["oauth-token"]` |
   | `budget_usd` | `0.75` (Wachiman's batch cap), `3`, or `0` (no cap, so no budget notice) |
   | `cache_ttl` | `default`, `5m` or `1h` |
   | `max_turns` | `40`, and `5` and `9` for the turn-limit check |
   | `runs` | `1,2,3` |

3. Read the run's summary page: mean turns per credential, cost per turn, cache lifetime. The
   `probe-summary` artifact holds every field of every call. Saved results and the final text
   of each call: [`results/`](../2026-11-26-credential-probe/results/) and
   [`reviews/`](../2026-11-26-credential-probe/reviews/); the labelling is
   [`labels.md`](../2026-11-26-credential-probe/labels.md).

The probe's second round (`cache_ttl: 5m`, cap `$0.75`) gave 13 to 14 turns, against 10 to 12 on
the automatic 1-hour cache. The same fix inside Wachiman is measured in the
[prompt-cache report](../2026-11-26-prompt-cache-5m/README.md). Its run labels W31–W33 are not the
Sonnet baseline's W31–W33: the two reports numbered their runs separately, so cite them by report.

## What is not proven

- **The Wachiman sets are different configurations, not a spend sweep.** They change the engine
  version, model, credential, budget and focus file between sets, three runs each. They show that
  the $3 budget left reviews partial and that the credential changes the turns. They do not show
  how known bugs grow with spend.
- **The only spend sweep is the probe, and it is plain `claude -p` on one pull request.** It sweeps
  the per-call cap and the cache lifetime. Past about 15 turns, more turns found no more known
  issues: 1.7 to 2.7 per call at 20 to 39 turns, against 2.0 to 2.3 at 13 to 17. On the key, going
  from the $0.75 cap (about $0.60 a call) to $3 (about $1.07) raised the mean from 2.0 to 2.3
  issues of 7: about $1.4 per extra issue, derived from the report's tables. It is not a measure of
  review quality: a Wachiman review found 4 to 8 of the 9 issues on the same pull request.
- **A Wachiman spend sweep is tracked in
  [the open spend-sweep issue](https://github.com/niway-dev/wachiman-benchmarks/issues/42)**.
  Until it runs, treat any statement about the best Wachiman budget as a hypothesis.
- **The cause of the earlier stop on the token is inferred.** The probe shows the gap vanishes
  with no cap and mostly vanishes with a forced 5-minute cache. It cannot show why the model stops.
  The budget notice was read from the strings of the Claude Code 2.1.304 binary; it is not in
  Anthropic's documentation.
- **Three runs per set.** Differences of two known bugs per run are inside the spread. Earlier sets were
  labelled by earlier subagent passes with the same rules, not re-labelled for W31–W33.
- **Costs on the token are API-equivalent prices, not a bill.** A subscription is not billed per call.
- **The comparison across dates is not controlled for the model's service.** Opus W13–W15 ran on
  2026-11-25, Sonnet W31–W33 on 2026-11-26.
