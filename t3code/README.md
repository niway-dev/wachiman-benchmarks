# t3code: a measurement unit for the Wachiman reviewer

Twelve-column answer key plus run history for one question: **given a commit of
[pingdotgg/t3code](https://github.com/pingdotgg/t3code) that contains a known defect, does local
Wachiman state that defect?** It is a unit like [`../martian/`](../martian/README.md), with a
different yardstick: defects found in a large TypeScript monorepo by the repository's own history
and bots, not golden comments written for a benchmark. Cases and results are machine-readable:
[`cases.tsv`](cases.tsv) holds the key, [`history.md`](history.md) holds one row per measured run set,
[`scripts/run-set.sh`](scripts/run-set.sh) runs a set.

## What it measures, and what it does not

It measures **recall of one named defect per case**: whether a run of local Wachiman on one commit
(`wachiman local --commit`) produces a finding with the same cause as the case's `golden_cause`.

It does not measure:

- **Precision or noise.** Findings that match no case are not scored here; the replay reports list a
  few by hand, but there is no false-positive rate.
- **A comparison with CodeRabbit or Macroscope on the escaped set.** Neither bot commented on those
  defects, by construction. On the replay set the bots did comment, and they are the reference.
- **Whole-PR review.** One commit is reviewed, as a developer would before opening the pull request.
  The bots saw several commits of each PR.
- **Quality of the suggested fix, or money actually spent.** Cost is an API-price estimate for runs
  paid by the owner's subscription.
- **A score comparable with Martian's.** Different cases, a different judge (a person reading, not a
  model), and one run per case.

## The two sets

