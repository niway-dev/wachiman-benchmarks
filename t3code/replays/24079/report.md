# Wachiman on replayed pingdotgg/t3code#24079

**One-minute block.** Wachiman 1.12.0 reviewed the replay head commit locally, as a developer would before opening the PR. It raised 1 finding, and that finding is real: it is the same defect as Macroscope's T1, and the merged PR fixed it. It partly covers CodeRabbit's T3, which has the same root cause. It missed two real bugs that already existed at the head (T2, T6). The other five useful bot threads were raised on code that was added after the head, so a review of the head could not have raised them. Wachiman-only findings: 0. Cost: $0.61 estimated (API-price estimate; the run was paid by the subscription).

## Run facts

| item | value |
| --- | --- |
| Wachiman | 1.12.0 (`WACHIMAN_DIR=…/wachiman/.claude/worktrees/main-1-12`, main at `fd99401`) |
| Command | `env -u ANTHROPIC_API_KEY WACHIMAN_DIR=… wachiman local --repo-dir /tmp/t3bench-24079 --commit HEAD --profile isolated:personal --format json --output wachiman.json` |
| Range | one commit: `a561750` (replay head) against `cf5db8a` (replay base); original head `69a7f1c3` |
| Model | Claude Opus 5.5 via Claude Code 2.1.321, effort high, isolated profile `personal`, verify off (product default) |
| Coverage | 5 of 5 changed files, none skipped, not partial. The snapshot lacked 2 submodule paths under `.repos/alchemy-effect/submodules/` (not in the diff) |
| Wall time | 206.6 s for the whole command (2026-11-11 23:34:00 to 23:37:26 UTC); 83.4 s of that was the model (1 batch, 10 turns); most of the rest was the 526 MB, 28k-file snapshot |
| Tokens | input 12, output 7,855, cache read 208,831, cache write 51,900 |
| Cost | $0.614 (Wachiman's API-price estimate, not a bill) |
| Files | [`wachiman.json`](wachiman.json); [`wachiman.md`](wachiman.md) is rendered from the same JSON, not from a second run |
| Posted | review https://github.com/niway-dev/t3code-bench-wachi/pull/3#pullrequestreview-5866798503, inline comment https://github.com/niway-dev/t3code-bench-wachi/pull/3#discussion_r4544442728 |

Failed attempts, with nothing posted and no output kept:

1. Wachiman 1.10.1 (plain `wachiman`): it stopped before any model call after 166 s, with `git add -A -f … spawnSync git ETIMEDOUT` while building the snapshot. That output was discarded because the owner asked for 1.12.0.
2. Wachiman 1.12.0, first try: it stopped before any model call after 79 s, with `tar -xf failed: spawnSync tar ETIMEDOUT`.

Both timeouts come from the 60 s `TIMEOUT_MS` in `src/connectors/local-git.ts`. While they ran, the load average was 24 to 27. The Avira scan service was using about 160% CPU, and another thread was extracting its own snapshot at the same moment. The likely cause is file scanning during snapshot I/O; this was inferred, not measured. The third try started only after no other `wachiman-snapshot` process was running, and it succeeded.

## Match table

Only the threads that bear on the Wachiman finding are listed. Every other thread is bot-only (next section).

| Wachiman finding | bot thread | verdict | basis |
| --- | --- | --- | --- |
| W1 `AgentAwarenessRelay.ts:546` (fix): the `subagentRequests` map is updated only after the publishing-disabled and relay-unlinked early returns, and nothing clears or rebuilds it. If publishing is turned off and then back on, a parent stays on "Approval needed" after its child's request has resolved | T1 (Macroscope, High, `:568`): a parent can keep publishing `waiting_for_approval` after its subagent request has resolved or the child has been deleted (chunk-05: "when publishing was disabled in between") | **matched** | checked in code: at the head, `trackSubagentRequest` (line 546) runs after the gates at lines 466-483, and `resetPublishedConnection` (458-462) does not touch `subagentRequests` (401). The merged PR (`60514be9`) adds `currentSubagentRequestFor`, which re-reads each waiting child before its parent is published, with the comment "The map can miss a child's update while publishing is off or the relay is unlinked" |
| W1 (same) | T3 (CodeRabbit, Major, `:688`, commit e17084bc): record the child requests that appear while publishing is off | **partial** | checked in code: same root cause (tracking runs after the gates), and it is present at the head. W1's claim covers the opposite direction: a request that resolves while publishing is off, which leaves a stale wait. A request that first appears while publishing is off is not stated, although W1's first proposed fix (track before the gates) would cover it |

## Bot findings Wachiman missed

"Present at head" means the defect is already in the replay head commit that Wachiman reviewed. "Later code" means the thread is about code that a later commit of the PR added, so no review of the head could have raised it.

| T# | bot | our verdict | at the head? | basis |
| --- | --- | --- | --- | --- |
| T2 | Macroscope | real-bug | **present at head, missed** | checked in code: `trackSubagentRequest` republishes the parent through `enqueueWorkerPublish` (= `worker.enqueue`, lines 687 and 694). It does not use `enqueueThreadPublish` (line 720), which first calls `cancelPublishRetry`, so an exhausted retry budget is reused |
| T6 | CodeRabbit | real-bug | **present at head, missed** | checked in code: `pendingSubagentRequestFor` (lines 299-310) returns the literal `"approval"` for the first waiting child. When a second child starts to wait, the parent's identity does not change, so the second approval push is skipped |
| T4 | Macroscope | real-minor | later code | inferred: the thread is about request timestamps and ids that were added after the head (raised on 1a89e06c). At the head the map stores only the request kind |
| T5 | CodeRabbit | real-minor | later code | inferred: it is about the paused-tracking path that was added to fix T3, which is not at the head |
| T7 | CodeRabbit | real-minor | later code | inferred: it is about the timestamp tie-break between children, which was added to fix T6; the head compares no timestamps |
| T8 | Macroscope | real-bug | later code | checked in code: the `previousPublication.updatedAt` bump (chunk-05, at b406b70) does not exist at the head (no `previousPublication` in the relay or the shared module) |
| T9 | CodeRabbit | wrong | n/a | from chunk-05: disputed, and the bot withdrew it |
| T10 | CodeRabbit | nit | n/a | asks for a comment on `Effect.fnUntraced`. Not a defect |

## Worthwhile Wachiman-only findings

None. Wachiman's only finding matched T1.

## Counts

| count | value |
| --- | --- |
| Wachiman findings | 1 (1 fix) |
| Matched | 1 (W1 = T1) |
| Partial | 1 (W1 ~ T3) |
| Wachiman-only | 0 (worthwhile 0, minor 0, wrong 0) |
| Bot-only | 8 threads: T2, T4, T5, T6, T7, T8, T9, T10 |
| Bot-only real defects present at the head (fair misses) | 2 (T2, T6, both real-bug) |
| Bot-only on code added after the head | 4 (T4, T5, T7, T8) |
| Bot-only not defects | 2 (T9 wrong, T10 nit) |
| Useful bot threads (real-bug + real-minor) | 8; of the 4 that are possible at the head (T1, T2, T3, T6), Wachiman got 1 and part of another |

## Limits

- One commit and one run. Verification was off (the product default). No other reviewer was run; the bot side comes only from [`bot-threads.md`](bot-threads.md) and `../../batches/2026-11-09/chunk-05.md`.
- The bots reviewed several commits as the PR evolved, and Wachiman reviewed one, the head. Most of their threads followed fixes made after the head. For a check before the PR existed, the fair comparison is against the 4 useful threads whose defect exists at the head.
- Judged by Claude Opus 5.5 (`claude-opus-5-5`), reading the head and the merge commit `60514be9` in `/tmp/t3code-mine/repo`. The "later code" rows marked inferred were not traced commit by commit.
