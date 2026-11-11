# Chunk 01: PRs #34106..#33867 (2026-11-10)

## 1. Header

- PRs covered: 25 (#34106 .. #33867). 15 have no bot thread at all.
- Bot threads: 56 total. CodeRabbit 34, Macroscope 22. #34007 alone has 31 (16 CR, 15 MS); #33943 has 12.
- Verdicts: real-bug 23, real-minor 29, nit 3, wrong 1, unclear 0. Of the 23 real-bug, 18 are stale-push threads of #34007 (T7-T13, T15-T25, see Observations); 5 are genuine defects in the PR's own code (#34007 T14, T29, T31; #33950 T2; #33943 T1).
- Outcomes: fixed-before-merge 48 (18 of them on #34007 are fixed only because the branch was rebuilt, and 6 more there because the file was removed), ignored 3 (#33982), disputed 4, unknown 1.
- Code checked at merge commits: #33943 T1 (ThreadFeed.tsx:2897 now tests `presentation.path`), #34007 T29/T31 (`prove-scenario.ts` requires exactly one executed test, skip handled), #33994 T1 (test expects "2m 0s"), #33950 T3 (`skipIf(windowsHost)`). Everything else is judged from the thread, replies and resolved/outdated flags: "(unverified)".
- Track B: 17 `fix` PRs; 8 traced with SZZ (#34094, #34087, #34017, #34016, #34011, #34003, #34020, #33982), 9 skipped as trivial or feature-adjacent. Bots at the introducing PR: caught 0, missed 5, did-not-run 1, not checked 2.
- Caveat: the code of #34007 T7-T25 cannot be read (a rebuilt branch dropped the stale head); those verdicts rest on the author's reply "an earlier push carried stale copies of unrelated files" plus the bot text (unverified in code).

## 2. Track A (bot threads)

"fixed-before-merge" on removed code means the thread became outdated because the file left the diff.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 34073 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Pending cloud sheet kept after cloud capability disappears. Resolved, reply "Fixed in 6a6cf78432" (unverified in code). |
| 34020 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Cancelling image generation replaced the row input with `{}`. Resolved, author reproduced and fixed in 86d2045983 (unverified in code). |
| 34007 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | race/ordering | no | `focused` expectation can pass after its deadline. Obsolete: runner file removed (unverified). |
| 34007 | 2 | MS | High | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Failed screenshot on rerun attaches the previous run's PNG as evidence. Dev tool only, obsolete: file removed (unverified). |
| 34007 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | resource leak | no | `log.end()` before readers stop can raise write-after-end. File removed; CR withdrew (unverified). |
| 34007 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | error handling | no | Upload failure throws before proof files are written. File removed; replacement catches upload errors (CR confirmed). |
| 34007 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | error handling | no | `chromium.launch()` outside `try` leaks temp home and exits with the wrong code. File removed (unverified). |
| 34007 | 6 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | race/ordering | no | Expectation poll not bounded (same as T1). File removed (unverified). |
| 34007 | 7 | MS | Medium | real-bug | fixed-before-merge | 2 | 2 | other | no | Stale push reverted the drag-title lookup (dragging a hidden search result shows "Thread"); same defect #34017 later fixed on main. Author: stale copies, branch rebuilt. Unverified in code. |
| 34007 | 8 | MS | Medium | real-bug | fixed-before-merge | 2 | 2 | other | no | Stale push removed `expandHomePath`, WSL `~` paths wrong. Stale copy (reply); unverified. |
| 34007 | 9 | MS | Medium | real-bug | fixed-before-merge | 3 | 2 | other | no | Stale push removed opencode `todowrite` projection, so no `todo_list` plan. Stale copy; unverified. |
| 34007 | 10 | MS | High | real-bug | fixed-before-merge | 3 | 2 | other | no | Stale push removed `canOpenApp`, so `.app` links open the editor instead of launching. Stale copy; unverified in code. |
| 34007 | 11 | MS | High | real-bug | fixed-before-merge | 3 | 2 | other | no | Stale push dropped the suffix-match fallback for `cloud/http.ts` style links. Stale copy; unverified. |
| 34007 | 12 | MS | Medium | real-bug | fixed-before-merge | 3 | 2 | other | no | Stale push lost projection of failed image-generation completions. Stale copy; unverified. |
| 34007 | 13 | MS | Medium | real-bug | fixed-before-merge | 2 | 2 | other | no | Stale push dropped Carbon quota label branch. Stale copy; unverified. |
| 34007 | 14 | MS | High | real-bug | fixed-before-merge | 3 | 5 | cross-file contract | maybe | Scenario with REPLAY model still calls the developer's real model for thread titles because `acpRegistry` is rejected by `selectionSupportsTextGeneration` and swapped for a fallback. Author "Confirmed and fixed in c642ff3400"; code unverified. |
| 34007 | 15 | MS | High | real-bug | fixed-before-merge | 3 | 2 | other | no | Stale push broke `:42-64` / `#L42-L64` links (same regex change CR T25 sees). Stale copy; unverified. |
| 34007 | 16 | CR | Minor | real-bug | fixed-before-merge | 2 | 2 | other | no | Stale push removed home expansion for file-manager targets. CR withdrew after the branch was rebuilt. |
| 34007 | 17 | CR | Minor | real-bug | fixed-before-merge | 2 | 2 | other | no | Stale push made `ScratchUnavailableError` message non-actionable. Stale copy; unverified. |
| 34007 | 18 | CR | Minor | real-bug | fixed-before-merge | 2 | 3 | error handling | no | Stale push swallows scratch-probe failures with no log. Stale copy; unverified. |
| 34007 | 19 | CR | Minor | real-bug | fixed-before-merge | 2 | 2 | other | no | Stale push merged Carbon and default Gemini quota labels. Stale copy; unverified. |
| 34007 | 20 | CR | Minor | real-bug | fixed-before-merge | 3 | 3 | data integrity | no | Stale push carries an older `model-manifest.json` `updatedAt`, so disk-cached newer manifest overrides it and removed models linger. Stale copy; unverified. |
| 34007 | 21 | CR | Minor | real-bug | fixed-before-merge | 2 | 3 | UI state | no | Stale push removed scoped resize path in timelineViewport (the area #34003 later changed). Stale copy; unverified. |
| 34007 | 22 | CR | Minor | real-bug | fixed-before-merge | 2 | 3 | UI state | no | Stale push dropped focus fallback in PreviewPanelShell. Stale copy; unverified. |
| 34007 | 23 | CR | Minor | real-bug | fixed-before-merge | 2 | 2 | other | no | Same as T7 (drag title), second bot. Stale copy; unverified. |
| 34007 | 24 | CR | Minor | real-bug | fixed-before-merge | 2 | 3 | state machine | no | Stale push dropped completed command-output cache (#34002 area). Stale copy; unverified. |
| 34007 | 25 | CR | Minor | real-bug | fixed-before-merge | 3 | 2 | other | no | Same as T15, with a concrete failure: chip opens literal `a.ts:42-64`. Stale copy; unverified. |
| 34007 | 26 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Uncaught errors in `prove-scenario.ts` exit 1 (not proven) instead of 2 (could not run). "Fixed in c642ff3400", CR rechecked. |
| 34007 | 27 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Upload failure discards proof files; index pairing of URLs and captures. Fixed c642ff3400. |
| 34007 | 28 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | resource leak | no | `devices.boot()` rejection after `allocate()` leaves the pooled device leased. Fixed c642ff3400 (unverified in code). |
| 34007 | 29 | MS | Low | real-bug | fixed-before-merge | 3 | 3 | cross-file contract | yes | A test skipped at runtime exits 0, so `readSide` reports it "passed" and the scenario is "Proven". Verified: merged file comments "e2e exits 0 for a skipped test too" (prove-scenario.ts:89). Bot rated Low, actual 3 for a tool whose output is proof. |
| 34007 | 30 | MS | High | real-minor | disputed | 2 | 3 | race/ordering | no | Concurrent iOS runs share `.t3/scenarios-mobile`. Author: one run per checkout by design; doc updated. MS accepted. |
| 34007 | 31 | MS | High | real-bug | fixed-before-merge | 3 | 3 | cross-file contract | yes | `readSide` ignores every executed test after the first, so a multi-test file can be "Proven" while another test fails. Verified: merged code requires `executed.length === 1` (prove-scenario.ts:69-76). |
| 34006 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Mobile inline-file regex rejects `src/http.ts:42-64` before the shared parser. Fixed acc1c8eece6 with tests. |
| 34006 | 2 | CR | Minor | wrong | disputed | 1 | 2 | other | no | Wanted hash ranges in inline code on mobile. Author: inline `#L` was never a link form; CR withdrew. |
| 33994 | 1 | CR | Major | real-minor | fixed-before-merge | 1 | 1 | other | no | Mobile test still expects "2m" after formatter change. Verified: merged test expects "2m 0s". A CI failure, not a defect; Major overrated. |
| 33982 | 1 | CR | Minor | nit | ignored | 1 | 2 | UI state | no | Add live-region announcement for steer status change (mobile). Unresolved, merged (unverified). |
| 33982 | 2 | CR | Minor | real-minor | ignored | 2 | 4 | state machine | maybe | `continuesSteer` hides the waiting marker on a later pending steer when the first of a group completes. Unresolved (unverified). |
| 33982 | 3 | CR | Minor | nit | ignored | 1 | 2 | UI state | no | Same live-region request on web. Unresolved. |
| 33957 | 1 | CR | Minor | real-minor | unknown | 1 | 2 | other | no | Highlighting an unbounded command may be slow on mobile. Outdated, no reply (unverified). |
| 33950 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | other | no | `~/Applications/Foo.app` passed literally to `open`. Fixed 6d4190173c with tests (reply). |
| 33950 | 2 | CR | Minor | real-bug | fixed-before-merge | 3 | 3 | security | maybe | Signed icon URL for a caller-chosen `app-path` required only `orchestration:read`, so a read-only client could probe icons of private host bundles. Fixed e3e8b78c01 (filesystem:read for path icons). Code unverified; reply describes the change. |
| 33950 | 3 | CR | Major | real-minor | fixed-before-merge | 1 | 1 | other | no | POSIX launcher test not skipped on Windows. Verified: merged test uses `it.effect.skipIf(windowsHost)` (externalLauncher.test.ts:99). Bot Major, actual 1. |
| 33949 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI state | no | Tile empty while local preview loads. Fixed 4746607202 with test (reply). |
| 33943 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 3 | cross-file contract | yes | Mobile link `/repo/src/config.ts:5` or `./src/config.ts:5`, if missing, opened an unrelated suffix match. Verified: merged ThreadFeed.tsx:2897 checks `presentation.path`. MS could not see the fix commit (see Observations). |
| 33943 | 2 | MS | Medium | real-minor | fixed-before-merge | 1 | 2 | other | no | Eval grader keeps `#L4` in lookup. Fixed 821239a0486 (eval-only). |
| 33943 | 3 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | Duplicate of T2. |
| 33943 | 4 | MS | Medium | real-minor | fixed-before-merge | 1 | 2 | other | no | Inline-code label counted as two pills in the grader. Fixed 5c17abbfdae. |
| 33943 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | `~/repo/src/config.ts` passes the lookup gate; a missing file opens another package's file. Fixed 31ce4997947 in shared `workspaceLinkLookupQuery` (unverified in code). |
| 33943 | 6 | MS | Medium | real-minor | fixed-before-merge | 1 | 2 | other | no | Grader compares basenames case-sensitively. Fixed c7cc38e4b7f. |
| 33943 | 7 | MS | Medium | real-minor | fixed-before-merge | 1 | 2 | other | no | Grader does not normalise `./` segments. Fixed c7cc38e4b7f. |
| 33943 | 8 | MS | Medium | real-minor | fixed-before-merge | 1 | 2 | other | no | Grader counts fenced examples as links. Fixed 88818d820ba. |
| 33943 | 9 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | Grader drops links under a non-home cwd such as /tmp. Fixed c6f7316ac32. |
| 33943 | 10 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | other | no | Links in inline code counted (fixed 16064865b21); media-image half rejected by author, CR withdrew. |
| 33943 | 11 | CR | Minor | nit | disputed | 1 | 4 | other | no | Escaped backticks around a link: author declines (regex grader, rare). CR accepted. |
| 33943 | 12 | CR | Minor | real-minor | disputed | 1 | 3 | other | no | Media previews graded against literal paths: fixed a99935c985b; `report.pdf#L4` edge left (grader fails safe). |

## 3. Track B (escaped bugs)

Fix PRs skipped as trivial or non-source: #34095 (CSS centring), #33994 (duration text, "12m" to "12m 0s"), #33964 and #33867 (tests, not fixes). Feature-adjacent, no SZZ: #34006 (range regex, pure widening), #33991 (recognise a new Gemini model), #33990 (new drag target), #33957 (mobile highlighting), #33950 (app icons and open action), #33949 (follow-up polish to #28499 named in its body), #33943 (rework of the link resolver after an audit showing 24% broken Claude links; no single origin).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 34094 | Desktop `ipcMain` handlers answered any webContents, including preview guests that load arbitrary pages, because no sender check existed | #3203 "[codex] Normalize Desktop IPC Effect service" (+78/-77, 9 files, merged 2026-06-20) is what SZZ blames (3 lines of signature/import) | low | missed (Macroscope reviewed #3203 with no inline comment; CR none) | 4 | 4 | The blamed PR is a refactor; the real origin is the ipcMain handler plus the preview-guest feature, not identified. The fix is mostly new code. Security class. |
| 34087 | `onProgress` divided `bytesSent / totalBytes`, but native Int64 events arrive as BigInt, so larger images threw a BigInt mixing error and the attach crashed | #8978 "feat(mobile): upload attachments while composing" (+1625/-121, 24 files, merged 2026-09-01); the single blamed line is the `totalBytes > 0` handler | high | missed (Macroscope 6 inline comments on the queue and drafts, none on progress) | 3 | 5 | Needs runtime knowledge of expo-modules-jsi, and that the TS type says `number`. A type-correct line; invisible in the diff. |
| 34017 | Dragging a search result from a collapsed shelf showed "Thread" instead of its title (`threadByKey` lacks hidden rows) | #28016 "fix(web): sidebar search results can be dragged onto the composer" (+73/-52, merged 2026-11-08); SZZ blamed #2829 (noise), origin found with `git log -S contextDragKeyRef` | medium | bots-did-not-run (no bot reviews, only the author) | 1 | 3 | A cosmetic miss. Bots on #34007 (stale revert) flagged the same defect, MS T7 and CR T23. |
| 34016 | A cancelled run that had started was not a handoff source, so a provider switch lost its context | #2829 (blame only; `isHandoffSourceRun` from the orchestrator import) | low | not checked (380k-line import, noise) | 3 | 4 | Condition needs `cancelled && startedAt !== null`: state-machine knowledge. No better origin found. |
| 34011 | "Earlier output not shown" notice sat outside the scroll area, so it did not scroll with logs | #15094 "fix: command output streams live while it runs" (+3287/-41, merged 2026-10-16); 27 blamed lines | medium | missed (CR Critical on a TS2367 error in `thread-command-output.tsx`, MS High on ws.ts; none on notice layout) | 1 | 1 | Layout nit, visible in one hunk. Bots found other issues on the same file. |
| 34003 | A focused HTML preview whose accordion expands resizes its row, so the follow-bottom logic dragged the reader to the end | #25463 "fix(web): find shows its match after a thread switch ... one viewport signal" (+1164/-731, merged 2026-10-26); 2 blamed lines | low | missed (Macroscope commented on `useTimelineFollow.ts:386`, not on frame resizes) | 2 | 4 | Real origin is likely the HTML-render iframe feature; SZZ cannot see it (the fix is mostly new code). Needs iframe message-timing knowledge. |
| 34020 | Codex image-generation notifications never appeared in the timeline as tool calls | #19066 "fix(server): Codex generated images show in chat ..." (merged 2026-10-30); 4 blamed lines | medium | missed (CR and MS left about 14 comments there on images; none on tool-item visibility, unverified) | 2 | 3 | A missing feature path, not a regression. Fix is 90% new code. |
| 33982 | Pi steer messages are stored "completed" when offered, so a steer behind a long command shows steered instead of waiting | #2829 (blame only; 1 line) | low | not checked | 2 | 4 | Pure addition of a `steer.updated` event; no SZZ target. |

## 4. Catalogue candidates (real bug, severity >= 3)

All three need a replay head from before the fix commit; the "head" below is the PR's real last commit, which already contains the fix. Replay should use the parent of the fix commit named (unverified).

1. `scenario-proof-false-proven` (#34007 T29 + T31). Golden: the proof script treats a side as passed whenever the e2e run exits 0, so a runtime-skipped test, or a file whose second test fails, is reported "Proven". Base d756fed7aa, head 00bd944d93489ac7c926e767b15381b482600024 (bug present before c642ff3400 and 00bd944d93). Caught by: Macroscope (T29 Low, T31 High).
2. `scenario-replay-falls-back-to-real-model` (#34007 T14). Golden: the `devReplay` ACP driver is not a text-generation provider, so background thread-title generation is routed to the developer's real provider while the scenario claims a replay model. Same base and head as 1 (bug before c642ff3400). Caught by: Macroscope. Replay: maybe (needs cross-file reading).
3. `file-link-authored-path-suffix-match` (#33943 T1, with CR T5). Golden: when a cited path such as `/repo/src/config.ts:5`, `./src/config.ts:5` or `~/repo/src/config.ts` does not exist, the workspace suffix lookup still runs on the stripped relative path and opens an unrelated `packages/other/src/config.ts`. Base 80e62619f5, head a99935c985b235b7b739ac778de7f2eab783029d (bug before 821239a0486 and 31ce4997947). Caught by: Macroscope (T1 High) and CodeRabbit (T5).
4. `app-icon-path-needs-filesystem-scope` (#33950 T2). Golden: signed-URL icon requests for a caller-supplied `app-path` need `filesystem:read`, not only `orchestration:read`. Base 1fed70cd19998cee7907f6fde3b4d4290ba99cfc, head e3e8b78c01a4259d4bbe06e1764e1ddc55c0d1c3 (that commit is the fix; pre-fix head 6d4190173c is the one CR reviewed). Caught by: CodeRabbit. Replay: maybe.
5. `stale-branch-reverts-main` (#34007 T7-T25). Golden: the PR diff silently reverts unrelated recent main changes (e.g. file-link range patterns, `.app` handling, `model-manifest.json` timestamp). Base: d756fed7aa (not the stale push's base). Head: not recoverable (the branch was rebuilt; bot permalinks cite e26b1e9ab2, unverified). Caught by: both bots, 18 threads. Replay: no, unless the stale head is recovered from GitHub's PR refs.

## 5. Observations

- #34007 is the standout: after a bad push that carried stale copies of unrelated files, both bots flagged 18 regressions the author never wrote, including Macroscope High findings on links and `.app` handling. This is bot value that no per-hunk metric shows: they noticed a diff that undid main.
- Macroscope fix-verification is unreliable here: on #33943 and #34007 it answered "I couldn't verify, commit not available on the branch" for six fixes whose commits the author had pushed (T1, T2, T4, T7, T8 on #33943 and T31 on #34007). CodeRabbit re-read the commit and confirmed each time.
- Severity labels drift in both directions: CR Major on a mobile test expectation (#33994) and on a Windows skipIf (#33950) were actual severity 1; Macroscope Low on the skipped-test false "Proven" (#34007 T29) was a 3.
- CodeRabbit accepted pushback and withdrew in every disputed thread (#34006 T2, #33943 T10-T12), so author replies are reliable ground truth for "wrong" verdicts.
- Bots did not run, or left nothing, on #28016, which introduced the "Thread" drag-title bug; Macroscope reviewed #3203 (the refactor SZZ blames for the desktop IPC bug) without an inline comment. Both Track B escapes with a clear origin (#34087 and #34017) have no bot comment on the defective line.
