# Re-review cost: where the turns go, and what makes them cheaper (2026-11-02)

## One-minute summary

- **What was measured.** Six Wachiman re-reviews from the 2026-11-02 field run (kaipu-record #478
  ×2, #479, #482, #483, #484) were rebuilt as the **v1.5.0** engine runs them and run through its
  own `review()` with a full tool trace. Opus 5.5, effort high, production limits. Baseline twice,
  each lever once. Total reported spend: **$13.40** (cap $15).
- **"Turns" are tool calls, not model requests.** Claude Code's `num_turns` is the number of tool
  calls plus one. The model batches calls, so 67 turns over the six baseline calls were 33 requests.
  Cost per turn ($0.04) is an average, not a unit price.
- **Where the money goes (baseline, $2.99 for six re-reviews).** Measured as what entered the
  context: **the fixed prompt 29 %**, **the model's output 26 %**, reading the changed files 21 %,
  `threads.json` 10 %, search 7 %, `pr.json` 6 %, unchanged files 2 %. By billing line: cache
  writes 56 %, output 26 %, cache reads 18 %.
- **Where the turns go (tool calls, baseline run 1 / run 2).** Reading changed files 21 / 25
  (mostly 200–400-line slices), search 17 / 15, unchanged files 6 / 7, `threads.json` 6 / 6,
  `pr.json` 5 / 5, the final answer 6 / 6, `evidence.json` 0.
- **The diff size barely matters.** A 5-line push on #483 cost $0.51–0.52; a 226-line push on #478
  cost $0.62–0.66. v1.5.0's own-rows filter shrank three of these deltas, and the six still cost
  what v1.4.0 charged in the field ($2.98 average of two runs, against $2.79).

| Arm (one run each, six cases) | Cost | vs baseline mean $2.98 | Turns | Requests | Audited findings found (of 5) | Thread replies | Lost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline v1.5.0, run 1 | $2.99 | — | 67 | 33 | 4 | 32 | — |
| Baseline v1.5.0, run 2 | $2.97 | — | 70 | 39 | 3 | 27 | — |
| **T**: threads only when the push can change them | $2.87 | −4 % (noise) | 69 | 38 | 4 | 18 | nothing measured |
| **F**: no flow questions, contracts or evidence | $2.46 | −17 % | 63 | 38 | 3 | 27 | #483 ordering bug (F17) |
| **T+F+R**: plus "read the hunks, not the whole file" | $2.11 | −29 % | 55 | 33 | 2 | 24 | F17; F18 and F21 not found |

- **Noise is large.** One case with an identical prompt cost $0.21 in one run and $0.28 in another.
  Each baseline run missed one or two of the five audited findings, and not the same ones.
  Only effects of about 15 % or more show up with one run per arm.
- **Recommendation.** Ship **T** (done in niway-dev/wachiman `feat/cheaper-re-reviews`, ADR 0019
  draft). It is the only lever that lost nothing. It cuts `threads.json` by 64 % and removes
  replies that only repeated an earlier verdict. Its saving is small. Do **not** ship F or T+F+R:
  both were cheaper, but both dropped the #483 ordering bug, which both baselines found (it is
  real, checked in the code below). A max-turns cap was not run: it cannot cut the context cost
  and loses the whole answer when hit (below).
