# Wachiman review of branch `bench/pr-276` of pr-276 against origin/replay/pr-276/base (merge-base 400c80e), at f91b56d

All 19 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

12 finding(s): 1 to fix, 11 to consider

## Findings

### 🟠❓ **Fix · question: Deferred cancel and delete hold quota until a job nothing schedules runs (confidence high)**

`packages/application/src/cloud/cancel-upload.ts:36`

With this change a user-initiated cancel inside the ticket window returns `{ released: false }` and leaves the revision `reserved` (cancel-upload.ts:36-38). The reserve path counts `reserved` revisions against `MAX_PENDING_UPLOADS_PER_ACCOUNT` (cloud-asset.repository.ts:142 `pending_uploads < maxPending`, classified as too-many-pending at :202). The only code that releases them is `sweepExpiredReservations`, and nothing calls it: no caller under apps/server-hono, and apps/server-hono/src/index.ts:43 exports only the Hono app with no `scheduled` handler. Merged alone, three cancels inside the window block every further cloud upload for that account with no way out in the API. `deleteCloudCopy` has the same dependency for bytes: a delete inside the window returns `{ deleted: true }` while the revision stays `deleting` and keeps counting as used (delete-cloud-copy.ts:29-31; cloud-asset.repository.ts:366-368 'no counter change'; :500-502 reconcile counts `deleting`). The spec's open question 2 says the branch is 'safe to merge first (the rows simply wait)'. That is not what the code does: the rows wait indefinitely and the pending cap stays full. Main already leaves abandoned reservations to the same unscheduled sweep, but a user's explicit cancel did release immediately on main, so this is a new trigger. Please confirm that 323 will not ship without 328, or state the permanent lock in the spec's rollout section.

### 🟡📝 **Consider · docs: 'Rare in practice' is wrong: ready revisions are deferred for about 3 h 05 min after issue (confidence high)**

`apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:171`

The spec says a ready revision 'only has an open window if it was confirmed within 5 minutes of its last ticket, so this branch is rare in practice'. The predicate is `ticketExpiresAt + RESERVATION_GRACE_SECONDS <= now` (ticket-window.ts:9-11), and `ticketExpiresAt` is set at issue (create-upload-intent.ts:98) and extended only by a resume. `markReady` changes only status, verified_at and updated_at (cloud-asset.repository.ts:296-300), so the confirm time has no effect on the window. Any delete of an asset whose last ticket was issued less than about 3 h 05 min earlier is deferred. A user who uploads a clip and deletes it within the hour hits this path every time, so the open-question-2 ship-order risk is larger than the paragraph suggests.

### 🟡📝 **Consider · docs: Out-of-scope note says no desktop client calls the assets API; kaipu-record does (confidence high)**

`apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:72`

'A desktop cloud client (none exists; `apps/kaipu-record` makes no call to the assets API)' is false. apps/kaipu-record/src/main/cloud/catalog-client.ts:47-49 calls `GET /api/v1/assets` with `limit` and `cursor`, and follows `nextCursor` until it is null (:89). The cursor validation in this PR does reach that client. It is safe today because the client only sends server-issued cursors and `if (cursor)` (:49) never sends an empty one, but the spec should say so and the note should be corrected.

### 🟡📝 **Consider · docs: Acceptance criterion 1 is false for account purge, which deletes without the window check (confidence high)**

`apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:350`

Acceptance criterion 1 says 'No code path releases bytes or deletes an object while `ticketWindowClosed` is false.' `purgeAccountObjects` lists every key under the account's prefixes and deletes each one with no window check (packages/application/src/cloud/purge-account-objects.ts:21-30). Its own comment says the database rows are already gone by cascade (purge-account-objects.ts:6-7), so a PUT still valid under a deleted account's prefix would land an object that no revision or account row covers. The spec's orphan sweep looks accounts up through `listAccountsTouchedSince` on the storage-account table (cloud-asset.repository.ts:544-551), which would then not return that account (this depends on that table cascading as well, which I did not confirm in the schema). Either narrow the criterion and state the purge gap in the spec's scope, or have the purge honour the window.

