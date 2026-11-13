# Opus 5.5 high vs Sonnet 5.5 high on replayed pingdotgg/t3code#24079

**One-minute summary.** Both runs (Wachiman 1.12.0, same commit `a561750`, same flags, only the model changed) found the same single real defect: the subagent-request map is not updated while publishing is off or the relay is unlinked, so a parent can stay stuck on a stale "waiting" state. That is Macroscope's T1 (matched) and partly CodeRabbit's T3 (partial). Neither run found T2 or T6, the two other real bugs that exist at the head. Sonnet added one extra "consider" finding, a test-coverage note that is a nit, not a defect. Sonnet cost $0.29 (72 s model time) against Opus $0.61 (83 s). Net: no difference in useful findings; Sonnet was cheaper and added only a nit.

## Reference threads (real-bug / real-minor)

| T# | verdict | catchable at head? | Opus | Sonnet |
| --- | --- | --- | --- | --- |
| T1 | real-bug | yes | found (W1) | found (S1) |
| T2 | real-bug | yes | missed | missed |
| T3 | real-bug | yes | partial (W1) | partial (S1) |
| T4 | real-minor | no, later code | not catchable at head | not catchable at head |
| T5 | real-minor | no, later code | not catchable at head | not catchable at head |
| T6 | real-bug | yes | missed | missed |
| T7 | real-minor | no, later code | not catchable at head | not catchable at head |
| T8 | real-bug | no, later code | not catchable at head | not catchable at head |

T9 (wrong) and T10 (nit) are not useful threads and were not matched by either run.

Sonnet's S1 partial on T3: it states the stale-entry direction (a request that resolves or a child that is deleted while publishing is off), which is T1's defect. Its fix ("call `trackSubagentRequest` before the gates") would also cover a request that first appears while publishing is off (T3), but the body does not state that case. Same reading as the Opus partial in report.md.

## Sonnet findings

| S# | severity | path:line | claim | match / verdict | basis |
| --- | --- | --- | --- | --- | --- |
| S1 | fix | `apps/server/src/relay/AgentAwarenessRelay.ts:546` | `trackSubagentRequest` runs after the publishing-enabled and relay-config gates, so the map goes stale while publishing is off or unlinked and the parent can republish a wrong "waiting" state | matched T1, partial T3; equals Opus W1 | from report.md (Opus judgment and its code check of lines 466-483, 546, `resetPublishedConnection`); Sonnet's cited lines are the same ones |
| S2 | consider (tests) | `apps/server/src/relay/AgentAwarenessRelay.test.ts:327` | the new test covers only one direct child going waiting then clearing; nested subagents, approval-over-input with two children, archived or deleted child and lineage cycles are untested | Sonnet-only: nit | checked in code: the head has one parent/child test at line 327 (plus a startup-filter test at 163); `pendingSubagentRequestFor` (lines 299-310) does return `"approval"` first, so the claim about the missing case is accurate. It is a coverage suggestion, not a defect, and it does not state T6 (second child does not change the parent's identity) |

## Opus-only and Sonnet-only

- Opus-only: none. Opus raised one finding (W1) and Sonnet raised it too.
- Sonnet-only: S2 (nit, test coverage). Not worthwhile as a defect; mildly useful as a pointer toward the multi-child area where T6 lives, but it does not name that bug.
- Both missed: T2 (parent republish skips `cancelPublishRetry`) and T6 (second waiting child does not change the parent identity).

## Wrong findings

None in either run. Nothing was judged wrong.

## Run facts (from the JSON files)

| item | Opus 5.5 high | Sonnet 5.5 high |
| --- | --- | --- |
| findings | 1 (fix) | 2 (1 fix, 1 consider) |
| cost estimate | $0.614 | $0.289 |
| model time | 83.4 s, 10 turns | 72.2 s, 10 turns |
| output tokens | 7,855 | 7,635 |
| coverage | 5 of 5 files | 5 of 5 files |

## Limits

- One run per model. Differences this small (one nit) are within normal run-to-run variation and say nothing reliable about the models.
- Judged by a Claude Sonnet 5.5 subagent reading code at `/tmp/t3bench-24079` (HEAD). No tests were run and wachiman was not re-run.
- Confirmed in code in this pass: only the S2 claim about what the head's tests and `pendingSubagentRequestFor` do. The S1 match and the Opus verdicts, including "later code" rows for T4, T5, T7, T8, come from `report.md` and were not re-traced; the "later code" rows were inferred there, not traced commit by commit.
- The T3 "partial" is a judgment call about wording versus fix scope.
