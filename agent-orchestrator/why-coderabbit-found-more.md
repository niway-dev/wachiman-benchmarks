# Why CodeRabbit found more than Wachiman on agent-orchestrator

Investigation of the difference measured in [Equal conditions](README.md#equal-conditions-every-coderabbit-review-event-both-sides-judged-blind-2026-11-26),
2026-11-26. Basis: `rerun`. We cannot see how CodeRabbit works inside; everything below is what the data
shows, and each cause is marked as measured or as a hypothesis.

## One-minute block

- **The gap.** On the same 24 review events, CodeRabbit raised 55 real defects and Wachiman 26. Of the 47
  defects only CodeRabbit raised, 7 are medium and none high.
- **No special tool shows up.** CodeRabbit's reviews ran on its default `CHILL` profile, with no
  configuration file from the repository and no linter named in the review info.
- **Four patterns explain the 47** (measured counts, hypothetical causes):
  1. the decisive fact sits outside the changed lines (20);
  2. two async steps interleave (16);
  3. an outside API rule (8) or a failure between two steps (4);
  4. Wachiman looked at the same function but said something weaker (17).
- **Project memory: a small, visible part.** 3 of CodeRabbit's real defects say "Source: Learnings", and
  all 3 are CodeRabbit-only. Wachiman ran with no memory for this repository. How much the learnings shape
  the other comments is unknown.
- **Go: no extra penalty in this sample.** The gap is about 2x in both languages (Go 23 vs 10, TypeScript
  32 vs 16). Wachiman's engine has no Go-specific code path, and our benchmarks have no Go set until this one.
- **Open:** whether a bigger context pack and a memory for the repository close the gap. Both checks are
  listed in [Next checks](#next-checks).

## Method

- **Data.** 24 CodeRabbit review events on 10 merged PRs, each replayed with Wachiman v1.17.0 on the exact
  range the review names ([`replays/events.tsv`](replays/events.tsv)).
- **Judging.** Both tools' items were judged blind against the code at the event head. The verdicts are in
  [`replays/judging-2026-11-26/`](replays/judging-2026-11-26/).
- **Classifying the 47.** Each CodeRabbit-only defect was then classified by a Sonnet 5.5 high worker that
  read the code at the event head. For each one it recorded:
  - where the decisive fact sits;
  - what a reviewer must know to see it;
  - the closest Wachiman finding in the same event;
  - a hypothesis for the miss.

  One row per defect, with a link to the CodeRabbit comment:
  [`coderabbit-only-why.tsv`](replays/judging-2026-11-26/coderabbit-only-why.tsv).

How to read the findings:

| You want | Read |
| --- | --- |
| The 47, with links to CodeRabbit's comments | [`coderabbit-only-why.tsv`](replays/judging-2026-11-26/coderabbit-only-why.tsv) |
| Both tools on one review, side by side | [`packages/<pr>.md`](replays/judging-2026-11-26/packages/), unblinded with [`judge-key.tsv`](replays/judging-2026-11-26/judge-key.tsv) |
| Wachiman's findings as it wrote them | [`runs-2026-11-26-events/<event>.json`](replays/runs-2026-11-26-events/) |
| The PRs | [9086](https://github.com/OrchestratorInc/agent-orchestrator/pull/9086), [8720](https://github.com/OrchestratorInc/agent-orchestrator/pull/8720), [9076](https://github.com/OrchestratorInc/agent-orchestrator/pull/9076), [8832](https://github.com/OrchestratorInc/agent-orchestrator/pull/8832), [9095](https://github.com/OrchestratorInc/agent-orchestrator/pull/9095), [9036](https://github.com/OrchestratorInc/agent-orchestrator/pull/9036), [8714](https://github.com/OrchestratorInc/agent-orchestrator/pull/8714), [9148](https://github.com/OrchestratorInc/agent-orchestrator/pull/9148), [9055](https://github.com/OrchestratorInc/agent-orchestrator/pull/9055), [8764](https://github.com/OrchestratorInc/agent-orchestrator/pull/8764) |

## The four patterns

### 1. The decisive fact sits outside the changed lines (20 of 47)

In 10 cases the fact is in the same file, outside the hunks. In the other 10 it is in a file the PR did not
touch. Only 6 of the 47 are visible from the diff alone.

Example: [#9148](https://github.com/OrchestratorInc/agent-orchestrator/pull/9148#discussion_r4709941353).
The PR adds a skills list to the chat screen. When the harness changes, that list is not cleared. The
cleanup lives in `mobile/lib/chat/useConversation.ts`, which the PR did not touch.

Hypothesis: before the review, Wachiman builds a context pack from the symbols and call sites around the
change. **The pack was marked `truncated` (about 15 KB) in 23 of the 24 runs.** The file a defect needed
may not have made it in. This is not measured: the run records do not list which files the model read.

### 2. Two async steps interleave (16 of 47)

These are "check, wait, act on a stale fact" and two actors crossing each other.

Example: [#8764](https://github.com/OrchestratorInc/agent-orchestrator/pull/8764#discussion_r4642390054)
checks that a session has not expired before a long wait, not after it.

Hypothesis: seeing these means following the steps in time. Wachiman runs one batch of 4 to 30 turns
(mostly 10 to 20) and has no step that does this on purpose.

### 3. An outside rule (8) or a failure between two steps (4)

- Outside rules: GitHub, React Native accessibility props, Vitest matchers, git behavior.
- Failures between two steps. Example:
  [#9086](https://github.com/OrchestratorInc/agent-orchestrator/pull/9086#discussion_r4698550172) deletes
  and saves the state before calling the provider. If the process dies in between, that state is lost.

### 4. Wachiman looked at the right place and said something weaker (17 of 47)

Wachiman had a finding on the same function but stated a different or weaker problem.

Example: [#9086](https://github.com/OrchestratorInc/agent-orchestrator/pull/9086#discussion_r4698550180).
CodeRabbit saw that an incomplete cross-platform listing makes a device look stopped. Wachiman, on the same
function, flagged only that it was slow.

Wachiman's attention also went elsewhere: 38 of its 64 findings were "add a test" or doc wording.

In 4 of these 17 (9036-r1-i02, 8714-r3-i04, 8764-r1-i03, 8764-r1-i06), Wachiman probably reported the same
defect in other words and the judge did not merge them. If that holds, the counts become 12 shared and 43
CodeRabbit-only.

## The two variables proposed by the owner

### Project memory

CodeRabbit keeps "learnings" per repository, built from earlier reviews and replies, and uses them on its
own. agent-orchestrator has more than 9,000 PRs, and CodeRabbit reviews them.

Measured:

- **4 of CodeRabbit's 62 comments end with "Source: Learnings".** 3 of them are real and CodeRabbit-only:
  - [9086-r1-i06](https://github.com/OrchestratorInc/agent-orchestrator/pull/9086#discussion_r4698550196): an ownership cleanup
    that must recheck state after the listing;
  - [8714-r1-i07](https://github.com/OrchestratorInc/agent-orchestrator/pull/8714#discussion_r4632273215): return focus after a
    dialog, following the repository's `returnFocus` pattern in `ArchiveModalHost.tsx`;
  - [9055-r2-i06](https://github.com/OrchestratorInc/agent-orchestrator/pull/9055#discussion_r4695283982): a restore barrier.

  The fourth (9086-r2-i01) was judged false.
- **Wachiman ran with no memory for this repository.** It has a memory feature in v1.17.0 (team entries
  under `.wachiman/memory/` and personal entries on the laptop). Entries are written on purpose, never
  learned automatically, and agent-orchestrator has none (no `.wachiman/` at the PR heads, and no personal entries on this laptop).

Not known: whether learnings shape comments that do not carry the label. Pattern 1 (facts in unchanged
files) is the kind of thing a memory of the repository would help with, but we cannot see CodeRabbit's
learnings to check.

**Reading: memory explains at least 3 of 47 directly. It may explain more, and that is not measured.**

### Go support

Measured on this sample:

| Language | CodeRabbit real | Wachiman real | Wachiman style | Distinct defects only CodeRabbit | Shared | Only Wachiman |
| --- | --- | --- | --- | --- | --- | --- |
| Go | 23 | 10 | 10 | 20 | 3 | 7 |
| TypeScript | 32 | 16 | 25 | 27 | 5 | 11 |

- **The gap is about 2x in both languages.** On Go, Wachiman made fewer noise findings, not more.
- **The engine is language-neutral.** The context pack in `src/evidence.ts` finds symbols and call sites by
  searching text. It skips Go keywords and recognizes `_test.go` files, and nothing else in it is specific
  to Go. It found symbols on every run, Go or TypeScript (5 to 72 per run).
- **Our benchmarks had no Go set before this one.** t3code is TypeScript. So we have never measured Go
  recall alone; this sample has 30 distinct Go defects, which is too few to rule out a Go-specific gap.

**Reading: nothing here shows that Go is worse. The lack of a Go benchmark is real and worth fixing.**

## Is it a regression? Three versions

v1.4.0 and v1.9.0 were replayed on the same 24 events and judged in one blind pass with v1.17.0 and
CodeRabbit ([results](README.md#three-wachiman-versions-on-the-same-events-2026-11-26)). Each version
finds 23 to 27 distinct real defects against CodeRabbit's 54, so the gap is not a regression. Only 9
defects were found by all three versions and 24 by exactly one. Together the three runs reach 45, so part
of the gap is that one Wachiman run is a sample of what it could find.

## Why Martian looked close and this does not

On [Martian's bench](../martian/README.md), Wachiman v1.9.0 on Sonnet 5.5 high reached 68% to 78% recall on
Cal.com's 10 PRs over three runs, with 35% to 43% precision. CodeRabbit, re-judged through the same route on
the same 10 PRs, had 78% recall and 33% precision. The two measurements answer different questions:

| | Martian | This unit |
| --- | --- | --- |
| Answer key | 173 human-curated goldens, 66 of them High or Critical | every real defect either tool raised |
| A real defect that is not on the key | counts as a false positive | counts for the tool that raised it |
| What wins | finding the serious bugs someone listed | breadth, including many low-severity defects |
| Severity of what CodeRabbit adds | | 40 of its 47 unique defects in the first pass are low |

Martian's key is selective, so CodeRabbit's extra minor findings cost it precision instead of earning
recall. Here, every real finding counts, and CodeRabbit raises many more small real defects. On the
serious end the two results agree: on Martian Wachiman finds most High and Critical goldens (44 to 54 of
66 across Sonnet runs), and here the only high-severity defect was found by CodeRabbit and by two of the
three versions.

Reading: Wachiman is close to CodeRabbit on the serious bugs a curator lists, and well behind it on the
volume of small real defects in a busy repository. Both are true; which one matters is a product choice.

## What is known and what is not

| Claim | Status |
| --- | --- |
| CodeRabbit raised about 2x the real defects at the same commits | Measured, one blind judge |
| 20 of 47 need a fact outside the changed lines | Measured by one classifier |
| Wachiman's context pack was truncated in 23 of 24 runs | Measured from the run logs |
| Truncation is why Wachiman missed those 20 | Hypothesis |
| 3 CodeRabbit-only defects came from its learnings | Measured from the label |
| Learnings explain more than those 3 | Unknown |
| Go is not worse than TypeScript for Wachiman | Consistent with this sample, too small to settle |
| The gap is not a regression | Measured: v1.4.0, v1.9.0 and v1.17.0 are level, one run each |
| Martian and this unit disagree because their answer keys differ | Reasoned from the two methods, not tested |

## Next checks

1. **Context.** Rerun 3 or 4 of the "outside the changed lines" events with a larger context pack. If
   Wachiman then finds those defects, truncation is a cause.
2. **Memory.** Write a short memory for agent-orchestrator with what a long-time reviewer would know (the
   sibling patterns behind pattern 1, the platform-scoped listing, the restore barriers). Then rerun events
   whose PRs come later than every fact in it. Otherwise the memory leaks the answers.
3. **Go.** Add a Go-only set, from agent-orchestrator's backend or another Go repository, and score recall
   by language.
4. **The 4 doubtful pairs.** Have a second judge rule only on whether each pair is the same defect.
