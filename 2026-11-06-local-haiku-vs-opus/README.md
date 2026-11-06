# Haiku 5.5 high against Opus 5.5 high, run locally, on ten replayed PRs (2026-11-06)

- **Date:** 2026-11-06.
- **Run locally**, on the owner's laptop, with `agent-review local` and the owner's claude.ai login
  (`subscriptionType: max`), no `ANTHROPIC_API_KEY`. No API credit was spent. Every dollar figure
  below is Claude Code's API-equivalent estimate, not a bill. Because it costs only subscription
  usage, this run can be repeated as often as needed.
- **Engine:** Wachiman v1.8.0 (`983cd0a`), unchanged. The only difference between arms is
  `AGENT_REVIEW_MODEL`: `claude-haiku-5-5` or `claude-opus-5-5`, both at `AGENT_REVIEW_EFFORT=high`,
  production limits, run budget $3. Driver: [`run.sh`](run.sh).
- **Cases:** the ten replay PRs in [kaipu-bench-wachi](https://github.com/niway-dev/kaipu-bench-wachi),
  base `replay/pr-<n>/base`, head `replay/pr-<n>/head`. Four held-out PRs with one catalogued bug
  each and one control ([2026-11-02-heldout](../2026-11-02-heldout/README.md)), and the five
  exhibition PRs with their 14 real Medium+ bugs ([2026-11-01](../2026-11-01/README.md)).
- **Runs:** one per arm per PR, 20 reviews in total (see [What ran](#what-ran)).
- **Scoring:** by reading each finding against the answer key, by the agent that ran the
  benchmark, not blind. ✅ found with the same mechanism; ~ the same symptom or code with a
  different or weaker mechanism; ✗ not found. Findings outside the answer key are listed but **not
  audited**.

## What ran

**20 reviews:** 10 PRs × 2 models, one review each. Each review is one `agent-review local` run;
the engine splits a large diff into batches and makes one model call per batch, so a review is
1 to 6 calls.

### The code reviewed

| PR | Set | Files | Lines added | Lines removed | Batches (calls per review) |
| --- | --- | --- | --- | --- | --- |
| #184 | held-out | 7 | 238 | 24 | 1 |
| #255 | held-out | 5 | 319 | 13 | 1 |
| #269 | held-out (control) | 12 | 1,198 | 26 | 2 |
| #276 | held-out | 19 | 641 | 357 | 1 |
| #402 | held-out | 26 | 1,820 | 504 | 3 |
| #463 | exhibition | 23 | 1,413 | 44 | 2 |
| #464 | exhibition | 31 | 1,139 | 123 | 2 |
| #465 | exhibition | 14 | 1,056 | 559 | 2 |
| #466 | exhibition | 28 | 1,283 | 12 | 2 |
| #467 | exhibition | 47 | 2,676 | 2,177 | 6 |
| **Total, per model** | | **212** | **11,783** | **3,839** | **22** |

Each model reviewed the same 212 files and about 15,600 changed lines, in 22 calls.

### Timeline (local time, UTC−5, 2026-11-06)

| Step | Start | End | Wall clock |
| --- | --- | --- | --- |
| Pilot: #184, Haiku then Opus, one at a time | 00:51 | 01:00 | about 9 min |
| Main run: the other 9 PRs, all 9 in parallel; within each PR Haiku first, then Opus | 01:14 | 01:47 | **about 34 min** |

The 9 PRs ran side by side, so the main run took 34 minutes of real time. The slowest PR set the
end: #467's Haiku review alone took 27 minutes (6 batches, one after the other), then Opus 6.

**Model time is not wall clock.** "Model time" in the tables below adds up every call's duration.
Haiku's 102 minutes and Opus's 24 minutes are the time each model would need if the 22 calls ran
one after another. Per review, Haiku took 2.5 to 27 minutes and Opus 1 to 6 minutes.

### Spend: expected and actual

| | Expected before the run | Actual (API-equivalent estimate) |
| --- | --- | --- |
| Pilot #184, Haiku | — | $0.04 |
| Pilot #184, Opus | $0.30–0.50 | $0.49 |
| Main run, 9 PRs × 2 models | $10–15 | **$16.95** (Haiku $5.86, Opus $11.09) |
| **Total** | | **$17.48** |
| Paid in API credit | $0 | **$0**: every call used the claude.ai subscription |

The main run came in about $2–7 over the estimate given before it started. No review reached its
$3 cap: the most expensive was #467 with Opus, at $2.91.

## Summary

| | Haiku 5.5 high | Opus 5.5 high |
| --- | --- | --- |
| Held-out catalogued bugs found (of 4) | **2** (#255, #402) | 1 (#255) |
| Exhibition real Medium+ bugs found (of 14) | **8**, plus 1 ~ | 4, plus 2 ~ |
| Findings posted, all ten PRs | 119 (63 docs, tests, cleanup or rules) | 41 (19 docs, tests, cleanup or rules) |
| Duplicate findings noticed | at least 6 (#464 ×1, #466 ×1, #467 ×4) | 1 (#467) |
| Estimated cost, ten PRs | **$5.90** | $11.58 |
| Model time, summed over calls (not wall clock; see Timeline) | 6,106 s (102 min) | 1,415 s (24 min) |
| Turns | 689 | 188 |

What this shows, with one run per arm:

1. **Haiku found more of the known bugs**, including #402's lost first state, which Opus missed
   here and in all three v1.4.0 runs.
2. **Haiku costs about half of Opus, not a twelfth.** On a small PR it is a twelfth (#184, #255).
   On large PRs it reads far more (8.2M cache-read tokens on #467 against 1.0M), so the saving
   shrinks to about 30–60 %.
3. **Haiku is about four times slower** and posts about three times as many findings, with
   duplicates. The volume is the cost a verifier step must remove.
4. **Opus scored below its own history.** v1.4.0 Opus found 7, 7 and 8 of the 14 exhibition bugs
   per run; this v1.8.0 run found 4. One run cannot say whether that is noise or a regression.
5. **Nobody found** #184's pointer-capture bug or #276's check-then-act race.

Limits: one run per arm (a model does not review the same PR the same way twice), non-blind
scoring, and the extra Haiku findings are unaudited.

## Reference: the other reviewers, and the target

The target for the next versions is to find everything Pullfrog and CodeRabbit found on these
PRs, then more. Bugs that **no** reviewer found are not a tuning target: shaping prompts or
detectors around one of them would fit Wachiman to this codebase, not make it a better reviewer.

Pullfrog and CodeRabbit columns come from [results.md](../results.md) (exhibition, 2 runs each) and
the [held-out report](../2026-11-02-heldout/README.md) (CodeRabbit, 1 run; Pullfrog did not run).
"Wachiman" here is either arm of this run.

| PR | Bug | Pullfrog | CodeRabbit | Wachiman v1.8.0 (Haiku / Opus) | Status |
| --- | --- | --- | --- | --- | --- |
| #463 | A queued camera-on reopens the camera after a newer off | ~ | 1/2 | ✗ / ✗ | **gap** |
| #463 | The take's first relay feed is ignored | 0/2 | 1/2 | ✗ / ✗ | **gap** |
| #463 | Random gap ids break Share's reuse | 1/2 | 0/2 | ✗ / ✗ | **gap** |
| #276 | Check-then-act between the ticket check and `release()` | did not run | match | ✗ / ✗ | **gap** (v1.4.0 Opus found it 1/3) |
| #463 | A superseded camera-on closes the gap too early | 2/2 | 0/2 | ✅ / ✗ | matched |
| #464 | Ready card skips `markCopySeen` | 0/2 | 2/2 | ✅ / ✅ | matched |
| #465 | A failed probe leaves the cards at "…" | 1/2 | 0/2 | ✅ / ✗ | matched |
| #466 | `show()` / a failed load loses the card | 0/2 | 1/2 | ✅ / ✅ | matched |
| #467 | A Library drop navigates the window to the file | 2/2 | 0/2 | ✅ / ✅ | matched |
| #467 | Editor exports labelled as destination copies | 1/2 | 0/2 | ✅ / ✗ | matched |
| #255 | The policy cache turns the Dock restore into a no-op | did not run | match | ✅ / ✅ | matched |
| #402 | The spare overlay's first state is lost before the listener | did not run | match | ✅ / ✗ | matched |
| #465 | The Drag handle skips `markCopySeen` | 0/2 | 0/2 | ✗ / ✅ | **beyond** |
| #466 | Back re-floats the card | 0/2 | 0/2 | ✅ / ~ | **beyond** |
| #467 | A finished Email copy is listed as "Slack · Discord" | ~ | 0/2 | ✅ / ✗ | **beyond** |
| #463 | The face is recorded in no file | 0/2 | 0/2 | ~ / ~ | nobody, fully |
| #467 | Export never re-lists the Library | 0/2 | 0/2 | ✗ / ✗ | nobody: not a target |
| #184 | Pointer capture on a re-rendered `<tspan>` breaks double-click | did not run | ~ (a different defect) | ✗ / ✗ | nobody: not a target |

Four gaps remain, three of them in #463's camera toggle and its queue, and one check-then-act race.
Those four are the next version's targets.

---

## Held-out PRs

### kaipu-record [#184](https://github.com/niway-dev/kaipu-record/pull/184) · replay head [`2c33d5b`](https://github.com/niway-dev/kaipu-bench-wachi/commit/2c33d5b8)

7 files, +238/−24, 1 batch. The held-out bug is the pointer capture; the other three rows are
the catalogue's other bugs for this PR.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| Pointer capture on a re-rendered `<tspan>` breaks double-click (held-out, difficulty 5) | ✗ | ✗ |
| Hit box ignores multi-line labels | ✅ | ✅ |
| Reopened label shows one line | ✅ | ✅ |
| Label drawn twice under the editor | ~ named inside another finding | ✅ |
| *Not in the key:* re-edit uses the toolbar's size and colour | ✅ | ✅ |
| *Not in the key:* clearing a re-edited label reverts it | posted | — |
| *Not in the key:* double-click inside the editor retargets the edit | posted | — |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 1 | 18 | 151 s | 32.9k | 384k | 97k | 6 | $0.04 |
| Opus | 1 | 9 | 51 s | 5.3k | 103k | 45k | 5 | $0.49 |

### kaipu-record [#255](https://github.com/niway-dev/kaipu-record/pull/255) · replay head [`78e20a2`](https://github.com/niway-dev/kaipu-bench-wachi/commit/78e20a25)

5 files, +319/−13, 1 batch.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| The activation-policy cache turns the Dock restore into a no-op (difficulty 5) | ✅ `Fix · question`: the cache makes the re-assert a no-op, so the app can drop out of Cmd+Tab after a recording | ✅ `Blocker · question`: names Electron changing the policy natively, so the cache goes stale |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 1 | 16 | 154 s | 34.7k | 329k | 85k | 4 | $0.04 |
| Opus | 1 | 13 | 89 s | 8.0k | 342k | 48k | 2 | $0.61 |

### kaipu-record [#276](https://github.com/niway-dev/kaipu-record/pull/276) · replay head [`f91b56d`](https://github.com/niway-dev/kaipu-bench-wachi/commit/f91b56de)

19 files, +641/−357, 1 batch.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| Check-then-act between the ticket check and `release()` (difficulty 4) | ✗ | ✗ |
| *Not in the key:* skipped in-window rows hold the batch | posted (`bug`) | posted (`perf`) |
| *Not in the key:* deferred cancel and delete hold quota until an unscheduled job runs | posted | — |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 1 | 42 | 394 s | 86.6k | 1,745k | 198k | 12 (10 docs/tests/cleanup) | $0.39 |
| Opus | 1 | 10 | 99 s | 8.7k | 251k | 51k | 4 | $0.63 |

### kaipu-record [#402](https://github.com/niway-dev/kaipu-record/pull/402) · replay head [`01dfe73`](https://github.com/niway-dev/kaipu-bench-wachi/commit/01dfe73f)

26 files, +1,820/−504, 3 batches.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| A spare overlay's first state message arrives before the listener; the blank window swallows clicks (difficulty 5; v1.4.0 Opus 0/3, CodeRabbit found it) | ✅ `Fix · question`, confidence low: names the `ready-to-show` send, the effect subscription and the blank window that takes clicks | ✗ |
| *Not in the key:* a crashed shade renderer is never replaced | posted | posted |
| *Not in the key:* the shade's state IPC may land before its listener (same shape as the key bug) | posted | — |
| *Not in the key:* a failed countdown acquisition is reused | — | posted |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 3 | 71 | 916 s | 193.2k | 5,269k | 593k | 14 (10 docs/tests) | $1.18 |
| Opus | 3 | 18 | 182 s | 17.2k | 455k | 163k | 4 | $1.74 |

### kaipu-record [#269](https://github.com/niway-dev/kaipu-record/pull/269) · replay head [`3159fb1`](https://github.com/niway-dev/kaipu-bench-wachi/commit/3159fb1c) · control

12 files, +1,198/−26, 2 batches. No catalogued bug (the catalogue row was moved to #286), so this
PR measures noise only.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| none | — | — |
| *Not in the key:* small-file preset under-reserves packets below the 30 fps floor | posted | posted |
| *Not in the key:* fps cap drops half the frames of a source at the cap | posted | — |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 2 | 42 | 522 s | 113.6k | 1,801k | 254k | 11 (7 docs/tests) | $0.43 |
| Opus | 2 | 13 | 139 s | 12.5k | 257k | 94k | 2 | $1.05 |

---

## Exhibition PRs

### kaipu-record [#463](https://github.com/niway-dev/kaipu-record/pull/463) · replay head [`3ec7a13`](https://github.com/niway-dev/kaipu-bench-wachi/commit/3ec7a138)

23 files, +1,413/−44, 2 batches.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| The face is recorded in no file (High, difficulty 5) | ~ a failed reopen leaves the protected window on screen | ~ a failed reopen leaves the face out of both files |
| A queued camera-on reopens the camera after a newer off (High) | ✗ | ✗ |
| The take's first relay feed is ignored (High) | ✗ | ✗ |
| Random gap ids break Share's reuse | ✗ | ✗ |
| A superseded camera-on closes the gap too early | ✅ | ✗ |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 2 | 46 | 613 s | 131.8k | 2,844k | 389k | 13 (7 docs/tests) | $0.70 |
| Opus | 2 | 12 | 99 s | 9.6k | 184k | 92k | 3 | $0.97 |

### kaipu-record [#464](https://github.com/niway-dev/kaipu-record/pull/464) · replay head [`e45c845`](https://github.com/niway-dev/kaipu-bench-wachi/commit/e45c8451)

31 files, +1,139/−123, 2 batches.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| Ready card's Show in Finder and drag skip `markCopySeen` | ✅ (posted twice) | ✅ |
| *Not in the key:* a leading copy card drops the tag, Send to, edit and delete actions | posted | — |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 2 | 86 | 654 s | 137.8k | 2,732k | 332k | 8 (4 docs/tests/rules) | $0.54 |
| Opus | 2 | 22 | 120 s | 10.1k | 427k | 84k | 2 | $0.96 |

### kaipu-record [#465](https://github.com/niway-dev/kaipu-record/pull/465) · replay head [`dac8318`](https://github.com/niway-dev/kaipu-bench-wachi/commit/dac8318b)

14 files, +1,056/−559, 2 batches.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| The new Drag handle skips `markCopySeen` | ✗ | ✅ |
| A failed file probe leaves the cards at "…" | ✅ | ✗ |
| *Not in the key:* Balanced, Light and YouTube copies lose their destination name and logo | posted (`Fix`) | — |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 2 | 75 | 637 s | 137.4k | 2,963k | 381k | 16 (8 docs/tests) | $0.73 |
| Opus | 2 | 13 | 122 s | 11.4k | 275k | 97k | 5 | $1.06 |

### kaipu-record [#466](https://github.com/niway-dev/kaipu-record/pull/466) · replay head [`b2705a9`](https://github.com/niway-dev/kaipu-bench-wachi/commit/b2705a9c)

28 files, +1,283/−12, 2 batches.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| `show()` returns true before the card renders; a failed load loses the card | ✅ | ✅ |
| Back re-floats the card (difficulty 5) | ✅ `Fix`, confidence high (also posted as a question) | ~ a remount under the same history entry re-floats it |
| *Not in the key:* `recording-ready:show` accepts any sender | — | posted (`security`) |
| *Not in the key:* the card stays up after its recording is deleted | — | posted |
| *Not in the key:* a file dropped on the card navigates its window | posted | — |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 2 | 57 | 466 s | 93.3k | 1,994k | 307k | 9 (3 docs/tests) | $0.52 |
| Opus | 2 | 18 | 141 s | 12.5k | 349k | 105k | 4 | $1.16 |

### kaipu-record [#467](https://github.com/niway-dev/kaipu-record/pull/467) · replay head [`b12d760`](https://github.com/niway-dev/kaipu-bench-wachi/commit/b12d760b)

47 files, +2,676/−2,177, 6 batches.

| Known bug | Haiku | Opus |
| --- | --- | --- |
| Export never re-lists the Library (difficulty 5) | ✗ | ✗ |
| A finished Email copy is listed as "Slack · Discord" | ✅ (posted twice) | ✗ |
| A video dropped on the Library navigates the window to the file | ✅ (posted four times) | ✅ (posted twice) |
| Editor exports labelled as destination copies | ✅ | ✗ |
| *Not in the key:* Library picker clipped on the no-video screen | posted | posted |
| *Not in the key:* Enter still exports while focus is inside a dialog | — | posted |

| Arm | Calls | Turns | Model time | Output | Cache read | Cache write | Findings | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Haiku | 6 | 236 | 1,599 s | 321.8k | 8,232k | 867k | 26 (10 docs/tests) | $1.33 |
| Opus | 6 | 60 | 373 s | 31.1k | 1,017k | 261k | 10 (6 docs/tests) | $2.91 |

---

## Raw data

[`raw/`](raw/): every report as Markdown (`pr<n>-<arm>.md`) and every engine log (`pr<n>-<arm>.log`,
with one `wachiman-cost` JSON line per call). #184's logs were not kept; its figures come from
the terminal output of the same run.
