# Wachiman 1.12.0 local review (Sonnet 5.5 high): replay of pingdotgg/t3code#33758

> Rendered from `wachiman.json` with `jq` (a copy of its fields, no new review). `wachiman local` has no option to re-render a saved result.

- Change: commit a908368 of t3bench-33758 against its parent (ddcbb24)
- Engine: Wachiman 1.12.0; provider: Claude Sonnet 5.5 via Claude Code 2.1.321, model claude-sonnet-5-5, effort high, profile isolated
- Coverage: 6 of 6 files reviewed, partial: false
- Execution: 29 turns, 179.601 s in the model, $0.526 estimated at API prices (not a bill)

## Summary

The change adds native `/goal` support for OpenCode: it reads the goal over RPC, mirrors `goal.changed` events, and holds a turn open while the goal is active. The tests exercise the happy paths. Two defects stand out. The goal reads added to `reconcile` are sequential and sit under the lock and the 15s reconcile budget, so a slow server can fail reconnects. A bare `/goal` skips the 2.2.5 version gate that the resume and reconcile paths apply, and the Orchestrator and turn-start service treat OpenCode as a goal driver for every version. Smaller points: an undecodable goal event is dropped without a log while turn completion depends on the last decoded state, `/goal show` updates the thread outside the lock, whether Stop and `/goal resume` end a turn is unconfirmed, the version literal is duplicated, and the docs wording is ambiguous.

## Findings

### W1. [fix] Goal reads in reconcile run under the 15s reconcile budget and the lock, before any real reconcile work

`packages/provider-opencode/src/server/v2/adapter.ts:2642` · topic bug · confidence medium

`reconnect` runs `lock.withPermit(reconcile).pipe(Effect.timeout(RECONCILE_TIMEOUT))` (line 2752, 15s). The new loop at 2642-2649 reads the goal of every loaded thread one after another, each with its own `INVENTORY_TIMEOUT` (5s). Nothing bounds the loop as a whole except the outer 15s. With three or more loaded sessions on a server that is slow or hung right after a restart, the loop alone uses the whole budget. The reconcile then times out before it reaches the part that ends lost executions, and `reconnect` retries. After `RECONNECT_ATTEMPTS` failures the session is failed through `failAll`. The event loop is also blocked on the same lock for that time. `threads` includes every registered session, not just the ones with an active turn. The loop also runs before the early return at 2658, so an idle adapter pays one RPC per thread on every reconnect.

Fix: read goals only for threads that need it (`state.active !== undefined`, which is what `endExecution` uses). Run the reads concurrently, or after the turn-ending work, with one overall bound.

### W2. [fix] `/goal` show is not gated on OpenCode >= 2.2.5, unlike the other goal call sites

`packages/provider-opencode/src/server/v2/adapter.ts:3457` · topic bug · confidence medium

`resumeThread` (3621) and `reconcile` (2642) only call `opencode.goal` when `connection.version >= 2.2.5`. The `show` branch in `submit` calls `readGoal` unconditionally. The V2 adapter supports older OpenCode 2.x: the minimum is 1.14.19 in OpenCode status checks and the testkit default is 2.0.18. On those versions `rpc.call` for `opencode.goal` is not expected to exist, so a bare `/goal` fails the turn through the `tapError` at 3776 with a raw provider error.

The Orchestrator and `ProviderTurnStartService` also treat `opencode` as a native goal driver for every version (Orchestrator.ts:1174, ProviderTurnStartService.ts:845-848). On an older server, `/goal <text>` is sent as plain text, because `goal` is not in `command.list`. It still stops the active run, as a goal command does (Orchestrator.ts:6114-6141). Its handoff history is also deferred to a later turn, as a goal turn's is. The docs say 2.2.5+, but the code does not enforce it.

Fix: check the version in `submit` for the show branch. Ideally also make `goalDriverFor` and the turn-start check depend on whether the instance supports goals.

### W3. [consider] A goal payload that fails to decode is dropped silently while turn completion depends on the last decoded goal

