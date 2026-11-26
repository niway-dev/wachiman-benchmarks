# agent-orchestrator: CodeRabbit-caught defects replayed on local Wachiman

A measurement unit like [`../t3code/`](../t3code/README.md), on
[OrchestratorInc/agent-orchestrator](https://github.com/OrchestratorInc/agent-orchestrator), a public
repository with a Go backend and a TypeScript/React frontend (desktop and mobile). Its pull requests are
reviewed by CodeRabbit. The question: **given the exact range CodeRabbit first reviewed on a merged PR, does
local Wachiman state the defects CodeRabbit raised and the PR's author then fixed?**

Wachiman is fed by open-source projects on purpose: this folder is public evidence of what it misses.

## Equal conditions: every CodeRabbit review event, both sides judged blind (2026-11-26)

The [first batch](#recall-of-owner-accepted-findings-first-batch-2026-11-26) below is one-directional.
Its answer key is CodeRabbit's fixed findings, so it cannot say what Wachiman found that CodeRabbit did not.
Its "8 of 34" also set one Wachiman run per PR against comments CodeRabbit posted across several commits.
This section replaces that comparison with one where each side gets the same input and the same judge.

**The rule.** A pair is one CodeRabbit review event: the commit it reviewed and the exact range its review
body names ("between X and Y"). Wachiman runs on that same range. When a later push triggers another
CodeRabbit review, that event is replayed as well. Both tools' findings then go into one shuffled list per
event, with the tool's name, its severity labels and every "Addressed" marker removed. A judge reads the code
at the event's head and rules on each item.

- **24 events on 10 PRs** ([`replays/events.tsv`](replays/events.tsv)). CodeRabbit posted 62 comments (60
  inline, 2 "outside diff range", no nitpicks). Wachiman made 64 findings
  ([`replays/runs-2026-11-26-events/`](replays/runs-2026-11-26-events/)), for $8.78 API-price estimate.
- **Judge:** Sonnet 5.5 high, one blind pass, four workers. Each item gets a verdict: `real` (the defect
  exists at head and causes wrong behavior), `style` (true, but no wrong behavior: docs, naming, a missing
  test), `false` or `unsure`. A real item also gets a severity and the later commit that fixed it. Items in
  one event that describe the same defect are merged into one defect. Packages, key and verdicts are in
  [`replays/judging-2026-11-26/`](replays/judging-2026-11-26/); `python3 -I scripts/score-events.py
  replays/judging-2026-11-26` prints the tables.

| Tool | Items | Real | Style | False | Unsure | Real, fixed later in the PR |
| --- | --- | --- | --- | --- | --- | --- |
| CodeRabbit | 62 | **55** | 2 | 3 | 2 | 47 |
| Wachiman | 64 | **26** | 38 | 0 | 0 | 14 |

| Distinct real defects | Low | Medium | High | Total |
| --- | --- | --- | --- | --- |
| Found by both | 3 | 4 | 1 | 8 |
| Only CodeRabbit | 40 | 7 | 0 | 47 |
| Only Wachiman | 17 | 1 | 0 | 18 |

What this says:

- **CodeRabbit found about twice as many real defects** at the same commits: 55 against 26. Of the 55,
  47 were found only by CodeRabbit, 7 of them medium.
- **Wachiman found 18 real defects CodeRabbit did not raise**, all but one low. Few were fixed later:
  the authors never saw them.
- **The one high-severity defect was found by both:** the New task page re-renders forever in #9148.
- **Most of Wachiman's findings were not defects.** 38 of 64 are `style`, mostly "add a test for this
  path" and doc wording, posted as `consider`. CodeRabbit posted almost none of those. Wachiman's 12
  `fix` and `blocker` findings were real in 9 cases.
- **Neither tool was often wrong.** CodeRabbit had 3 false and 2 unsure, Wachiman none.

Limits of this comparison: one judge, one pass, one model. The judge never saw the tool names, but the two
tools write differently (CodeRabbit leads with a bold title), so the blinding is imperfect. "Fixed later"
favors CodeRabbit by construction: its comments were posted on the PR and the authors answered them.
Wachiman ran weeks later (basis `rerun`) on v1.17.0, one run per event.

## Recall of owner-accepted findings (first batch, 2026-11-26)

> One-directional, kept for the gap analysis below. For the comparison between the tools, read
> [Equal conditions](#equal-conditions-every-coderabbit-review-event-both-sides-judged-blind-2026-11-26).

- **10 merged PRs** (3 Go, 3 mixed, 4 TypeScript), **34 valid cases**: each is a CodeRabbit finding that was
  fixed later in the same PR and whose line is in the reviewed diff. One more row is `valid=no`.
- **Wachiman found 8 of 34, plus 1 partial; it missed 25.** Basis: `rerun`. Wachiman ran on a laptop at
  the same base..head that CodeRabbit reviewed, weeks later. It never ran live on these PRs.
- **Engine:** Wachiman v1.17.0 (`f6bd3afa`), `claude-sonnet-5-5`, product defaults (verify off, history off),
  profile `isolated:personal`. One run per PR.
- **Cost:** $5.06 API-price estimate for the 10 runs (sum of `execution.costUsdEstimate`), paid by the
  subscription. CodeRabbit's cost is not published.
- **What CodeRabbit found that Wachiman did not** (25 misses and the partial), by kind of check (details in [Gaps](#gaps)):
  1. a fact that sits in a file outside the changed hunks (6);
  2. interleavings on state the change shares across calls (6);
  3. crash and partial-failure windows around a side effect (3);
  4. a rule of an external API or tool (4);
  5. a UI control whose handler disagrees with its enabled state (3);
  6. an invariant between parts and a whole: rounding against a total, a cap across sources, a dedup key,
     route identity (4).
- **None of the 25 misses is high severity.** By our judgement, 4 are medium and the rest are low or none.
  The bot's labels are 4 Major and 21 Minor.

## What it measures, and what it does not

It measures **recall of CodeRabbit's owner-accepted findings**. Each run gets the same diff CodeRabbit
first reviewed. A case is scored by reading, as in t3code: `caught`, `partial`, `noted`, `missed`.

It does not measure:

- **Precision.** Wachiman made 32 findings; the 8 that match a case are scored. The others are judged only
  in [Equal conditions](#equal-conditions-every-coderabbit-review-event-both-sides-judged-blind-2026-11-26).
- **What CodeRabbit misses.** The cases are CodeRabbit's best findings by construction.
- **A live comparison.** These are not pairs in the sense of `scripts/pair.ts`, which reads posted reviews.
  The pairing is by construction: the same base and head, recorded in [`replays/manifest.tsv`](replays/manifest.tsv).
- **Variance.** One run per PR. On t3code, three identical runs found 2, 3 and 3 of 6 defects.

## Files

| Path | What it holds |
| --- | --- |
| [`cases.tsv`](cases.tsv) | The answer key: one row per CodeRabbit finding, with its thread, fix sha, our severity and difficulty, and what a reviewer must know beyond the diff |
| [`replays/manifest.tsv`](replays/manifest.tsv) | Per PR: base, head (the earliest commit CodeRabbit reviewed), PR totals |
| [`replays/runs-2026-11-26/`](replays/runs-2026-11-26/) | One `<pr>.json` (the ReviewResult) and `<pr>.log` per run, and `scores.tsv` (the verdict per case) |
| [`history.md`](history.md) | One row per measured run set |
| [`mining.md`](mining.md) | How the cases were mined and verified, with the funnel |
| [`scripts/run-set.sh`](scripts/run-set.sh), [`scripts/fetch-heads.sh`](scripts/fetch-heads.sh) | Run local Wachiman over the manifest; fetch the PR heads first |
| [`scripts/mining/`](scripts/mining/) | The throwaway mining scripts, kept for provenance (`AO_CLONE` is the clone path) |

## How to run

```sh
export WACHIMAN_DIR=~/path/to/wachiman   # the engine checkout; pins the version
agent-orchestrator/scripts/fetch-heads.sh ~/path/to/agent-orchestrator
agent-orchestrator/scripts/run-set.sh ~/path/to/agent-orchestrator agent-orchestrator/replays/runs-<date>
agent-orchestrator/scripts/run-set.sh --dry-run ~/path/to/agent-orchestrator /tmp/out   # print only
```

- The clone must be full, not shallow. Each row gets a worktree on a throwaway branch `ao-replay/<pr>` at
  head, because the engine refuses a detached HEAD. `wachiman local --base <base>` runs there, then the
  worktree and the branch are removed. The clone's own checkout is not touched.
- One PR at a time. `ANTHROPIC_API_KEY` is never passed on. An existing JSON is kept, so a rerun resumes.
- Model and effort variants go in the environment. Use a new output directory per variant.

## How to score

The same rules as [t3code](../t3code/README.md#how-to-score), against `golden_cause` and `golden_location`:

```sh
jq -r '.findings[] | [.severity, "\(.path):\(.line)", .title] | @tsv' replays/runs-<date>/<pr>.json
```

**Caught** means the same cause; the same file is not enough. **Partial** means the right cause with a wrong
trigger or site. **Missed** is everything else. A finding in the same file on another cause is a near miss,
which counts as missed; `scores.tsv` names it in `note`.

## Admission rule for a new case

1. A merged PR into `main`, at most 40 files and 3000 added lines.
2. **Head** is the earliest commit CodeRabbit reviewed, meaning the one that is an ancestor of every other
   commit it commented on. It must still be reachable. **Base** is the merge base of the merge commit's
   first parent and head.
3. The finding was fixed later in the PR. That is either CodeRabbit's "Addressed in commit" marker with
   the fix as an ancestor of the PR head, or a later commit that changes that site the way the bot asked.
   The second kind needs reading: the heuristic picked the wrong fix sha in 3 of 11 rows of the first batch.
4. The defect's line is an added line of `git diff base head`, at a line number taken at head.
5. The claim holds when the code at head is read. If the thread shows the bot was wrong, the row is kept
   with `valid=no` and the reason.

Nitpicks and "Outside diff range" items are not mined yet. They live in review bodies, without a thread
or a marker. That is the kind of the #9068 gap, so it is the next thing to add.

## Results, first batch

| PR | Area | Diff (base..head) | Cases | Caught | Partial | Wachiman findings | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [9086](https://github.com/OrchestratorInc/agent-orchestrator/pull/9086) | go | 5 files, +532 | 4 | 0 | 0 | 1 | $0.43 |
| [8720](https://github.com/OrchestratorInc/agent-orchestrator/pull/8720) | go | 7 files, +498 | 3 | 1 | 0 | 3 | $0.53 |
| [9076](https://github.com/OrchestratorInc/agent-orchestrator/pull/9076) | go | 5 files, +455 | 3 | 0 | 1 | 4 | $0.54 |
| [8832](https://github.com/OrchestratorInc/agent-orchestrator/pull/8832) | mixed | 21 files, +751 | 2 | 1 | 0 | 3 | $0.72 |
| [9095](https://github.com/OrchestratorInc/agent-orchestrator/pull/9095) | mixed | 14 files, +743 | 2 (+1 invalid) | 0 | 0 | 3 | $0.48 |
| [9036](https://github.com/OrchestratorInc/agent-orchestrator/pull/9036) | mixed | 20 files, +659 | 4 | 2 | 0 | 4 | $0.58 |
| [8714](https://github.com/OrchestratorInc/agent-orchestrator/pull/8714) | ts | 22 files, +485 | 5 | 0 | 0 | 5 | $0.55 |
| [9148](https://github.com/OrchestratorInc/agent-orchestrator/pull/9148) | ts | 14 files, +474 | 2 | 2 | 0 | 4 | $0.29 |
| [9055](https://github.com/OrchestratorInc/agent-orchestrator/pull/9055) | ts | 6 files, +127 | 4 | 0 | 0 | 1 | $0.45 |
| [8764](https://github.com/OrchestratorInc/agent-orchestrator/pull/8764) | ts | 17 files, +996 | 5 | 2 | 0 | 4 | $0.49 |
| **Total** | | | **34** | **8** | **1** | **32** | **$5.06** |

What it caught includes the one serious-looking case of the batch. In #9148, an unstable `select` callback
re-renders the New task page forever, and Wachiman rated it `blocker`. It also caught deleted files offered
in @-completion (#8832), a cache key that leaks one project's skills to others (#9148), a resume route
applied after an unbounded wait (#8764), invisible buttons VoiceOver can still reach (#8764), and two
telemetry boundaries (#9036).

## Gaps

The 25 missed cases and the partial one, grouped by the check that would have found them. Severity and
difficulty (1 to 5) are ours, from the verification pass. Everything else is in `cases.tsv`.

### 1. A fact outside the changed hunks (6)

The diff is correct only if a file it does not change behaves a certain way, and it does not.

| Case | What a reviewer had to open | Sev / diff. |
| --- | --- | --- |
| ao-8714-C3 | `artifactContentUrl` always rewrites through the local daemon base URL, so a remote session reads from the wrong host | medium / 4 |
| ao-8764-C3 | `store.tsx`: `config` stays null for unpaired and cloud-only users, so a restore gated on `config !== null` never runs | medium / 4 |
| ao-9055-C1 | `processFiles` still counts the submitted files against the limit, so a file for the next message is rejected | low / 4 |
| ao-9095-C1 | `skill_metadata.go` searches the skill roots in another order than discovery, so the metadata shown belongs to another copy | low / 4 |
| ao-8764-C1 | `app/_layout.tsx` declares `/conversation-actions` as a sheet that the new transient list omits | low / 4 |
| ao-9076-C2 (partial) | `devices/service.go` feeds `NoteBooted` from a cached listing, so an older boot id can replace a newer one | low / 4 |

Two of these are other readers of the same data (9095-C1, 8764-C1). That is
[the proposal to list readers of extended types](https://github.com/niway-dev/wachiman/issues/314). The
other four are the contract of a function or store the added lines depend on. That proposal as written
would not list those.

### 2. Interleavings on shared state (6)

| Case | What happens | Sev / diff. |
| --- | --- | --- |
| ao-9086-C4 | `Open` lists devices before taking the lock; a device booted meanwhile looks stopped and loses its records | low / 4 |
| ao-8720-C2 | Two resolvers both see "not fresh" before either records an attempt (check-then-act) | low / 3 |
| ao-9076-C1 | A boot that happens between the helper start and `recordBoots` is accepted as the helper's own | low / 4 |
| ao-9076-C3 | A boot change during a hub replacement is stored but schedules nothing | low / 3 |
| ao-9055-C3 | `finally` deletes the in-flight entry by key without owning it, removing a second restore's barrier | low / 3 |
| ao-9055-C4 | The upload reads the restore entry after it was deleted, so an attachment posts to a failed restore | low / 3 |

Wachiman did raise concurrency findings in the same PRs, at other sites. In #9076 one of them is the
partial above. In #8720 one is a near miss.

### 3. Crash and partial-failure windows (3)

| Case | What happens | Sev / diff. |
| --- | --- | --- |
| ao-9086-C1 | The lease end is saved before the parked record is written; a stop in between leaks a booted simulator | low / 3 |
| ao-9086-C2 | Records are deleted and saved before `Shutdown`; an exit during it forgets a running device | low / 3 |
| ao-9086-C3 | `Provider.List` succeeds with one platform failed; absence is read as "stopped" and the device leaks | medium / 4 |

### 4. A rule of an external API or tool (4)

| Case | Rule | Sev / diff. |
| --- | --- | --- |
| ao-8714-C1 | GitHub answers 301 for a transferred issue; the destination's repository is not checked (not verified live) | medium / 4 |
| ao-8714-C2 | Artifact names cannot contain parentheses; `gh` strips them, the new direct API call does not | low / 5 |
| ao-8720-C3 | A renamed remote default can leave an old `refs/remotes/origin/<branch>`, so the fetch is skipped | low / 4 |
| ao-9036-C4 | Long Animation Frames: ResizeObserver callbacks run after `styleAndLayoutStart` | low / 5 |

8714-C2 has a general shape: replacing a wrapper with a direct call loses whatever the wrapper normalized.

### 5. A UI control that disagrees with its handler (3)

| Case | What happens | Sev / diff. |
| --- | --- | --- |
| ao-9055-C2 | Remove is enabled during an optimistic send, but its handler returns early on `submitInFlight` | low / 3 |
| ao-8714-C4 | The dialog has no trigger, and the menu's focus restore is skipped, so focus lands on `body` | low / 4 |
| ao-8714-C5 | Without the desktop bridge the lookup returns an empty list, so the desktop-required error never shows | low / 3 |

### 6. An invariant between parts and a whole (4)

| Case | What happens | Sev / diff. |
| --- | --- | --- |
| ao-9036-C2 | Each step is truncated to ms on its own, so the steps no longer sum to the total | none / 2 |
| ao-8832-C2 | The cap is applied source by source, so a changed file from a later source is dropped | low / 3 |
| ao-9095-C2 | Plugins are deduplicated before the manifest name is resolved (contrived trigger) | low / 3 |
| ao-8764-C2 | The restore compares pathnames only, so `?hostId=` is ignored and the wrong machine stays selected | low / 3 |

### Where the gaps went

Every gap above is filed on a Wachiman issue as a case, with no change to Wachiman itself:

- group 1 on [readers of extended types](https://github.com/niway-dev/wachiman/issues/314);
- groups 2 to 6 on [the rule inventory and candidate rules](https://github.com/niway-dev/wachiman/issues/315).

## Known limits

- **One run per PR, one model.** A rerun may catch or miss different cases.
- **Basis `rerun`, not live.** The engine is v1.17.0, run on 2026-11-26. It is not what CI would have run
  on the day.
- **The judge.** Opus 5.5 scored the cases. A second pass on Sonnet 5.5 high verified the 27 rows Wachiman
  did not catch, by reading the code at head and the fix; it found one invalid row and three wrong fix shas.
  The 8 caught cases were not re-verified, and no blind second judge scored the matches.
- **11 of 34 rows have no "Addressed" marker.** Their acceptance rests on a later commit changing the site.
  All 11 were read; for 3 the fix sha was corrected.
- **Severity is low overall.** 25 misses, none high. The batch says more about breadth of checks than
  about serious escapes.
- **Several cases are narrow:** 9095-C2, 9076-C1, 9076-C2, 8764-C2, 8720-C2 and 9036-C2 need rare timing
  or a constructed input.
- **8714-C1 rests on GitHub's documented behavior.** It was not reproduced.
