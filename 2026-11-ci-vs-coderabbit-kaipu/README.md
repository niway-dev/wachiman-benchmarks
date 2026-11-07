# Live Wachiman CI vs CodeRabbit on kaipu-record PRs, 2026-11-06

Status: **draft, hand-labelled, one day of data.** Nothing here is a benchmark result yet. It is the
ledger a later study can extend, plus a first read of the gaps.

Companion to the [field run with Haiku and verifiers](../2026-11-field-kaipu/README.md) (draft #11):
that one reruns Wachiman locally on cheaper models; this one reads what the **live CI review**
(Claude Opus 5.5, high effort; **v1.7.0** on #534 and #535, v1.8.0 from #536 on, per the workflow runs: the review footer does not show the version) and **CodeRabbit** actually posted on the same PRs,
and builds ground truth by hand.

## Read this first (one minute)

- **Scope.** Seven kaipu-record PRs, #534 to #540, all opened on 2026-11-06 UTC (`niway-dev/kaipu-record`,
  public). Wachiman CI posted 19 distinct findings; CodeRabbit posted 4.
- **Rule for scoring.** A finding counts toward a comparison only when it can be tied to a defect we
  verified. Findings only one tool made and nobody verified are listed but **not scored**.
- **Verified defects: 2.** (1) #534: Space on a focused checkbox toggles playback instead of the
  checkbox. (2) #535: the "kill switch" for native capture cannot reach installs with *Send diagnostics*
  off. CodeRabbit found both; Wachiman CI found the second (as a docs note) and, on #534, **never ran**
  because the Anthropic account had no credit (3 runs, 00:36 to 00:54 UTC).
- **Rerun closes the #534 gap.** Wachiman run locally on the same commit found the checkbox bug as
  🟠 Fix · bug, on the same line CodeRabbit used (see [L1](#ledger)). So **no confirmed quality miss by
  Wachiman today**; the one open candidate is C3 below, and it is unverified.
- **Confound.** The #534 rerun used Sonnet 5.5 on v1.8.0 ($0.20), not the CI's Opus 5.5 on v1.7.0. It shows a cheaper model
  finds it; it does not reproduce the CI run.

## Correction (2026-11-06, later)

The first version of this page said every CI review ran v1.8.0. The workflow runs say v1.7.0 for #534 and #535; the bump to v1.8.0 (#536) merged at 02:01 UTC. `scripts/pair.ts` (PR #13) reads the version from the run, which is how the mistake was found.

## Method

1. Listed PRs opened 2026-11-06 UTC. `github-actions[bot]` is Wachiman; `coderabbitai[bot]` is CodeRabbit.
2. Pulled every inline comment, review body and issue comment of both bots with the GitHub API.
   Wachiman's "outside the diff" items live in the review body; CodeRabbit's nitpicks do too.
3. De-duplicated the same finding repeated across pushes of one PR.
4. Verified each candidate we could against the code at the reviewed commit (`git show <sha>:<path>`);
   the owner's in-thread replies ("Fixed in <sha>") count as owner acceptance, a weaker signal.
5. For #534, ran `wachiman local --commit ef8e681 --profile isolated:personal` (one commit, 2 files).

Ground truth column values: **verified** (we read the code), **owner-accepted** (fixed in the PR after the
finding), **answered** (the question has a checkable answer), **unverified**.

## Ledger

Ids: `C` = CodeRabbit, `W` = Wachiman CI, `L` = Wachiman local rerun. Wachiman labels are
severity · topic ([label set](https://github.com/niway-dev/wachiman/blob/v1.8.0/docs/reviews.md)); CodeRabbit
labels are as posted.

| id | PR | what | label | ground truth | matched by the other tool |
| --- | --- | --- | --- | --- | --- |
| C1 | #534 | Space on a focused checkbox now toggles playback (`video-editor-page.tsx:288`) | Major · Functional Correctness | **verified**, owner-accepted (fixed in `42d19bb`) | W: not run (no credit). L1: yes |
| C2 | #535 | Kill switch cannot reach installs with diagnostics off (`analytics.ts:26`) | Major · Functional Correctness | **verified** | W1: yes, but as docs |
| C3 | #535 | Flag is read once, synchronously, at take start; nothing refreshes it first (`analytics.ts:26`) | Major · Functional Correctness · Heavy lift | unverified | no |
| C4 | #539 | Slider test should assert `cancelAnimationFrame` is called (`history-slider.test.tsx:8`) | Trivial · Low value | unverified (taste) | no |
| W1 | #535 | Runbook says the 0% kill switch reaches every build; it does not with diagnostics off (`analytics-and-flags.mdx:69`) | 🟡 Consider · docs, high | **verified** (same root as C2) | C2: yes, rated Major |
| W2 | #535 | `FLAG_DEFAULTS` docstring still says "experiments stay off" while the default is now `true` (`analytics.ts:19`, outside diff) | 🟡 Consider · docs, high | **verified** | no |
| W3 | #537 | Docs still name `agent-review.yml` and `/wachi review` (`wachiman-review.yml:1`) | 🟡 Consider · docs, high | **verified** (`ci-cd-pipelines.md:193-194` at `680c6c7`) | no |
| W4 | #537 | Does v1.8.0 accept `/wachiman review`? (`wachiman-review.yml:6`) | 🟡 Consider · question, low | **answered**: yes, `MENTION_ALIASES` in `src/engine.ts` and `parseCommand` test in `src/engine.test.ts:83` at v1.8.0 | no |
| W5 | #538 | Title button gives no accessible hint that it renames (`recording-title.tsx:52`) | 🟡 Consider · bug, high | unverified | no |
| W6 | #538 | No test clicks the title to rename (`recording-title.tsx:52`) | 🟡 Consider · tests, high | unverified | no |
| W7 | #538 | Backlog doc still describes a "Send to…" button (`prepare-screen.md:119`, outside diff) | note | unverified | no |
| W8 | #539 | Comment says every controller callback is stable; `undo`/`redo` are not (`use-video-scene.ts:106`) | 🟡 Consider · docs, high | owner-accepted (`012efef`); Wachiman re-confirmed twice | no |
| W9 | #540 | Spec's background ranges are not the screenshot editor's | 🟡 Consider · docs, high | owner-accepted (`98c09f94`) | no (CodeRabbit skipped: `.md`/`.mdx` path filter) |
| W10 | #540 | `bg = none` with padding/radius/shadow undefined: preview and export disagree | 🟡 Consider · docs, high | owner-accepted (`deb0ba3e`) | no (same) |
| W11 | #540 | Acceptance criterion `Tracks 5/5` contradicts the count rule | 🟡 Consider · docs, high | owner-accepted (`c5300fc7`) | no (same) |
| W12 | #540 | "Parser drops `activity` without `zooms`" would forget a valid choice | 🟡 Consider · docs, medium | owner-accepted (`82670484`) | no (same) |
| W13 | #540 | `availableLanes` vs `availableTracks` with two signatures | 🟡 Consider · docs, high | owner-accepted (`4459f719`) | no (same) |
| W14 | #540 | Plan location given as `docs/plans/`, against the repo rule | 🟡 Consider · rules, high | owner-accepted (`970004e4`) | no (same) |
| W15 | #540 | Decision 7 (new lanes hidden by default) cannot work with a stored list of hidden keys | 🟡 Consider · docs, high | unverified | no (same) |
| W16 | #540 | ADR 0048's Amends row omits that it also amends 0040's "Camera lane cannot be removed" | 🟡 Consider · adr, high | unverified | no (same) |
| W17 | #540 | `BeautifyPanel` cannot be reused as-is for the video background | 🟡 Consider · docs, high | unverified | no (same) |
| W18 | #540 | `BACKGROUNDS[bg]` indexes an array by id; `backgroundCss(bg)` is the lookup | 🟡 Consider · docs, high | unverified | no (same) |
| W19 | #540 | Settings store drops unknown keys; `exportQuality` can be overridden per workspace | 🟡 Consider · docs, medium | unverified | no (same) |
| L1 | #534 | Space and letter shortcuts now fire from focused checkboxes and radios (`video-editor-page.tsx:288`) | 🟠 Fix · bug | **verified** (same defect as C1) | C1: yes |
| L2 | #534 | Original doc comment left stranded above the new constant (`:265`) | 🟡 Consider · cleanup | **verified** (visible in the diff) | no |
| L3 | #534 | Inline mute removal; `mutes` in the effect deps re-subscribes the listener each render (`:1356`) | 🟡 Consider · cleanup | unverified | no |
| L4 | #534 | Mute test title does not match its action; no coverage for the narrowed `isEditingTarget` (`.test.tsx:786`) | 🟡 Consider · tests | unverified | no |

Not findings: #536 got 0 from both tools. #540: CodeRabbit posted "Review skipped" (path filters exclude
`*.md` and `*.mdx`), so all 11 Wachiman findings there are Wachiman-only by construction.

### Cost

Wachiman CI, as posted per review: #535 $0.51, #536 $0.08, #537 $0.16, #538 $0.34, #539 $0.54 + $0.12 + $0.11
(two incremental re-reviews), #540 $0.46 + $0.50. Sum **$2.82** for 9 completed reviews, plus 3 empty runs on
#534. The local rerun on #534 was $0.20 (Sonnet 5.5). CodeRabbit's cost is not visible to us.

## Gap analysis: what CodeRabbit found that Wachiman did not

Per the scoring rule, only findings with a path to ground truth are analysed. C4 is a taste nit and is not.

### C1, Space on a focused checkbox (#534) — not a Wachiman miss

- **What happens.** The fix lets Delete work while the Level slider holds focus, by narrowing
  `isEditingTarget` to text-like inputs. That also frees checkboxes, so Space (handler at `:1303`, unchanged,
  1,000 lines below the hunk) calls `preventDefault` and toggles playback. Keyboard users can no longer
  toggle the cursor or webcam checkboxes.
- **Why CodeRabbit found it.** Its comment cites a file outside the diff
  (`cursor-inspector.tsx`, which contains a checkbox): it looked for consumers of the narrowed function.
- **Why Wachiman CI did not.** It did not run. Locally, a cheaper model found it (L1) and rated it Fix.
- **Severity (ours): medium.** No data loss; an accessibility regression introduced by the fix itself. Owner
  confirmed and fixed it in the PR.
- **Difficulty to find in our own review: 3 of 5.** The function's own docstring, in the diff's context lines, names Space as a
  key the guard protects, and the handler is in the same file. A reader who asks "which keys does
  this guard protect?" gets there; one who reads only the diff does not.

### C3, flag read once and never refreshed (#535) — the only open candidate

- **Claim.** `recorder-engine.ts` reads the flag with `isFlagEnabled` once, at the start of each take;
  nothing in the app calls `reloadFeatureFlags` or similar, so a kill switch set remotely may not apply until
  PostHog reloads on its own.
- **Why CodeRabbit found it.** Its comment shows the commands it ran: `rg` for every caller of
  `reloadFeatureFlags|identify|setPersonPropertiesForFlags|setAnalyticsEnabled`, then it read
  `analytics-client.ts` and `recorder-engine.ts:360-460`. It reasoned from the **absence** of a refresh call.
  The comment carries a "Supported by static analysis" badge; we do not know what that analysis was.
- **Is it real? Unverified.** The code facts hold: one synchronous read, no refresh call in the repo (CodeRabbit's
  search; not rerun here). Whether it matters depends on how posthog-js loads and caches flags, which we did not
  check. If flags are cached across launches and reloaded only at start, the failure is: a long-running tray app
  keeps the old value until restart, and the first take after a cold start with no cache reads the default `true`.
- **Severity (ours), if real: low to medium.** The kill switch is a rollback for a risky default flip, so its
  latency matters; the window is short or needs a cold cache.
- **Difficulty to find in our own review: 4 of 5.** The repo-visible part is a grep away; the part that decides
  whether it is a bug is a third-party library's runtime behaviour, which no line of the diff shows.

### C2 / W1, both found it — a labelling gap, not a detection gap

Wachiman saw the root cause (its flow answer says installs with diagnostics off "always read true") but posted
the finding on the runbook line as `docs`, `Consider`. Wachiman's own rule caps it: *"a problem that is only in
a comment, docstring, name or document is never a Fix"* ([review-policy.md](https://github.com/niway-dev/wachiman/blob/v1.8.0/docs/review-policy.md)).
CodeRabbit anchored the same fact on the code line `analytics.ts:26` and rated it Major. We have not read the
model's reasoning, so "the rule caused the downgrade" is a hypothesis consistent with the label, not proof.

## What Wachiman found that CodeRabbit did not

Verified: W2, W3, L2. Owner-accepted: W8, W9 to W14. Everything else is unverified. #540 is not a fair
comparison, because CodeRabbit never looked at the files.

## Next, to make this a study

- **Tie every unverified row to evidence.** Check C3 against posthog-js; read the code behind W5 to W7, W15 to
  W19, L3 and L4.
- **Rerun Wachiman locally on each CodeRabbit-only row** at the same commit, on Opus as well as Sonnet, to
  separate model from tool.
- **More columns once there is more data:** time from push to first comment, cost per owner-accepted finding,
  repeats across pushes, reply rate by the owner, severity as judged by us against each tool's label.
- **Daily collection** already runs in draft #11 on Haiku; the CI side here is still manual.
- **Record verdicts** with `wachiman history --verdict` for the local rows so the history stays consistent.

## Limits

One day, seven PRs, one repository, one owner. "Owner-accepted" means the owner fixed it after the comment, not
that it was independently judged. The ledger was built by one model reading both bots' output and the code, and
has not been reviewed by a second reader.
