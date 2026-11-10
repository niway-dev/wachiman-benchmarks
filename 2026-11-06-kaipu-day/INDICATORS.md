# Indicators and conclusions: Wachiman vs CodeRabbit on kaipu-record, 2026-11-06

This file explains every number in this folder: which CSV it comes from, how it is computed, what it
tells us and why it can mislead. Every value below is produced by
`bun scripts/indicators.ts 2026-11-06-kaipu-day` and stored in `indicators.json`; none is typed by
hand. `README.md` has the day's headline and the per-pair detail; this file has the arithmetic.

## One-minute block

- **What we can conclude:** the two tools are complementary, not interchangeable. On the 6
  distinct defects I verified by reading the code, Wachiman found 5, CodeRabbit found 3 and 2 were
  found by both. If the 8 owner-accepted rows are added (file-level evidence only) there are 13
  distinct defects: Wachiman 9, CodeRabbit 7, both 3. Neither tool alone covers the set.
- **What we cannot conclude:** that Wachiman is better. The sample is 14 commit pairs and 6
  verified defects, from one day, one repository and one judge, and no finding was judged wrong,
  so false positives are not measured.
- **Operational gap, not quality gap:** Wachiman completed 26 of 33 observed commits (3 more
  partial, 0 refused). CodeRabbit completed 17 of 33 and skipped 4 because of its own settings
  (stacked pull requests and path filters). Only 14 commits (42%) are comparable.
- **Possibly cheap misses:** 4 confirmed defects were found only by CodeRabbit: one verified (a
  failed-save reset, #542, low, difficulty 3) and three owner-accepted (focus indicator,
  movability check, test cleanup) whose severity and difficulty are my unread estimates, low and 2
  to 3. Nothing high severity was found by either tool. That the misses are cheap is a hypothesis.
- **Cost:** $7.16 on the 14 pairs, $16.34 for every Wachiman review of the day. 56% of the spend
  falls outside the pairs, so the pairs understate the real day.

## Where each number comes from

| File | Made by | Holds | Feeds |
| --- | --- | --- | --- |
| `pairs/reviews.csv` | `pair.ts` | one row per review a tool completed, skipped or left partial, with status, version, model, cost, findings count | coverage, cost |
| `pairs/pairs.csv` | `pair.ts` | one row per commit both tools completed, with both finding counts, Wachiman's cost and the minutes between the two reviews | pair rate, cost per pair, timing |
| `pairs/special-cases.csv` | `pair.ts` | every commit that is not a pair, with the reason it is not comparable | coverage failures |
| `pairs/findings.csv` | `pair.ts` | one row per posted finding, with `comparison` = `paired` or `special`, Wachiman's `fix`/`consider` label and `topic` | counts of findings, label and topic indicators |
| `verdicts.csv` | by hand (claude-sonnet-5-5) | one row per paired finding: `verified`, `owner-accepted` or `unverified`, severity, difficulty, `matched_by` | every quality indicator |
| `pairs/pairs.md` | `pair.ts` | the pairs and special cases as tables | reading only |
| `indicators.json` | `scripts/indicators.ts` | every number in this file | this file |

The rule behind every comparison: a **pair** is one commit both tools finished. A finding is
compared only when its commit is a pair (`comparison: paired`). Everything else is a special case:
reported, never counted in a comparison.

## 1. Coverage: did each tool review the commits? (`reviews.csv`, `special-cases.csv`)

| Indicator | Formula | Value |
| --- | --- | --- |
| Commits seen | distinct (PR, commit) in `reviews.csv` | 33 |
| Pair rate | pairs / commits seen | 14 / 33 = **42.4%** |
| Wachiman completed | distinct commits with status `completed` / commits seen | 26 / 33 = **78.8%** |
| Wachiman partial, refused | rows with status `partial`, `refused` over commits seen | 3 / 33 = **9.1%**, 0 |
| CodeRabbit completed | same formula | 17 / 33 = **51.5%** |
| CodeRabbit skipped | rows with status `skipped` | 4 |
| Special-case rows vs commits | rows in `special-cases.csv` vs distinct commits in it | 22 rows, 19 commits |

