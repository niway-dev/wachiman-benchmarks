# Wachiman review of branch `bench/pr-276` of pr-276 against origin/replay/pr-276/base (merge-base 400c80e), at f91b56d

All 19 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

4 finding(s): 4 to consider

## Findings

### 🟡⚡ **Consider · perf: Skipped open-window revisions still use up the `limit` slots, so closed ones can wait behind them (confidence medium)**

`packages/application/src/cloud/retry-pending-deletes.ts:21`

`listDeleting(limit)` returns the oldest `deleting` rows by `updatedAt` (`cloud-asset.repository.ts:534-541`). The window filter is applied only after that, in the loop. If the first `limit` rows all still have an open window (for example, a burst of deletes of fresh uploads), the run finishes 0 rows, and revisions further down the list whose window has already closed are not reached. The delay is bounded (≤ TTL + grace), but each run spends its budget on rows it already knows it will skip. You could filter in the query instead, with `ticket_expires_at < now - grace` as `listReservedExpiredBefore` does (`:519-532`), or pass a `before` into `listDeleting`.

### 🟡📝 **Consider · docs: "Rare in practice" is wrong: almost every delete within ~3 h of an upload gets deferred (confidence high)**

`apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:171`

The window is `ticketExpiresAt + RESERVATION_GRACE_SECONDS` (`ticket-window.ts:10`), with a 3 h grace (`cloud-limits.ts:30`). A revision can only become `ready` after a PUT that started before its 5-minute ticket expired, so almost every confirmed revision has an open window for about 3 h after confirm, not only those "confirmed within 5 minutes of its last ticket". In practice, any user who deletes a cloud copy within about 3 h of uploading it hits the deferred branch. The asset stays `deleting` and its bytes keep counting as used. Until NIW2-328 schedules `retryPendingDeletes` (spec :132-134), they count indefinitely. Open question 1 and the release-order discussion should cover the delete case too, not only cancel.

### 🟡📝 **Consider · docs: "And vice versa" contradicts the boundary note later in the spec (confidence high)**

`apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:157`

Line 157-158 says the sweep and the predicate agree in both directions. The sweep lists `ticketExpiresAt < now - grace` (strict, `sweep-expired-reservations.ts:22-23` plus `cloud-asset.repository.ts:526`), while `ticketWindowClosed` uses `<=`. At the exact instant the predicate already says closed and the sweep does not list yet, and the spec's own remaining item 1 (:392-396) says exactly that. Replace "and vice versa" with the one-instant asymmetry, or drop it.

### 🟡🧪 **Consider · tests: Existing cancel/delete tests now depend on the wall clock (confidence high)**

`packages/application/src/cloud/cloud.test.ts:594`

Now that the window check exists, the pre-existing `cancelUpload` test (:579-613) and the `deleteCloudCopy` tests in "list / download / delete / usage" call the use cases without `now`, so they fall back to `new Date()`. They pass only because the real clock is more than TTL + grace after the fixture `NOW`. If `NOW` is ever moved to the future, or a fake timer is introduced, they would silently test the deferred branch instead. Pass `now: AFTER`-style explicit dates. The spec lists this as remaining work for the cancel test, and it applies to the delete tests as well.

## Summary

I reviewed all 19 files in this part and found no blocker or fix-level issue. There are four "consider" findings.

**What I checked:**
- **Deferred cancel and delete:** both match the sweep's claim-first order. The new check only defers work and never releases quota early.
- **Legacy upload routes:** their removal is clean, with no remaining callers.
- **Asset-list cursor:** the new schema accepts exactly what the repository's encoder produces.

**Findings (all "consider"):**
- **Retry job budget (`retry-pending-deletes.ts:21`):** rows whose ticket window is still open are skipped, but they still count against the run's `limit`. Rows that are ready to finish can wait behind them for up to about 3 hours. Filtering by the window in the database query would avoid this.
- **Spec claim that deferred deletes are "rare in practice" (line 171):** this is wrong. Almost every cloud copy deleted within about 3 hours of its upload is deferred, and its bytes keep counting against the user's storage until the retry job runs. That job is not scheduled until NIW2-328 ships.
- **Spec "and vice versa" (line 157):** the spec says the sweep and the new window check agree in both directions. Its own later note (lines 392-396) says they differ at the exact boundary instant.
- **Wall-clock-dependent tests (`cloud.test.ts:594`):** the existing cancel test and the existing delete tests call the use cases without an explicit `now`. They now pass only because the real clock is well past the test fixture date.

