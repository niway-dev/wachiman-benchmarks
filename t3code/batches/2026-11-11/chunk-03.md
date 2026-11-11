# Chunk 03: PRs #32963..#29183 (2026-11-11)

## 1. Header

- PRs covered: 25 (#32963 .. #29183). 6 have no bot thread (#32963, #32880, #32504, #31868, #30620, #29956).
- Bot threads: 63 total. CodeRabbit 52, Macroscope 11.
- Verdicts: real-bug 5, real-minor 35, nit 14, wrong 8, unclear 1.
- Outcomes: fixed-before-merge 27, disputed 14 (author replied "not changing", CodeRabbit withdrew in 12 of them), ignored 9, unknown 13 (thread outdated and unresolved, no reply; #30768 x7, #30473 x5, #32913 T4).
- Code read at the merge commit (or comment commit): #32913 T3, #32494 T1, #32151 T1, #32040 T1, #32646 T2, #31972 T1, #29923 T1, #30473 T1 (file gone). All other verdicts come from thread text and replies and are marked "(unverified)" where nothing else backs them.
- Track B: 23 `fix` PRs. 1 trivial (#31868 copy), 21 SZZ runs, 1 traced from the PR body (#30665 -> #30588). Many "fixes" are really missing behaviour (feature gaps), so SZZ blames refactors; those rows say so.
- Caveat: All 5 real-bug threads (4 distinct bugs; #30556 T1/T4 are one) are in PRs whose own code was wrong when first pushed, and all were fixed before merge by the author after a bot comment. Nothing in this chunk is a bot-caught bug that was ignored.
- Caveat: `base` shas below are `pulls/N .base.sha` (the base when the PR merged), not a verified merge-base.

## 2. Track A (bot threads)

CR = CodeRabbit, MS = Macroscope. "reply" = author reply says fixed; "outdated" = thread flagged outdated by GitHub.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | one-line finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 32913 | 1 | MS | none | nit | fixed-before-merge | 1 | 1 | other | no | Asks to fold a 504 test into an existing one. Outdated+resolved (965b08b) (unverified). |
| 32913 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | error handling | no | `TRANSIENT` retry list excluded 507/524 although PR says all 5xx. "Addressed in 965b08b"; merged `isTransient` uses `>= 500`. |
| 32913 | 3 | CR | Major | real-minor | ignored | 2 | 3 | error handling | maybe | Retry loop wraps only `fetch()`. Body read (`.text()`, archive stream in `download`) is outside it, so a mid-stream drop still aborts install. Confirmed in merged t3.mjs. Unresolved, merged. Severity overstated: CLI install just fails and can be re-run. |
| 32913 | 4 | MS | none | nit | unknown | 1 | 1 | other | no | Same test-duplication request for install.test.ts; outdated, unresolved (unverified). |
| 32902 | 1 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | Doc must state the fallback conditions. reply 0ebbb6a2f3, resolved. |
| 32902 | 2 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | other | no | Doc: a queued delegated-task result can run before the replacement. reply 0ebbb6a2f3. |
| 32902 | 3 | CR | Minor | wrong | disputed | 1 | 3 | other | no | Wants `/goal clear` to honor restart. Author: goal branch precedes fallback on every provider, by design. CR withdrew. |
| 32902 | 4 | CR | Minor | real-minor | fixed-before-merge | 1 | 4 | state machine | no | Doc: only an unheld delegated result that survives the interrupt runs first. Addressed 7d2da57. |
| 32902 | 5 | CR | Minor | wrong | disputed | 1 | 2 | other | no | `freshContext` turns restart into queue; predates PR. CR withdrew. |
| 32902 | 6 | CR | Minor | nit | disputed | 1 | 3 | error handling | no | Document failed-stop outcome; response already says `delivery: "queued"`. CR withdrew. |
| 32832 | 1 | CR | Minor | wrong | disputed | 1 | 2 | other | no | Test uses one `yieldNow`; 33 existing uses in the file. CR agreed it overstated and withdrew. |
| 32681 | 1 | CR | Minor | real-minor | ignored | 2 | 3 | cross-file contract | no | GitHub Enterprise on a custom host: tree page URL still passed to clone (unverified). Unresolved. |
| 32681 | 2 | CR | Minor | nit | ignored | 1 | 2 | other | no | Wants a palette test for the destination (test request). |
| 32681 | 3 | CR | Minor | nit | ignored | 1 | 1 | other | no | Doc: not every page URL is recognized (outdated). |
| 32646 | 1 | CR | Major | real-minor | fixed-before-merge | 1 | 2 | other | no | New bash test failed in CI because `/etc/profile` runs first. Reply 1e836dc: switched to `BASH_ENV`. Test-only. |
| 32646 | 2 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | maybe | `trap - DEBUG` for `sh`/ksh: on OpenBSD ksh it exits the probe shell so no env is captured; ksh93 also left trap active. Addressed 6f9adc6; merged code runs `(trap - DEBUG) 2>/dev/null && trap - DEBUG` and has ksh93 in the set. Bug was in the PR's own first version. |
| 32494 | 1 | CR | Major | real-minor | ignored | 2 | 4 | race/ordering | maybe | MCP update reads the task, then upserts `existing.workspaceStrategy`; a Settings change between read and upsert is overwritten. Pattern confirmed in merged code (read at top, full-object upsert). Narrow window, no reply. |
| 32151 | 1 | CR | Major | real-minor | ignored | 2 | 3 | UI state | no | Rail height capped relative to timeline, so with 200 turns on a short pane the strip is denser than the pointer grid. Cap constant confirmed in merged logic; exotic. No reply. |
| 32151 | 2 | CR | Major | real-minor | ignored | 1 | 3 | UI state | no | No regression test; plus a Minor: centered preview pokes 6px above a 160px timeline (unverified). |
| 32040 | 1 | MS | High | real-minor | fixed-before-merge | 2 | 4 | other | no | One oversized header/footer made the expansion drop every optional part. Outdated; `oversized` no longer in merged officeArchive.ts (omitted set now `truncated \|\| !used.has`). Only degrades a preview. |
| 31972 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Disabled menu trigger blocks refresh-on-open, so Commit stays unavailable after terminal edits. Addressed f693214; merged code adds `refreshStatusForEmptyMenu` on pointer enter and focus. |
| 30841 | 1 | CR | Minor | nit | disputed | 1 | 2 | UI state | no | `max-md:hidden` headings; predates #25877 and restores old behavior. CR withdrew. |
| 30841 | 2 | CR | Minor | real-minor | ignored | 1 | 2 | UI state | no | Untitled groups have no accessible heading (unverified). Unresolved. |
| 30768 | 1 | MS | High | real-minor | fixed-before-merge | 2 | 2 | other | no | Matcher stops at `[`, linking `/tmp/app/` instead of `/tmp/app/[id]/page.tsx`. reply 301e174. |
| 30768 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Mobile table-break fallback applies only `fileEdits`, so prose paths stay unlinked. reply 301e174. |
| 30768 | 3 | MS | High | real-minor | fixed-before-merge | 2 | 2 | other | no | Duplicate of T1. |
| 30768 | 4 | CR | Minor | real-minor | unknown | 2 | 4 | data integrity | no | An unrelated escape in a text node makes the guard skip the whole node (unverified). Outdated, unresolved. |
| 30768 | 5 | CR | Minor | nit | unknown | 1 | 2 | other | no | Eval `textMustNot` only catches ellipsis after one prefix; plus control-case request. |
| 30768 | 6 | CR | Minor | real-minor | unknown | 1 | 2 | other | no | Trailing `)` trim breaks `/tmp/report(1)` (unverified). |
| 30768 | 7 | CR | Minor | real-minor | unknown | 1 | 2 | other | no | `See [ /tmp/notes.md]` includes `]` in path (unverified). |
| 30768 | 8 | CR | Minor | nit | fixed-before-merge | 1 | 3 | other | no | Eval grader: link inside backticks passes. Maria fixed in 3219130; CR still saw fenced-block gap. |
| 30768 | 9 | CR | Minor | nit | unknown | 1 | 3 | other | no | Eval pattern can reject a valid link between two code spans. |
| 30768 | 10 | CR | Minor | nit | unknown | 1 | 2 | other | no | Eval pattern eats prose `...` after a link. |
| 30768 | 11 | CR | Minor | nit | unknown | 1 | 2 | other | no | Use `finalTextMust`; eval hygiene. |
| 30665 | 1 | MS | High | real-minor | fixed-before-merge | 2 | 3 | other | no | `relabelThreadLinks` mangles a link whose label has a closed code span. reply 965262e: linear backtick-run scan. |
| 30575 | 1 | MS | Medium | real-minor | fixed-before-merge | 1 | 2 | UI state | no | Code tab counts overview threads in the orphan count. reply 7e8420f277. |
| 30575 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Resolve button re-enables on stale `isResolved` after a detail re-render, so second click repeats the resolve. reply 7e8420f277. |
| 30575 | 3 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | UI state | no | Duplicate of T1. |
| 30575 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Duplicate of T2 (same fix). |
| 30575 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Closing and reopening a thread clears the pending guard. Fixed with a keyed store (a1dc160). |
| 30575 | 6 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | resource leak | no | The fix for T5 retained full activity snapshots; CR caught its own follow-on. WeakRef (8ffe863). |
| 30556 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | If `merge_requests` create fails, the `revert-<sha8>` branch stays and retries fail at branch creation. reply c5a9985d80. |
| 30556 | 2 | CR | Major | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Single-commit fast-forward MRs have both SHA fields null, so revert reports "unavailable". reply c5a9985d80. |
| 30556 | 3 | CR | Minor | wrong | disputed | 1 | 2 | error handling | no | Bound error detail; author: same as merge/rebase/close. CR withdrew. |
| 30556 | 4 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | Same defect as T1 (branch left behind). |
| 30556 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Server gate checks capabilities only; revert of a non-merged MR would revert an unmerged commit. UI hides it, so only API/MCP callers. bea8fa08b3. |
| 30556 | 6 | CR | Major | nit | disputed | 1 | 3 | other | no | Gate on create-MR permission, not `can_merge`. Author: conservative on purpose. |
| 30535 | 1 | CR | Major | real-bug | fixed-before-merge | 3 | 5 | cross-file contract | yes | Range endpoint `line_code` built as `_0_12` for an added line; GitLab keeps the old-side counter (`_10_12`), so the range cannot find its lines. Fixed a4cd1ba by reading the hunk. Needs GitLab diff-format knowledge. |
| 30535 | 2 | CR | Major | wrong | disputed | 1 | 4 | cross-file contract | no | Context endpoint `type: null`; author shows GitLab's own form sends nil. CR withdrew. |
| 30535 | 3 | CR | Minor | wrong | disputed | 1 | 3 | other | no | Skip diff reads for one-line ranges; clients never send them. CR withdrew. |
| 30473 | 1 | CR | Major | unclear | unknown | 1 | 3 | cross-file contract | no | Mobile question preview cannot load workspace images. Outdated; `PendingUserInputCard` has no resolver text at merge (unverified fate). |
| 30473 | 2 | CR | Minor | real-minor | unknown | 1 | 2 | other | no | `trim()` drops indented-code indentation. Outdated (unverified). |
| 30473 | 3 | CR | Minor | real-minor | unknown | 1 | 2 | UI state | no | Thumbnail width goes to -4 before layout. Outdated (unverified). |
| 30473 | 4 | CR | Minor | real-minor | unknown | 2 | 4 | state machine | no | Failed run after an image read shows no thumbnail (mobile). Outdated (unverified). |
| 30473 | 5 | CR | Minor | real-minor | unknown | 2 | 4 | state machine | no | Same for web itemized failed-run path. Outdated (unverified). |
| 30473 | 6 | CR | Minor | real-minor | ignored | 2 | 4 | data integrity | maybe | Codex `imageView` path with `#`, `?` or `%20` is parsed as Markdown destination, thumbnail resolves to a different file (unverified in code). Unresolved, not outdated. |
| 30150 | 1 | CR | Major | real-minor | disputed | 2 | 3 | other | no | `author:a author:b` drops the author filter instead of OR. Author: contract carries one author; separate capability. A user later asked for multi-select. |
| 29923 | 1 | CR | Minor | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Root under sudo got `/run/user/0` fallback, so install could write and activate a separate root `t3code.service`. a66d091; merged code has `rootUnderSudo` excluded from `userManagerEnv`. Author reproduced it in a Debian 13 container. |
| 29923 | 2 | CR | Minor | nit | disputed | 1 | 3 | error handling | no | Wants admin guidance when linger fails. Author: would give wrong advice on non-systemd hosts. |
| 29923 | 3 | CR | Minor | nit | disputed | 1 | 2 | other | no | Bound the polling deadline; worst case about a minute on a broken host. |
| 29923 | 4 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | state machine | no | `sudo` install ran `enable-linger 0`, persisting root config even if install later fails. Outdated at a3150d7. |
| 29183 | 1 | CR | Minor | wrong | disputed | 1 | 3 | other | no | Wanted a bigger test transcript; budget charges ~2 B/char, test fails on main. CR withdrew. |
| 29183 | 2 | CR | Major | wrong | disputed | 1 | 4 | resource leak | no | Evict before rejecting a near-budget window. Author: parsed record is in memory with the window, so the check is correct. CR agreed. |

## 3. Track B (escaped bugs)

Introducing-PR confidence is about the SZZ answer. "feature gap" means the fix adds behavior that never existed; SZZ then points at the PR that wrote the surrounding code and the defect has no real introducing change. Bot columns come from `gh api .../pulls/N/comments` for coderabbit/macroscope.

| fix PR | bug | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 32963 | Mouse tilt wheel switched threads on Windows/Linux (swipe handler ran everywhere) | #27430 feat(desktop): back/forward + trackpad swipe (+307/-5) | high | missed (MS commented on a different defect, phone-trackpad conflict at :146) | 2 | 3 | The handler was added with no platform gate. Needs knowing a tilt wheel looks like a swipe. |
| 31868 | Copy: "1 page" plural | n/a | n/a | n/a | 1 | 1 | Trivial, no SZZ. |
| 32913 | Installers gave up on first transient GitHub 5xx | #12044 feat(cli): installer progress (10 lines) | low | missed (MS/CR threads on progress code only) | 2 | 2 | Feature gap (no retry ever existed); #12044 only rewrote the download path. |
| 32902 | `restart` send always failed on a running Claude thread | #25426 goals stop turn (5 lines) | low | missed (MS on Codex goal hang, CR on goal text; none on restart) | 3 | 4 | Probably older policy gap in `decideSteeringExecution`; #25426 touched adjacent lines. Needs provider-capability knowledge. |
| 32880 | Codex chats moved from scratch folder into a project were not imported | #30652 rewound Codex imports (2 lines) | low | no bot comments on #30652 | 2 | 4 | Likely a feature gap in scanner cwd handling; #30652 was merged 5 days earlier. |
| 32832 | Stable channel showed newest nightly's notes under the stable version | #3832 nightly changelog tooltip (1 line) | medium | missed (MS found 3 unrelated tooltip issues) | 2 | 5 | Root cause is electron-updater's fallback to the feed's first entry; diff alone cannot show it. |
| 32681 | Pasted repo page URL (`/tree/main`) cloned into `~/main` and failed | #24904 ghq-style clone folders (2 lines) | low | missed (CR on reserved device names; MS on a folder race) | 2 | 3 | Mostly feature gap; #24904 passed `rawRepository`, which this fix removes. |
| 32646 | `DEBUG` trap in `.bashrc` echoed probe commands, corrupting captured env values | #972 backfill SSH_AUTH_SOCK (1 line) | low | no bot comments on #972 | 2 | 4 | Marker-based probe design from #972; no SZZ-quality target. |
| 32504 | A follow-up task waited only for runs it started, not a run its child queued on its own thread | #17696 track resumed subagent follow-ups (+954/-122) | medium | missed (MS High on a different follow-up finalization case; CR on test/edge cases) | 3 | 5 | Same mechanism, adjacent case. Candidate `delegated-followup-ignores-self-queued-run`. |
| 32494 | Unbound scheduled task reset to "new worktree" when an agent updated it with `bindToCurrentThread:false` | #21514 comment-halving refactor (1 line) | low | bots did not comment on #21514 | 3 | 3 | Real origin is the PR that added the rebinding branch; pickaxe on the blobless clone was too slow to find it. User's saved setting silently lost. |
| 32151 | Minimap preview stole hover and jumped at end ticks | #22662 minimap moved to own file (32 lines) | low | no bot comments on #22662 | 2 | 2 | A move refactor, real origin is earlier (#3869 7 lines). |
| 32040 | Word preview stopped at the first long table; styles lost on long docs | #21362 office/font/mermaid previews (23 lines) | high | missed (MS on xlsx memory and mermaid, CR on slide painter etc.) | 2 | 4 | Limits were sized for main-thread rendering; fix re-measured them. No bot could know without measuring the engine. |
| 31972 | Git actions chevron stayed clickable with nothing usable in the menu | #12453 narrow chat headers (8 lines) | low | missed (MS on header layout) | 1 | 3 | UX gap reported in issue #13406. |
| 30841 | Settings section nav as an ARIA tree broke NVDA browse mode and Tab | #25877 F6 and keyboard navigable sidebar (22 lines) | high | missed (MS/CR commented on focus and tabIndex details in the same PR, none on the tree role) | 3 | 5 | Fix body names #25877. Screen-reader behavior needs NVDA knowledge. |
| 30768 | Plain scratch paths in prose not clickable; `...` paths became broken chips | #24263 bound streaming markdown cache (1 line) | low | missed (CR on mobile test script and markdownDocument 358) | 2 | 2 | No SZZ target: feature gap. |
| 30665 | Thread URLs inside code or titled links rewritten wrongly | #30588 hosted thread URLs inside other links (named in PR body) | high | caught (MS Medium and CR on label with backtick, `threadLinks.ts:17`; same defect fixed by this follow-up) | 2 | 3 | #30588 was still unmerged; this PR targets its branch. 203 files because of a main merge. |
| 30620 | Image path tooltips stayed after preview and scroll | #11265 inline file previews (4 lines) | low | missed (CR threads on ExpandedImageDialog:98, a different bug) | 1 | 3 | UI polish. |
| 30535 | GitLab review comments could only cover one line | #4849 multi-provider PR page (19 lines) | low | missed | 2 | 3 | Feature gap, not a regression. |
| 30473 | Images the agent opened were invisible outside the collapsed tool group | #15056 (7 lines) | low | not checked (unverified) | 2 | 3 | Feature gap; no SZZ target. |
| 30150 | GitHub-style search query (`is:pr state:open -draft:true ...`) listed no PRs | #19934 typed qualifiers filter mobile PR search (6 lines) | medium | missed (CR on comma splitting inside quotes only) | 2 | 3 | #19934 parsed `is:`/`state:` as required labels. |
| 29956 | `t3 doctor` gave no warning of reclaim duration or steps | #19436 doctor reclaims database space (7 lines) | medium | missed (MS on error taxonomy) | 1 | 2 | UX copy and progress, not a defect in data. |
| 29923 | `t3 service install` failed on Linux hosts with no login session | #8173 keep provider CLIs in macOS service (9 lines) | low | missed (MS on plist chars) | 3 | 4 | Linux user-manager probing predates; #8173 touched the same file. Blame is spread over #23878, #29244 and others. |
| 29183 | Long Claude sessions skipped by the 32 MiB import budget | #19161 import long Claude sessions (1 line each across many) | low | missed (CR and MS on retention window edge cases, adjacent to this) | 2 | 4 | #19161 built the budget and retention that this PR replaces with a windowed history. |

Summary: of 22 traced, bots at the introducing PR caught 1 (#30588 -> #30665), missed 16 (several are feature gaps, so a miss is not meaningful), 4 had no bot comments (#22662, #21514, #30652, #972), 1 not checked (#15056).

## 4. Catalogue candidates (real bugs, severity >= 3)

| id | PR(s) | golden (reviewer must state) | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| gitlab-revert-branch-left-behind | #30556 | If creating the revert merge request fails after the `revert-<sha8>` branch is created, the branch is not deleted, so a retry fails at branch creation and the user cannot complete the revert. | a03d9bce02 | 2824155f32 | Macroscope (High) and CodeRabbit (Major) |
| gitlab-range-line-code-counters | #30535 | A ranged comment endpoint on an added line is sent with `line_code` `_0_N`; GitLab keys it by both old and new counters (`_<old>_<new>`), so the range does not resolve to its lines. | b3fdf2b10f | 9347349ce5 | CodeRabbit (Major) |
| service-install-root-under-sudo | #29923 | The `/run/user/<uid>` fallback also applies to uid 0 under sudo, so `sudo t3 service install` can reach a root user manager and install a separate root `t3code.service`. | b3fdf2b10f | 6d21c45dc4 | CodeRabbit (Minor) |
| shell-probe-oksh-trap-debug | #32646 | `trap - DEBUG` is run for `sh` and ksh; on OpenBSD ksh it exits the probe shell so no environment is captured, and ksh93's trap was left active. | 871b00907d | 8457e47106 | CodeRabbit (Major) |
| delegated-followup-ignores-self-queued-run | #17696 (introduced), fixed by #32504 | A follow-up delegated task does not wait for a run its child queues on its own thread, because that run is not linked to the task's `delegatedTaskId`. | 03bd839554 | e195ddbc36 | none |
| settings-nav-aria-tree-blocks-screen-readers | #25877 (introduced), fixed by #30841 | The settings section nav is an ARIA tree with one Tab stop and `aria-hidden` group headings, so screen-reader browse mode and heading navigation cannot reach the sections. | 0894156d9a | d8eecf9459 | none |

Replay notes: bases are `.base.sha` from the API (unverified merge-base). The last two replay a 45-file and a 14-file PR and are hard (difficulty 5); the first four are in small PRs and replay from the PR itself.

## 5. Observations

- Both bots caught real defects in feat PRs that were fixed before merge (#30556, #30535, #29923, #32646). All four sat in provider- or platform-specific behaviour (GitLab API, systemd, ksh) where the bot cited external docs.
- Escaped bugs in this chunk are mostly feature gaps or UX/platform behaviour (tilt wheel, NVDA, electron-updater fallback). Bots at the introducing PR did not mention any of them; the ones with real SZZ targets (#27430, #25877, #17696, #21362) were reviewed by bots on other lines.
- CodeRabbit withdrew 12 of 14 disputed threads after a short author reply. Pattern: it raised an "intended" behaviour as a bug, the author gave a one-paragraph reason, CodeRabbit agreed. Several carried the Major label (#30535 T2, #29183 T2, #30150 T1).
- Macroscope's "Sorry, I'm unable to act on this request because you do not have permissions" appears under several of its threads here (count not tallied), after the author (or a GPT/Opus agent writing for them) replied. The replies are bot-written fixes ("responding on behalf of") in #30768, #30665, #30575.
- CodeRabbit's own follow-up created a finding (#30575 T6: the T5 fix retained full snapshots), and it raised the same defect twice with Macroscope (#30575 T1/T3, T2/T4; #30768 T1/T3; #30556 T1/T4), so thread counts overstate distinct bugs.
