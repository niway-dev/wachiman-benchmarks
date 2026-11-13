# Wachiman 1.12.0 local review (Sonnet 5.5 high): replay of pingdotgg/t3code#32830

> Rendered from `wachiman.json` with `jq` (a copy of its fields, no new review). `wachiman local` has no option to re-render a saved result.

- Change: commit 97a175e of t3bench-32830 against its parent (f3237a9)
- Engine: Wachiman 1.12.0; provider: Claude Sonnet 5.5 via Claude Code 2.1.321, model claude-sonnet-5-5, effort high, profile isolated
- Coverage: 4 of 4 files reviewed, partial: false
- Execution: 25 turns, 116.105 s in the model, $0.416 estimated at API prices (not a bill)

## Summary

The change adds a threadTitles lookup so thread links to archived or omitted threads show a titled chip, on web and mobile. I found two defects to fix and three smaller points. The web lookup indexes the returned titles object with ids taken from message text, so ids like `constructor` crash the render. On mobile, a pending or failed lookup returns \"Thread\" instead of null, which overwrites labeled v1 link text and skips the cross-environment fallback in `resolveThreadLink`. The smaller points are the tooltip now always saying \"Open thread\" for the composer and user-message chips, links to unreachable environments showing as live chips, and no mobile test. I did not run anything; this is from reading the code.

## Findings

### W1. [fix] Plain-object lookup of a link-supplied thread id crashes the render for ids like `constructor`

`apps/web/src/components/chat/MarkdownThreadLink.tsx:62` · topic bug · confidence medium

`titles.data?.[ref.threadId] !== undefined` (line 62) and `titles.data?.[ref.threadId]?.trim()` (line 68) index a plain `Record<ThreadId, string>` (contract: `OrchestrationV2ThreadTitles = Schema.Record(ThreadId, Schema.String)`, packages/contracts/src/orchestrationV2.ts:3729) with an id taken from message text. `t3-thread://v1/constructor` parses as a valid link, because `parseThreadLinkHref` accepts any `ThreadId` (packages/shared/src/threadLinks.ts:61-64). Once the query succeeds with `{}`, `data["constructor"]` is `Object`, which is not `undefined`. `target` is then set, and `.trim()` on a function throws a TypeError while rendering. `toString` and `__proto__` fail the same way. An agent or other-party message can therefore crash the message row. The sibling use of the same query, `ThreadRelationshipsControl.tsx:538`, uses `Object.hasOwn(resolvedThreadTitles, threadId)` for this reason. Use `Object.hasOwn` for the `candidates.find` and the title read. Mobile has the same pattern at `apps/mobile/src/state/entities.ts:72`: `titles.value[ref.threadId] ?? ...` returns the function and `relabelThreadLinks` calls `.trim()` on it.

### W2. [fix] Non-success title lookups return "Thread" (non-null), which resolveThreadLink and relabelThreadLinks treat as a found thread

`apps/mobile/src/state/entities.ts:71` · topic bug · confidence medium

When `threadTitles` is initial, failed or still loading, the atom returns the literal `"Thread"` instead of `null` (lines 71-73). Two consumers rely on `null` meaning unknown.
- `resolveThreadLink` (line 236-239) treats `!== null` as known. A v1 link to a thread in another environment resolves to the message's own environment while the lookup is pending. If the lookup fails, for example because the environment is disconnected, it never reaches the `guessThreadLinkRef` fallback (line 240-242). `ThreadFeed.tsx:2853` then opens the wrong target, and `threadChipIconsAtom` gets a wrong icon.
- `relabelThreadLinks` (packages/shared/src/threadLinks.ts:208-210) keeps a labeled v1 link's written label only when `title()` is `undefined`, so the label can stay and the link can open elsewhere. A `"Thread"` answer rewrites `[My essay](…)` to `[Thread](…)`. On failure that stays; while loading it flickers.
The web `UnloadedThreadLink` also shows a generic `"Thread"` chip while loading and on failure, but it only affects display there. Return `null` unless the query has settled with the title, or keep the placeholder out of the shared atom.

### W3. [consider] Tooltip no longer says "Thread no longer available" for the composer and user-message chips

`apps/web/src/components/ThreadContextChip.tsx:44` · topic bug · confidence medium

The `shell ? "Open thread" : "Thread no longer available"` branch is now always "Open thread". `MarkdownThreadLink` was the only caller that now resolves titles itself. The composer chip (`composerContextPresentation.tsx:337`) and the user-message chip (`UserMessageContextChips.tsx:321`) also render this component. For a record whose thread is deleted or not in the shell, they previously said it was unavailable. They now say "Open thread" and link to a dead route. Keep the old branch, or have `MarkdownThreadLink` pass an explicit prop, instead of removing the signal for those callers.

### W4. [consider] Links to another environment now render as a live chip when that lookup never succeeds

`apps/web/src/components/chat/MarkdownThreadLink.tsx:56` · topic question · confidence medium

For a v2 link with a different `environmentId`, `UnloadedThreadLink` queries that environment. Only a successful lookup with no match yields `UnresolvedChip` (line 63). If the environment is not connected, not saved on this client, or the request fails, the user sees a normal `Thread` chip that navigates to `/$environmentId/$threadId`. Before this change they saw the `Thread on another machine` unresolved chip, which `unknownThreadLinkLabel` still produces on the success path. The test asserts the failure state keeps the generic chip (test lines 48-51). Is that intended for an unreachable environment, as opposed to a transient error on a connected one?

### W5. [consider] No test covers the new mobile title-lookup behavior

`apps/mobile/src/state/entities.ts:62` · topic tests · confidence medium

The `threadTitleAtom` change alters what `resolveThreadLink`, `useLiveThreadLinkLabels` and `useThreadChipIcons` return for threads absent from the shell. This pull request adds only a web browser test. Per AGENTS.md, logic and state changes get a test. The loading, failure and empty-success branches are the ones where the null versus "Thread" distinction matters, and none is exercised.

