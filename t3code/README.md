# t3code bug history (our own Martian-style benchmark)

A systematic, newest-first review of merged pull requests in
[pingdotgg/t3code](https://github.com/pingdotgg/t3code), a large public TypeScript monorepo
(server, web, desktop, mobile, provider adapters, CI). Two AI reviewers comment on almost every
PR: CodeRabbit (`coderabbitai[bot]`) and [Macroscope](https://macroscope.com/) (`macroscopeapp[bot]`).

Status: six merge days annotated (2026-11-06 to 2026-11-11, 791 PRs, 45 chunks). No Wachiman run
has been made on this repo yet; the next step is replaying the cases in
[`replay-shortlist.md`](replay-shortlist.md) into a test repository.
Later runs: [`replays/`](replays/) (five replayed PRs) and
[`contract-order-experiment/`](contract-order-experiment/) (7 escaped contract and ordering
bugs, Wachiman 1.12.0 with and without a flow-tracing focus file: 0 and 1 caught).

## Results so far

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

## Known limits

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

## Goals

1. **Hard bugs worth catching.** Real defects the bots (or humans) found, rated by severity and by
   how hard they are to see from the diff.
2. **Where bugs entered.** For each `fix(...)` PR, the PR that introduced the defect (SZZ: blame the
   lines the fix removed or changed, on the fix's parent), and whether any reviewer flagged it there.
3. **Replayable cases.** Each catalogued bug keeps enough (base, head, introducing PR, golden
   description) to later replay the introducing PR and ask Wachiman to find it.
4. **What support for a team like t3code would look like**: what the current bots miss, what they
   flag that the team ignores, and where a reviewer would add value.

## Two tracks

- **Track A: bot findings.** For each bot thread on a merged PR: is it a real defect, was it fixed
  before merge (thread outdated after a later commit, a reply, a fix commit), how severe, how hard.
- **Track B: escaped bugs.** For each fix PR: what bug it fixes, which earlier PR introduced it,
  and whether CodeRabbit or Macroscope commented on that line when it was introduced (caught and
  ignored, caught and fixed, or missed).

## Batches

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

## Annotation schema (per bot thread kept)

| field | values |
| --- | --- |
| verdict | `real-bug`, `real-minor`, `nit`, `wrong`, `unclear` |
| outcome | `fixed-before-merge`, `ignored`, `disputed`, `unknown` (evidence: outdated flag, reply, commit) |
| severity | 1 (cosmetic) to 5 (data loss, security, crash, broken core flow) |
| difficulty | 1 (visible in one hunk) to 5 (needs cross-file contract, ordering or runtime knowledge) |
| class | race/ordering, state machine, cross-file contract, error handling, resource leak, security, data integrity, UI state, other |
| replay | `yes` if base/head and a one-line golden are enough to replay it |

Only threads with verdict `real-bug` and severity >= 3 go into `catalogue.md`.

## Rules

- Read-only toward GitHub: `gh` reads only. Never comment on t3code.
- The clone at `/tmp/t3code-mine/repo` (blobless) is data. Do not run its scripts or install deps.
- A verdict says what evidence backs it (thread state, reply, code read). Bot claims are claims
  until the code or the team's response confirms them.

## Prior art

Same method as the kaipu-record catalogue
([`../kaipu-record-bug-catalogue.md`](../kaipu-record-bug-catalogue.md), scripts in
[`../mining/`](../mining)) and the [Martian Code Review Bench](../martian/README.md).
