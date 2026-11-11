# Chunk 03: PRs #30910..#30679 (2026-11-06)

## 1. Header

- PRs covered: 25 (#30910 .. #30679). 18 have no bot thread at all.
- Bot threads: 27 total. CodeRabbit 25, Macroscope 2 (both PRs with Macroscope threads also had CodeRabbit). Threads by PR: #30857 x9, #30805 x6, #30747 x4, #30724 x3, #30719 x2, #30689 x2, #30798 x1.
- Verdicts: real-bug 1, real-minor 17, nit 6, wrong 3, unclear 0.
- Outcomes: fixed-before-merge 23, disputed 4 (3 of them withdrawn by the bot after the author's reply: #30805 T5, #30724 T3, #30719 T1; #30689 T2 declined by the author), ignored 0.
- Code checked: #30857 T4 (at comment commit 09491d55b7 and at merge e4ff5da0d3), #30724 T2 (merged code, `escapeLength`). Every other verdict comes from thread text, author replies and resolved/outdated flags (unverified in code).
- Track B: 18 `fix` PRs. 1 trivial (#30820 Chrome version bump). #30805 is an agent-prompt wording change (no code defect), one line only. 16 non-trivial. SZZ run on 16: 3 returned "pure addition" (#30910, #30848, #30762). Of the 13 with a blame result, 2 have no usable target (#30830, #30719: #2829 import noise) and 11 have a candidate (1 low confidence: #30834). Bot caught at intro: 1 (#30743, caught-and-ignored). Missed: 10 of 11 traced. No fix traced to an unmerged stack commit, but 3 candidate introducing PRs merged into stack branches, not main (see notes).
- No Track B bug rates severity >= 3 with a replayable introducing PR. One Track A catalogue candidate.

## 2. Track A (bot threads)

Outcome evidence: "reply" = author reply says fixed; "outdated" = GitHub flag; "withdrawn" = the bot retracted after the reply.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30857 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Mobile hook keeps `isLoading` true for a bare `#`/`!`/`@` or short query because the settled key is `""`, not `undefined`; picker stuck on "Searching...". Reply: fixed in fc87427cc7, web had the same bug (unverified in code). |
| 30857 | 2 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | other | no | First burst of typing after a trigger bypasses the debounce, one host query per keystroke. Reply: fixed 78bf2b8d27; bot confirmed. |
| 30857 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI state | no | IME confirmation Enter (keyCode 229) inserts a completion. Reply: fixed 821acf4047 on #30747. |
| 30857 | 4 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | cross-file contract | yes | `PullRequestFilterOptions.references` added as a required field; an older server omits it, so a newer client (app.t3.codes, mobile) fails to decode the whole response, breaking labels, authors and `@` completion too. VERIFIED: at 09491d55b7 contracts line 544 is `references: Schema.Array(...)` with no default; at the merge commit it has `Schema.withDecodingDefault(Effect.succeed([]))`. |
| 30857 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Long digit query (up to 100 chars) overflows GraphQL `Int` and the request fails, no suggestions. Reply: out-of-range sends 0 (78bf2b8d27). |
| 30857 | 6 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | GitLab `search` also matches descriptions; page filled with unusable rows. Fixed with `in=title`. |
| 30857 | 7 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | One failing GitLab request (Issues disabled) discards the other kind's results. Fixed per-request `catchIf`, test added. |
| 30857 | 8 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | GitHub `NOT_FOUND` for a missing exact number fails the whole query, losing prefix matches. Reply: reruns without exact lookup (dbf35c4977), test added. |
| 30857 | 9 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | UI state | no | `!` on GitHub opens an empty popup. Fixed differently (list only appears with a candidate), bot accepted the trade-off. |
| 30805 | 1 | CR | Major | nit | fixed-before-merge | 1 | 1 | other | no | CI Agent Context Budget job fails (+68 bytes). Pipeline failure, not a code defect. Fixed in 3bad363 (final fix is a 9-byte drop in the merged budget JSON). |
| 30805 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | Eval case would also pass with the old tool description. Test-strength request. Fixed 73ee8b9. |
| 30805 | 3 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | Eval grader counts calls by name, one combined card could still pass. Reply: distinct-call matching added. |
| 30805 | 4 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | Eval should require `value: null` so a direct-save call does not count as opening a card. Fixed. |
| 30805 | 5 | CR | Minor | wrong | disputed | 1 | 1 | other | no | Wants tool alternatives in `distinctCalls`. Author: exact names by design; bot withdrew. |
| 30805 | 6 | CR | Minor | nit | fixed-before-merge | 1 | 2 | other | no | A combined label plus two single labels could satisfy the eval. Fixed 49e0eeb0f6. |
| 30798 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | yes | `git@[2001:db8::1]:/srv/repo.git` falls into the plain-host alternative and yields `https://[2001/db8::1]:/srv/repo.git`, offered in the clone dialog. Outdated, addressed in 2287ce4 (not read in code). |
| 30747 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Completing a mention before existing whitespace leaves the caret right after the login, so the picker reopens and Enter/Tab re-selects. Fixed e4a7387 with test. |
| 30747 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Browser test should assert popover closure through `expect.element`. Fixed 2011268. |
| 30747 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Same defect as T1 (caret before the reused space). Fixed e4a7387. Duplicate. |
| 30747 | 4 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | UI state | no | Mention followed by a newline sends the caret to the next line. Fixed 6853658. |
| 30724 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | yes | First revision consumed an interrupting ESC as the final byte (`a ESC # ESC [31m b` rendered `a[31mb`). A bug in the PR's own new code; fixed 1717fdfcbe. |
| 30724 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Same family: a control char (LF) after intermediates was swallowed (`ESC # LF 8` lost the newline). Thread unresolved but VERIFIED fixed: merged `escapeLength` ends the sequence before any byte outside 0x30-0x7E. |
| 30724 | 3 | CR | Minor | wrong | disputed | 1 | 2 | state machine | no | Asks to retain very long intermediate-byte escapes across chunks. Author: same bounded trade-off as CSI on main; bot withdrew. |
| 30719 | 1 | CR | Minor | wrong | disputed | 1 | 2 | other | no | Split on LF only (lone `\r` also splits). Pre-existing readline behaviour, author kept `Stream.splitLines`; bot withdrew. |
| 30719 | 2 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | error handling | no | Test writes both chunks synchronously so a byte-mode PassThrough could merge them and not catch split UTF-8. Author reproduced with naive decoding; fixed 2e70711664 (object-mode stream). |
| 30689 | 1 | CR | Major | real-minor | fixed-before-merge | 1 | 2 | other | no | Test asserts a hard-coded `--base-dir` string that fails on Windows or with quoted paths. Test-only, fixed 637955d. Bot rated Major, actual severity 1. |
| 30689 | 2 | CR | Minor | real-minor | disputed | 2 | 3 | cross-file contract | no | The recovery hint reuses `resolveHostCliCommand`, whose Windows `& ""` prefix fails in cmd.exe. Author declined: shared resolver issue, other hints behave the same. |

## 3. Track B (escaped bugs)

Rows for the 16 non-trivial `fix` PRs. "Bots at intro" says what CodeRabbit/Macroscope did on the introducing PR.

| fix PR | bug | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 30910 | SSH `Include config.d/*` discovery reads dot-files (`.backup.conf`), giving a wrong hostname and a duplicate suggestion. | no SZZ target | - | - | 2 | 2 | Pure addition (one `continue` added in `expandGlob`). |
| 30848 | RTF text reader drops paragraph breaks written as a backslash before a line break. | no SZZ target | - | - | 2 | 2 | Pure addition (one `else if` branch). |
| 30834 | MCP auth span wrapped the whole tool call, polluting traces; also arguments risked landing on the span. | #17130 (feat @-mention a machine; base `t3code/peer/agent-link`, stack branch) | low | missed (bots flagged other items: composer drafts, mobile queued edit) | 1 | 4 | SZZ weights are 4 lines in the middleware, but the `Effect.fn` wrapper dates from the June refactor (f7c422d5815). Observability only. |
| 30830 | A stopped run's late checkpoint recorded baselines with the next run's node id and time (queued or post-Stop message re-creates the scope first). | no usable target | - | - | 3 | 5 | SZZ blames #2829 (import, `input.scope.nodeId`/`createdAt`) and #26901 (side chats; touches only `forceMissing: sideChat`). The race only matters once runs queue; no single introducing PR. |
| 30798 | Switching an IPv6 SCP/SSH/HTTPS clone URL produced `https://[2001/db8::1]:org/repo.git`. | #23170 (clones retry over HTTPS when SSH is refused) | medium | missed: no bot comments on #23170 | 2 | 3 | Original host regexes forbade colons. #24005 only edited two of the lines (CodeRabbit commented there at `cloneUrl.ts:47`, topic not read). |
| 30743 | Git config parser accepted unfinished quoted continuations (`core.bare` read at onboarding). | #30174 (read continued `core.bare` values) | high | caught-and-ignored: CodeRabbit flagged "Reject unterminated quoted values at EOF" on git.ts:194; author confirmed with Git and deferred it to #30743 | 2 | 2 | Fix-of-fix, merged 3 days apart. Thread left unresolved on #30174. |
| 30762 | `/tmp/...` shortened paths became broken file chips. | no SZZ target | - | - | 2 | 2 | Pure addition (new elision pattern). |
| 30726 | Sanitized stack frames with a query lost `:line:col`. | #3405 (sanitize client error log diagnostics) | medium | missed: no bot comments (June PR, unverified why) | 1 | 3 | Single blamed line `return url.toString()`. |
| 30724 | Valid ESC sequences with intermediates (`ESC # 8`, `ESC % G`, `ESC SP F`) printed their final byte as text. | #15094 (command output streams live) | medium | missed: Macroscope and CodeRabbit left 15+ threads on `terminalOutput.ts` (cursor move, SOS, resync) but none on intermediates | 2 | 3 | SZZ also names #21514 (comment refactor): noise. |
| 30721 | `t3 thread` project path `~/repo` was not expanded. | #22732 (`t3 thread` CLI) | medium | missed: bots flagged other `resolveProject` defects (`..notes`, symlink root) | 2 | 2 | One blamed line in `resolveProject`. |
| 30719 | MCP bridge split JSON-RPC messages on U+2028/U+2029 (readline), failing tool calls whose arguments contain them. | no usable target | - | - | 3 | 3 | Readline framing arrived in #2829 (import); #31028 only renamed a diagnostics comment. Not replayable. |
| 30717 | Review-guide excerpt patches dropped CRLF and no-newline-at-EOF markers; EOF-only changes hidden, expansion rebuilt wrong old side. | #18124 (guided reviews) | medium | missed: 13 bot threads on #18124, none on line terminators (thread list grepped) | 2 | 3 | Five blamed lines in `rowsToPatch`/`excerptExpansionOldContents`. |
| 30706 | Reopening a closed folder tab lost its breadcrumb trail. | #15207 (reopen closed tabs) | medium | missed: bots flagged failed-close history and malformed persisted payload, not `folderTrail` | 2 | 3 | One blamed line in `reopenClosedView`. |
| 30701 | Clipped fx replies ending in a literal `\u...` text were damaged by the partial-escape repair. | #18277 (add Vercel fx as a provider) | medium | missed: bots commented only on marketing grid and skills discovery | 2 | 3 | Regex repair applied before trying a plain decode. |
| 30689 | `t3 pair --base-dir /x` hint told the user to run `npx t3 serve` without `--base-dir`. | #4955 (`npx t3 pair`) | medium | missed: Macroscope flagged other pair.ts defects (devUrl hostname, pid check); #22855 alt (CodeRabbit Major on service boundary, unrelated) | 2 | 2 | Hint string dates from #4955; #22855 added the worktree note. |
| 30686 | Forgejo author filter paginated the unpaginated assignees endpoint: 34 requests for 3 users, duplicate rows, false truncation. | #23924 (label and author filters search the host; base `t3/pr-filter-fill`, stack branch) | medium | missed: CodeRabbit flagged pagination on the `users/search` branch ("Preserve pagination status for author search"), not the `/assignees` read | 2 | 3 | Same class as #23580, which fixed it for the reviewer picker (merged 2026-10-31). |
| (trivial) | #30820 Chrome version bump for the preview browser: no SZZ. #30805 agent tool description wording for `request_secret` (prompt text, SZZ blames #30257 into stack `t3/secret-request-evals`): no code defect, no SZZ follow-up. | - | - | - | - | - | - |

## 4. Catalogue candidates (severity >= 3, real-bug)

- id: `pr-filter-options-references-skew`
  - PR: #30857 (Track A T4, fixed before merge; merges into main).
  - Golden: "`PullRequestFilterOptions` makes the new `references` array a required field with no decoding default, so a newer client talking to an older server fails to decode the whole filter-options response and loses label, author and mention completion too."
  - base: `42a0e917cf89df34b48c7106b7753e12830036a4`
  - head (commit the bot commented on, still has the bug): `09491d55b7ccdd4636cdcaa10bc101bb6da9fbca`
  - caught by: CodeRabbit (Major, resolved in 78bf2b8d27).

No Track B escaped bug in this chunk is both severity >= 3 and traceable to an introducing PR. Near misses: #30830 and #30719 (severity 3, but SZZ lands on the #2829 import).

## 5. Observations

- CodeRabbit dominated: 25 of 27 threads. Its severity labels were inflated for test and CI matters (#30805 T1 Major = CI budget gate, #30689 T1 Major = test quoting).
- Macroscope produced the 2 threads that were real UI defects (#30857 T1, #30747 T1), both the caret/loading class; CodeRabbit reported the same caret defect separately (#30747 T3), so the pair duplicated.
- No thread was ignored: the authors replied to nearly all and fixed 23 of 27; CodeRabbit withdrew 3 after replies. The one thing that stayed open is the cmd.exe hint, declined with a reason.
- Missed at intro in 10 of 11 traced fix PRs: bots reviewed the PR but flagged other lines. Typical escapes are small edge cases in parsers (terminal escapes, IPv6 URLs, EOF/CRLF, `\u` clipping), which bots rarely probe unless asked.
- Track A behaviour that recurs: bots caught the PR's own first-revision bugs in the escape-sequence parser (#30724 T1/T2), while the same file's older code (#15094) got many other threads but not this gap.
