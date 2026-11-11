# Chunk 04: PRs #30678..#30397 (2026-11-06)

## 1. Header

- PRs covered: 25 (#30678 .. #30397). 12 have no bot thread at all. 10 of the 25 are GitLab provider PRs by one author (TonybynMp4), merged to main in sequence (each PR's base is the previous one's merge commit); none merge into an unmerged stack branch.
- Bot threads: 32 total. CodeRabbit 28, Macroscope 4 (#30579 x3, #30483 x1).
- Verdicts: real-bug 9, real-minor 12, nit 2, wrong 9, unclear 0.
- Outcomes: fixed-before-merge 21, disputed 11 (all 9 "wrong" plus #30480 T1 and #30453 T3), ignored 0, unknown 0. In every disputed thread but #30453 T3 the author rebutted with evidence and CodeRabbit withdrew the finding.
- Code checked at the merge commit: none. Verdicts come from thread text, author replies, resolved/outdated flags and the fix-commit descriptions (all unverified in code).
- Track B: 25 PRs, 16 `fix`-titled PRs touch non-trivial source. SZZ run on 15 (1 returned "no changed lines"). Bot coverage at intro: caught 0, missed 6 (#30603, #30601, #30569, #30562, #30479, #30563), partial-adjacent 1 (#30480), not checked 1 (#30652), no usable target 7.

## 2. Track A (bot threads)

CR = CodeRabbit, MS = Macroscope. "withdrawn" = bot agreed it was wrong after the author's reply.

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30579 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 3 | cross-file contract | yes | "Add to chat" does nothing for comments only present in `detail.reviewThreads` (lookup used `detail.comments`). Outdated+resolved, fixed in a3fe0230 (unverified in code). |
| 30579 | 2 | MS | High | real-bug | fixed-before-merge | 3 | 3 | data integrity | yes | `hasPullRequest` compares only PR number, so a `#42` from another repo suppresses this repo's PR reference and the agent gets the wrong PR identity. Fixed in a3fe0230 (compare URL). |
| 30579 | 3 | MS | High | real-minor | fixed-before-merge | 2 | 3 | other | no | `readableBody` drops the rest of a remark when an HTML comment is unclosed/inline (bot text truncated in the input). Fixed by switching to mdast parser. |
| 30579 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI state | no | Body fully removed by parsing should give `null` not an empty chip. Fixed in 6459365. |
| 30579 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | data integrity | no | Chip IDs lack the PR identity so a same-ID comment on another PR replaces the first chip. Fixed in 6459365 (duplicate class of T2). |
| 30579 | 6 | CR | Minor | real-bug | fixed-before-merge | 3 | 3 | data integrity | no | Same root as MS T2 (number-only reference check, wrong repo's PR). Duplicate; fixed in 6459365. |
| 30579 | 7 | CR | Major | wrong | disputed | 1 | 2 | other | no | Asked for `appendReference: false`; author showed composer drops chips whose inline reference is absent (ChatComposer.tsx:1684-1690). CR withdrew. |
| 30579 | 8 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Duplicate check also matched a handoff context chip, so a later handoff for another PR leaves a comment chip with no PR reference. Fixed in 134d377. |
| 30579 | 9 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | other | no | Fence parser ignores blockquote depth: `> ``` ` inside an outer fence treated as a close. Fixed in e3eb569 with tests. |
| 30569 | 1 | CR | Major | wrong | disputed | 1 | 4 | other | no | Claimed fff's indexed prefilter drops `regexFallbackError`. Author reproduced against pinned fff 0.11.0: error is returned. CR withdrew. |
| 30563 | 1 | CR | Major | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | Remote `"."` handled in one function but `prLookupCache` still treated the local upstream as published, bypassing `isUnpublishedBranch` and matching an unrelated same-name PR. Author: "Partly fixed in 6e79ab717f" with a failing-before regression test; CR accepted. |
| 30562 | 1 | CR | Major | wrong | disputed | 1 | 3 | security | no | Wanted `..` rejected on failed normalization. Author: same lexical `path.resolve` is used on the success path and by `project add`; CR withdrew. |
| 30549 | 1 | CR | Major | wrong | disputed | 1 | 3 | error handling | no | Top-level GraphQL errors: author checked `glab api graphql` exits 1 so decoder never sees them. CR withdrew. |
| 30549 | 2 | CR | Major | wrong | disputed | 1 | 3 | error handling | no | Unreadable `reviewState` reply fallback: same exit-1 mapping already reaches the existing catch. CR withdrew. |
| 30549 | 3 | CR | Major | wrong | disputed | 1 | 4 | other | no | Viewer-assignment check on GitLab Free: reviewer (juliusmarminge) read GitLab source; failure already surfaces as `Reviewer not found`. CR withdrew. |
| 30546 | 1 | CR | Minor | wrong | disputed | 1 | 3 | other | no | Asked for scalar count on deletion; author keeps grapheme count to match one Backspace = one DEL. CR withdrew. |
| 30524 | 1 | CR | Minor | real-minor | fixed-before-merge | 1 | 2 | other | no | `GL-123` and `[issue:123]` forms not linked. Fixed in f9ac046. |
| 30518 | 1 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | Optional fork "maintainer edits" GraphQL permission read failure blocks the whole merge request detail (and previews, checks). Fixed in e1b3e89 (fall back to false except CLI-unavailable/auth/rate-limit). |
| 30518 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | other | no | Permission read on non-edit views (preview/summary) costs an extra glab call. Fixed in 26aa85bafe. |
| 30483 | 1 | MS | High | real-bug | fixed-before-merge | 3 | 3 | data integrity | yes | `setLabels` looks up labels in one page of 100; an existing label beyond it is reported unknown and the write is skipped. Fixed in 04bc9b5ad6 (single-label endpoint). Macroscope's "fix it" reply returned "no permissions". |
| 30483 | 2 | CR | Minor | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | New label-permission GraphQL read is in the same `Effect.all` as the detail read, so a failure (e.g. errors-only reply) makes no merge request openable. Same class as #30518 T1. Fixed in 04bc9b5ad6. |
| 30483 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | UI state | no | Applied labels beyond the first page missing from picker so cannot be removed. Fixed in 31d9ad3f40. |
| 30483 | 4 | CR | Minor | wrong | disputed | 1 | 2 | other | no | `allowStale: true` atom not patched; author: no client reads that variant. CR withdrew. |
| 30483 | 5 | CR | Minor | wrong | disputed | 1 | 3 | other | no | Use `updateMergeRequest` permission instead of `adminMergeRequest`; author: it would over-report for authors whose label params GitLab drops. CR withdrew. |
| 30480 | 1 | CR | Minor | nit | disputed | 1 | 1 | other | no | Asks for a test of the declined-restart hint; author explains the harness cannot reach that branch. Withdrawn. |
| 30453 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | `locked` state treated as settled, allowing branch deletion during a merge. Fixed in 0f37a75. |
| 30453 | 2 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | error handling | yes | Same pattern a third time: branch-deletion permission query failure fails the whole detail read for closed/merged MRs. Fixed in 0f37a75. |
| 30453 | 3 | CR | Major | real-minor | disputed | 3 | 4 | race/ordering | no | Branch delete is not atomic on the SHA, so a push between check and delete can remove unmerged commits. Author: GitLab has no atomic expected-SHA delete (REST/GraphQL take none) and `--force-with-lease` needs credentials. Unfixed; real but platform-limited. |
| 30433 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | state machine | no | Resumed GraphQL cursor falling back to an offset REST read can re-emit rows. Fixed in 242bff6 (only first read falls back). |
| 30433 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 1 | security | no | Log `error.cause` (may embed payload) instead of bounded `error._tag`. Fixed in 242bff6. |
| 30423 | 1 | CR | Major | real-bug | fixed-before-merge | 3 | 3 | data integrity | yes | `diff_refs` with a null `base_sha` (orphaned source branch) fails whole-MR decode because the schema requires all three SHAs. Fixed in 08e61d971b. |
| 30423 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | no | Discussions and MR `diff_refs` read from different snapshots (cached detail, up to 60 s stale after a push) misclassify outdated. Fixed in 08e61d971b. |

## 3. Track B (escaped bugs)

Skipped as trivial or non-bug: #30678 (perf, tracing), #30596 (menu typography), #30564 (error text now carries decider reason; no SZZ run, sev 2). #30546 (iOS CJK input, missing capability in a Swift view, no SZZ). Titled `fix` but their bodies describe new capability, so no SZZ: #30483 (labels), #30453 (delete branch).

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 30652 | A Codex thread rewound several times imported only its last rollout; earlier history lost without the "not imported" notice | #5362 (first-run welcome wizard, +15520/-494, 2026-09-05) low; #10430/#23192 touched the same read path | low | not checked | 3 | 5 | Rewind chain support never existed; the blamed lines are the single-file read. Needs knowledge of Codex rollout format. |
| 30643 | OpenCode edit that deletes text (empty `newString`) lost its empty replacement because `recordString` treats blank as missing | no usable SZZ target (blames #2829 only; file moved there by the orchestrator import, origin earlier) | n/a | n/a | 2 | 3 | Diff view for the deletion loses its after-state. |
| 30603 | Terminal links broke at `@ + $ [ ] ( )` after the first slash (Next.js, SvelteKit, pnpm paths) | #20264 "fix(web): terminal links keep Unicode file paths intact" (+17/-2, 2026-10-20) | medium (1 line, the path pattern) | missed (Macroscope reviewed, no inline comment; CR comment not checked) | 2 | 2 | Regex too narrow, visible in one hunk if you know path shapes. |
| 30601 | CSV/TSV with generic labels `binary/octet-stream` or `application/unknown` got no table | #29360 "fix: honor generic MIME aliases in attachment previews" (+22/-4, 2026-11-03), named by the fix PR body | medium (SZZ blames original #11265, 1 line; #29360 is the PR that left this sibling behind) | missed (Macroscope and CR ran, no inline comment) | 1 | 3 | Sibling-helper inconsistency; author found no real source of such labels. |
| 30569 | Invalid regex with Match case off (`foo(`) returned no results because the `(?i)` prefix made the literal fallback keep the prefix | #4855 "Add project file picker and content search" (+2928/-476, 2026-07-30) | high (2 of 2 lines) | missed (Macroscope: 6 comments on WholeWord, debounce, selection; none on regex fallback) | 2 | 4 | Needs knowing fff's invalid-pattern behaviour. |
| 30563 | A branch tracking a local branch (`branch.x.remote = .`) showed that other branch's PR | #788 "Fix cross-repo PR detection and push remote selection" (+752/-84, 2026-03-10) | low (lines also touched by #8600, #6216, #17063; #1511 rename is noise) | missed (cursor[bot] review and CR ran; no inline comment on this) | 3 | 4 | Several call sites each needed the `"."` special case. |
| 30562 | `t3 project remove/rename` of a deleted project failed for relative or trailing-slash paths | #9885 "fix(cli): resolve projects with missing workspace directories" (+224/-4, 2026-09-05) | high (commit that added the raw-identifier fallback) | missed (Macroscope reviewed, no inline comments) | 2 | 2 | The fix PR for the missing-directory case used the raw text. |
| 30528 | Diagnostics resource timeline read history once and stayed empty while live counters updated | no SZZ target (pure addition) | n/a | n/a | 2 | 3 | Fix adds 5 s polling. |
| 30480 | `t3 up --base-dir` dropped `--base-dir` in two printed next-step hints | #27996 "feat(cli): t3 up asks how your other devices reach this machine" (+1263/-322, 2026-10-31) | medium (2 lines) | missed for these two hints; adjacent: Macroscope flagged the same omission on the fallback `t3 serve` hint (up.ts:215, :263) and the PR fixed those | 2 | 2 | Same defect class was caught elsewhere on the same PR. |
| 30479 | Command output lost text after an unterminated OSC string (ESC restarts sequence) | #15094 "fix: command output streams live while it runs" (+3287/-41, 2026-10-16) | high (1 line) | missed (Macroscope: High on cursor-move overflow and resume text in the same file; none on OSC termination) | 2 | 4 | Needs terminal-parser knowledge (xterm behaviour). |
| 30423 | GitLab threads always `isOutdated: false` | no clear target: SZZ blames #4849 (GitLab adapter import, +34121) and same-day PRs #30411/#30433/#30397 on touched lines | n/a | n/a | 2 | 3 | Missing capability, not a regression. |
| 30411 | GitLab comments had `url: null` | no clear target (#4849 import, #6039, same-day #30383/#30403) | n/a | n/a | 1 | 2 | Missing capability. |
| 30403 | Edited GitLab comments never set `editedAt`, so a rewritten bot comment never woke `watch_pull_request` | no clear target (SZZ #30383, 1 line, same-day PR on main) | n/a | n/a | 2 | 3 | Missing capability. |
| 30397 | Unresolved overview threads on a GitLab MR were plain comments (no Fix button, left out of "Fix findings") | no clear target (#4849 import, 8 lines) | n/a | n/a | 2 | 3 | Missing capability. |
| 30433 | GitLab checks filter did nothing; review filter ran after fetch; "changes requested" never reported | no SZZ target (blames #21514, a comment-halving refactor, noise) | n/a | n/a | 2 | 4 | Missing capability. |

Bot coverage on the 7 SZZ-resolved bugs: caught 0, missed 6, partial-adjacent 1 (#30480), not checked 1 (#30652, low-confidence target).

## 4. Catalogue candidates (real bugs, severity >= 3)

All five are Track A bugs fixed before merge: head is the commit the bot commented on.

| id | PR(s) | golden description | base | head | caught by |
| --- | --- | --- | --- | --- | --- |
| pr-comment-chip-add-to-chat-thread-only-and-cross-repo | #30579 | "Add to chat" resolves the comment id against `detail.comments` only, so comments that exist only in review threads do nothing, and the existing-reference check compares PR number instead of URL, so a `#42` from another repo suppresses this repo's PR reference. | 03dbb2fb4866ceb3b06950cf580614562199cc42 | a8ae50f4ae8434bfc8259e9d4a0986ee8967ae71 | Macroscope (both) and CodeRabbit (the number check) |
| git-pr-lookup-local-tracking-branch-remote-dot | #30563 | A branch whose remote is `.` (tracking a local branch) is still treated as published in the PR lookup cache, so the unpublished-branch guard is bypassed and an unrelated same-name PR or the tracked branch's PR is shown. | d51bc58f5e05123a416a3737ac4bce42d1d76b7c | 38592140de982d37469a9679b63710d216d11964 | CodeRabbit |
| gitlab-set-labels-unknown-beyond-first-page | #30483 | `setLabels` validates names against one page of 100 project labels and discards the truncated flag, so an existing label past the first page is rejected as unknown and the update skipped. | d694c44d07842a2b403b6c4dd98950ba6e1c6339 | c2adfe0b886730abbd991cffb241f1b7b970aad4 | Macroscope |
| gitlab-optional-graphql-read-fails-whole-detail | #30483 T2, #30518, #30453 | An optional GraphQL permission read (label edit, maintainer edits, branch delete) is run inside the core merge-request detail read without a fallback, so its decode or CLI failure makes the whole detail, previews and checks fail instead of defaulting the permission to false. | d694c44d07842a2b403b6c4dd98950ba6e1c6339 | c2adfe0b886730abbd991cffb241f1b7b970aad4 | CodeRabbit (3 times; the same defect pattern repeated in three consecutive PRs) |
| gitlab-diff-refs-null-sha-fails-decode | #30423 | `diff_refs` is decoded as three required strings, so a merge request with `base_sha: null` (orphaned source branch) fails the entire decode and cannot be opened. | bd7da7fa485d20d361e9c7146bfe29c0bcf82d5a | 2b8444e2e6ec7edc691847032f4ec3ba571afbc9 | CodeRabbit |

Not promoted: #30453 T3 (non-atomic branch delete, real but platform-limited, disputed, sev 3 design risk).

## 5. Observations

- Nine of 32 threads (28%) were wrong and every one was withdrawn by CodeRabbit after the author replied with evidence (a repro against pinned fff, `glab` exit codes, GitLab source). CodeRabbit's willingness to withdraw is useful, but its Major labels on these were inflated: 6 of its 11 Major threads here were wrong.
- The same defect pattern came up three times in consecutive GitLab PRs (optional permission read fails the whole detail: #30483, #30518, #30453) and CodeRabbit caught it each time, but only after the author had already repeated it; there was no cross-PR learning on the author's side.
- Macroscope found the most consequential logic bugs it commented on (#30579 T1/T2, #30483 T1, all High), but its replies to "fix it" requests return "no permissions".
- Escaped bugs: in 6 of 6 SZZ-checked cases neither bot commented on the defect at introduction, including PRs with many bot comments (#4855, #15094, #27996). Several fixes are sibling or edge cases of an earlier fix (#20264, #29360, #9885), which a reviewer reading the previous PR would not see.
- Most GitLab "fix" PRs are really missing capabilities; SZZ on them lands on the #4849 import or same-day PRs and is noise, so they are not escaped-bug evidence.
