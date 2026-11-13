# Sonnet 5.5 high vs Opus 5.5 high on the t3code#30579 replay

## Summary (one minute)

Same Wachiman 1.12.0, same head commit, same flags; only the model changed. Judged by a Claude Sonnet 5.5 subagent that read the code at `/tmp/t3bench-30579` (HEAD). No tests were run.

- Sonnet made 6 findings. 3 match reference threads: S1 = T4, S2 = T2/T6, S3 = T5. No finding is partial.
- Sonnet found T5, which Opus never found in 3 runs. It missed T1 (Opus run 1 found it) and T8 (Opus run 3 found it). T3 is missed by everyone.
- Reachable real defects at head: 6 (T1, T2/T6, T3, T4, T5, T8). Sonnet found 3 of 6 (T2/T6, T4, T5). Opus run 1 found 2 of 6 (T1, T2/T6). The Opus 3-run union found 4 of 6 (T1, T2/T6, T4, T8).
- Union of Opus (3 runs) plus Sonnet covers 5 of 6; only T3 is never found.
- Sonnet-only findings: S4 (real-minor), S5 (same as Opus N1, real-minor), S6 (nit). None judged wrong.
- Sonnet cost $0.413 and 21 turns, 13,187 output tokens, 125 s review call. Opus run 1: $0.568, 9 turns, 5,331 output tokens, 57 s.
- Sonnet ranked T4 and T2 as `fix`, and T5 as `consider`.

## Reference threads (real-bug or real-minor, catchable at head)

T7 (wrong, disputed) is excluded. T9 is excluded because it is not reachable at head (`ee55f44a` added the code after the head). Reachability of T8 is inferred in `report.md`, not checked.

| T# | Verdict | Opus run 1 | Opus 3-run union | Sonnet |
| --- | --- | --- | --- | --- |
| T1 Timeline "Add to chat" ignores `reviewThreads`-only comments | real-bug | found (W1, fix) | found (runs 1, 2) | missed |
| T2 PR reference dedupe by number, not URL | real-bug | found (W2, medium) | found (runs 1, 2, 3) | found, S2 (fix, medium confidence) |
| T3 `readableBody` drops text after an unclosed `<!--` | real-minor | missed | missed | missed (S1 reports only the empty-return consequence, i.e. T4) |
| T4 Return `null` when parsing removes the whole body | real-minor | missed | found (runs 2, 3) | found, S1 (fix, high) |
| T5 Scope comment chip ids to the PR | real-minor | missed | missed | found, S3 (consider) |
| T6 same defect as T2 (duplicate) | real-bug | found (with T2) | found | found (with S2) |
| T8 Keep a durable PR reference when a hand-off chip exists | real-minor | missed | found (run 3) | missed (S2 names only the number-versus-URL collision) |

## Sonnet findings

Basis column: "checked" means I read the cited code at the head. "report" means I relied on the existing Opus report's check.

| S# | Severity | path:line | Claim | Match or verdict | Basis |
| --- | --- | --- | --- | --- | --- |
| S1 | fix | `pullRequestDetail.logic.ts:709` | `readableBody` returns `""` not `null` for a body that is only an unclosed `<!--`, so a hollow chip is added | matched T4 (same defect, same fix) | checked against T4 text and `report.md` (head `:709` returns the joined string); the "buttons gated on `visibleBody !== null`" part checked at `PullRequestReviewAnnotation.tsx:255` |
| S2 | fix | `PullRequestDetailPanel.tsx:1077` | `hasPullRequest` compares number only; same `#N` from another repository suppresses the PR reference | matched T2/T6 (same defect, same fix: compare URL). Not T8: the hand-off chip sweep is not mentioned | checked (`:1077-1079` compares `pullRequest?.number`) |
| S3 | consider | `pullRequestDetail.logic.ts:1164` | Chip id `pr-comment:<commentId>` is not scoped to the PR, so a same-id comment from another PR overwrites a chip | matched T5 (same defect, same fix) | checked against T5 text and `report.md`; the line shifted (`:1157` in the thread, `:1164` here) but is the same id construction. I did not re-open the `composerDraftStore` replace-by-id claim |
| S4 | consider | `PullRequestTimelineTab.tsx:272` | Timeline renders Add to chat on every thread reply, but the panel adds the whole thread; Summary tab hides it on replies | Sonnet-only: real-minor (inconsistent behaviour, not a crash) | checked: `PullRequestSummaryTab.tsx:~603` skips replies (`reply ? null : chatSubject`); Timeline renders `ConversationCard` with `AddToChatButton` for each reply (`:272`, `:~472`); `addCommentToChat` looks up the containing thread (`PullRequestDetailPanel.tsx:1064-1071`). Whether the owners consider this intended is unknown |
| S5 | consider | `PullRequestReviewAnnotation.tsx:270` | Resolve's `ml-auto` follows `onAddToChat`, but Add to chat renders only if a comment has visible text | Sonnet-only: real-minor (cosmetic). Same as Opus N1 | checked: `:255` conditional render, `:270` class tests `onFix \|\| onAddToChat` |
| S6 | consider | `pullRequestDetail.logic.test.ts:1017` | `reviewThreadContext` now uses `readableBody`, changing Fix hand-off text; tests do not cover it (nor the unclosed `<!--` case) | Sonnet-only: nit (test-coverage remark) | partly checked: `logic.ts:855` uses `readableBody` where the old code used `visibleBody` (git diff of HEAD^..HEAD). The "no test covers it" claim is unverified; I only saw the `buildPullRequestCommentContext` tests, not every test of `reviewThreadContext` |

## Opus-only (not found by Sonnet)

- T1 (real-bug): Opus run 1 and run 2 found it. Sonnet missed it. This is the most serious gap in this comparison, but Opus itself missed T1 in run 3, so it is not a stable difference.
- T8 (real-minor): Opus run 3 only.
- Opus extras: N1 is also found by Sonnet (S5). N2 (Summary-tab Add to chat sends only the first page of a thread's replies, run 3) is not found by Sonnet; N2 is unverified (see `experiments/README.md`).

## Sonnet-only

- T5 (S3): a reference thread that no Opus run found.
- S4: real-minor, no reference thread, no Opus equivalent.
- S6: nit, no reference thread, no Opus equivalent.
- S5 is Sonnet-only against run 1 and the references, but it equals Opus N1 (run 2).

## Wrong findings

None judged wrong, for Sonnet or for Opus (N2 is unverified, not wrong).

## Limits

- One Sonnet run against three Opus runs. The Opus runs already moved between 2 and 3 of 6 defects, so a 3/6 Sonnet result is within that spread. This does not show that Sonnet is better or worse.
- Matching and verdicts for S1..S6 were judged by a Claude Sonnet 5.5 subagent that read the code at the head. No tests were run and Wachiman was not re-run.
- Reference-thread verdicts and Opus results come from `bot-threads.md`, `report.md` and `experiments/README.md` and were not re-judged.
- Unverified: S3's replace-by-id claim in `composerDraftStore.ts`, S6's "no test covers it", and whether S4 is intended behaviour. T8 reachability at head is inferred in `report.md`.
- Sonnet's Wachiman run used the same snapshot flow. I did not compare timing beyond the figures in the JSON files.
