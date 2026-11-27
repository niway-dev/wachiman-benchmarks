# agent-orchestrator run history

One row per measured run set, newest first. Cost is the engine's `costUsdEstimate`, an API-price estimate
for runs paid by the owner's subscription (`jq -s 'map(.execution.costUsdEstimate) | add' <dir>/*.json`).

| Date | Engine | Reviewer | Variant | Set | Caught of valid | Partial | Est. cost | Run files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | v1.9.0 (tag) | Sonnet 5.5 high | every CodeRabbit review event (24); joint blind pass with CodeRabbit, v1.4.0, v1.17.0 | 10 PRs, 24 events, 60 findings | 27 distinct real defects vs CodeRabbit 54 (16 shared) | - | $8.41 | [`replays/runs-2026-11-26-v1.9.0/`](replays/runs-2026-11-26-v1.9.0/), [judging](replays/judging-2026-11-26-versions/) |
| 2026-11-26 | v1.4.0 (tag), offline `gh` shim | Sonnet 5.5 high | same events, same joint pass | 10 PRs, 24 events, 65 findings | 25 distinct real defects vs CodeRabbit 54 (14 shared) | - | $8.54 | [`replays/runs-2026-11-26-v1.4.0/`](replays/runs-2026-11-26-v1.4.0/), [judging](replays/judging-2026-11-26-versions/) |
| 2026-11-26 | v1.17.0 (`f6bd3afa`) | Sonnet 5.5, product defaults | every CodeRabbit review event (24), same range; both tools judged blind | 10 PRs, 24 events, 62 CodeRabbit and 64 Wachiman items | real defects 26 vs CodeRabbit 55 (8 shared) | - | $8.78 (14 new runs $3.72 + first batch) | [`replays/runs-2026-11-26-events/`](replays/runs-2026-11-26-events/), [judging](replays/judging-2026-11-26/) |
| 2026-11-26 | v1.17.0 (`f6bd3afa`) | Sonnet 5.5, product defaults | first runs (verify off, history off, one run per PR) | 10 PRs, 34 valid CodeRabbit cases | **8 of 34** | 1 | $5.06 | [`replays/runs-2026-11-26/`](replays/runs-2026-11-26/) |
