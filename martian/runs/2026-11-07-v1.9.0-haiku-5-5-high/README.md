# Arm 1: Haiku 5.5 high alone

- **Date:** 2026-11-07, 12:11 to 15:22 local.
- **What ran:** Wachiman v1.9.0 as released, `claude-haiku-5-5`, effort `high`, `wachiman local`, one
  run over Martian's 50 PRs with [`run-weekly.sh`](../../scripts/run-weekly.sh) (two review queues,
  eight judge calls in flight). Everything else as the [baseline](../2026-11-07-v1.9.0-opus-5-5/README.md).
- **One variable:** the review model. The judge route is the baseline's, so the rows compare.
- **Data:** [metrics.json](metrics.json), [data/](data/), [run.log](run.log).

## Result next to the baseline

| | Opus 5.5 high (baseline) | Haiku 5.5 high (arm 1) |
| --- | --- | --- |
| High+Critical found | 47/66 | 47/66 |
| Goldens found (recall, All) | 110 (63.6%) | 111 (64.2%) |
| Findings posted | 273 | 421 |
| False positives | 174 | 314 |
| Precision (All) | 38.7% | 26.1% |
| F1 (All) | 48.1% | 37.1% |
| F2 (Core, the site's metric) | 55.7% | 49.1% |
| Reviews, total (API list price) | $25.01 | **$8.98** |
| $/PR median · p90 · max | $0.48 · $0.61 · $2.31 | **$0.10** · $0.35 · $1.90 |
| $/golden found · $/High+Critical found | $0.23 · $0.53 | **$0.08** · **$0.19** |
| Minutes per PR, median · max | 1.4 · 4.4 | 3.6 · 26.5 |
| Partial reviews | 0 | 0 |

## Which bugs each finds

| | Both | Only Opus | Only Haiku | Either |
| --- | --- | --- | --- | --- |
| Goldens (of 173) | 96 | 14 | 15 | 125 |
| High+Critical (of 66) | 41 | 6 | 6 | 53 |

## Reading

- **Haiku finds as much as Opus for about a third of the cost** (a fifth at the median PR), and
  is 2.5 times slower.
- **It is much louder:** 314 false positives against 174, which costs 11 F1 points and 6.6 F2 points.
- **The two overlap heavily but not fully.** Each finds about 15 goldens the other misses; together
  they would reach 53 of 66 High/Critical, more than any tool in the reference tables, at the cost of
  even more noise.
- **That is exactly the premise of arm 3:** a cheap, loud proposer is worth it only if a falsifier
  removes the noise for less than the difference in cost ($16 on this bench). Arm 2 measures the
  falsifier on the baseline first.
- One run. A difference of 3 or fewer High/Critical goldens is noise; the recall tie is a tie.

## Cost of the measurement

The judge made 1,832 calls (about $37 at API list price, the owner's subscription in practice):
more than the baseline's ~1,075 because Haiku posts more findings.
