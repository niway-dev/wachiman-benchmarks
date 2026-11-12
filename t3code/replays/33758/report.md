# Wachiman on the replay of pingdotgg/t3code#33758

**Status: no review.** Wachiman 1.12.0 never reached the model on this replay. All three local runs failed in the snapshot step, so nothing was posted on [replay PR #4](https://github.com/niway-dev/t3code-bench-wachi/pull/4) and there is no `wachiman.json`. The bot threads in [`bot-threads.md`](bot-threads.md) have no Wachiman findings to be compared with yet.

## Failed runs

Command, identical in every attempt (`wachiman --version` with this `WACHIMAN_DIR` printed 1.12.0):

`env -u ANTHROPIC_API_KEY WACHIMAN_DIR=<wachiman main-1-12 worktree> wachiman local --repo-dir /tmp/t3bench-33758 --commit HEAD --profile isolated:personal --format json --output t3code/replays/33758/wachiman.json`

Tree: a fresh clone of `replay/pr-33758/head` (`a9083686`, 6 files, +243/-12 against `ddcbb245`).

| # | started (local, -05) | load at start (1/5/15 min) | wall time | error |
| --- | --- | --- | --- | --- |
| 1 | 2026-11-11 23:11 | ~3.8 / 2.5 / 2.4, rose to ~9.5 during the run | 102 s | `git add -A -f failed in .../wachiman-snapshot-*: spawnSync git ETIMEDOUT` |
| 2 | 2026-11-11 23:15 | 8.3 / 5.4 / 3.7 | 122 s | same |
| 3 | 2026-11-12 00:02 | 6.9 / 6.2 / 7.3 | 79 s | same |

None of them wrote output or posted anything. The snapshot step runs `git add` with a fixed 60 s timeout (`TIMEOUT_MS` in `src/connectors/local-git.ts`).

Probable cause, not confirmed: between attempts 2 and 3, with no Wachiman run going, the load was 16.7. The top process was the Avira scan service (`com.avira.scanservice`) at ~155% CPU, with Zscaler `zdpd` next at ~24%. An on-access scanner that inspects each of the ~31k files the snapshot writes would explain a `git add` that takes more than 60 s even at moderate load. No run was timed with the scanner paused, so this is a hypothesis.

## Bot threads catchable at the head

Prepared for the comparison, from reading the code at the replay head and the PR's later commits in `/tmp/t3code-mine/repo`:

- **Catchable at the head (6):** T1, T2, T3 (raised on the head itself); T4 (the `/goal show` path, `readGoal` then `finishTurn` without checking `state.active === turn`, exists unchanged at the head); T5 (reconcile now calls `endExecution`, which holds `heldEnd` while `turn.steers` is non-empty, introduced at the head); T7 (reconcile `continue`s for sessions in `active` without clearing `heldEnd`, and the new `goal.changed` handler calls `endIfSettled`, both at the head).
- **Not catchable at the head (2):** T6 is about the `freshGoals` path added in `d674e881`; T8 is about the capability gate in `driver.ts`, a file the head does not change, added in `27c9f6a3`.

## To finish

Rerun once the snapshot can complete (scanner exclusion for the temp snapshot directory, or a quieter machine), then post the review, fill the match table and judge the Wachiman-only findings as in [`../32830/report.md`](../32830/report.md).