### 🟡📝 **Consider · docs: Decision 2 claims one predicate for the sweep; the sweep has its own boundary (confidence high)**

`apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:34`

Decision 2 says `ticketWindowClosed` is 'the single definition' used by cancel, delete, the retry job 'and (indirectly) the sweep'. The sweep does not call it: it computes `before = now - RESERVATION_GRACE_SECONDS` itself (sweep-expired-reservations.ts:22) and lists with a strict `<` (cloud-asset.repository.ts:519-531). The rationale in the same row, 'two independent definitions would drift', describes the situation the spec then creates. Say that the sweep keeps its own boundary and that the two agree at the millisecond level, which the spec covers in its remaining tests.

### 🟡📝 **Consider · docs: A v2 key has two segments after the account prefix, not three (confidence high)**

`apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:227`

The spec says 'a v2 key has three path segments after the prefix'. The key is `<prefix>/<userId>/<assetId>/<revisionId>.<ext>` (cloud-asset.ts:151-160), and the account prefix is `videos/<userId>/` (accountPrefixes, cloud-asset.ts:173-175). What follows that prefix is `<assetId>/<revisionId>.<ext>`, two segments. The legacy shape `videos/<userId>/<id>.<ext>` has one. An implementer who counts the spec's way would misclassify every v2 key.

### 🟡📝 **Consider · docs: The cloud data model invariant is quoted without its exception (confidence high)**

`apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:24`

The spec quotes the data model as saying 'a reservation must not expire while a valid ticket can still write'. The source (apps/documentation/src/content/docs/specs/2026-09-09-cloud-data-model.md:98) continues 'unless a strategy accounts for that risk'. The omitted clause is the one that lets the deferral design satisfy the invariant, so the quote makes the requirement look stricter than it is. Quote the sentence in full and say which strategy is used.

### 🟡🧪 **Consider · tests: Cancel and delete tests read the wall clock; the fixture is 2026-09-10 (confidence high)**

`packages/application/src/cloud/cloud.test.ts:579`

Every fixture uses `NOW = 2026-09-10`, but several tests call `cancelUpload` or `deleteCloudCopy` without `now`, so the use case reads the real clock. Examples: the cancel-then-intent test (cloud.test.ts:163-169), the pre-existing cancel test (:593-611), and the deleteCloudCopy tests (:831, :842, :849, :860). They pass only because today is more than 3 h 05 min after NOW, so the outcome depends on when the suite runs. The spec lists only the :579 case. Pass an explicit `now` to each, as the new window tests do.

### 🟡📝 **Consider · docs: Comment refers to a fake field this diff removed (confidence high)**

`packages/application/src/recordings/recordings.test.ts:63`

The comment at lines 62-64 says `Object.assign` lets 'a test flipping `storage.failNextUpload` afterwards' see the change. This diff removes `failNextUpload` from the fake, so the comment describes a field that no longer exists. Also, `createAndUpload` (line 104) now only seeds a ready row and marks the key as existing; nothing is uploaded. Rename it to match (e.g. `seedReadyRecording`) and drop the stale comment.

### 🟡🧹 **Consider · cleanup: buildStorageKey and extensionForContentType have no production caller after this change (confidence high)**

`packages/domain/src/schemas/recording.ts:55`

The only remaining callers of `buildStorageKey` and `extensionForContentType` are `recording.test.ts` and the barrel export in packages/domain/src/schemas/index.ts:6-7. Nothing writes legacy keys now, and the spec's orphan sweep only needs to recognise the legacy shape, not generate it. Either delete both with their tests or say in the spec why they stay (for example, to classify legacy keys).

### 🟡📝 **Consider · docs: The pending status doc describes a flow this change removes (confidence high)**

`packages/domain/src/schemas/recording.ts:7`

