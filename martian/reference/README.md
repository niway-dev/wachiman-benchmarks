# The yardstick: judge route, calibration, and competitors re-judged

Martian's dataset already holds every listed tool's review comments on the 50 PRs. Martian judged
them through its own paid gateway. We judge through `scripts/judge_shim.py` (Claude Code CLI 2.1.319,
Claude Opus 4.5, the same prompts), and that route turned out stricter. So the competitors' **saved
comments** were re-judged through our route: nobody re-ran their products. Only Wachiman reviews code
on our machine.

**Refresh this directory when the route changes:** a new judge model, a major Claude Code CLI
version, or a change to `judge_shim.py`. Then re-run the calibration and the three reference tools,
and start a new section of [history.md](../history.md), because old rows are no longer comparable.

## Calibration (2026-11-07)

| Check | Result | File |
| --- | --- | --- |
| claude-code on Cal.com: Martian's stored judgment vs ours, same candidates and dedup | 22 vs 17 matches; 7 of 10 PRs identical; all 5 differences are matches Martian accepted and we rejected | `evaluations/calibration-claude-code-cal.json` |
| claude-code on Cal.com, our route twice | 17 vs 18 matches; 1 of 41 goldens differs | `evaluations/rejudge-cal-8-tools.json` |
| Three tools, all 50 PRs, ours minus stored | F1 −3.5 (augment), −5.1 (qodo-extended-v2), −3.5 (claude-code); Core F2 −3.8, −5.1, −3.6 | below |

Reading: the route is stable and systematically stricter, probably because the CLI cannot send
`temperature: 0` and frames the prompt in its own way.

## Same-judge scores

All 50 PRs (`evaluations/rejudge-cal-8-tools.json` for Cal.com, `evaluations/rejudge-other40-*.json`
for the other 40):

| Tool | High+Critical | Recall | Precision | F1 (All) | F2 (Core) | TP | FP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qodo-extended-v2 | 44/66 | 56.1% | 63.0% | 59.3% | 60.0% | 97 | 57 |
| augment | 46/66 | 59.0% | 57.0% | 58.0% | 60.2% | 102 | 77 |
| claude-code | 29/66 | 44.5% | 45.8% | 45.2% | 44.1% | 77 | 91 |

Cal.com only (10 PRs), eight tools:

| Tool | High+Critical | Recall | Precision | F1 |
| --- | --- | --- | --- | --- |
| copilot-v2 | 15/19 | 75.6% | 52.5% | 62.0% |
| augment | 15/19 | 68.3% | 54.9% | 60.9% |
| qodo-extended-v2 | 12/19 | 51.2% | 56.8% | 53.8% |
| macroscope | 13/19 | 43.9% | 51.4% | 47.4% |
| bugbot | 12/19 | 43.9% | 51.4% | 47.4% |
| claude-code | 10/19 | 43.9% | 50.0% | 46.8% |
| coderabbit | 18/19 | 78.0% | 33.3% | 46.7% |
| cubic-v2 | 11/19 | 43.9% | 45.0% | 44.4% |

## Martian's stored list, for context only

Core profile, F2, Martian's own Opus 4.5 judgments (`analysis/score_profiles.py --profile core
--beta 2.0`), 22 tools: qodo-extended-v2 65.1, cubic-v2 64.9, augment 64.0, qodo-v2 60.6, copilot-v2
58.0, gemini-v2 52.8, gitlab 52.7, sourcery 51.5, greptile-v4-1 51.2, coderabbit 51.1, macroscope
50.8, bugbot 48.6, claude-code 47.7, devin 44.8, greptile-v5 44.5, kodus-v2 41.5, codeant-v2 40.9,
copilot 40.6, baz 40.5, claude 38.9, kg 18.4, graphite 9.3.

Wachiman's place on it is an **estimate**: its raw Core F2 (55.7) would be 6th. Adding back the
judge offset measured above (3.6 to 5.1 points) gives about 59 to 61, about 4th or 5th. Only Martian
running the pipeline would make it a measurement.

## Files

- `evaluations/`: step3 evaluation files from our route (they contain Martian's golden comments,
  MIT, as Martian's own files do).
- `judge-calls/`: per-call logs of the reference re-judging (duration, model usage, estimated cost;
  no prompts).
- `shas/`: base and head of each PR as fetched, and the flattened merge-base commits.
