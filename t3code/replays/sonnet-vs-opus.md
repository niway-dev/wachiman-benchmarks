# Sonnet 5.5 high vs Opus 5.5 high on the t3code replays

**Answer.** On this second codebase, Sonnet 5.5 high did about as well as Opus 5.5 high, for about 40% less money. That fits the default change in niway-dev/wachiman#192, but it does not prove it. On the four replays where both models ran, they found the same serious bugs in three. In the fourth (#30579), Sonnet missed T1, a serious bug, but found two real-minor defects that Opus run 1 missed. Opus also missed T1 in one of its three runs on that PR. Counting every useful defect the bots raised, Sonnet stated 6 in full and 1 in part; Opus stated 5 in full and 3 in part. Neither model made a finding we judged wrong. Sonnet cost $1.47 against Opus's $2.53 on the same four PRs. Its model time was similar, but it took more turns. On #33758, Sonnet is the only review, because the Opus run never got past the snapshot step. Sonnet found 1 of the 6 useful bot defects there.

One run per model per PR. That is not enough to rank the two models (see [Limits](#limits)).

## Per PR

"Reference" counts the distinct real-bug and real-minor defects that the bots raised and that could be caught at the replay head. When two bot threads describe the same defect, they count once. "p" means partial. Opus means the run judged in `<pr>/report.md` (run 1 on #30579). Costs are Wachiman's API-price estimates, not bills.

| t3code PR | Reference: real-bug / real-minor | Opus found | Sonnet found | Opus extras (not bot) | Sonnet extras (not bot) | Opus cost | Sonnet cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [#30579](30579/sonnet-high/comparison.md) | 2 (T1, T2/T6) / 4 (T3, T4, T5, T8) | bugs T1, T2/T6; minors none | bugs T2/T6; minors T4, T5 | none | 2 real-minor (S4 reply "Add to chat" adds the whole thread; S5 = Opus run 2's N1), 1 nit | $0.57 | $0.41 |
| [#32830](32830/sonnet-high/comparison.md) | 1 (T1/T3) / 1 (T2) | bug T1/T3; T2 missed | bug T1/T3; T2 missed | 3 real-minor (W1, W3, W4), 1 real with an unlikely trigger (W5) | the same as W1, W3 and W5, plus 1 nit; W4 not found | $0.64 | $0.42 |
| [#24079](24079/sonnet-high/comparison.md) | 4 (T1, T2, T3, T6) / 0 | T1, T3p | T1, T3p (the same finding as Opus) | none | 1 nit (test gap) | $0.61 | $0.29 |
| [#30556](30556/sonnet-high/comparison.md) | 1 (T1/T4) / 2 (T2, T5) | bug T1/T4; minors T2p, T5p | bug T1/T4; T2, T5 missed | 1 real-minor sub-point inside W1 | 1 real-minor (missing tests for two revert failure paths) | $0.71 | $0.35 |
| [#33758](33758/sonnet-high/comparison.md) | 5 (T1, T2, T4, T5, T7) / 1 (T3) | no review (3 snapshot timeouts) | T1 | — | 2 real-minor (S2 no version gate on `/goal show`, S3 a bad `goal.changed` event is dropped without a log), 4 nit, 1 unverified | — | $0.53 |
| **4 comparable PRs** | **8 / 7** | **bugs 5 + 1p; minors 2p** | **bugs 4 + 1p; minors 2** | | | **$2.53** | **$1.47** |

Run facts for Sonnet (one batch per PR, all files reviewed, none partial):

| PR | turns (Opus → Sonnet) | review call, s (Opus → Sonnet) | whole command, s (Opus → Sonnet) | output tokens (Sonnet) |
| --- | --- | --- | --- | --- |
| #30579 | 9 → 21 | 57.1 → 117.8 | 136.9 → 196 | 13,187 |
| #32830 | 18 → 25 | 93.0 → 108.2 | 160 → 193 | 11,542 |
| #24079 | 10 → 10 | 83.4 → 66.1 | 206.6 → 134 | 7,635 |
| #30556 | 11 → 18 | 79.0 → 73.6 | 147 → 161 | 7,734 |
| #33758 | — → 29 | — → 171.8 | — → 254 | 18,843 |

The two models ran at different times and under different machine load, so the wall times are only roughly comparable. The successful Opus runs started at a load of about 5 to 8, on a busier machine. The Sonnet runs ran at a load of 3 to 5.

## What differs, case by case

- **#30579.** Sonnet missed T1, a High Macroscope bug: "Add to chat" did nothing for comments that exist only in `detail.reviewThreads`. Opus caught it in runs 1 and 2 and missed it in run 3. Sonnet found T4 and T5. T4 also shows up in Opus runs 2 and 3; no Opus run found T5. Sonnet's S5 is the same finding as Opus run 2's N1. Across the three Opus runs and the one Sonnet run, 5 of the 6 reachable defects were found at least once. T3 was found by none.
- **#30556.** Both models found the serious bug: the leftover `revert-<sha8>` branch blocks every retry. Only Opus raised W2, which names the fast-forward and unmerged-MR cases (a partial match on T2 and T5). Sonnet's `contracts` text mentions the unmerged-MR case, but Sonnet did not raise it as a finding.
- **#32830 and #24079.** The two models are nearly identical. On #32830, Sonnet repeated three of Opus's four extra findings and dropped W4 (one query per link). On #24079, both made the same single finding.

## Matching rule

This is the rule from [`README.md`](README.md) and the existing reports. A finding matches a reference thread when it states the same defect, not when it only touches the same line. A partial match names the same defect or case but proposes a materially weaker or different fix, or covers only part of it. Reference threads are the threads in `<pr>/bot-threads.md` with our verdict real-bug or real-minor that could be caught at the head according to `<pr>/report.md`. Threads raised on code added after the head are left out of the counts.

## How the runs were made

- Wachiman 1.12.0 (`WACHIMAN_DIR` = the `main-1-12` worktree at `fd99401`; `wachiman --version` printed 1.12.0). Same clones, same head commits and same command as in each `report.md`; only the model changed: `env -u ANTHROPIC_API_KEY AGENT_REVIEW_MODEL=claude-sonnet-5-5 AGENT_REVIEW_EFFORT=high AGENT_REVIEW_VERIFY=0 wachiman local --repo-dir /tmp/t3bench-<pr> --commit HEAD --profile isolated:personal --no-verify --format json --output <pr>/sonnet-high/wachiman.json`. The Opus runs had verification off by product default; here it was set off explicitly.
- Runs were sequential, one review at a time, under `caffeinate -i`, from 2026-11-12 02:15 to 02:30 (-05:00), with the default temp dir. All five succeeded on the first attempt: no snapshot timeout, and the RAM disk was not needed.
- `<pr>/sonnet-high/wachiman.md` is a `jq` rendering of the JSON, not CLI output. `<pr>/sonnet-high/comparison.md` holds the per-PR match tables.
- Nothing was posted to GitHub, and nothing was committed.

## Limits

- **One run per model per PR is not a rank.** On #30579, three identical Opus runs found between 2 and 3 of the 6 reachable defects, and one of them missed T1. Sonnet's single run (3 of 6, T1 missed) sits inside that spread. Every per-PR difference in the table could be run-to-run variance.
- Four comparable PRs, picked because the bots made several useful comments on them. They are the bots' best cases, not a sample of typical PRs.
- The matching was done by Claude Sonnet 5.5 subagents (one per PR) and spot-checked by Claude Opus 5.5 in the main session. The Opus verdicts in `report.md` were taken as given. Sonnet-only findings were checked by reading the code at the head; the claims each `comparison.md` marks as unverified stay unverified. No tests were run.
- A Sonnet model judged Sonnet's output. A reader who wants an independent read should recheck the Sonnet-only rows and the #30579 T4/T5 matches.
- The cost figures are Wachiman's API-price estimates. The runs were paid by the subscription.
