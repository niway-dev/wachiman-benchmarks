# Wachiman 1.12.0 local review (Sonnet 5.5 high): replay of pingdotgg/t3code#24079

> Rendered from `wachiman.json` with `jq` (a copy of its fields, no new review). `wachiman local` has no option to re-render a saved result.

- Change: commit a561750 of t3bench-24079 against its parent (cf5db8a)
- Engine: Wachiman 1.12.0; provider: Claude Sonnet 5.5 via Claude Code 2.1.321, model claude-sonnet-5-5, effort high, profile isolated
- Coverage: 5 of 5 files reviewed, partial: false
- Execution: 10 turns, 72.216 s in the model, $0.289 estimated at API prices (not a bill)

## Summary

The change is correct for the common paths: it moves the subagent-request classification into shared code, tracks child requests in the relay, republishes the top-level parent, and the new tests match the code. One real defect: `trackSubagentRequest` runs only after the publishing-enabled and relay-config gates, so while publishing is disabled or the relay is unlinked the in-memory map can go stale. After the relay is re-enabled, the parent can then publish a wrong \"waiting\" state with nothing to correct it. I also suggest a few extra test cases for nested subagents, mixed requests and archived children. I did not run any code.

## Findings

### W1. [fix] Subagent request map is not updated while publishing is disabled or the relay is unlinked, so a parent can later publish a stale "waiting" state

`apps/server/src/relay/AgentAwarenessRelay.ts:546` · topic bug · confidence medium

`trackSubagentRequest` runs only after `publishThreadUnsafe` has passed the `publishAgentActivity` check (466-474) and the `relayConfig` check (475-483). Both of those return early. While publishing is off or the relay is unlinked, a child's request can clear, or the child can be archived or deleted, and `subagentRequests` never hears about it. The entry keeps its old `approval` or `user_input` value. After publishing is re-enabled, `resetPublishedConnection` clears `publishedStateByThreadRef`, and the parent is republished from `pendingSubagentRequestFor(subagentRequests, threadId)` at line 568. That read still sees the stale entry, so the parent shows "Approval needed" or "Waiting for input" on the relay. Only a later event on that same child can fix it. A child whose run has ended may never emit another event, and the early return at 548-555 means `publishActiveThreadsUnsafe` does not clear the entry either. Nothing logs or surfaces this, and the user sees a wrong state. Fix: call `trackSubagentRequest` right after `threads.getThreadShell` and before the enabled and config gates. This needs the shell read to move up with it. Parent enqueues triggered while disabled return early in the same way, so nothing extra is published.

### W2. [consider] Relay test covers only one direct child going waiting and then clearing

`apps/server/src/relay/AgentAwarenessRelay.test.ts:327` · topic tests · confidence medium

The new test covers a direct child of the top-level thread, with the request appearing and then clearing. The code adds other branches that nothing exercises: a nested subagent resolved through `findTopLevelThreadId`, two children where `approval` has to win over `user_input` in `pendingSubagentRequestFor`, a child that is archived or deleted while waiting, and a cycle or missing parent in the lineage. The approval-over-input choice and the top-level resolution are the logic most likely to regress. A focused case or two on those would be worth adding.

