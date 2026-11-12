# Wachiman on the replay of pingdotgg/t3code#32830

**One minute.** Wachiman 1.12.0 ran locally on the replay head (one commit, 4 files, +109 lines) and made 5 findings. It matched both real bugs the bots raised (Macroscope T1 and CodeRabbit T3 describe the same defect). It missed one bot finding, CodeRabbit T2 (the mobile title lookup is not refreshed after a shell removal), a real minor bug that was fixed before merge. Of its 4 findings that no bot raised, 3 are real but minor and 1 is real but its trigger is improbable. None of the 4 was changed in the merged PR or in any later t3code commit, so the code gives no outside confirmation of them.

Basis: a local rerun at the replay head (`basis: rerun` in the `wachiman-audit` sense), compared with the bot threads in [`bot-threads.md`](bot-threads.md). The bots reviewed the original PR on GitHub. No other reviewer was run for this report.

## Run facts

| | |
| --- | --- |
| Command | `env -u ANTHROPIC_API_KEY WACHIMAN_DIR=<wachiman main-1-12 worktree> wachiman local --repo-dir /tmp/t3bench-32830 --commit HEAD --profile isolated:personal --format json --output wachiman.json` |
| Wachiman version | 1.12.0 (`engine.version` in `wachiman.json`; `wachiman --version` with that `WACHIMAN_DIR` printed 1.12.0) |
| Model | Claude Opus 5.5 via Claude Code 2.1.321, effort high, isolated profile `personal` |
| Range | one commit: `97a175e` (replay head = t3code `f54e7cf3`) against its parent `f3237a9` (replay base = t3code `e11c2fdc`) |
| Coverage | 4 of 4 files reviewed, 0 skipped, not partial, 1 batch, verify off |
| Wall time | 160 s for the whole command; the review batch itself took 93.0 s and 18 turns |
| Cost | $0.64 estimated at API prices (not a bill: the run used the subscription). Tokens: 18 input, 8,059 output, 280,638 cache read, 53,152 cache write |
| Outputs | [`wachiman.json`](wachiman.json); [`wachiman.md`](wachiman.md) is rendered from that JSON with `jq`, because `wachiman local` has no option to re-render a saved result |

Failed attempts, discarded: two earlier runs never reached the model. A 1.10.1 run failed with `git add -A -f ... spawnSync git ETIMEDOUT` and a first 1.12.0 run with `tar -xf failed: spawnSync tar ETIMEDOUT`. Both happened while the shared Mac was at load ~25 with two other Wachiman runs going. The snapshot step has a fixed 60 s timeout (`TIMEOUT_MS` in `src/connectors/local-git.ts`), and extracting this 395 MB, 31,782-file tree took 44 s by hand at that load. Neither failed run wrote any output or posted anything. The run reported here was started once the load had fallen to ~5.

## Posted review

One review with 5 inline comments on the head commit `97a175e`, all on lines in the diff, so the review body holds none of them: https://github.com/niway-dev/t3code-bench-wachi/pull/2#pullrequestreview-5867704930

| W# | path:line | comment |
| --- | --- | --- |
| W1 | `apps/web/src/components/chat/MarkdownThreadLink.tsx:63` | https://github.com/niway-dev/t3code-bench-wachi/pull/2#discussion_r4545202916 |
| W2 | `apps/mobile/src/state/entities.ts:73` | https://github.com/niway-dev/t3code-bench-wachi/pull/2#discussion_r4545202921 |
| W3 | `apps/web/src/components/ThreadContextChip.tsx:44` | https://github.com/niway-dev/t3code-bench-wachi/pull/2#discussion_r4545202927 |
| W4 | `apps/web/src/components/chat/MarkdownThreadLink.tsx:56` | https://github.com/niway-dev/t3code-bench-wachi/pull/2#discussion_r4545202933 |
| W5 | `apps/web/src/components/chat/MarkdownThreadLink.tsx:62` | https://github.com/niway-dev/t3code-bench-wachi/pull/2#discussion_r4545202935 |

## Match table

T# refers to the rows of [`bot-threads.md`](bot-threads.md): T1 Macroscope High, T2 CodeRabbit Minor, T3 CodeRabbit Major.

| Wachiman finding | severity | bot thread | verdict | judgment basis |
| --- | --- | --- | --- | --- |
| W2: the placeholder "Thread" title stops `resolveThreadLink` from falling through to `guessThreadLinkRef` for v1 links while the lookup is loading or after it fails (`entities.ts:73`) | fix | T1, T3 | **matched** (same defect, same line, same mechanism: a fallback title is treated as proof that the candidate exists) | checked in the code (`entities.ts:70-73` at the head) |
| W1: a v2 link to an environment this client cannot reach now renders a clickable "Thread" chip instead of "Thread on another machine" (`MarkdownThreadLink.tsx:63`) | fix | none | Wachiman-only | checked in the code |
| W3: removing the tooltip branch makes truly deleted threads in message and composer chips say "Open thread" (`ThreadContextChip.tsx:44`) | consider | none | Wachiman-only | checked in the code |
| W4: one `getThreadTitles` RPC per unloaded link, never cached (`MarkdownThreadLink.tsx:56`) | consider | none | Wachiman-only | checked in the code |
| W5: `titles.data?.[id] !== undefined` also matches prototype keys such as `constructor` (`MarkdownThreadLink.tsx:62`) | consider | none | Wachiman-only | checked in the code; reachability inferred |
| none | | T2: refresh mobile title lookups after shell removals | **bot-only** | checked in the code |

