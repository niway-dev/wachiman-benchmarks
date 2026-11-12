# Wachiman 1.12.0 local review: commit a561750 of t3bench-24079 against its parent (cf5db8a)

Rendered from `wachiman.json` (the same run; not a second run). Model: Claude Opus 5.5 via Claude Code 2.1.321, effort high, profile isolated.

Coverage: 5 of 5 changed files reviewed.

## Findings (1)

### [fix] Subagent request map goes stale while publishing is disabled or unlinked, so the parent can stay stuck on "Approval needed"

`apps/server/src/relay/AgentAwarenessRelay.ts:546` · topic bug · confidence medium

`trackSubagentRequest` only runs after the publication-disabled and missing-relay-config early returns (lines 466-483), but `subagentRequests` (line 401) is never cleared or rebuilt. Here is a sequence that breaks it. A child raises an approval while publishing is on, so its entry is stored and the parent is published as `waiting_for_approval`. Then publishing is turned off, for example with `t3 connect publish` from another process. While it is off, the child's request resolves and its run ends. Those events return before line 546, so the entry stays. When publishing is turned back on, nothing rebuilds the map: the startup snapshot runs only once, because `activeSnapshotPublishedRef` is never reset (lines 806-811). The parent's next event then publishes the stale "approval" from `pendingSubagentRequestFor` at line 568. The child has finished and sends no more events, so nothing corrects the parent's row, and the user's activity card keeps showing "Approval needed" with no error. `resetPublishedConnection` clears `publishedStateByThreadRef` but not this map. One fix: run `trackSubagentRequest` (it already has the shell) before the gates, but only for subagent shells, so the disabled path doesn't get a shell read on every event. Another: clear `subagentRequests` in `resetPublishedConnection` and reset `activeSnapshotPublishedRef` so a catch-up rebuilds the map from the shell snapshot.