- **What would make re-reviews substantially cheaper** is the fixed part: the prompt (the
  repository's instructions alone are 15,200 characters on kaipu-record) and the output. Neither is
  specific to re-reviews, and neither was measured here.

## Method

### The rebuild

`harness/rereview.ts` imports the engine (`src/engine.ts`) from a checkout and calls its `review()`
with a `gh` answered locally, so the delta (`compare`, `rebaseDelta`, `ownChangeSince`), batching,
open threads, call-site evidence, data-path questions and prompt are the engine's own:

- `pulls/<n>/files`: `git diff <merge-base> <head>` in the kaipu-record clone, with blob SHAs, the
  merge base taken against the base branch as it was when the job started. #479 and #483 were
  stacked PRs at that moment (base = #478's and #482's branch), from the PR timeline's
  `AutomaticBaseChangeSucceededEvent`.
- `compare/A...B`: `git diff merge-base(A,B) B`, status `ahead` when A is an ancestor of B.
- `pulls/<n>/reviews` and `pulls/<n>/comments`: the field's raw JSON
  ([`2026-11-02-field/raw/`](../2026-11-02-field/raw/)), cut at the job's start time, through the
  engine's own `--jq` program.
- Review threads: built from those comments. A thread counts as open unless it is resolved today
  and the real re-review did not reply to it (only 16 of 74 threads are resolved today).
- Writes are refused (`AGENT_REVIEW_DRY_RUN=1`); the provider call is real.

The provider is the engine's Claude Code adapter with production settings (budget $0.75 per batch,
40 turns, 900 s), through a wrapper that restores `USER` for the keychain login (as in the
[2026-11-03 A/B](../2026-11-03-data-path-questions-ab/harness/claude-with-user.sh)), switches
`--output-format json` to `stream-json --verbose`, and keeps the stream as the trace. Production
defaults are not changed.

**The rebuild matches the field.** File counts per re-review match the Actions logs (10, 7, 8, 2,
1, 2 files), and where v1.5.0 changes nothing the call-site evidence matches to the byte (#478
`64db30b`: 24 symbols, 24 call sites, 15,061 bytes; `392778f`: 8 / 24 / 12,948; `c573b8e`:
11 / 26 / 15,055 and 34 / 27 / 16,115). On #479, #482 and #483 v1.5.0 sends fewer rows than v1.4.0
did, because of the own-rows filter (#89).

| Case | Head | Since | Delta sent (v1.5.0) | Open threads | Field v1.4.0 | Baseline v1.5.0 (run 1 / 2) |
| --- | --- | --- | --- | --- | --- | --- |
| 478-64db30b | `64db30b` | `c573b8e` | 10 files, +226 | 13 | 11 turns, $0.53 | 9 / 10 turns, $0.62 / $0.66 |
| 478-392778f | `392778f` | `64db30b` | 7 files, +46 | 14 | 10 turns, $0.36 | 12 / 11 turns, $0.56 / $0.49 |
| 479-413ee15 | `413ee15` | `02dbb2e` | 8 files, +18 | 12 | 15 turns, $0.59 | 17 / 18 turns, $0.60 / $0.65 |
| 482-ad0fa5c | `ad0fa5c` | `543053c` | 2 files, +5 | 10 | 17 turns, $0.60 | 9 / 11 turns, $0.48 / $0.36 |
| 483-0253fd7 | `0253fd7` | `4ed1580` | 1 file, +5 | 13 | 13 turns, $0.54 | 14 / 12 turns, $0.51 / $0.52 |
| 484-59f6d48 | `59f6d48` | `de9134b` | 2 files, +9 | 1 | 8 turns, $0.16 | 6 / 8 turns, $0.21 / $0.28 |

`478-c573b8e`, the re-review that found the one real Medium bug of the field run, was rebuilt and
checked with dry runs only. It is two batches (about $1.24 a run), and its delta is a
1,500-line feature push.

### The classification

`harness/classify.ts` reads each trace. A request is one assistant message: Claude Code streams a
message's blocks as several events with one `message.id`. Each tool call gets a class: whole-file
read of a changed file, slice of a changed file, read of an unchanged file, search (Grep or Glob),
`threads.json`, `pr.json`, `evidence.json`, or the final answer (`StructuredOutput`).

Cost is attributed two ways:

1. **By turn:** each request's share of the reported cost, split among its tool calls.
2. **By what entered the context** (used in the summary): request k+1's cache write holds what
   request k's tools returned; it is split among those results by size. Each result is written
   once and then read by every later request. The prompt is written once and read by every
   request. Output is priced on its own. The prices were fitted to the six reported totals: cache
   write 6.25, cache read 0.5 and output 25 USD per million tokens. The sum matches the reported
   cost to within 1 %.

An example: #483 at `0253fd7`, a push that added 5 lines to one file, baseline run 1 ($0.51, 14
turns, 6 requests):

```
request 1  $0.100  threads.json (20,587 ch) | pr.json (12,670 ch) | index.ts lines 600-820 (9,746 ch)
request 2  $0.172  sync-state.ts (unchanged) | grep "syncStates|relocateWorkspace|WorkspaceRelocateResult"
request 3  $0.042  relocate.ts (unchanged) | index.ts lines 100-400 | workspaces.ts lines 175-200
request 4  $0.082  grep relocateActive | grep "activeEvictionProbe|activeScratch("
request 5  $0.073  grep detectSync | grep afterCommit
request 6  $0.040  final answer: 1 finding, 1 contract, 0 of 13 thread replies
```

Request 2's cache write (17,731 tokens) is 39 % of the call's writes. It is mostly the 33,000
characters of `threads.json` and `pr.json`, which every later request reads again.

## Phase 1: where the turns and the money go

Tool calls by class, summed over the six cases (turns = tool calls + 1 per call):

| Class | Baseline 1 | Baseline 2 | T | F | T+F+R |
| --- | --- | --- | --- | --- | --- |
| Changed file, whole | 7 | 4 | 5 | 3 | 1 |
| Changed file, slice | 14 | 21 | 18 | 16 | 14 |
| Unchanged file | 6 | 7 | 7 | 4 | 6 |
| Search (Grep, Glob) | 17 | 15 | 16 | 21 | 17 |
| `threads.json` | 6 | 6 | 5 | 6 | 5 |
| `pr.json` | 5 | 5 | 6 | 1 | 0 |
| `evidence.json` | 0 | 0 | 0 | 0 | 0 |
| Final answer (findings, thread replies, contracts) | 6 | 6 | 6 | 6 | 6 |
| **Requests (model calls)** | **33** | **39** | **38** | **38** | **33** |

Cost by what entered the context (USD, six cases):

| Part | Baseline 1 | Baseline 2 | T | F | T+F+R |
| --- | --- | --- | --- | --- | --- |
| Prompt (written once, re-read by every request) | 0.880 | 0.907 | 0.893 | 0.807 | 0.755 |
| Output (thinking, tool calls, final answer) | 0.766 | 0.833 | 0.822 | 0.621 | 0.592 |
| Changed files, whole | 0.303 | 0.092 | 0.181 | 0.160 | 0.006 |
| Changed files, slices | 0.332 | 0.519 | 0.416 | 0.324 | 0.343 |
| Unchanged files | 0.052 | 0.085 | 0.094 | 0.028 | 0.056 |
| Search | 0.198 | 0.182 | 0.238 | 0.239 | 0.285 |
| `threads.json` | 0.291 | 0.309 | 0.107 | 0.311 | 0.114 |
| `pr.json` | 0.176 | 0.164 | 0.194 | 0.041 | 0.000 |
| **Reported total** | **2.991** | **2.972** | **2.871** | **2.461** | **2.106** |

What the trace shows:

- **Every call pays a floor before it reads anything.** The prompt is 25,000–63,000 characters.
  On #483's 5-line push it is 26,700, of which the diff is 900, the repository's instructions
  15,200, the label rules 4,000 and the flow questions 2,200. Writing it and re-reading it in
  every request is 29 % of the cost.
- **Output is about a quarter**: 2,600–8,300 tokens per baseline call. That is mostly thinking;
  the final JSON is 3,000–9,000 characters.
- **`threads.json` holds every open thread of the PR**, not the push's.
  `assignThreads` gives the first batch every thread whose file is in no batch. A one-batch
  re-review therefore gets them all: 13 threads and 20,600 characters on #483, for a 5-line push.
  On #478 at `392778f` both baselines answered all 14. Seven of those threads were on files the
  push did not touch and were already "Looks addressed". In each run, six of the seven replies
  said only "Not in this round's files. Accepting the fix in 886d67f0 as described" (or "Already
  fixed in an earlier round"). The seventh repeated the same verdict, citing a line in a file the
  push did change. In the field, one thread on #478 got "Looks addressed" four times on a file no
  push changed.
- **`pr.json` is read in every re-review** (10,000–12,700 characters: kaipu-record's PR bodies are
  long). The flow questions' first paragraph sends the model to it ("verify each statement against
  the code"). With the flow questions off, it was read once in six calls.
- **Exploration is modest.** Search and unchanged files are 9 % of the cost. The model reads
  changed files in 200–420-line slices, rarely whole.

## Phase 2: the levers

The levers were prototyped as local-only switches in a scratch engine
([`harness/levers-prototype.patch`](harness/levers-prototype.patch), never pushed): `WACHI_X_THREADS`,
`WACHI_X_FLOW` and `WACHI_X_READ`. Each was run on the same six rebuilt re-reviews.

**Audited findings.** The field audit ([`2026-11-02-field/prs/`](../2026-11-02-field/prs/))
lists five valid findings that Wachiman posted at these heads. All five are Low:

| Id | Case | Finding (field audit) | Base 1 | Base 2 | T | F | T+F+R |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F18 | 478-64db30b | Picking the current folder still shows "now points to the new folder" (Valid, Low) | ✓ | — | — | — | — |
| F20 | 478-392778f | No renderer test for the unchanged-relocate toast (Valid, Low) | ✓ | — | ✓ | ✓ | ✓ |
| F21 | 478-392778f | Keeping `pendingInit` after an offline edit lets adoption overwrite it (Valid, Low) | — | ✓ | ✓ | ✓ | — |
| F17 | 483-0253fd7 | Active relocate re-lists the Library before the new folder's sync provider is detected (Partly valid, Low) | ✓ | ✓ | ✓ | — | — |
| F2 | 484-59f6d48 | Double-click on a name still toggles the row once (Valid, Low) | ✓ | ✓ | ✓ | ✓ | ✓ |
| | | **Found** | **4** | **3** | **4** | **3** | **2** |

F17 was re-checked in the code for this study. At `0253fd7`, `relocateFolder` calls
`relocateWorkspace` (`apps/kaipu-record/src/main/workspaces/index.ts:751`). For the active
workspace that runs `relocateActive`, whose `afterCommit` re-lists the Library
(`switch-transaction.ts:136`). Only then does `index.ts:755` call `syncStates.refresh(current)`.
The order is as the finding says. Both baselines and T found it; F and T+F+R, the two arms without
the flow questions, did not. Their question 2 ("which existing path does the same thing, and what
does it do before and after") is the one that leads to it.

Findings no audit covers: #479 got the same two Consider findings (missing test, docs) in both
baselines, and one in each lever arm. #478 `64db30b` got an unaudited "deferred colour upgrade
writes a stale snapshot" finding in baseline 2 and T+F+R. Neither is counted above.

### T: a re-review sends only the threads its push can change

**Change.** On a re-review, leave out a thread Wachiman last judged addressed when its file did not
change in the push. Threads on the push's files, threads never answered, and threads left
"Still open" still go.

| | Baseline (mean of 2) | T |
| --- | --- | --- |
| Threads sent, six cases | 63 | 24 |
| `threads.json` characters | 87,600 | 31,800 |
| `threads.json` cost (context view) | $0.30 | $0.11 |
| Total cost | $2.98 | $2.87 (−4 %, inside the noise) |
| Thread replies | 32 / 27 | 18 |
| Audited findings | 4 / 3 | 4 |

**What it lost: nothing measured.** Baseline 1 wrote 10 replies on the threads T leaves out
(#478 `64db30b` ×3, `392778f` ×7). Nine restated an earlier "addressed" without reading
anything: "workspace-name.ts is outside this round's diff. I'm going by the fix described in
886d67f0." The tenth repeated the same "addressed", citing `workspaces-context.tsx:177-183`, a file
the push changed. Baseline 2 shows the same pattern. T
dropped F18 in its one run, but its prompt for that case differs from the baseline's only by three
of those threads, and baseline 2 missed F18 too.

**Shipped form.** One condition is added: a thread where a person with access replied after
Wachiman's last reply also goes. ADR 0012 relies on it: the thread-only run leaves an owner's reply
to the push's review when the head is unreviewed. A dry run of the shipped engine on all seven
rebuilt re-reviews (including `c573b8e`) sends the same threads as the measured prototype
(`raw/runs/*/dry-shipped/engine-log.txt`).

### F: no flow questions, contracts or call-site evidence on a re-review

**Change.** On a re-review, drop `FLOW_QUESTIONS`, ask for an empty `contracts`, and leave out the
evidence slice.

| | Baseline (mean of 2) | F |
| --- | --- | --- |
| Total cost | $2.98 | $2.46 (−17 %; cheaper than both baselines in 5 of 6 cases) |
| Output cost | $0.80 | $0.62 |
| `pr.json` reads | 5 | 1 |
| Audited findings | 4 / 3 | 3 |

**What it lost.** F17 on #483: both baselines and T found it, F did not. This is the class of bug
the flow questions were added for in v1.4.0.

### T+F+R: plus "read the hunks and what they reach"

**Change.** T and F, and on a re-review replace "before you report a finding, read that file in
full" with "read the new hunks and the code they reach; read a whole file only when a finding
depends on code you have not read". R was not run alone, to stay within the spend cap. This arm
measures the three mechanisms together, and the table cannot separate them.

| | Baseline (mean of 2) | T+F+R |
| --- | --- | --- |
| Total cost | $2.98 | $2.11 (−29 %; cheaper than both baselines in 6 of 6 cases) |
| Whole-file reads of changed files | 7 / 4 | 1 |
| Audited findings | 4 / 3 | 2 |

**What it lost.** F17. F18 and F21 were not found either; each baseline also missed one of them,
so those two may be noise. T+F+R is the only arm below both baselines.

### Levers not run

1. **`--max-turns` proportional to the delta.** Turns are tool calls, and the cost is the context
   each request re-reads, so a cap removes the last requests, which are the cheapest. A call that
   hits the cap ends as `error_max_turns` with no structured output. The engine then reports "hit
   the turn limit" and retries the batch's files (`batchGaps`), which pays for the same prompt
   again. Not worth a run.
2. **Previous review's summary and contracts in the prompt.** This adds input to a prompt that is
   already 29 % of the cost. Its other half, "read only the new hunks", is R, which is in T+F+R.
3. **No full-file read on a re-review**: measured only inside T+F+R (above).

## What this changes in Wachiman

- **Shipped:** T, as niway-dev/wachiman `feat/cheaper-re-reviews` (ADR 0019 draft). The default
  is on. There is no setting: a left-out thread is one the model could only repeat its answer
  on.
- **Not shipped:** F and T+F+R. A lighter re-review prompt saves 17–29 %, but it lost the one
  finding that the flow questions exist for.
- **Next, if re-review cost still matters:**
  1. The fixed prompt. On kaipu-record, the repository's instructions (15,200 characters) are
     re-sent and re-read in every request of every batch.
  2. Lower effort on re-reviews. Output is a quarter of the cost and mostly thinking. The
     quality risk is untested.
  3. A per-thread reply cap in reviews (ADR 0008's two replies), for threads whose file changes
     on every push.

  Each needs its own measurement on these cases, with at least two runs per arm.

## Limits

- **One run per lever, two baseline runs.** The per-case spread between the two baselines reaches
  25 % (#482: $0.48 and $0.36), so T's −4 % is not distinguishable from zero. F's −17 % and
  T+F+R's −29 % are consistent across cases (5 of 6 and 6 of 6 below both baselines).
- **Local, not CI.** Claude Code 2.1.316 on the owner's login, against 2.1.304 with an API key in
  CI. The reported cost is Claude Code's own `total_cost_usd`. The local session listed the
  owner's skills in its system prompt; it is the same in every arm and is a cached prefix of
  about 5,000 tokens.
- **Reconstructed state.** The open threads at each moment come from today's resolution state plus
  the field's replies. PR titles and bodies are today's.
- **Audited findings are few and all Low.** The one real Medium bug found in a re-review (#478
  `c573b8e`, `pendingInit`) was not run, to stay within the cap. Its two batches cost about $1.24
  a run. The shipped T changes only which threads it receives: 5 of its 7, the two left out being
  "addressed" threads on files the push did not touch.

## Reproduce

Needs Bun, `jq`, Claude Code logged in, a kaipu-record clone, a wachiman checkout per engine, and
one detached worktree of the clone per head under `$HEADS/kaipu-<sha7>`.

```sh
cd harness
# One run: case id from cases.tsv, a label for the output dir; --dry-run stops before the paid call.
ENGINE=/path/to/wachiman ./run.sh 483-0253fd7 base --dry-run
# A lever, with a scratch engine that has levers-prototype.patch applied:
ENGINE=/path/to/wachiman-with-patch WACHI_X_THREADS=delta ./run.sh 483-0253fd7 T
./spent.sh                                # total reported cost of every traced call
bun classify.ts ../raw/runs/483-0253fd7/base   # one run's classes, context costs and timeline
bun table.ts ../raw/runs > ../tables.md        # every table above
python3 requests.py ../raw/runs/483-0253fd7/base/call-1.jsonl   # per-request cache writes and reads
```

`raw/runs/<case>/<arm>/` holds each call's trace (`call-N.jsonl`; the init event's list of local
skills and plugins is removed), argv, prompt, provider result, engine log and classification.
`dry/` holds the baseline prompt from a free dry run, and `dry-shipped/` holds the shipped
engine's log. `raw/state/` holds the PR metadata and today's thread-resolution dump.
[`tables.md`](tables.md) is `table.ts`'s output.