The comment on `recordingStatusSchema` says `pending` means 'a presigned upload URL was handed out, but the object has not been confirmed'. No code path can create a pending row now (the create use case and route are gone), and the status is kept only because old rows may hold it. Say that, so a reader does not look for the flow.

### 🟡🐛 **Consider · bug: Skipped in-window rows can hold the batch and delay settled ones (confidence medium)**

`packages/application/src/cloud/retry-pending-deletes.ts:21`

`listDeleting` orders by `updatedAt` and takes `limit` rows (cloud-asset.repository.ts:534-542). A row skipped by `continue` at line 21 is not updated, so it stays at the front of the next listing. If `limit` or more deleting rows are inside their window, every run spends its whole batch on them and rows past the window wait until those close, up to about 3 h 05 min. The effect is bounded, but it is easy to avoid by filtering the window in the query or listing a larger batch. The retry job has no caller yet, so this is a design point for NIW2-328.

## Summary

Reviewed the 19 files of this part at head f91b56d. The core deferral logic is sound. cancelUpload, deleteCloudCopy and retryPendingDeletes all check the same window, and the sweep's boundary agrees at the millisecond level. The removal of the legacy upload routes has no remaining callers in the repository. The cursor schema matches what the repository encodes, and the desktop catalog client only sends server-issued cursors. The main problems are in how the spec describes the change, and one ship-order risk the spec understates: a deferred cancel holds the account's pending slot, and a deferred delete holds bytes, until a sweep and a retry job that nothing schedules. Tests also read the wall clock in several places. I did not run anything. Two files in this part are deleted at head, so I reviewed them from their removed lines and from caller searches.

