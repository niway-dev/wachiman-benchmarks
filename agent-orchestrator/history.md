# agent-orchestrator run history

One row per measured run set, newest first. Cost is the engine's `costUsdEstimate`, an API-price estimate
for runs paid by the owner's subscription (`jq -s 'map(.execution.costUsdEstimate) | add' <dir>/*.json`).

| Date | Engine | Reviewer | Variant | Set | Caught of valid | Partial | Est. cost | Run files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | v1.17.0 (`f6bd3afa`) | Sonnet 5.5, product defaults | first runs (verify off, history off, one run per PR) | 10 PRs, 34 valid CodeRabbit cases | **8 of 34** | 1 | $5.06 | [`replays/runs-2026-11-26/`](replays/runs-2026-11-26/) |
