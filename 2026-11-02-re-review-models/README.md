# Re-review cost, part 2: cheaper models, lower effort, a compact prompt (2026-11-02)

Follow-up to [`2026-11-02-re-review-cost`](../2026-11-02-re-review-cost/README.md). Same six rebuilt
re-reviews (kaipu-record #478 ×2, #479, #482, #483, #484), same v1.5.0 engine and harness, same
audited answer key (5 findings, all Low). Only the model, the effort and the shared prompt wording
changed. **Reported spend: $7.55 of the $8 cap** ($7.539 for 48 traced review calls, $0.011 for
the token counts).

## One-minute summary

**Haiku 5.5 at effort high is the only arm that looks like a safe way to cut re-review cost.**
It cost **$0.07 per re-review** (Opus: $0.50), found **5 and 4 of the 5 audited findings** (Opus:
4 and 3), and answered every thread the Opus baselines answered. Sonnet 5.5 is 55 % cheaper than
Opus but found fewer findings and skipped a third of the thread replies; at effort medium it
found none. The compact prompt saved 3 % of the prompt and nothing measurable in cost.

| Arm (2 runs each, six re-reviews) | Cost per re-review | vs Opus | Audited findings found, run 1 / run 2 | Union of 2 runs | Other findings valid / invalid | Needed thread replies missing |
| --- | --- | --- | --- | --- | --- | --- |
| Opus 5.5 high (previous study) | $0.50 | — | 4 / 3 | 5 of 5 | not audited here | 0 of 19 |
| **Sonnet 5.5 high** | $0.22 | −56 % | 2 / 3 | 3 of 5 | 7 / 0 | 6.5 of 19 per run |
| **Sonnet 5.5 medium** | $0.12 | −75 % | 0 / 0 | 0 of 5 | 1 / 0 | 6 of 19 per run |
| **Haiku 5.5 high** | $0.07 | −86 % | 5 / 4 | 5 of 5 | 21 / 2 | 0 of 19 |
| **Compact prompt, Sonnet 5.5 high** | $0.21 | −57 % (−3 % vs Sonnet) | 3 / 1 | 3 of 5 | 6 / 0 | 5.5 of 19 per run |

- **Cost is far outside the baseline's noise** for the three model/effort arms: every case is at
  least 51 % cheaper than the Opus mean, and the Opus runs differ by up to 25 % per case. The
  compact prompt against plain Sonnet high (−3 % in total, −22 % to +7 % per case) **is inside
  the noise**.
- **Findings are mostly inside the noise too, except medium.** Sonnet high (2 / 3) overlaps
  Opus (4 / 3) and the compact arm (3 / 1) overlaps Sonnet high; with two runs and five findings
  one run swings by 1–2. Medium (0 / 0) and Haiku's lead are the only differences beyond that.
- **Thread replies are where Sonnet clearly loses.** On threads whose file the push changed and
  that both Opus runs answered, the Sonnet arms left 5.5–6.5 of 19 unanswered per run (one run
  of #479 answered 1 of 4). Haiku left none.
- **Recommendation.** Use **Haiku 5.5, effort high, the current prompt** for incremental
  re-reviews, behind a setting, and check it on the next ~20 field re-reviews before making it
  the default (limits below: 12 Haiku runs, only Low findings, and the one real Medium bug of the
  field run was not in the set). Do not use Sonnet at either effort: the saving is real, but it
  loses findings and replies. Do not ship the compact prompt: it cannot pay for itself, because
  the sections it can shorten are 23 % of #483's prompt and shrank by 12 %.

## What was run

| Arm | Model | Effort | Engine | Runs |
| --- | --- | --- | --- | --- |
| S-high | `claude-sonnet-5-5` | high | v1.5.0 | 2 per case |
| S-medium | `claude-sonnet-5-5` | medium | v1.5.0 | 2 per case |
| H-high | `claude-haiku-5-5` | high | v1.5.0 | 2 per case |
| C-S-high | `claude-sonnet-5-5` | high | v1.5.0 + [compact prompt](harness/compact-prompt.patch) | 2 per case |

Everything else is the previous baseline's: production limits (batch budget $0.75, 40 turns,
900 s), writes refused, the engine's own `review()` with a full tool trace. 48 runs, 48 traced
calls (each case is one batch). Engine `dce32d9` is v1.5.0 plus one docs-only merge (#97); the
tool code is identical.

**Order.** The arm order was shuffled per case with a fixed seed
([`harness/order.tsv`](harness/order.tsv), [`order-round2.tsv`](harness/order-round2.tsv)). Round 2
(the second run of S-high, S-medium and H-high) was stopped early by its own spend guard
(`STOP_AT=5.6`) and finished by hand for the five missing runs, and the second compact run was
added last, in fixed case order. Prompt caching did not leak between runs: every run's first
request read only the shared system prefix (4,982 tokens, 5,785 on Haiku) from cache and wrote the
rest.

## Arm 4: the compact prompt

[`harness/compact-prompt.patch`](harness/compact-prompt.patch) rewrites `RULES`,
`FLOW_QUESTIONS` and the static framing in `buildBatchPrompt` (part, file lists, the
"review every file" paragraph, the threads paragraph). It keeps every severity test, confidence
level, topic, evidence rule and all six flow questions, and every phrase the engine's tests pin.
The engine's suite passes except the one test that compares the prompt byte for byte with the old
one (517 pass, 1 fail by design). `EVIDENCE_PARAGRAPH` and the data-path questions were out of
the stated scope and are unchanged.

| | Before | After | Change |
| --- | --- | --- | --- |
| `RULES` | 4,039 chars | 3,373 | −16 % |
| `FLOW_QUESTIONS` | 2,195 | 2,106 | −4 % |
| Static framing | — | — | −78 chars |
| The three sections together | 6,236 | 5,482 | −12 % (−754 chars) |
| Sections, tokens | 1,956 | 1,745 | −211 tokens (−11 %) |
| Whole prompt of #483 (re-review of a 5-line push) | 26,717 | 25,884 | −833 chars (−3.1 %) |
| Whole prompt, tokens | 9,638 | 9,408 | −230 tokens (−2.4 %) |
| Whole prompt of #478 `64db30b` | 63,320 | 62,487 | −1.3 % |
| Consumer instructions (`CLAUDE.md` 13,046 + `.github/agent-review.md` 1,546 + wrapper), not touched | 15,201 | 15,201 | 57 % of #483's prompt |

Tokens were counted with one Haiku 5.5 call per text and the input-token total minus a control
call ([`raw/token-counts/`](raw/token-counts/)); characters per token come out at about 2.8–3.2.
The original text is already dense, so a rewrite that keeps every check cannot cut much more:
the sections are 23 % of the smallest re-review prompt, and what remains is the repository's
instructions and the diff. The cost effect is below what one run can show: 3 % of an input that
is 29 % of the cost.

## Results

Full tables: [`tables.md`](tables.md). Per-run metrics: [`raw/metrics.tsv`](raw/metrics.tsv).
Every finding with its verdict: [`raw/audit.tsv`](raw/audit.tsv).

### Cost, turns, requests (six cases, per run)

| Run | Cost | Turns | Requests | Findings | Thread replies |
| --- | --- | --- | --- | --- | --- |
| Opus 1 / 2 | $2.99 / $2.97 | 67 / 70 | 33 / 39 | 6 / 6 | 32 / 27 |
| S-high 1 / 2 | $1.32 / $1.33 | 68 / 69 | 31 / 30 | 4 / 8 | 25 / 10 |
| S-medium 1 / 2 | $0.73 / $0.77 | 32 / 34 | 16 / 17 | 1 / 0 | 14 / 32 |
| H-high 1 / 2 | $0.46 / $0.37 | 114 / 91 | 50 / 40 | 18 / 14 | 20 / 20 |
| C-S-high 1 / 2 | $1.34 / $1.22 | 66 / 66 | 32 / 30 | 6 / 4 | 26 / 20 |

Haiku makes about 1.5 times the tool calls (it reads in many small steps), and still costs the least.
Its reported cost is not proportional to its tokens: on #479 the same prompt cost $0.148 (48.8k
output tokens) and $0.032 (24.9k), and #483's two runs both cost $0.03. Treat its per-case cost
as a range, $0.01–$0.17.

### The five audited findings

✓ = found (matched by mechanism), — = missed. No run found one *partly*; the field audit's
"partly valid" F17 counts as found when its mechanism is.

| Id | Case | Opus 1 / 2 | S-high | S-medium | H-high | C-S-high |
| --- | --- | --- | --- | --- | --- | --- |
| F18 | 478-64db30b | ✓ / — | — / — | — / — | ✓ / — | ✓ / — |
| F20 | 478-392778f | ✓ / — | ✓ / ✓ | — / — | ✓ / ✓ | ✓ / — |
| F21 | 478-392778f | — / ✓ | — / — | — / — | ✓ / ✓ | — / — |
| F17 | 483-0253fd7 | ✓ / ✓ | ✓ / ✓ | — / — | ✓ / ✓ | ✓ / ✓ |
| F2 | 484-59f6d48 | ✓ / ✓ | — / ✓ | — / — | ✓ / ✓ | — / — |
| **Found** | | **4 / 3** | **2 / 3** | **0 / 0** | **5 / 4** | **3 / 1** |

Quotes of the matching findings:

- **F18** (H-high): "Picking the folder a workspace already has reports that it 'now points to the new folder'".
- **F20** (S-high): "Nothing tests that `unchanged` reaches the renderer and suppresses the toast".
- **F21** (H-high, both runs): "An offline rename of a pending workspace is silently dropped when
  its folder later carries another id" and "An offline rename of a never-initialized workspace is
  silently replaced when its folder returns with another identity". Haiku named the adoption
  branch, `registry.ts:724`, which is the audited mechanism, and the fix (skip adoption while
  `pendingIdentity` is set).
- **F17** (S-high): "Relocating the active workspace detects the new folder's provider after the
  commit, so the first re-list treats an xattr-only Drive folder as plain". The ordering bug that
  the "no flow questions" lever lost in the previous study was found by every arm except
  Sonnet medium.
- **F2** (S-high run 2): "Double-clicking a name to select it still toggles the row once".

Sonnet medium's one finding on these cases, "Relocating out of an unverified synced folder leaves
the id in `unverified`" (#483), is a different, valid bug; it does not match F17.

### The other findings (checked against the code)

Each finding that is not one of the five was checked by reading the code at the push's head
([`raw/audit.tsv`](raw/audit.tsv) gives the reason for each). Reading only, nothing run.

| Arm (both runs) | Findings | Audited five | Other valid | Other invalid |
| --- | --- | --- | --- | --- |
| S-high | 12 | 5 | 7 | 0 |
| S-medium | 1 | 0 | 1 | 0 |
| H-high | 32 | 9 | 21 | 2 |
| C-S-high | 10 | 4 | 6 | 0 |

- **The only invalid finding** is Haiku's `registry.ts:848` question ("is it intended that a pending
  workspace takes any identity-less folder with Kaipu items?"), in both its runs on #478
  `64db30b`. The code comment at that branch already gives the reason.
- **Valid does not mean worth posting.** Seven of Haiku's run-1 findings are on #479, mostly
  stale lines in two docs (a table row that ends mid-sentence, a status banner, a list missing
  `io`). They are true and Low. Haiku posts 2–3 times as many findings as Opus (32 over two
  runs against 12), so an author gets more to read. It also found the new relocation-does-not-refresh-
  settings gap on #482 (`index.ts:406`, `:608`), which no Opus run reported; it is real, and Low.
- Findings the previous study left unaudited and that recur here (#479's missing `moving`
  test and stale docs; #478's `registry.ts:684` deferred colour upgrade) were checked: valid.

### Thread replies

A reply is "needed" when the thread's file is in the push's delta and both Opus runs answered it
(19 threads over the six cases). Presence only; the wording was not graded.

| Arm | Replies per run | Replies on delta files | Needed replies missing, per run |
| --- | --- | --- | --- |
| Opus | 29.5 | 19.5 | 0 |
| S-high | 17.5 | 12.5 | 6.5 of 19 |
| S-medium | 23 | 13 | 6 of 19 |
| H-high | 20 | 20 | 0 of 19 |
| C-S-high | 23 | 14 | 5.5 of 19 |

Sonnet's gaps are erratic, not systematic: #479 got 12 replies from some runs and 1 or 2 from
others, and #478 `392778f` got 1–5 of 6. Unanswered threads stay "open" with no status on the
pull request. Sonnet arms sometimes answer threads on files the push did not touch (#479, 12
replies), which is the repetition the previous study's lever T removes.

## Is each arm inside the Opus baseline's noise?

Opus's two runs match in total ($2.99, $2.97) but differ by up to 25 % in one case (#482: $0.48,
$0.36). Per case, against the Opus mean:

- **S-high**: 51–63 % cheaper in all six cases. **Outside the noise** (cost). Findings 2 / 3
  against 4 / 3: inside it. Thread replies: outside it.
- **S-medium**: 73–79 % cheaper. **Outside.** Findings (0 / 0 against 4 / 3): outside it.
- **H-high**: 75–95 % cheaper. **Outside**. Findings 5 / 4: at or above the baseline's.
- **C-S-high** against S-high: −3 % in total, between −22 % and +7 % per case. **Inside the
  noise**; findings 3 / 1 against 2 / 3 are inside it as well.

## Limits

- **Two runs per arm, five findings, all Low.** One run swings by 1–2 findings; Haiku's 5 / 4
  and Sonnet's 2 / 3 are a signal, not a measurement. The field run's one real Medium bug (#478
  `c573b8e`, `pendingInit`, two batches) was not rebuilt here, so nothing shows whether Haiku
  catches the kind of bug that matters most.
- **Re-reviews only.** First reviews of a pull request were not tested.
- **Haiku's cost spread** is wide and not explained by token counts (above). Its savings are
  large enough that the spread does not change the conclusion.
- **Validity is by reading**, mine, and generous toward Haiku's documentation findings. It is not
  an author's verdict on whether they would fix them.
- **Local, not CI**, as before: Claude Code 2.1.316 on the owner's login, the harness's USER
  wrapper, the kaipu-record state rebuilt from a local copy of the clone (`git clone --local`
  plus the original's `origin/*` refs, so the original was not touched).
- The previous study's Opus runs are reused as the baseline, not re-run; they date from the same
  day, with the same harness.

## Reproduce

```sh
# Engines: v1.5.0-equivalent and the compact variant (the patch applies to it)
git -C wachiman worktree add --detach /tmp/rrc2/engine-base dce32d9
git -C wachiman worktree add --detach /tmp/rrc2/engine-compact dce32d9 && git -C /tmp/rrc2/engine-compact apply <path>/harness/compact-prompt.patch
# kaipu-record: local clone plus one detached worktree per head under /tmp/rrc2/heads/kaipu-<sha7>
cd harness
./run-case.sh 483-0253fd7 H-high            # arms are defined in arms.sh; writes ../raw/runs/<case>/<arm>/
./spent.sh                                  # reported cost of every traced call (the cap is tracked from this)
python3 metrics.py ../raw/runs > ../raw/metrics.tsv
python3 audit.py                            # raw/audit.tsv (verdicts are in the script)
python3 replies.py > ../raw/replies.tsv
```

`raw/runs/<case>/<arm>/` holds each call's trace (`call-N.jsonl`; the init event's lists of local
skills, plugins and agents are emptied), argv, prompt, the provider's result with the structured
review, the engine log and its info. `raw/driver.log` is the run log. The harness is the
previous study's, unchanged ([`../2026-11-02-re-review-cost/harness`](../2026-11-02-re-review-cost/harness)).
