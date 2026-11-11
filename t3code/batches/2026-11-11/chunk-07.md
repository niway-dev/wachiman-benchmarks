# Chunk 07: PRs #22997..#21676 (2026-11-11)

## 1. Header

- PRs covered: 25 (#22997 .. #21676), all `fix(...)`. 4 have no bot thread (#22948, #22553, #22347, #21897).
- Bot threads: 72 total. CodeRabbit 56, Macroscope 16.
- Verdicts: real-bug 8, real-minor 45, nit 14, wrong 5 (all withdrawn by CodeRabbit after an author rebuttal), unclear 0. Most are judged from thread text, see "(unverified)".
- Outcomes: fixed-before-merge 40, ignored/no reply 27, withdrawn after rebuttal 5, disputed 0.
- Code checked at the merge commit: #22755 T2 (busy error missing from the early-return list, confirmed), #22997 T6 (no horizontal-rule check in `parseListPrefix`, confirmed by reading), #22208 T1 (`Number(raw)` gone at merge, so fixed). All other verdicts come from thread text, replies and resolved/outdated flags (unverified in code).
- Track B: 25 fix PRs, 23 SZZ runs (#22997 and #22226 pure additions, #22836 only #2829 noise, #22960 not run). Several targets are low confidence. Time: about 40 minutes (SZZ run 3 at a time).
- Caveat: PR numbers in this chunk are not merge-ordered (a fix numbered #22xxx can blame a PR numbered #28xxx). Dates below are merge dates from `gh`.

## 2. Track A (bot threads)

Outcome evidence: "reply" = author reply says fixed; "outdated+resolved" = flags; "none" = unresolved, no reply, merged anyway; "withdrawn" = author rebutted and the bot withdrew.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | one-line finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 22997 | 1 | CR | Minor | real-minor | ignored | 1 | 4 | race/ordering | no | Composition ends without a transaction, so a pending list paragraph stays literal (unverified). |
| 22997 | 2 | CR | Minor | real-minor | ignored | 2 | 4 | cross-file contract | no | Wrapped list not joined with an adjacent compatible list, so editor differs from the Markdown rebuild (unverified). |
| 22997 | 3 | MS | Medium | real-minor | ignored | 1 | 2 | other | no | Evidence script ignores `--theme` when storage state sets a theme (unverified). |
| 22997 | 4 | MS | Medium | real-minor | ignored | 1 | 1 | error handling | no | Evidence script exits 0 after a failed row (unverified). |
| 22997 | 5 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Shift-Backspace cannot undo the list input rule. Outdated+resolved ("no longer relevant as of 2f1053ae"). |
| 22997 | 6 | MS | High | real-minor | ignored | 2 | 4 | cross-file contract | maybe | `* *` edited to `* * *` is wrapped as a bullet list, but the Markdown rebuild reads it as a horizontal rule. Checked: `parseListPrefix` (line 606) accepts `*` bullets and the normalizer (line 682) has no horizontal-rule exclusion. Rare input, so sev 2. |
| 22996 | 1 | MS | Medium | real-minor | ignored | 1 | 1 | resource leak | no | Evidence script rejects unknown fixture after launching Electron, leaving processes holding the lock (unverified). |
| 22996 | 2 | CR | Minor | real-minor | ignored | 1 | 2 | other | no | Evidence script F2 may send `window.close()` to a foreign CDP port 9333 (unverified). |
| 22996 | 3 | CR | Major | real-minor | ignored | 1 | 2 | error handling | no | F2 can hang if CDP close fails; script only, not product (unverified). Bot Major is inflated. |
| 22996 | 4 | CR | Minor | real-minor | ignored | 1 | 1 | error handling | no | Duplicate of T1. |
| 22993 | 1 | MS | Medium | real-minor | ignored | 1 | 2 | data integrity | no | Fixture script overwrites edited widget sources on reapply (unverified). |
| 22993 | 2 | CR | Major | nit | fixed-before-merge | 1 | 1 | other | no | Knip reports the script unused (CI log). Outdated, thread resolved by registering it (unverified). |
| 22993 | 3 | CR | Minor | real-minor | ignored | 1 | 2 | data integrity | no | Same as T1 (unverified). |
| 22993 | 4 | CR | Minor | real-minor | ignored | 1 | 2 | error handling | no | Hook check should run before file writes in the fixture script (unverified). |
| 22964 | 1 | CR | Minor | real-minor | ignored | 2 | 4 | state machine | maybe | A suppressed `Stop says:` notice is not recorded in `noticeTexts`, so a repeated copy in the final result can become fallback assistant text (unverified). |
| 22960 | 1 | CR | Minor | wrong | withdrawn | 1 | 3 | race/ordering | no | Stale find results: author showed Chromium already drops them; CR withdrew. |
| 22960 | 2 | CR | Minor | wrong | withdrawn | 1 | 2 | other | no | Bare-key find shortcuts: filter is deliberate (page typing); CR withdrew. |
| 22960 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | AltGraph guard lost on the forwarded key path. Fixed in 942aeb092e. |
| 22960 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | UI state | no | Find input focus stolen by the closing command palette when the bar was already open. Author first refused, then reproduced in the dev app and fixed in d4971487a0. Good bot catch. |
| 22960 | 5 | CR | Minor | real-minor | ignored | 2 | 3 | cross-file contract | no | Cmd+F consumed with no action on draft routes when toolbar has focus. Author: shared limitation of all preview shortcuts, deferred. |
| 22960 | 6 | CR | Minor | wrong | withdrawn | 1 | 4 | UI state | no | Same focus concern as T4; author explained effect ordering; CR withdrew. |
| 22960 | 7 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Find query lost when switching runtime tab. Fixed in 9ef9043599. |
| 22947 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | maybe | `queue.resume` after Stop would wrongly keep the old work timer start. Outdated, no reply (unverified fix). |
| 22947 | 2 | MS | Low | nit | ignored | 1 | 1 | error handling | no | Verify script ignores a nonzero CLI exit (unverified). |
| 22947 | 3 | MS | High | real-bug | ignored | 2 | 4 | cross-file contract | maybe | Ordinary MCP message from an app-owned child whose settled relationship is filtered out resets the parent's work timer (projection uses `omitSettledSubagents: true`). Not outdated, unresolved, merged. Not verified in code. Cosmetic (a timer), so sev 2. |
| 22874 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | Enter advances a non-final question without the Submit button's guards. Outdated (unverified fix). |
| 22874 | 2 | MS | High | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | maybe | `/side explain this` typed in a custom answer advances the question instead of opening side chat. Outdated, no reply. Merged file still has the `/side` and `/btw` command handling in ChatComposer (line 1911), so likely handled (unverified). |
| 22861 | 1 | CR | Major | wrong | withdrawn | 1 | 3 | data integrity | no | `gh-merge-base` forms `refs/heads/dev`, `origin/dev` and cache key. Author (Claude on Theo's behalf) showed T3 only writes bare branch names; CR withdrew both. |
| 22839 | 1 | MS | Medium | real-minor | fixed-before-merge | 2 | 2 | error handling | no | Disabled instance still ran the CLI probe (10 s). Fixed 4538f006 with test. |
| 22839 | 2 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | data integrity | no | Only `127.0.0.1` treated as loopback, not 127.0.0.0/8. Fixed 4538f006. |
| 22839 | 3 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | Restart instruction not shown on the success path. Outdated+resolved (fixed later, shown via messages; unverified). |
| 22839 | 4 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | cross-file contract | no | Toast lost the environment label. Fixed e68919d295. |
| 22839 | 5 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | 1.x server with a 2.x CLI selected the wrong updater (`opencode-ai` instead of `@opencode/cli`). Fixed 72c414bb20 with test. |
| 22839 | 6 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | cross-file contract | no | "Already up to date" skipped the restart advice. Fixed 72c414bb20. |
| 22836 | 1 | CR | Minor | real-minor | ignored | 2 | 1 | other | no | Evidence script writes `ANTHROPIC_AUTH_TOKEN` in plaintext into the evidence dir (unverified). |
| 22755 | 1 | MS | none | nit | fixed-before-merge | 1 | 2 | other | no | Busy rejection should be a structured tagged error. Outdated, resolved (6b3bdce4a6). |
| 22755 | 2 | CR | Major | real-bug | ignored | 3 | 3 | race/ordering | yes | The new `OrchestratorProviderSelectionBusyError` is not in the early-return list of `dispatchWithReceiptEffect`, so it is committed as a rejected receipt and a retry with the same commandId gets "previously rejected" after the turn ends. Checked at merge 94f54a5710: early-return list (lines ~14083-14084) names only the mode-limit and ceiling errors; the busy tag is absent. Unresolved at merge. |
| 22425 | 1 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | state machine | yes | Held queue releases when the limited provider reports `resetAt: null`, retrying a provider that is still limited. Outdated+resolved (unverified fix). |
| 22425 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Unparseable `resetAt` gives `NaN` and lifts the hold. Fixed f42e7da. |
| 22349 | 1 | MS | Medium | real-minor | fixed-before-merge | 1 | 3 | UI state | no | ResizeObserver fractional width causes a render loop. Outdated (unverified fix). |
| 22239 | 1 | MS | Medium | real-minor | ignored | 2 | 4 | cross-file contract | no | Reference-link definitions in another segment are lost when a message is split around an insight (unverified). |
| 22239 | 2 | MS | Medium | real-minor | ignored | 2 | 3 | data integrity | no | A four-space-indented `★ Insight` is extracted as a callout instead of staying code (unverified). |
| 22239 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Line breaks lost in ordinary segments. Fixed 104c8c4. |
| 22226 | 1 | CR | Major | real-minor | ignored | 2 | 5 | cross-file contract | no | A UNC path from WSL distro B picked in a picker targeting A clones in A with a bare path (unverified). WSL-specific. |
| 22226 | 2 | CR | Minor | real-minor | ignored | 2 | 4 | race/ordering | no | Picker result applied after the flow changed; failed submit keeps old destination (unverified). |
| 22226 | 3 | CR | Minor | real-minor | ignored | 1 | 3 | data integrity | no | `.trim()` drops trailing spaces in folder names (unverified). |
| 22226 | 4 | CR | Minor | nit | ignored | 1 | 1 | other | no | Wants a regression test. |
| 22208 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 3 | data integrity | yes | German locale: Enter on `1.000` saved 1 day instead of 1000, so retention could delete artifacts early (`Number(raw)` on localized text). Checked: no `Number(raw)` in the merged file (grep empty at fcddd737e2), so fixed before merge. Comment commit 095182815f. |
| 22208 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | error handling | no | A failed scoped save leaves "holding" mode on. Outdated (unverified fix). |
| 22208 | 3 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | UI state | no | `pointerInsideRef` not cleared on pointer leave. Fixed 87649a2. |
| 22208 | 4 | CR | Major | real-minor | fixed-before-merge | 2 | 2 | other | no | Ref written during render breaks React Compiler coverage test (CI). Fixed c72a309. |
| 22208 | 5 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | state machine | yes | Draft survives a settings-scope change, so the previous scope's age can be saved to the new scope. Fixed 8fb4132. |
| 22208 | 6 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Pending Off save completing wipes a new draft. Fixed 8fb4132. |
| 22208 | 7 | CR | Minor | nit | fixed-before-merge | 1 | 1 | resource leak | no | Test helper leaks a screen on failure. Fixed 08a14c5. |
| 22208 | 8 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Fixture harness files break typecheck. Fixed 08a14c5. |
| 22208 | 9 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Test assertion should use `vi.waitFor`. Fixed 1e57ef1. |
| 22193 | 1 | CR | Minor | nit | ignored | 1 | 1 | error handling | no | Evidence `diff.sh` treats compare errors as differences (unverified). |
| 22193 | 2 | CR | Minor | nit | ignored | 1 | 1 | error handling | no | Evidence `run-all.sh` redirects into a missing dir (unverified). |
| 22193 | 3 | CR | Minor | nit | ignored | 1 | 2 | error handling | no | Evidence `server.mjs` empty PID could kill the caller's process group (unverified). |
| 22155 | 1 | MS | High | real-minor | fixed-before-merge | 2 | 4 | state machine | maybe | Continued imported session omitted from forks because run-less messages lack `historyOrigin`. Author: importer writes `v1_import` in the same transaction (not a code change). Resolved (unverified). |
| 22155 | 2 | CR | Major | nit | fixed-before-merge | 1 | 2 | other | no | Move import workflow to a domain service. Author first deferred, then did it in fa34498cb2. Architecture, not a defect. |
| 22155 | 3 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | state machine | yes | If the history read fails the thread is created and never retried; the user cannot recover history without deleting the thread. Fixed da62b612f3, b14157fd17 (`nativeHistoryPending`). |
| 22155 | 4 | CR | Major | real-minor | fixed-before-merge | 2 | 3 | resource leak | no | `session/resume` unbounded while holding the session-mutation lock. Fixed 62458d6 (2 min timeout). |
| 22155 | 5 | CR | Major | wrong | withdrawn | 1 | 4 | data integrity | no | Move the `canReadThreadSnapshot` check first; author showed resume-only agents populate the snapshot; CR withdrew. |
| 22148 | 1 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | cross-file contract | no | Windows paths in file-mention chip labels. Fixed 1366714. |
| 21968 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Browser test uses fixed delays (test flake). |
| 21968 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Test should call `setup()` first. |
| 21968 | 3 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Final geometry assert outside `vi.waitFor`. |
| 21968 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Grouped reveal not retried when the outer list grows, so output stays behind the composer. Fixed 50fdcc53f1. |
| 21676 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Cancel of a follow-up run was not recorded, so it stayed `completed`. Fixed 016597c. |
| 21676 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Child stop waits for child lock while holding the parent lock (up to 15 s). Resolved, not outdated (unverified fix). |
| 21676 | 3 | CR | Minor | real-bug | fixed-before-merge | 2 | 4 | data integrity | no | `cancelledTask` marker lost when the Stop plan is empty. Fixed 3188d3d. |

Counts check: 72 rows. Several "verdict" labels for the evidence-script threads are real-minor/nit with sev 1 because the code is a manual proof script, not product code.

## 3. Track B (escaped bugs)

Fix PRs treated as trivial or non-bug: #22960 (feature-like find bar, mostly additions, no SZZ) and #22226 (pure addition). One line each below.

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 22997 | Completing a list marker inside existing composer text left a paragraph while saving list Markdown | no SZZ target (pure addition) | n/a | n/a | 2 | 3 | Follow-up to the list input rules; drift between editor and Markdown. |
| 22996 | Quitting desktop could finish while the backend still held the single-writer lock (outer wait and SIGKILL deadline equal) | #2679 "Reduce idle work and disk churn with native resource diagnostics" (+18478/-2154, 122 files, 2026-07-29), 8 of 8 lines in DesktopBackendManager | medium | missed (Macroscope 140+ comments on resource telemetry; none on quit waiting) | 3 | 4 | Giant PR dilution; needs process-teardown timing knowledge. |
| 22993 | iOS widget treated an already-passed session reset as the whole provider's expiry, clearing every quota row | #11506 "feat(mobile): add pooled subscription usage widgets" (+1085/-300, 2026-09-13), 2 lines | high | missed (Macroscope/CR commented on period selection, "more" count and URL, not expiry) | 2 | 3 | Needs real provider timestamps (author says not collected). |
| 22964 | Passive Claude Stop-hook summaries showed an orange warning after every turn | #21231 "fix(server): a Claude hook that drops a prompt now shows its reason" (+83/-2, 2026-10-18), 1 line | medium | bots did not comment (0 bot comments) | 1 | 3 | UX noise, not a defect in logic. |
| 22948 | Preview `evaluate` returned some results by reference instead of by value | #3053 "[codex] Add integrated browser preview, annotations, and agent automation" (+21242/-1214, 2026-06-14), 4 lines; other lines #15328, #24850 | low | missed (not examined in detail; PR is 203 files, unverified) | 2 | 4 | Initial megapatch, treat as noise-level evidence. |
| 22947 | Queued agent continuation reset the working timer (21 s shown after a 2 min 7 s run) | #15029 "fix(server): working timers no longer reset on every background wake" (+245/-11, 2026-10-03), 11 of 12 lines | high | bots did not comment (0 bot comments) | 2 | 4 | Fix-of-a-fix: the earlier timer fix did not cover queue drains. |
| 22874 | Question-answer Submit enabled but did nothing when normal sends were blocked (no provider, loading, in flight, reconnecting) | #4117 "fix(web): default provider selection for users without Codex" (+458/-97, 2026-07-22), 12 of 22 ChatComposer lines | low | missed (Macroscope on #4117 flagged persisted instance replacement, a different defect) | 3 | 4 | Guard sharing between sends and answers is spread across files (also #26901 side chats, 7 lines). |
| 22861 | Worktree cut from non-default base `dev` showed the newest merged `dev -> main` PR | #9125 "fix(server): find newly opened pull requests after agent turns" (+788/-60, 2026-09-04), 7 of 8 lines | high | missed (Macroscope: fork head search, stale poll, CheckpointReactor wiring; none on upstream-as-base) | 2 | 4 | Semantic: upstream equals a base branch. Adjacent defect (fork head) was flagged. |
| 22839 | After an OpenCode CLI update with a loopback server, verification compared with the old server's version and reported "unchanged" | #24763 "fix(server): skip provider CLI update when already on latest" (+291/-20, 2026-10-30) | low (1 line; the rest is #2829 noise) | missed (CR commented on this PR: advisory enrichment and cached fallback, not loopback servers) | 2 | 4 | Needs the loopback server model. |
| 22836 | Forking a Claude thread after changing the project root failed the first turn (transcript searched under the new cwd) | no SZZ target (#2829 only, noise) | n/a | n/a | 2 | 3 | The `forkSession` cwd restriction is old; origin not recoverable. |
| 22755 | Switching a thread to another provider instance during a running turn closed the live session and failed the turn | #27197 "feat: managed policy for organization-wide T3 Code configuration" (+9048/-543, 2026-11-01), 1 line; other 1 line #2829 | low | missed (CR/Macroscope 40 comments on the policy PR; none on instance switching) | 3 | 4 | Weak target; probably original orchestrator design. |
| 22553 | Thread search missed phrases inside quotes and their comments | #24343 "feat(search): Cmd+K finds the right thread first, with indexed message search" (+5797/-718, 2026-10-24), 8 lines; #27383 8 lines | low | missed (Macroscope flagged accents, 2000-hit cap, perf; CR on #27383 flagged 10k hit cap; none on quote text) | 2 | 4 | Missing text source in the search index. |
| 22425 | Held queue released when a later turn on another provider succeeded, so queued messages for the limited provider ran and failed | #22790 "fix(queue): send selected held messages when a thread is stopped" (+341/-44, 2026-10-21), 8 of 12 lines | high | bots did not comment (0 bot comments) | 3 | 4 | Fix-of-a-fix in queue hold logic; needs multi-provider state view. |
| 22349 | Full-screen HTML replies stretched over 92vw and zoomed without reflow | #17561 "feat(web): view visual replies full screen with zoom" (+306/-18, 2026-10-14), 12 of 13 lines | high | missed (CR flagged concurrent refresh only) | 1 | 2 | Design iteration, cosmetic. |
| 22347 | Diff selection was lost on navigation | #19941 "feat(web): review local commits in the Diff pane" (+1375/-162, 2026-10-30), 28 of ~60 lines; also #23064, #20297 | medium | missed (Macroscope flagged a pending commit-link preview overwriting a newer picker selection, adjacent but not the navigation case; unverified) | 2 | 3 | Adjacent finding at intro. |
| 22239 | Claude insight blocks were shown as raw box-drawing text | #10439 "feat(web): find messages and plans in the current thread" (+8005/-1467, 139 files, 2026-10-08), 11 lines | low | missed | 1 | 2 | Feature gap, not a regression; only thread-find indexing lines blamed. |
| 22226 | Open in Finder added the chosen folder as a project and never started the clone | no SZZ target (pure addition) | n/a | n/a | 2 | 3 | Missing wire-up. |
| 22208 | Switching a retention rule on saved 8 days at once and could start a cleanup sweep before the user picked the age | #11598 "feat(settings): add automatic storage cleanup per machine and project" (+1911/-7, 36 files, 2026-09-17), 19 of 24 lines | high | missed (Macroscope: 3 High on cleanup races and terminals; none on saving the default age) | 3 | 3 | Destructive default (deletes artifacts). Seen from the diff: toggle handler writes `8`. |
| 22193 | Changing effort in Settings could replace the saved default model with the substitute shown | #28005 "fix(web): show mixed automatic defaults across environments" (+219/-15, 2026-11-01), 7 of 16 lines | medium | missed (Macroscope High on null preferences inheriting; adjacent, not substitution) | 3 | 4 | Silent overwrite of a setting. Earlier PRs #13479, #9754 also blamed. |
| 22155 | Imported ACP sessions opened an empty thread | #13612 "feat: start threads without a project" (+1081/-100, 2026-09-30), 20 lines (after #2829 noise, 181) | low | missed | 2 | 3 | Actually an unimplemented feature, not a regression. |
| 22148 | Single-line unfocused composer on narrow windows showed serialized citation links instead of chips | #20391 "fix(web): pending questions no longer squash the composer on narrow windows" (+22/-94, 2026-10-18), 2 lines | medium | bots did not comment (0 bot comments) | 1 | 3 | Cosmetic. |
| 21968 | Expanding a work row near the composer left output hidden under it | #22675 (refactor, noise); next: #26255 "feat(web): pending approvals show on their timeline row" (+546/-185, 2026-10-28), 2 lines | low | not checked (unverified) | 2 | 4 | Scroll geometry; needs browser test. |
| 21897 | Grok and Cursor usage limits lost pace and the even-spend line | #17061 "fix(server): show zero-use Grok billing periods" (+136/-8, 2026-10-20), 6 lines | medium | missed (CR flagged calendar validation before zero inference, not pace data) | 1 | 3 | Cosmetic. |
| 21676 | `task_cancel` stopped a delegated child's background work but `task_status` still said `completed` and the parent kept running | #16002 "fix(server): Stop also stops delegated tasks and pull request watches" (+1271/-183, 2026-10-05), 13 of ~25 lines | medium | missed (Macroscope 4 High on #16002 about the stop barrier and successful thread.stop leaving children running; adjacent, none on cancelling completed background-only tasks) | 3 | 5 | Orchestrator lifecycle semantics. |
| 22960 | Cmd+F did nothing in the integrated browser | n/a | n/a | n/a | 1 | 1 | Feature add; not a bug escape. |

Bot coverage on 22 SZZ-traced bugs: caught 0, missed 17, no bot comment at the introducing PR 4 (#22964, #22947, #22425, #22148), not checked 1 (#21968). Not traced (pure addition, noise or feature): #22997, #22836, #22226, #22960.

## 4. Catalogue candidates (real bugs, severity >= 3)

| id | PR(s) | golden description | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| busy-provider-selection-recorded-as-rejected-receipt | #22755 | The new busy error is not in `dispatchWithReceiptEffect`'s early-return list, so it is committed as a permanent rejected receipt and a retry with the same commandId fails as "previously rejected". | a0efdaeb89a75050612a82436432de4ebf526206 | dd9772c252c558b852e7a7ffbc232bd87f6e82d0 | CodeRabbit (ignored, merged) |
| retention-age-parsed-from-localized-text | #22208 | Enter on a localized display value such as `1.000` is parsed with `Number(raw)` and saves 1 day instead of 1000, which lets the retention sweep delete artifacts far earlier than requested. | a03d9bce026ef11930b35e9855adc1cdb5ea6eb7 | 095182815fae93e1661068267d69f17d19b10a01 (the commit Macroscope reviewed; the PR's last commit is 85f953017c) | Macroscope (fixed before merge) |
| retention-draft-saved-to-wrong-scope | #22208 | The retention draft survives a settings-scope change, so committing it saves the previous scope's age into the new scope. | a03d9bce026ef11930b35e9855adc1cdb5ea6eb7 | 85f953017c3207022f193a9978e3b651dda65308 (comment commit unverified; earlier head needed) | CodeRabbit (fixed before merge) |
| held-queue-released-after-other-provider-turn | #22425 (introduced by #22790) | Held queued messages for a usage-limited provider are released when a later run on a different provider succeeds (and when `resetAt` is null), so they run against the still-limited provider, fail, and flip the thread back. | 1dfb57287174230e5c386e452f54bb0cce2fc32f | 7b48ba2f733957c0635536e1cec496fb714ec9e1 (head of #22790) | none at intro (CodeRabbit caught the null-reset variant in the fix PR) |
| acp-import-history-never-retried | #22155 | When the native history read fails after the thread is created, a later import returns early because the thread exists and never retries, so the user cannot recover history without deleting the thread. | fix PR base (not fetched) | fix PR head at the comment (not fetched) | CodeRabbit (fixed before merge) |
| opencode-wrong-updater-for-newer-cli | #22839 | When a 1.x server is still running after its CLI moved to 2.x, maintenance resolves the updater from the server's generation and picks `opencode-ai` instead of `@opencode/cli`. | fix PR base (not fetched) | fix PR head at the comment (not fetched) | CodeRabbit (fixed before merge) |
| cancel-background-only-task-reports-completed | #21676 (introduced by #16002, low-medium) | Cancelling a delegated task whose turn already completed stops its background work but leaves `task_status` as `completed` and the parent task running. | 51f7f77f87318a5329d3bab15d513fda5654200b (base of #16002) | 55aa540a1d91147670635b2d541d06169e7a408c (head of #16002) | none |

Shas for #22155 and #22839 not fetched (marked); fill with `gh pr view <N> --json baseRefOid,commits` before replay.

Borderline not promoted: #22874 (question Submit did nothing, sev 3, intro #4117 low confidence; no bot caught the Submit no-op itself), #22996 (quit leaves lock held, sev 3, intro in a 122-file PR, too diluted for a fair replay).

## 5. Observations

- CodeRabbit dominates thread count (56 of 72), and on author-owned PRs from AI-assisted loops (#22839, #22155, #22208, #22960) nearly every thread gets a reply and a fix commit. On #22960 four of seven threads were rebutted with a technical reason and CodeRabbit withdrew them, which is a healthy sign but means the first comment was wrong 4 times.
- CodeRabbit severity labels are noisy: "Major" was a CI knip failure (#22993), a manual evidence-script hang (#22996 T3), a test request (#22226 T4 minor), and an architecture refactor on code that predated the PR (#22155 T2).
- Macroscope's High findings were more often real: #22208 T1 (locale parsing, would have deleted data), #22947 T3, #22997 T6. On #22208 the High was fixed before merge. Its reply bot returns "no permissions" when asked to act (#22839 T1).
- Evidence and fixture scripts committed with the PR draw about 25 of 72 threads (#22997, #22996, #22993, #22193, #22836). Almost all are real but sev 1 because the script is a manual proof, not product code.
- At introduction the bots missed every traceable escape (0 of 17 where they commented on the PR); 4 introducing PRs had no bot comment at all. Several escapes are fix-of-a-fix (#15029 to #22947, #22790 to #22425, #28005 to #22193), meaning the same module was reviewed twice by bots without catching the interaction.
