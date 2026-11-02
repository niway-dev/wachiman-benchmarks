# Replay benchmark 2026-11-01: Wachiman v1.3.0, Pullfrog and CodeRabbit on five kaipu-record PRs

## In one minute

- **What:** the five kaipu-record PRs of the [2026-10-31 field benchmark](../2026-10-31/README.md)
  (#463–#467), replayed at their exact commits in fresh public repositories and reviewed again:
  Wachiman v1.3.0 three times, Pullfrog twice, CodeRabbit twice. 76 findings were posted across
  the 35 reviews. Each one was checked by reading the code at the head and the later history.
- **Expected issues:** the 26 findings that were verified on 2026-10-31 and still visible at the
  head. They come from Wachiman v1.2.0's and Pullfrog's live reviews, so they lean toward what
  those two look for (17 of them are Wachiman's, mostly test quality). **The fairer measure is the
  real bugs of severity Medium or higher**, whoever found them. There are 14.
- **Result:**

| | Wachiman v1.3.0 | Pullfrog | CodeRabbit |
| --- | --- | --- | --- |
| Runs | 3 | 2 (v1, v2) | 2 (v1, v2) |
| Cost per run, five PRs | **$3.85** (3.59–4.17) | $7.15 (7.07–7.23) | $0 here (public repo); $24–72 per developer per month on private repos |
| Findings posted per run | 15–17 | 9–11 | 3–6 |
| Invalid findings | **0** | 0 | 0 |
| Expected issues found per run (of 26) | **10–11** | 1–4 | 2–3 |
| Real Medium+ bugs found per run (of 14) | 0–3 (avg 1.3) | 3–4 (avg **3.5**) | 2–3 (avg 2.5) |
| Distinct real Medium+ bugs in all its runs | 3 | **5** | 4 |
| Message quality (0–5, mean) | **4.87** | 4.65 | 4.57 |

- **Reading:**
  - Wachiman is the cheapest and finds the most issues in total.
  - Pullfrog finds the most bugs a user would notice: about 2.6 times as many per run as Wachiman,
    for 1.9 times the price.
  - CodeRabbit posts little. What it posts is mostly real, and it found two of the three bugs
    rated High.
  - **Only three real Medium+ bugs were found in every run of a reviewer**, and none of them by
    Wachiman: Pullfrog's superseded camera-on (#463) and Library drop (#467), and CodeRabbit's
    `markCopySeen` (#464), each 2 of 2. Wachiman's best is 2 of 3 (Email listed as Slack, #467).
  - Three real bugs were found by nobody in any replay. Pullfrog had found all three live.
- **What it means for Wachiman:**
  - Its reliable output is test quality and leftovers.
  - The flow questions in the [design](https://github.com/niway-dev/wachiman/blob/main/docs/specs/2026-10-31-flow-questions-and-evidence-design.md)
    target exactly the missing class: follow an action to its effect on the running app.
  - The baseline is now measured: 1.3 real Medium+ bugs per run, at $3.85.

Per-PR analysis, one issue at a time: [`prs/`](prs/). Raw review bodies and comments: [`raw/`](raw/).

## The runs

| Reviewer | Run | Repository | PRs | Date | Notes |
| --- | --- | --- | --- | --- | --- |
| Wachiman v1.3.0 | W-R1 | [kaipu-bench-wachi](https://github.com/niway-dev/kaipu-bench-wachi) | #1–#5 | 11-01 | `/wachi review`; Claude Opus 5.5, effort high (Claude Code default) |
| Wachiman v1.3.0 | W-R2 | same | #6–#10 (`head-r2`) | 11-01 | same commit, new branch: the engine does not re-review a head it marked |
| Wachiman v1.3.0 | W-R3 | same | #11–#15 (`head-r3`) | 11-01 | |
| Pullfrog | PF-v1 | [kaipu-bench-pullfrog](https://github.com/niway-dev/kaipu-bench-pullfrog) | #1–#5 | 11-01 | Opus 5.5, effort high; log says `learnings … existing=no` |
| Pullfrog | PF-v2 | [kaipu-bench-pullfrog-v2](https://github.com/niway-dev/kaipu-bench-pullfrog-v2) | #2–#6 | 11-01 | fresh repository, so no learnings from v1 |
| CodeRabbit | CR-v1 | [kaipu-bench-coderabbit](https://github.com/niway-dev/kaipu-bench-coderabbit) | #1–#5 | 11-01 | plan "Advanced", profile `chill`; started by `@coderabbitai review` |
| CodeRabbit | CR-v2 | [kaipu-bench-coderabbit-v2](https://github.com/niway-dev/kaipu-bench-coderabbit-v2) | #2–#6 | 11-01 | fresh repository |

The live reviews of 2026-10-31 (Wachiman v1.2.0 and Pullfrog on kaipu-record) are not counted as
runs: they produced the expected set.

## The real bugs (severity Medium or High)

Every real bug of severity Medium or higher on these five PRs, whether expected or found for the
first time in a replay. "✓" means found, "~" means a run flagged the same code with a different
or weaker claim, and an empty cell means not found. **Status** gives the author's later fix where
one exists. A later fix is the strongest evidence a bug is real.

| PR | Bug | Sev. | Diff. | Origin | W-R1 | W-R2 | W-R3 | PF-v1 | PF-v2 | CR-v1 | CR-v2 | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #463 | Camera cannot reopen mid-take, so the face is recorded in no file | High | 5 | expected (W live) | | ✓ | | | | | | fixed `b0f028c` |
| #463 | A queued camera-on reopens the camera after a newer off: the camera records while the toggle shows off | High | 4 | expected (P re-review) | | | | ~ | ~ | | ✓ | **still open on main** |
| #463 | The take's first relay feed is ignored, so the face can end up in no file | High | — | new | | | | | | | ✓ | fixed `7155941` |
| #463 | Random gap ids break Share's "already exported, reuse" | Medium | 5 | expected (P live) | | | | ✓ | | | | fixed `29395c3` |
| #463 | A superseded camera-on closes the gap too early, so the editor shows a frozen frame | Medium | — | new | | | | ✓ | ✓ | | | fixed `8609fab` |
| #464 | Show in Finder and drag on the ready card skip `markCopySeen` | Medium | 4 | expected (P live) | | | | | | ✓ | ✓ | fixed `7f28eb97` |
| #465 | The new Drag handle skips `markCopySeen` | Medium | 4 | expected (P live) | | | | | | | | fixed `e2e6e238` |
| #465 | When the file probe fails, five of six destination cards show "…" forever | Medium | — | new | | ✓ | | | ✓ | | | **still open on main** |
| #466 | `show()` returns true before the card renders; a failed load loses the card for the session | Medium | 3 | expected (W live) | | | | | | ✓ | | fixed `1ff66f1b` |
| #466 | Back re-floats the always-on-top ready card | Medium | 5 | expected (P live) | | | | | | | | fixed `84afb264` |
| #467 | Export never re-lists the Library when an export finishes | Medium | 5 | expected (P live) | | | | | | | | fixed `3f7a3557` |
| #467 | A finished Email copy is listed as "Slack · Discord" in Recent exports | Medium | 4 | expected (noticed by hand) | | ✓ | ✓ | | ~ | | | fixed `54a08d37` |
| #467 | A video dropped on the Library navigates the Electron window to the file (no `will-navigate` guard) | Medium | — | new | | | | ✓ | ✓ | | | open; valid by reading, not run |
| #467 | Recent exports labels editor exports as destination copies | Medium | — | new | | | | | ✓ | | | likely still open |
| | **Found in this run** | | | | **0** | **3** | **1** | **3** | **4** | **2** | **3** | |

One more claim is plausible but unconfirmed: on #466, the card's actions may not bring Kaipu to the
front from another app (PF-v2, rated Medium; it would need a run on macOS to confirm).

What the table shows:

1. **Who finds what.**
   - Pullfrog finds the action-to-effect class: where the window goes, what the timeline shows,
     how a label is computed.
   - CodeRabbit finds main-process failure paths (a load that fails, a feed that never delivers)
     and the `markCopySeen` contract.
   - Wachiman found three. All three came from one run (W-R2); the other two runs found one
     between them.
2. **Nobody is reliable.** Three rows are ✓ in every run of one reviewer: Pullfrog on the
   superseded camera-on (#463) and on the Library drop (#467), and CodeRabbit on `markCopySeen`
   (#464). Everything else comes and goes. Pullfrog's random-ids catch, which made it look
   decisive live, came back in 1 of 2 replays.
3. **Three bugs were missed by every replay.** They are `markCopySeen` on #465, Back re-floats on
   #466 and Export never re-lists on #467. All three need cross-file reasoning, all three were
   Pullfrog's live catches, and the author fixed all three. They are the hardest test for the
   next Wachiman version.
4. **#463 holds all three High bugs, and CodeRabbit v2 found two of them.** One, the camera that
   reopens after a newer off, is still open on `main`. The other, the ignored first feed, was
   fixed by the author without any reviewer flagging it live. Wachiman found the third, once in
   three runs.

## All expected issues, by run

The 26 expected issues that can be caught at the head, by severity. One more expected issue on
#464, the "For chat" tag on Email copies, was introduced by a later commit, `da6d41b`. It is not
in the head and is not counted.

| Severity | Expected | W-R1 | W-R2 | W-R3 | PF-v1 | PF-v2 | CR-v1 | CR-v2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| High | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| Medium | 7 | 0 | 1 | 1 | 1 | 0 | 2 | 1 |
| Low | 15 | 9 | 6 | 8 | 2 | 1 | 0 | 1 |
| Info | 2 | 1 | 2 | 2 | 1 | 0 | 0 | 0 |
| **Total** | **26** | **10** | **10** | **11** | **4** | **1** | **2** | **3** |

By PR (found / expected):

| PR | Expected | W-R1 | W-R2 | W-R3 | PF-v1 | PF-v2 | CR-v1 | CR-v2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #463 | 6 | 2 | 3 | 2 | 1 | 0 | 0 | 1 |
| #464 | 3 | 1 | 0 | 1 | 1 | 1 | 1 | 2 |
| #465 | 3 | 2 | 2 | 2 | 0 | 0 | 0 | 0 |
| #466 | 4 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| #467 | 10 | 5 | 4 | 6 | 1 | 0 | 0 | 0 |

Wachiman's 10–11 are mostly the Low test-quality issues it found itself live. It finds them
again run after run: on #465 its two expected tests appear in all three runs, and on #467 the
two test findings and the CSS comment do too. That is real value, but it is the cheapest part of
a review to lose.

## Everything posted, by run

| Run | Posted | Valid | Partly valid | Unconfirmed | Invalid | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| W-R1 | 15 | 13 | 2 | 0 | 0 | $3.80 |
| W-R2 | 15 | 15 | 0 | 0 | 0 | $3.59 |
| W-R3 | 17 | 15 | 2 | 0 | 0 | $4.17 |
| PF-v1 | 9 | 7 | 1 | 1 | 0 | $7.23 |
| PF-v2 | 11 | 7 | 3 | 1 | 0 | $7.07 |
| CR-v1 | 3 | 2 | 1 | 0 | 0 | not billed (public repo) |
| CR-v2 | 6 | 5 | 1 | 0 | 0 | not billed (public repo) |

"Partly valid" means the code does what the finding says, but the effect is narrower than claimed,
only a future risk, or contradicted by a documented design choice. No reviewer posted a false
finding in 35 reviews. Counts include findings written only in a review body, not inline.

New issues (not in the expected set) that each reviewer found, all runs together:

| Reviewer | Distinct new issues | Valid | Of which Medium+ | Partly valid / unconfirmed |
| --- | --- | --- | --- | --- |
| Wachiman | 11 | 8 | 1 (#465 "…" forever) | 3 |
| Pullfrog | 12 | 7 | 4 | 5 |
| CodeRabbit | 4 | 2 | 1 (#463 ignored first feed, High) | 2 |

## Cost

| PR | Size (files, lines changed) | Wachiman, mean of 3 | Pullfrog, mean of 2 | CodeRabbit |
| --- | --- | --- | --- | --- |
| #463 | 26, 1,966 | $0.62 | $1.87 | — |
| #464 | 31, 1,298 | $0.51 | $1.12 | — |
| #465 | 14, 1,615 | $0.53 | $1.17 | — |
| #466 | 28, 1,297 | $0.57 | $1.36 | — |
| #467 | 47, 4,853 | $1.63 | $1.64 | — |
| **Five PRs** | 146, 11,029 | **$3.85** | **$7.15** | — |
| Per 1,000 changed lines | | $0.35 | $0.65 | — |
| Per valid finding | | $0.27 | $1.02 | — |
| Per real Medium+ bug found | | $2.89 | $2.04 | — |

- **Wachiman** reads every changed file in every run, so its cost follows the size of the PR:
  #467 costs 3 times #464. Pullfrog's cost is nearly flat ($1.12–$1.87), because it decides
  how far to read.
- **Per real bug, Pullfrog is cheaper.** Per finding of any kind, Wachiman is four times cheaper.
  Which number matters depends on what the review is for. A reviewer that misses the bug a user
  would hit is expensive at any price.
- **CodeRabbit** does not bill public repositories and shows the consumer no per-review cost. On
  private repositories it is seat-based: $24, $48 or $72 per developer per month on annual billing
  (Essentials, Team, Advanced; [pricing page](https://www.coderabbit.ai/pricing), read
  2026-11-01). These reviews ran on the Advanced plan. A per-PR figure cannot be derived.
  Wachiman and Pullfrog charge the consumer's own API key per token.

## How well the findings were explained

Each finding that caught an expected issue or a valid new one was scored 0–5, one point each:

- **Effect:** says what the user or developer will experience.
- **Location:** gives the exact file and line.
- **Cause:** explains why, with evidence from the code.
- **Fix:** gives an actionable fix.
- **Signal:** the severity is in proportion, and there is no padding.

| Reviewer | Scored messages | Mean | 5/5 | Where points were lost |
| --- | --- | --- | --- | --- |
| Wachiman | 45 | **4.87** | 39 | Signal. It labels comment-only issues "Fix" (the orphaned CSS comment, misplaced JSDoc). It also labelled #463's face loss only "Consider". |
| Pullfrog | 17 | 4.65 | 13 | It overstates unverified claims: an IMPORTANT banner on "most likely" (#466 bring-to-front) and a panel flip on #465 that the head's loader hides. A suggestion block dropped a line and needed a correction comment. |
| CodeRabbit | 7 | 4.57 | 4 | Padding: raw dumps of its own shell scripts inside the comment. Under-calling: the ignored first feed, where the face can be lost, rated "Minor". |

All three write well. The messages name the user effect, cite lines and propose a fix. The
differences are in severity labels and noise, not in clarity. Examples, from
[`prs/`](prs/):

- Wachiman, #465: "every card except Archive keeps the loading ellipsis forever".
- Pullfrog, #467: "Electron navigate the window to `file://…/clip.mp4` and replaces the app".
- CodeRabbit, #463: "can record webcam frames while the camera setting is off".

## Limits and biases

- **The expected set favours the live reviewers.** It is the verified output of Wachiman v1.2.0
  and Pullfrog on 2026-10-31. CodeRabbit had no say in it. That is why the Medium+ table counts
  new bugs as well.
- **Verdicts come from reading code, not from running the app.** Five subagents (Claude Sonnet
  5.5) checked every finding against the code at the head and against `origin/main`, one PR each.
  Where only a run of the app could confirm a finding, it is marked "by reading" or
  "unconfirmed". Severities and difficulties are their judgment, using the scale in each
  [`prs/`](prs/) file.
- **Small sample.** Five PRs, two or three runs per reviewer. Every per-run figure moves by a
  bug or two from one run to the next. Read a cell as "found in k of n runs", not as a rate.
- **CodeRabbit ran with kaipu-record's own configuration.** It reads `.coderabbit.yaml` from the PR's
  head commit, so the replayed file applied: profile `chill`, Markdown and lockfiles excluded,
  auto review limited to `production` and `master`. That last rule is why every review was started
  with `@coderabbitai review`. It cannot be changed without rewriting the replayed commits.
- **A correction to the 2026-10-31 report.** [`pr-465.md`](../2026-10-31/pr-465.md) says none of its
  three findings was fixed later. All three were, in `e2e6e238`, which cites the review comments.

## Method

- Every replay branch is a real kaipu-record commit, so each PR's diff is byte-identical to the
  original. Each repository's `main` holds only a README and the reviewer's configuration.
  Branches and SHAs: [kaipu-bench-wachi README](https://github.com/niway-dev/kaipu-bench-wachi).
- Wachiman was started with `/wachi review`. A `pull_request` event would have run the replayed
  commits' own `agent-review.yml` (v1.2.0), and that workflow and `pr-checks.yml` are disabled
  in every benchmark repository. `/wachi review` goes through the same `review()` as the
  automatic job, with the same budgets and model (`src/cli.ts:121-122`, `src/engine.ts:1688`).
- Pullfrog and CodeRabbit keep per-repository memory, so their second runs are in fresh
  repositories. Wachiman keeps none, so its repeat runs use `head-r2`/`head-r3` branches on the
  same commit.
- **Effort:** Wachiman's adapter sets none, so Claude Code's default applied, which is `high` for
  API-key users since 2.1.94. Pullfrog logs `effort: high (default)`. PR #56 makes effort an
  explicit, logged input.
- Costs: Wachiman's from its review footers; Pullfrog's from the usage table in each run log
  ([`raw/pullfrog-v2-costs.txt`](raw/pullfrog-v2-costs.txt); v1 from its tool-call logs).
- Scripts: [`../replay/`](../replay/).
