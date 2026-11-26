# Martian run 2026-11-26: Wachiman v1.22.0 on Sonnet 5.5, effort high

- **Answer:** v1.22.0 scores inside the spread of the three v1.9.0 Sonnet 5.5 high runs on every
  quality measure, and its reviews cost slightly less ($16.54 against $16.95 to $17.94 for the 50).
  One run: it shows no regression, not an improvement.
- **Engine:** Wachiman v1.22.0 (`79ce0f0`), pinned with `WACHIMAN_DIR` (a `git archive v1.22.0`
  export; the installed CLI was 1.17.0), `claude-sonnet-5-5`, effort `high`, no verifier,
  `AGENT_REVIEW_BUDGET_USD=10`, two queues, `wachiman local` on the owner's subscription
  (`ANTHROPIC_API_KEY` unset). Same inputs, judge model and prompts as the v1.9.0 rows; the judge calls
  differed in one way, see "Judge cost rose".
- **Command:** `JUDGE_PORT=8897 WACHIMAN_DIR=/tmp/wachiman-1.22.0 QUEUES=2 ./scripts/run-weekly.sh 2026-11-26-v1.22.0-sonnet-5-5-high claude-sonnet-5-5 high`

## Against v1.9.0, same model and effort

| Measure | v1.9.0 Sonnet high (11-11, r2, r3) | v1.22.0 |
| --- | --- | --- |
| Recall | 70.5%, 67.6%, 71.1% | 69.9% |
| Precision | 39.1%, 35.8%, 36.2% | 38.2% |
| F1 (All profile) | 50.3%, 46.8%, 48.0% | 49.4% |
| F2 (Core profile) | 60.4%, 55.9%, 59.2% | 59.6% |
| High/Critical goldens found (of 66) | 52, 52, 54 | 54 |
| False positives | 190, 210, 217 | 196 |
| Reviews total | $17.94, $17.07, $16.95 | $16.54 |
| $/PR median | $0.30, $0.29, $0.27 | $0.24 |
| $/PR p90 | $0.57, $0.55, $0.54 | $0.44 |
| $/golden found | $0.15, $0.15, $0.14 | $0.14 |
| Partial reviews | 1, 0, 1 | 2 |

Costs are API-list-price estimates from the CLI, not a bill. Every quality figure is inside the
v1.9.0 range. The total cost is 2% below the cheapest v1.9.0 run, and the median and p90 per PR
are below all three; the saving is much smaller than on the kaipu-record replay (21%), where each
review runs more than twice as many batch calls (2.8 per review there, 1.2 here), so the
cheaper cache write counts for more of the bill.

## Partial reviews

Two reviews stopped short because one call reached its per-call cap ("not reached: the call ran
out of its budget"): `keycloak/36880` (1 of 10 files reviewed) and `sentry-greptile/5` (30 of 106
files reviewed). v1.9.0 had 0 or 1 per run, so this is within what earlier runs showed, but each
one costs recall on that PR.

## Judge cost rose, for a reason outside Wachiman

The judge (Claude Opus 4.5 through the Claude Code CLI, `judge_shim.py`) cost $107.96 for 1,296
calls, against $30.42 to $31.37 for the v1.9.0 runs. From `data/judge-calls/`:

| Judge, Opus 4.5 tokens | v1.9.0 high r3 | This run |
| --- | --- | --- |
| Cache reads | 0 | 84.2 M (about 65,000 per call) |
| 1-hour cache writes | 0.61 M | 5.06 M |
| Uncached input | 1.58 M | 0.01 M |

Each Opus judge call now carries about 69,000 prompt tokens, mostly read from the cache, against
about 1,500 in v1.9.0 r3. The cause, found after the run: the profile the judge runs in has claude.ai connectors (MCP servers),
and the Claude Code CLI loaded their tool definitions into every call even with `--tools ""`. One
test call (a one-line prompt, not a real judge prompt) measured 65,389 cached prompt tokens and
$0.063 as the shim ran; with `--strict-mcp-config` and an empty MCP config, 714 tokens and $0.005.
A real judge call adds its own prompt on top, which the v1.9.0 r3 figure of about 1,500 includes.
The connectors were added to the judge's profile after v1.9.0 r3 was judged; the fix returns the
calls to that condition. `scripts/judge_shim.py`
now passes both. Wachiman's own reviews already pass `--strict-mcp-config`
([`src/providers/claude-code.ts`](https://github.com/niway-dev/wachiman/blob/79ce0f0db5cbb3d627aa9b2a9bfa8bebbbea1215/src/providers/claude-code.ts#L225)), so its product cost
is not affected. The judge model is the same, so the scores stay comparable, though that the
extra tool definitions did not sway this run's judgments is not checked.

## Incident: the judge port was taken

The first judging pass failed: another program on the laptop began listening on port 8797, the
judge shim's fixed port, 14 seconds after the run started. The shim could not bind, and every
dedup and judge call got a 404 from that program. That pass was discarded whole, the bench was
rebuilt from Martian's upstream copy, and judging ran again on port 8897 with zero judge errors.
`scripts/run-weekly.sh` now takes `JUDGE_PORT` and stops when the port is already in use or the
shim does not start.

## Limits

- One run against three. A difference within the v1.9.0 spread is not a change.
- Same judge model, prompts and `judge_shim.py` (as it was before the MCP fix) as every row in
  [history.md](../../history.md), but this run's judge calls also carried the connector tool
  definitions that the earlier rows' calls did not (see "Judge cost rose"). That they did not
  move the scores is not checked. Not comparable with Martian's stored numbers.
- **Raw data kept as produced.** Three of the 50 review summaries end with a stray quote or carry
  literal `\n` sequences (for example `cal.com/22532`, `cal.com/14740`). v1.9.0 r3 has two such
  summaries, so this is an older Wachiman output defect, not new in v1.22.0. It does not reach
  scoring, which reads findings only.
