# Chunk 03: PRs #33142..#31739 (2026-11-09)

## 1. Header

- PRs covered: 25 (#33142 .. #31739). 10 have no bot thread at all (#33142, #33141, #33139, #33133, #32995, #32288, #32287, #32180, #31998, #31754).
- Bot threads: 66 total. CodeRabbit 41, Macroscope 25. #33093 (Cursor Origin provider, 19 threads) and #31760 (docs, 10) hold 29 of them.
- Verdicts: real-bug 13, real-minor 40, nit 7, wrong 4, unclear 2.
- Outcomes: fixed-before-merge 51 (#33093 x14, #31760 x7, #32941 x5, #33126 x4, #32927 x4, #32190 x4, #33113 x3, #33092 x3, others 1-2), disputed 13 (author declined, usually with evidence, and the bot withdrew or accepted), ignored 1 (#33092 T5), unknown 1 (#31760 T8).
- Code checked (via `gh api contents?ref=<sha>` for the comment commit, and `git show` at the merge commit): #33126 T3/T4, #33092 T1/T3, #33093 T6/T11/T13/T17, #32927 T2, #31956 T1, #33134 T1. All other verdicts come from thread text, replies and resolved/outdated flags (unverified in code).
- Track B: 11 `fix` PRs. 2 trivial (#33113 copy, #33135 dependency bump with perf motive, no SZZ). 2 pure additions (#32812 patch file, #31754 +15/-0). SZZ run on 7 (#33134, #33133, #33126, #32995, #32929, #31956, #31739); 2 of them are layout noise (#33133, #32995).
- Bots at the introducing PR (Track B, 5 meaningful traces): caught 0, missed 4 (#33126, #32929, #31956, #33134), missed/uncertain 1 (#31739, no clean introducing PR). #32995 introducing PR had no bot comments at all.
- Stack check: every PR here has a main-line base (each base sha is the previous merge); no SZZ target is an unmerged stack commit.
- Caveat: pre-merge commit shas are not in the blobless clone. They were read through the GitHub contents API, which works because the commits are still reachable.

## 2. Track A (bot threads)

Outcome evidence: "reply" = author reply says fixed; "outdated" = thread outdated flag; "none" = no reply. (unverified) = judged from thread text only.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | one-line finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 33135 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Test should assert converted physical bounds reach focus worker. Reply: d210e11 (unverified). |
| 33134 | 1 | MS | Medium | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | `commentCount` keeps counting hidden replies past page 1, so the PR watcher never sees "all comments loaded", holds its watermark and stops waking on new comments. Code at 2b0f49bd9f has no `hiddenCount`; reply: fixed in 958b27a. The author says the watcher effect was worse than the label bug. |
| 33134 | 2 | CR | Major | real-minor | disputed | 2 | 4 | cross-file contract | no | Thread whose first 10 comments are all minimized is dropped although later replies are visible. Declined: needs >10-comment thread with 10 hidden first, web/mobile skip rootless threads anyway; listed as deferred in PR body. CR accepted. |
| 33131 | 1 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Docs omit the one-open-project exception. Reply: 0c7f219. |
| 33126 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Tap below a trailing chip clamps to `token.end` and opens it; add y bounds. Reply: faca193. |
| 33126 | 2 | CR | Major | nit | fixed-before-merge | 1 | 1 | other | no | `chipContains` has 3 returns, lint ReturnCount fails. Style rule, not a defect; fixed 271e95de7a. |
| 33126 | 3 | MS | High | real-bug | fixed-before-merge | 3 | 4 | error handling | yes | New `chipContains` calls `getPrimaryHorizontal(token.end)` with stale token bounds before the length check; a tap after deleting a trailing chip can throw IndexOutOfBounds. Verified: at c81e5f78ba the length guard comes after `chipContains`; merged code checks `it.end <= editor.length()` first. Crash on Android 16 is the bot's claim (not run). |
| 33126 | 4 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | error handling | yes | Same defect as T3 (duplicate), separate bot. Bot also asked for `start >= 0`; author declined, CR agreed. |
| 33113 | 1 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | Removing "change" from search terms breaks "change description" search. Reply: c389f8d, no test added. |
| 33113 | 2 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | Placeholder example (paragraphs, no headings) contradicts the default prompt's required headings. Fixed c389f8d. |
| 33113 | 3 | CR | Minor | real-minor | fixed-before-merge | 1 | 1 | other | no | Docs claim instructions apply "in every project" although per-project override exists. Fixed c389f8d. |
| 33093 | 1 | MS | Medium | wrong | disputed | 1 | 3 | cross-file contract | no | `heads/refs/heads/main` ref path. Author checked live API: `base.ref` is bare `main`. Claim refuted by evidence in reply (unverified by me). |
| 33093 | 2 | MS | High | real-bug | fixed-before-merge | 3 | 3 | state machine | yes | List always returns first page and `continues=false`, so repos with >100 PRs cannot reach older ones. Outdated; reply: token kept in memory map, "Load more" grew 100 to 198 rows. |
| 33093 | 3 | MS | High | real-minor | fixed-before-merge | 2 | 5 | race/ordering | no | Push between `getPull` and `/files` caches a newer patch under the older `base...head` key for an hour. Fixed by re-reading the PR before caching. Narrow window (unverified). |
| 33093 | 4 | MS | Medium | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Dismissed reviews filtered out of activity. Fixed (kept as DISMISSED). |
| 33093 | 5 | MS | Medium | unclear | disputed | 1 | 3 | cross-file contract | no | `involvement=reviewing` returns the unfiltered list. Author: Origin has no reviewer filter, web builds Reviewing from `viewerReviewRequested`, so rows never reach it. Plausible (unverified). |
| 33093 | 6 | MS | High | real-bug | fixed-before-merge | 4 | 3 | data integrity | yes | Ordinary merge of a stacked child merges its unmerged ancestors with no warning (irreversible). Verified: `case "merge"` at line 819 in 00a0cdb41f has no stack check; merged file lines 574-579 reject with "stacked on #N" when parent is open. |
| 33093 | 7 | MS | Medium | wrong | disputed | 1 | 3 | cross-file contract | no | Thread `endLine: 0` leaves line null. Author: live API always sets start=end for line threads; 0/0 only on PR-level comments with empty path, already skipped (unverified). |
| 33093 | 8 | MS | High | real-bug | fixed-before-merge | 3 | 3 | cross-file contract | yes | `getChangeRequest` with a URL of another repo returns the checkout repo's PR of the same number (wrong PR shown). Fixed 707e7abeaf. |
| 33093 | 9 | MS | High | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | `isOutdated` always false, so comments on an old version attach to unrelated code. Fixed (compare `version.headSha`). |
| 33093 | 10 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Rename patches lack `similarity index`, so the code tab loses the old filename. Fixed. |
| 33093 | 11 | MS | High | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | All-cancelled checks reported as passing (green for an aborted run). Fixed. Bot rated High; effect is a misleading badge, sev 2. |
| 33093 | 12 | CR | Minor | real-bug | fixed-before-merge | 3 | 3 | cross-file contract | no | Same root as T8 (URL repository dropped); also checkout would pass `7 -R acme/web`. Fixed. CR also asked for tests; author declined (repo adds tests only on request). |
| 33093 | 13 | CR | Major | real-bug | fixed-before-merge | 4 | 3 | error handling | yes | Publish creates repo (team-visible), then PATCHes private; if PATCH fails the repo stays visible, retry fails with "already exists", user sees a generic error. Verified: merged code retries and says "Created X, but could not make it private, so your Cursor team can still see it". Contradicts the documented "published privately". |
| 33093 | 14 | MS | Medium | real-minor | fixed-before-merge | 1 | 2 | cross-file contract | no | Copied files emitted with `rename` headers. Fixed 6cd2daaaf4; bot could not see the commit, author showed the ancestry. |
| 33093 | 15 | MS | High | real-minor | disputed | 2 | 5 | race/ordering | no | Mergeability verdict for newer commits cached under the older key. Head sha fixed (`expectedHeadSha`); base race left because base tip comes from a 2 s cache and a wrong entry is unreadable once the base moves. Bot accepted. |
| 33093 | 16 | MS | High | unclear | disputed | 1 | 2 | error handling | no | `webUrl` required in schema; one missing field rejects a whole list page. Author paged 433 PRs live, none lacked it; failing loudly judged acceptable. |
| 33093 | 17 | MS | High | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | >1000 check runs dropped `truncated`, so an all-green partial read shows "passing". Verified: merged line 323 returns `truncated: page.truncated`. |
| 33093 | 18 | MS | High | real-bug | fixed-before-merge | 3 | 2 | cross-file contract | yes | `123/fix` and `feature/pull/42` parsed as PR numbers 123 and 42, so checkout opens an unrelated PR instead of the branch. Fixed 09a453ed0b (`^#?\d+$`). |
| 33093 | 19 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Evicted or expired list cursor reported a successful final page, hiding "Load more". Fixed f69b5f973f. |
| 33092 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 4 | race/ordering | yes | With pending approvals, a failed attachment upload still declines the approvals before the send is rejected: no message goes out but the agent's approval decision changed. Verified at 08b4d3e61a: `declinePendingApprovals` (line 1119) runs before `prepareTurnAttachments` (line 1175); merged code waits for uploads first. |
| 33092 | 2 | CR | Major | real-minor | disputed | 2 | 3 | data integrity | no | Reload after composer clears but before upload finishes loses the send. Declined: same window already exists for worktree prep; durable outbox is a separate change. CR accepted. |
| 33092 | 3 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | race/ordering | no | Same as T1 (decline before upload success). Second item in this thread, multi-model send clears the draft after the upload wait and can erase newer edits, was still open per CR's last reply (unverified). |
| 33092 | 4 | CR | Major | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Server file-limit change during upload can pass the guard, then decline approvals and reject the turn. Fixed (recheck capability after wait). |
| 33092 | 5 | MS | High | real-minor | ignored | 2 | 4 | UI state | no | Failed upload while user types a new draft leaves the optimistic row stuck with no retry. Author: unchanged from main for other failures, follow-up. |
| 32941 | 1 | MS | Low | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Mobile footer omits run-the-command guidance when permission is missing. Fixed 089e5939a1. |
| 32941 | 2 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | `SQLITE_TMPDIR` pointing at a non-writable dir makes the free-space check measure the wrong filesystem. Fixed in two rounds (writable, then also searchable `W_OK|X_OK`). |
| 32941 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Duplicate of T1 (footer ignores permission fallback). Fixed. |
| 32941 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | `requestReclaim` clears the failure but does not publish status, so a retry shows the old failure and an enabled button while the server restarts. Fixed a01375427a. |
| 32941 | 5 | MS | Medium | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Duplicate of T4 on the mobile row. Fixed on the server. |
| 32941 | 6 | CR | Minor | wrong | disputed | 1 | 2 | other | no | Docs should mention `environment:maintain`. Standard clients include it; CR withdrew. |
| 32929 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 4 | UI state | no | With a maximized side chat, F6 could re-select the side-chat editor and never advance. Fixed 7253794 (nested targets only for panel-opening). |
| 32927 | 1 | MS | Medium | real-minor | fixed-before-merge | 1 | 3 | UI state | no | Settings search hides "Fast checkout" when any connected server is unsupported (`.every`). Fixed 70a299e (to `some`). |
| 32927 | 2 | CR | Major | real-bug | fixed-before-merge | 3 | 5 | data integrity | yes | On coarse-timestamp filesystems a file added right after a cache build leaves the directory mtime unchanged, so the cache is accepted and the cloned worktree can miss that file. Verified: no backdating at 0a0629b47b; merged code backdates every cached dir to 1_000_000 before recording. |
| 32927 | 3 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | UI state | no | Search gate used environments without config. Fixed 70a299e. |
| 32927 | 4 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Grammar in docs. Fixed. |
| 32927 | 5 | CR | Minor | real-minor | disputed | 1 | 3 | UI state | no | `some` gate can lead to a scope with no Fast checkout row. Declined; CR withdrew. |
| 32927 | 6 | CR | Minor | nit | disputed | 1 | 2 | UI state | no | Asks for an eligible-machine notice. Declined; CR withdrew. |
| 32812 | 1 | CR | Minor | nit | disputed | 1 | 2 | other | no | `orient="90deg"` falls back to 0 degrees. Same as pre-fix behavior minus the crash; out of scope, CR withdrew. |
| 32190 | 1 | MS | High | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | `var(--x)` inside a Mermaid label is rewritten as CSS, losing the label text. Fixed c9c5f0a4834 with test. Bot rated High; sev 2. |
| 32190 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Duplicate of T1. |
| 32190 | 3 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | other | no | Renderer deps change per streaming update and reset the library cache. Part this PR introduced fixed; older identity churn left. |
| 32190 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | iOS `toDataURL` empty callback throws and leaves the diagram stuck in `exporting`. Fixed. |
| 31956 | 1 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | New client schema requires `benchmarkTier` and a new benchmark shape; an older server omits them, so the client rejects its status and can block voice capture and the settings panel. Verified: required at 422bdb931a (line 116); merged code decodes legacy shapes (`optionalKey`, legacy comment at line 135). |
| 31760 | 1 | CR | Major | real-minor | fixed-before-merge | 2 | 2 | security | no | Docs: agents run with the server env and can read the 1Password token. Warning added 6e2caf752e7. |
| 31760 | 2 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | Check command ignores the service's env. Fixed; CR still wanted a no-shell-history input method. |
| 31760 | 3 | CR | Major | real-minor | fixed-before-merge | 2 | 2 | security | no | Check prints the secret into retained terminal output. Fixed (stdout discarded). |
| 31760 | 4 | CR | Major | real-minor | fixed-before-merge | 2 | 2 | security | no | Connect over plain HTTP exposes the token. Fixed c906e51. |
| 31760 | 5 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | `op item get` needs `--format json`. Command dropped. |
| 31760 | 6 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | Shell check is not a server check. Fixed. |
| 31760 | 7 | CR | Major | real-minor | disputed | 1 | 3 | other | no | Refresh only rereads enabled provider instances. Refresh promise dropped; follow-up restart advice declined, CR agreed. |
| 31760 | 8 | CR | Major | real-minor | unknown | 1 | 3 | other | no | Running provider keeps old secret after failed reread, so "feature works" proves nothing. Author dropped Refresh; CR said guidance still needed change; resolved without visible final reply (unverified). |
| 31760 | 9 | CR | Minor | real-minor | fixed-before-merge | 1 | 3 | other | no | Refresh does not read EAS tokens. Addressed e942296. |
| 31760 | 10 | CR | Minor | wrong | disputed | 1 | 3 | other | no | Wants an uncached reference for the check. Author: check is for new references; CR withdrew. |
| 31739 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Failed web model-pick save only logs, picker shows the draft as applied. Fixed 5e8ca8ff. |
| 31739 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | Same on mobile. Fixed 66bab50 with rejection test. |

## 3. Track B (escaped bugs)

| fix PR | bug | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 33135 fix(desktop) xa11y bump | Windows App Shots lose window text on big pages (3 s limit) | n/a | n/a | n/a | 2 | n/a | Dependency bump for speed; trivial, no SZZ. |
| 33134 fix(github) hidden comments | Minimized comments and reviews still shown; hidden CHANGES_REQUESTED review set "changes requested" on PRs | #4849 (multi-provider PR page, +34121, 2026-08-10); #19224 reformatted the same code | low | missed (65 bot comments on #4849, none on `isMinimized`/hidden; unverified for #19224) | 3 | 4 | Omission in the original feature, not a wrong line. SZZ blamed 8 lines in #4849, 6 in #19224 (a +85k refactor, treat as noise). Needs GitHub-domain knowledge. |
| 33133 fix(web) mic button | Mic button not next to send (layout) | n/a | n/a | n/a | 1 | n/a | Layout; SZZ returned a dozen unrelated blames (#1574, #13209, #26238...). Trivial, no target. |
| 33126 fix(mobile) chip taps | Tapping the right half of an Android composer chip moved the cursor instead of opening it (offset at chip end excluded by `offset < it.end`) | #11265 (inline file previews and attachment chips, +21441, 2026-09-12) | high | missed (21 bot comments, none on the Android hit test) | 2 | 3 | Both SZZ lines are the original hit test. Needs Android `getOffsetForPosition` behavior. |
| 33113 fix(web) settings copy | Settings copy about PR descriptions | n/a | n/a | n/a | 1 | n/a | Copy; trivial. |
| 32995 fix(mobile) compose button | Compose button covers last tab on iPhone (+5/-1 Swift layout) | #28955 (another fix: iOS compose button no longer grows while pressed, 2026-11-06) | medium | bots-did-not-run (0 bot comments on #28955) | 1 | 3 | Regression from a one-line fix three days earlier; layout only. |
| 32929 fix(web) side chat focus | New side chat focused its Bring back button instead of the message input | #25877 (F6 workspace areas, +1870, 2026-10-28) | medium | missed (26 bot comments, 3 on workspaceFocus.ts, none about nested areas / panel-open focus) | 2 | 4 | `belongs()` required the element's own area, so the nested input area was skipped when opening the panel. Needs DOM focus knowledge. |
| 32812 fix(mobile) SVG markers | Android app crashes (and on every reopen of the thread) on `orient="auto-start-reverse"` in react-native-svg | n/a | n/a | n/a | 4 | n/a | Library bug fixed by patch file (pure addition). Origin is when inline SVG rendering was added (unverified). Severity 4 (repeat crash). |
| 31956 fix(speech) benchmarks | Voice settings always showed the GPU speed reference even when the environment ran on CPU (catalog generator dropped the CPU result) | #30625 (transcribe audio on a chosen environment, +8714, 2026-11-05) | medium | missed (14 bot comments, all on other speech issues: dictionary, locks, streams) | 2 | 3 | Wrong figure shown, no crash. Feature shipped four days earlier. #30623 is a secondary blame. |
| 31754 fix(web) secret provider removal | Removing a secret provider did not list the Simlock tokens reading from it | n/a | n/a | n/a | 2 | n/a | +15/-0 in `SecretsSettings.logic.ts`: pure addition, no SZZ target. |
| 31739 fix(composer) model picks | A model picked in the composer lived only in the local draft, so answering a question card or `t3_thread_send` started the next turn on the previous model while the UI showed the new one | none clean; closest #1371 (persist provider-aware model selections, composerDraftStore) | low | missed (20 bot comments on #1371, none on this) | 3 | 5 | Design gap across draft store, thread commands and mobile, not one bad line. SZZ spread over 12 PRs (#1371, #23069, #1121 ...). Silent wrong-model turn is why sev 3. |

## 4. Catalogue candidates (real bugs, severity >= 3)

Track B (escaped): none qualifies for replay. #33134 and #31739 are sev 3 but the introducing PR is a 34k-line feature or a design gap, which is a poor replay target.

Track A (fixed before merge; head is the commit the bot commented on, base is the PR base):

| id | PR | golden (a reviewer must state) | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| origin-stacked-merge-merges-ancestors | 33093 T6 | Merging a stacked child PR through the plain merge action also merges its unmerged parent PRs, with no stack check or confirmation. | c4ce7b0fd74f6beb37ed6034f5c8416e5aa7e165 | 00a0cdb41fd37d1450f1fe33df882b743fd4ea65 | Macroscope |
| origin-publish-leaves-repo-team-visible | 33093 T13 | Publishing creates the repo team-visible and then PATCHes it private; if the PATCH fails the repo stays visible and the retry fails with "already exists", with no specific error. | c4ce7b0fd74f6beb37ed6034f5c8416e5aa7e165 | 00a0cdb41fd37d1450f1fe33df882b743fd4ea65 | CodeRabbit |
| origin-pr-url-ignores-repository | 33093 T8/T12 | A PR URL for another repository is resolved against the checkout's repository, returning or checking out the wrong PR of the same number. | c4ce7b0fd74f6beb37ed6034f5c8416e5aa7e165 | 00a0cdb41fd37d1450f1fe33df882b743fd4ea65 | Macroscope, CodeRabbit |
| origin-branch-ref-parsed-as-pr-number | 33093 T18 | `123/fix` or `feature/pull/42` is parsed as PR number 123 or 42 because the regex allows a `/...` suffix, so an unrelated PR is opened. | c4ce7b0fd74f6beb37ed6034f5c8416e5aa7e165 | 5586b3f7cf60d0150aad0ed5cda96cdf947d5698 | Macroscope |
| origin-list-never-pages | 33093 T2 | `listChangeRequests` always returns the first page with `continues=false` and ignores the next-page token, so older PRs are unreachable. | c4ce7b0fd74f6beb37ed6034f5c8416e5aa7e165 | 00a0cdb41fd37d1450f1fe33df882b743fd4ea65 | Macroscope |
| composer-send-declines-approvals-before-upload-result | 33092 T1/T3 | Sending with pending approvals declines them before attachment uploads are known to have succeeded, so a failed upload changes the agent's approval without sending the message. | 7078dcbfbef09b5c970aba2b4771b2f1e8bcfbb9 | 08b4d3e61a4641612bc0b1aae6922eac3cc522e2 | Macroscope, CodeRabbit |
| android-chip-tap-stale-token-out-of-range | 33126 T3/T4 | `chipContains` measures `token.end` with stale token offsets before checking they are within the editor length, so a tap after a chip was deleted can throw. | d456cd77e56b73906cd155000a276d17f70a240e | c81e5f78ba7318d2e4a7dd5d0a91af34f94326f0 | Macroscope, CodeRabbit |
| worktree-cache-coarse-mtime-stale-accept | 32927 T2 | Cache validity relies on directory mtimes that are not backdated, so on coarse-timestamp filesystems a file added just after the build leaves the mtime unchanged and a stale cache is accepted. | d456cd77e56b73906cd155000a276d17f70a240e | 0a0629b47bb0e484efa4c03e555c3fd11836b264 | CodeRabbit |
| speech-status-requires-new-fields-from-old-servers | 31956 T1 | The client schema requires `benchmarkTier` and the new benchmark shape, which older servers do not send, so decoding fails and voice settings and capture break against an older server. | e455200077ce60806a01c8f28435b58860dcfc74 | 422bdb931a923db3021afceb4d18769ca2155e56 | CodeRabbit |
| github-hidden-reply-holds-comment-count | 33134 T1 | `commentCount` counts minimized replies beyond page 1 as loaded-and-displayable, so the watcher's "all comments loaded" check never passes and new-comment wakes stop. | d5290e9167ccbd8d2c7043eab8e311fd21a14464 | 2b0f49bd9fad71f039c9d6e1a30504f3580f2af3 | Macroscope |

Replay caveat: the base for #33093 and #33092 is the PR's base, not the first commit of the PR; the head for #33093 T2/T6/T8/T13 is the same commit 00a0cdb41f (state at first review). The head of each Track A row contains the bug per the bot's comment; verified in code only for T6 (no stack check at line 819), #33126 (guard after `chipContains`), #33092 (decline before prepare), #32927 T2, #31956 T1.

## 5. Observations

- Macroscope found the serious defects in the 2611-line Cursor Origin PR (stacked-merge, wrong PR from URL or branch name, never paging); CodeRabbit found the privacy failure path (T13) and a duplicate of the URL bug. Together they raised 19 threads and the author fixed or answered all of them: strong value on a new provider.
- Macroscope rated several threads High that were sev 2 (cancelled checks shown green, `var()` in a label) and CodeRabbit rated a lint ReturnCount failure Major. Bot severity labels over-rate presentation bugs and under-rate data-integrity ones (T13 was only CR "Major" and the stacked merge is irreversible).
- Both bots were wrong on the live behavior of an external API in #33093 (T1 and T7 refuted, T5 doubtful), refuted by the author running the real Origin API. Bots reasoning about a third-party API they cannot call are a false-positive source; a reviewer that can hit the API would avoid them.
- Macroscope several times replied "I couldn't verify commit X, it isn't in my checkout" (#33093 T14/T17/T18, #30625), so it cannot confirm a fix that arrived after the review and the author had to prove ancestry by hand. Author replies are Claude-written and cite exact commits and live runs.
- Escaped bugs in this chunk (#33126, #32929, #31956, #33134) were all missed by both bots at introduction: UI hit-testing and focus behavior, a dropped CPU benchmark, and a GitHub field omission. None is a wrong-looking line; each needs platform or product knowledge, which is where an added reviewer would have to show value.
