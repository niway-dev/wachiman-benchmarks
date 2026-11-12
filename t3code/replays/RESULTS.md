# Results: Wachiman 1.12.0 run locally on five t3code replays

Wachiman 1.12.0 (main at `fd99401`) reviewed each replay head on the owner's Claude subscription
(`--profile isolated:personal`, no API key). No other reviewer was run. The bot side comes from the
CodeRabbit and Macroscope threads saved in each `bot-threads.md`. Each replay head is the earliest
commit a bot reviewed, so a run there shows what a developer would have seen locally before
opening the pull request.

## One minute

- On the four replays that ran, Wachiman found every serious bug the bots raised on code present at
  the head. Each one was fixed before merge, usually the way Wachiman proposed.
- It found nothing serious that both bots missed. This was expected from the selection: the five
  PRs were chosen because the bots made several useful comments on them, so they are the bots'
  best cases. Measuring what Wachiman finds that the bots do not needs the escaped-bug cases in
  [`../replay-shortlist.md`](../replay-shortlist.md).
- Its misses are mostly real-minor edge cases. On #30579, three identical runs show these misses
  are run-to-run variance, not a fixed blind spot. Each run found 2 or 3 of the 6 reachable
  defects, and the three runs together found 4. One run also missed T1, a serious bug. See
  [`30579/experiments/README.md`](30579/experiments/README.md).
- The local snapshot step failed often on this 31k-file repository. Its 60 s timeout
  (`TIMEOUT_MS` in `src/connectors/local-git.ts`) is too short when the laptop is loaded and an
  on-access scanner is running (probable cause, not confirmed). #33758 never got a review.

## Per replay

| t3code PR | Replay | Wachiman findings | Matched bot defects | Bot defects missed (reachable at head) | Wachiman-only | Cost (API-price estimate) |
| --- | --- | --- | --- | --- | --- | --- |
| [#30579](30579/report.md) | [#1](https://github.com/niway-dev/t3code-bench-wachi/pull/1) | 2 | 2 serious (T1, T2/T6) | 4 real-minor (T3, T4, T5, T8) | 0 | $0.57 |
| [#32830](32830/report.md) | [#2](https://github.com/niway-dev/t3code-bench-wachi/pull/2) | 5 | 1 (T1/T3, raised by both bots) | 1 real-minor (T2) | 4: 3 real-minor, 1 real but unlikely trigger | $0.64 |
| [#24079](24079/report.md) | [#3](https://github.com/niway-dev/t3code-bench-wachi/pull/3) | 1 | 1 (T1), partly T3 | 2 (T2, T6) | 0 | $0.61 |
| [#30556](30556/report.md) | [#5](https://github.com/niway-dev/t3code-bench-wachi/pull/5) | 2 | 1 serious (T1/T4), partly T2 and T5 | none worth fixing | 0 | $0.71 |
| [#33758](33758/report.md) | [#4](https://github.com/niway-dev/t3code-bench-wachi/pull/4) | — | — | — | — | no review: 3 snapshot timeouts |

On #30579, runs 2 and 3 also found two findings that no bot raised. N1, a real cosmetic layout bug,
was checked in the code. N2 is plausible but was not verified.

## Next

1. Rerun #33758 once the snapshot can complete.
2. File the snapshot timeout as a Wachiman defect: a large repository on a busy laptop gets no
   review at all.
3. Replay the six escaped-bug cases in `../replay-shortlist.md`, run only Wachiman, and count the
   bugs it catches that both bots missed.