<details><summary>What the change connects to (6 closed, 1 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- POST /assets/{assetId}/revisions/{revisionId}/confirm after a deferred cancel (`packages/application/src/cloud/cancel-upload.ts:36`) — Should confirm after a deferred cancel be refused, or is resurrection intended? The spec names only the resume and confirm-after-resume cases in its test plan. Files that would answer it: `apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md`, `packages/application/src/cloud/confirm-upload.ts`.

**Closed, with the lines they rest on**
- POST /assets/{assetId}/revisions/{revisionId}/cancel: cancelUpload inside the ticket window (`packages/application/src/cloud/cancel-upload.ts:36`) — Response is { released: false } (cloud.router.ts:113). The cancel is not recorded. The revision keeps its pending slot and reserved bytes (cloud-asset.repository.ts:142, :202). If it fails: The revision stays reserved until sweepExpiredReservations runs, and nothing calls it (no caller under apps/server-hono; apps/server-hono/src/index.ts:43 exports only the app). Three such cancels mak… Evidence: `packages/application/src/cloud/cancel-upload.ts:35-38`, `apps/server-hono/src/modules/cloud/cloud.router.ts:104-114`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:142`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:202`, `packages/application/src/cloud/sweep-expired-reservations.ts:22-23`, `apps/server-hono/src/index.ts:43`.
- DELETE /assets/{assetId}/cloud: deleteCloudCopy inside the ticket window (`packages/application/src/cloud/delete-cloud-copy.ts:29`) — API returns { deleted: true } (cloud.router.ts:154). The asset is hidden and auto-upload excluded (cloud-asset.repository.ts:375-383). Usage is unchanged, because beginDelete makes no counter change (cloud-asset.repository.ts:366-368), and reconcile counts deleting as used (:500… If it fails: The object and its bytes stay counted until retryPendingDeletes runs. Nothing calls it (no caller under apps/server-hono). The window is about 3 h 05 min after the last ticket, not 5 minutes, because… Evidence: `packages/application/src/cloud/delete-cloud-copy.ts:27-31`, `apps/server-hono/src/modules/cloud/cloud.router.ts:143-154`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:366-386`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:500-502`, `packages/application/src/cloud/ticket-window.ts:9-11`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:296-300`.
- retryPendingDeletes: skip revisions whose ticket window is open (`packages/application/src/cloud/retry-pending-deletes.ts:21`) — None directly. The function returns finished and failed counts only. If it fails: listDeleting orders by updatedAt and skipped rows are not touched (cloud-asset.repository.ts:534-542), so a batch full of in-window rows delays later rows until those windows close. The job never run… Evidence: `packages/application/src/cloud/retry-pending-deletes.ts:16-21`, `packages/application/src/cloud/retry-pending-deletes.ts:26-28`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:534-542`.
- GET /assets?cursor=: contract validates the cursor with assetCursorSchema (`apps/server-hono/src/contract/cloud.contract.ts:47`) — Shipped clients: the desktop catalog only sends nextCursor values the server issued (catalog-client.ts:49, :89), which the schema accepts (cloud-asset.repository.ts:96-98 encodes what cloud-asset.ts:276-294 validates; cloud-asset.test.ts:160-161 covers the round trip). The catal… If it fails: Only a cursor the server itself issued that the schema rejected would break the desktop catalog, and the encoder and schema agree. The empty string now gets 400 where it used to list page one; no cal… Evidence: `apps/server-hono/src/contract/cloud.contract.ts:43-50`, `packages/domain/src/schemas/cloud-asset.ts:276-294`, `packages/infra-db/src/repositories/cloud-asset.repository.ts:96-108`, `apps/kaipu-record/src/main/cloud/catalog-client.ts:47-49`, `apps/kaipu-record/src/main/cloud/catalog-client.ts:55`, `apps/kaipu-record/src/main/cloud/catalog-client.ts:89`.
- POST /recordings and POST /recordings/{id}/confirm removed (legacy upload flow) (`apps/server-hono/src/modules/recording/recording.router.ts:15`) — None for shipped clients. The web hook uses only list, delete and downloadUrl (apps/web-hono/src/hooks/use-recordings.ts:10,20,34). kaipu-record has no call. If it fails: A stale client gets 404 rather than a silent write. The read and delete routes remain. Evidence: `apps/web-hono/src/hooks/use-recordings.ts:10`, `apps/web-hono/src/hooks/use-recordings.ts:20`, `apps/web-hono/src/hooks/use-recordings.ts:34`, `apps/server-hono/src/modules/recording/recording.router.ts:15-42`, `apps/server-hono/src/contract/recording.contract.ts:11-25`.
- POST /assets/upload-intents with the same intentKey after a deferred cancel (`packages/application/src/cloud/create-upload-intent.ts:147`) — The client gets a fresh ticket and can upload. The earlier cancel is undone, and the bytes stay counted. If it fails: No accounting error. The spec says this resume is intended (spec line 164-165). Evidence: `packages/application/src/cloud/create-upload-intent.ts:136-169`, `packages/application/src/cloud/create-upload-intent.ts:147-151`, `packages/application/src/cloud/create-upload-intent.ts:152-168`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 1 | 19 | 998 | 4 | reviewed | 42 | $0.39 |

Cost: $0.39, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 1 call(s), 42 turn(s), 6 min 36 s.

stop: complete

Claude Haiku 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of f91b56d below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. packages/application/src/cloud/cancel-upload.ts:36 · 🟠❓ Fix · question: Deferred cancel and delete hold quota until a job nothing schedules runs (confidence high)
   With this change a user-initiated cancel inside the ticket window returns `{ released: false }` and leaves the revision `reserved` (cancel-upload.ts:36-38). The reserve path counts `reserved` revisions against `MAX_PENDING_UPLOADS_PER_ACCOUNT` (cloud-asset.repository.ts:142 `pending_uploads < maxPending`, classified as too-many-pending at :202). The only code that releases them is `sweepExpiredReservations`, and nothing calls it: no caller under apps/server-hono, and apps/server-hono/src/index.ts:43 exports only the Hono app with no `scheduled` handler. Merged alone, three cancels inside the window block every further cloud upload for that account with no way out in the API. `deleteCloudCopy` has the same dependency for bytes: a delete inside the window returns `{ deleted: true }` while the revision stays `deleting` and keeps counting as used (delete-cloud-copy.ts:29-31; cloud-asset.repository.ts:366-368 'no counter change'; :500-502 reconcile counts `deleting`). The spec's open question 2 says the branch is 'safe to merge first (the rows simply wait)'. That is not what the code does: the rows wait indefinitely and the pending cap stays full. Main already leaves abandoned reservations to the same unscheduled sweep, but a user's explicit cancel did release immediately on main, so this is a new trigger. Please confirm that 323 will not ship without 328, or state the permanent lock in the spec's rollout section.
2. apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:171 · 🟡📝 Consider · docs: 'Rare in practice' is wrong: ready revisions are deferred for about 3 h 05 min after issue (confidence high)
   The spec says a ready revision 'only has an open window if it was confirmed within 5 minutes of its last ticket, so this branch is rare in practice'. The predicate is `ticketExpiresAt + RESERVATION_GRACE_SECONDS <= now` (ticket-window.ts:9-11), and `ticketExpiresAt` is set at issue (create-upload-intent.ts:98) and extended only by a resume. `markReady` changes only status, verified_at and updated_at (cloud-asset.repository.ts:296-300), so the confirm time has no effect on the window. Any delete of an asset whose last ticket was issued less than about 3 h 05 min earlier is deferred. A user who uploads a clip and deletes it within the hour hits this path every time, so the open-question-2 ship-order risk is larger than the paragraph suggests.
3. apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:72 · 🟡📝 Consider · docs: Out-of-scope note says no desktop client calls the assets API; kaipu-record does (confidence high)
   'A desktop cloud client (none exists; `apps/kaipu-record` makes no call to the assets API)' is false. apps/kaipu-record/src/main/cloud/catalog-client.ts:47-49 calls `GET /api/v1/assets` with `limit` and `cursor`, and follows `nextCursor` until it is null (:89). The cursor validation in this PR does reach that client. It is safe today because the client only sends server-issued cursors and `if (cursor)` (:49) never sends an empty one, but the spec should say so and the note should be corrected.
4. apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:350 · 🟡📝 Consider · docs: Acceptance criterion 1 is false for account purge, which deletes without the window check (confidence high)
   Acceptance criterion 1 says 'No code path releases bytes or deletes an object while `ticketWindowClosed` is false.' `purgeAccountObjects` lists every key under the account's prefixes and deletes each one with no window check (packages/application/src/cloud/purge-account-objects.ts:21-30). Its own comment says the database rows are already gone by cascade (purge-account-objects.ts:6-7), so a PUT still valid under a deleted account's prefix would land an object that no revision or account row covers. The spec's orphan sweep looks accounts up through `listAccountsTouchedSince` on the storage-account table (cloud-asset.repository.ts:544-551), which would then not return that account (this depends on that table cascading as well, which I did not confirm in the schema). Either narrow the criterion and state the purge gap in the spec's scope, or have the purge honour the window.
5. apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:34 · 🟡📝 Consider · docs: Decision 2 claims one predicate for the sweep; the sweep has its own boundary (confidence high)
   Decision 2 says `ticketWindowClosed` is 'the single definition' used by cancel, delete, the retry job 'and (indirectly) the sweep'. The sweep does not call it: it computes `before = now - RESERVATION_GRACE_SECONDS` itself (sweep-expired-reservations.ts:22) and lists with a strict `<` (cloud-asset.repository.ts:519-531). The rationale in the same row, 'two independent definitions would drift', describes the situation the spec then creates. Say that the sweep keeps its own boundary and that the two agree at the millisecond level, which the spec covers in its remaining tests.
6. apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:227 · 🟡📝 Consider · docs: A v2 key has two segments after the account prefix, not three (confidence high)
   The spec says 'a v2 key has three path segments after the prefix'. The key is `<prefix>/<userId>/<assetId>/<revisionId>.<ext>` (cloud-asset.ts:151-160), and the account prefix is `videos/<userId>/` (accountPrefixes, cloud-asset.ts:173-175). What follows that prefix is `<assetId>/<revisionId>.<ext>`, two segments. The legacy shape `videos/<userId>/<id>.<ext>` has one. An implementer who counts the spec's way would misclassify every v2 key.
7. apps/documentation/src/content/docs/specs/2026-10-12-api-upload-abuse.md:24 · 🟡📝 Consider · docs: The cloud data model invariant is quoted without its exception (confidence high)
   The spec quotes the data model as saying 'a reservation must not expire while a valid ticket can still write'. The source (apps/documentation/src/content/docs/specs/2026-09-09-cloud-data-model.md:98) continues 'unless a strategy accounts for that risk'. The omitted clause is the one that lets the deferral design satisfy the invariant, so the quote makes the requirement look stricter than it is. Quote the sentence in full and say which strategy is used.
8. packages/application/src/cloud/cloud.test.ts:579 · 🟡🧪 Consider · tests: Cancel and delete tests read the wall clock; the fixture is 2026-09-10 (confidence high)
   Every fixture uses `NOW = 2026-09-10`, but several tests call `cancelUpload` or `deleteCloudCopy` without `now`, so the use case reads the real clock. Examples: the cancel-then-intent test (cloud.test.ts:163-169), the pre-existing cancel test (:593-611), and the deleteCloudCopy tests (:831, :842, :849, :860). They pass only because today is more than 3 h 05 min after NOW, so the outcome depends on when the suite runs. The spec lists only the :579 case. Pass an explicit `now` to each, as the new window tests do.
9. packages/application/src/recordings/recordings.test.ts:63 · 🟡📝 Consider · docs: Comment refers to a fake field this diff removed (confidence high)
   The comment at lines 62-64 says `Object.assign` lets 'a test flipping `storage.failNextUpload` afterwards' see the change. This diff removes `failNextUpload` from the fake, so the comment describes a field that no longer exists. Also, `createAndUpload` (line 104) now only seeds a ready row and marks the key as existing; nothing is uploaded. Rename it to match (e.g. `seedReadyRecording`) and drop the stale comment.
10. packages/domain/src/schemas/recording.ts:55 · 🟡🧹 Consider · cleanup: buildStorageKey and extensionForContentType have no production caller after this change (confidence high)
   The only remaining callers of `buildStorageKey` and `extensionForContentType` are `recording.test.ts` and the barrel export in packages/domain/src/schemas/index.ts:6-7. Nothing writes legacy keys now, and the spec's orphan sweep only needs to recognise the legacy shape, not generate it. Either delete both with their tests or say in the spec why they stay (for example, to classify legacy keys).
11. packages/domain/src/schemas/recording.ts:7 · 🟡📝 Consider · docs: The pending status doc describes a flow this change removes (confidence high)
   The comment on `recordingStatusSchema` says `pending` means 'a presigned upload URL was handed out, but the object has not been confirmed'. No code path can create a pending row now (the create use case and route are gone), and the status is kept only because old rows may hold it. Say that, so a reader does not look for the flow.
12. packages/application/src/cloud/retry-pending-deletes.ts:21 · 🟡🐛 Consider · bug: Skipped in-window rows can hold the batch and delay settled ones (confidence medium)
   `listDeleting` orders by `updatedAt` and takes `limit` rows (cloud-asset.repository.ts:534-542). A row skipped by `continue` at line 21 is not updated, so it stays at the front of the next listing. If `limit` or more deleting rows are inside their window, every run spends its whole batch on them and rows past the window wait until those close, up to about 3 h 05 min. The effect is bounded, but it is easy to avoid by filtering the window in the query or listing a larger batch. The retry job has no caller yet, so this is a design point for NIW2-328.
```
