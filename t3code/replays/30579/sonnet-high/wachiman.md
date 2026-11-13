# Wachiman 1.12.0 local review (Sonnet 5.5 high): replay of pingdotgg/t3code#30579

> Rendered from `wachiman.json` with `jq` (a copy of its fields, no new review). `wachiman local` has no option to re-render a saved result.

- Change: commit dcb8635 of t3bench-30579 against its parent (91dc71f)
- Engine: Wachiman 1.12.0; provider: Claude Sonnet 5.5 via Claude Code 2.1.321, model claude-sonnet-5-5, effort high, profile isolated
- Coverage: 7 of 7 files reviewed, partial: false
- Execution: 21 turns, 125.136 s in the model, $0.413 estimated at API prices (not a bill)

## Summary

The change adds an "Add to chat" action on review threads and comments. It writes `pr-comment:` and `pr-reference:` chips into the attached composer. I found two bugs worth fixing:

- **Hollow chip:** `readableBody` returns `""` instead of `null` when a body's only text is after an unclosed `<!--`. The button still shows, and a click adds a chip containing just `"author: "`.
- **Number collision:** the panel decides whether the composer already has a PR reference by PR number only, so a same-numbered PR from another repository suppresses the reference.

Smaller notes: the comment-chip id isn't scoped to the PR; Timeline reply cards add the whole thread, unlike the Summary tab; the Resolve button's `ml-auto` follows a prop instead of whether Add to chat renders; and the switch of `reviewThreadContext` to `readableBody` also changes Fix prompts, which isn't tested. I did not run the code or tests. I did trace the new tests by hand against `readableBody`; the cases I traced give their expected output.

## Findings

### W1. [fix] readableBody returns "" (not null) for a body whose only content is an unclosed `<!--`

`apps/web/src/components/pullRequest/pullRequestDetail.logic.ts:709` · topic bug · confidence high

The docstring says "Null for a body with no words", but the early guard uses `visibleBody`, whose regex only strips *closed* comments. A body like `<!-- bot state` (or `text` after a stray `<!--` at the start) passes the guard, then the line loop drops everything after the unclosed `<!--`, and the function returns `""`. Callers only test for `null`: `buildPullRequestCommentContext` (line 1161) builds a chip with text `"octocat: "`, and `reviewThreadContext` (line 856) emits `"octocat: "` lines. The UI gates the Add to chat buttons on `visibleBody(...) !== null` (PullRequestSummaryTab `chatSubject`, ReviewThreadCard line 255, Timeline `event.body`), so the button is shown and clicking it adds a hollow chip plus a success toast. Fix: return `null` when the joined result is empty, i.e. `const text = kept.join("\n").trim(); return text === "" ? null : text;`, and add a case to the test file.

### W2. [fix] "Already has the pull request" is decided by number, but numbers collide across repositories

`apps/web/src/components/pullRequest/PullRequestDetailPanel.tsx:1077` · topic bug · confidence medium

`buildPullRequestReferenceContext` keys its chip by URL (`pr-reference:${url}`, logic.ts:1138) with the comment "repositories can share pull request numbers". Here `hasPullRequest` compares only `pullRequest?.number === detail.number`. If the composer already holds a chip for another repository's #N (e.g. from a composer `#` reference), the reference to this pull request is skipped and the added comment arrives with no pointer to which PR it belongs to; the section ids (`pull-request:N`) collide too. Compare `existing.pullRequest?.url === detail.url` (the stored url is `boundedField(url)`, so compare against the same bounded form or compare the chip id).

### W3. [consider] Chip id `pr-comment:<commentId>` is not scoped to the pull request

`apps/web/src/components/pullRequest/pullRequestDetail.logic.ts:1164` · topic bug · confidence medium

The Timeline tab itself notes "Host comment ids can collide across pull requests" (PullRequestTimelineTab.tsx:380), and `addReviewComment` replaces any entry with the same id (composerDraftStore.ts:3772). A composer that moves between pull requests can have a chip from PR A silently overwritten by a same-id comment from PR B. Scope the id by something unique to the PR, e.g. its URL as the reference chip does.

### W4. [consider] Add to chat on a thread reply adds the whole conversation, and the Summary tab deliberately does not offer it on replies

`apps/web/src/components/pullRequest/PullRequestTimelineTab.tsx:272` · topic bug · confidence medium

Summary tab hides the button on replies ("A reply goes with its conversation, from the card that heads it", PullRequestSummaryTab.tsx:603). Timeline `ReviewThreadEvent` renders `ConversationCard` for each reply (line 472), so every reply gets the same icon button; `addCommentToChat` in the panel then looks up the thread containing the comment and adds the entire thread. The tooltip "Add to chat" on one reply therefore adds something larger than that reply, and behaves differently from the Summary tab. Either hide the button on replies here too or document the behaviour in the tooltip.

### W5. [consider] Resolve button's `ml-auto` depends on `onAddToChat` being passed, not on the Add to chat button rendering

`apps/web/src/components/pullRequest/PullRequestReviewAnnotation.tsx:270` · topic bug · confidence high

The Add to chat button renders only when `onAddToChat && comments.some(visibleBody...)` (line 255). The Resolve button drops `ml-auto` when `onFix || onAddToChat` is truthy. For a thread with no visible text and no `onFix`, `onAddToChat` is set but no button renders, so neither button carries `ml-auto` and Resolve sits left. Compute the render condition once and use it for both class names.

### W6. [consider] readableBody now also changes fix-in-thread prompts, but only the "no words" thread case is tested

`apps/web/src/components/pullRequest/pullRequestDetail.logic.test.ts:1017` · topic tests · confidence medium

`reviewThreadContext` (logic.ts:855) switched from `visibleBody` to `readableBody`, so the text of existing `Fix` hand-offs (`pull-request-finding:` chips) now loses HTML comments and handles fences, which is a behaviour change outside "Add to chat". No test covers a thread with real text plus bookkeeping comments or multiple comments, and none covers the unclosed `<!--` case. Add a row to the existing thread test.

