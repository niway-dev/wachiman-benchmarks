# Chunk 01: PRs #33109 .. #32498 (2026-11-08)

## 1. Header

- PRs covered: 25 (#33109 .. #32498). 18 have no bot thread.
- Bot threads: 10 total. CodeRabbit 6 (#33109, #33050, #32937, #32830 x2, #32503), Macroscope 4 (#32833 x2, #32830, #32777).
- Verdicts: real-bug 2 (same defect, #32830 T1 and T3), real-minor 5, nit 1, wrong 2 (#33109, #32937; the bot withdrew), unclear 0.
- Outcomes: fixed-before-merge 6 (#33050, #32830 x3, #32777, #32503), ignored 2 (#32833 x2), disputed 2 (#33109, #32937).
- Code checked: #32830 T1/T3 (read at the commented commit). Everything else is judged from thread text and replies, marked "(unverified)".
- Track B: 9 `fix` PRs touch non-trivial source (#33109, #33050, #32937, #32893, #32830, #32777, #32712, #32593, #32573). SZZ run on 8 (not #32593, a 483-line tab-strip rewrite, a layout refactor). Trivial (one line each, no SZZ): #32926 (1-line combobox prop), #32770, #32704, #32695, #32692, #32687, #32685, #32603, #32584 (web CSS and spacing), #32498 (mobile padding), #32777 (Windows spawn shim, tooling only, SZZ not worth it).
- Many PRs target a stack branch, not main: #32893 (redesign foundation branch, PR #28839), and the introducing commits of #32712 (`fa4d2e31` etc., redesign stack, unmerged commits, PR unknown). #16719 and #16337 merged into stack branches (`t3code/peer/links-ui`, `t3code/mcp/oauth-sign-in`), not main.

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 33109 | 1 | CR | Minor | wrong | disputed | 1 | 2 | other | no | CR: moving "No project" ahead of pinned projects for a scratch current thread. Team declined (intent of PR), CR withdrew. Resolved. (unverified in code) |
| 33050 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 2 | other | no | Docs tell Ubuntu 24.04/Debian 13 users to install distro `cargo`, too old for sysinfo 0.39.3 (Rust 1.95). Outdated, fixed in 8f89392 per reply. Docs only, build instruction, not a runtime bug. (unverified) |
| 32937 | 1 | CR | Major | wrong | disputed | 1 | 3 | state machine | no | CR: do not prefer an offline relay URL. Team: stable T3 Connect address is the intent. CR withdrew that part. (unverified) |
| 32833 | 1 | MS | Low | real-minor | ignored | 1 | 4 | other | no | Eval grader: unquoted heredoc records `$COLOR` unexpanded. Won't-fix reply, test tooling. (unverified) |
| 32833 | 2 | MS | Low | real-minor | ignored | 1 | 4 | other | no | Eval grader keeps stale file contents after `sed -i`. Won't-fix reply, test tooling. (unverified) |
| 32830 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Pending/failed title lookup returns `"Thread"`, which `resolveThreadLink` treats as proof the candidate exists, so a v1 link is routed to the message's environment instead of being guessed elsewhere. Verified at commit f54e7cf3db (mobile `entities.ts` lines 72-73 return "Thread" when lookup is not success; `known = candidates.find(title !== null)` at resolveThreadLink). Author: "Confirmed and reproduced", regression added. |
| 32830 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Mobile title lookup not refreshed after shell removal. "Addressed in be177ec". (unverified) |
| 32830 | 3 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Same defect as T1 (provisional "Thread" title as existence proof). Outdated, fixed. Duplicate of T1; CR and Macroscope both found it. |
| 32777 | 1 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Test mirrors mocked spawn call; asked to remove. Removed in 2da1430. |
| 32503 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | After an executable `agy_acp_server` without harness, PATH search stopped, hiding a valid install. Outdated, "Addressed in a7bedbe". (unverified) |

## 3. Track B (escaped bugs)

| fix PR | bug | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 33109 | Cmd+Shift+O ("New thread in") lists a pinned project above the current one; Enter starts the thread in the wrong project | #26154 (pin favorite projects; +1367/-256, 68 files, merged 2026-10-31, main). SZZ: #26154 5 lines in `sidebarProjectGrouping.ts` | medium | missed (CR even asked for the opposite: "Preserve pinned-first order in the web pickers" in `projectGrouping.ts:255`; team declined that thread) | 2 | 2 | A product-intent mismatch more than a defect. Second SZZ candidate #22699 (2 lines, refactor) is noise. |
| 33050 | Linux ARM64 desktop builds skipped server bytecode prep | #32987 (perf, merged the same day, 4 lines) | low | bots-did-not-run (no threads on #32987) | 2 | 1 | A deliberate platform guard that was widened, not an accident. #22428 is CI noise. |
| 32937 | "Copy MCP URL" copied a LAN/localhost route instead of the T3 Connect address | #16337 (feat copy MCP URL; +120/-0; base `t3code/mcp/oauth-sign-in`, a stack branch, merged 2026-10-06). SZZ: #16337, #16909, #19559 (comment-prune refactor, noise) | medium | bots-did-not-run on line comments (no inline threads on #16337; only summary comments) | 2 | 2 | The old route order was the original design; the fix changes policy. Unmerged-stack note: introducing PR merged into a stack branch. |
| 32893 | Mobile thread-list timer printed `1m 34s`, web `1m` | redesign foundation commits `4889acdc600` (feat(web): establish redesign primitives and shell) and `7099ac13572` (restore main sidebar rows) | low | not checked (stack branch commits, PR number not resolved) | 1 | 1 | Cosmetic format mismatch. Stack branch (#28839), SZZ lands on unmerged stack commits. |
| 32830 | Existing threads rendered as "Thread no longer available" when absent from the loaded thread list | #26239 (thread links name their environment and never a title; +427/-185, merged 2026-10-28, main). SZZ: #26239 16 lines (mobile+web link code) | low | #26239 had 3 CR threads (instructions, evals), none on link resolution: missed | 3 | 4 | Fix is closer to a feature (new metadata read). Other candidates #17017, #18310, #21505 are earlier link work. |
| 32712 | Plain sidebar click replaced the focused side panel tab (Diff, Files) instead of the chat's tab, opening the thread as a split | `fa4d2e31` fix(layout): reuse focused launchers when opening content (maria-rcks, 2026-10-31; same subject exists as 3 commits on redesign stack branches) | low | not checked (stack commits, PR not resolved) | 2 | 3 | One blamed line. Lands on unmerged stack commits. |
| 32593 | Pane tabs truncated labels and strip did not scroll | not traced | n/a | n/a | 2 | 3 | 483-line removal, mostly a layout rewrite (UI). |
| 32573 | A blocking delegated-task read could return after the parent run ended and acknowledge the result with no observing run, consuming the completion so the idle parent was never woken | Origin is `observedByRunId: null` acknowledgement from the orchestrator import #2829 (noise) as extended by #17696 and #20310; SZZ's other candidate #16719 (delegate_task to a linked environment; +5156/-322, base `t3code/peer/links-ui`, a stack branch) only changed the provider-instance filter | low | #16719 had many threads (peer RemoteDelegation, follow, stop) but none on late-read acknowledgement: missed. #2829/#17696 not checked | 3 | 5 | Race between run end and late read; needs cross-file knowledge of delivery ownership. Pre-existing from the import, not a clean introducing PR. |

## 4. Catalogue candidates

1. `thread-link-provisional-title-as-existence` (PR #32830, Track A fixed before merge). Golden: the mobile title atom returns the fallback "Thread" while the metadata read is pending or failed, and `resolveThreadLink` treats any non-null title as proof the candidate exists, so a v1 link whose thread lives in another environment is routed to the message's environment instead of being guessed. Base `20fcc6ca57195cf9180114387e4f659d8e1ee2b4`, head `f54e7cf3db0def7e4e5b12e05401e7ae9966d9ae` (the commit both bots commented on). Caught by: Macroscope (High) and CodeRabbit (Major).
2. `late-delegated-read-consumes-wake` (PR #32573, Track B escaped). Golden: a delegated-task read made after the spawning parent run ended acknowledges the completion with `observedByRunId: null`, which consumes it and leaves the idle parent with no wake; late reads must keep delivery ownership and offer a wake. Replay target is the fix parent (introducing PR unresolved, pre-existing from #2829 and later PRs): base `564b2f96b21076353c334a82eaf7af6e60781f60`, head `b76a5958890f8d1dbcc150e1d435a3dced222202`. Caught by: none (found by the author while testing, per PR body). Severity 3, lowish confidence the bug is reviewable from a single introducing diff.

## 5. Observations

- Only 2 of 10 bot threads were disputed (the team declined, the bot withdrew after an explanation), many from an AI author replying "on behalf of" a human. CodeRabbit withdrew its finding in both disputes (#33109, #32937).
- The one repeated real bug (#32830) was found by both bots within the same PR; Macroscope rated it High and CodeRabbit Major, matching my severity 3.
- CodeRabbit asked for the pinned-first order on #26154, the behavior #33109 later reversed; bots can endorse the behavior that later gets fixed.
- On #16719 (5156 added lines) the bots left about 25 threads and none touched the later-escaped delivery race; large PRs get many findings but miss ownership/ordering contracts.
- Macroscope's two "Low" threads on the eval grader (#32833) and its test-mirror rule on #32777 are style/tooling items; team ignored or fixed without a code defect.
