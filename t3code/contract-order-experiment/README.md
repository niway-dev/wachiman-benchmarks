# Contract and ordering bugs: does local Wachiman 1.12.0 catch what the t3code bots let through?

Run on 2026-11-12. Result in one line: **Wachiman caught 0 of 7 with product defaults (1 partial) and 1 of 7 with a flow-tracing focus file, for $7.22 (estimated) across 14 runs.** The flow questions do not, on their own, find these bugs.

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

### Cases

Seven escaped bugs from `../replay-shortlist.md` (six) and `../catalogue.md` (one), each of class race, ordering, state machine or cross-file contract, introduced by a PR merged to `main` with at most 40 files, with no bot comment on the defect at the introducing PR. Goldens are the shortlist's, checked there against the fix PR's diff; for #7599 the fix #22572 was read here (it replaces the 5 s quit timeout with `BACKEND_QUIT_STOP_TIMEOUT`).

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

Run files: [`runs/`](runs/) (`A-<pr>.json`, `B-<pr>.json`).

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

1. **Checked:** with product defaults Wachiman 1.12.0 stated none of the 7 goldens as a finding, and came close on one (#33632, right cause as a question, wrong trigger). The flow questions alone do not catch these contract and ordering bugs.
2. **Checked:** with the focus file it stated 1 of 7 (#19432) and lost the partial on #33632. Net change: +1 caught, -1 partial.
3. **Inferred:** the B gain is not attributable to the focus file. Each arm ran once per case, and the 1.12.0 reviewer is non-deterministic, so one hit in seven, with another hit lost, is within run-to-run noise. Repeated runs (at least 3 per arm and case) are needed before saying the focus file helps.
4. **Inferred:** the misses share a pattern. The reviewer reads the changed code's contracts carefully (21 and 17 findings, several plausible) but does not follow a value to the other side of the boundary where the bug is: an undefined option to the process that never gets SIGKILL (#22107), a removed set member to the loop that reads the set (#19355), a 5 s timeout to the 5 s grace in another file (#7599), an empty `check-ignore` output to git's blank-line semantics (#21315). Even when asked explicitly to do this (arm B, point 4 of the focus file), it did not, in 6 of 7 cases.
5. **Checked:** cost is small: $0.23 to $1.14 per run (estimated), 2 to 6 minutes, about $0.50 a run on average.
6. **Inferred:** "look at the bug, not the line" is a real weakness of Wachiman too, not only of CodeRabbit and Macroscope, on this sample. A prompt asking for tracing is not enough; a mechanism that hands the reviewer the other side of the boundary (callers and readers of changed values, sibling loops, the matching timeout) is the next thing to test.

## Limits

- Seven cases, one run per arm and case: no variance estimate.
- The local `TIMEOUT_MS` change means the engine was not exactly 1.12.0 as shipped; it affects only how long git snapshot commands may run, not the prompt.
- Goldens for six cases come from the shortlist's earlier check against the fix diffs; this run re-read only #22572.
- The fork's `main` was used as "later t3code" for the other-findings check (the fork was created on 2026-11-12 from upstream `main`).