**What it tells us.** Wachiman did run on almost every commit; CodeRabbit did not. All 4
CodeRabbit skips come from its own configuration: path filters (#540, #549) and "auto reviews are
off on non-default base branches" (#546, #547, stacked pull requests). Those are settings, so they
say nothing about its review quality. The 3 Wachiman partials are all on #540.

**Why it can mislead.**
- "Commits seen" is the commits at least one tool left a record on. A commit neither tool touched
  is not counted, so the real denominator is unknown.
- "Completed" can mean a review of only the changes since the previous commit; it is not always a
  review of the whole pull request.
- The 22 special-case rows overlap on commits (a commit can appear once per tool). Never add 22 to
  14 as a commit count: the commit count is 19 + 14 = 33.

## 2. Quality: were the findings right? (`findings.csv` + `verdicts.csv`)

### 2.1 What the verdict words mean

| Verdict | Meaning | Strength of evidence |
| --- | --- | --- |
| `verified` | I read the code at that commit and the defect is real | strong |
| `owner-accepted` | the owner changed the cited file after the comment | weak: compares files, not lines, so the file may have changed for another reason |
| `unverified` | not read, not fixed | none: listed, never scored |
| `wrong` | the finding is false | **0 rows**: nobody was judged wrong |

"Confirmed" below means `verified` plus `owner-accepted`.

### 2.2 Counts per tool (paired findings only)

| | Findings | Verified | Owner-accepted | Unverified | Wrong | Confirmed |
| --- | --- | --- | --- | --- | --- | --- |
| Wachiman | 18 | 5 | 4 | 9 | 0 | 9 |
| CodeRabbit | 10 | 3 | 4 | 3 | 0 | 7 |

Wachiman also posted 38 findings on commits that are not pairs. They are in `findings.csv` as
`comparison: special` and are in no indicator here.

### 2.3 Defects, not rows

Three defects were found by both tools, so three pairs of rows describe one defect each. A defect
is counted once.

| Indicator | Formula | Value |
| --- | --- | --- |
| Distinct verified defects | verified rows, a matched pair counted once | 8 rows = **6 defects** |
| Distinct confirmed defects | confirmed rows, a matched pair counted once | 16 rows = **13 defects** |
| Recall on verified defects | defects the tool found / 6 | Wachiman 5/6 = **83%**; CodeRabbit 3/6 = **50%** |
| Recall on confirmed defects | defects the tool found / 13 | Wachiman 9/13 = **69%**; CodeRabbit 7/13 = **54%** |
| Overlap | defects both found / distinct defects | verified 2/6 = **33%**; confirmed 3/13 = **23%** |
| Only one tool | confirmed defects found by exactly one tool | Wachiman only 6, CodeRabbit only 4 |

The three matched defects are the screenshot zoom-out that enlarges and crops tall images (#543,
verified), the pager that disappears when the open version is outside the passed order (#543,
verified; Wachiman and CodeRabbit worded it differently and one fix covers both) and the history
arrows that miss pushes while unmounted (#545, owner-accepted).

**What it tells us.** The union is larger than either tool alone (verified: 6 against 5 and 3;
confirmed: 13 against 9 and 7), and the overlap is small, so each tool finds things the other does
not. This is the strongest result of the day, and the verified figures carry it: the confirmed ones
lean on file-level evidence.

**Why it can mislead.** Recall here is against the defects the two tools found, not against all
defects in the code: a defect both missed is invisible. With 6 verified defects, one defect moves a
recall figure by about 17 points, so read 83% and 50% as ranges.

### 2.4 Precision (`verdicts.csv`)

| Indicator | Formula | Value |
| --- | --- | --- |
| Verified-only lower bound | verified / all findings | Wachiman 5/18 = **28%**; CodeRabbit 3/10 = **30%** |
| Accepted-or-verified share | confirmed / all findings | Wachiman 9/18 = **50%**; CodeRabbit 7/10 = **70%** |
| Unverified share | unverified / all findings | Wachiman 9/18 = **50%**; CodeRabbit 3/10 = **30%** |
| Among resolved | (verified) / (verified + wrong) | 5/5 and 3/3 = 100% |

**What it tells us.** Almost nothing yet. The 100% among resolved findings is meaningless because
I never marked a finding `wrong`, so the true precision is somewhere between the verified-only
lower bound and 100%. The accepted-or-verified share is not a true lower bound: an accepted row may
be an unrelated change to the same file. The most useful number is the unverified share: half of
Wachiman's result is still open.

### 2.5 Does Wachiman's own label carry information? (`findings.csv` label + verdicts)

| Label | Findings | Confirmed | Unverified | Confirmed among judged |
| --- | --- | --- | --- | --- |
| `fix` | 5 | 4 | 1 | 4/4 |
| `consider` | 13 | 5 | 8 | 5/5 |

**What it tells us.** Nothing yet. `fix` looks better (4 of 5 against 5 of 13) only because 8 of
the 13 `consider` rows are unverified, against 1 of 5 for `fix`. Among the rows I judged, both
labels were right every time. The label is worth testing once the unverified rows are judged.

### 2.6 Test-quality notes (`topic = tests`, Wachiman only)

6 of Wachiman's 18 paired findings (33%) are about tests: 2 owner-accepted, 4 unverified, 0
verified. Tuning to reduce them would be premature: unverified is not the same as noise. CodeRabbit
rows carry no `topic`, so this cannot be compared.

### 2.7 Severity and difficulty (`verdicts.csv`, hand-written)

Among the 6 verified defects: severity 0 high, 2 medium, 4 low; difficulty (1 to 5, how hard for a
human reviewer to find) 1, 4, 1 at levels 2, 3 and 4. Six defects cannot show whether either tool
finds high-severity defects; both scales are my judgement. For the 8 owner-accepted rows they are
estimates made without reading the changed lines.

## 3. Cost (`pairs.csv`, `reviews.csv`)

| Indicator | Formula | Value |
| --- | --- | --- |
| Wachiman on pairs | sum of `wachiman_cost_usd` in `pairs.csv` | **$7.16** |
| Per pair | sum / 14 | mean $0.511, median $0.36 |
| Largest pair | #543 `d70421e` | $2.50 = 34.9% of the pair cost |
| Per confirmed finding | $7.16 / 9 | $0.80 |
| Per verified defect | $7.16 / 4 | $1.79 |
| All Wachiman reviews | sum of `cost_usd` over Wachiman rows in `reviews.csv` | **$16.34** |
| Outside pairs | all − pairs | $9.18 = 56.2% |
| Partial reviews | status `partial` | $1.32 |
| Zero-finding pairs | pairs with 0 Wachiman findings | 7 pairs, $2.15 (30% of pair cost) |
| CodeRabbit cost | not published | not published |

**What it tells us.** The cost of a day is the $16.34, not the $7.16. The 7 pairs with no
Wachiman finding cost $2.15, a candidate for an effort cap on small incremental commits, though
part of that spend is the price of confirming a commit is clean.

**Why it can mislead.** One pull request (#543, five commits) carries a large part of the pair
cost. "Per verified defect" is inflated by the 9 unverified findings. A CodeRabbit comparison needs
its cost, which it does not publish.

## 4. Timing (`pairs.csv` `minutes_apart`)

`minutes_apart` is the time between the two tools' review submissions: median 1 minute, mean 23.8,
range −2 to 309, 12 of 14 pairs within 5 minutes. The outlier is #541 (309 minutes).

This is not review latency. The files carry no push time, so it cannot say how long either tool
took. Use it only to confirm the pairing is fair: the two tools reviewed the same commit at about
the same time.

## 5. Conclusions and what to do next

**Concluded (supported by the data):**
1. The tools are complementary: 6 verified defects (2 shared) and 13 confirmed ones (3 shared)
   (§2.3).
2. Wachiman's coverage was high (79% completed, 0 refused); CodeRabbit's gaps come from its
   settings (§1).
3. The day cost $16.34, of which the paired part is 44% (§3).

**Not concluded (the data does not support it):**
1. That Wachiman is better or worse. The 5-vs-3 verified lead is six defects.
2. That Wachiman's `fix` label is more reliable than `consider`: the gap comes from how many rows
   were verified (§2.5).
3. That the defects only CodeRabbit found are cheap: only one of the four is verified (§2.3).
4. A precision figure. No finding was judged `wrong`.
5. Anything about the 38 Wachiman findings on non-pair commits.
6. Why a tool missed a defect: `findings.csv` carries no commands or cited files.
7. Any trend: one day, one release (v1.8.0), one repository.

**Next, in value order:**
1. Verify the 12 `unverified` rows, starting with the path-traversal finding on #543 and the
   `setSize` finding on #541, and mark any false one `wrong`. Until then precision stays a range.
2. Have a second judge re-judge a sample, since every verdict here is mine.
3. Add days. Six defects cannot support a release decision; the same script runs on any day.
4. Replace the owner-accepted file-level check with a line-level one.

## Reproduce

```sh
bun scripts/indicators.ts 2026-11-06-kaipu-day
```

It reads `pairs/*.csv` and `verdicts.csv`, writes `indicators.json` and prints it. If a verdict
changes, rerun it and update the numbers in this file from the new JSON.
