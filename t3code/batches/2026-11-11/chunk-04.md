# Chunk 04: PRs #29151..#26963 (2026-11-11)

## 1. Header

- PRs covered: 25 (#29151 .. #26963). 11 have bot threads, 14 have none.
- Bot threads: 24 total. CodeRabbit 20, Macroscope 4.
- Verdicts: real-bug 0, real-minor 12, nit 8, wrong 2, unclear 2.
- Outcomes: fixed-before-merge 8, ignored 13, disputed 2 (bot withdrew both: #28459 T1, #27953 T1), unknown 1.
- Code checked at the merge commit: #28056 T1, #27275 T1. Everything else is judged from thread text, replies and outdated/resolved flags (unverified in code).
- Track B: 22 `fix` PRs, 21 non-trivial (#27335 trivial: one-line swipe label fix). SZZ run on 21; 2 returned no target (#27192 pure addition, #28195 only a 1-line refactor hit). Bots at the introducing PR: 0 caught, 19 missed or silent (checked by keyword grep of bot comments, so "missed" means no comment on the defect found).
- Caveats: SZZ often lands on `#2829` (a 1912-file orchestrator rewrite) or on a refactor that only moved the line. Those are marked low confidence. Several introducing PRs have higher numbers than the fix chunk because PR number is not merge order.

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 28957 | 1 | CR | Minor | nit | ignored | 1 | 2 | other | no | Windows backslash in an include path in a test fixture. Test only (unverified). |
| 28732 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI state | no | Label description tooltip not reachable by keyboard. Reply: fixed in f812f2013b, CR confirmed. |
| 28732 | 2 | CR | Major | nit | fixed-before-merge | 1 | 1 | other | no | Asks for a Forgejo mapping test. Test coverage request, added. |
| 28543 | 1 | CR | Major | nit | ignored | 1 | 1 | other | no | Asks for a reachable-alternate-address test. Not a defect. |
| 28543 | 2 | CR | Minor | nit | unknown | 1 | 1 | other | no | Join the listing fiber in a test. Outdated, no reply (unverified). |
| 28459 | 1 | CR | Minor | wrong | disputed | 1 | 1 | other | no | Windows root path label. Author: worktrees are never at a root. CR withdrew. |
| 28219 | 1 | CR | Major | real-minor | ignored | 2 | 4 | cross-file contract | maybe | Without Command Line Tools the macOS git shim starts and exits nonzero, so it is a command failure, not a NotFound spawn, and the new "Git isn't installed" message never shows (unverified: did not read resolveMacosGit, blobless clone too slow). |
| 28195 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Recovery item id changes on retry after a failed event write, so the handoff lands after the user message. Outdated, no reply (unverified). |
| 28195 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Divider model taken from a run that never started. Outdated (unverified). |
| 28195 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Interruption during ensureThread leaves a handoff item for a run that never runs. Outdated (unverified). |
| 28056 | 1 | CR | Major | real-minor | ignored | 2 | 3 | data integrity | maybe | Staleness guard compares only the tail length, so an edited line after the last hunk is hydrated as unchanged context. Verified in merged diffFileContents.ts `reproducesPatch`: hunk lines are compared, omitted regions only by count. Rare (needs an edit that keeps line count). |
| 27953 | 1 | CR | Minor | wrong | disputed | 1 | 3 | race/ordering | no | Activity rate limit hidden by later detail failure. Author: order-dependent before, detail failure is real. CR withdrew. |
| 27953 | 2 | CR | Minor | unclear | ignored | 2 | 3 | state machine | no | Re-arm notice should require activity recovery. Wording-level, no reply (unverified). |
| 27953 | 3 | CR | Minor | unclear | ignored | 2 | 3 | state machine | no | Same for detail reads. Duplicate of T2 (unverified). |
| 27564 | 1 | CR | Minor | real-minor | ignored | 2 | 3 | security | no | Raw CLI response and log path go into `DeviceHostUnavailableError.reason`. Unresolved (unverified). |
| 27564 | 2 | MS | n/a | nit | ignored | 1 | 1 | other | no | Fold a duplicate test into the existing one. |
| 27564 | 3 | MS | n/a | real-minor | ignored | 2 | 3 | security | no | Same as CR T1 (keep reason bounded, details in cause). Duplicate. |
| 27490 | 1 | CR | Minor | nit | ignored | 1 | 1 | other | no | Regression test request. |
| 27484 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | yes | Unread saved channel treated as Stable disables a valid confirm. Reply: fixed in 6c6fab6 (null until known). |
| 27387 | 1 | CR | Minor | real-minor | ignored | 2 | 5 | race/ordering | maybe | Wake-upgrade decision split between finalizer and an explicit step; cancel in the gap leaves `settled_only`. Author said nothing; narrow window (unverified). |
| 27275 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 4 | race/ordering | maybe | Baseline session and update RPC session read separately. Merged code (server.ts ~878) reads the session once via `acceptingSession` and rides it; comment states this. No reply, so fixed by code evidence only. |
| 27275 | 2 | MS | n/a | nit | ignored | 1 | 1 | other | no | Move assertion into existing test. |
| 27275 | 3 | MS | n/a | nit | ignored | 1 | 1 | other | no | Remove duplicate test case. |
| 27192 | 1 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | state machine | no | `preparing` runs get a "provider work interrupted" notice though nothing started. Outdated, no reply (unverified). |

## 3. Track B (escaped bugs)

| fix PR | bug | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 29151 | Links in mobile question cards did nothing (all sent to the PR opener). | #19197 "make links in agent questions clickable" | medium | no bot comments on it | 2 | 2 | Same feature, missed file links. Only 2 lines blamed. |
| 29051 | Japanese/Chinese/Korean text in docx/pptx viewer rendered as boxes. | #21362 "preview office files, fonts, mermaid" | high | missed (50 bot comments, none on the CJK stub alias) | 2 | 4 | Build alias stubbed the CJK font package. |
| 28957 | Git failure (bad .git/config) read as "not a repository" / "ref absent"; checkpoints silently `missing`. | #27103 "git status in parallel, 3x fewer git processes" | medium | missed (Macroscope High and CR on other lines of the same function: newline paths, cached null) | 3 | 3 | Probe rewrite by #27103; older lines from #2829. |
| 28918 | Text generation fell back to a disabled default instead of an enabled custom one. | #26164 "fall back when default provider is out of usage" | medium | missed (14 comments, none on this) | 2 | 3 | |
| 28543 | Listing linked environments probed addresses serially, 10 s each. | #29779 (7 lines), originally #16655 | low | no bot comments on #29779 | 2 | 2 | Performance, not correctness. |
| 28258 | Missing npm reported as a generic failure. | #20377 "report missing Node on SSH device hosts" | low | missed (1 CR comment, other topic) | 2 | 2 | Sibling case of the same error mapping. |
| 28219 | New project without Git said "failed to create folder". | #2829 (1 line) | low | not checked | 2 | 2 | Mega-PR, not informative. |
| 28195 | Silent history replacement on failed provider resume (new notice). | no SZZ target | n/a | n/a | 2 | n/a | Mostly additive. |
| 28084 | Assistant message ids over 512 chars broke citations (raw link in composer). | #9146 "cite assistant responses" | high | missed (Macroscope Medium on hash length, adjacent, not the id cap) | 2 | 3 | Schema cap never checked against Pi id growth. |
| 28056 | Expanding diff after files changed throws and crashes the app to the root error screen. | #18124 "guided reviews" (GuideExcerpt expand) | medium | missed (36 comments, none on stale contents) | 3 | 5 | Depends on third-party hydration contract. |
| 27953 | Closed PR watch with failing activity read never ended; agent re-armed it in a loop. | #29450 "keep PR watches active after host failures" | high | missed (CR flagged a neighbouring co-failure ordering case at line 498; fixed, but not this one) | 3 | 4 | A fix of a fix. |
| 27595 | Rate-limited host blocked opening a PR; `Interactive` overwritten with false. | #6466 "protect provider API budgets" | low | missed (19 comments, none on Interactive) | 2 | 3 | |
| 27588 | `t3_project_clone` inherited a 120 s clone deadline. | #11762 "clone in background" | low | missed (Macroscope High flagged the opposite: null timeout removes the deadline) | 2 | 2 | Intro uncertain. |
| 27564 | Simlock open failures hid the CLI's reason. | #25259 "lease simulators from Simlock pool" | medium | missed (14 comments, none on diagnostics) | 2 | 2 | |
| 27490 | Mobile web thread controls drew over the sidebar sheet (z-index). | #18193 / #23072 / #22706 | low | no bot comments on #18193 | 2 | 2 | |
| 27484 | Track switch dialog offered a switch that moves nothing. | #26288 "switch fleet between Stable and Nightly" | medium | missed (Macroscope High on a related saved-channel skip, different bug) | 2 | 3 | |
| 27387 | Steer during `delegate_task` wait dropped the child result (`settled_only` forever). | #16719 "delegate_task to a linked environment" (#2829 42 lines) | low | missed (40 comments, none on steer) | 3 | 5 | Ordering across cancel, wake and settle. |
| 27335 | Swipe labels wrap on large Android text. | trivial | n/a | n/a | 1 | 1 | Skipped. |
| 27275 | Update wait lasted 32 min when host returned without this update's outcome. | #2978 / #5181 | low | missed (not examined in depth) | 2 | 4 | |
| 27192 | Runs cancelled by restart gave no reason in thread (new notice). | no SZZ target (pure addition) | n/a | n/a | 1 | n/a | |
| 26992 | PR search dropped partial-word matches once GitHub answered. | #22727 (refactor moved the code; origin #21514) | low | no bot comments on #22727 | 2 | 2 | |
| 26963 | SSH reconnect trusted `kill -0` on a stale pid; 60 s hang, and disconnect SIGTERMed an unrelated process. | #19432 "reconnecting keeps remote server running" | medium | no bot comments | 4 | 4 | Introduced the pid-file reuse design. |

## 4. Catalogue candidates (real bugs, severity >= 3)

No Track A thread qualifies (no real-bug verdict). These come from Track B and are replays of the introducing PR.

| id | PR(s) | golden | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| git-failure-read-as-no-repo | #27103 (fix #28957), medium conf | A git command that fails for a reason other than "not a repository" (corrupt .git/config, exit 128) is treated as no work tree or absent ref, so checkpoints are recorded `missing` with no error. | 08a463e299 | e55bf3e978 | none |
| ssh-stale-pid-wrong-process | #19432 (fix #26963), medium conf | The launch and stop scripts trust `kill -0 <pid>` on a saved pid file, so a reused pid makes reconnect hang 60 s and disconnect SIGTERMs an unrelated process. | 8414d16819 | 4572c6bec9 | none |
| pr-watch-closed-rearm-loop | #29450 (fix #27953), high conf | When a PR is closed but its activity read keeps failing, the closed detail is ignored and the watch gives up with a "watch again" notice, so the agent re-arms it forever. | c8a601c0df | 793be57c3d | none |
| diff-expand-stale-contents-crash | #18124 (fix #28056), medium conf | Expanding unchanged context loads current file contents without checking they still match the patch, so hydration throws and the app crashes to the root error screen. | 8d199b4f7b | 9196ac4064 | none |
| delegate-wait-steer-drops-result | #16719 (fix #27387), low conf | A steer cancelling a `delegate_task` wait leaves the task `settled_only`, so the child result is never delivered after the parent run settles. | 78c084ad41 | b7b14bfdd8 | none |

## 5. Observations

- Zero of 19 traced escaped bugs had a bot comment on the defect in the introducing PR (keyword grep; "unverified" for anything not read). The bots comment heavily (50 on #21362, 40 on #16719) but on other lines.
- Most bot threads here are test-coverage requests or notice wording (8 nits, 2 unclear); no thread rated real-bug. CodeRabbit "Major" is mostly "add a test" (#28732 T2, #28543 T1).
- Macroscope's two duplicates (#27564 T3, #27275 T2/T3) are Test Signal or convention checks; its higher-severity finds in the intro PRs (#25259, #26288) are real but unrelated to the later fixes.
- Bots withdrew findings when the author gave a reason (#28459, #27953 T1, #28732): replies work and the bot does not argue back.
- Many fixes are "a fix of a fix" or a new notice (#27953, #28195, #27192): the author (mostly one person, with an AI co-author) reproduces each bug first, so the bug list is reliable even though SZZ is noisy.
