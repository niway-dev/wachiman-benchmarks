# Chunk 01: PRs #34490..#34139 (2026-11-11)

## 1. Header

- PRs covered: 25 (#34490 .. #34139). 16 have no bot thread at all.
- Bot threads: 32 total. CodeRabbit 24, Macroscope 8.
- Verdicts: real-bug 5, real-minor 22, nit 3, wrong 0, unclear 2.
- Outcomes: fixed-before-merge 19 (#34141 x12, #34181 x3, #34168 x2, #34176, #34204 T1), ignored/no reply 13, disputed 0.
- Code checked at the merge commit: #34204 (T3/T4), #34176 (T1). All other verdicts come from thread text, replies and resolved/outdated flags (unverified in code unless stated).
- Track B: 19 `fix` PRs, 10 touch non-trivial source. SZZ run on 9 (2 returned "pure addition"). Time: about 25 minutes.
- Caveat: raw.jsonl `head` for #34141 is b368b819c9, but the PR kept changing after that (dfc152bd4a). Replay should use the real final head (unverified which).

## 2. Track A (bot threads)

Outcome evidence: "reply" = author reply says fixed; "outdated+resolved" = flags; "none" = unresolved, no reply, merged anyway.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | one-line finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 34245 | 1 | CR | Minor | real-minor | ignored | 2 | 3 | cross-file contract | no | tool_search can list tools the caller cannot call (EnabledWhen not applied). Unresolved, merged (unverified in code). |
| 34245 | 2 | CR | Minor | real-minor | ignored | 2 | 3 | cross-file contract | no | Deferred Copilot session does not advertise link_pull_request though instructions demand it as next call. Unresolved (unverified). |
| 34245 | 3 | CR | Minor | nit | ignored | 1 | 2 | other | no | list_changed broadcast on repeated query; harmless re-list. |
| 34227 | 1 | CR | Major | nit | ignored | 1 | 1 | other | no | Asks for a test that the removed flag is rejected. Test-coverage request, not a defect. |
| 34218 | 1 | CR | Minor | real-minor | ignored | 2 | 4 | state machine | maybe | Checkout marker compared with latest discovered PR; with several completed PRs on one branch the explicitly checked-out older PR is dropped (unverified). |
| 34218 | 2 | CR | Minor | real-minor | ignored | 3 | 4 | state machine | maybe | Branch-level marker exempts every later thread on that branch, restoring the historical-PR inheritance the PR fixes (unverified). |
| 34218 | 3 | CR | Minor | real-minor | ignored | 2 | 3 | data integrity | no | Bitbucket listings lack completion timestamps so the guard accepts old PRs (unverified). |
| 34218 | 4 | CR | Minor | unclear | ignored | 2 | 4 | race/ordering | no | PR opened after thread settles may lose its badge when later merged (unverified). |
| 34208 | 1 | CR | Minor | real-minor | ignored | 1 | 2 | error handling | no | Retry also fires on 404, adding 1 s per stale URL. Reasonable, unresolved. |
| 34205 | 1 | CR | Minor | real-minor | ignored | 1 | 3 | error handling | no | Regex can match parse-error phrase quoted inside a valid selector value, misclassifying ambiguous as invalid. |
| 34204 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Wants a real-recorder test. outdated+resolved, "Addressed in f5f438f". |
| 34204 | 2 | CR | Minor | real-minor | ignored | 2 | 3 | resource leak | no | Pending clipboard entries unbounded while a read stalls (each up to 1 MiB, CLIPBOARD_TEXT_LIMIT at line 429 confirmed in merged file; unbounded growth not exercised). |
| 34204 | 3 | CR | Major | unclear | ignored | 3 | 5 | race/ordering | no | Cut text lost if navigation destroys document before a queued read runs. Plausible; the merged code awaits `tab.copyReads` only inside the read chain (line 2479-2483), but navigation interaction not traced. |
| 34204 | 4 | CR | Major | real-minor | ignored | 2 | 4 | race/ordering | maybe | Verified in merged code (ServerBrowser.ts:2461-2462): `while (Date.now() <= tab.copyKeyedUntil) await sleepUntil(copyKeyedUntil+1)`. A backward clock step stalls the key handler for the step size. Real, but rare; rated Major by bot, actual severity 2. |
| 34181 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI state | no | Quote-only messages cannot collapse. outdated+resolved, "Addressed in 4841735..2589f5e". |
| 34181 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Client find-highlight text and server count diverge across quote card. resolved, fixed. |
| 34181 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | data integrity | no | Selection inside one quote text node copies without citation source. resolved, fixed. |
| 34176 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | yes | Gateway-version rewrite also hid a genuine "upgrade CLI" error because the required version was not compared. Outdated; merged file (399df485a4:ClaudeAdapterV2.ts:4113-4128) now captures `required` and checks `sessionVersion >= required`. Verified. |
| 34168 | 1 | MS | Medium | real-bug | fixed-before-merge | 3 | 4 | UI state | yes | Fold choices stored as toggles relative to the Viewed default flip when Viewed state loads late. Author reply: fixed in a96349169f (absolute per-file map). |
| 34168 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 2 | UI state | no | "Expand all" ignored when files viewed. Outdated; reply: fixed in a5b7e6453c. |
| 34141 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Final shell output truncated after 4 pages x 64 KiB on exit. Outdated+resolved, reply: five-page regression added. |
| 34141 | 2 | MS | High | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | Shell-removal error aborts `stopBackground`, so parent session is never interrupted. Resolved, reply: per-shell catch + test. Duplicate of T9. |
| 34141 | 3 | MS | Low | real-minor | fixed-before-merge | 2 | 2 | data integrity | no | Failed shell lost exitCode. Reply: fixed, exit code 7 test. |
| 34141 | 4 | MS | High | real-bug | fixed-before-merge | 3 | 5 | cross-file contract | yes | Cold-resume recovered shells never projected to a turn item. Took 3 bot rounds (null runId dropped by server routing, then idle case); each partial fix refuted by Macroscope, final dfc152bd4a. Strong example of bot value. |
| 34141 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | error handling | no | `shell.output` read without timeout holds global lock. Reply: INVENTORY_TIMEOUT added. |
| 34141 | 6 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | error handling | no | `shell.remove` unbounded. Fixed with timeout. |
| 34141 | 7 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | One failed lookup aborts whole recovery loop. Fixed per-shell. |
| 34141 | 8 | CR | Minor | real-bug | fixed-before-merge | 3 | 4 | race/ordering | yes | `recoverShells` mutates shared shell map without the adapter lock; concurrent poll can duplicate output. Reply: lock added. |
| 34141 | 9 | CR | Minor | real-bug | fixed-before-merge | 3 | 4 | race/ordering | no | `stopBackground` runs `stopShell` outside the lock and propagates its failure (same root as T2 plus a lock race). Fixed. |
| 34141 | 10 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | race/ordering | no | Poll holds global lock during up to six serial network reads (about 30 s stall). Fixed in dfc152bd4a. |
| 34141 | 11 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Stale `sessionScopedBackground` on child drops updates. Fixed b368b819c9 with test. |
| 34141 | 12 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | resource leak | no | Interrupted recovery leaves shells in roster without turn item. Fixed b368b819c9. |

## 3. Track B (escaped bugs)

Fix PRs skipped as trivial or non-source: #34417 (test flake), #34326 (CI retry, no SZZ), #34258 (mobile layout offset), #34191 (test), #34178 (CSS outlines), #34170 (test removal), #34140 (spacing), #34182 (hide empty replies, small UI), #34176/#34168 (feature-adjacent UI/error text; see track A, no SZZ run).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 34331 | `coverMerges` recursed once per chained merge, so a long chain of merged cells overflows the stack and crashes spreadsheet selection | #21362 "feat(web): preview office files, fonts, and mermaid diagrams" (+8370/-93, 54 files, merged 2026-10-26); 17 of 17 blamed lines | high | missed (CR and Macroscope each left 10+ comments incl. many on sheet code; none on recursion) | 3 | 3 | Giant PR; the recursive `coverMerges` is visible in one hunk with a code comment "A merge ... can touch another". |
| 34243 | Zero-credit cap window ("individual") marked seat-based Codex plans out of usage | #26164 "feat: fall back when the default provider is out of usage" (+763/-37, merged 2026-10-29) | medium (1 blamed line only; the missing `codex` case is logically that PR's feature) | missed (Macroscope: 14 reviews on this PR about other providers' windows; nothing on codex seat plans) | 3 | 4 | Needs provider-specific domain knowledge about how windows are reported. |
| 34218 | New threads on a reused branch inherited an old merged/closed PR (issue #31896) | #10101 "fix(server): link thread PRs without an open client" (+2309/-1486, 2026-09-06) | medium (5 of 15 lines; #2829 orchestrator rewrite has 8, but that PR is a 380k-line megapatch) | missed (Macroscope: 7 comments on #10101 about GitLab, race and docs; none about historical PRs) | 3 | 4 | Semantic gap: "latest PR for branch" lacks a "created after thread" check. |
| 34208 | One dropped network probe listed a live linked peer as unreachable (retry fired immediately) | no SZZ target (pure addition) | n/a | n/a | 2 | 3 | Best guess PeerLinks probe from the peer-link feature (#17129, unverified). |
| 34205 | Playwright "strict mode violation" (ambiguous selector) reported as invalid selector | #15328 "feat(preview): run the browser on the environment server" (+13552/-7701, 2026-10-06) | high (3 of 3 lines) | missed (Macroscope: 12+ comments on ServerBrowserPage, none on error classification) | 2 | 3 | Misleading error text, not wrong behaviour. |
| 34192 | An SSH password prompt that ended (timeout/cancel) stayed on screen, later prompts stacked behind it | #25239 "fix(web): SSH password prompts wait for their dialog, and the app shell drops its sync effects" (+334/-277, 2026-10-26) | medium (5 of 8 lines) | missed (CR only commented on a live-region nbsp; 2 comments) | 2 | 4 | Needs IPC lifecycle knowledge (main process never told the renderer the request settled). |
| 34177 | Collapsed turn shows several "context compacted" dividers instead of one | #24334 "feat: compactions T3 Code starts read as one working row" (+1375/-82, 2026-10-24) | medium (2 lines) | missed (Macroscope flagged duplicate IDs for retried /compact, CR flagged hiding the only compaction row; neither the multiple-divider outcome) | 1 | 2 | Cosmetic. |
| 34163 | Auto-mode thread sends did not queue while a turn was stopping (missing `deliveryIntent: "auto"`) | no SZZ target (pure addition) | n/a | n/a | 3 | 4 | Behaviour lives in another file (queueing logic); the omission is only visible by knowing the consumer (unverified). |
| 34139 | A link request named a machine from whatever answered at an arbitrary address (unconfirmed identity; loopback addresses offered) | #17129 "feat: an agent sets up a link to another environment" (+4642/-122, 62 files, 2026-10-27) | high (34 of 36 lines) | missed (bots flagged 5+ other defects incl. a plaintext-redirect issue and Connect-URL omission; not address trust) | 3 | 4 | Trust/UX design flaw; Macroscope came near it (linkRequest.ts:81) but argued the opposite direction (include more URLs). |
| 34245/34227 | Copilot token bloat / unused CLI flag | n/a | n/a | n/a | 1-2 | 1 | Not bug escapes (perf and API polish); no SZZ. |

Bot coverage on the 9 SZZ-checked bugs: caught 0, missed 7 (34331, 34243, 34218, 34205, 34192, 34177, 34139), n/a 2.

## 4. Catalogue candidates (real bugs, severity >= 3)

| id | PR(s) | golden description | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| opencode-cold-resume-shell-not-projected | #34141 | After a cold `resumeThread`, shells recovered by `recoverShells` have no turn/toolId so their output and completion are never emitted to a turn item (or are routed with a null runId), leaving the command activity stuck running. | b3fdf2b10fb92e5dbc71a83381c602a8a464bbca | b368b819c98130cc7009d7d8cc21597e9f16012e (earlier head than final) | Macroscope (iterated 3 rounds) |
| opencode-stop-background-aborts-on-shell-error | #34141 | `stopBackground` awaits `stopShell` per shell with no error handling and outside the adapter lock, so one failed shell removal aborts `interruptTurn` and the parent session and remaining subagents are never interrupted. | b3fdf2b10fb92e5dbc71a83381c602a8a464bbca | b368b819c98130cc7009d7d8cc21597e9f16012e | Macroscope + CodeRabbit |
| opencode-recover-shells-outside-lock | #34141 | `recoverShells` mutates shared shell state and roster without taking the adapter lock, so a concurrent poll or exit event can duplicate output or leave `shells` and the roster inconsistent. | b3fdf2b10fb92e5dbc71a83381c602a8a464bbca | b368b819c98130cc7009d7d8cc21597e9f16012e | CodeRabbit |
| pr-viewed-fold-toggle-relative-to-default | #34168 | Per-file fold state is stored as toggles relative to the current Viewed-derived default, so a late or changed Viewed state flips the reader's explicit fold choice. | ed52af3a478652c55aeaaf5a64bbf6584dd6a0b4 | 9c174f7f355af036631a089e30946acf37827814 | Macroscope |
| sheet-cover-merges-stack-overflow | #21362 (fixed by #34331) | `coverMerges` recurses once per chained merged range, so a long chain of merges overflows the stack and crashes the spreadsheet selection. | e856833a66e8663316645776a1c101644beb4a32 | ab0039944e8fb1004cb80eca2a2dd8054665ec2b | none (human fix 15 days later) |
| usage-fallback-codex-seat-plan-credit-cap | #26164 (fixed by #34243) | The exhausted-window check treats the zero-credit "individual" cap window as exhaustion for seat-based Codex plans that have primary/secondary windows, wrongly marking Codex out of usage and triggering fallback. | 5eebf77b373b719ca4456985340707afa267310e | ced10aa2804601542c7490b1d2065e82b4df499a | none |
| thread-inherits-historical-branch-pr | #10101 (fixed by #34218) | A new thread on a reused long-lived branch is associated with the latest merged/closed PR for that branch even though the PR finished before the thread existed. | 5fa35d211682ee02e34fba0711838ca431ed003b | 03c0d05e109a3e887e27a5036cbaf068c556b764 | none (low confidence on the introducing PR) |
| link-request-names-machine-from-unverified-address | #17129 (fixed by #34139) | A link request for an arbitrary address takes the machine's name from whatever answers at that address, so the approval card can show a machine identity the app cannot confirm; loopback addresses are also offered as another machine's address. | b7b14bfdd858c359c8f4f541d5227f3d7a8d6051 | 6edd16995f3dff11e1a76ecdd1f73f80db330648 | none |

Also borderline (sev 3 but only a partly verified claim, not promoted): #34204 T3 (cut text lost on navigation, Major by CodeRabbit, unclear).

## 5. Observations

- Macroscope is the stronger finder of real defects in this chunk: on #34141 its High findings (stop aborts, cold-recovery projection) were correct, and it re-checked the author's fixes and refuted two incomplete ones. Its verdict reliability on the rest is untested (unverified), and its replies to "fix it" requests return "no permissions".
- CodeRabbit leaves many Minor threads on every PR (24 of 32 here). Most are plausible robustness points, but 13 were left unresolved and merged, including genuinely design-level ones (#34218 T2 marker scope). The team mostly ignores them unless the PR author is an AI-assisted loop (#34141, #34181) that replies to each.
- CodeRabbit severity labels are inflated: the two "Major" threads on #34204 were an unlikely clock-rewind stall (real severity 2) and a speculative navigation race; the "Major" on #34227 was a test request.
- Escaped bugs: in 7 of 7 SZZ-resolved cases neither bot commented on the defect at introduction, even on PRs with 10-30 bot comments (#21362, #17129, #26164). Misses are domain-semantic (Codex plan windows, branch-PR lifecycle, IPC lifecycle) or large-PR dilution, not syntax.
- Fixes land fast on bot findings in the author-owned PRs but the bug-to-fix gap for escapes ranges 2 weeks (#21362 to #34331) to 2 months (#10101 to #34218), suggesting escapes are found by users, not reviewers.
