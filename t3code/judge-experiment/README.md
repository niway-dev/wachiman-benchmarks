# Hazard judge: a second model call that attacks the reviewer's own contract notes

Run on 2026-11-13. Result in one line: **on 13 new escaped t3code bugs the first reviewer (Wachiman 1.14.0, Sonnet 5.5 high) caught 1. Adding a Sonnet 5.5 high judge brought it to 3, for $0.42 more per review. Running the reviewer a second time, at about the same cost, brought it to 1. No judge configuration caught more than 2 extra, and on the 5 earlier cases every configuration caught only #19432.** One run per cell and 13 cases, so two hits against zero is a signal, not a measurement.

## One-minute table

New cases (13, the result that counts) and the 5 known cases (in-sample: the prompt was revised once after seeing them). "Hits" are bugs the judge stated that the first reviewer did not: the first reviewer alone caught 1 of 13 new cases (#21046) and 0 of 5 known ones, in both stored arms. Alarms are `breaks` verdicts that are not the golden, per review. "Wrong" means the scenario is not reachable or misreads the code. Cost is the CLI's API-price figure (subscription runs, so an estimate, not a bill).

| second reviewer | hits on new cases (of 13) | hits on 5 known (arm A / arm C inputs) | new alarms per review (new cases) | wrong alarms (new cases) | cost per review | time per review |
| --- | --- | --- | --- | --- | --- | --- |
| judge, Opus 5.5 high | 2 (#14892, #29838) | 1 / 1 (#19432) | 0.62 | 0 of 8 | $1.15 | 209 s |
| judge, Opus 5.5 medium | 1 (#29838) | 0 / 1 | 0.23 | 0 of 3 | $0.53 | 101 s |
| **judge, Sonnet 5.5 high** | **2 (#25239, #29838)** | 1 / 1 | 0.46 | 0 of 6 | **$0.42** | 130 s |
| judge, Sonnet 5.5 medium | 0 | 1 / 1 | 0.00 | 0 of 0 | $0.09 | 24 s |
| judge, Haiku 5.5 high | 2 (#25239, #29838) | 1 / 0 | 1.23 | 0 of 16 | $0.20 | 277 s |
| control: the same review run again | 0 | not run | 0.85 | 4 of 11 | $0.47 | 153 s |

**Answer: use Sonnet 5.5 high as the second reviewer, as a judge over the first reviewer's contract notes, not as a second plain review.** See [Which model for the second reviewer](#which-model-for-the-second-reviewer) for what is checked and what is inferred.

## Question

On 5 valid escaped bugs of pingdotgg/t3code (cross-file contract, ordering, state), local Wachiman caught 0 to 1 per arm, and adding questions did not help ([`../contract-order-experiment/README.md`](../contract-order-experiment/README.md)). The diagnosis there: the reviewer often had the far side of the boundary in hand and did not report the bug. Twice it wrote the hazard in its `contracts` notes and judged it fine. So the gap is in judging what was read.

The idea under test is a "hazard judge". It is a second model call per review that receives the first reviewer's `contracts` notes as hypotheses, plus its findings so it does not repeat them. For each note it must read the code at the reviewed commit and give one verdict:

- `breaks`: the concrete input or ordering that breaks it (scenario, file:line, consequence, severity);
- `safe`: the line that makes it safe;
- `cannot_tell`: what is missing.

It may also raise hazards the notes imply. This differs from Wachiman's verifier (wachiman ADR 0027), which only refutes findings. It is also meant to answer wachiman ADR 0009's objection that a pass over conclusions "ratifies the gap": the judge has to read code, not summaries. [#22107](#did-the-judge-read-the-other-side-pr-22107) tests that directly.

The owner's question: the default reviewer is Sonnet 5.5 high because it finds the same as Opus for about 40% less. That margin could pay for a second reviewer. Which model should it be?

## Setup

- **Repository:** the fork niway-dev/t3code of pingdotgg/t3code, cloned in full to `/tmp/t3code-fork`. Main at the time: `4fd40e1a16e3800418b8f6a32932b68179098c8d`. Each judge call reads a detached worktree of the reviewed commit (`/tmp/t3code-judge/wt-<sha12>`).
- **Judge driver:** [`judge.py`](judge.py). It makes one `claude -p` call per (input run, judge config), skips outputs that already exist, and logs failures and continues. Calls run one at a time.
- **Call shape:** the call mirrors the wachiman engine's reviewer call (`src/providers/claude-code.ts` on wachiman `origin/main` at [`aef4422`](https://github.com/niway-dev/wachiman/commit/aef442293e0c5c56366078dd236c001f3c2b4e68)):
  - `--model`, `--effort`, `--max-budget-usd 5`, `--restricted --strict-mcp-config`;
  - tools `Read,Grep,Glob` only, Bash disallowed;
  - the engine's settings file (copied here as [`claude-code.settings.json`](claude-code.settings.json)), `--no-session-persistence`;
  - `--output-format json` with a `--json-schema` for the verdicts;
  - prompt on stdin, `CLAUDE_CONFIG_DIR=~/.wachiman/claude-personal` (the `isolated:personal` profile), `ANTHROPIC_API_KEY` removed.
- **Deviation from the brief:** the brief asked for working directory = the checkout. The engine instead starts Claude Code in an empty scratch directory and passes the checkout as `--add-dir`, so the repository's `CLAUDE.md`/`AGENTS.md` are not loaded. t3code has both, and the first reviewer never saw them. The judge does the same, so the checkout is its file root but not its process cwd.
- **Judge inputs:** the reviewed commit, its parent, the title, the changed files, the path of the full diff (written to `/tmp/t3code-judge/diffs/`), the first reviewer's findings (index, location, title, body), and its `contracts` entries verbatim.
- **Configs (all five, same prompt):** `opus-high`, `opus-medium`, `sonnet-high`, `sonnet-medium`, `haiku-high` (`claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`). Claude Code also bills a small Haiku share on every call; it is included in the cost.
- **Baseline reviewer:** local Wachiman at wachiman `origin/main` = [`aef4422`](https://github.com/niway-dev/wachiman/commit/aef442293e0c5c56366078dd236c001f3c2b4e68) (version 1.14.0), in a separate worktree. It ran with product defaults (Sonnet 5.5 high), one run per case, using [`baseline.sh`](baseline.sh): `env -u ANTHROPIC_API_KEY WACHIMAN_DIR=<worktree> wachiman local --repo-dir /tmp/t3code-fork --commit <squash sha> --profile isolated:personal --format json --output <file>`. One local, uncommitted change, the same as in the earlier experiment: `TIMEOUT_MS` in `src/connectors/local-git.ts` raised from 60 000 to 300 000 (wachiman issue #193, the t3code snapshot times out). It is still 60 000 on 1.14.0.

### Prompt: v1, one revision, v2 frozen

[`judge-prompt-v1.md`](judge-prompt-v1.md) was written before any judge output. After one pass of Sonnet high over the 14 phase-1 inputs ([`runs/v1/`](runs/v1/)), it was revised once into [`judge-prompt-v2.md`](judge-prompt-v2.md) and frozen. `judge-prompt.md` equals v2. What changed and why:

1. **`safe_line` became required.** In v1, 12 of 23 `safe` verdicts left `safe_line` empty and put lines only in `evidence`, so the rule "no `safe` without a cited line" could not be checked. v2 requires the field and the case tried. In the v2 Sonnet-high pass, 0 of 24 `safe` verdicts lack it.
2. **"It keeps the previous behaviour", "it takes the default path" and "the other side handles it" are no longer accepted as reasons.** The judge must state what that path does in the scenario it tried. This was prompted by v1's C-#22107 output, which repeated the first reviewer's dismissal ("undefined keeps the old grace-only path"). This makes the revision **in-sample** for the known cases. It names no bug, file or class, but it was written after seeing one. The new cases (phase 3) were not seen before the freeze.

Neither prompt names these bugs, their files or their classes beyond "concrete input, state, or ordering of events".

## Cases

- **Phase 1 (in-sample, 14 inputs):** the stored arm A and arm C runs of the 7 earlier cases ([`goldens-known.md`](goldens-known.md)). 5 are valid goldens. [#7599](https://github.com/pingdotgg/t3code/pull/7599) and [#21315](https://github.com/pingdotgg/t3code/pull/21315) are controls whose diff does not add the bug, so any `breaks` there is a new alarm.
- **Phase 2/3 (out-of-sample, 13 cases):** [`cases-new.tsv`](cases-new.tsv), with evidence in [`cases-new-notes.md`](cases-new-notes.md).
  - Picked by a worker from `../catalogue.md`, `../replay-shortlist.md` and `../batches/`.
  - Each case is a race, ordering, state-machine or cross-file-contract bug.
  - The introducing PR was merged to main with at most 17 files (the limit was 40).
  - No bot comment on the defect at the introducing PR.
  - **The defect's line, or the omission, is in the introducing diff's added lines.** This was checked per case in the clone, and the added line is quoted in the `note` column.
  - Goldens were written from the fix PR's diff before any review ran.
  - `cases.tsv` is not on `origin/main` (the `docs/t3code-index` branch has not merged), so the brief's fallback columns are used.
- **The two candidate replacements from the earlier Golden check:**
  - [#14892](https://github.com/pingdotgg/t3code/pull/14892) is admitted. It adds both the `filterIgnoredPaths(input.cwd, ["."])` probe (`GitVcsDriver.ts:969`) and the `workspaceIgnored ? "-u" : "-A"` consumer (`:1038`).
  - [#19291](https://github.com/pingdotgg/t3code/pull/19291) is rejected: it changes 46 files.
- **Weaker cases:** #16926, #33511 and #29909 read more like feature gaps than regressions. In #16926 the added comment calls the behaviour intended. They are kept and counted.

| id | intro PR | class | fix PR | first review, run 1 | run 2 |
| --- | --- | --- | --- | --- | --- |
| checkpoint-ignore-probe-drops-untracked | [#14892](https://github.com/pingdotgg/t3code/pull/14892) | cross-file contract | [#32374](https://github.com/pingdotgg/t3code/pull/32374) | noted, not reported | noted, not reported |
| delegated-followup-self-queued-run | [#17696](https://github.com/pingdotgg/t3code/pull/17696) | state machine | [#32504](https://github.com/pingdotgg/t3code/pull/32504) | missed | missed |
| local-refresh-writes-null-remote | [#21046](https://github.com/pingdotgg/t3code/pull/21046) | state machine | [#33263](https://github.com/pingdotgg/t3code/pull/33263) | **caught** | **caught** |
| usage-resume-agent-cancelled-on-restart | [#29838](https://github.com/pingdotgg/t3code/pull/29838) | cross-file contract | [#31292](https://github.com/pingdotgg/t3code/pull/31292) | missed | missed |
| compaction-steer-client-server-split | [#15631](https://github.com/pingdotgg/t3code/pull/15631) | cross-file contract | [#24138](https://github.com/pingdotgg/t3code/pull/24138) | missed | missed |
| settle-after-run-dropped-by-new-run | [#17145](https://github.com/pingdotgg/t3code/pull/17145) | race | [#31815](https://github.com/pingdotgg/t3code/pull/31815) | partial | partial |
| live-buffer-charged-before-coalescing | [#9715](https://github.com/pingdotgg/t3code/pull/9715) | ordering | [#16317](https://github.com/pingdotgg/t3code/pull/16317) | missed | missed |
| goal-command-notice-not-steered | [#29909](https://github.com/pingdotgg/t3code/pull/29909) | state machine | [#33268](https://github.com/pingdotgg/t3code/pull/33268) | missed | missed |
| auto-resume-arms-archived-parent-subagents | [#27951](https://github.com/pingdotgg/t3code/pull/27951) | state machine | [#30363](https://github.com/pingdotgg/t3code/pull/30363) | missed | missed |
| ssh-prompt-queue-never-settles | [#25239](https://github.com/pingdotgg/t3code/pull/25239) | cross-file contract | [#34192](https://github.com/pingdotgg/t3code/pull/34192) | noted, not reported | noted, not reported |
| notification-key-ignores-new-request | [#24760](https://github.com/pingdotgg/t3code/pull/24760) | state machine | [#32719](https://github.com/pingdotgg/t3code/pull/32719) | missed | missed |
| restart-send-to-ended-run-errors | [#16926](https://github.com/pingdotgg/t3code/pull/16926) | state machine | [#32899](https://github.com/pingdotgg/t3code/pull/32899) | noted, not reported | noted, not reported |
| model-refresh-keeps-latest-version-cache | [#33511](https://github.com/pingdotgg/t3code/pull/33511) | cross-file contract | [#33515](https://github.com/pingdotgg/t3code/pull/33515) | missed | missed |

## Results

### Hits per config

A hit is a `breaks` verdict that names the golden's cause: the same cause, not only the same file. A different trigger with the same cause counts as a hit (see [Scoring notes](#scoring-notes)).

| config | new cases (of 13) | partial, new | known, arm A inputs (of 5) | known, arm C inputs (of 5) |
| --- | --- | --- | --- | --- |
| first reviewer alone | 1 (#21046) | 1 | 0 (+1 partial, #33632) | 0 |
| opus-high | 2 (#14892, #29838) | 3 | 1 (#19432) + 1 partial | 1 (#19432) + 1 partial (#33632) |
| opus-medium | 1 (#29838) | 3 | 0 + 1 partial | 1 (#19432) + 1 partial (#33632) |
| sonnet-high | 2 (#25239, #29838) | 1 | 1 (#19432) | 1 (#19432) + 3 partial (#22107, #33632, #19432 variant) |
| sonnet-medium | 0 | 1 | 1 (#19432) | 1 (#19432) |
| haiku-high | 2 (#25239, #29838) | 5 | 1 (#19432) + 2 partial | 0 + 1 partial |

With the first reviewer's own catch, reviewer + judge reaches **3 of 13** new cases with Opus high, Sonnet high or Haiku high, 2 with Opus medium, and 1 with Sonnet medium. None of the judge hits is #21046, which the reviewer already caught. Of the 5 known cases, every config hits only #19432. #18505, #19355 and #22107 are hit by none, and #33632 only partially, as before.

Where the hits come from:

- **#14892 and #25239** are cases the first reviewer had **noted and judged fine** in its `contracts`. That is the pattern the judge was built for.
- **#29838** was missed by the first reviewer in both runs. Its single contract note sits at `UsageLimitRecoveryWorker.ts:76`. Four of five judges followed it to the startup-recovery filter that keeps only `createdBy === "user"` messages.

### New alarms

Every `breaks` that is not a hit or a partial is a new alarm. Each distinct alarm was checked against the code at the reviewed commit, the fork's main and the later history, and put in one class:

- `real-fixed`: real, and a later commit changes the code;
- `real-present`: real and still at main;
- `minor`: negligible effect, or pre-existing behaviour the change did not touch;
- `wrong`: not reachable, or misreads the code.

Files: [`alarms-phase1.tsv`](alarms-phase1.tsv) and [`alarms-phase3.tsv`](alarms-phase3.tsv).

| config | new cases: alarms (per review) | real-fixed / real-present / minor / wrong | known cases: alarms (per input, of 14) | real-fixed / real-present / minor / wrong |
| --- | --- | --- | --- | --- |
| opus-high | 8 (0.62) | 2 / 0 / 6 / 0 | 11 (0.79) | 3 / 5 / 3 / 0 |
| opus-medium | 3 (0.23) | 1 / 0 / 2 / 0 | 7 (0.50) | 3 / 2 / 1 / 1 |
| sonnet-high | 6 (0.46) | 1 / 0 / 5 / 0 | 11 (0.79) | 3 / 2 / 6 / 0 |
| sonnet-medium | 0 (0.00) | - | 1 (0.07) | 1 / 0 / 0 / 0 |
| haiku-high | 16 (1.23) | 0 / 1 / 15 / 0 | 29 (2.07) | 5 / 6 / 16 / 2 |
| control: run 2's findings not in run 1 | 11 (0.85) | 0 / 0 / 7 / 4 | - | - |

- **The owner's criterion ("at most 1 new false alarm per PR") holds for every judge config.** No judge alarm on the new cases was classed `wrong`. On the known cases there were 3 wrong in 70 calls. If `minor` also counts as a false alarm, only Haiku high goes over (1.15 per review on new cases).
- **Real alarms later fixed upstream.** Distinct alarms:
  - Phase 1: [`e9bd77e`](https://github.com/pingdotgg/t3code/commit/e9bd77ea2ff9811b023029a2dad1d8d559ffe389) (#16580) and [`8653c8f`](https://github.com/pingdotgg/t3code/commit/8653c8f09bb691e4ebdd1a2e62258f8911873ac7) (#20446) on #18505, and [`849d2b5`](https://github.com/pingdotgg/t3code/commit/849d2b5ac8fc9b1a891f0115f030c73d672ec646) (#24258) on #22107.
  - Phase 3: [`321b86b`](https://github.com/pingdotgg/t3code/commit/321b86b05d9c1c59df044fbc0b8a39f0b983c209) on #17696, [`94827737`](https://github.com/pingdotgg/t3code/commit/94827737ea018902dd2e932cddb51643365dc446) and [`ce4712d`](https://github.com/pingdotgg/t3code/commit/ce4712d5b04fb998f79fe132245289191147e5d5) on #9715, [`20081ef`](https://github.com/pingdotgg/t3code/commit/20081ef95f78b17c1f0e8d9be8bacf28b191bdc9) on #27951.
  - Partials whose real bug was fixed later: [`a22068f`](https://github.com/pingdotgg/t3code/commit/a22068f3716bf6f0b1ae8ad53ac69bc7ea8fcafe) on #21046 and `dd5b5401e1` on #25239 (short sha as recorded by the worker).
- **Controls #7599 and #21315** drew 9 alarm rows over 14 calls: 7 distinct, 6 minor, 1 wrong. The judge did not invent the moved goldens there.

### Control: the reviewer run twice

This control exists because repeated runs of one PR already differed in the earlier replays: 2, 3 and 3 of 6 on [#30579](https://github.com/pingdotgg/t3code/pull/30579), with a union of 4. A judge is worth building only if it beats a second run at the same cost.

- **Setup:** the same 13 cases, the same wachiman commit, defaults and command. Outputs in [`runs/baseline-run2/`](runs/baseline-run2/), scores in [`baseline-run2-scores.tsv`](baseline-run2-scores.tsv), finding-level comparison in [`baseline-run2-findings.tsv`](baseline-run2-findings.tsv).
- **Run 2 alone:** 1 caught (#21046), 1 partial (#17145), 3 noted-not-reported (#14892, #25239, #16926). That is the same case for case as run 1, so the union of run 1 and run 2 is still 1 caught (2 with the partial).
- **Run 2's 22 findings:** 11 are not in run 1 and are not the golden. Of those, 0 are real, 7 minor and 4 wrong: 0.85 extra alarms per review, 0.31 wrong per review.

| pair, per review on the 13 new cases | bugs caught (of 13) | extra alarms per review | wrong extra alarms per review | cost per review |
| --- | --- | --- | --- | --- |
| run 1 + run 2 | 1 | 0.85 | 0.31 | $0.98 |
| run 1 + Sonnet high judge | 3 | 0.46 | 0 | $0.93 |
| run 1 + Opus high judge | 3 | 0.62 | 0 | $1.66 |

### Did the judge read the other side? (PR #22107)

On [#22107](https://github.com/pingdotgg/t3code/pull/22107) the bug is on the other side of an option. In `NodeChildProcessSpawner.ts:484-493` at the reviewed commit, an undefined `forceKillAfter` sends SIGTERM, waits `processGroupGraceMillis` (1 s, `:79`), and then awaits exit forever (`Deferred.await(exitSignal)`, `:493`), with no SIGKILL. Checked in the saved outputs:

- **Arm C inputs** (the first reviewer's notes mention `forceKillAfter`): every judge config, in v1 and v2, **cited `NodeChildProcessSpawner.ts`**, which the prompt only allows for lines opened in the session (`:473-494`, `:484`, `:550-559`). Every one judged it `safe`:
  - Haiku high: "undefined takes the old one-second path for every other caller";
  - Opus medium: "When the option is undefined, the default SIGTERM-then-wait path runs as before";
  - Opus high cited `Duration.ts:245` and `effect.ts:5525` as safe lines.

  They read the 1 s grace as if it were a force kill, or stopped at "as before". The v2 rule against "keeps the previous behaviour" did not prevent it.
- **Arm A inputs** (no note about the option): no judge cited the spawner.

So on this case **the judge ratified the gap after reading the code**, which is wachiman ADR 0009's objection in its strongest form. It is not a case of "did not look". It also shows the limit of a judge fed by notes: with no note about the option (arm A), nobody went there.

### Cost and time

| config | phase 1: cost per call | phase 1: time per call | phase 3: cost per call | phase 3: time per call | avg turns |
| --- | --- | --- | --- | --- | --- |
| opus-high | $1.05 | 182 s | $1.15 | 209 s | 28.0 |
| opus-medium | $0.66 | 116 s | $0.53 | 101 s | 18.7 |
| sonnet-high | $0.42 | 133 s | $0.42 | 130 s | 25.1 |
| sonnet-medium | $0.09 | 25 s | $0.09 | 24 s | 6.6 |
| haiku-high | $0.21 | 298 s | $0.20 | 277 s | 40.9 |

The first review on the new cases cost **$0.51 per review** measured (15 batches over 13 reviews, 156 s per review); run 2 cost $0.47.

Sonnet medium is cheap because it barely reads: 6.6 turns per call, against 19 to 41 for the others. Haiku high is slow because it takes the most turns.

**Pair against an Opus high reviewer alone**, per review on these 13 cases:

- **Opus high reviewer alone:** about **$0.80**, inferred. That is the measured Sonnet cost × 0.50/0.32, the per-batch ratio in wachiman's `src/estimate.ts` (`PER_BATCH_USD = { sonnet: 0.32, opus: 0.5, haiku: 0.28 }`). The batch figures alone give $0.58, but they underestimate these reviews, where Sonnet's estimate is $0.37 against $0.51 measured.
- **Pairs:** Sonnet high reviewer + judge costs, by judge:

  | judge | pair cost |
  | --- | --- |
  | Sonnet medium | $0.60 |
  | Haiku high | $0.72 |
  | **Sonnet high** | **$0.93** |
  | Opus medium | $1.04 |
  | Opus high | $1.66 |

  The Sonnet high pair costs about 16% more than an Opus high reviewer alone, and about the same as running the reviewer twice ($0.98).

### Running total

| item | cost |
| --- | --- |
| judge calls v1 (Sonnet high, 14) | $6.80 |
| judge calls v2, phase 1 (70) | $34.13 |
| judge calls v2, phase 3 (65) | $31.20 |
| failed calls (58, logged in `runs/*/failures.log`, raw in `runs/*/failed/`) | $1.17 |
| baseline run 1 (13) | $6.65 |
| baseline run 2 (13) | $6.15 |
| **total** | **$86.10** |

No single call exceeded $5; the largest was $2.54 (Opus high on A-#19355). The $80 report threshold was crossed during baseline run 2. The launching thread raised the limit to $95, since the owner set no cap.

## Which model for the second reviewer

**Recommendation: Sonnet 5.5 high, as a hazard judge over the first reviewer's contract notes.**

Checked, on this sample:

1. A judge beats a second plain run at the same cost. Sonnet high judge + reviewer caught 3 of 13 against 1 of 13 for two reviewer runs, for $0.93 against $0.98 per review. It also raised fewer extra alarms (0.46 against 0.85 per review), and none of them was wrong (against 4 of 11).
2. Among judges, Sonnet high ties Opus high and Haiku high on hits (2 of 13 new, #19432 on the known cases).
   - Against Opus high, it costs 37% as much and raises fewer alarms.
   - Against Haiku high, it raises about a third as many alarms (0.46 against 1.23 per review) and runs faster (130 s against 277 s), for about twice the cost.
   - Opus medium and Sonnet medium found less: 1 and 0 of 13. Sonnet medium reads too little (6.6 turns) to judge anything.
3. No config crosses the owner's false-alarm line (wrong alarms: 0 on the new cases).

Inferred, not shown:

- That Sonnet high is better than Opus high or Haiku high. The three tie at 2 hits, with one shared case (#29838) and one different case each. One run per cell cannot separate them.
- That the judge generalises. Its hits are 2 of 13 new bugs, and on the 5 known cases it caught only the one that the focus file and Opus had already caught.

What would change the answer:

- **Opus high:** if repeated runs on a larger set show Opus high catching cases Sonnet high does not, at more than about one extra bug per 20 reviews, its extra $0.73 per review would be worth weighing.
- **Haiku high:** if its minor-alarm rate can be cut (for example, by dropping low-severity `breaks`), it becomes the cheaper equal.
- **No judge at all:** if a second Sonnet high judge run shows its two hits do not repeat, the case for any judge weakens to "the reviewer is noisy".
- **A different design:** if the #22107 pattern (read it, misjudged it) dominates on more cases, a judge fed by notes is the wrong shape and the effort belongs in the reviewer.

## Scoring notes

- **Hit labels:** two Sonnet 5.5 medium workers labelled every `breaks` verdict (hit / partial / other): [`scores-phase1-preliminary.tsv`](scores-phase1-preliminary.tsv) and [`scores-phase3-preliminary.tsv`](scores-phase3-preliminary.tsv). gpt-6.1-sol (high) added the last 10 Haiku high files after Sonnet hit its weekly limit. Spot-checked here:
  - **#14892, Opus high, kept as a hit.** The trigger is an allowlist `.gitignore` (`*` then `!` lines), not the golden's blank line. The cause is the same: a false positive of the `.` probe makes capture use `add -u`, so untracked files are dropped and a restore deletes them. Its step on git's `dir.c` was not opened in the session, and the judge says so.
  - **#25239, Sonnet high and Haiku high, kept as hits.** Both reach the golden's cause, a prompt the desktop ends without telling the renderer and that stays queued, through the narrow trigger of a route where the dialog is not mounted.
- **Alarm classes:** Sonnet 5.5 medium classified phase 3 apart from the last Haiku files. gpt-6.1-sol (high) classified phase 1, the last Haiku files and run 2 (the Sonnet worker for phase 1 stopped at the weekly limit before writing). Each set had one classifier and no second opinion. The run-2 alarms and the judge alarms on the new cases were classed by different models, so the "wrong" columns are not strictly comparable.
- **Baseline scoring:** a Sonnet 5.5 medium worker scored run 1 ([`baseline-scores.tsv`](baseline-scores.tsv)); gpt-6.1-sol scored run 2 against the same rule.
- [`stats.py`](stats.py) recomputes every count and cost above from the files.

## Limits

- One run per cell. No variance estimate for any judge config. The control itself shows that a second reviewer run can differ: it did not here on catches, but it did on findings, 11 of 22 new.
- Sample sizes are 13 out-of-sample cases, and 5 valid plus 2 control in-sample cases.
- **In-sample numbers:** everything on the 5 known cases. The prompt was revised after seeing their v1 output, and #22107 prompted rule 2.
- **Out-of-sample:** phase 3 and the control.
- Hits and alarm classes are model-labelled and spot-checked, not all read by a person.
- Costs are the CLI's API-price estimates on a subscription, not bills.
- Operational events:
  - From 04:46 to 04:49 local, the API's edge returned `403 Attention Required | Cloudflare` to every call.
  - Later, Sonnet hit the weekly limit (`429`), on the workers and on one Haiku judge call.
  - Every failed cell was re-run and none is missing. The driver now backs off after a failure.
  - A bug in a shell wait loop (it matched its own command line) delayed phase 3 by about 50 minutes, at no cost.
  - Another session on the shared Mac ran its own Wachiman reviews at the same time. This experiment kept to 2 model processes of its own.
- The `TIMEOUT_MS` patch means the engine was not exactly 1.14.0 as shipped. It only affects how long git snapshot commands may run.
- The fork's main was used as "later t3code" when classing alarms.

## Files

- **Driver and inputs:** [`judge.py`](judge.py), [`judge-prompt-v1.md`](judge-prompt-v1.md), [`judge-prompt-v2.md`](judge-prompt-v2.md) (frozen; [`judge-prompt.md`](judge-prompt.md) is identical), [`baseline.sh`](baseline.sh), [`stats.py`](stats.py).
- **Judge runs:**
  - [`runs/v1/`](runs/v1/): prompt v1, Sonnet high, 14 phase-1 inputs.
  - [`runs/v2-phase1/`](runs/v2-phase1/): v2, 5 configs × 14 inputs.
  - [`runs/v2-phase3/`](runs/v2-phase3/): v2, 5 configs × 13 new cases.
  - Each run's `failures.log` and `failed/`.
- **Baseline runs:** [`runs/baseline/`](runs/baseline/) and [`runs/baseline-run2/`](runs/baseline-run2/), each with the engine's text log per case and `wall-seconds.txt`.
- **Labels:** the score and alarm TSVs listed above.
