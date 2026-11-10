# v1.10.0: predictions

- **Registered:** 2026-11-09, before the release PR
  ([wachiman#150](https://github.com/niway-dev/wachiman/pull/150)) merged. #150 replaced #143,
  which went stale when the package was renamed from `agent-review` to `wachiman`.
- **Previous version:** v1.9.0. **Changes:**
  [v1.9.0...v1.10.0](https://github.com/niway-dev/wachiman/compare/v1.9.0...v1.10.0) (breaking
  change: Haiku 5.5 high is the default reviewer and the verifier is on by default; plus the
  verifier, result format `/2`, accounts, `setup`/`doctor`/`init`, skills install, and the npm
  launcher).
- **Rolled out to:** niway-dev/kaipu-record. The pin moves from `@v1.8.0` to `@v1.10.0` (it skipped
  v1.9.0, whose changes are local-mode only). The caller sets `model: claude-opus-5-5`, so the
  **reviewer stays Opus 5.5**. Triggers are `pull_request` (opened, ready_for_review, synchronize)
  and `issue_comment`. There is no `pull_request_review_comment`, so thread-reply runs do not run
  there. The verifier is not set in the caller, so it takes the new default: **on, Opus 5.5, high**.
- **Evaluation point:** after 5 kaipu-record pull requests reviewed on v1.10.x, or on 2026-11-23,
  whichever comes first. The result goes in `RESULTS.md` next to this file. Patch releases
  (v1.10.1 and later) are scored under this file; a patch that changes the engine gets a dated
  amendment, not a new baseline.

## In one minute

On kaipu-record, the visible change is the **verifier**: a second Opus call that tries to refute
every finding before it is posted. It should remove wrong findings without removing a real bug, at
a modest extra cost per review. **The number that matters most is real bugs lost to the verifier:
zero.** The Haiku default, the CLI, accounts and the npm launcher do not run on kaipu-record. This
release does not change what the batches find, so recall on data-path PRs should stay where it is.

## Predictions, one per change

| # | Change (commit or PR) | What it should improve | Metric | Baseline (source) | Predicted | Where to read it | Falsified if |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Verifier on by default (#139, ADR 0027) | No real bug dropped | Real Medium+ bugs among findings the verifier refuted, audited | none measured; the spec's gate allows High+Critical to fall by up to 3 of 66 on Martian | **0** of the audited refuted findings is a real bug | `verification` block of the result JSON and the footer's dropped count, audited by reading the code | any refuted finding is a real bug |
| P2 | Same | Fewer wrong findings posted | Share of posted findings that are invalid or partly valid, audited | 6 partly valid, 0 invalid of 76 (field run, [README](../../2026-11-02-field/README.md)); on Martian, 174 findings for 38.7 % precision (v1.9.0, [history](../../martian/history.md)) | Invalid ≤ 1 in 20, partly valid ≤ 6 % (down from 8 %). The verifier drops ≤ 25 % of candidates | Same audit, plus the dropped count over candidates | invalid > 1 in 20, or the verifier drops > 40 % of candidates (it is then refuting findings rather than checking them) |
| P3 | Same | Cost of the extra call | Verifier cost per review that had candidates | Spec estimate: about $7 per 50 PRs, about $0.14 per PR, against $0.48 median per PR (Martian v1.9.0, Opus 5.5) | Median **$0.10–0.30**; p90 ≤ $0.60 | "verified by Opus 5.5 … $x" footer line and `cost_usd` in the review job log | median > $0.40, or a PR above the $6 automatic ceiling |
| P4 | Same | The review is never blocked | Reviews whose verification failed or was partial | none (new) | ≤ 1 in 10 reviews, and each says so in its footer | Footer line "the verification did not run" | a review is missing or delayed because of the verifier, or a failure is not stated |
| P5 | Verifier reserve of $1 out of the $3 `budget_usd`, capped at half (#139) | The batches keep enough money | Reviews that end partial | 0 partial reviews, Martian v1.9.0; no count for kaipu-record | ≤ 1 in 10 reviews partial. A PR under about 1,500 changed lines is never partial | "partial" notice in the review body | a PR under about 1,500 lines ends partial |
| P6 | Result format `/2`, tier words, Pre-existing and Inconclusive sections, verification lines (#142, #139) | The reader sees what was checked and whether the PR introduced it | Review bodies that carry a verification line when candidates existed; review bodies over the GitHub size limit | none (new) | 100 % carry the line. 0 over the limit | The posted review bodies | a review with candidates has no line, or a body is rejected for size |
| P7 | Haiku 5.5 high as the default reviewer (#139, breaking) | — | — | — | **Does not run on kaipu-record**: the caller pins `claude-opus-5-5`. The Haiku default is judged on Martian arm 2, not here | — | — |
| P8 | `setup`, `doctor`, `init`, profiles, skills install, npm launcher, `local` flags | — | — | — | **Do not run on kaipu-record**: they belong to the CLI, not to the reusable workflow | — | — |
| P9 | Thread-reply runs | — | — | — | **Do not run**: no `pull_request_review_comment` trigger. Adding one is the owner's separate decision | — | — |

## Known not fixed

| Problem | Current number (source) | Expected in this release |
| --- | --- | --- |
| Precision on the Martian bench | 38.7 % precision, F1 48.1 (v1.9.0, Opus 5.5) | not measured on this bench; arm 2 is the unfinished acceptance box of the verifier spec |
| Recall on data-path PRs | 4 of 14 Medium+ bugs in the field run; no RESULTS for v1.5.0 yet | unchanged ± 15 points. The verifier removes findings; it never adds one |
| Share of cost spent on re-reviews | 49 %, field run (older versions) | unchanged. The verifier also runs on every push re-review, so a re-review costs a little more |
| Cost measured for the Haiku reviewer | none | not measured here; kaipu keeps Opus |

## Risks to watch, and when to roll back

| Risk | Signal | Roll back the pin if |
| --- | --- | --- |
| The verifier refutes a real bug | A refuted finding that later proves real (a bug found by another bot, the owner or production) | one real bug is dropped. Set `verify: false` first, then judge whether the pin must move |
| The verifier adds cost on top of Opus | Median verifier cost above $0.40 | the PR median is more than 50 % above its v1.8.0 level |
| A second call hits rate limits | "Not reviewed" or "verification did not run" notices | more than 1 in 5 reviews carries one of them |
| The default was never gated: Martian arm 2 has not run | Arm 2, when it runs, shows false positives down by less than 30 % or High+Critical down by more than 3 | the arm fails its gate: `verify: false` in the caller and an amendment here |

## How the results will be scored

- **Audit.** Read the code behind every finding refuted by the verifier (P1) and a sample of
  20 posted findings, or all if fewer (P2), and mark each valid, partly valid or invalid. The owner
  or a fresh-context reviewer judges the verdicts from the code, not from the review text.
- **Cost, partial reviews, footers.** Read from the review job logs and the posted review bodies of
  the evaluated pull requests (P3 to P6). Take the v1.8.0 PR median from the same repository's
  earlier runs.
- **Not measurable on kaipu-record:** P7 to P9; marked so in `RESULTS.md`.
- **Martian arm 2** is a separate run in `martian/`; its row is cited in `RESULTS.md` but does not
  replace the kaipu-record numbers.

## Amendments

None yet. Dated corrections only; never edit the tables above after the release.
