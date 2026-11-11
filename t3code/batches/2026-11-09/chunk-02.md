# Chunk 02: PRs #33268..#33143 (2026-11-09)

## 1. Header

- PRs covered: 25 (#33268 .. #33143). 13 have no bot thread at all.
- Bot threads: 42 total. CodeRabbit 21, Macroscope 21.
- Verdicts: real-bug 4, real-minor 20, nit 17, wrong 1, unclear 0.
- Outcomes: fixed-before-merge 27, disputed 14 (author replied with a reason for declining), ignored 1 (#33229 T1, left "for a maintainer call"), unknown 0.
- Code read at the comment's commit: #33209 T1, #33157 T1, #33177 T2, #33147 T9 and T10. Everything else comes from thread text, replies and resolved/outdated flags (unverified in code). "Fixed" is the author's reply, not re-read at the merge commit.
- All PRs in this chunk and all SZZ targets merged into `main`. No stack-branch case. (#33153 was stacked on #33150 and retargeted to main before merge; its T3/T4 threads are about #33150's file and were outdated.)
- Track B: 12 `fix` PRs, 7 non-trivial source; SZZ run on 6 (#33143 is almost a pure addition, no SZZ). Time: about 25 minutes.
- Caveat: this day's bots reviewed a heavily agent-written stream (Opus 5.5 / GPT-6.1 Sol replies on behalf of the maintainers). Replies like "Fixed in <sha>" come with a new test row, which is strong evidence of a real fix.

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 33255 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Titled link breaks for thread IDs containing `)` (e.g. clientRequestId `qa(1)`): the link parser truncates the ID. Reply: angle-bracket destinations, test for balanced/unbalanced parens (c760f335a6). Unverified in code. |
| 33255 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | Eval fixture for `t3_thread_send` still expects a bare link. Fixed in c760f33 (unverified). |
| 33229 | 1 | MS | Medium | real-minor | ignored | 2 | 4 | state machine | no | Patched keyboard-controller: after unfreeze `onContentInsetChange` keeps the old height. Owner confirms but the hunk is byte-identical in the 1.22.8 patch on main; left for a maintainer. Pre-existing, unverified. |
| 33229 | 2 | MS | Medium | nit | disputed | 1 | 3 | cross-file contract | no | `onContentInsetChange` reports only `bottom`. Reply: sole consumer is a non-inverted list that merges static inset itself. Not applicable (unverified). |
| 33213 | 1 | CR | Minor | nit | disputed | 1 | 2 | UI state | no | Wants a header button to reopen a closed preview. Author: intentional; CR withdrew. |
| 33209 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 3 | cross-file contract | yes | "Turn on" sets only top-level `enabled`; verified at 277b0642aff6 line 514 `instance: { ...instance, enabled: true }` with `config.enabled` untouched, while the resolver treats either false flag as disabled. Fixed in be2e8d4a8ef with a failing-before test (reply). |
| 33209 | 2 | MS | (none) | nit | fixed-before-merge | 1 | 1 | other | no | Test-signal rule: assertion only checks callback wiring. Removed in 0afca2a16bf. |
| 33209 | 3 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Retrying `Start` loses the imported-thread count, suppressing the success toast. Fixed in 0afca2a16bf (unverified). |
| 33209 | 4 | CR | Minor | real-minor | disputed | 2 | 4 | state machine | no | Failed history import plus failed setup save, then retry creates a duplicate project and is rejected. Author: same behaviour on main, recovery exists, needs three failures. |
| 33209 | 5 | MS | Medium | nit | disputed | 1 | 3 | UI state | no | Deselecting all projects after a failed save still lands in the imported project. Author's reasoning (import already happened) is sound. |
| 33209 | 6 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | Doc: per-file 100,000-record limit stated as per-attempt. Fixed f9971293865. |
| 33196 | 1 | CR | Minor | nit | disputed | 1 | 3 | other | no | `inspectConnector` waits on `/ready` up to 5 s when reading link state. Author: same server as `/config`, no gain. |
| 33196 | 2 | CR | Minor | real-minor | disputed | 2 | 3 | security | no | A level-bound code above the managed ceiling shows full access without the ceiling note; server still enforces the cap. Display-only edge, reachable only via direct pairing API (unverified). |
| 33177 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Doc: Standard sends no `service_tier`. Fixed 795c210101. |
| 33177 | 2 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Pi before 0.99 acknowledges a handled tier command with no `disposition`; verified at 00e350ff1119 `adapter.ts:2615` `recordString(result,"disposition") !== "handled"` fails the turn on a missing value. Fixed in e095e4b482 (legacy reply accepted, adapter test). |
| 33157 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 3 | data integrity | yes | `REASON_LINK` uses `\]\((https?:\/\/[^)\s]+)\)`, verified at 06489b40fa4c line 29; a sign-in URL with `(def)` is truncated at the first `)` and the card opens the wrong URL, dropping OAuth state. Fixed d265ad754d2 with a table row. |
| 33157 | 2 | CR | Minor | wrong | disputed | 1 | 2 | other | no | Suggests `fileUse: "safe"` on an eval case. Author ran it: it rejects correct runs (`cat code > ...`). CR withdrew. |
| 33157 | 3 | CR | Minor | nit | disputed | 1 | 3 | other | no | Eval grader gap for "enter the code" in question tools, already on main. Declined. |
| 33157 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | `trimPunctuation` strips the final `)` of a bare URL `...?state=abc(def)`. Fixed ea5d73d97fd. Same family as T1 (unverified). |
| 33157 | 5 | MS | High | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | `Open ***https://a.dev/device***` yields `/device*`. Fixed c6ee10d5586 (Macroscope first noted the fix was not on the branch head). Bot rated High; actual 2 (agent-written text, rare markup). |
| 33157 | 6 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Two spellings of the same URL count as two links, so no button. Fixed 0ed22b784b3. |
| 33157 | 7 | MS | Medium | real-minor | disputed | 1 | 3 | data integrity | no | Bare IPv6 URL in `reason` not extracted. Declined: no button, text stays visible; `url` field accepts IPv6. |
| 33155 | 1 | CR | Minor | real-minor | fixed-before-merge | 1 | 1 | UI state | no | Language picker stays open when focus leaves (keyboard). Fixed f9d99359f1 (focusout). |
| 33153 | 1 | MS | (none) | nit | fixed-before-merge | 1 | 1 | other | no | Convention: `String(error)` in log annotations. Fixed 6bf191108b. |
| 33153 | 2 | MS | (none) | nit | disputed | 1 | 2 | error handling | no | Convention: structured tagged error for fs failure. Declined, same pattern across the service; bot agreed. |
| 33153 | 3 | MS | (none) | nit | disputed | 1 | 1 | other | no | Convention on `failed` factory in a file from #33150, outside this diff. |
| 33153 | 4 | MS | (none) | nit | disputed | 1 | 1 | other | no | Same, `CliInstallError` fields. |
| 33153 | 5 | MS | (none) | nit | fixed-before-merge | 1 | 1 | other | no | Test-signal: fold assertions into the existing case. Done 5276559de2. |
| 33150 | 1 | CR | Minor | real-minor | disputed | 1 | 3 | error handling | no | `fs.realPath` on a symlinked `/bin` makes `t3 install` refuse with "Another t3 is already at...". Author: fails closed, needs an unusual layout. |
| 33150 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | install.ps1 compares PATH entries without trimming a trailing `\`, appending a duplicate and printing a wrong note. Fixed a39cbc9 with a Windows test row. |
| 33147 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Redacted API key gives a constant atom key, so a corrected key keeps showing the cached model error. Fixed 9e50bb46e2c (re-read after save). |
| 33147 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Review guide with no eligible coding agent fails with "No provider instance registered for id 'openrouter'". Fixed 565514f (clear error). |
| 33147 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Duplicate of T1. Fixed 9e50bb46e2c. |
| 33147 | 4 | MS | High | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Review-guide picker hidden when Codex is disabled for the project though Claude is enabled (selection resolved against unfiltered providers). Fixed 9e50bb46e2c. Bot rated High; settings UI only, actual 2. |
| 33147 | 5 | MS | Low | nit | fixed-before-merge | 1 | 1 | UI state | no | Duplicate placeholder options. Fixed. |
| 33147 | 6 | CR | Major | real-minor | disputed | 2 | 4 | cross-file contract | no | Shared selection allowed across environments with the same brand but different endpoints; fixed for kind and base URL, remainder (key-specific model access) declined. Left unresolved, CR accepted. |
| 33147 | 7 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Doc: where `localhost` resolves. Fixed. |
| 33147 | 8 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Doc: fallback needs Codex or Claude. Fixed. |
| 33147 | 9 | MS | High | real-minor | fixed-before-merge | 2 | 3 | race/ordering | maybe | Verified at ed03542cbccf lines 307-332: `connect()` installs `result.models` and advances the wizard without checking the draft still matches the checked config, while `save()` uses the current `config`. A model from API A can be paired with settings for API B. Fixed by disabling the form while checking (reply). |
| 33147 | 10 | MS | High | real-bug | fixed-before-merge | 4 | 4 | security | yes | Verified at 984774c536b5 `TextGenerators.ts:118-150`: `listModels` takes `input.config` (unsaved) and with `test: true` calls `connect(config)` with no allow-list check; a redacted key is replaced by the saved key (`saved?.apiKey`), so a caller-chosen base URL receives the stored secret and bypasses `providers.allowedDrivers`. Fixed 9e50bb46e2c, test added (reply). |
| 33147 | 11 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Settings search returns "Text generators" under a managed provider allow-list though the panel is omitted. Fixed d03a8d9cfab. |
| 33146 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Electron startup files (`ElectronProtocol.ts`) not in the `desktop_launch` CI gate. Fixed 011e5bc04b1 with path-table test. |

## 3. Track B (escaped bugs)

Skipped as trivial or non-source: #33149 (CI retry), #33145 (CI checkout), #33146 (CI gate), #33148 (release signing retry, CI/release script), #33226 (dependency bumps), #33193 (mobile primitive sweep, refactor-shaped, no SZZ), #33255 and #33157 (feature-adjacent "fix": new formatting/field behaviour; see Track A), #33143 (adds a 4-line mode mapper; SZZ not run, only touched lines are additions and a mock tweak: no SZZ target. Bug: agy CLI rejects `yolo`/`auto_edit` modes so Full access and Auto-accept threads failed to open; the introducing PR is whichever added the Antigravity driver, not traced).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 33268 | Background command notices queue behind a running Codex `/goal` (one run stays open until the goal ends), so the agent never learns its commands finished; 10 notices waited over 10 minutes, one 49 hours (PR body, unverified) | #29909 "fix(server): subagent questions reach a busy parent agent" (+132/-25, merged 2026-11-03; 4 blamed lines; #30323 has 1) | low | missed (CR 1 comment and Macroscope 1 review on other lines; nothing about command notices) | 3 | 4 | The steering path was added for `delegated_task` only; extending to `command` is a missing case, not a changed line. Needs knowledge that goals hold one run open. |
| 33260 | The first goal turn text "Start working toward this goal: X" makes Codex call `create_goal`, which is rejected (5 of 5 real runs, per PR body) | #25426 "fix(server): goals stop the running turn, clear while working, no echoes" (+913/-91, merged 2026-10-26; 2 of 2 blamed lines; the string was added by commit cc0b86ddf12) | high | missed (Macroscope 1 High on goal-set hang, CR 2 on other lines; none on the prompt wording) | 2 | 5 | Only a live Codex run reveals it; invisible from the diff. |
| 33213 | iPhone Duo thread header lost its sidebar toggle and gained a generic inspector toggle | #31310 "refactor(mobile): screens declare what they are..." (+3179/-5203, 210 files, merged 2026-11-05); named in the fix body | high | missed (CR about 20 inline comments, Macroscope 2; grep found none on sidebar toggle or Duo) | 2 | 4 | `AppBar` hid the toggle on the assumption that native columns show their own; `displayModeButtonVisibility="never"` elsewhere contradicts it. Cross-file assumption. |
| 33192 | Focus lost to the body when a timeline prompt control becomes disabled, not removed | #25877 "feat(web): F6 moves between workspace areas..." (+1870/-91, 45 files, merged 2026-10-28; 5 of 5 blamed lines) | high | missed (Macroscope and CR left about 15 comments on this PR; Macroscope flagged a different `disabled` focus issue on `settled:more`, none on the `recover` handler) | 2 | 3 | The recover handler checked only visibility. |
| 33189 | Mobile chat messages showed only the time even for old messages | #3101 "[codex] Add native mobile composer and markdown" (+8550/-715, 148 files, merged 2026-06-16) | medium (formatter came with the feature; it was an omission, not a regression) | missed (Macroscope 5 threads, none on timestamps) | 1 | 1 | Product gap more than a defect. |
| 33151 | Muse HTTP-error retries (429/504) were not surfaced, and a second retry chain overwrote the first row | #17082 "feat(providers): run Muse Code as a native provider" (+7366/-9, 52 files, merged 2026-10-08; 17 of 18 blamed lines) | medium | missed (CR and Macroscope about 11 comments, 0 mentioning retry or `modelRetryScheduled`) | 2 | 4 | Unhandled protocol event in a big initial provider; the reviewer needed the Muse protocol spec. |

## 4. Catalogue candidates (severity >= 3, real bugs)

| id | PR(s) | golden (a reviewer must state this) | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| text-generator-listmodels-policy-bypass | #33147 T10 | `listModels` accepts an unsaved `input.config` (and `test: true`) and connects to its base URL without checking `providers.allowedDrivers`, and swaps in the saved API key for a redacted one, so a caller can send the stored secret to an arbitrary endpoint and bypass the managed provider allow-list. | 225685a8d5a620503d7713a8e48131f567df9f6b | 984774c536b5ca4e9a23b97eb639b2b6dc737bd4 | Macroscope |
| welcome-turn-on-leaves-agent-disabled | #33209 T1 | "Turn on" sets only the top-level instance `enabled` flag, but the provider resolver also honours `config.enabled`, so an agent whose config flag is false stays disabled after the click; both flags must be set. | 965ddc1d6caec14ad5adead211fcb4e3f1f6b030 | 277b0642aff64ea7c4bce8f528fd34feedf19d5e | Macroscope |
| secret-link-markdown-paren-truncation | #33157 T1 | The `REASON_LINK` markdown-target pattern `[^)\s]+` stops at the first `)`, so a sign-in URL containing balanced parentheses is truncated and the card opens a different URL, losing OAuth state. | 0770446869d247a8b28c27d7ed93f47f8ff0c1e4 | 06489b40fa4cbb279b5d9ffcb01ff678bea36694 | Macroscope (CodeRabbit T4 found the bare-URL variant) |
| pi-legacy-tier-reply-fails-turn | #33177 T2 | The tier command check requires `disposition === "handled"`, but Pi before 0.99 replies success with no disposition, so a handled non-Standard tier fails the turn even though the extension stored it. | 357fb754fa9dae4111f0945fb8a13d30b012a62a | 00e350ff11191c0926a082e17fede319f6ed773e | CodeRabbit |
| codex-goal-command-notice-queued | #33268 (introduced by #29909) | During an active Codex `/goal` run, only `delegated_task` notices steer into the running turn; background `command` notices queue until the run ends, which can be never for a goal, so the agent is not told its commands finished. | 61c3794c32b0eeebfac09add43e403618c65d2d7 | 8fe7b265684387d4b0e1f427e5f1af8ffc86c2cf | none (escaped) |

Replay base for the last row is the base of #29909 (the introducing PR) and its last commit. Confidence is low that a diff-only reviewer could reach it.

## 5. Observations

- Macroscope's threads on #33147 (6) and #33157 (4) were mostly real and fixed with new tests. Its High ratings on UI-only or rare-markup issues (#33147 T4, T9; #33157 T5) overstate severity (actual 2); its two High findings that were truly serious (#33147 T10, #33209 T1) were right.
- CodeRabbit rated only 2 threads Major: #33177 T2 (real-bug, fixed) and #33147 T6 (partly fixed, rest declined, actual 2). Its Minor threads on docs and parentheses were mostly accurate.
- 6 of 21 Macroscope threads are rule enforcement, not bugs ("Effect Service Conventions" and "Test Signal": #33153 x5, #33209 T2). Authors fixed those touching the PR's own lines and pushed back on conventions about older files.
- Authors (agents on behalf of maintainers) decline with a reproduction or a reasoned boundary (14 disputed). Bots usually accept; CodeRabbit explicitly withdrew twice (#33213 T1, #33157 T2). One CodeRabbit suggestion was demonstrably wrong (#33157 T2, the grader would fail valid runs).
- None of the 6 traced escaped bugs had a bot comment on the defect at introduction; the main ones depended on runtime or cross-file knowledge (live Codex behaviour, `displayModeButtonVisibility`, a goal run staying open). A reviewer that reads related code outside the diff has room to add value.
