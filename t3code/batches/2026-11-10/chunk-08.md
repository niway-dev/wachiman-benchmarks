# Chunk 08: PRs #28353..#13809 (2026-11-10, last chunk of the day, 11 PRs)

## 1. Header

- PRs covered: 11 (#28353 .. #13809). 2 have no bot thread (#26630, #26374).
- Bot threads: 41 total. CodeRabbit 29, Macroscope 12.
- Verdicts: real-bug 5, real-minor 20, nit 12, wrong 3, unclear 1.
- Outcomes: fixed-before-merge 33, ignored/no reply 4 (all #27677), disputed 4 (3 bot withdrawals or acceptances, 1 author dispute accepted).
- Code checked: #27677 adapter.ts at merge commit eff45664fa (lines 2975-3045). Everything else is judged from thread text, replies and resolved/outdated flags (unverified in code).
- Track B: all 11 are `fix` PRs; 8 touch non-trivial source (the rest: #25422 icon swap and lint rule, trivial). SZZ run on 10; 2 pure additions (#27677, #26374). Several PR numbers are low relative to merge date (for example #13809 merged 2026-11-10), so PR number does not order merges.
- Caveat: the author replies are written by AI agents ("on behalf of"), and the PR bodies are long evidence reports. Verdicts rely on those replies.

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 28353 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | security/privacy | no | Full error `cause` logged on screenshot failure can carry URL query or command output. Fixed b8c6ca5 (unverified in code). |
| 28353 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Test mock should assert fallback omits `--display`. Test strengthening, fixed bd62026. |
| 28353 | 3 | MS | Medium | real-minor | fixed-before-merge | 2 | 2 | security/privacy | no | New early-return screenshot response lacks `Cache-Control: no-store`, so authenticated PNGs could be cached. Fixed 7d1f93d. |
| 28221 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | After an idle-write failure a new snapshot waits for the old retry deadline because `scheduleIdleFlush` returns when a timer exists. Outdated after 27c2e13 (unverified). |
| 28221 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 3 | race/ordering | no | Test awaits the wrong ingestion, flaky by fiber scheduling. Test only. |
| 28221 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | resource leak | no | Idle-flush failure logs a warning on every retry (about 120 per hour during disk full). Fixed fb8d99b with the 10-minute limit used elsewhere. |
| 28221 | 4 | CR | Minor | nit | fixed-before-merge | 1 | 2 | race/ordering | no | Second test race, await a Deferred. Test only. |
| 28221 | 5 | CR | Major | real-bug | fixed-before-merge | 3 | 5 | race/ordering | yes | An idle tick can end ingestion before queued OpenCode continuation events reach the consumer, dropping nested output. Fixed 9a3ac59 by keeping the last stored root snapshot's pending flag (unverified in code; CR re-checked `9a3ac59`). |
| 28221 | 6 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Asks for a comment on an untraced helper (convention). Fixed 41e8ac4. |
| 27791 | 1 | CR | Minor | wrong | disputed | 1 | 4 | race/ordering | no | Wanted release to await a pending usage-limit read. Author: Force Stop and sign-in change deliberately terminate; CR withdrew R3 and its sibling R4. |
| 27791 | 2 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Redundant test row; removed d2dfacc. |
| 27791 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | A defect in reset reconciliation kills the fiber before terminal publication, losing the usage-limit semantics. Fixed 52b2ecd. |
| 27791 | 4 | MS | High | real-bug | fixed-before-merge | 3 | 4 | data integrity | yes | A successful `account/rateLimits/read` leaves removed windows in published usage limits (stale exhausted allowance). Fixed 43bb8fd with a replacement path (unverified in code). |
| 27791 | 5 | CR | Minor | nit | fixed-before-merge | 1 | 3 | race/ordering | no | Test gate for late reset notification. Test only. |
| 27791 | 6 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | data integrity | no | Enrichment of the failure item drops retry state and `startedAt`. Fixed a18548c. |
| 27791 | 7 | MS | High | real-bug | fixed-before-merge | 3 | 4 | data integrity | yes | A notification without `resetsAt` during a pending read drops the read's reset, so the terminal never auto-recovers. Fixed 65d61c3 with a regression row (unverified in code). |
| 27791 | 8 | MS | High | real-bug | fixed-before-merge | 3 | 5 | data integrity | yes | A pending read can attach a Plus-plan reset to a Free-plan snapshot when window values are unchanged. Fixed e5c699b: the whole read is rejected on plan mismatch. Domain-specific. |
| 27677 | 1 | CR | Major | real-minor | ignored | 2 | 4 | error handling | maybe | After receipt completes, `tapError` still propagates a request rejection, so `raceFirst` can fail an admitted command. Merged code (lines 3000-3015) shows `tapError` returns `Effect.void` but the error continues; consistent with the claim, not exercised. Unresolved. |
| 27677 | 2 | CR | Minor | real-minor | ignored | 1 | 2 | error handling | no | Pre-admission failures get the generic "Provider turn failed." instead of `OpenCodeRuntimeError.detail`. Unresolved. |
| 27677 | 3 | CR | Major | unclear | ignored | 3 | 4 | error handling | maybe | Guard suppresses admitted HTTP failures (error before runner start) so the turn can hang. Plausible: merged guard only checks `Deferred.isDoneUnsafe(receipt)`, no status check. Hang not reproduced. Unresolved. |
| 27677 | 4 | MS | none | nit | ignored | 1 | 1 | other | no | Fold a duplicate test setup. |
| 26570 | 1 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | other | no | Eval regexes match anywhere in the expression (false passes). Eval harness, fixed 4fd58c2 (unverified). |
| 26570 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Chart eval ignores `type`/`data`. Fixed ff30815. |
| 26570 | 3 | CR | Major | real-minor | fixed-before-merge | 1 | 3 | other | no | Eval grades invocation text as an executed call. Rated Major by CR but only affects eval quality; fixed ff30815. |
| 26570 | 4 | CR | Major | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Fixtures used `navigator.modelContext.callTool`, not the documented `document.modelContext.executeTool`; evals could pass against a nonexistent API. Fixed 29e2204. Eval only, not product. |
| 26570 | 5 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Chart argument order in regex. Fixed. |
| 26570 | 6 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | other | no | Omitted `tabId` keyed as `undefined` in the replay. Fixed d492068. |
| 26570 | 7 | MS | Low | real-minor | fixed-before-merge | 1 | 3 | other | no | `notCalls delete_note` passes because a throwing mock hides the delete. Fixed 1d49b65. |
| 26570 | 8 | CR | Minor | wrong | disputed | 1 | 3 | other | no | Author cites the WebMCP spec: input is serialized first; CR agreed. |
| 26570 | 9 | CR | Minor | nit | fixed-before-merge | 1 | 3 | other | no | Reject non-object parsed inputs in the replay. Fixed c2f9d7b. |
| 25422 | 1 | CR | Minor | wrong | disputed | 1 | 1 | other | no | Lint rule flags the whole lowercase string "sparkles". Author: intentional, icon names reach SymbolView indirectly; CR withdrew. |
| 24599 | 1 | MS | Medium | real-bug | fixed-before-merge | 3 | 4 | state machine | yes | After a pass, a read with an unread-approval placeholder plus a real failed or pending gate check leaves `passed` true, so recovery never wakes the thread. Fixed 5f30a39 (unverified in code). |
| 24599 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Placeholder-only read resets `failedChecks` and the no-checks timer, restoring the flapping. Fixed 4304491. |
| 24599 | 3 | CR | Major | real-minor | fixed-before-merge | 2 | 4 | state machine | maybe | Mixed partial read drops unread check state. The `failedChecks` part was later withdrawn (7b5c16c); the name-based approval part stands. Partly wrong. |
| 24599 | 4 | CR | Major | nit | fixed-before-merge | 1 | 1 | other | no | CI context-budget check fails by 37 bytes. Pipeline note, not a code defect. |
| 24599 | 5 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Absent `awaitingApproval` treated as `[]` in persistence equality. Fix later reverted by the follow-up that unified absent and empty (7b5c16c); remaining cost is one extra notice after upgrade. |
| 24599 | 6 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | error handling | no | Placeholder-only first read lets the no-check timer report "no checks" while the approval read is unavailable. Fixed 61ed921. |
| 24599 | 7 | MS | High | nit | disputed | 1 | 3 | state machine | no | Later distinct action-required checks on the same head are not reported. Author: single wake is the intended policy of issue #24575; Macroscope accepted. Rated High by bot, actual severity 1. |
| 23589 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Shown state not cleared when the desktop input stream ends. Author first declined, then fixed in e3992ab with a reattach re-send. |
| 23589 | 2 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | race/ordering | no | `shown: true` reported before the tab is acquired, ignored by PreviewManager. Fixed 70ee122 by gating on `clientSettingsHydrated`. |
| 13809 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Merged alias keeps `rateModel: "antigravity-unknown"`, so usage stays unpriced. Fixed 33bfddf with regression test. |

## 3. Track B (escaped bugs)

Trivial fix PRs skipped: #25422 (sparkles icon swap plus lint rule). #26570 is a prompt-wording change (traced below, low value).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 28353 | iOS Simulator screenshots fail on Xcode 26: the hub always passes a numeric `--display`, which Xcode 26's `simctl` rejects (issue #28035) | #10677 "feat(devices): add simulator and emulator support" (+9041/-98, 77 files, 2026-09-10) | medium (1 blamed line; the bug is an external tool version change, not a coding error) | missed (CR and Macroscope left 32 comments; none on `--display` or Xcode versions) | 3 | 5 | Depends on an external, later Xcode release; not visible from the diff. Poor replay candidate for a reviewer. |
| 28221 | Paragraph streaming hid the last paragraph while a provider kept the turn open on background work (issue #28175) | no usable SZZ target: blame lands on #2829 (72 lines, 380k-line orchestrator import), #29001, #31656 (batching, 14 lines) and a refactor #17427 | low | n/a (unknown origin) | 3 | 4 | Held-snapshot design from the original orchestrator; #31656 only touched batching. Not replayable. |
| 27791 | First usage-limit failure of a Codex run lost its reset time (empty `premium` notification), so recovery could not auto-continue (issue #27773) | #2829 (15 lines, noise); closest feature PR #25341 "sharing usage limits offer the existing recovery options" (+290/-58, 2026-11-05), low confidence | low | #25341: CR 2 comments about error classification, none on missing reset; missed | 3 | 4 | Needs knowledge of Codex protocol behavior. |
| 27677 | OpenCode `/command` turns were failed about 300 s in, when Node's fetch timed out waiting for response headers, while OpenCode kept running (issue #27664) | no SZZ target (pure addition). Likely origin #11519 "expose native slash commands across clients" (+1023/-103, 2026-09-16), low confidence, unverified | low | #11519: Macroscope left a High comment on command admission (adapter line 3249, a different failure); no comment on request timeout: missed | 4 | 4 | Undici 300 s header timeout is environment knowledge; hard to see from diff. |
| 26630 | Plain mouse-wheel over an expanded image zoomed instead of panning/scrolling | #10869 "feat(web): zoom and pan expanded images" (+251/-4, 2026-09-09); also #25246 (ref-callback refactor, 2 lines) | high | caught-and-ignored: CR Major "Preserve native scrolling for ordinary wheel input" (author: the PR requires wheel zoom, CR withdrew); Macroscope Medium on Ctrl-wheel suppression, author kept it | 2 | 1 | Design choice reversed 2 months later. Both bots saw it; not an escaped surprise. |
| 26570 | `preview_evaluate` description and shared instructions said page (WebMCP) tools only read, so agents refused user-requested writes (issue #26471) | #24850 "cut T3's agent instructions and tool copy by 60%" (+473/-794) for the tool copy; #32833 for one instructions line | medium | missed (no bot comment on that copy; unverified beyond the comment scan) | 2 | 4 | Wording regression from a copy cut; behavioral, evals-only detection. |
| 26374 | Antigravity install failed on a stale Windows Crashpad pipe | no SZZ target (pure addition, 4 lines) | n/a | n/a | 2 | 4 | Windows-only platform quirk. |
| 24599 | Fork workflows awaiting approval were reported as failed, and a later empty approval read made an unchanged head look green and repeatedly woke the agent (issue #24575) | #15057 "agents can watch a PR and get woken..." (+1531/-39, 31 files, 2026-10-03; 6 lines, treated `action-required` as failed); follow-ups #23904 (4 lines, pass gate) and #23863 | medium | #15057: missed (CR 6, Macroscope 14 comments, none on `action-required`); #23904: CR one Minor on required-vs-owed names, not this | 3 | 4 | Needs GitHub semantics (fork approval placeholder). |
| 23589 | Agents saw `visible: false` for a tab the desktop showed, and got a hidden tab as default when `tabId` was omitted (issue #17015) | #16956 "agent browser tools stop bloating history, fall back sensibly, respect ownership" (+743/-122, 2026-10-09; 3 of 4 lines) | medium | missed (Macroscope and CR left 7 comments on ownership, attachments; none on visibility) | 2 | 3 | Visibility was defined as `viewers.size > 0`; desktop shows tabs without a streaming viewer. |
| 13809 | Most Antigravity usage shown as Unpriced: model table stopped at Gemini 3.1 and effort suffixes were not stripped | #24834 "Gemini 4 Argon usage from Antigravity now has a price" (+66/-9, 2026-10-25), 2 lines | medium | bots did not comment (0 bot comments on #24834) | 2 | 3 | Data coverage gap; table lagged new models. |

## 4. Catalogue candidates (severity >= 3)

All are Track A, fixed before merge, except the last. base = PR base; head = the commit the bot commented on (still contains the bug).

- `codex-read-keeps-removed-windows`: #27791, a successful `account/rateLimits/read` must replace the published usage windows, because windows absent from the authoritative read otherwise stay as a stale exhausted allowance with a stale reset. Base `41443e5706c4605bc3efc17bcf431970488a146d`, head `d2dfacc071d1222fb5fa51207a599d6b0e6c9063`. Caught by Macroscope (High).
- `codex-notification-drops-read-reset`: #27791, when a notification updates an exhausted window without `resetsAt` while the first read is pending, reconciliation must keep the read's `resetsAt`, otherwise the terminal reset is null and auto-recovery never starts. Base `41443e5706c4605bc3efc17bcf431970488a146d`, head `ff265e82d4cab6d511585b1f8ee2334b8545ebf0`. Caught by Macroscope (High).
- `codex-read-wrong-plan-reset`: #27791, a pending quota read taken under the old plan must be rejected when the snapshot plan changed even if window values are unchanged, because a Plus reset gets attached to a Free snapshot and persisted in the recovery card. Base `41443e5706c4605bc3efc17bcf431970488a146d`, head `9d81fba410cad184e00a2ec8f369af78efaaccd4`. Caught by Macroscope (High).
- `paragraph-idle-tick-ends-ingestion`: #28221, in paragraph mode an idle tick can stop ingestion while a nested OpenCode continuation's events are still queued, because the pending-work probe returns false; the stop decision must honor the last stored root snapshot's pending flag. Base `402d0623d5f4160859607e9b7c11fc829fbe3e18`, head `c2eba7006f04559a2c998b307a1e84ae16f080ba`. Caught by CodeRabbit (Major).
- `pr-watch-pass-survives-unread-gate-failure`: #24599, a read with an unread-approval placeholder plus a failed or pending real gate check must clear a previous `passed`, otherwise the later recovery emits no `checks-passed` change and the thread is never woken. Base `20bb685e68fda77f60f9324f0db96d4ef06902d2`, head `873a9bce88949a9337c7f16762455ef32159356a`. Caught by Macroscope (Medium).
- `opencode-command-header-timeout` (Track B, escaped): #27677 fix; an admitted native `/command` turn is failed when the SDK request times out, although OpenCode keeps running. Introducing PR is unconfirmed (candidate #11519, low), so no replay head is given. Caught by: none at intro.
- `ios-screenshot-numeric-display` (Track B, escaped, low replay value): #28353 fix; screenshot capture must not pass a numeric `--display` on Xcode 26's `simctl`. Introducing PR #10677 (medium). Base `502131adff7494d1a1797b4fe518870f7e8431fd` (PR base at merge time, may have moved), head `3ed624aaf7e8f816817c239339e8c3a1fa91fcee`. Caught by: none.

## 5. Observations

- Macroscope's High-rated threads on #27791 (T4, T7, T8) were the best of the chunk: three distinct data-integrity defects in a quota reconciliation, each fixed with a regression row. CodeRabbit's matching thread there (T1) was withdrawn after a design argument.
- Bot severity labels over-state eval and policy threads: CR Major on #26570 (T3, T4) are eval-harness quality (actual severity 1-2); Macroscope High on #24599 T7 was a deliberate policy and was accepted as such.
- On #26630 both bots flagged the exact behavior that later needed a fix (#10869 wheel zoom). The author chose it deliberately and the bots withdrew or conceded; a reviewer that keeps the finding but rates it as design risk would have been right.
- #27677 is the only PR whose bot threads were all left unresolved at merge, including two Major ones (T1, T3) about request-failure handling after admission. Plausible but unreproduced.
- Escaped bugs here come from outside the diff (Xcode version, undici header timeout, Windows pipe, GitHub fork approval, new model names): none of the intro PRs got a bot comment on the defect.
