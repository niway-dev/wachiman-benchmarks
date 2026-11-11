# Audit of the Cal.com false positives (2026-11-11)

Question: are the Opus findings that the judge matched to no golden ("FP") wrong, or true observations the golden
set does not contain? Scope: Cal.com only, 31 FP on 9 PRs (the tenth PR has none).

**Result [measured, one auditor, not spot-checked by a human]:** 17 of 31 are `real-defect` (a named failing path
with file and line), 14 are `real-minor` (true, low impact), 0 `wrong`, 0 `unverifiable`, 0 duplicates of another
finding. The auditor would expect a maintainer to fix 23 (17 defects + 6 minor), "maybe" 7, "no" 1.

| Cut | real-defect | real-minor |
|---|---|---|
| Wachiman severity blocker or fix | 14 | 0 |
| Wachiman severity consider or info | 3 | 14 |
| Echoed by Haiku within 10 lines | 13 | 9 |
| Not echoed | 4 | 5 |
| Opus scorer, mean score (values) | 6.4 (4 to 9) | 3.3 (2 to 5) |
| Haiku scorer, mean score | 6.8 | 3.9 |

Reading: on this repo the scorer and Wachiman's own severity do separate "defect" from "minor" among the FP. They fail
against the benchmark because the benchmark counts these 17 defects as false positives, the same as the 14 minor ones.

Method: one `gpt-6.1-sol` child (Codex, reasoning effort high) per PR through `delegate_task`, following
[brief.md](brief.md): refute first, then construct the failure, verdict with citations. It saw all findings of the PR
and the diff, on a checkout of the head commit; it was not told which findings matched a golden and was told not to
read the benchmark's reference data. Inputs in `inputs/`, verdicts with evidence in `outputs/`, joined table in
`audit.csv`.

Limits: one auditor, one pass, every verdict "high confidence" and none "wrong", which may be lenient; no human
checked the evidence. A different provider than the reviewer reduces, but does not remove, shared blind spots. Cal.com
is the repo where Opus is most precise; Sentry (54 FP) may look different. Cost not reported by the tool (Codex
subscription).
