# Probe 2026-11-26: does Claude Code alone stop earlier on a subscription token?

- **Question:** the [release bisect](../2026-11-26-release-bisect/README.md) found that the same
  Wachiman batch call makes about 15 turns on an API key and about 9 on a Claude subscription
  token. Does a plain Claude Code call, with no Wachiman in between, do the same?
- **Method:** [`replay/credential-probe.yml`](../replay/credential-probe.yml), started by hand in
  [kaipu-bench-wachi-v3](https://github.com/niway-dev/kaipu-bench-wachi-v3). Each job runs one
  `claude -p` call on the diff of kaipu-record #465 (14 files), in a clean environment and a
  fresh profile, with exactly one credential: `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`.
  Same prompt, Claude Code 2.1.304, `claude-opus-5-5`, effort `high`, 40 turns, read-only tools
  (Read, Grep, Glob). Three calls per credential, at two caps on `--max-budget-usd`.
- **Runs:** [$3 cap](https://github.com/niway-dev/kaipu-bench-wachi-v3/actions/runs/45770878853)
  and [$0.75 cap](https://github.com/niway-dev/kaipu-bench-wachi-v3/actions/runs/45771412660),
  Wachiman's batch cap. Each call's `init` and `result` records (the review text removed) and its
  summary are in [`results/`](results/).

## Result

**At Wachiman's $0.75 cap, the gap reproduces without Wachiman: 15, 17 and 15 turns on the key,
10, 12 and 12 on the token.** At $3 the two ranges overlap.

| Cap | Credential | Turns | Output tokens | Seconds | Cost |
| --- | --- | --- | --- | --- | --- |
| $0.75 | API key | 15 / 17 / 15 | 8,605 / 8,328 / 8,122 | 85 / 82 / 79 | $0.61 / $0.60 / $0.60 |
| $0.75 | Subscription token | 10 / 12 / 12 | 6,458 / 6,582 / 7,034 | 75 / 74 / 84 | $0.65 / $0.69 / $0.67 (estimate) |
| $3 | API key | 38 / 27 / 28 | 17,156 / 12,910 / 12,036 | 176 / 131 / 125 | $1.31 / $0.93 / $0.96 |
| $3 | Subscription token | 20 / 26 / 28 | 10,002 / 11,154 / 14,900 | 128 / 144 / 185 | $1.10 / $1.27 / $1.28 (estimate) |

- **Every call ended on its own** (`stop_reason` `end_turn`, `subtype` `success`). None reached the
  turn limit or its cap: the highest cost at $0.75 is $0.69.
- **The token writes the prompt cache for 1 hour, the key for 5 minutes, in all 12 calls.**
  `usage.cache_creation` holds only `ephemeral_1h_input_tokens` on the token and only
  `ephemeral_5m_input_tokens` on the key. A 1-hour cache write is priced higher, so Claude Code's
  cost per turn is higher on the token: about $0.060 against $0.038 at $0.75, $0.049 against $0.035
  at $3. On the token that figure is an API-price estimate, not a bill.
- **The cap shapes depth on the key too.** The same call makes 27 to 38 turns at $3 and 15 to 17 at
  $0.75, and writes about 40% fewer output tokens (14,034 against 8,352 on average). Wachiman's
  batches run at $0.75.

## What it means, and what it does not show

- **Measured:** with the same Claude Code version, call and cap, a call on the token makes fewer
  turns than on the key at $0.75, and its prompt cache is written with a different lifetime.
- **Not measured: why the call stops earlier.** No call reached its cap, so Claude Code did not
  cut it. One explanation fits both caps: the model is told its budget and wraps up as the spend
  nears it, and a higher cost per turn makes the token get there in fewer turns. Nothing in the
  stream shows a budget notice, and Claude Code 2.1.304 ships as a native binary, so this was not
  checked. The test that would: the same calls with no `--max-budget-usd`. If the gap goes away,
  the cap is how the credential reaches the turns.
- **No documentation found.** Anthropic's docs and the claude-code issues searched on 2026-11-26
  describe no difference in behaviour between the two credentials.

## Limits

- **One pull request, three calls per credential and cap.** Enough for a 15-against-11 gap with no
  overlap at $0.75, not to size it.
- **The review text was not compared.** Only counts were recorded; which bugs each call found is
  not in this report.
- **Thinking text is almost empty in the stream:** 0 characters in 10 calls, about 220 in the other
  two. The thinking token counts are the only usable record of it.
- **One call tried Bash once.** The first key call at $3 (38 turns) called `Bash` with `echo`;
  Claude Code refused it ("No such tool available"), which cost that call one turn. Without it,
  the key's range at $3 would still be 27 to 37.
