# Chunk 07: PRs #25988..#15632 (2026-11-06, last chunk of the day, 17 PRs)

## 1. Header

- PRs covered: 17 (#25988 .. #15632). 4 have no bot thread (#25484, #25320, #25287 perf, #15632 fix).
- Bot threads: 43 total. CodeRabbit 35, Macroscope 8.
- Verdicts: real-bug 3, real-minor 30, nit 9, wrong 1, unclear 0.
- Outcomes: fixed-before-merge 37, disputed/withdrawn 4 (#25971 T5, T12; #23901 T1; #24990 T2), ignored (unresolved) 2 (#22572 T1, #18385 T1).
- Code checked: #22489 T5 (comment commit 133e4144 has only `reviewerUsers`, merge c52df24d has `reviewerIds`). Everything else is judged from thread text, replies and resolved/outdated flags (unverified in code).
- Track B: 12 `fix` PRs touch source (#25988, #25971, #25847, #25579, #24990, #24983, #22572, #22489, #21542, #18385, #16317, #15632). SZZ run on all 12: 1 pure addition (#24983), 2 land only on noise (#18385 on #2829, #15632 on a refactor). 4 PRs are perf/feat and skipped (#25484, #25320, #25287, #19288 perf; #23901 feat, its threads are in Track A).
- Caveat: PR numbers are not merge order. Several introducing PRs have a higher number than the fix (#30704, #27760, #26297) but merged earlier.
- Bot coverage at introduction (9 traced fixes with a real target): caught 1 (#22489 via #4849), missed 8 (incl. 2 adjacent near-misses: #25988, #21542).

## 2. Track A (bot threads)

"fixed" = thread outdated/resolved plus author reply naming a fix commit. "(unverified)" = not read in code.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 25988 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Table with a caption was consumed by the splitter but the caption was dropped. Reply: fixed 831e9e8 with test (unverified). |
| 25971 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Hub's future timeout text not matched, so iOS listing treated as complete and simulators dropped. Forward-looking (upstream hub not yet shipping it). Fixed 3593280. |
| 25971 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Details triggers need host-specific accessible name. Fixed e13427d. |
| 25971 | 3 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Layout class on wrong element (repo style rule). |
| 25971 | 4 | CR | Major | nit | fixed-before-merge | 1 | 3 | race/ordering | no | Test needs a gate so concurrent opens overlap deterministically (test flake). Fixed 6fdebf0. |
| 25971 | 5 | CR | Major | real-minor | disputed | 2 | 3 | data integrity | no | Stopped Android AVDs dropped when `emulator -list-avds` fails. Author: pre-existing behaviour, out of scope; CR withdrew. Real but not introduced here. |
| 25971 | 6 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | WS caller can pass iOS deviceId with platform android and skip the iOS open lock. Fixed 6fdebf0 with test. |
| 25971 | 7 | CR | Major | nit | fixed-before-merge | 1 | 3 | race/ordering | no | Test must take both attaches before releasing in the different-device case (test flake). Fixed ec0f438. |
| 25971 | 8 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | resource leak | no | `withOpenLock` semaphore map never shrinks; unbounded with unique invalid IDs over WS. Outdated, no reply (unverified). |
| 25971 | 9 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | iOS boot returning the original ID matches the retained pre-boot entry, so a session opens while the device stays marked stopped. Fixed e26916d. |
| 25971 | 10 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Hub timeout marked Android incomplete on hosts without Android SDK, hiding SDK install guidance. Fixed e26916d at source. |
| 25971 | 11 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | AVD-list failure not counted as an incomplete Android listing in the panel. Fixed cbf1052 (shared helper). |
| 25971 | 12 | CR | Minor | nit | disputed | 1 | 2 | other | no | Bound local platform checks after timeout. Author: same unbounded check already runs on every listing; CR withdrew. |
| 25971 | 13 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | UI state | no | Settings row omitted the incomplete-list label. Fixed 6a824fe. |
| 25971 | 14 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Dismissed warning stayed dismissed on A to B to A cause change. Fixed, test added. |
| 25971 | 15 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Effect convention: helper only builds an error. Fixed 03183a9. |
| 25971 | 16 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Effect convention: missing named `Effect.fn` span. Fixed 03183a9. |
| 25971 | 17 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Readiness `starting` update cleared the incomplete-listing detail, so the warning vanished while `incompletePlatforms` was still set. Fixed ea35c35, differently from the suggestion. |
| 25847 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Android did-only repair can emit `keyboardDidHide` without will-hide, leaving the store stuck dismissed. Fixed 98d0423. |
| 25579 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 2 | error handling | no | Regex rewrites `team-management.html` to `team-/`. Fixed b1a6db0. |
| 25579 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | error handling | no | Same defect plus trailing-slash variant. Fixed f55e07a. Duplicate of T1. |
| 24990 | 1 | CR | Minor | real-bug | fixed-before-merge | 3 | 4 | data integrity | yes | Line-level dedupe in `appendHandoff` drops quoted lines and headers that are identical across two PRs (same failing check name), so the second PR's findings vanish and the agent gets no signal. Fixed c4a0a34 with a shared-`lint` test. Bot rated Minor; impact is lost findings. |
| 24990 | 2 | CR | Minor | real-minor | disputed | 1 | 2 | data integrity | no | Legacy numeric-key PR chip duplicates once for pre-change drafts. Author declined (one-time, removable); CR withdrew. |
| 24990 | 3 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Ask handoff adds "Do not change any code" context; a later Fix handoff keeps it, so the agent gets conflicting instructions. Fixed b39a419 (plain context chip wins in both orders, tested). |
| 24983 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | `KEYCODE_DEL` does not update tracked `sentText`, so a later emoji IME delete emits extra DELs. Fixed 0a3f2e3. |
| 24983 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | data integrity | no | Each half of a surrogate pair counted as a separate delete (two DELs). Fixed 0a3f2e3. |
| 24983 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Tracker mutated during read-only IME callbacks, stale state later. Fixed 29d53bd. |
| 23901 | 1 | CR | Minor | wrong | disputed | 1 | 3 | state machine | no | Asks that `setStatus` text changes count as activity. Author refutes (arbitrary UI text would defeat the idle-pin cap, restoring the leak the PR fixes); CR withdrew. Author is right (unverified in code). |
| 23901 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 2 | UI state | no | Black capsule applied to the whole control makes agents/queue unreadable in light mode. Fixed 81a09ea. |
| 23901 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Statuses not restored after non-cancel lifecycle errors. Author retires the ambiguous runtime instead (f57c3f9); CR accepted. |
| 23901 | 4 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Use an `output` element for polite live-region announce. Fixed 5deba48. |
| 22572 | 1 | CR | Major | nit | ignored | 1 | 1 | other | no | Wants a `DesktopApp.test.ts` test of the quit deadline. Test-coverage request, unresolved at merge; bot "Major" is inflated. |
| 22489 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Failed host search showed "Nobody matches" instead of the error. Fixed 133e414. |
| 22489 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | race/ordering | no | Debounce window kept showing results of the previous query for 250 ms. Fixed 7f4f1dd. |
| 22489 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | race/ordering | no | Same defect as T2. |
| 22489 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Host-search failure hid local matches without telling the user. Fixed in footer note. |
| 22489 | 5 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | data integrity | yes | GitLab reviewer IDs derived from actors; a reviewer with empty username is dropped, so changing another reviewer rewrites `reviewer_ids` without them and silently removes them. Verified: comment commit 133e4144 has only `reviewerUsers`; merge has separate `reviewerIds`. |
| 21542 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | New SGR parser dropped `38;2:255:0:0` mixed-separator colour values that the old parser accepted. Fixed a6cf32e. |
| 19288 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | `rev-parse --help` dispatches to a viewer yet is classed as a read command. Fixed b5a79d1. |
| 19288 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | `config --edi` (abbrev of `--edit`) classed as read. Fixed b5a79d1, allow-list instead. |
| 19288 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | `symbolic-ref --del` (abbrev) classed as read; ref deletion would get read spawn options. Fixed 49325e5, allow-list. Good example of "abbreviated git option" reasoning. |
| 18385 | 1 | CR | Minor | real-minor | ignored | 2 | 3 | security/privacy | no | Replay path returns another thread's stored rejection detail before checking thread ownership. Unresolved, merged (unverified). |
| 16317 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | performance | no | Coalescer rebuilt the whole pending batch per event under the mutex. Fixed 61b561a. |

## 3. Track B (escaped bugs)

Skipped as not fix PRs: #25484, #25320, #25287, #19288 (perf), #23901 (feat).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 25988 | PR-body splitter lifted video lines out of HTML tables, so before/after tables rendered broken | #4849 "feat: multi-provider pull requests page with in-app reviews" (+34121/-443, 143 files, 2026-08-10); `splitPullRequestBody` and video-line lifting first appear there, carried to client-runtime by #18351 (2026-10-11) | low (SZZ blames #30704, #18351, #4849; the lifting design is #4849) | missed (Macroscope: 7+ comments on the same splitter for fences, indented code, inline `<video>`; none on tables) | 2 | 3 | Near-miss: same function reviewed closely, wrong cases. Cosmetic. |
| 25971 | Failed simulator discovery discarded known iOS devices, so setup recommended installing an already installed runtime | #21835 "refactor(server): device hosts own their device operations" (+528/-413, 2026-10-20); Android half was patched earlier by #19974 "retain inventory when AVD enumeration fails" | low (spread over #22012 24, #21835 20, #19974 12 lines) | missed (#21835: 1 Macroscope convention comment; #19974: 2 CR comments about warning text) | 2 | 4 | #19974 fixed the same class for Android only; the iOS twin stayed. A reviewer who sees the sibling fix could ask "what about iOS". |
| 25847 | Android nonanimated IME show emitted `keyboardDidShow` without `keyboardWillShow`, so accessory/dismiss state stayed hidden while the keyboard was up | #26297 "fix(mobile): smoother Settings and composer transitions on wide Android" (+182/-63, merged 2026-11-03) added `useSoftKeyboardShowing` (will-events only) | medium (4 blamed lines; SZZ also lists #2013 WIP mobile import, noise) | missed (Macroscope High and CR Major on `useSoftKeyboardShowing.ts:8`, about mount during dismissal, a different case) | 2 | 4 | Needs knowledge of the library's desync-repair event order. |
| 25579 | CLIProxy hub saved as its `management.html` panel URL requested `.../management.html/v0/management/...`, so every hub account vanished from Usage | #19336 "fix(usage): a CLIProxyAPI hub served under a path keeps its path" (+18/-2, merged 2026-10-18) | high (4 of 5 lines; fix PR body names it) | missed (CR and Macroscope reviewed, 0 inline comments) | 3 | 4 | Regression from a fix: keeping the path broke URLs saved with the panel filename. Needs user-behaviour knowledge. |
| 24990 | New "Add to agent"/"Fix finding" handoffs replaced earlier findings/selections instead of appending | #4849 (handoff design, 41 lines in `pullRequestDetail.logic.ts`), reshaped by #11265 "inline file previews and attachment chips" (+21441/-4843) | low | missed (Macroscope on #4849 flagged `handoffPrompt` discarding the reader's own text, fixed there; not the replace-previous-handoff behaviour) | 3 | 3 | Design gap rather than regression. Findings lost silently. |
| 24983 | Android terminal Backspace swallowed on some IMEs (FUTO) | no SZZ target (pure addition) | n/a | n/a | 2 | n/a | New IME deletion path, hardware reproduction needed. |
| 22572 | Quit waited 5 s per backend while the spawner's SIGKILL fires after a 5 s SIGTERM grace plus 1 s, so a slow backend was orphaned (holds sqlite, 10+ min "hung" quit) | #7599 "fix(desktop): bound backend shutdown wait during quit" (+95/-12, 2026-09-12) set the 5 s quit bound; #22222 revert reinstated 1 line in DesktopUpdates | medium (1 blamed line in DesktopApp from #7599, 1 in DesktopUpdates from #22222) | missed (CR, Macroscope, Codex bot reviewed #7599; 0 inline comments on the timeout) | 3 | 4 | Timeout arithmetic across two modules: needs the 5 s grace constant and the spawner's kill sequence. |
| 22489 | Reviewer menu loaded one page (100) and filtered locally, so some people could not be requested; GitLab requested reviewers outside the page could not be removed | #4849 (original reviewer picker, 16 of 27 lines) | high for the page limit | caught-and-ignored at intro (Macroscope High on `PullRequestReviewerPicker.tsx:52`: typing only filters the first page, candidates beyond can never be picked; same for Bitbucket 50) | 2 | 2 | The bot stated the defect on 2026-08-05; it shipped and was fixed 3 months later. |
| 21542 | `ESC[4:3m`, `ESC[4:0m`, `ESC[58;...m` scrambled bold/colour/italic in command output | #15094 "fix: command output streams live while it runs" (+3287/-41, 2026-10-16); 7 of 7 lines | high | missed, near-miss (Macroscope noted colon-to-semicolon normalisation breaks `38:2:0:255:0:0`; the same normalisation causes the underline-subparameter bug, not mentioned) | 2 | 3 | Root cause is the `:` to `;` rewrite; the bot named it for colour only. |
| 18385 | Same `commandId` for two threads at once: both report success, only one thread changed | no meaningful target (SZZ: #2829 34 lines = original orchestrator import; `replayed` flag from #24601 reformat) | n/a | n/a | 3 | 4 | Race in the original receipt design; no replayable PR. |
| 16317 | Bursts of full tool updates filled the 8 MiB live buffer before the 50 ms window; `LiveStreamBufferError` | #9715 "fix(server): bound slow-client event buffers" (+786/-105, 2026-09-04) added the budget; #24267 "coalesce superseded streaming text updates" (2026-10-24) kept retain-then-replace-at-flush | medium-low (8 lines in #9715, 2 in #24267, 3 in #2829) | missed (#9715: Macroscope review, 0 inline; #24267: 0 inline) | 3 | 4 | Interaction of two mechanisms (charge on retain, coalesce on flush). |
| 15632 | Usage provider summaries ranked in fixed order, not by selected metric | no real target (SZZ lands on #20807 "usage page keeps its caching without use memo", a refactor) | n/a | n/a | 1 | 1 | Feature-ish ordering fix. |

## 4. Catalogue candidates (real bugs, severity >= 3)

| id | PR(s) | golden description | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| desktop-quit-timeout-equals-sigterm-grace | #7599 (fixed by #22572) | Quit waits `stop({timeout: 5s})` per backend, equal to the 5 s SIGTERM grace, so the wait expires before the SIGKILL and the app exits, orphaning a backend whose shutdown is slow. | c52b8d96e4b34201f19b5e5bb12c6b2a77bfaa9a | 44ad0b15ee359464abd1976d6950efafc1f20330 | none (found by a user, 2 months later) |
| live-buffer-charged-before-coalescing | #9715 (fixed by #16317) | Each full tool-output update is charged to the live-event byte budget when retained, before superseded updates for the same thread, run and tool are dropped, so a burst of large updates raises `LiveStreamBufferError` before the 50 ms batch flushes. | 7839140e5e93d3f401d7eb45b86cf1a234eb3609 | 8f228395cbfb7c44b8702f80534bb12f26308746 | none (low confidence on the introducing PR) |
| cliproxy-hub-panel-url-path-404 | #19336 (fixed by #25579) | Keeping the hub URL path means a hub saved as its `management.html` page requests `.../management.html/v0/management/auth-files`, gets 404, and every hub account disappears from Usage. | 8e018ff91f64d6caedc029e498eca446ff0fad20 | ea289d28279ecee9f0e1da30987fe10e66d33125 | none |
| gitlab-reviewer-ids-dropped-without-username | #22489 | GitLab reviewer IDs are built from converted actors, so a reviewer with an empty username is dropped and changing another reviewer sends a `reviewer_ids` set without them, removing them. | e4ff5da0d344909de1d80eff73803d9924cd7aaa | 133e4144988d6b5af4012bb995ca529ef5a8630e (commit CR commented on) | CodeRabbit (fixed before merge) |
| pr-handoff-line-dedupe-drops-other-pr-findings | #24990 | `appendHandoff` drops every incoming line already in the draft, including quoted check lines and section headers, so a second PR's identical findings (same failing check) are lost with no signal to the agent. | 35bda281170f14d772183f8fc690579758343d10 | 757a6d441c071bb270ad870d711291182d45251c (commit CR commented on) | CodeRabbit (fixed before merge) |
| pr-handoff-ask-context-not-superseded-by-fix | #24990 | An Ask handoff adds a context chip saying not to change code, and a following Fix handoff keeps it because it adds no replacing chip, leaving the agent with contradictory instructions. | 35bda281170f14d772183f8fc690579758343d10 | a6cdd6e60a22da9947daba87c814cb68771476ba (commit CR commented on) | CodeRabbit (fixed before merge) |

Not promoted: #18385 (sev 3 race, no replayable introducing PR; the original receipt design is inside the #2829 import).

## 5. Observations

- CodeRabbit again leads on volume (35 of 43 threads) and rates tests and style requests Major (#25971 T4, T7; #22572 T1), while its real severity-3 finds carry Minor or Major inconsistently (#24990 T1 is Minor and loses user findings).
- The author-side AI loop (Codex "on behalf of" the author, Claude Code) answers nearly every thread with a fix commit and a test; both bots then confirm. 37 of 43 threads end fixed, and bots withdraw when the author gives a concrete refutation (#23901 T1, #25971 T5, T12, #24990 T2). The author was right in the one case checked (#23901 T1).
- #19288 shows CodeRabbit reasoning about external tool behaviour (abbreviated git options such as `--del`, `--edi`) from the Git source, and the author confirming each on Git for Windows. Three real defects, all fixed.
- Escaped bugs here come from timeout arithmetic (#22572), regressions from an earlier fix (#25579), and sibling cases (#25971 iOS after the Android fix #19974). Neither bot commented on any of these at introduction.
- The one "caught" escape (#22489 via #4849) is Macroscope stating the exact limitation on day one, rated High, and the shipped code keeping it for 3 months; flags without an owner decision do not become fixes.
