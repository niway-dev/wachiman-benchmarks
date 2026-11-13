# Sonnet 5.5 high on the replay of pingdotgg/t3code#33758: comparison with the bot threads

## Summary (one minute)

There is no Opus 5.5 run to compare on this PR: the earlier Opus run never reached the model (snapshot timeouts, see [`../report.md`](../report.md)). Only Sonnet 5.5 high ran (Wachiman 1.12.0, verify off, 8 findings).

- Of the 6 reference threads catchable at the head (T1, T2, T3, T4, T5, T7), Sonnet found **1**: T1 (S1). It missed T2, T3, T4, T5 and T7.
- T8 (not catchable at the head) is touched partially by S2, which names the same family of defect (the OpenCode goal capability is gated by version in some places and not in others). T6 was not found, as expected.
- Sonnet-only findings: S2 (real-minor, checked in code), S3 (real-minor, partly unverified), S4 (nit, plausible race but not checked at runtime), S5 and S8 (questions or docs, unverified), S6 (nit), S7 (test coverage, nit). No finding was judged wrong.

Basis: one run, judged by a Claude Sonnet 5.5 subagent reading the code at `/tmp/t3bench-33758` (head `a9083686`). No tests were run.

## Reference threads

| T# | bot | our verdict | catchable at head? | Sonnet result |
| --- | --- | --- | --- | --- |
| T1 | macroscope | real-bug | yes | **found** (S1): same defect, goal reads of every loaded session run in series inside the 15 s reconcile budget, reconnect retries and then fails every turn. S1 also proposes the right fix (read only sessions with an active turn, bounded). |
| T2 | macroscope | real-bug | yes | missed. S1 touches reconcile, but not the defect: `endExecution` trusting the cached `active` status when `readGoal` fails. |
| T3 | coderabbit | real-minor | yes | missed. Nobody names the stale `/goal` read replacing a newer `goal.changed` event. S4 is on the same line but a different defect (see below). |
| T4 | macroscope | real-bug | yes | missed. Nobody names that a delayed `readGoal` can return after the turn was cleared and `finishTurn(state, ...)` ends the replacement turn. S4 is on the same line (3459) but about the lock. |
| T5 | macroscope | real-bug | yes | missed. S5 asks a related question (can a goal turn hang forever) but about `/goal resume` and Stop, not about reconcile holding `heldEnd` for steers. |
| T6 | coderabbit | real-bug | no (`freshGoals` path added later) | not found, as expected. |
| T7 | macroscope | real-bug | yes | missed. S3 is about undecodable events leaving a held turn, a different cause. |
| T8 | coderabbit | real-minor | no (`driver.ts` not changed at head) | **partial** (S2): same family (version gate inconsistent between call sites and the Orchestrator/turn-start "native goal driver" check) and a fix that mentions `goalDriverFor`. It does not mention `driver.ts:137`. Credit is judged from the thread headline only; the thread body was not read. |

## Sonnet findings

| S# | severity | path:line | claim | match / verdict | basis |
| --- | --- | --- | --- | --- | --- |
| S1 | fix | `adapter.ts:2642` | Reconcile reads every loaded thread's goal in series (5 s each) inside the 15 s budget and the lock; reconnect times out and fails the session. | matches T1 | checked in code: loop at 2642-2649, `RECONCILE_TIMEOUT` at 2752 |
| S2 | fix | `adapter.ts:3457` | `/goal` show calls `readGoal` without the OpenCode >= 2.2.5 check used at 2642 and 3621. | partial T8; on its own real-minor | checked in code: `readGoal` at 3459 is unconditional, gates at 2642 and 3621. Whether old servers lack the RPC was not checked (the claim is from the finding). |
| S3 | consider | `adapter.ts:2469` | A `goal.changed` event that fails to decode is dropped with no log, so a stale `active` can hold a turn. | Sonnet-only, real-minor | checked in code: `if (goal._tag === "Failure") return;` with no log. Whether OpenCode sends a shape the schema rejects is unverified. |
| S4 | consider | `adapter.ts:3459` | `/goal` show runs `readGoal` outside the adapter lock, so `updateGoal` can overwrite a concurrent event. | Sonnet-only, nit (plausible) | checked in code: no lock at 3459, lock at 3623; `updateGoal` spreads the thread and then yields `DateTime.now`. Whether the interleaving can happen was not checked (likely very narrow). Not the T3/T4 defects. |
| S5 | consider | `adapter.ts:3480` | Can a goal turn from `/goal resume` or Stop never end? | Sonnet-only, unverified (question) | code read: `pause`/`clear` finish the turn, `set`/`resume` rely on OpenCode events. OpenCode behaviour not checkable here. |
| S6 | consider | `adapter.ts:3621` | The literal "2.2.5" is repeated; name it once. | Sonnet-only, nit | checked in code: the literal appears at 2642 and 3621 |
| S7 | consider | `OpenCode2AdapterV2.test.ts:5047` | No tests for the reconcile goal read, `/goal resume`, the pre-2.2.5 path or an undecodable event. | Sonnet-only, nit (test gap) | gaps not enumerated against the test file; default version 2.0.18 confirmed at test line 798 |
| S8 | consider | `docs/user/composer.md:314` | "Stopping their goal pauses it" is ambiguous for OpenCode and unsupported by code. | Sonnet-only, nit | checked in code: docs line read at 314-315; the adapter's interrupt path was not re-read |

## Sonnet-only findings

- **S2, real-minor (confirmed in code).** The only Sonnet-only item with a concrete inconsistency. Related to T8.
- **S3, real-minor.** Silent drop is confirmed; the harm depends on OpenCode payloads that were not checked.
- **S4, nit.** Plausible lock inconsistency; the window is likely tiny.
- **S5, unverified.** Questions to the author; depends on OpenCode 2.2.5 behaviour.
- **S6, S7, S8, nit.** Cleanup, tests and docs.

## Wrong findings

None found. No Sonnet finding contradicted the code that was read.

## Limits

- One run of one model; no Opus run exists.
- Judged by a Claude Sonnet 5.5 subagent reading the code. No tests were run and no OpenCode server was available.
- The T8 partial rests on the thread headline in `bot-threads.md`, not on the full thread text.
- "Confirmed in code" means the cited lines say what the finding says. It does not mean the runtime behaviour was reproduced.