Partial matches: none. W4 touches the same query family as T2 but describes another defect (repeated round trips, not a stale result), so it is not counted as a match.

## Bot findings Wachiman missed

**T2 (CodeRabbit, Minor): mobile title lookups are not refreshed after a shell removal.** Checked in the code. At the head, the shared `threadTitles` query family re-checks its ids when a thread leaves the shell, but only if it was built with a `shellState` (`packages/client-runtime/src/state/orchestration.ts:57-65`). The web client passes one (`apps/web/src/state/orchestration.ts:7`). The mobile client does not (`apps/mobile/src/state/orchestration.ts:6`). So on mobile, a thread deleted after its title was looked up keeps its old title. The merged PR adds `shellState: environmentShell.stateValueAtom` to the mobile file (`23e3465e`, line 8), which confirms the bug. Wachiman read the query family (it cites `orchestration.ts:54-55` in W4) but did not compare how the two clients construct it.

## Wachiman-only findings

None of the four was changed in the merged commit `23e3465ec6a5`, and no later commit in `/tmp/t3code-mine/repo` touches `MarkdownThreadLink.tsx`, `ThreadContextChip.tsx`, `UserMessageContextChips.tsx` or the mobile `entities.ts`. Nothing outside our own reading confirms them.

- **W1, real but minor (checked in the code).** At the head, `UnresolvedChip` renders only when `titles.isSuccess && !titles.isPending` (`MarkdownThreadLink.tsx:63`). When the query fails, a link renders as a `ThreadContextChip` titled "Thread" with the tooltip "Open thread". Before the change, a v2 link to another environment rendered `unknownThreadLinkLabel`, which is "Thread on another machine" (`packages/shared/src/threadLinks.ts:165-172`). The new browser test shows that a failed lookup keeping a clickable "Thread" chip is intended (`MarkdownThreadLink.browser.test.tsx:48-51`, failure "offline"). So the real point is narrower: a link to an environment that is not connected used to name the other machine, and that label is gone. The merged version keeps the same `settled` gate, so this behaviour shipped. Worth raising as a UX question, not a must-fix.
- **W3, real but minor (checked in the code).** `ThreadContextChip` is also used by `UserMessageContextChips.tsx:321` and `composerContextPresentation.tsx:337`, and neither runs a title lookup. With the `shell ? "Open thread" : "Thread no longer available"` branch removed, a deleted thread in those chips is now labelled "Open thread". The merged version still ends with an unconditional `"Open thread"` (line 57), so the maintainers kept it, deliberately or not.
- **W4, real but minor (checked in the code).** `threadTitles` has `staleTimeMs: 0, idleTtlMs: 0` (`orchestration.ts:54-55`), and each `UnloadedThreadLink` creates its own query, keyed by its own ids. The merged version renames the query to `threadLinkMetadata` and still sends one query per link. It costs extra round trips; nothing breaks.
- **W5, real but its trigger is improbable (checked in the code; reachability inferred).** `ThreadId` is only a trimmed non-empty string (`packages/contracts/src/baseSchemas.ts:246-250`), so a link id like `constructor` would decode. If the decoded record has a normal prototype, `titles.data["constructor"]` is a function, and line 68 then calls `.trim()` on it and throws. Whether the RPC result is a plain object was not checked. The sibling `ThreadRelationshipsControl.tsx:538` uses `Object.hasOwn`. The trigger needs an agent to write a link with that id, so the case is improbable.

Wrong findings: none found.

## Counts

| | count |
| --- | --- |
| Wachiman findings | 5 (2 fix, 3 consider) |
| Bot reference threads | 3 (2 distinct defects: T1 and T3 are the same defect) |
| Matched | 1 Wachiman finding (W2) ↔ 2 bot threads (T1, T3) |
| Partial | 0 |
| Bot-only | 1 (T2, real-minor, fixed before merge) |
| Wachiman-only | 4: 3 real but minor (W1, W3, W4), 1 real but improbable (W5), 0 wrong; none fixed upstream |

Of the 2 distinct defects the bots found, Wachiman found 1: the High/Major one.

## Limits

- One PR, one local rerun, one Wachiman run (the model is not deterministic; another run could differ).
- The bots reviewed GitHub's PR state; Wachiman reviewed the same tree as a single commit on a laptop. Same code, different setting.
- Judged by Claude Opus 5.5 (`claude-opus-5-5`) in the main session, reading the code at the replay head and the merged commit `23e3465ec6a5`. No test was run. T1/T3 "fixed before merge" comes from the chunk verdict in `bot-threads.md`, not rechecked here.
- No verdicts were recorded in Wachiman's history: the run did not use `--history`.
