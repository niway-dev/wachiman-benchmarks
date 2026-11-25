# CodeRabbit against Wachiman local on agent-orchestrator #9068 (2026-11-25)

## One-minute block

- **PR:** [OrchestratorInc/agent-orchestrator#9068](https://github.com/OrchestratorInc/agent-orchestrator/pull/9068),
  a name and a color per agent account. It touches a Go backend (store, service, HTTP DTOs,
  generated OpenAPI) and a React/TypeScript frontend. The repository is public.
- **Pairs: 0.** Special cases: 2 (both `unpaired`). Wachiman never ran on the PR. It ran six
  times **locally** (`wachiman local --history`, `basis: rerun`), on its own ranges, while
  CodeRabbit ran live on two commits. No commit was reviewed by both tools, so nothing here is
  a scored comparison.
- **Verified defects that CodeRabbit raised:** 4, all low severity. Three were fixed in the PR.
  One was declined as a follow-up for the spec generator.
- **What CodeRabbit found that Wachiman did not:** two contract gaps in code that Wachiman's
  first run read line for line (an OpenAPI enum and its Go struct tag), and one gap in a file
  **outside the diff** (a second account picker that did not get the new badge). The fourth
  finding was in code Wachiman never saw before it was fixed, so it is not a miss.
- **Wachiman version:** v1.17.0 on all six runs, model `claude-sonnet-5-5`, profile `personal`
  (from each run's `engine.version` and its log). CodeRabbit's version is not published.

## Pairs

None. [`pairs/pairs.md`](pairs/pairs.md) is the generated table, with no rows.
`pair.ts` reads only the reviews posted on the PR. The local runs never posted anything, so it
does not see them.

### Wachiman's six local runs

| Run | Range (base..head) | Files | Findings | Estimated cost |
| --- | --- | --- | --- | --- |
| r1 | `2fe8d90..aa05b6d` (the whole branch at that point) | 45 | 1: `UpdateIdentity` reads then writes both columns with no lock | $0.76 |
| r2 | `aa05b6d..cf6d22c` | 3 | 1: the identity lock stays held while `view()` runs CLI reads | $0.26 |
| r3 | `cf6d22c..42e6c13` | 2 | 0 | $0.16 |
| r4 | `42e6c13..2faf7ac` | 2 | 0 | $0.11 |
| r5 | `2faf7ac..abe9009` | 2 | 0 | $0.16 |
| r6 | `abe9009..5d2be83` (after CodeRabbit's comments were fixed) | 7 | 0 | $0.35 |

Both Wachiman findings were Go concurrency bugs, and both were fixed (`cf6d22c`, `42e6c13`).
CodeRabbit first ran at `abe9009`, after both fixes, so whether it would have flagged them is
unknown.

### CodeRabbit's findings and the verdicts

[`verdicts.csv`](verdicts.csv) holds one row per finding. These verdicts are **not** pair
verdicts: every finding is in `special-cases.csv` as `unpaired`.

| Finding | Commit | Verdict | Severity | Fix |
| --- | --- | --- | --- | --- |
| The `color` enum on `AddAgentAccountAPIKeyRequest` lacks `""` | `abe9009` | owner-accepted | low | `4d1ed08` |
| The nullable `color` schema in `openapi.yaml` lacks `null` in its enum | `abe9009` | verified, declined | low | follow-up for the generator |
| The session account picker (`SessionAccountSummary.tsx`) does not show the new badge | `abe9009` | owner-accepted | low | `f4fc86d` |
| The new badge broke typeahead in that picker (needs `textValue`) | `f4fc86d` | owner-accepted | low | `5d2be83` |

## Gaps

These are findings that only CodeRabbit made, that were verified, and whose lines Wachiman had
actually reviewed. `git diff aa05b6d abe9009` is empty for `dto.go`, `openapi.yaml` and
`SessionAccountSummary.tsx`. So r1 read the same code that CodeRabbit flagged later. Its
coverage lists `dto.go` and `openapi.yaml` as reviewed.

1. **Creation enum without the empty color.** The PATCH request already listed `""` (the value
   that clears a color, added in `0564bbd`). The create request in the same file, nine lines
   above it, did not.
   - What happens: the generated TypeScript type rejects `""` on create, so a client that sends
     "no color" has to omit the field or cast the body.
   - Why CodeRabbit found it: it compared the two sibling struct tags in the same file.
   - Difficulty 2: the evidence sits in two adjacent lines.
2. **Nullable enum without `null`.** In OpenAPI 3.0, `nullable: true` combined with an `enum`
   still rejects `null` unless the enum lists it. A validator would reject a `null` color.
   - This is a spec-correctness rule, not app behavior, and the field comes from the generator.
     That is why it was declined in the PR.
   - Why CodeRabbit found it: a rule about the OpenAPI format, applied to generated YAML.
   - Difficulty 3.
3. **A second picker outside the diff.** The PR added the badge to the composer picker. A
   separate session account picker, in a file the PR did not touch, kept showing bare emails.
   - Why CodeRabbit found it: it searched the repository for other places that render the same
     account options. It posted this under "Outside diff range comments". Wachiman reviews the
     diff and its declared context, so it cannot see this kind of gap.
   - Difficulty 4: you have to know the other component exists.

The fourth finding (typeahead) is **not a gap**. CodeRabbit flagged `f4fc86d`, and that defect
was fixed in `5d2be83` before r6 ran. r6 reviewed `abe9009..5d2be83`, which already included
the fix.

### What the gaps have in common

All three are **consistency** findings: "this sibling has X, that one does not". None of them is
a local logic bug. Wachiman found the deeper Go problems (a read-then-write race, and a lock held
across I/O) and missed the cheaper cross-checks:

- sibling struct tags in one file;
- format rules on generated specs;
- other call sites outside the diff.

Each of the three is a candidate check to add to Wachiman's instructions. The third one also
needs repository search beyond the diff.

## Special cases

| PR | Commit | Tool | Status | Reason |
| --- | --- | --- | --- | --- |
| 9068 | `abe9009` | coderabbit | unpaired | Wachiman never reviewed this commit live. r1 covered identical lines at `aa05b6d` (rerun). |
| 9068 | `f4fc86d` | coderabbit | unpaired | Wachiman never reviewed this commit. r6 reviewed past it, at `5d2be83`. |

None of these is `refused`, `skipped` or `partial`.

## Cost

- **Wachiman:** about $1.80 across six runs, at API prices. This is an estimate, not a bill:
  the runs used the `personal` subscription profile. Each run's figure is the sum of the
  batches' `cost_usd` from its log. `pairs.csv` has no Wachiman rows.
- **CodeRabbit:** not published.

## Limits

- **One PR, one day, one repository.**
- **No pairs.** Every comparison above depends on identical lines across different commits
  (`basis: rerun`), not on the same commit.
- **Who judged:** `claude-opus-5-5`, the same agent that wrote the PR and its fixes. The judging
  was not blind.
- **Not tested:** whether CodeRabbit would have caught the two concurrency bugs.
- **Local data:** the local review JSONs and logs stay on the laptop. Only their counts,
  ranges, versions and costs are copied here.

## How to reproduce this on another repository

1. **During the PR, run Wachiman locally after each push, with history:**
   `wachiman local --repo-dir <clone> --base <previous-head> --history --format json --output <dir>/rN.json 2> <dir>/rN.log`.
   Keep every `rN.json` and `rN.log`.
2. **Let CodeRabbit review the same PR on GitHub.** At least once, run Wachiman on the exact
   commit CodeRabbit reviewed (`--commit <sha>`, or `--base <merge-base>` with HEAD at that
   sha). That turns an `unpaired` case into a rerun pair.
3. **When the PR is done, run** `bun scripts/pair.ts --repo <owner/name> --prs <n> --other coderabbit --out <date>-<topic>/pairs`
   from a worktree of this repository.
4. **For each CodeRabbit finding,** use `git diff <wachiman-head> <coderabbit-commit> -- <path>`
   to check whether a local run read the same lines. Then write `verdicts.csv` and this README,
   in the order the `wachiman-audit` skill gives.
5. **Classify each gap:** a sibling inconsistency, a format rule, or outside the diff. That
   classification tells you which review instruction to add.

Tooling gap: `pair.ts` cannot ingest local `wachiman.review-result/1` files, so step 4 is done by
hand. A `--local <dir>` input that adds rerun rows would make it mechanical.
