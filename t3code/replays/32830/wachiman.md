# Wachiman 1.12.0 local review: replay of pingdotgg/t3code#32830

> Rendered from `wachiman.json` with `jq` (a copy of its fields, no new review). `wachiman local` has no option to re-render a saved result, and a second run would cost another review and could differ.

- Change: commit 97a175e of t3bench-32830 against its parent (f3237a9)
- Engine: Wachiman 1.12.0; provider: Claude Opus 5.5 via Claude Code 2.1.321, effort high, profile isolated
- Coverage: 4 of 4 files reviewed, partial: false

## Summary

I reviewed all four files and found two likely bugs, both medium confidence. Both come from treating a failed or still-loading `threadTitles` lookup as if the thread exists.

**Bugs (fix):**
- **Web:** a link to a machine this client can't reach used to show "Thread on another machine". Now it shows a clickable "Thread" chip with an "Open thread" tooltip, pointing at a thread that can't load.
- **Mobile:** while the lookup is loading or after it fails, the placeholder "Thread" title counts as a match. That skips the step that finds a v1 link's thread in another connected environment, so tapping the link opens the wrong one.

**Worth considering:**
- Removing the tooltip branch in `ThreadContextChip` changes two other callers, the message chips and the composer chips. Truly deleted threads there now say "Open thread".
- Each unloaded link sends its own lookup with no caching. A message with many links to older threads means one round trip per link.
- The web title check uses `!== undefined` where the existing sibling uses `Object.hasOwn`. A thread id like `constructor` would make it throw.

The new browser test covers loading, failure, success and empty results. It mocks the entity hooks, so it doesn't exercise the case of a link to another machine.

## Findings

### W1. [fix] A link to a machine this client can't reach now shows a live "Thread" chip instead of "Thread on another machine"

`apps/web/src/components/chat/MarkdownThreadLink.tsx:63` · topic bug · confidence medium

Before this change, a thread the client didn't know rendered `UnresolvedChip` with `unknownThreadLinkLabel`. That label tells the user "Thread on another machine" when a v2 link names a different environment. Now the unresolved chip only renders when `titles.isSuccess && !titles.isPending`. For a v2 link to an environment that isn't connected, the `threadTitles` query runs against that environment (line 55). It can't succeed, so it stays Initial or turns into Failure (`EnvironmentRpcUnavailableError`, packages/client-runtime/src/state/runtime.ts:886). The chip then renders as a clickable `ThreadContextChip` titled "Thread" with the "Open thread" tooltip, and it navigates to a route that can't load. An older server without `getThreadTitles` hits the same failure, so every unknown link looks openable. Keeping transient failures clickable is fine. But when `props.link.environmentId` differs from `props.environmentId` and isn't connected, fall back to the existing `unknownThreadLinkLabel` chip rather than a fake "Thread" link.

### W2. [fix] Placeholder "Thread" title stops v1 links from being matched to another environment while loading or after a failure

`apps/mobile/src/state/entities.ts:73` · topic bug · confidence medium

`threadTitleAtom` now returns "Thread" (never null) whenever the `threadTitles` query hasn't succeeded. `resolveThreadLink` (lines 236-242) treats any non-null title as proof the thread exists. So for a v1 link, the written candidate in the message's environment wins whenever the query is Initial or failed. `guessThreadLinkRef`, which would find the thread in the other connected environment it actually lives in, is never reached. The same thing happens when the percent-decoded candidate is the real one: the written candidate wins first. A tap in ThreadFeed (`apps/mobile/src/features/threads/ThreadFeed.tsx:2853`) then opens the wrong environment's thread. Chip icons (line 146) resolve against the wrong ref too. If the RPC keeps failing (an older server, or the environment offline), this stays wrong for the session. Only a settled success with no title returns null and lets the guess run. Consider keeping the placeholder in the label path only, and having `resolveThreadLink` require a real shell or successful title.

### W3. [consider] Deleted threads in message and composer chips now say "Open thread"

`apps/web/src/components/ThreadContextChip.tsx:44` · topic bug · confidence medium

Dropping the `shell ? … : "Thread no longer available"` branch also affects the other callers: `UserMessageContextChips.tsx:321` and `composerContextPresentation.tsx:337`. Those callers never run a title lookup. For them, a missing shell used to show "no longer available", and it now promises "Open thread" for threads that really were deleted. The Markdown path now decides availability itself, but these two callers have no replacement signal. You could pass availability in as a prop, or run the same title lookup there.

### W4. [consider] One `getThreadTitles` RPC per unloaded link, with no caching

`apps/web/src/components/chat/MarkdownThreadLink.tsx:56` · topic perf · confidence medium

Each `UnloadedThreadLink` issues its own query, keyed by its own one- or two-id input. The family has `staleTimeMs: 0, idleTtlMs: 0` (packages/client-runtime/src/state/orchestration.ts:54-55), so it refetches on every remount, e.g. when virtualized message rows scroll back into view. Mobile does the same per ref (`apps/mobile/src/state/entities.ts:66`), even though `threadLinkRefs` already collects every ref in a message. A message with many links to older threads sends one round trip per link. Batching per message, as `useLiveThreadLinkLabels` already groups refs, would make it one.

### W5. [consider] `!== undefined` on the titles record matches prototype keys

`apps/web/src/components/chat/MarkdownThreadLink.tsx:62` · topic bug · confidence low

The sibling caller uses `Object.hasOwn(resolvedThreadTitles, threadId)` (ThreadRelationshipsControl.tsx:538). Here `titles.data?.[ref.threadId] !== undefined` holds for an id like `constructor`, and line 68 then calls `.trim` on a Function and throws. Link ids come from agent-written Markdown, so using `Object.hasOwn` would match the sibling and remove the edge case.