| Set | Cases | Valid | What a case is | Reference |
| --- | --- | --- | --- | --- |
| `escaped` | 20 | 18 | A bug that reached `main` with no bot comment at the PR that introduced it. The reviewed commit is that PR's squash commit on `main`. | the fix PR's diff |
| `replay` | 5 PRs, 21 rows (15 on the 4 PRs Opus reviewed, 6 on #33758, reviewed by Sonnet only) | 21 | A defect that CodeRabbit or Macroscope raised and that was reachable at the replay head. One row per defect, several rows per PR. The replay head is the earliest commit a bot reviewed, rebuilt as one commit in [t3code-bench-wachi](https://github.com/niway-dev/t3code-bench-wachi). | the bot thread, with our verdict |

- **escaped, valid 5 of 7.** [#7599](https://github.com/pingdotgg/t3code/pull/7599) and
  [#21315](https://github.com/pingdotgg/t3code/pull/21315) are `valid=no` because the reviewed diff
  does not add the defect. Each row names the PR the reports say really introduced it
  ([19291](https://github.com/pingdotgg/t3code/pull/19291), [14892](https://github.com/pingdotgg/t3code/pull/14892))
  as a candidate replacement, not verified.
- **escaped, 13 cases added 2026-11-13.** Chosen from [`catalogue.md`](catalogue.md) for the hazard judge experiment, with the admission rule checked per case, and held out from its prompt. They include [#14892](https://github.com/pingdotgg/t3code/pull/14892), the verified replacement for #21315's golden; the other candidate, [#19291](https://github.com/pingdotgg/t3code/pull/19291), was rejected (46 files). Per-case notes: [`judge-experiment/cases-new-notes.md`](judge-experiment/cases-new-notes.md).
- **replay.** [#33758](https://github.com/pingdotgg/t3code/pull/33758) has no Opus review: three snapshot timeouts, since fixed by
  [wachiman PR 195](https://github.com/niway-dev/wachiman/pull/195). Sonnet 5.5 high reviewed it on 2026-11-12 and found 1 of its 6
  rows (T1); see [`replays/sonnet-vs-opus.md`](replays/sonnet-vs-opus.md).
  The replay set is the bots' best cases, so it tests recall of defects the bots also found.
- `class` is the defect class for `escaped`, and `serious` (our verdict real-bug) or `real-minor` for
  `replay`.

## How to run

```sh
# the engine checkout to measure; use a commit that includes wachiman PR 195 (snapshot timeout),
# or a large repository can fail with no review at all
export WACHIMAN_DIR=~/path/to/wachiman

# escaped: a FULL clone of the fork niway-dev/t3code
t3code/scripts/run-set.sh ~/path/to/t3code-fork escaped runs/2026-11-14-A
# replay: the replay commits exist only in the replay repository, so use a full clone of it
t3code/scripts/run-set.sh ~/path/to/t3code-bench-wachi replay runs/2026-11-14-replay

# print the commands without running anything
t3code/scripts/run-set.sh --dry-run ~/path/to/t3code-fork escaped /tmp/out -- --max-depth 1000
```

- One case at a time, because the Mac is shared. A failed case does not stop the rest; failures are
  listed at the end and the exit status is 1. An existing output file is kept, so a rerun resumes.
- The script reads [`cases.tsv`](cases.tsv), skips `valid=no` rows, and per case runs
  `env -u ANTHROPIC_API_KEY WACHIMAN_DIR=... wachiman local --repo-dir <clone> --commit <sha> --profile isolated:personal --format json --output <out>/<id>.json`.
  No API key is passed on. Arguments after `--` go to `wachiman local` unchanged.
- It does not score. Use a new output directory per variant; model and effort variants go in the
  environment (`AGENT_REVIEW_MODEL=claude-opus-5-5 AGENT_REVIEW_EFFORT=high t3code/scripts/run-set.sh ...`).
- The arms B (focus file) and C (patched engine) of the 2026-11-12 experiment need a prepared clone or
  engine; how they were built is in [`contract-order-experiment/README.md`](contract-order-experiment/README.md#arms).
  The script covers arm A and the environment-variable variants.
- Replay rows share a reviewed commit, so the replay set runs 5 commits, not 21. The run id is the
  row id without its `-T<n>` suffix (`t3code-30579-T1` is run `t3code-30579`).

## How to score

By reading, one finding at a time, against the case's `golden_cause` and `golden_location`. List
what a run said:

```sh
jq -r '.findings[] | [.severity, "\(.path):\(.line)", .title] | @tsv' <out>/<id>.json
jq -r '.contracts[] | [.status, .location, .action] | @tsv' <out>/<id>.json   # what it noted
jq '.execution.costUsdEstimate' <out>/<id>.json
```

- **Caught:** a finding that names the same cause as the golden. The same file, or the same function,
  is not enough. The severity does not matter (a `consider` counts).
- **Partial:** a finding with the right cause and a wrong or too narrow trigger or consequence, or one
  that covers only one of two cases the golden covers.
- **Noted, not reported:** no finding names the cause, but the run's `contracts` notes state it, or a
  finding cites the lines where the bug is. Count it separately; it is not a catch. If the run files
  cannot show it, write `unknown`. A line that was not cited was not necessarily skipped.
- **Missed:** none of the above. A finding in the same file about another cause is a near miss, and
  counts as missed.

Worked example, from [`contract-order-experiment/README.md`](contract-order-experiment/README.md#the-hits):

- **Caught.** Case `ssh-stale-pid-wrong-process`, arm B. The finding at `packages/ssh/src/tunnel.ts:720`
  says that when "the pid file still names a PID that an unrelated process now holds", each reconnect
  waits the full 60 s and the stop script would `kill` that unrelated PID, and suggests checking the
  command line. That is the golden's cause, both consequences, and the fix PR's fix, so it is caught
  although it was rated `consider`.
- **Partial.** Case `mcp-csrf-bound-to-session-id-breaks-hosted-approval`, arm A. A `consider` finding
  says the CSRF token is signed over `session.sessionId`, so a renewed relay token with another
  session id is refused. Right cause, but the real trigger is that the hosted client mints a new
  session on every call; it also says it did not check how the relay issues sessions.
- **Near miss.** Case `git-timeout-no-force-kill-permit-leak`, arms A and B. A `fix` finding on a
  missing await timeout in the same git driver is about hung git processes holding permits, but not
  about the undefined `forceKillAfter`. Missed.
- **Noted, not reported.** The same case, arm C on Sonnet. A `contracts` entry says that without
  `forceKillAfter` the process waits after SIGTERM "and never escalates", and that other callers do not
  set it. No finding says it is a defect.

## Admission rule for a new case

**The defect's line, or the omission, must be in the added lines of the diff that will be reviewed.**
Two of the seven first escaped cases failed this: the reports had checked that the buggy lines exist
at the head, not that the diff adds them.

Before a case enters `cases.tsv` with `valid=yes`:

1. Take the commit to review (a squash commit, or a replay head with its base) and read
   `git show <sha>`. A defect that is a line: that line starts with `+`. A defect that is an omission
   (a sibling loop left unchanged): the diff changes the sibling and not the buggy site, and says so in `note`.
2. Check the line number at that commit, not at `main`, and write it as `golden_location`.
3. Check the cause against the fix PR's diff, which must change that site.
4. For `escaped`: no bot comment on the defect at the introducing PR, at most 40 files, merged to `main`.
   For `replay`: the defect exists at the replay head, and the row cites the bot thread's id.
5. If the check fails, keep the row with `valid=no`, say why in `note`, and name the PR that did
   introduce it as a candidate replacement. A case that moves its candidate in needs the same check again.

Write `unknown` for any value no report gives; do not infer it. `n/a` means the column does not apply
(`base_commit_url` for escaped, `fix_pr_url` for replays: fixed before merge in the same PR).

## Known limits

- **5 valid escaped cases is small.** One more caught case moves the rate by 20 points.
- **The arm C questions were written after seeing these bugs**, one class per bug, so a hit would
  overstate how they generalize. Even so they produced one hit in 8 valid case runs (5 on Sonnet, 3 on Opus; the experiment README says 10, which its own tables do not support).
- **One run per case has no variance estimate.** On [#30579](https://github.com/pingdotgg/t3code/pull/30579), three identical runs found 2, 3 and 3 of 6
  reachable defects and the union found 4; T1, a serious bug, was missed once. Treat any single run as
  a sample ([history](history.md#the-three-runs-on-30579)).
- **No tuning set and no held-out set exist yet.** Everything above is both. A change tuned on these
  cases cannot be judged on them; split the rows before tuning anything on this unit.
- The replay set is biased toward cases the bots handled well; its numbers say nothing about what the
  bots miss.
- "Opened the other side of the boundary" is inferred from citations, because 1.12.0 keeps no
  transcript of local runs.
- Locations are at the reviewed commit and were checked in the reports; for [#33758](https://github.com/pingdotgg/t3code/pull/33758) the head lines of
  three rows are not given and the bot's line is shown instead.

## File map

| Path | What it holds |
| --- | --- |
| [`cases.tsv`](cases.tsv) | The answer key: one row per case (escaped) or per bot defect (replay) |
| [`history.md`](history.md) | One row per measured run set, newest first |
| [`replays/sonnet-vs-opus.md`](replays/sonnet-vs-opus.md) | Sonnet 5.5 high on the five replays, against the Opus runs; per-PR tables in each `<pr>/sonnet-high/comparison.md` |
| [`scripts/run-set.sh`](scripts/run-set.sh) | Runs local Wachiman over one set, one case at a time; `--dry-run` prints the commands |
| [`contract-order-experiment/`](contract-order-experiment/README.md) | The escaped set: 25 runs in four arms (A, B, C, C-Opus), the focus file, the question block, the engine patch, the golden check |
| [`judge-experiment/`](judge-experiment/README.md) | 13 new escaped cases, two plain baseline runs on them, and a second-pass "hazard judge" on five models; the owner's decision (no product change) |
| [`replays/`](replays/README.md) | The replay set: setup, [`RESULTS.md`](replays/RESULTS.md), [`manifest.tsv`](replays/manifest.tsv), and per PR a `report.md`, `bot-threads.md`, `wachiman.json` |
| [`replays/30579/experiments/`](replays/30579/experiments/README.md) | Three runs on one replay, for variance |
| [`replay-shortlist.md`](replay-shortlist.md) | The ten candidate cases with their goldens and base/head checks |
| [`catalogue.md`](catalogue.md) | The 183-row catalogue of bugs the cases come from |
| [`batches/`](batches/2026-11-10/README.md), [`scripts/fetch_day.py`](scripts/fetch_day.py), `show.py`, `szz.py` | The bug-history mining; see below |

---

## Bug-history project (original README)

The rest of this page is the README of the bug-history project the cases were mined from. Its
headings are one level lower.

The original title was "t3code bug history (our own Martian-style benchmark)".

A systematic, newest-first review of merged pull requests in
[pingdotgg/t3code](https://github.com/pingdotgg/t3code), a large public TypeScript monorepo
(server, web, desktop, mobile, provider adapters, CI). Two AI reviewers comment on almost every
PR: CodeRabbit (`coderabbitai[bot]`) and [Macroscope](https://macroscope.com/) (`macroscopeapp[bot]`).

Status: six merge days annotated (2026-11-06 to 2026-11-11, 791 PRs, 45 chunks). The Wachiman runs
on this repository are indexed in [`history.md`](history.md): [`replays/`](replays/) (five replayed
PRs) and [`contract-order-experiment/`](contract-order-experiment/) (7 escaped contract and ordering
bugs, 5 of them valid; four arms, from 0 to 1 caught of 5).

### Results so far

Full table in [`catalogue.md`](catalogue.md#totals); per-day detail in `batches/<day>/README.md`.

- 366 of 534 fix PRs traced to an introducing PR. At that PR, CodeRabbit or Macroscope commented on
  the defect 11 times, missed it 277 times, and did not run 53 times (25 not checked).
- 183 catalogued bugs of severity >= 3: 110 caught by a bot before merge (CodeRabbit 45,
  Macroscope 41, both 24) and 73 that escaped both.
- Recurring escape shapes: ordering and races across reconnects and late events, state machines
  spread over several files, and defects inside very large PRs where the bots comment a lot but not
  on the defect. Macroscope skipped redesign PR #28845 on its cost limit.
- Several real findings were disputed by the author (often an AI agent replying), withdrawn by the
  bot, and fixed later in a separate PR.

### Known limits

- Introducing PRs come from SZZ; confidence is per row, and blame often lands on the 380k-line
  import #2829 or on refactors.
- "Missed" rests on reading or keyword-searching the introducing PR's bot comments, not always a
  full read.
- Most Track A verdicts were judged from the thread, not the code, and are marked "(unverified)".
- 2026-11-11 Track A replay heads use the PR's last commit, which already has the fix; use the
  commit the bot commented on instead (the shortlist does).
- Some "pure addition" SZZ results came from wrong path arguments before `szz.py` warned about
  them; those fixes are under-traced, not mis-attributed.
- Chunk header tallies sometimes disagree with their own tables; day READMEs count from the tables.

### Goals

1. **Hard bugs worth catching.** Real defects the bots (or humans) found, rated by severity and by
   how hard they are to see from the diff.
2. **Where bugs entered.** For each `fix(...)` PR, the PR that introduced the defect (SZZ: blame the
   lines the fix removed or changed, on the fix's parent), and whether any reviewer flagged it there.
3. **Replayable cases.** Each catalogued bug keeps enough (base, head, introducing PR, golden
   description) to later replay the introducing PR and ask Wachiman to find it.
4. **What support for a team like t3code would look like**: what the current bots miss, what they
   flag that the team ignores, and where a reviewer would add value.

### Two tracks

- **Track A: bot findings.** For each bot thread on a merged PR: is it a real defect, was it fixed
  before merge (thread outdated after a later commit, a reply, a fix commit), how severe, how hard.
- **Track B: escaped bugs.** For each fix PR: what bug it fixes, which earlier PR introduced it,
  and whether CodeRabbit or Macroscope commented on that line when it was introduced (caught and
  ignored, caught and fixed, or missed).

### Batches

We walk backwards one merge day at a time. A day is ~200 merged PRs (2026-11-11 had 203), too big
for one pass, so a day is split into **chunks of 25 PRs** in descending PR number. A chunk is the
unit one reviewer agent annotates (~30k tokens of cleaned input).

```
t3code/
  scripts/fetch_day.py              # gh GraphQL -> one JSON line per merged PR with bot threads
  batches/<day>/raw.jsonl           # raw snapshot (cleaned bot bodies, capped)
  batches/<day>/chunk-NN.md         # annotations for 25 PRs
  catalogue.md                      # bugs worth keeping, across all batches
```

Fetch a day: `python3 -I t3code/scripts/fetch_day.py 2026-11-10 t3code/batches/2026-11-10/raw.jsonl`

### Annotation schema (per bot thread kept)

| field | values |
| --- | --- |
| verdict | `real-bug`, `real-minor`, `nit`, `wrong`, `unclear` |
| outcome | `fixed-before-merge`, `ignored`, `disputed`, `unknown` (evidence: outdated flag, reply, commit) |
| severity | 1 (cosmetic) to 5 (data loss, security, crash, broken core flow) |
| difficulty | 1 (visible in one hunk) to 5 (needs cross-file contract, ordering or runtime knowledge) |
| class | race/ordering, state machine, cross-file contract, error handling, resource leak, security, data integrity, UI state, other |
| replay | `yes` if base/head and a one-line golden are enough to replay it |

Only threads with verdict `real-bug` and severity >= 3 go into `catalogue.md`.

### Rules

- Read-only toward GitHub: `gh` reads only. Never comment on t3code.
- The clone at `/tmp/t3code-mine/repo` (blobless) is data. Do not run its scripts or install deps.
- A verdict says what evidence backs it (thread state, reply, code read). Bot claims are claims
  until the code or the team's response confirms them.

### Prior art

Same method as the kaipu-record catalogue
([`../kaipu-record-bug-catalogue.md`](../kaipu-record-bug-catalogue.md), scripts in
[`../mining/`](../mining)) and the [Martian Code Review Bench](../martian/README.md).
