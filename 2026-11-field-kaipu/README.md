# Field run: Haiku proposes, Opus and Sonnet verify, on live kaipu-record PRs (November 2026)

Status: **collecting, draft.** Raw material for the month-end analysis; no conclusion is drawn here.

## What runs

Once a day, on the owner's laptop, [`harness/field-run.sh`](harness/field-run.sh) reviews every
kaipu-record pull request opened since 2026-11-06 that has no run yet:

1. **Propose.** Wachiman v1.8.0, `agent-review local`, Haiku 5.5 at effort high, unchanged.
2. **Filter, with code, at no cost** ([`harness/verify.py`](harness/verify.py)): drop a finding
   whose cited file or line does not exist at the commit, and a near-duplicate (same file, within
   three lines, similar title).
3. **Verify.** The same candidates go to Opus 5.5 high and to Sonnet 5.5 high, **one call each per
   PR**. Each gets the diff, every candidate with 15 lines of code around its cited line, and
   read-only access to the snapshot (Read, Glob, Grep; 15 turns, $1.50 cap). Each answers keep or
   drop, with a severity and a reason.
4. **CodeRabbit.** Its inline comments and reviews on the PR are saved next to ours.

Haiku runs once per PR; only the verification step is doubled.

- **Which commit.** The first commit CodeRabbit reviewed, so both reviewers read the same code. A
  PR CodeRabbit has not reviewed after 24 hours is reviewed at its head, and its summary says so.
- **Where it runs.** Locally on the claude.ai subscription. The script refuses `ANTHROPIC_API_KEY`,
  so no API credit is spent. Every dollar figure is Claude Code's API-equivalent estimate.
- **Nothing is posted** to kaipu-record. Wachiman's own CI workflow there is separate and unchanged
  by this run.
- **Schedule.** launchd, daily at 23:00 local time ([`harness/dev.niway.wachi-field.plist`](harness/dev.niway.wachi-field.plist)).
  A run missed while the laptop sleeps starts when it wakes.

- **Notification.** macOS shows a notification with a sound when the run starts and when it ends,
  with how many PRs were reviewed, any failures, and the night's estimate.

## To watch

- **Small PRs may cost more with a verifier than Opus alone.** On #535 (84 changed lines) Haiku took
  35 turns: Haiku plus the Opus verifier was $0.58, against $0.51 for the live Opus review of the same
  commit; Haiku plus Sonnet was $0.41. One PR; check the trend by size at month end.

## Month-end analysis (planned, not done)

- Against CodeRabbit: what it found that we did not (a gap), and what we found that it did not.
- Opus against Sonnet as the verifier: real findings each kept or dropped, and cost.
- Every finding on both sides judged valid, invalid or uncertain, with later fixes as evidence.
  The judge is to be chosen then.

## Runs

Each row links the PR's summary: cost and work per step, every candidate with both verdicts, and
the reasons.

<!-- runs:begin -->

| PR | Commit | Run | Size | Haiku candidates | Opus keeps | Sonnet keeps | CodeRabbit comments | Haiku | Opus verify | Sonnet verify |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [#535](runs/pr-535/summary.md) | `1fb882cd` | 2026-11-06 | 6 f, +68/−16 | 7 | 5 | 4 | 1 | $0.25 | $0.33 | $0.16 |
| **1 PRs** | | | | | | | | **$0.25** | **$0.33** | **$0.16** |

<!-- runs:end -->
