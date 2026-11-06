# Haiku high against Opus high, local mode, one replay PR (2026-11-06)

Status: **pilot, one run per arm on one PR.** A first look, not a result. It shows the method works
on the subscription; it says nothing yet about which model is better.

## Setup

- Engine: Wachiman v1.8.0 (`983cd0a`), `agent-review local`, unchanged. Only the model differs.
- Case: `kaipu-bench-wachi` replay of kaipu-record #184 (`replay/pr-184/base` → `replay/pr-184/head`,
  head `2c33d5b`), 7 files, +238/-24, one batch.
- Auth: the owner's claude.ai login (`subscriptionType: max`), no `ANTHROPIC_API_KEY`. Costs below
  are Claude Code's API-equivalent estimates, not money spent.
- Answer key: the four bugs `kaipu-record-bug-catalogue.md` attributes to #184.

## Cost and work

| Arm | Turns | Wall time | Output tokens | Cache read | Cache write | Estimate |
| --- | --- | --- | --- | --- | --- | --- |
| Haiku 5.5, effort high | 18 | 151 s | 32.9k | 384k | 96.9k | $0.04 |
| Opus 5.5, effort high | 9 | 51 s | 5.3k | 103k | 45.1k | $0.49 |

## Recall on the answer key

| Catalogued bug | Difficulty note from the catalogue | Haiku high | Opus high |
| --- | --- | --- | --- |
| `video-label-hit-box-ignores-multiline` | hit-test code outside the diff | found (Fix) | found (Fix) |
| `video-label-reopen-shows-one-line` | visible against the sibling editor | found (Fix) | found (Fix) |
| `video-label-drawn-twice-under-editor` | visible against the sibling editor | partial: named inside another finding | found (Consider, own finding) |
| `video-label-double-click-edit-broken-by-pointer-capture` | faulty line in unmodified code | missed | missed |

## Findings outside the answer key (not audited)

| Finding | Haiku high | Opus high |
| --- | --- | --- |
| Re-edit uses the toolbar's size and colour, not the label's | Fix | Fix |
| Clearing a label while re-editing reverts it instead of removing it | Consider | — |
| Double-clicking inside the open editor can retarget the edit | Consider (medium) | — |
| No test for multi-line hit-test or reopen | Consider | Consider |

## What this does and does not show

- Both arms found the same two clear bugs and missed the same hard one. Opus reported the
  drawn-twice bug on its own; Haiku only mentioned it.
- Haiku cost about a twelfth of Opus here, while taking twice the turns and three times the time.
- One run per arm: a model does not give the same review twice (see the plan in PR #9), so a
  one-bug difference is within noise. The two extra Haiku findings are unverified.

Raw reports: [`raw/`](raw/).
