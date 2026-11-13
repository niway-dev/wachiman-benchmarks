# Contract and ordering bugs: does local Wachiman 1.12.0 catch what the t3code bots let through?

Run on 2026-11-12. Result in one line: **of the 5 cases whose bug the reviewed diff really adds, Wachiman caught 0 with product defaults (1 partial), 1 with a flow-tracing focus file (arm B), 0 with boundary questions in the batch prompt on Sonnet (arm C), and 1 of 3 with the same questions on Opus (arm C-Opus), for $13.62 (estimated) across 25 runs.** Two of the original 7 goldens are not in the diff that was reviewed (see [Golden check](#golden-check)). Questions, wherever they sit and however strict the answer they demand, did not reliably find these bugs.

## Question

Our t3code analysis (`../README.md`, `../catalogue.md`) claimed the bots fail where a reviewer has to "look at the bug, not the line": races, event ordering, state machines and contracts that span files. Wachiman 1.12.0 already asks flow questions (`FLOW_QUESTIONS` in the wachiman repo's `src/engine.ts`: equivalent path, before/after, remount, failure path). Do those questions catch bugs of this kind that CodeRabbit and Macroscope missed in pingdotgg/t3code? And does a focus file that asks for explicit caller/callee, ordering and state-transition tracing help?

## Setup

- Repository: fork `niway-dev/t3code` of `pingdotgg/t3code` (GitHub Actions disabled on the fork), cloned in full to `/tmp/t3code-fork`. Main at the time of the run: `4fd40e1a16e3800418b8f6a32932b68179098c8d`.
- Engine: a separate worktree of the wachiman repo at `origin/main` = `c3e46d5` (version 1.12.0). **Local, uncommitted change:** `TIMEOUT_MS` in `src/connectors/local-git.ts` raised from `60_000` to `300_000`. Without it the t3code snapshot times out (wachiman issue #193: `git add` takes about 57 s against a 60 s limit). Nothing else was changed.
- Reviewer: Claude Sonnet 5.5, effort high (product default), through Claude Code, profile `isolated:personal`. No other reviewer ran. Runs were sequential, one at a time.
- Command, per run: `env -u ANTHROPIC_API_KEY WACHIMAN_DIR=<worktree> wachiman local --repo-dir /tmp/t3code-fork --commit <sha> --profile isolated:personal --format json --output runs/<arm>-<pr>.json`.
- Commit reviewed: the introducing PR's squash commit on `main` (one parent each, checked), so Wachiman sees the diff the author would have reviewed locally. The defect's lines were checked to exist in each commit.

### Arms

- **A, product defaults:** `--commit <squash sha>`.
- **B, focus file:** the engine reads `.github/wachiman.md` from the base (parent) commit. For each case a branch `bench/contract-order-B-<pr>` in the fork has one extra commit on the squash commit's parent that adds [`focus-file-arm-b.md`](focus-file-arm-b.md) as `.github/wachiman.md`, then the squash commit cherry-picked on top. Wachiman reviewed the cherry-pick. Checked: `git patch-id --stable` of the reviewed diff equals that of the original squash commit for all 7 cases; no original parent had a `.github/wachiman.md`; each B report's `instructionChanges.baseSha` is the focus commit, and the local connector reads the focus file at that sha (`instructionsFrom` in `src/connectors/local-git.ts`). Not checked: the rendered prompt itself, since 1.12.0 does not dump it.
- The brief said to run B only on cases A missed. A missed 6 outright and caught #33632 only partially, so B ran on all 7.
- **C, boundary questions in the batch prompt:** the same command and commit as A, with one local, uncommitted patch to the engine worktree ([`engine-arm-c.diff`](engine-arm-c.diff), on top of the `TIMEOUT_MS` change): a constant `BOUNDARY_QUESTIONS` holding [`question-block-arm-c.md`](question-block-arm-c.md), rendered in `buildBatchPrompt` right after `FLOW_QUESTIONS` and the data-path questions of [wachiman PR #88](https://github.com/niway-dev/wachiman/pull/88). Unlike those, it is asked of every batch, with no trigger. Its six questions are written by class (timer, option passed to a callee, collection, stored id, external command output, list sent to a save endpoint) and each demands a `contracts` entry with the path:line opened on the other side of the boundary, or `status: "open"` with an `open_question` starting "not found:". The only difference from A is this block. Checked: the wrapper runs `src/cli.ts` of `WACHIMAN_DIR`, and the patched template line is the only `${BOUNDARY_QUESTIONS}` use. Not checked: the rendered prompt itself (1.12.0 does not dump it).
- **C-Opus:** arm C again with `AGENT_REVIEW_MODEL=claude-opus-5-5 AGENT_REVIEW_EFFORT=high` (the 1.12.0 local CLI has no `--model` flag; the engine reads these variables, and each report's `provider.model` confirms `claude-opus-5-5`). It was meant for every case C missed (all 7). It ran on 4 of them (#21315, #19432, #22107, #19355): with Opus at about 1.8 times C's measured cost per run, the other 3 would have pushed this thread past its $8 cap. Skipped: #18505 and #33632 (estimated $1.8 and $2.1), and #7599, whose golden is not in the reviewed diff.

### Cases

Seven escaped bugs from `../replay-shortlist.md` (six) and `../catalogue.md` (one), each of class race, ordering, state machine or cross-file contract, introduced by a PR merged to `main` with at most 40 files, with no bot comment on the defect at the introducing PR. Goldens are the shortlist's, checked there against the fix PR's diff; for #7599 the fix #22572 was read here (it replaces the 5 s quit timeout with `BACKEND_QUIT_STOP_TIMEOUT`). Two of these goldens later proved not to be in the reviewed diff; see [Golden check](#golden-check).

| id | intro PR | squash commit | files | class | fix PR |
| --- | --- | --- | --- | --- | --- |
| checkpoint-ignore-check-drops-untracked | #21315 | `2e860972ae1740e0e82717a5fc2683513936188b` | 2 | contract (git output to consumer) | #32374 |
| git-timeout-no-force-kill-permit-leak | #22107 | `3fdcef09944955a3e94e906ecf892bfbc1f7efc4` | 3 | race, resource leak | #26601 |
| detach-session-strands-pending-approval | #19355 | `519d64f6cec0a0f9ed18fbca4a3f8695cac44506` | 7 | state machine | #33535 |
| provider-env-duplicate-row-deletes-stored-secret | #18505 | `d514a8c6176ace9057dc8c7619f0b5f0d81d1bd0` | 15 | contract (web rows to server save) | #31337 |
| mcp-csrf-bound-to-session-id-breaks-hosted-approval | #33632 | `9a0d02723c182cd9da01973b30c2b38b299bdbc6` | 24 | cross-file contract (server token vs client runtime) | #33645 |
| ssh-stale-pid-wrong-process | #19432 | `36f91c45687f97fc8e12ff89eaa8cff6f23abe8b` | 2 | ordering, process identity | #26963 |
| desktop-quit-timeout-equals-sigterm-grace | #7599 | `8ddd9f7efcdfb6e32b614595242b5986942d37b0` | 2 | ordering, cross-file timing contract | #22572 |

## Results

Caught = a finding that names the same defect (same cause, not only the same file). Cost is the engine's `costUsdEstimate` (subscription run, so an API-price estimate, not a bill). Time is wall clock for the whole command, snapshot included.

| case | A caught | A findings | A cost | A time | B caught | B findings | B cost | B time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #21315 checkpoint ignore probe | no | 0 | $0.25 | 107 s | no | 0 | $0.23 | 121 s |
| #22107 git force-kill / permit leak | no | 3 | $0.38 | 154 s | no | 3 | $0.37 | 136 s |
| #19355 detach strands approval | no | 2 | $0.38 | 141 s | no | 2 | $0.38 | 131 s |
| #18505 duplicate row deletes secret | no | 5 | $0.69 | 230 s | no | 4 | $0.96 | 303 s |
| #33632 CSRF bound to session id | partial | 9 | $1.14 | 326 s | no | 4 | $1.13 | 336 s |
| #19432 stale pid, wrong process | no | 0 | $0.31 | 140 s | **yes** | 2 | $0.36 | 171 s |
| #7599 quit timeout = SIGTERM grace | no | 2 | $0.33 | 105 s | no | 2 | $0.30 | 119 s |
| **total** | **0 (+1 partial)** | 21 | **$3.49** | 20 min | **1** | 17 | **$3.73** | 22 min |

Arm C and C-Opus, same cases and command (caught on the 5 valid cases in bold; "-" = not run):

| case | golden valid | C caught | C findings | C contracts | C cost | C time | C-Opus caught | C-Opus findings | C-Opus cost | C-Opus time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #21315 checkpoint ignore probe | no | no | 1 | 1 | $0.29 | 255 s | no | 0 | $0.51 | 138 s |
| #22107 git force-kill / permit leak | yes | no | 3 | 3 | $0.38 | 400 s | no | 4 | $0.65 | 166 s |
| #19355 detach strands approval | yes | no | 1 | 3 | $0.44 | 153 s | no | 1 | $0.47 | 134 s |
| #18505 duplicate row deletes secret | yes | no | 4 | 6 | $0.99 | 298 s | - | - | - | - |
| #33632 CSRF bound to session id | yes | no | 5 | 10 | $1.20 | 349 s | - | - | - | - |
| #19432 stale pid, wrong process | yes | no | 3 | 3 | $0.30 | 154 s | **yes** | 2 | $0.65 | 177 s |
| #7599 quit timeout = SIGTERM grace | no | no | 3 | 3 | $0.51 | 167 s | - | - | - | - |
| **total** | 5 valid | **0** | 20 | 29 | **$4.11** | 30 min | **1 of 3 valid** | 7 | **$2.29** | 10 min |

On the 5 valid cases: A 0 (+1 partial), B 1, C 0, C-Opus 1 of the 3 it ran. Arm A wrote 20 `contracts` entries over the 7 runs, C wrote 29; C used "not found:" once (#7599).

Run files: [`runs/`](runs/) (`A-<pr>.json`, `B-<pr>.json`, `C-<pr>.json`, `C-opus-<pr>.json`). The engine's text logs were not kept in the repository; the data-path questions of PR #88 that fired per C run were read from them: `bounded-wait` on #22107, #19432, #7599 and #33632 (part 1), `stale-write-back` on #19355, none on #21315 and #18505. The trigger is a regex over the diff, so A had the same ones.

## Golden check

While reading the arm C answers, two goldens turned out not to be in the diff that was reviewed. Checked against the fork:

- **#7599:** at the reviewed commit [`8ddd9f7`](https://github.com/pingdotgg/t3code/commit/8ddd9f7efcdfb6e32b614595242b5986942d37b0), `DEFAULT_BACKEND_TERMINATE_GRACE` is **2 s** (`DesktopBackendManager.ts:67`), so the new 5 s quit timeout leaves room for SIGTERM, the 2 s grace and SIGKILL. The fix's own rule, `BACKEND_QUIT_STOP_TIMEOUT = grace + 2 s`, gives 4 s, under 5 s. The grace became 5 s later, in [`eeaac49`](https://github.com/pingdotgg/t3code/commit/eeaac49a9d20d94970b26fe7775fc8ddb4672f4f) ("update all no longer runs agents twice", #19291), which did not touch the quit timeout. The bug was introduced there, not in #7599. Arm C's answer at #7599 compared exactly these numbers and was right for that commit.
- **#21315:** the `check-ignore --no-index` probe and its `workspaceIgnored ? "-u" : "-A"` consumer (`GitVcsDriver.ts:1053`, `:1122` at the reviewed commit) were added by [`6d266ea`](https://github.com/pingdotgg/t3code/commit/6d266ea683ecc46c17aed5d68a093221be093862) (#14892). The #21315 diff never touches them: none of its added or removed lines mention the probe. The shortlist checked that the lines exist at head, not that the diff adds them.
- The other five were checked the same way: the defect's line, or the omission, is in the diff's added lines. #22107 adds `forceKillAfter: input.forceKillAfterMs`; #19355 adds `detachedThreadId` to the loop at `:800` and not to the loop at `:687`; #18505 adds both `remove-secret` pushes; #33632 switches `approvingSession` to `authenticateHttpRequest` (DPoP sessions) while the CSRF token stays derived from the session id; #19432 adds the `kill -0` checks.

Every count below uses the 5 valid cases; the 7-case counts above are kept so the tables match the run files.

## Diagnosis: did arm B open the other side of the boundary?

Wachiman 1.12.0 runs local reviews with `--no-session-persistence`, so no transcript of the B runs exists. The isolated profile kept only two oversized tool-result files from that day, which cannot be tied to a run. What the run JSON shows is what the reviewer **cited** in `contracts.evidence` and finding bodies. A cited line was opened. An uncited one may or may not have been opened, so "no citation" means "unknown", not "did not look".

| case | other side, at the reviewed commit | cited in B | opened |
| --- | --- | --- | --- |
| #21315 (golden not in diff) | `filterIgnoredPaths` probe `GitVcsDriver.ts:724-760`, consumer `:1053`, `:1122`; git's `check-ignore` output (outside the repo) | no (cited `:793-953` only) | unknown |
| #22107 | where `forceKillAfter` is read: `.repos/effect-smol/packages/platform/node-shared/src/NodeChildProcessSpawner.ts:478-493` | no | unknown |
| #19355 | the loop in `writeReleasedRuntimeRequestEvents`, `ProviderSessionManager.ts:687` | sibling loop `:800` and caller `:906` cited; `:671-700` not | sibling yes, buggy loop unknown |
| #18505 | the server save, `serverSettings.ts:953` and `:965` | yes (`:932-987`) | **yes: looked and did not see** |
| #33632 | the client's credential renewal, `packages/client-runtime/src/state/environmentHttpAuth.ts:178-271`, and `McpOAuth.ts:310-319`, `:410-422` | yes | **yes: looked and did not see** |
| #7599 (golden not in diff) | `DesktopBackendManager.ts:67` grace, `:486` | no (cited `:350-371`, `:1048-1090`) | unknown |

Arm C answers part of the question for the uncited cases. On #22107 Sonnet C cited the spawner at `:478-493` and wrote the bug's mechanism in a contract entry: "When undefined it waits ... after SIGTERM and never escalates", and "Other `execute` callers do not set it". It did not call that a defect, and it reported no finding. On #19355, C wrote a class (c) entry for `attachedThreadIds` that listed readers at `:2454-2470` and `:2524-2533`. It still did not cite the loop at `:687`.

## Which questions worked

"Should have caught" uses the 5 valid cases. Arm B's focus file has four points; arm C's block has six questions. One run per arm and case: "did" means it happened once, not that the question causes it.

| arm | question (short) | should have caught | did it | what the runs show |
| --- | --- | --- | --- | --- |
| B | 1. trace callers and callees across files | #22107, #33632 | no | no citation of the spawner in #22107 |
| B | 2. order of events for processes, sessions, timers | #22107, #19432 | #19432 yes, #22107 no | the #19432 finding fits point 2 or 4; which one drove it is not visible |
| B | 3. every reader of a state the change adds or removes | #19355 | no | cited the correct sibling loop, not the buggy one |
| B | 4. a value that crosses a boundary: empty, blank, reused, default | #33632, #19432 | #19432 yes, #33632 no (A's partial lost) | see point 2 |
| C | 1. a timeout: every other timer on the operation, compare numbers | none valid (#7599 was the target) | n/a | answered with numbers in C-7599, C-19432, C-Opus-22107; correct each time. The question works as an instruction. |
| C | 2. an option passed to a callee: where it is read, what undefined does | #22107 | no | Sonnet opened the callee and stated the undefined behaviour, but judged it fine. Opus cited only the type (`ChildProcess.ts:269`) and assumed "the platform default escalation". |
| C | 3. a collection: every loop or reader, what each skips | #19355 | no | Sonnet listed two readers, not `:687`; Opus wrote no entry for the set |
| C | 4. a stored id, pid, token: who else creates it, reuse | #19432, #33632 | #19432 on Opus yes, on Sonnet no; #33632 no | Opus entry: "server_running ... catches zombies but not a reused PID", then a `fix` finding with the golden's fix. Sonnet C on #33632 wrote "a renewed token with a different session id gives a CSRF mismatch" in a contract, the same partial as A, with no finding. |
| C | 5. external command output on empty or no match | none valid (#21315 was the target) | n/a | no entry in either run |
| C | 6. a list sent to a save endpoint: duplicate keys, missing vs empty | #18505 | no | no entry about duplicate rows |

Checked: the arm C questions were written in this thread, from the owner's list of classes, after these bugs were known, one class per bug. That makes them **in-sample**: a hit would overstate how well they generalise, and even so they produced one hit in 10 valid case runs (C and C-Opus). Each arm ran once per case, so there is no variance estimate.

### The hits

- **B-19432, caught.** The finding at `packages/ssh/src/tunnel.ts:720` says that when "the pid file still names a PID that an unrelated process now holds", `server_running` is true, each reconnect waits the full 60 s, and "even that [stop] script would `kill` the unrelated PID", and suggests "checking the command line" before treating the PID as ours. That is the golden's cause, both consequences and the fix #26963 applied (`managed_server_running` checks `ps -o args=`). It was rated `consider`, not `fix`.
- **A-33632, partial.** A `consider` finding at `connectMcpApproval.ts:95` asks: "`csrfToken` is signed over `session.sessionId` ... and `approve` compares it with the session of the decision request ... If a renewed relay token maps to a different session id", the approval is refused. That is the golden's cause. It is partial because it limits the trigger to token renewal near expiry, while the real trigger is that the hosted client mints a fresh session on every call, so every hosted approval failed; and it says it did not check how the relay issues sessions. B, on the same diff, did not raise it.

### Near misses (same file or area, different cause)

- #22107 (A and B): a `fix` finding on `Fiber.await(pending)` in pull, in the same git driver and about hung git processes holding permits, but it blames the missing await timeout, not the undefined `forceKillAfter` that leaves a SIGTERM-ignoring git alive.
- #7599 (A and B): both flag the 5 s quit timeout, but say it bounds only `closeRun`, not the rest of `stop()`. Neither compares it with the 5 s SIGTERM grace in `DesktopBackendManager.ts`, which is the bug.
- #19355 (B): a finding on the release path in `ProviderSessionManager.ts` (compare-and-set retries), the right function family, but not the `attachedThreadIds` loop that skips the detached thread.

### Other findings that name a possible real bug

A Sonnet worker checked the seven most bug-like other findings against `main` at `4fd40e1a16`. None was fixed by a later commit, so none is confirmed real by t3code's own history:

| finding | arm | at main |
| --- | --- | --- |
| Pull's `Fiber.await(pending)` has no timeout (`GitVcsDriverCore.ts`) | A, B | still present (`:3065`) |
| Code fallback link renders only after a successful Connect call (`ApproveAgentSurface.tsx:159`) | A | still present |
| Wizard skips the code on the static capability, server redirect is conditional (`UseInAnotherAppDialog.tsx:125`) | A, B | still present |
| Quit timeout bounds only `closeRun` (`DesktopApp.ts:154`) | A, B | still present; #22572 changed only the value |
| Card/dialog branches pass the redaction marker as `SecretInput` value (`ProviderSettingsForm.tsx:516`) | A, B | still present |
| Hand-maintained `providerSecretFields` list (`settingsSecrets.ts:24`) | A, B | not a bug so far: every driver with a secret is listed |
| Exhausted compare-and-set retries never retried (`ProviderSessionManager.ts:877`) | B | still present |

"Still present" means unconfirmed, not wrong: these may be real bugs nobody has hit yet.

## Conclusions

1. **Checked:** with product defaults Wachiman 1.12.0 stated none of the 5 valid goldens as a finding, and came close on one (#33632, right cause as a question, wrong trigger).
2. **Checked:** with the focus file (B) it stated 1 of 5 (#19432) and lost the partial on #33632.
3. **Checked:** with boundary questions in the batch prompt (C, Sonnet 5.5 high) it stated 0 of 5. With the same questions on Opus 5.5 high it stated 1 of the 3 valid cases it ran (#19432, rated `fix`, with the golden's fix).
4. **Checked:** two of the 7 goldens (#7599, #21315) are not in the reviewed diff. A, B and C could not have caught them as introduced bugs. Arm C's timer answer on #7599 was correct for the code it saw.
5. **Checked:** the reviewer obeyed the "show the other side" demand only in part. C wrote 29 contract entries against A's 20, and used "not found:" once. Several values that cross a boundary got no entry: the duplicate rows in #18505, the pid file in Sonnet's #19432, the command output in #21315.
6. **Checked, from the run files:** in at least three valid cases the reviewer had the other side in hand and still did not report the bug. In #18505 and #33632, B cited the lines where the bug is. In #22107, C wrote the mechanism in a contract and called it fine. For these, the failure is in judging what was seen, not in finding the code. For #19355 and B's #22107 the run files cannot say whether the reviewer looked.
7. **Inferred:** the three differences between B and the [2026-11-03 data-path A/B](https://github.com/niway-dev/wachiman-benchmarks/blob/main/2026-11-03-data-path-questions-ab/README.md) do not explain the gap on this sample. Moving the questions into the batch prompt and demanding a visible answer (C) did not beat B. Opus caught the same single case that Sonnet B caught. One run per case cannot separate a model effect from noise.
8. **Inferred:** a question helps when it names the comparison the reviewer would otherwise skip and the answer is a fact (timer numbers, pid identity). It did not help when the defect needs a judgment about what the fact means: an undefined option, one loop of two, two rows with one key. That matches the 2026-11-03 result only loosely, since those questions were scored on another repository.
9. **Checked:** cost per run, estimated: $0.29 to $1.20 for C, $0.47 to $0.65 for C-Opus (about 1.8 times C on the same cases). This thread spent $6.40 (C $4.11, C-Opus $2.29).

## Limits

- Seven cases, of which five are valid, and one run per arm and case: no variance estimate.
- The arm C questions were written after seeing these bugs (in-sample), one class per golden.
- C-Opus ran on 4 of the 7 cases, 3 of them valid, because of the $8 cap on this thread.
- "Opened" is inferred from citations, because 1.12.0 keeps no transcript of local runs.
- The local `TIMEOUT_MS` change means the engine was not exactly 1.12.0 as shipped; it affects only how long git snapshot commands may run, not the prompt.
- Goldens for six cases come from the shortlist's earlier check against the fix diffs; this run re-read only #22572.
- The fork's `main` was used as "later t3code" for the other-findings check (the fork was created on 2026-11-12 from upstream `main`).
