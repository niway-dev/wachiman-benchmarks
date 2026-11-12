# Wachiman on the replay of pingdotgg/t3code#30579

Wachiman 1.12.0 ran locally on the replay head and made 2 findings. Both match reference bot threads (T1, and T2/T6). Both were fixed before merge, in the way Wachiman proposed. Wachiman made no finding of its own. It missed 5 useful bot threads; 4 of them target code that exists at the replay head. The question here is what Wachiman would have caught during local development, before the PR existed.

- Replay PR: https://github.com/niway-dev/t3code-bench-wachi/pull/1, head `dcb8635831860544c038627e9d04bab8a1ce4f2d` (tree of t3code `a8ae50f4`), base `91dc71f7` (tree of `d51bc58f`).
- Posted review: https://github.com/niway-dev/t3code-bench-wachi/pull/1#pullrequestreview-5866837904
- Reference: [`bot-threads.md`](bot-threads.md), 9 CodeRabbit and Macroscope threads. No bot was run for this report.

## Run facts

| | |
| --- | --- |
| Wachiman | 1.12.0, from `main` at `fd99401` (`WACHIMAN_DIR=…/wachiman/.claude/worktrees/main-1-12`) |
| Command | `env -u ANTHROPIC_API_KEY WACHIMAN_DIR=… wachiman local --repo-dir /tmp/t3bench-30579 --commit HEAD --profile isolated:personal --format json --output wachiman.json` |
| Product defaults | verify off, 1 batch, history off |
| Model | Claude Opus 5.5 via Claude Code 2.1.321, effort high, managed profile `personal` |
| Coverage | 7 of 7 changed files; none skipped, not partial. The snapshot lacked 2 submodule paths under `.repos/alchemy-effect/submodules/`, which are outside the change |
| Wall time | 136.9 s end to end, of which the review call took 57.1 s (9 turns). Evidence gathering took 11.8 s. The rest was snapshotting a 31,559-file tree on a loaded machine |
| Cost | $0.568 (Wachiman's API-price estimate, not a bill; the subscription paid). Tokens: 10 input, 5,331 output, 196,065 cache read, 52,783 cache write |

What failed along the way:

- A first run with the plain `wachiman` (1.10.1) completed. It was discarded on the owner's instruction, because only 1.12.0 counts. Nothing from that run was posted, and history was off.
- Two 1.12.0 attempts failed before any model call: `tar -xf failed: spawnSync tar ETIMEDOUT`, then `git add -A -f failed … spawnSync git ETIMEDOUT`. The snapshot steps have a fixed 60 s timeout (`TIMEOUT_MS` in `src/connectors/local-git.ts`). The machine's load average was 17 to 27, with three threads sharing it. The third attempt waited until the load dropped below 8, and then it succeeded. A large repository on a busy laptop can therefore fail a local run with no review at all.
- `wachiman.md` is a `jq` transcription of `wachiman.json`, not CLI output. `--input` takes a review input, not a saved result, so the CLI cannot render Markdown from a saved result. A second run would have been a second paid review.

## Match table

| Wachiman finding | Bot thread | Verdict | Evidence |
| --- | --- | --- | --- |
| W1 (fix, high) `PullRequestTimelineTab.tsx:686`: "Add to chat" does nothing for comments that exist only in `detail.reviewThreads` | T1 Macroscope High, `:687` | **matched** | Same defect, same fix. Checked in code: head line 686 searches `detail.comments` only. Merged `f08d8dd0` passes the comment object (`onAddToChat(comment)`, `PullRequestTimelineTab.tsx:196`), as W1 proposed |
| W2 (fix, medium) `PullRequestDetailPanel.tsx:1078`: the PR-reference dedupe matches on number, not URL | T2 Macroscope High, `:1078` | **matched** | Same defect and scenario: two repositories with the same `#42`. Checked: `64593653` changed the line to `existing.pullRequest?.url === detail.url`, which is exactly W2's fix, and the change is still at `f08d8dd0:1048` |
| W2 (same) | T6 CodeRabbit Minor, `:1079` | **matched** | Same defect as T2 (T2 and T6 are duplicates of each other) |

## Bot findings Wachiman missed

"Reachable at head" means that the code the thread is about already exists at the replay head, so a local review of that commit could have raised it.

| T# | Bot | Claim | Our verdict (from `bot-threads.md`) | Reachable at head |
| --- | --- | --- | --- | --- |
| 3 | Macroscope High | `readableBody` drops the rest of a remark, and the lines after it, when an HTML comment is left unclosed | real-minor, fixed before merge | Yes, checked: head `pullRequestDetail.logic.ts:698-702` truncates at `<!--` and sets `inComment` until a `-->` |
| 4 | CodeRabbit Minor | Return `null` when parsing removes the entire body | real-minor, fixed before merge | Yes, checked: head `:709` returns `kept.join("\n").trim()`, so it returns `""` and not `null` |
| 5 | CodeRabbit Minor | Scope comment chip IDs to the pull request | real-minor, fixed before merge | Yes, checked: head `:1157` builds the id `pr-comment:${thread.id}` with no PR in it. Fixed in `64593653` ("scope Add to chat chips to their pull request") |
| 8 | CodeRabbit Minor | Keep a durable PR reference when a handoff chip already exists | real-minor, fixed before merge | Probably. Inferred: the head's `hasPullRequest` check (`PullRequestDetailPanel.tsx:1077-1079`) counts any chip that carries `pullRequest`, so the same gap exists before `64593653`. Fixed in `134d3779` |
| 7 | CodeRabbit Major | Add both chips without inserting inline prompt references | wrong (disputed) | Not counted as a miss |
| 9 | CodeRabbit Minor | Preserve the fence's blockquote scope | real-minor, fixed before merge | No, checked: it is about the `BLOCKQUOTE_PREFIX` handling that `ee55f44a` added after the head. At the head, quoted fences are not recognized at all |

The 4 reachable misses are all real-minor. The 2 real-bug threads at the head (T1, T2/T6) are both covered by Wachiman. The bot verdicts in this table come from the chunk and were not re-judged. Only reachability was checked.

## Worthwhile Wachiman-only findings

None. Both of Wachiman's findings match bot threads.

## Counts

- Wachiman findings: 2. Matched: 2. Partial: 0. Wachiman-only: 0 (0 worthwhile).
- Reference threads: 9. Matched by Wachiman: 3 (T1, T2, T6; T2 and T6 are one defect). Bot-only: 6. Of those, 1 is wrong (T7), 1 is not reachable at the head (T9), and 4 are reachable real-minor misses (T3, T4, T5, T8).
- Distinct real defects at the head (by the chunk verdicts): 6 (T1, T2/T6, T3, T4, T5, T8). Wachiman found 2 of them: both real-bug defects, and none of the 4 real-minor ones.

## Limits

- One case, one run, at the product defaults (verify off). With 9 turns and 5,331 output tokens, the review is short. A second run could differ.
- Bot verdicts are reused from `bot-threads.md` and were not re-judged here. The match verdicts and reachability were judged by Claude Opus 5.5 (`claude-opus-5-5`), as marked above.
- The bots reviewed several commits of the PR, while Wachiman reviewed only the head. That is the local-development view this replay is meant to test, but it also means bot threads on later commits (T8, T9) were never fully in reach.