`packages/provider-opencode/src/server/v2/adapter.ts:2469` · topic bug · confidence medium

`rpc.opencode.goal.changed` events that fail `decodeGoal` return with no log (2469-2470). `NativeGoal` accepts only `active|paused|complete` and requires `objective` to be non-empty. Whether a turn is held open depends on `state.providerThread.goal?.status === "active"` (2332, 2343). If OpenCode sends a terminal status this schema does not list, or a shape change, the last decoded `active` stays. The turn is then held after its next successful execution with nothing to release it, until the user presses Stop. There is no log either. Log the decode failure at least, as `Effect.ignore({ log: true })` does at the other call sites. Consider treating an unreadable goal as not active.

### W4. [consider] `/goal` show updates the thread's goal outside the adapter lock

`packages/provider-opencode/src/server/v2/adapter.ts:3459` · topic bug · confidence low

`readGoal(state)` in the show branch (3459) runs without `lock.withPermit`. The `resumeThread` call site wraps it in the lock (3623), and `handleEvent` runs under the lock (2765). `updateGoal` rebuilds `state.providerThread` from a spread and then yields on `DateTime.now` before assigning. An event handled in that window, such as a model update at 2477-2479, can be overwritten. Wrap it like the resume path. The `finishTurn` call two lines later already takes the lock.

### W5. [consider] How does an OpenCode goal turn end for `/goal resume` and for Stop?

`packages/provider-opencode/src/server/v2/adapter.ts:3480` · topic question · confidence low

After `session.command`, `pause` and `clear` finish the turn at once. `set` and `resume` rely on an execution starting and the goal later leaving `active`. If `/goal resume` is sent with no paused goal, or on a completed goal, and OpenCode starts no execution and emits no `goal.changed`, the turn never ends. Is that case handled by OpenCode? The tests cover show, pause, clear and set, but not resume.

The docs (composer.md:314-315) also say 'Stopping their goal pauses it'. The adapter does nothing to the goal on interrupt (`interruptTurn`, 3897-3938). It relies on OpenCode pausing the goal and emitting `goal.changed`. If it does not, `goal.status` stays `active` locally. Every later turn on that thread would then be held after its first successful execution (2332). Can you confirm both behaviours against OpenCode 2.2.5?

### W6. [consider] The literal "2.2.5" is repeated at two call sites

`packages/provider-opencode/src/server/v2/adapter.ts:3621` · topic cleanup · confidence high

The goal version gate is written inline at 2642 and 3621, and would have to be repeated at 3457 once that call is gated. Name it once, for example `GOAL_MIN_VERSION` next to the other timeouts and constants at ~550, with a helper such as `supportsGoal()`.

### W7. [consider] No test for the reconcile goal read, `/goal resume`, the pre-2.2.5 path, or an undecodable goal event

`apps/server/src/orchestration-v2/Adapters/OpenCode2AdapterV2.test.ts:5047` · topic tests · confidence medium

The new tests cover resume-time reads, the held turn for set, and show/pause/clear. They do not cover the 2.2.5 gate on the negative side (a version below 2.2.5 must not issue `rpc.call`). The `show` case runs against the default 2.0.18 and asserts that `rpc.call` is sent, so it locks in the ungated behaviour. They also do not cover the reconcile loop at adapter.ts:2642, which holds the lock and uses the shared 15s budget. They do not cover `/goal resume`, or `goal.changed` with a payload that fails to decode. Extend the existing table rows for these rather than adding new `it` blocks.

### W8. [consider] Goals section: 'their goal' is ambiguous, and the OpenCode Stop-pauses claim has no support in the code

`docs/user/composer.md:314` · topic docs · confidence low

'Codex and OpenCode also support `/goal pause` and `/goal resume`. Stopping their goal pauses it.' is hard to parse. It reads as if Stop pauses a goal for both providers, but only Codex's behaviour is implemented here (see the question at adapter.ts:3480). Line 307 is also a single unwrapped line, unlike the surrounding prose. Consider separate bullets for Codex and OpenCode, and state the OpenCode Stop behaviour only once it is confirmed.