<details><summary>What the change connects to (4 closed, 0 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Closed, with the lines they rest on**
- cancelUpload defers release/delete while the ticket window is open (`packages/application/src/cloud/cancel-upload.ts:36`) — The router returns { released: false } (the same as for 'not reserved'). Bytes and the pending slot stay counted in /me/storage until the sweep runs. If it fails: The sweep is not scheduled yet (spec), so deferred cancels hold their bytes and pending slot until NIW2-328 ships. The client cannot tell a deferral from a no-op. Evidence: `packages/application/src/cloud/cancel-upload.ts:33-40`, `packages/application/src/cloud/sweep-expired-reservations.ts:22-29`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:519-532`, `apps/server-hono/src/modules/cloud/cloud.router.ts:104-114`.
- deleteCloudCopy skips the physical delete while the window is open (`packages/application/src/cloud/delete-cloud-copy.ts:29`) — The router logs cloud.delete.ok and returns deleted: true. The quota keeps counting until retryPendingDeletes runs after the window closes. If it fails: Without the cron, the bytes stay counted indefinitely. Affects any delete within about TTL + 3 h of upload. Evidence: `packages/application/src/cloud/delete-cloud-copy.ts:24-39`, `apps/server-hono/src/modules/cloud/cloud.router.ts:143-154`, `packages/domain/src/constants/cloud-limits.ts:25-30`.
- retryPendingDeletes skips revisions with an open window (`packages/application/src/cloud/retry-pending-deletes.ts:21`) — Closed rows may wait for a later run. If it fails: Bounded delay. See the perf finding. Evidence: `packages/infra-db/src/repositories/cloud-asset.repository.ts:534-541`, `packages/application/src/cloud/retry-pending-deletes.ts:16-24`.
- Contract validates the asset-list cursor with assetCursorSchema (`apps/server-hono/src/contract/cloud.contract.ts:47`) — A malformed cursor now gets a 400 instead of a silent first page or a driver error. Evidence: `packages/domain/src/schemas/cloud-asset.ts:276-294`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:96-108`, `apps/server-hono/src/modules/cloud/cloud.router.ts:116-124`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 1 | 19 | 998 | 4 | reviewed | 10 | $0.63 |

Cost: $0.63, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 1 call(s), 10 turn(s), 1 min 40 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of f91b56d below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. packages/application/src/cloud/retry-pending-deletes.ts:21 · 🟡⚡ Consider · perf: Skipped open-window revisions still use up the `limit` slots, so closed ones can wait behind them (confidence medium)
   `listDeleting(limit)` returns the oldest `deleting` rows by `updatedAt` (`cloud-asset.repository.ts:534-541`). The window filter is applied only after that, in the loop. If the first `limit` rows all still have an open window (for example, a burst of deletes of fresh uploads), the run finishes 0 rows, and revisions further down the list whose window has already closed are not reached. The delay is bounded (≤ TTL + grace), but each run spends its budget on rows it already knows it will skip. You could filter in the query instead, with `ticket_expires_at < now - grace` as `listReservedExpiredBefore` does (`:519-532`), or pass a `before` into `listDeleting`.
2. apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:171 · 🟡📝 Consider · docs: "Rare in practice" is wrong: almost every delete within ~3 h of an upload gets deferred (confidence high)
   The window is `ticketExpiresAt + RESERVATION_GRACE_SECONDS` (`ticket-window.ts:10`), with a 3 h grace (`cloud-limits.ts:30`). A revision can only become `ready` after a PUT that started before its 5-minute ticket expired, so almost every confirmed revision has an open window for about 3 h after confirm, not only those "confirmed within 5 minutes of its last ticket". In practice, any user who deletes a cloud copy within about 3 h of uploading it hits the deferred branch. The asset stays `deleting` and its bytes keep counting as used. Until NIW2-328 schedules `retryPendingDeletes` (spec :132-134), they count indefinitely. Open question 1 and the release-order discussion should cover the delete case too, not only cancel.
3. apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:157 · 🟡📝 Consider · docs: "And vice versa" contradicts the boundary note later in the spec (confidence high)
   Line 157-158 says the sweep and the predicate agree in both directions. The sweep lists `ticketExpiresAt < now - grace` (strict, `sweep-expired-reservations.ts:22-23` plus `cloud-asset.repository.ts:526`), while `ticketWindowClosed` uses `<=`. At the exact instant the predicate already says closed and the sweep does not list yet, and the spec's own remaining item 1 (:392-396) says exactly that. Replace "and vice versa" with the one-instant asymmetry, or drop it.
4. packages/application/src/cloud/cloud.test.ts:594 · 🟡🧪 Consider · tests: Existing cancel/delete tests now depend on the wall clock (confidence high)
   Now that the window check exists, the pre-existing `cancelUpload` test (:579-613) and the `deleteCloudCopy` tests in "list / download / delete / usage" call the use cases without `now`, so they fall back to `new Date()`. They pass only because the real clock is more than TTL + grace after the fixture `NOW`. If `NOW` is ever moved to the future, or a fake timer is introduced, they would silently test the deferred branch instead. Pass `now: AFTER`-style explicit dates. The spec lists this as remaining work for the cancel test, and it applies to the delete tests as well.
```
