# Indicators and conclusions: Wachiman vs CodeRabbit on kaipu-record, 2026-11-06

This file explains every number in this folder: which CSV it comes from, how it is computed, what it
tells us and why it can mislead. Every value below is produced by
`bun scripts/indicators.ts 2026-11-06-kaipu-day` and stored in `indicators.json`; none is typed by
hand. `README.md` has the day's headline and the per-pair detail; this file has the arithmetic.

## One-minute block

- **What we can conclude:** the two tools are complementary, not interchangeable. Of 14 distinct
  confirmed defects, Wachiman found 9, CodeRabbit found 7, and only 2 were found by both. Using
  both would have caught 14; using one alone, at most 9.
- **What we cannot conclude:** that Wachiman is better. The sample is 14 commit pairs and 5
  verified defects, from one day, one repository and one judge, and no finding was judged wrong,
  so false positives are not measured.
- **Operational gap, not quality gap:** Wachiman completed 26 of 33 observed commits (3 more
  partial, 0 refused). CodeRabbit completed 17 of 33 and skipped 4 because of its own settings
  (stacked pull requests and path filters). Only 14 commits (42%) are comparable.
- **Cheap misses:** the 5 confirmed defects only CodeRabbit found are low severity and
  difficulty 2 to 3 (focus indicator, movability check, navigation order, a failed-save reset, test
  cleanup). Nothing high severity was found by either tool.
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
| Wachiman partial, refused | rows with status `partial`, `refused` | 3 (10%), 0 |
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
| Wachiman | 18 | 4 | 5 | 9 | 0 | 9 |
| CodeRabbit | 10 | 2 | 5 | 3 | 0 | 7 |

Wachiman also posted 38 findings on commits that are not pairs. They are in `findings.csv` as
`comparison: special` and are in no indicator here.

### 2.3 Defects, not rows

Two defects were found by both tools, so two pairs of rows describe one defect each. A defect is
counted once.

| Indicator | Formula | Value |
| --- | --- | --- |
| Distinct verified defects | verified rows, a matched pair counted once | 6 rows = **5 defects** |
| Distinct confirmed defects | confirmed rows, a matched pair counted once | 16 rows = **14 defects** |
| Recall on verified defects | defects the tool found / 5 | Wachiman 4/5 = **80%**; CodeRabbit 2/5 = **40%** |
| Recall on confirmed defects | defects the tool found / 14 | Wachiman 9/14 = **64%**; CodeRabbit 7/14 = **50%** |
| Overlap | defects both found / distinct defects | verified 1/5 = **20%**; confirmed 2/14 = **14%** |
| Only one tool | confirmed defects found by exactly one tool | Wachiman only 7, CodeRabbit only 5 |

The two matched defects are the screenshot zoom-out that enlarges and crops tall images (#543,
verified) and the history arrows that miss pushes while unmounted (#545, owner-accepted).

**What it tells us.** The union (14) is larger than either tool (9 and 7), and the overlap is
small, so each tool finds things the other does not. This is the strongest result of the day.

**Why it can mislead.** Recall here is against the defects the two tools found, not against all
defects in the code: a defect both missed is invisible. With 5 verified defects, one defect moves a
recall figure by 20 points, so read 80% and 40% as ranges.

### 2.4 Precision (`verdicts.csv`)

| Indicator | Formula | Value |
| --- | --- | --- |
| Lower bound | confirmed / all findings | Wachiman 9/18 = **50%**; CodeRabbit 7/10 = **70%** |
| Unverified share | unverified / all findings | Wachiman 9/18 = **50%**; CodeRabbit 3/10 = **30%** |
| Among resolved | (verified) / (verified + wrong) | 4/4 and 2/2 = 100% |

**What it tells us.** Almost nothing yet. The 100% among resolved findings is meaningless because
I never marked a finding `wrong`, so the true precision is somewhere between the lower bound and
100%. The most useful number is the unverified share: half of Wachiman's result is still open.

### 2.5 Does Wachiman's own label carry information? (`findings.csv` label + verdicts)

| Label | Findings | Confirmed | Share |
| --- | --- | --- | --- |
| `fix` | 5 | 4 | 80% |
| `consider` | 13 | 5 | 38% |

**What it tells us.** Wachiman's `fix` label is more reliable than `consider`, which is what a
severity label should do. Confirmed excludes the unverified rows, so `consider` is probably
undercounted.

### 2.6 Test-quality notes (`topic = tests`, Wachiman only)

6 of Wachiman's 18 paired findings (33%) are about tests: 2 owner-accepted, 4 unverified, 0
verified. Tuning to reduce them would be premature: unverified is not the same as noise. CodeRabbit
rows carry no `topic`, so this cannot be compared.

### 2.7 Severity and difficulty (`verdicts.csv`, hand-written)

Among the 5 verified defects: severity 0 high, 2 medium, 3 low; difficulty (1 to 5, how hard for a
human reviewer to find) 1, 3, 1 at levels 2, 3 and 4. Five defects cannot show whether either tool
finds high-severity defects; both scales are my judgement.

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
1. The tools are complementary: 14 confirmed defects in total, 2 shared (§2.3).
2. Wachiman's coverage was high (79% completed, 0 refused); CodeRabbit's gaps come from its
   settings (§1).
3. Wachiman's `fix` label is reliable on this sample, 4 of 5 (§2.5).
4. The defects CodeRabbit found and Wachiman did not are low severity and easy to moderate, so
   they are reasonable tuning candidates (§2.3).
5. The day cost $16.34, of which the paired part is 44% (§3).

**Not concluded (the data does not support it):**
1. That Wachiman is better or worse. The 4-vs-2 verified lead is five defects.
2. A precision figure. No finding was judged `wrong`.
3. Anything about the 38 Wachiman findings on non-pair commits.
4. Why a tool missed a defect: `findings.csv` carries no commands or cited files.
5. Any trend: one day, one release (v1.8.0), one repository.

**Next, in value order:**
1. Verify the 12 `unverified` rows, starting with the path-traversal finding on #543 and the
   `setSize` finding on #541, and mark any false one `wrong`. Until then precision stays a range.
2. Have a second judge re-judge a sample, since every verdict here is mine.
3. Add days. Five defects cannot support a release decision; the same script runs on any day.
4. Replace the owner-accepted file-level check with a line-level one.

## Reproduce

```sh
bun scripts/indicators.ts 2026-11-06-kaipu-day
```

It reads `pairs/*.csv` and `verdicts.csv`, writes `indicators.json` and prints it. If a verdict
changes, rerun it and update the numbers in this file from the new JSON.
