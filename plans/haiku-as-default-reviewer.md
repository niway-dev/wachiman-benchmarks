# Plan: can Haiku 5.5 be the default reviewer? (registered 2026-11-02)

Status: **planned, not run.** Working document; the report that runs it replaces it.

## One-minute summary

The re-review study (`2026-11-02-re-review-models`, wachiman-benchmarks #8) found Haiku 5.5 at
effort high cheaper than Sonnet and Opus and at least as good on six re-reviews. That evidence is
thin: two runs per arm, a five-finding answer key, every finding Low, and the only real Medium bug
from a field re-review not rebuilt. This plan measures Haiku against Sonnet (the owner's intended
default for affordable reviews) and Opus (reference) on **both** jobs: the first ("formal") review
of a PR and the incremental re-review after a push.

Two questions, answered separately:

1. **Re-reviews.** Does Haiku high keep the Medium+ findings and the thread replies Opus gets?
2. **First reviews.** Can Haiku high replace Sonnet high as the default first reviewer?

No conclusion is drawn before an independent auditor (GPT-6.1 Sol, blind to the arm) has
validated every posted finding.

## Why more runs

A model does not return the same review twice. In the re-review study Opus found 4 audited
findings in one run and 3 in the other on identical input. With two runs and five findings, a
one-finding gap between arms is noise. Five runs per arm per case give a hit rate per bug
(found in 0–5 of 5 runs), which separates "this model cannot see this bug" from "this model saw
it once by luck".

## Arms

| Arm | Model | Effort | Runs per case |
| --- | --- | --- | --- |
| H | `claude-haiku-5-5` | high | 5 |
| S | `claude-sonnet-5-5` | high | 5 |
| O | `claude-opus-5-5` | high | 3 (reference only) |

| H→V | Haiku high proposes; free code filters, then one batched verifier call | high | 5 |
| H-scope | Haiku high; a finding must cite the changed line of this push that causes it | high | 5 |

**Why H→V and H-scope.** The blind audit of the re-review study (GPT-6.1 Sol, 2026-11-03,
`evidence/gpt-sol-audit-2026-11-03/`) found Haiku high posted about twice Opus's valid findings
(11 against 6 per run) and also far more invalid ones (5 of 17 and 2 of 13; Opus 0). Most invalid
ones were true but pre-existing and outside the push. So Haiku looks like a high-recall,
low-precision proposer. H→V tests "Haiku proposes, code and a stronger model keep only what
holds". Order: free code filters first (cited line exists, finding traces to this push, not a
duplicate of an open thread), then **one** verifier call for all remaining alarms, with the engine
packing each alarm and the code lines it cites, so the verifier neither searches nor reads whole
files. One call per alarm would pay the fixed prompt floor (about $0.15 of Opus's $0.50
re-review) for every alarm and cost more than Opus alone. Estimate to test, not measured:
$0.15–0.30 for the batched Opus call plus $0.07 for Haiku, against $0.50 for Opus alone.
Verifier model to pick before the run: Sonnet high or Opus high. H-scope tests
whether an output rule removes most of the noise by itself: each finding names the line of this
push (the author's rows, `ownChangeSince`) that causes it, or is dropped. The rule is "caused by a
changed line", not "located on a changed line": a valid finding can sit on an old line the push
made wrong (#478, `registry.ts:821`, stale after the new branch at `:848`). Cutting the input
context instead is ruled out: the #483 ordering bug needs a file outside the diff, and the hunks-only
lever lost findings in the re-review cost study. Untested: whether the extra suspicions come from the model or from effort high;
add a Haiku medium arm if budget allows.

Engine: the current release (v1.5.0 with data-path questions), production limits, writes refused,
the harness from `2026-11-02-re-review-models/harness/`. Arm order shuffled per case with a fixed
seed, as before.

## Cases

- **First reviews:** the field run's PRs with the 14 audited real Medium+ bugs
  (`2026-11-02-field/`) and the 10 missed bugs of the data-path A/B
  (`2026-11-03-data-path-questions-ab/`).
- **Re-reviews:** the six rebuilt re-reviews of the re-review study, plus a rebuild of #478
  `c573b8e`, the one field re-review with a real Medium bug.
- **Held-out:** at least three kaipu-record PRs opened after 2026-11-02 that no design work has
  looked at. The cases above shaped the questions and prompts, so a result on them alone is
  in-sample.

## What is measured

Per arm, separately for first reviews and re-reviews:

- recall on audited bugs, split Medium+ and Low, as a hit rate per bug over the runs;
- invalid findings per 20 posted, and Low/doc-only findings per review (noise);
- thread replies: needed replies missing, and replies that wrongly say "fixed" or "still open";
- cost per review, turns, wall time;
- run-to-run spread of each of the above.

Every posted finding, from every arm, goes to the blind auditor (GPT-6.1 Sol): VALID, INVALID or
UNCERTAIN with a cited line. The auditor's verdicts, not the harness's, are the scored ones;
disagreements with the harness audit are listed in the report.

## Side output: pattern mining

Every finding the auditor marks VALID and that only Haiku found becomes a candidate for the pattern
catalogue (data-path questions, detectors, "bug → lint rule";
see wachiman `docs/research/2026-11-03-code-derived-review-signals.md`). For each one, record:
the bug class, the code shape that signals it, and whether a plain-code detector could select a
question for it. Example from the audit: #482 `ad0fa5c`, active relocation broadcasts settings
from the old folder's cache (`index.ts:406`), a stale-read shape close to `stale-write-back`.

## Decision rules (proposed; the owner confirms before the run)

- **Haiku for re-reviews** if its Medium+ hit rate is not below Opus's by more than one bug-run
  in five, invalid findings are at most 1 in 20, and no needed thread reply is missing more often
  than with Opus.
- **Haiku replaces Sonnet for first reviews** if, on the same rules against Sonnet, it loses no
  Medium+ bug and costs at most half of Sonnet's.
- Otherwise the arm that wins stays, and the report says which bug class Haiku misses.

## Budget

Run on the owner's Claude Code subscription, from the local terminal (wrap `claude` to restore
`USER`, as the earlier harnesses do). Stop guard at **$25** of reported spend; Haiku and Sonnet
arms run first, Opus last, so a stop costs only the reference arm. The auditor runs on Codex.

## Open before running

- The owner confirms the decision rules.
- Pick the three held-out PRs.
- Confirm the `c573b8e` rebuild reproduces the field review's input (same diff, same threads).
