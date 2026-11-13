# Opus 5.5 high vs Sonnet 5.5 high on pingdotgg/t3code#32830

**One minute.** Same Wachiman 1.12.0, same head commit, same flags; only the model changed. Both runs found the one defect behind T1 and T3 (the placeholder "Thread" title treated as proof the thread exists, `entities.ts:73`). Both missed T2 (mobile title lookups not refreshed after shell removals), a real-minor bug that was fixed before merge. Sonnet made 5 findings: 1 matched T1/T3, 2 overlap Opus-only findings (W3, W1 from report.md), 1 overlaps Opus W5 (and adds a mobile site), and 1 is a new test-coverage remark (nit). Sonnet did not make Opus W4 (one RPC per link). No finding of either run was judged wrong. The two runs are close on this PR; Sonnet's S1 is slightly broader than Opus W5 (adds the mobile site), and its S2 is more detailed on `relabelThreadLinks` than Opus W2.

## Reference threads (real-bug / real-minor)

| T# | verdict | Opus | Sonnet |
| --- | --- | --- | --- |
| T1 | real-bug (fixed-before-merge) | found (W2) | found (S2) |
| T2 | real-minor (fixed-before-merge) | missed | missed |
| T3 | real-bug (fixed-before-merge) | found (W2) | found (S2) |

All three are catchable at the head (the code at the head contains each defect). T1 and T3 are the same defect. Partial matches: none in either run.

## Sonnet findings

Basis column: "checked in code" = I read `/tmp/t3bench-32830` at HEAD; "from report" = taken from report.md's Opus judgment of the same defect; "unverified" = not checked.

| S# | severity | path:line | claim | match / verdict | basis |
| --- | --- | --- | --- | --- | --- |
| S1 | fix (confidence medium) | `apps/web/src/components/chat/MarkdownThreadLink.tsx:62` | Plain-object lookup with a link-supplied id (`constructor`, `toString`, `__proto__`) returns a prototype function, then `.trim()` throws during render; same pattern in mobile `entities.ts:72` | Sonnet-only vs references; equals Opus W5 (web part). Verdict real-minor (improbable trigger), as for W5. | Web part: from report (W5, checked in code there) plus I confirmed the contract is `Schema.Record(ThreadId, Schema.String)` and `ThreadId` is a plain string. Mobile part: checked in code that `titles.value[ref.threadId] ?? ...` has the same pattern at `entities.ts:72`. Unverified: whether the decoded record has a normal prototype at runtime; not run. |
| S2 | fix (medium) | `apps/mobile/src/state/entities.ts:71` | Non-success lookups return `"Thread"` instead of `null`; `resolveThreadLink` and `relabelThreadLinks` treat it as a found thread, so a v1 link to another environment never reaches `guessThreadLinkRef` | matched T1 and T3 (same defect, same lines as Opus W2) | checked in code (`entities.ts:68-74` shows `"Thread"` for non-success and while waiting; `relabelThreadLinks` takes `title() === undefined`). Not run. |
| S3 | consider (medium) | `apps/web/src/components/ThreadContextChip.tsx:44` | Removing the `shell ? "Open thread" : "Thread no longer available"` branch makes composer and user-message chips for deleted threads say "Open thread" | Sonnet-only vs references; equals Opus W3. Verdict real-minor. | from report (W3 checked in code there); same callers named. |
| S4 | consider (medium), topic question | `apps/web/src/components/chat/MarkdownThreadLink.tsx:56` | A link to an unreachable environment now renders a live "Thread" chip instead of "Thread on another machine" | Sonnet-only vs references; equals Opus W1. Verdict real-minor (UX question; the new browser test asserts the failure state keeps the generic chip). | from report (W1 checked in code there). |
| S5 | consider (medium), topic tests | `apps/mobile/src/state/entities.ts:62` | No test covers the new mobile title-lookup behavior (loading, failure, empty-success) | Sonnet-only; not an Opus finding. Verdict nit: true that the head commit adds only a web browser test and there is no mobile `entities` test file (checked in code), but AGENTS.md also says to test behavior that can break and to avoid duplicating web/mobile cases, so it is a process remark, not a defect. | checked in code (file listing, AGENTS.md lines 105-107). Whether a mobile test is wanted by maintainers: unverified. |

## Opus-only (not found by Sonnet)

- W4 (`MarkdownThreadLink.tsx:56`): one `getThreadTitles` RPC per unloaded link, never cached (`staleTimeMs: 0, idleTtlMs: 0`). Opus verdict: real-minor (cost, nothing breaks). Sonnet did not raise it.
- Reference: T2 is missed by both.

## Sonnet-only (not found by Opus)

- S5: no test for the mobile change. Verdict: nit.
- S1 adds the mobile site of the `Object`-prototype issue, which Opus W5 did not mention. This extends W5; it is not a separate defect. Its basis for the mobile site is the code pattern only, not execution.

Overlap with Opus-only findings from report.md: S1 = W5, S3 = W3, S4 = W1.

## Wrong findings

None, in either run (Opus per report.md; Sonnet per my reading of the code at the head).

## Limits

- One run per model; the model is not deterministic, so another run could differ.
- Sonnet findings were judged by a Claude Sonnet 5.5 subagent reading the code at the replay head (`/tmp/t3bench-32830`). No test was run, nothing was executed. Opus verdicts are taken as given from report.md.
- Confirmed: S2 matches T1/T3 (code read); S1, S3, S4 coincide with Opus findings whose verdicts come from report.md; S5's factual premise (no mobile test in the commit). Unverified: runtime reachability of the `constructor` case (S1, mobile and web); whether maintainers want the S5 test.
- No upstream change confirms any Wachiman-only finding (per report.md).
