# Chunk 02: PRs #34132..#33058 (2026-11-11)

## 1. Header

- PRs covered: 25 (#34132 .. #33058). 10 have no bot thread (#34121, #34050, #33985, #33966, #33900, #33745, #33396, #33395, #33352, #33129).
- Bot threads: 51 total. CodeRabbit 32, Macroscope 19.
- Verdicts: real-bug 14, real-minor 29, nit 6, wrong 0, unclear 2.
- Outcomes: fixed-before-merge 40, ignored/no reply 11 (#34048 x2, #34030 x3, #33989 T4, #33641, #33479, #33439 x2, #33130 T4), disputed 0.
- Many threads are duplicates (Macroscope and CodeRabbit flagging the same defect): #33783 T1/T2, #33680 T1/T2, #33548 T1/T2, #33130 T1/T3, #34089 T5/T6 partly.
- Code checked: #34030 T1 (`UsageService.ts` at c03f84bcde, lines 382-440). Everything else is judged from thread text, author replies naming the fix commit, and resolved/outdated flags, so it is "(unverified)" in code unless stated. Author replies often name a failing regression test, which counts as team confirmation.
- Track B: 19 `fix` PRs. Trivial or not traced: #34113 (scroll offset), #33989 (feature-sized, see Track A). SZZ run on 17; #33641 returned "pure addition"; #33130 not run (173 additions, 0 deletions). #33129 returned a diffuse list (20+ PRs). Bots caught the escaped defect at the introducing PR: 0 of 15 traced; missed: 15 (2 with an adjacent comment on the same code).
- Caveat: the Macroscope and CodeRabbit "I could not verify the fix" replies on #33783, #33680, #33548, #33130 are bot sandbox lag (they inspected an older head), not evidence that the fix is missing (unverified).

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 34132 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | resource leak | no | Scan-cache hit path skipped `RcRef.get`, so repeated queries did not reset the idle minute. Reply: fixed in 2a8b4c96e5c with test. |
| 34113 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Asks for before/after screenshots in the PR body. Author added them. |
| 34096 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Hard-linked model install is shown as a download (Delete not Unlink). Fixed 593ec1f8cf0 via `.source` file. (unverified) |
| 34096 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Link path can mark replaced bytes as hash-verified (stat vs hash identity, TOCTOU on a local file). Fixed 593ec1f8cf0. (unverified) |
| 34096 | 3 | CR | Minor | real-bug | fixed-before-merge | 3 | 3 | security | yes | Remote client with only `settings:write` can probe server paths and learn the matched file path via model linking; needs `filesystem:read`. CR confirmed fix in code. |
| 34096 | 4 | CR | Minor | real-bug | fixed-before-merge | 3 | 3 | data integrity | yes | `finalPath` is removed before the link is created; if symlink and hard-link both fail an installed model is lost. Fixed by staging and rename. |
| 34096 | 5 | CR | Minor | nit | fixed-before-merge | 1 | 1 | UI state | no | Error toast title wrong for most failures. Neutral title now. |
| 34096 | 6 | CR | Minor | real-bug | fixed-before-merge | 3 | 3 | security | yes | `linkedFrom` absolute path returned by all model endpoints to callers without `filesystem:read` (leaks home dir name). Fixed f2e0793b0eb with test. |
| 34089 | 1 | MS | Medium | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Image jobs recovered by the inventory fallback are emitted without a preview and marked terminal, so no later notice can add one. Fixed 80401f600d; author notes the suggested fix (use `job.path`) would not work on OpenCode 2.2.7. |
| 34089 | 2 | CR | Minor | real-bug | fixed-before-merge | 3 | 4 | resource leak | yes | `failAll` does not settle running image jobs, so after a failed reconnect the tool item stays running and `hasBackground` pins the thread from unloading. Author: regression fails on original, fixed 80401f600d. |
| 34089 | 3 | CR | Major | real-bug | fixed-before-merge | 3 | 5 | race/ordering | yes | `imageReport` sets `job.status` before interruptible preview reads; a 5 s recovery timeout interrupts it and the tool item stays running forever. Author reproduced with an interrupt regression; fix is an uninterruptible finalizer. Not read in code. |
| 34089 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | 11 MiB image passes both 20 MiB checks but exceeds the base64 limit and the preview is stripped later. Shared 10 MiB limit now. |
| 34089 | 5 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | `failAll` settles a child image job but does not sync ancestors, parent still advertises pending work. Fixed 62addc8331. |
| 34089 | 6 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Root thread omits subagent-launched image jobs from `pendingBackgroundTasks`. Fixed 62addc8331. |
| 34048 | 1 | CR | Major | nit | ignored | 1 | 1 | other | no | Wants a regression test for web auto-open. Test-coverage request; unresolved, merged. |
| 34048 | 2 | CR | Major | unclear | ignored | 2 | 3 | cross-file contract | maybe | LAN-connected web client gets `localhost` rewritten to the LAN address, so a loopback-only dev server cannot load in the server-side Preview. Merged code passes `resolveDiscoveredServerUrl(env, previewUrl)` (read at 1bdf470328:useChatTerminalActions.ts:296-300); whether the server-side browser needs the rewrite not traced. |
| 34030 | 1 | MS | Critical | real-minor | ignored | 2 | 3 | data integrity | no | Legacy cache files deleted after first persist. Code read (UsageService.ts 382-440): legacy files are loaded only when the v11 file is missing, and then merged into v11 before deletion, so history is lost only if an older server wrote the legacy file after v11 existed. Narrow; issue text asked for the cleanup. Rated Critical by bot, actual 2. |
| 34030 | 2 | CR | Major | real-minor | ignored | 2 | 3 | data integrity | no | Same defect as T1 from the "older server starts later" side. Duplicate. |
| 34030 | 3 | CR | Minor | real-minor | ignored | 2 | 4 | data integrity | no | Surrogate pair split across encoding batches becomes U+FFFD in the cache file (unverified). |
| 33989 | 1 | MS | High | real-minor | fixed-before-merge | 2 | 4 | UI state | no | Mobile `/checks` link can leave checks off-screen on a reused screen. Fixed c448e3bc3b. |
| 33989 | 2 | MS | High | real-minor | fixed-before-merge | 2 | 4 | UI state | no | After a diff permalink, picking file B from overview reopens file A with its line range. Fixed c448e3bc3b (not with the suggested line, author explains why). |
| 33989 | 3 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Activity row re-scrolls to the linked comment on filter or refresh. Fixed with a per-request guard. |
| 33989 | 4 | MS | High | real-minor | ignored | 2 | 4 | UI state | no | Links to unchanged lines outside partial hunks never reveal. Author reproduced, deferred (library `prepareForEditing` did not help). Known limitation. |
| 33989 | 5 | MS | High | real-minor | fixed-before-merge | 2 | 3 | UI state | no | `#issue-N` or heading links do nothing while Description is collapsed. Fixed c448e3bc3b. |
| 33989 | 6 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | UI state | no | `pendingTop` not cleared, so later content changes yank the user back to the linked comment. Two rounds; final fix a1aabe2c85. |
| 33989 | 7 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | security | no | `selectedUrl` copied as PR link without matching repo and number. Fixed c448e3bc3b. |
| 33989 | 8 | MS | High | real-minor | fixed-before-merge | 2 | 4 | UI state | no | Description link received while the editor is open is lost after Cancel. Fixed b4ed475c57. |
| 33989 | 9 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | UI state | no | Effect omits the target thread id so a filtered-out linked thread never opens its discussion. Fixed d37c38768f. |
| 33989 | 10 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Pending range reveal can scroll the user back after they scroll. Fixed d37c38768f with `cancel()`. |
| 33989 | 11 | MS | High | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Range reveal on a deleted-file patch waits on `loadingFile` forever. Author: valid, fixed 855c266fba. |
| 33989 | 12 | MS | High | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Effect lacks `revealUrl` dependency; a second missing-comment link can stick. Author: narrower than stated, fixed. |
| 33783 | 1 | MS | Medium | real-bug | fixed-before-merge | 3 | 4 | UI state | yes | A queued thread creation vanishes from the pending list when the environment is connected but the outbox will not send (no operate scope, shell not live), removing open/delete actions. Fixed 6b06a810f77 with the outbox's own gate. |
| 33783 | 2 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | UI state | yes | Same defect as T1 (duplicate). |
| 33783 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Web row reads the unmodified shell so "Setting up" status is lost. Fixed 547cd860b9c, author checked in a browser. |
| 33783 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Retry backoff mark kept during a retry send, so the creation stays Unsent while sending. Fixed cdad7b192f2. |
| 33680 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 2 | cross-file contract | yes | New highlighted-fallback branch runs before the Mermaid branch, so completed mermaid fences render as code, not diagrams (feature from #32190 regresses). Fixed 0c6994dceb. |
| 33680 | 2 | CR | Major | real-bug | fixed-before-merge | 3 | 2 | cross-file contract | yes | Duplicate of T1. |
| 33641 | 1 | CR | Minor | real-minor | ignored | 1 | 3 | error handling | no | `process.versions.electron` undefined in Node tests, so GPU-cache deletion could run against `/tmp` data before the marker write fails. Unresolved (unverified). |
| 33548 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 4 | race/ordering | yes | Consecutive host events evaluate the same stale `target.watch`, so an earlier-reported comment wakes the agent again and the comment wake limit uses an old count. Fixed 7e50071 with a test that two events wake once. |
| 33548 | 2 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | race/ordering | yes | Same stale-target root cause on a failed-check group read (duplicate wake). Fixed 7e50071. |
| 33548 | 3 | MS | Low | real-minor | fixed-before-merge | 1 | 3 | error handling | no | A 404 pull request is never put on the one-hour cooldown. Fixed bd62ae1. |
| 33548 | 4 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | error handling | no | Duplicate of T3. |
| 33479 | 1 | CR | Minor | real-minor | ignored | 2 | 3 | cross-file contract | no | When discovery rejects the OpenZFS `zed`, `resolveEditorLaunch` still falls back to bare `zed`, so a direct RPC could run the daemon. Unresolved (unverified). |
| 33439 | 1 | CR | Major | unclear | ignored | 2 | 4 | cross-file contract | no | Project-ID substitution by the clone tracker may confuse older clients still waiting for the requested ID. Plausible, not exercised (unverified). |
| 33439 | 2 | CR | Minor | real-minor | ignored | 2 | 3 | state machine | no | Reused project may be archived and is opened without unarchiving. Unresolved (unverified). |
| 33130 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 4 | race/ordering | yes | Stall timer checks the retry identity before taking `turnTerminalizationPermit`, so a turn that recovered meanwhile is failed and interrupted. Fixed fa405b4eed (check moved inside the permit). |
| 33130 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 3 | race/ordering | no | Test milestone fires before the timer is registered (TestClock flake). Fixed with `startImmediately: true`. |
| 33130 | 3 | CR | Minor | real-bug | fixed-before-merge | 3 | 4 | race/ordering | yes | Duplicate of T1 plus: early write of `latestProviderFailure` survives when finalize returns false. Fixed fa405b4eed, e45aa316e2. Author declined a race test (no seam). |
| 33130 | 4 | CR | Minor | real-minor | ignored | 1 | 2 | other | no | Test replay lacks the account read request. Unresolved, test-only (unverified). |
| 33058 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | Fake child needs a SQLite busy timeout to avoid a flaky test. Fixed fe4bff9814. |
| 33058 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | Constructor `timeout` ignored on Node 23.11, use PRAGMA. Fixed 923309a465. |

## 3. Track B (escaped bugs)

Not traced: #34113 (picker scroll offset, UI), #33989 (feature-sized, Track A), #33641 (pure addition, no SZZ target; bug is "no GPU-cache invalidation on Electron upgrade", sev 3, diff 5), #33130 (pure addition, no SZZ target; bug is "no timeout for a Codex retry that never resolves", sev 4, diff 4; the adapter's original retry handling is the logical origin, unverified).

| fix PR | bug | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 34132 | Find kept parsed thread text and the last 8 query results in memory until restart because Effect `Cache` expires an entry only when the same key is read again | #10439 "feat(web): find messages and plans in the current thread" (+8005/-1467, 139 files, 2026-10-08); 20 of 22 blamed lines | high | missed (Macroscope commented on the same cache but on a different defect: stale counts within the 1 min TTL for a recreated thread; none on never freeing) | 2 | 4 | Needs knowledge of Effect `Cache` expiry semantics. |
| 34121 | Scenario runner failed where `localhost` resolves to IPv6 first | #34007 "feat(scripts): scenarios prove a fix in the real app" (+2112/-148, 26 files, 2026-11-10); 12 of 12 lines | high | missed (Macroscope: High on `start-app.ts:42` about thread-title generation, not IPv6) | 2 | 4 | Environment-dependent, dev tooling only. |
| 34050 | Local server cards in the browser empty state ignored pointer clicks | #15328 "feat(preview): run the browser on the environment server" (+13552/-7701, 163 files, 2026-10-06); 5 of 5 lines | medium | missed (Macroscope left 14+ comments, none on PreviewView or pointer events) | 2 | 3 | Giant PR. |
| 34048 | Project-action auto-open Preview was gated on a desktop-only check, so web clients never auto-opened | #23063 "refactor(web): ChatView's terminal actions live in useChatTerminalActions" (2 lines) | low | bots ran (Macroscope approved, CR summary) with no inline comments | 2 | 3 | Refactor moved the line; the real origin is the earlier ChatView code that used `isPreviewSupportedInRuntime` (not traced). |
| 34030 | Usage-scan cache written as one string: OOM on very large histories (head wrote a 361 MB cache) | #15149 "perf(usage): cut warm usage scans from seconds to milliseconds on large histories" (+579/-131, 9 files, 2026-10-03); 14 of 20 blamed lines in `usageScanCache.ts` | high | missed (Macroscope: 2 comments on `usageTranscriptReader.ts` promise memory, none on cache serialization) | 4 | 4 | Needs scale reasoning: cache size grows with history. A perf PR whose own memory cost was not examined. |
| 33783 | New threads jump in the sidebar between create and first run (draft, Unsent, Working) | diffuse: #15705 (3), #10260 (3), #3670 (2), #22730 (2), 6 more with 1 line | low | not assessed | 2 | 4 | No single introducing PR; UX consequence of the thread.create then message.dispatch split. |
| 33745 | Snapshot shedding order dropped page text before the ARIA tree, so large trees left no page text | #13558 "fix(mcp): preview snapshots fit in the agent's tool output again" (+125/-40, 3 files, 2026-09-25); 5 of 9 lines | medium | missed (Macroscope High and CR on the same `cutText` function about bytes vs characters, not the shedding order) | 2 | 3 | Introduced by an earlier fix to the same area. |
| 33680 | Mobile code fences in diff, kotlin, sql and others render as plain grey text after the markdown renderer swap | #16979 "feat(mobile): replace custom Markdown rendering with Enriched" (+3031/-8559, 177 files, 2026-10-12) per PR body; SZZ blamed #32190 (69 lines, Mermaid file refactor), which is not the origin | medium (origin taken from the PR body, not from SZZ) | missed (CR left one comment on a navigator file, none on code-block languages) | 2 | 3 | Limitation of the library's 14 default grammars. SZZ output is misleading here. |
| 33479 | Linux editor discovery accepted any executable named `zed`, including the OpenZFS daemon | #12439 "fix: detect installed editors outside PATH" (+341/-37, 6 files, 2026-09-19); 12 of 13 lines | medium | missed (CR Major on `editor.ts:92` was about Cursor paths; Macroscope about imports) | 2 | 3 | Domain knowledge (two programs named `zed`). |
| 33439 | Cloning into a stranded clone project's empty folder failed with ProjectConflictError after restart | #11762 "feat(web): clone repositories in the background" (+2206/-25, 28 files, 2026-09-14); 19 of 38 lines | medium | missed (Macroscope: 15+ comments incl. a High on restart behavior in `ChatView`, none on folder reuse) | 3 | 4 | Needs the state machine across restart. |
| 33396 | Trackpad flicks over right-panel tabs navigated back | #9461 "fix(web): make right panel tabs easier to scroll" (+134/-2, 2026-09-03); 3 of 3 lines | high | missed (Macroscope approved, cursor[bot] commented, no inline comment on this) | 1 | 3 | Browser gesture behavior. |
| 33395 | Settings search shortcut used the character, not the physical key, on non-US layouts | #17859 "fix(web): focus settings search with command-f" (+18/-30, 2026-10-11); 5 of 5 lines | high | missed (CR and Macroscope approved, no inline) | 2 | 2 | Keyboard layout knowledge. |
| 33352 | MCP App cards flash white in dark mode while the app loads | #25246 "fix(web): Escape and copy work in chat media and markdown widgets" (+536/-387, 17 files, 2026-10-26); 1 line | low | missed (CR had 2 comments on `McpAppFrame.tsx` about popover and fullscreen) | 1 | 2 | Cosmetic. |
| 33129 | Cmd+J terminal toggle re-rendered the whole sidebar | diffuse: #7277 (23), #5672 (17), #29678 (10), #15549 (10), ... | low | not assessed | 2 | 3 | Performance refactor; no single origin. |
| 33058 | Updates fail when the live database cannot be cloned | #19311 "fix(server): service updates no longer fail on full disks or large databases" (+604/-31, 4 files, 2026-10-14); 2 lines | low | bots ran (summary comments), no inline comments | 3 | 5 | Mostly additions; origin is the earlier clone-only design. |

## 4. Catalogue candidates (real bugs, severity >= 3)

Shas are from `git rev-parse <merge>^1` for the base and `gh pr view --json commits` for the real last commit. Replay base/head is the PR that carries the bug in its pre-fix state.

| id | PR(s) | golden (a reviewer must state this) | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| usage-scan-cache-single-string-oom | #15149 (escaped; fixed by #34030) | The scan cache is serialized as one string, so a cache for a very large transcript history can exceed memory when written. | 39efcd8558 | 5d38fd0ab8 | none |
| speech-model-link-path-leak | #34096 | Model linking and `linkedFrom` expose server filesystem paths to callers who lack `filesystem:read`. | 04f6cfca87 | f2e0793b0e | CodeRabbit (T3, T6), fixed |
| speech-model-link-nonatomic-replace | #34096 | The installed model file is removed before the link exists, so a failed link loses the installed model. | 04f6cfca87 | f2e0793b0e | CodeRabbit, fixed |
| opencode-image-failall-pins-thread | #34089 | `failAll` does not settle running image jobs, leaving the tool item running and the thread never unloadable after a failed reconnect. | 1d80047048 | 62addc8331 | CodeRabbit, fixed |
| opencode-image-status-before-preview | #34089 | `job.status` is set before interruptible preview I/O, so a recovery timeout leaves the tool item running and the job unmatched. | 1d80047048 | 62addc8331 | CodeRabbit (Major), fixed |
| opencode-image-recovery-no-preview | #34089 | Image jobs recovered from the inventory are emitted without a preview and marked terminal so no later notice can add one. | 1d80047048 | 62addc8331 | Macroscope, fixed |
| mobile-pending-creation-hidden-undeliverable | #33783 | A queued thread creation is hidden from the pending list when the environment is connected but the outbox cannot send (no operate scope or shell not live). | 11611419f3 | cdad7b192f | Macroscope, CodeRabbit, fixed |
| mobile-mermaid-fence-rendered-as-code | #33680 | The highlighted-code fallback is checked before Mermaid, so completed mermaid fences render as source code. | 2163d41409 | b4ca413d44 | Macroscope, CodeRabbit, fixed |
| watch-reactor-stale-target-duplicate-wake | #33548 | Event-driven passes evaluate cached `target.watch`, so consecutive events wake the agent twice for the same comment or failure. | 8cbc95923a | bd62ae1db0 | Macroscope, CodeRabbit, fixed |
| codex-stalled-retry-fails-recovered-turn | #33130 | The stall timer checks retry identity outside the terminalization permit, so a turn that recovered while waiting is failed and interrupted. | f15fbdef2e | 65f62fdb9b | Macroscope, CodeRabbit, fixed |

Not catalogued: #33439 clone-folder reuse (escaped, sev 3, origin #11762 is a 2206-line PR; replay possible but golden needs the restart case) and #33641 (no origin).

## 5. Observations

- Macroscope rates UI-navigation issues High (#33989: 8 threads, 7 High) where the real severity is 2; CodeRabbit's Major on #34048 and #34030 T2 were test-request or speculative. Bot severity is not a usable ranking in this repo.
- The strongest finds were races and cleanup paths under timeout or interruption (#34089 T2/T3, #33130 T1/T3, #33548 T1/T2). These were found by both bots and fixed, usually within hours, by AI-authored replies naming the fix commit.
- Both bots answer "I could not verify the fix" when the author's fix commit is not in the bot's snapshot (#33783, #33680, #33548, #33130); the threads were still resolved by the author, so these lines carry no evidence either way.
- At introduction, 0 of 15 escaped bugs were flagged. Two had an adjacent comment on the same function (#34132 via #10439, #33745 via #13558) that targeted another defect, so even a related comment did not catch it. All escaped bugs came from large feature PRs or earlier fixes.
- Unresolved merged threads this chunk are mostly test requests and a few plausible design edges (#34030 T3 surrogate pairs, #33479 fallback launch, #33439 archived project); none confirmed in code.
