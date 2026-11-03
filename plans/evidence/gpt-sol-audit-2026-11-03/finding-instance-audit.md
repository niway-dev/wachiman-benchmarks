# Independent audit instance inventory

60 run outputs cross-checked against final stream-json structured_output; 67 findings. No study verdict used to derive classifications.

## 1. 478-392778f / base / group G
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspaces-context.tsx:168` (consider; tests)
No test checks that an unchanged relocate shows no toast

The new flag is asserted only at the start of its path, in `relocate.test.ts:158`. Nothing checks the two steps that make the fix visible to the user:
- `relocateFolder` copying `unchanged` into the IPC result (`index.ts:349`);
- `onRelocated` returning before `showToast`.

The Settings tests only check the case where the toast does appear (`workspaces-settings.test.tsx:262` and `:282`). If either step stopped passing the flag along, the "now points to the new folder" toast would come back and no test would fail.

Suggested test: in `workspaces-settings.test.tsx`, mock `relocate` to resolve `{ ok: true, workspace, unchanged: true }` and assert that `showToast` is not called.

Independent evidence: relocate.test.ts:158 asserts marker only; index.ts:349 and workspaces-context.tsx:168 forwarding/toast suppression have no test.

## 2. 478-392778f / base2 / group H
**VALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:634` (consider; bug)
An offline edit now keeps `pendingInit`, so a later adoption can silently replace the user's rename

An offline edit used to delete `pendingInit` in every case. It now keeps it and sets `pendingIdentity` alongside it. When the folder comes back with an identity whose id this Mac doesn't know, `availability` now takes the adoption branch (lines 718-726). `Object.assign(entry, entryFromIdentity(...))` overwrites `name`/`color`/`initials` with the folder's values. That silently discards the rename the user made offline, even though the `editSavedOffline` toast had told them it would reach the folder. The branch also leaves `pendingIdentity` set. Before this change, the same case ended as `unavailable: different`. That was worse in a different way, so the new behaviour is arguably better overall. Still, nothing tells the user their edit was dropped. If the registry's newer name should win here, as it does in the `pendingIdentity` branch at line 670, apply the pending name and color after adopting. Otherwise, clear `pendingIdentity` in the adoption `refresh` so the flag doesn't outlive its meaning. This is the same scenario the owner already noted as a follow-up (a moved drive plus an identity written by another Mac), so it is rare.

Independent evidence: registry.ts:634 preserves pendingInit after offline edit; :718-727 adoption overwrites name/color without preserving pendingIdentity values.

## 3. 478-64db30b / base / group A
**VALID** — `apps/kaipu-record/src/main/workspaces/relocate.ts:43` (consider; bug)
Picking the current folder now does nothing, but the user is still told it "now points to the new folder"

The early return gives back `{ ok: true, entry: current }`. `relocateFolder` passes that on as success (`index.ts:340-349`), and both callers then show `folderChanged` ("Done. {name} now points to the new folder.", `workspaces-context.tsx:167`, which the dialog reaches through `onRelocated`). This case is easy to hit, because the picker opens at `dirname(entry.path)` (`index.ts:331`). When that happens, the user is told the folder changed when it did not. One way to fix it: return a distinct marker (for example `unchanged: true`, or the `cancelled` reason, which needs no toast) so the renderer can skip the toast or say the folder is already in use.

Independent evidence: Same-path success reaches unconditional folderChanged toast; relocate.ts:43 and workspaces-context.tsx:167.

## 4. 478-64db30b / base2 / group B
**VALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:684` (fix; bug)
Deferred color upgrade writes a snapshot read before an await and can overwrite a concurrent rename

The `pendingColorUpgrade` branch writes `{ ...identity.identity, color: entry.color }`. Here `identity.identity` is the file read at line 657, before the `isDirectory` and `readIdentity` awaits. `availability` takes no lock, and `index.ts` probes from several places (`index.ts:114,126,136,214`), so a background probe can overlap an `edit`. Consider this order:

1. Probe A reads the old Default/rose file and suspends.
2. `edit(id, { name: "Studio" })` runs its own probe (line 591), writes `Studio` to `identity.json` (line 612), and its `update` clears `pendingColorUpgrade` (line 629).
3. A resumes and writes the stale snapshot: name "Default workspace", color kaipu.

The registry now says "Studio" with no pending flag. The next probe takes the "folder's file wins" branch (lines 693-707), so the registry goes back to "Default workspace". The rename is lost with no message to the user.

The `pendingIdentity` branch just above has a smaller version of this window, but it builds name and color from the live `entry`. This branch puts back the old name from the file.

Possible fixes:
- Just before the write, re-read the file and re-check `entry.pendingColorUpgrade`.
- Better, serialize per-id probes and edits behind one lock, the way `update` uses `UPDATE_LOCK`.

Independent evidence: registry.ts:657,681-685 writes an identity snapshot without a per-folder lock; update lock at :928 covers registry persistence only.

## 5. 479-413ee15 / base / group J
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:347` (consider; tests)
No test pins the new 'moving' lock on Change folder…

Moving `busy: busyNow` into `activeTransactionDeps()` is what makes `relocateRefusal` (`relocate.ts:24-25`) and `relocateActive` (`switch-transaction.ts:105-118`) refuse while a group move runs. But `relocate.test.ts` only types and sets `busy` as `"recording" | "exporting" | null` (lines 37, 54), and its lock tests (lines 107-113, 253-258) never use `"moving"`. Nothing would catch a regression back to the old wiring, where only `runSwitch` saw the move. Consider widening `setBusy` to `WorkspaceBusy` and adding a `"moving"` case, plus a `relocateRefusalMessage` case for `relocateMoving`.

Independent evidence: index.ts:347 newly shares busyNow; workspace-dialog.test.tsx:323-331 omits moving, as do relocate.test.ts busy cases. S-high overstates the absence of other refusal tests, but moving gap is real.

## 6. 479-413ee15 / base / group K
**VALID** — `apps/documentation/src/content/docs/backlog/several-workspaces.md:26` (consider; docs)
Change folder… is now also refused while a move runs; the docs list only recording and export

This line says Change folder… is refused "while a recording or export runs". The spec's `workspaces:relocate` row (`specs/2026-10-29-several-workspaces-design.md:1302`) says the same. With this change, `relocateRefusal` also returns `moving` during a group move (`index.ts:346-347`, `relocate.ts:24-25`), and the user sees `relocateMoving`. Consider adding "or a move" in both places. The Part 2 paragraph would also work.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 7. 479-413ee15 / base2 / group J
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:347` (consider; tests)
No test pins that "Change folder…" is refused with `moving` during a group move

This commit moves `busy: busyNow` into `activeTransactionDeps()`, so relocation now picks up the move lock as well. There are three places it applies: the check before the picker (`relocateFolder` → `relocateRefusal`, index.ts:483), the check after the picker (relocate.ts:33), and the late check inside `relocateActive` (switch-transaction.ts:115-118). `busyNow` returns `"moving"` while `moveRun` is set (index.ts:66-67).

The switch has a test for `moving` (switch-transaction.test.ts:73-74). The relocate tests only check `recording` (relocate.test.ts:170, 185). Nothing tests `relocateRefusalMessage`'s new `moving` → `relocateMoving` branch either. If someone later moves `busy` back into the switch-only deps, relocation would silently stop refusing during a move and no test would fail. Consider adding one `relocateWorkspace` case with `busy: () => "moving"`.

Independent evidence: index.ts:347 newly shares busyNow; workspace-dialog.test.tsx:323-331 omits moving, as do relocate.test.ts busy cases. S-high overstates the absence of other refusal tests, but moving gap is real.

## 8. 479-413ee15 / base2 / group K
**VALID** — `apps/documentation/src/content/docs/backlog/several-workspaces.md:26` (consider; docs)
Change folder refusal list leaves out "while a move runs"

The backlog banner says Change folder… is refused "while a recording or export runs". The spec's `workspaces:relocate` row (specs/2026-10-29-several-workspaces-design.md:1302) says the same. On this branch it is also refused while a group move runs (`WorkspaceRelocateRefusal` now includes `"moving"`, shared/types/workspaces.ts:157-158, via `busyNow`, index.ts:66-67). Since this PR adds that lock, consider mentioning it in the part 2 text, or in the relocate row.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 9. 483-0253fd7 / base / group R
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:755` (fix; bug)
Relocating the active workspace re-lists the Library before the new folder's provider is detected, and the list is not refreshed afterwards

For the active workspace, `relocateWorkspace` runs `relocateActive` (`relocate.ts:46-48`). Its `afterCommit` (`index.ts:524-530`) calls `host?.broadcastLibraryChanged()` inside the transaction, before line 755 detects the new folder. Until then, `syncStates.of` sees a path that changed since the last detection and falls back to the path rule (`sync-state.ts:26-30`). The path rule misses a Drive folder that only the xattr identifies, which is the case `detectSync` exists for (`synced-folder.ts:83-91`). So the windows re-list with `currentVault()` built with no eviction probe (`library/index.ts:71-74`). Evicted items get thumbnail URLs and no "In the cloud" state, and the `kaipu-media://` gate (`media-protocol.ts:126`) is off for requests made in that gap. Those requests open the files, which downloads them.

Once `refresh` finishes, only `broadcastState()` runs (line 759). The Library is never told to re-list, so those cards stay wrong until some unrelated library change. The PR's renderer-side move and drag guards read that list.

Fix: call `host?.broadcastLibraryChanged()` after line 755 when the relocated workspace is the active one. Alternatively, detect the chosen folder before the transaction commits.

Independent evidence: relocateActive switch-transaction.ts:136 commits/broadcasts before index.ts:755 refresh; sync-state.ts:28-29 falls back to path rule, missing xattr-only Drive. Recording staging and media gate can be wrong in gap.

## 10. 483-0253fd7 / base2 / group R
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:755` (consider; bug)
Active relocation commits and re-lists the Library before the new folder's sync state is detected

For the active workspace, `relocateWorkspace` goes through `relocateActive`. That calls `afterCommit` (`switch-transaction.ts:136`), which reopens the gate and sends `library:changed` (`index.ts:524-530`). The new `syncStates.refresh(current)` runs only after that, at line 755. Until it finishes, `syncStates.of(active)` has no cached result for the new path, so it falls back to the path rule (`sync-state.ts:26-30`). The path rule does not recognise a Drive folder that only the xattr identifies (`synced-folder.ts:83-91`). For up to about 4 s (the 2 s realpath bound plus the 2 s xattr bound), `activeEvictionProbe()` and `syncedStagingFor()` treat that folder as unsynced.

The Library list built from that commit's broadcast has no eviction info. Nothing lists it again afterwards: after the refresh, line 759 sends only `broadcastState()`, not `broadcastLibraryChanged()`. So evicted items keep a thumbnail URL and stay draggable and movable until something else re-lists the Library. That is the case decision 15 is meant to stop.

Two fixes:
- Detect the chosen folder before the transaction commits (refresh with the resolved `chosen` path before `relocateWorkspace`).
- Or call `host?.broadcastLibraryChanged()` after the refresh when the provider differs from what the path rule said.

For a non-active workspace the order is harmless, because nothing lists it in between.

Independent evidence: relocateActive switch-transaction.ts:136 commits/broadcasts before index.ts:755 refresh; sync-state.ts:28-29 falls back to path rule, missing xattr-only Drive. Recording staging and media gate can be wrong in gap.

## 11. 484-59f6d48 / base / group U
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile-dialog.tsx:216` (consider; bug)
Double- or triple-click to select a name still toggles the row once

The guard works for drag-select, because the text is already selected when the click fires. A double-click (select a word) or triple-click (select the whole name) sends a separate `click` for each press. The first click comes before anything is selected, so `getSelection()` is empty and the row toggles. Only the later clicks are skipped. Before this change a double-click toggled twice and the row ended where it started. Now it ends flipped, so copying a name by double- or triple-click still unticks the row as a side effect.

One option: ignore a click when `event.detail > 1`. That doesn't undo the first toggle, though. If you want to cover these cases, you could toggle on `mouseup` only when nothing is selected, or delay the toggle until the double-click window has passed. You may decide this is fine, since the row's dimmed state does show the change.

Independent evidence: reconcile-dialog.tsx:216-217 first click toggles before word selection on second press; second click then skips toggle. Low severity is proportionate.

## 12. 484-59f6d48 / base2 / group U
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile-dialog.tsx:216` (consider; bug)
Double-clicking a name to copy it still toggles the row once

The guard covers a drag-select, but not a double- or triple-click, which is the other common way to select a name. In Chromium the first click's `click` fires while nothing is selected yet, so line 217 toggles the row. The word only gets selected on the second mousedown, so only the second `click` is skipped. The net result is one toggle plus a selection, which is the same side effect the earlier thread described. Two possible fixes: on the row's `onMouseDown`, call `preventDefault()` when `event.detail > 1` (but that blocks word selection), or compare `event.detail` and undo the first toggle when `detail === 2`. If double-click copying isn't a goal, a comment saying so would be enough.

Independent evidence: reconcile-dialog.tsx:216-217 first click toggles before word selection on second press; second click then skips toggle. Low severity is proportionate.

## 13. 478-392778f / C-S-high / group G
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspaces-context.tsx:168` (consider; tests)
No test covers the new `unchanged` branches in main's result or the renderer toast

The flag is pinned at the `relocateWorkspace` level (`relocate.test.ts:158`). Nothing checks that `relocateFolder` in `index.ts:349` forwards it to the IPC result, or that `onRelocated` here stays silent when it is set. The dialog test (`workspace-dialog.test.tsx:283`) only covers the changed case. If either end drops the flag, picking the current folder shows "now points to the new folder" again and every test stays green. A small provider test with `{ ok: true, unchanged: true }` that asserts no toast would pin it.

Independent evidence: relocate.test.ts:158 asserts marker only; index.ts:349 and workspaces-context.tsx:168 forwarding/toast suppression have no test.

## 14. 478-392778f / H-high / group H
**VALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:724` (fix; bug)
An offline rename of a pending workspace is silently dropped when its folder later carries another id

The change at registry.ts:634 keeps `pendingInit` after an edit made while the folder is away, and registry.ts:637-638 sets `pendingIdentity` for that edit. Before this change, the edit cleared `pendingInit`.

Now take the case where the folder comes back with an identity.json whose id is not registered on this Mac (for example, written by another Mac that uses the same drive). `availability` reaches the adoption branch at registry.ts:718-727. There, `Object.assign(entry, entryFromIdentity(...))` at line 724 replaces `name` and `color` with the folder's values. It does not clear `pendingIdentity`, so the entry keeps the flag while now holding the folder's name. The offline rename the user made is gone. The edit had told the user it would reach the folder (workspaces-context.tsx:158-160). On the next probe, registry.ts:670-672 writes the folder's own name back over the file, so nothing shows the loss.

Before this change the same sequence ended differently: `pendingInit` was already cleared, so the adoption branch was skipped, the probe returned `different`, and the renamed name stayed in the registry.

Suggested fix for this failure: do not take the adoption branch when `entry.pendingIdentity` is set, which restores the earlier outcome. The other option is to keep the pending name and tell the user it was replaced. The adoption rule for pending entries without an offline edit is not changed by this. registry.test.ts:210 covers adoption without any edit, so it does not exercise this case. This is a different path from the deferred `relocate` refusal in the open thread on registry.ts:809.

Independent evidence: registry.ts:634 preserves pendingInit after offline edit; :718-727 adoption overwrites name/color without preserving pendingIdentity values.

## 15. 478-392778f / H-high / group G
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspaces-context.tsx:168` (consider; tests)
The silent path for an unchanged folder has no renderer test

`onRelocated` now returns early when `result.unchanged` is set (line 168). No test under `features/workspaces` checks this. `workspace-dialog.test.tsx` only mocks `onRelocated`, and the main-side test at relocate.test.ts:158 pins the flag but not the toast. If the early return were removed, every test would still pass and the "now points to the new folder" toast would come back for the Settings and dialog paths. Add a case to the context or dialog tests that resolves `relocate` with `{ ok: true, unchanged: true, workspace }` and asserts that no toast is shown.

Independent evidence: relocate.test.ts:158 asserts marker only; index.ts:349 and workspaces-context.tsx:168 forwarding/toast suppression have no test.

## 16. 478-392778f / H-high-2 / group H
**VALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:718` (fix; bug)
An offline rename of a never-initialized workspace is silently replaced when its folder returns with another identity

The edit at registry.ts:634 now keeps `pendingInit` for a workspace whose folder is away, and registry.ts:638 sets `pendingIdentity`, so the rename lives only in the registry. `availability` adopts a folder's identity whenever the entry still has `pendingInit` and the folder's id is not registered (registry.ts:718-727). The adoption runs `Object.assign(entry, entryFromIdentity(...))`, which overwrites `name` and `color` with the folder's values (registry.ts:724), and it clears only `pendingInit`. `pendingIdentity` stays set, so the user's offline rename is gone and nothing tells them: no toast, no `different` state. Before this change, edit deleted `pendingInit` unconditionally, so this adoption could not run after an offline edit; the folder showed as `different` and the rename survived.

Failure: rename a pendingInit workspace while its drive is away, then bring back a folder at that path whose identity.json carries an id this Mac does not know. The next probe (listState, or any availability call) renames the entry to the folder's name.

Fix for this path: refuse that adoption while the entry carries the user's pending edit, by adding `&& !entry.pendingIdentity` to the condition at line 718. The entry then reports `different` and keeps the edit, as it did before this change. The comment at 719 gives the adoption's reason (an identity that arrived while unreachable wins), and it does not mention edits, so this is the only path I am changing.

Independent evidence: registry.ts:634 preserves pendingInit after offline edit; :718-727 adoption overwrites name/color without preserving pendingIdentity values.

## 17. 478-392778f / H-high-2 / group G
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspaces-context.tsx:168` (consider; tests)
The toast suppression for an unchanged pick has no test

The early return at line 168 is the only renderer change in this pull request, and no test reaches it. Grepping the app finds no test that asserts `folderChanged` or the `unchanged` skip. The only assertion is the flag itself (`relocate.test.ts:158`), and the dialog test mocks `onRelocated` (`workspace-dialog.test.tsx:50` and `:283`), so it never sees the context. A regression that shows the toast again, or one that hides the toast for a real move, would pass every current test. Add a provider-level test: an `ok` result with `unchanged: true` shows no toast, and a plain `ok` result still shows `folderChanged`.

Independent evidence: relocate.test.ts:158 asserts marker only; index.ts:349 and workspaces-context.tsx:168 forwarding/toast suppression have no test.

## 18. 478-392778f / H-high-2 / group I
**INVALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:189` (consider; cleanup)
RelocateOutcome documents `unchanged`, but registry.relocate never sets it

The `unchanged` field is declared on the registry's `RelocateOutcome` (registry.ts:188-189), which reads as a registry result. Only the wrapper sets it, at relocate.ts:44. `registry.relocate` (registry.ts:866-882) returns a plain `{ ok: true, entry }` even for the same path, and it still runs an `update` that writes preferences (registry.ts:870-876). A reader of the registry type would expect the flag from `relocate` and not get it. Move the field to the wrapper's return type in relocate.ts, or note in the comment that only `relocateWorkspace` sets it.

Independent evidence: registry.ts:189 declares an optional positive marker, not a promise every successful registry.relocate sets it; wrapper relocate.ts:44 supplies it for its own no-op path.

## 19. 478-392778f / S-high / group G
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspaces-context.tsx:168` (consider; tests)
Nothing tests that `unchanged` reaches the renderer and suppresses the toast

The flag crosses three layers: `relocateWorkspace` sets it (pinned in `relocate.test.ts:158`), `relocateFolder` copies it into the IPC result (`index.ts:349`), and `onRelocated` skips the toast (`workspaces-context.tsx:168`). Only the first hop has a test. If the spread at `index.ts:349` were dropped, or the early return here removed, the "now points to the new folder" toast would come back for a no-op and every test would still pass. A small test in the workspaces context or dialog tests would cover it: resolve `relocate` with `{ ok: true, unchanged: true, workspace }` and assert no toast, then resolve it without the flag and assert the toast.

Independent evidence: relocate.test.ts:158 asserts marker only; index.ts:349 and workspaces-context.tsx:168 forwarding/toast suppression have no test.

## 20. 478-392778f / S-high-2 / group G
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspaces-context.tsx:168` (consider; tests)
The part that silences the toast has no test

`relocate.test.ts:158` pins the `unchanged` flag in main. Nothing covers the other two links: `index.ts:349` copying the flag into the IPC result, and `onRelocated` returning early at line 168 (the dialog tests only mock `onRelocated`). If either link were dropped, the "now points to the new folder" toast would come back and every test would still pass. A small test of `WorkspacesProvider`'s `changeFolder` with a relocate result carrying `unchanged: true` that asserts no toast would pin the user-visible behavior.

Independent evidence: relocate.test.ts:158 asserts marker only; index.ts:349 and workspaces-context.tsx:168 forwarding/toast suppression have no test.

## 21. 478-64db30b / C-S-high / group A
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspaces-context.tsx:167` (consider; bug)
Picking the folder the workspace already points at still toasts "now points to the new folder"

`relocateWorkspace` now returns early with the unchanged entry when the chosen path is the current one (`relocate.ts:43`). The result is still `{ ok: true }`, so `onRelocated` here and the dialog's `onRelocated(result)` (`workspace-dialog.tsx:145`) show `folderChanged`: "Done. {name} now points to the new folder." The picker opens at `dirname(entry.path)`, so picking the same folder is easy, and the user is told something changed when nothing did. Consider distinguishing the no-op, or wording the toast so it is true in both cases.

Independent evidence: Same-path success reaches unconditional folderChanged toast; relocate.ts:43 and workspaces-context.tsx:167.

## 22. 478-64db30b / C-S-high-2 / group C
**INVALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:629` (consider; bug)
An unrelated offline edit turns the deferred color upgrade into a write of the folder's color

`edit` deletes `pendingColorUpgrade` and sets `pendingIdentity` (lines 629-631) even when the user changed only the name. On reconnect, the `pendingIdentity` branch (lines 663-672) writes name, color and initials from the cache over the folder's file. The cached color is the app-supplied brand color, not one the user chose. So if another Mac recolored the folder while this one was away and the user then renames it here, that recolor is overwritten without a choice from anyone. The new test at `registry-create-edit.test.ts:206` pins the rename-wins case but not the color. Consider clearing `pendingColorUpgrade` only when the patch includes a color. When the patch has only a name, keep it, and have the pending-identity write skip the color unless `isOldDefault`.

Independent evidence: registry.ts:628 explicitly assigns identity ownership to an edit; :663-671 writes all cached fields. This is existing whole-identity offline-edit behavior, not a new per-field merge contract.

## 23. 478-64db30b / H-high / group B
**VALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:684` (fix; bug)
Deferred color upgrade rewrites the folder's identity from a read taken before the awaits

`availability` reads the folder's identity at line 657 (await), then at 681-684 writes `{ ...identity.identity, color: entry.color }`: the whole object from that earlier read, with no re-read and no per-workspace lock. `UPDATE_LOCK` (line 928) serializes only registry updates, not identity-file writes. `edit` probes (line 591), reads the file (596) and writes its name (612) with the same unlocked pattern. Overlap: a probe that read the old Default before `edit`'s write lands its write after it, so the folder's name reverts to "Default workspace" while `edit` has already set the registry name and cleared `pendingIdentity` (630). The next probe sees a different name and takes the folder's (700-708), so the rename is lost with no message. Probes run on every capture (index.ts:113-115), so the overlap is reachable. The same window exists if another Mac writes between the read at 657 and the write at 684. The pendingIdentity branch (663-671) has the same whole-object write. Fix: re-read the identity immediately before writing and write only if it is still the old Default in rose, or serialize identity-file writes per workspace path with `withLock`.

Independent evidence: registry.ts:657,681-685 writes an identity snapshot without a per-folder lock; update lock at :928 covers registry persistence only.

## 24. 478-64db30b / H-high / group A
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspaces-context.tsx:167` (consider; bug)
Picking the folder a workspace already has reports that it 'now points to the new folder'

`relocate.ts:42-43` now returns `{ ok: true }` for the folder the workspace already points at, so `relocateFolder` (index.ts:340-349) answers ok and `onRelocated` shows the toast `folderChanged` ("Done. {name} now points to the new folder.", en.json:2622). Nothing changed, so "new folder" is false. Consider a no-change message, or no toast, for this case.

Independent evidence: Same-path success reaches unconditional folderChanged toast; relocate.ts:43 and workspaces-context.tsx:167.

## 25. 478-64db30b / H-high / group D
**INVALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:848` (consider; question)
A pending workspace now accepts any folder that has Kaipu items and no identity.json

`checkRelocate` returns ok at 848 for any `pendingInit` entry when the picked folder has `.kaipu/` and no identity. The probe after the move (index.ts:342 → registry.ts:724-737) then writes identity.json there under the registered id. Before this change, that folder was refused as `has-items-no-identity` because no workspace could claim it. Now a pre-workspaces library, or another Mac's folder that was never given an identity, can be taken, and its items appear under this workspace. The PR body still lists "`.kaipu/` items but no identity: refused" as a rule, which is now true only for non-pending entries. Is adopting any such folder intended for pending workspaces? The new test (registry-relocate.test.ts:200-219) covers only the moved-folder case. Also: the second half of the open thread on this line (a folder whose identity belongs to another id, registry.ts:835-838) is still refused, so this is a question about the first half only.

Independent evidence: registry.ts:843-848 explicitly permits this pendingInit recovery case; no narrower provenance rule is established.

## 26. 478-64db30b / H-high-2 / group E
**VALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:821` (consider; docs)
checkRelocate doc says only identity-carrying folders qualify, which the new pendingInit branch contradicts

The doc comment above `checkRelocate` says "Only a folder whose `.kaipu/workspace/identity.json` carries this workspace's id qualifies." The new branch at registry.ts:843-848 accepts a folder with `.kaipu/` and no identity when `entry.pendingInit` is set, and the test at registry-relocate.test.ts:200-219 pins that behaviour. Update the comment to say a pending workspace may also take an identity-less folder that holds Kaipu items, which the next probe then stamps with its id.

Independent evidence: registry.ts:821 says only matching-identity folders qualify, contradicted by new :848 branch.

## 27. 478-64db30b / H-high-2 / group D
**INVALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:848` (consider; question)
A pending workspace now takes any identity-less folder with Kaipu items: is that intended for folders that belong to another library?

Before this change an identity-less folder with `.kaipu/` was refused as `has-items-no-identity` (registry.ts:848 else-branch). Now `entry.pendingInit ? { ok: true }` accepts it for any pending entry. The probe then writes this entry's id into that folder (registry.ts:724-735), so whatever items it holds appear under this workspace. The guard that was there before ("the items are not in it") is bypassed for any folder that happens to hold Kaipu items without an identity file, not only the folder the workspace used to live in. Is it intended to accept a folder that was never this workspace's, for example a copy or another library's folder? If so, a note in the comment is enough; if not, consider requiring the folder to have been this entry's own path or to be unregistered.

Independent evidence: registry.ts:843-848 explicitly permits this pendingInit recovery case; no narrower provenance rule is established.

## 28. 478-64db30b / H-high-2 / group B
**VALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:684` (fix; question)
Deferred color upgrade writes identity.json without a per-folder lock, so an overlapping edit can be overwritten and lost

The `pendingColorUpgrade` branch at registry.ts:681-690 reads identity.json in `availability` (line 657), then writes `{...identity, color}` (line 684) with no lock around the read-check-write. `edit` does the same thing: it probes (line 591), reads `previous` (line 596), and writes `next` (line 612). Only the registry `update`/`persist` calls are serialized (UPDATE_LOCK, LOCK). `availability` is called from many places (for example `requireCaptureWorkspace` at apps/kaipu-record/src/main/workspaces/index.ts:114), so a probe can start before an edit's write and land after it. If the probe's write lands last, identity.json keeps the old color while the registry keeps the edited one. The next probe then sees the stale folder value and adopts it (registry.ts:694-707), so the edit's color is dropped silently. The window is narrow (it needs a pending upgrade and an overlapping probe), so the confidence is low. The same shape already exists for the `pendingIdentity` branch (registry.ts:663-680). Is there a reason the folder write does not go through a per-entry lock?

Independent evidence: registry.ts:657,681-685 writes an identity snapshot without a per-folder lock; update lock at :928 covers registry persistence only.

## 29. 478-64db30b / S-high-2 / group F
**VALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:836` (consider; bug)
Change folder… still refuses a pendingInit workspace's moved folder when it holds another id's identity

The pendingInit fix at line 848 covers a moved folder with no identity. The earlier thread also named a second case, and it is still refused. A `pendingInit` entry has a minted id. Suppose its folder is remounted elsewhere and already holds an identity.json with a different id, for example one written by another Mac. `checkRelocate` returns `different` at lines 836-838. `availability` adopts that id at lines 711-721 (`entry.pendingInit && !this.get(identity.identity.id)`). So the user is told the folder holds a different workspace and cannot repoint it, although a probe would have accepted it. Applying the same adoption rule in `checkRelocate` (accept when `entry.pendingInit && !this.get(identity.identity.id)`) would close it. `relocate` would then need the probe to run afterwards so the id is adopted, which `relocateFolder` already does at `index.ts:342`.

Independent evidence: registry.ts:836-838 refuses foreign id; :711-721 would adopt unregistered foreign id. Existing related thread remains partly unhandled.

## 30. 478-64db30b / S-high-2 / group C
**INVALID** — `apps/kaipu-record/src/main/workspaces/registry.ts:629` (consider; bug)
An offline edit of only the name turns the cached upgrade color into a pendingIdentity write, overwriting another Mac's recolor

The `edit` update callback deletes `pendingColorUpgrade` and sets `pendingIdentity = true` (lines 629-631). When the folder is back, the `pendingIdentity` branch (lines 663-672) writes the cached name, color and initials over the folder's file without comparing. Take the migrated Default with a cached color of `kaipu` and a not-connected folder. The user renames it offline, which changes the name only. Meanwhile another Mac recolors that folder's file to `sky`. When the folder returns, its file is overwritten with `kaipu`, a color this user never chose (it came from the deferred upgrade). The other Mac's recolor is lost with no visible sign. The new test at `registry-create-edit.test.ts:206` pins this outcome for an unchanged folder, but nothing covers the case where the folder changed meanwhile. `pendingIdentity` already overwrites whole cached fields for any offline edit, so this follows the existing design. The upgrade makes it more likely, because the user did not set the color. One option is to drop `pendingColorUpgrade` only when the edit changes the color, and let the name-only edit keep the cached color behind the old-Default check.

Independent evidence: registry.ts:628 explicitly assigns identity ownership to an edit; :663-671 writes all cached fields. This is existing whole-identity offline-edit behavior, not a new per-field merge contract.

## 31. 479-413ee15 / C-S-high / group J
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspace-dialog.test.tsx:328` (consider; tests)
The new "moving" refusal has no test

The "explains each remaining refusal" table (lines 323-331) lists recording and exporting but not `moving`. The `relocateMoving` string and its `case "moving"` in `relocate-copy.ts:35` are therefore not exercised. The default `relocateFailed` branch and `unknown` have no test either. `relocate.test.ts` also has no `busy: () => "moving"` case for `relocateRefusal` (lines 247-260), so nothing pins that the move lock refuses a relocate. Add `[{ ok: false, reason: "moving" }, /Wait for the move/]` to the table and a `moving` case to the `relocateRefusal` tests.

Independent evidence: index.ts:347 newly shares busyNow; workspace-dialog.test.tsx:323-331 omits moving, as do relocate.test.ts busy cases. S-high overstates the absence of other refusal tests, but moving gap is real.

## 32. 479-413ee15 / C-S-high / group K
**VALID** — `apps/documentation/src/content/docs/backlog/several-workspaces.md:26` (consider; docs)
Docs say Change folder… is refused only while a recording or export runs

With this PR, `busyNow()` (`main/workspaces/index.ts:66-67`) also returns `"moving"` while a group move runs. `activeTransactionDeps` passes it as `busy`, and `relocateRefusal` (`relocate.ts:24-25`) returns it as the reason. A relocate is now refused during a move as well. This paragraph, and the `workspaces:relocate` row in the spec (line 1302, "while a recording or export runs"), still list only the first two. Add the move so the docs match the new `relocateMoving` message.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 33. 479-413ee15 / C-S-high-2 / group J
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspace-dialog.test.tsx:328` (consider; tests)
The new "moving" refusal has no test

`relocate-copy.ts:35-36` adds a `moving` branch (`relocateMoving`), and the `explains each remaining refusal` table lists `recording` and `exporting` but not `moving`. Add `[{ ok: false, reason: "moving" }, /Wait for the move/]` so the new string and the switch case are covered. The `default` branch (`relocateFailed`) has no test either.

Independent evidence: index.ts:347 newly shares busyNow; workspace-dialog.test.tsx:323-331 omits moving, as do relocate.test.ts busy cases. S-high overstates the absence of other refusal tests, but moving gap is real.

## 34. 479-413ee15 / C-S-high-2 / group K
**VALID** — `apps/documentation/src/content/docs/specs/2026-10-29-several-workspaces-design.md:1302` (consider; docs)
The relocate row says "while a recording or export runs", but a group move now refuses it too

`busyNow()` returns `"moving"` while a group move runs (`main/workspaces/index.ts:66-67`). It is wired into the relocate path through `activeTransactionDeps` (`index.ts:343-347`, spread at `index.ts:480`) and checked in `relocateRefusal` (`relocate.ts:24-25`). So `workspaces:relocate` is also refused while a move runs, and the new `relocateMoving` string says so. The spec row, and the matching sentence in `backlog/several-workspaces.md:26`, list only a recording or an export.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 35. 479-413ee15 / H-high / group J
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspace-dialog.test.tsx:328` (consider; tests)
The "moving" refusal of Change folder… is never asserted

The "explains each remaining refusal" table covers recording and exporting but not `moving`, so the new `relocateMoving` text (packages/i18n/messages/en.json:2630, mapped in apps/kaipu-record/src/renderer/src/features/workspaces/relocate-copy.ts:35-36) is never rendered in a test. The main side has the same gap: apps/kaipu-record/src/main/workspaces/relocate.test.ts:54 types the harness's `busy` as `"recording" | "exporting" | null`, so `relocateRefusal` returning `moving` (apps/kaipu-record/src/main/workspaces/relocate.ts:24-25) is not exercised. Adding `[{ ok: false, reason: "moving" }, /Wait for the move to finish/]` here, and widening the harness type, would cover both.

Independent evidence: index.ts:347 newly shares busyNow; workspace-dialog.test.tsx:323-331 omits moving, as do relocate.test.ts busy cases. S-high overstates the absence of other refusal tests, but moving gap is real.

## 36. 479-413ee15 / H-high / group K
**VALID** — `apps/documentation/src/content/docs/specs/2026-10-29-several-workspaces-design.md:1302` (consider; docs)
workspaces:relocate row omits the move refusal and misstates when a folder is accepted

The row says the folder is "Accepted only when the folder's `identity.json` has the same id" and lists the refusals as recording or export only. The code also refuses while a group move runs (`moving`, apps/kaipu-record/src/shared/types/workspaces.ts:157-158, returned through apps/kaipu-record/src/main/workspaces/relocate.ts:24-25). It also accepts two cases without a matching identity: the folder the workspace already points at (apps/kaipu-record/src/main/workspaces/registry.ts:849) and a pending-init entry's folder that holds `.kaipu` items (registry.ts:855). Update the row to name the move refusal and those two exceptions.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 37. 479-413ee15 / H-high / group L
**INVALID** — `apps/documentation/src/content/docs/specs/2026-10-29-several-workspaces-design.md:1307` (consider; docs)
workspaces:move-items row ends mid-sentence

The row's description stops at "a group of single moves" and never says what a group of single moves is or does. Complete the sentence, for example "runs one single move after another, each under the same lock and gate as its own call"; the body at apps/documentation/src/content/docs/specs/2026-10-29-several-workspaces-design.md:1506 has the intended wording.

Independent evidence: Spec :1307 already ends this way in 413ee15 first parent; noun-phrase summary is not a broken contract or newly introduced truncation.

## 38. 479-413ee15 / H-high / group M
**INVALID** — `apps/documentation/src/content/docs/specs/2026-10-29-several-workspaces-design.md:1298` (consider; docs)
workspaces:switch row lists reasons the switch never returns

The row says the result is `{ reason: "busy" | "unavailable" | "cancelled" }`. `busy` is not a reason: `switchWorkspace` returns the busy value itself (apps/kaipu-record/src/main/workspaces/switch-transaction.ts:50-51, 105-106), which is `recording`, `exporting` or `moving`. The refusal union also has `unknown` and `read-only` (apps/kaipu-record/src/shared/types/workspaces.ts:28-41). This table was rewritten in this pull request, so the row should match the type.

Independent evidence: Spec :1298 already has identical busy/unavailable/cancelled content in first parent; delta only changes table padding on that row. Factual old mismatch, unrelated to new relocation lock.

## 39. 479-413ee15 / H-high / group K
**VALID** — `apps/documentation/src/content/docs/backlog/several-workspaces.md:26` (consider; docs)
Backlog paragraph does not mention the move refusal of Change folder…

The Part 1b paragraph says "Change folder…" is refused "while a recording or export runs". This pull request adds the `moving` refusal (apps/kaipu-record/src/shared/types/workspaces.ts:157-158), and the Part 2 paragraph below does not mention it either. Add "or a group move runs" here or in the Part 2 paragraph.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 40. 479-413ee15 / H-high / group N
**INVALID** — `apps/documentation/src/content/docs/backlog/several-workspaces.md:9` (consider; docs)
Status banner says nothing is implemented, which is no longer true

Line 9 says "The spec is written; nothing is implemented." Part 1b is marked 🟢 Ready to validate on line 18 and Part 2 is in progress on line 29, so the banner contradicts the rest of the page. This line predates this change, but the file is edited here, so it can be corrected in the same pass.

Independent evidence: Backlog :9 is stale but unchanged and predates this replay delta; reporting it because the file was touched does not establish push relevance.

## 41. 479-413ee15 / H-high / group O
**INVALID** — `apps/kaipu-record/src/shared/types/workspaces.ts:253` (consider; docs)
Whole-group refusal list omits "io"

The comment lists the whole-group refusals as "(busy, stale, maintenance)". `moveItems` now also refuses the whole group with `io` when it throws (apps/kaipu-record/src/main/workspaces/index.ts:215-217, mapped by apps/kaipu-record/src/main/workspaces/move-group.ts:62-66). Add `io` to the list, or say "for example".

Independent evidence: shared/types/workspaces.ts:253-254 parenthetical predates this delta and does not state an exhaustive union; failed/skipped behavior is correct. index.ts:217 maps other exceptions to io.

## 42. 479-413ee15 / H-high-2 / group K
**VALID** — `apps/documentation/src/content/docs/backlog/several-workspaces.md:26` (consider; docs)
Part 1b text says Change folder… is refused only while a recording or export runs

This PR makes a group move lock the switch and the relocate path too: `busy` now comes from `activeTransactionDeps()` (`apps/kaipu-record/src/main/workspaces/index.ts:346-347`), `relocateFolder` spreads that object (`index.ts:480`), and `relocate.ts:24-25` returns `{ reason: busy }`, which can be `"moving"` (`shared/types/workspaces.ts:25`). The renderer already has the `moving` copy (`relocate-copy.ts:35-36`, `en.json:2630`). The sentence at lines 25-27 still lists only "while a recording or export runs". Suggest adding "or a group move" there, matching the spec's relocate row.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 43. 479-413ee15 / H-high-2 / group K
**VALID** — `apps/documentation/src/content/docs/specs/2026-10-29-several-workspaces-design.md:1302` (consider; docs)
IPC table: workspaces:relocate refusals omit the group-move lock

The `workspaces:relocate` row ends with "and while a recording or export runs". The code also refuses with `reason: "moving"` during a group move (`apps/kaipu-record/src/main/workspaces/relocate.ts:24-25` via the shared `busy()` at `index.ts:346-347`, re-checked after the picker at `relocate.ts:33`). Add "or a group move" to the list so the channel contract matches `WorkspaceRelocateRefusal` (`shared/types/workspaces.ts:157-158`). I read this table and grepped the rest of the spec for the relocate wording; no other place says this.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 44. 479-413ee15 / H-high-2 / group J
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspace-dialog.test.tsx:321` (consider; tests)
The new "moving" refusal has no test

`explains each remaining refusal` lists every other `WorkspaceRelocateRefusal` reason, but not `moving`. The string `relocateMoving` appears only in `relocate-copy.ts:35-36` (grep over the feature folder found no other reference), so a wrong key or a dropped case would pass. Add `[{ ok: false, reason: "moving" }, /Wait for the move to finish/]` to the list. The main-side `relocate.test.ts:170-185` and `:247-271` also cover only recording and exporting, so the `moving` branch of `busy` is not tested there either (that file is outside this part).

Independent evidence: index.ts:347 newly shares busyNow; workspace-dialog.test.tsx:323-331 omits moving, as do relocate.test.ts busy cases. S-high overstates the absence of other refusal tests, but moving gap is real.

## 45. 479-413ee15 / S-high / group K
**VALID** — `apps/documentation/src/content/docs/specs/2026-10-29-several-workspaces-design.md:1302` (consider; docs)
`workspaces:relocate` row does not mention the new refusal while a group move runs

This PR makes "Change folder…" refuse with `moving` while a group move holds the lock. `busyNow()` returns `"moving"` (`main/workspaces/index.ts:66-67`) and is now wired into `activeTransactionDeps` (`index.ts:347`). `relocateRefusal` returns that busy value for any workspace (`relocate.ts:24-25`). The row still says "while a recording or export runs", and the backlog banner (`backlog/several-workspaces.md:26`) repeats it. Add "or a group move" to both so the docs match the code.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 46. 479-413ee15 / S-high / group J
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/relocate-copy.ts:36` (consider; tests)
The new `moving` branch of `relocateRefusalMessage` has no test

`relocateRefusalMessage` has no test for any reason, and the dialog test added here covers only `not-a-workspace`. Nothing checks that `moving` maps to `relocateMoving`. `relocate.test.ts` types its `busy` stub as `"recording" | "exporting"` (line 54), so the main-side refusal for a running move is not covered either. A small case for each, with `busy: () => "moving"`, would pin the new lock.

Independent evidence: index.ts:347 newly shares busyNow; workspace-dialog.test.tsx:323-331 omits moving, as do relocate.test.ts busy cases. S-high overstates the absence of other refusal tests, but moving gap is real.

## 47. 479-413ee15 / S-high-2 / group J
**VALID** — `apps/kaipu-record/src/renderer/src/features/workspaces/workspace-dialog.test.tsx:328` (consider; tests)
The refusal table does not cover the new "moving" reason

`relocate-copy.ts:35-36` adds `case "moving"` → `relocateMoving`, and `shared/types/workspaces.ts:158` adds the reason, but the "explains each remaining refusal" table (lines 323-331) lists `recording` and `exporting` and has no `moving` row. If the case or the key were dropped, it would fall into the `relocateFailed` default and no test would notice. Add `[{ ok: false, reason: "moving" }, /Wait for the move/]`.

Independent evidence: index.ts:347 newly shares busyNow; workspace-dialog.test.tsx:323-331 omits moving, as do relocate.test.ts busy cases. S-high overstates the absence of other refusal tests, but moving gap is real.

## 48. 479-413ee15 / S-high-2 / group K
**VALID** — `apps/documentation/src/content/docs/backlog/several-workspaces.md:26` (consider; docs)
Docs say Change folder… is refused only while a recording or export runs

This PR makes a group move refuse a relocate too (`main/workspaces/index.ts:347` passes `busy: busyNow`, which returns `"moving"` while `moveRun` is set; `relocate.ts:24-25` returns that reason). This banner and the `workspaces:relocate` row in the spec (2026-10-29-several-workspaces-design.md, "while a recording or export runs") still list only the other two. Add "or a move" to both.

Independent evidence: index.ts:347 passes busyNow, relocate.ts:24-25 refuses moving; backlog/several-workspaces.md:26 and specs/2026-10-29-several-workspaces-design.md:1302 omit it. Additional identity-only wording in H-high is stale but not newly introduced.

## 49. 482-ad0fa5c / H-high / group P
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:608` (consider; bug)
Change folder on the active workspace broadcasts without re-reading its folder file

`relocateFolder` runs the active workspace through `activeTransactionDeps()` (index.ts:585). Its `afterCommit` now calls `notifyOverridesChanged()` (index.ts:406), but nothing re-reads the folder's `settings.json` for the new path. The switch does that in `persistActive` (index.ts:425-427, `workspaceSettings?.refresh(target)`). The other refresh calls are on add, app start and capture start (index.ts:135, 313, 476), and ADR 0034 (`0034-per-workspace-setting-overrides.mdx:219-220`) names the same moments, not relocation.

So after "Change folder…" the cache still holds the old folder's read, and the notify rebroadcasts that stale snapshot. Main-side `settings:get` and `onSettingsChanged` listeners keep the old folder's overrides until something refreshes. The Settings UI appears to correct this itself: `settings-scope.tsx:91` calls `getScoped`, which calls `refresh` (workspace-settings.ts:248), and that re-read runs again when `workspaces` changes (settings-scope.tsx:99). Pending review also waits for that re-read. Suggest calling `workspaceSettings?.refresh(id)` on the relocate path before `afterCommit`, the way `persistActive` does for a switch, or recording in ADR 0034 that relocation is not a read moment. I have not run this.

Independent evidence: index.ts:406 newly notifies on relocate commit, but relocateFolder :580-619 never refreshes settings cache keyed by id (workspace-settings.ts:58,155).

## 50. 482-ad0fa5c / H-high-2 / group Q
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:427` (consider; bug)
Switch still broadcasts the target's settings before the commit

The diff moves `notifyOverridesChanged()` from `persistActive` into `afterCommit`, so the explicit broadcast now runs after `gate.commit`. But `persistActive` still calls `workspaceSettings?.refresh(target)` (index.ts:427) after `reg.setActive(target)`. `refresh` calls `deps.changed()`, which is `notifyOverridesChanged`, whenever the target's overrides differ from its cached value (workspace-settings.ts:159-160). That happens while the gate is still closed and the stamp still names the old workspace (switch-transaction.ts:70-80). So `settings:changed` with the new workspace's effective settings can still go out before the commit, and the comment at index.ts:405 ("reach every window ... ") only holds for the explicit call. If the ordering is what the move is for, `refresh` needs a way to skip its notification when it runs inside the switch. If the pre-commit broadcast is acceptable, the comment at index.ts:405 should not imply the broadcast waits for the commit. The exposure is a few milliseconds with no user action possible (the gate is closed), so this is a judgement call.

Independent evidence: index.ts:427 awaits refresh before gate commit; workspace-settings.ts:159-160 can invoke changed there, so moving only explicit notify does not eliminate precommit notifications.

## 51. 482-ad0fa5c / H-high-2 / group P
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:406` (consider; question)
Relocating the active folder notifies, but the folder's settings file is not re-read

`afterCommit` is also the commit callback of `relocateActive` (switch-transaction.ts:135-136, via relocate.ts:48). The new `notifyOverridesChanged()` therefore runs after "Change folder…" on the active workspace. `relocateFolder` (index.ts:580-619) never calls `workspaceSettings.refresh`, and the cache is keyed by workspace id (workspace-settings.ts:58, 145-162), so the notification recomputes the effective settings from the old folder's cached `settings.json`. The new folder's file is read only on the next settings scoped read, switch, or capture start. The ADR's list of read triggers (decisions/0034 line 166: switch, add, capture start) omits relocation. Is that intended? Relocation is accepted only for a folder with the same identity (spec line 1302), so the file is usually the same one, which limits the impact. Should relocation refresh the workspace settings before commit, as `persistActive` does for a switch?

Independent evidence: index.ts:406 newly notifies on relocate commit, but relocateFolder :580-619 never refreshes settings cache keyed by id (workspace-settings.ts:58,155).

## 52. 483-0253fd7 / C-S-high / group R
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:755` (consider; bug)
Relocating the active workspace re-lists the library before its sync state is detected

For the active workspace, `relocateWorkspace` runs `relocateActive` (`switch-transaction.ts:100-141`). It calls `deps.afterCommit` and reopens the gate before it returns. `afterCommit` (index.ts:524-530) runs `broadcastState()` and `host.broadcastLibraryChanged()`. Only after that does line 755 call `syncStates.refresh(current)`. Until then `SyncStates.of` (`sync-state.ts:26-30`) sees that the stored path differs and falls back to the path rule, which only knows `~/Library/CloudStorage/...`. A Drive or iCloud folder that only the xattr check detects therefore looks unsynced: `availabilityOf` takes the unbounded `reg.availability` branch (line 179), `activeEvictionProbe()` returns null (line 369), `activeScratch()` returns null (line 375), and the `syncedStagingFor` check (line 397) is false. `refresh` can add up to 2 s (`SYNC_DETECT_TIMEOUT_MS`), and the app uses stale state for that long. A library re-list or a capture start in that window can read evicted files or stage a take in `.kaipu/tmp/` of the synced folder. The other branch (a non-active workspace) is not affected, because nothing re-lists for it. Consider detecting the new folder before the commit: call `syncStates.refresh({ id, path: chosen })` right after the picker returns, or inside the `apply` callback of `relocateActive`. The window then starts with the right state.

Independent evidence: relocateActive switch-transaction.ts:136 commits/broadcasts before index.ts:755 refresh; sync-state.ts:28-29 falls back to path rule, missing xattr-only Drive. Recording staging and media gate can be wrong in gap.

## 53. 483-0253fd7 / C-S-high-2 / group R
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:755` (fix; bug)
Relocating the active workspace detects the provider only after the library has already re-listed

`syncStates.refresh(current)` runs after `relocateWorkspace` returns. For the active workspace, `relocateActive` (`switch-transaction.ts:100-141`) calls `afterCommit` inside the transaction. That calls `host?.broadcastLibraryChanged()` (`index.ts:529`), so every window starts re-listing the new folder, and the gate reopens, before the detection at line 755 has finished. The detection can take up to 2 s per step. Until `refresh` stores the result, `SyncStates.of` (`sync-state.ts:26-30`) answers from the path rule only, because the entry's path no longer matches the cached one. A Google Drive folder outside `~/Library/CloudStorage` is recognised only by its xattr, so for it `of()` returns null. During that window `activeEvictionProbe()` (line 369) returns null and the listing runs without the dataless probe. `activeScratch()` (line 373) and `syncedStagingFor()` (line 397) also return null. An evicted file in the new folder can then be listed and thumbnailed, and a take started in the gap stages in `.kaipu/tmp/` inside the synced folder. The `kaipu-media://` gate and the scratch folder are what decision 15 and NIW2-577 depend on. Nothing re-lists after the refresh: line 759 sends only `workspaces:changed`, not a library change. `addWorkspace` (line 578) and `createWorkspace` (line 630) both refresh before `runSwitch`. Relocate is the one path that refreshes afterwards. Fix: detect the chosen folder before the active transaction commits. For example, refresh inside the `apply` callback after `registry.relocate`, or refresh `{ id, path: chosen }` first and make sure the stored path is the one `of()` compares. Alternatively, call `host?.broadcastLibraryChanged()` after the refresh when the detected provider differs from the path-rule answer. The new line 755 only fixes the non-active case, where `registry.relocate` runs without a transaction.

Independent evidence: relocateActive switch-transaction.ts:136 commits/broadcasts before index.ts:755 refresh; sync-state.ts:28-29 falls back to path rule, missing xattr-only Drive. Recording staging and media gate can be wrong in gap.

## 54. 483-0253fd7 / H-high / group R
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:755` (fix; bug)
Relocated folder's sync provider is detected only after the gate has committed

`relocateFolder` calls `relocateWorkspace` (index.ts:751), which for the active workspace runs `relocateActive` (relocate.ts:48, switch-transaction.ts:121-136). That transaction calls `gate.commit(id)` and `afterCommit` (switch-transaction.ts:136), and releases `inFlight`, before this handler reaches `syncStates.refresh(current)` at line 755.

In that window `syncStates.of()` still answers from the path rule (sync-state.ts:26-29), and the new path is not in `known`. A Google Drive folder outside `~/Library/CloudStorage` is recognised only by its xattr (synced-folder.ts:83-91), so the path rule returns null and the folder is treated as plain. A capture started in the window goes through `create()` (recording-writer.ts:136-139, 181): `stagingFor` returns `.kaipu/tmp`, and `byRename` is false, so finalize uses `placeNew`, which hard-links (recording-writer.ts:113). That is the hard-link-into-Drive case decision 15 rules out. The window lasts as long as the xattr detection (up to 2 s, synced-folder.ts:22, 86-90). The sibling paths avoid this: `addWorkspace` (index.ts:577-578) and `createWorkspace` (index.ts:628-630) refresh before `runSwitch`. The `afterCommit` broadcast (index.ts:528) also runs before the refresh, so the switcher's first listing carries the stale null until the broadcast at line 759.

Suggested fix: detect the new folder before `gate.commit`, the way `addWorkspace` and `createWorkspace` do before `runSwitch`. For example, wrap `registry.relocate` in the deps that `relocateFolder` passes to `relocateWorkspace` (index.ts:728), so the relocated entry is refreshed inside `apply` before `relocateActive` commits. Keep the post-commit refresh only if the pre-commit one is absent for the non-active path.

Independent evidence: relocateActive switch-transaction.ts:136 commits/broadcasts before index.ts:755 refresh; sync-state.ts:28-29 falls back to path rule, missing xattr-only Drive. Recording staging and media gate can be wrong in gap.

## 55. 483-0253fd7 / H-high / group S
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:762` (consider; tests)
No main-process test covers the relocate result or the new sync refresh

The new `workspace` field on the `ok: true` result (line 762) and the new `syncStates.refresh` (line 755) are not exercised by any test. There is no `index.test.ts` under `main/workspaces/` (the test files there cover relocate.ts, registry and switch-transaction only). The field is also what the type requires: `WorkspaceRelocateResult` `ok: true` has `workspace: WorkspaceView` (shared/types/workspaces.ts:183-189). The renderer reads `result.workspace.name` in `onRelocated` (renderer/src/features/workspaces/workspaces-context.tsx:208-211). Before this diff the success result had no `workspace`, so this line fixes a real contract break, and nothing pins it. A test could assert that a successful relocate returns the relocated folder's `workspace.path`, `state` and `sync`. Adding it needs an electron mock, which this part does not have.

Independent evidence: New index.ts:755 refresh and :762 workspace result are absent from main-process integration tests; no index.test.ts or relocateFolder test exists.

## 56. 483-0253fd7 / H-high-2 / group R
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:755` (consider; bug)
Relocating the active workspace broadcasts before its new sync provider is detected

`relocateFolder` calls `relocateWorkspace` (line 751), which for the active workspace runs `relocateActive` (relocate.ts:48). That commits the gate and calls `afterCommit` (switch-transaction.ts:135-137), and `afterCommit` broadcasts `workspacesChanged` and `library:changed` (index.ts:524-530). Only after that returns does line 755 run `syncStates.refresh(current)`. So the re-list in those broadcasts sees the new folder through the path rule alone (`SyncStates.of`, sync-state.ts:26-29), not the detection.

The siblings do it the other way round. `addWorkspace` refreshes at index.ts:578 and `createWorkspace` at index.ts:630, both before `runSwitch` commits.

For a folder under `~/Library/CloudStorage` or iCloud the path rule is right and nothing is lost. For a Drive folder outside those roots, detected only by the xattr (synced-folder.ts:85-91), the path rule answers null until the detection finishes. That detection can take up to about 4 s, since `realpath` and the xattr check are each bounded at 2 s (synced-folder.ts:80, 86-90). In that gap the gate is open, so `currentVault()` builds a `LibraryVault` with a null eviction probe (library/index.ts:74), and `syncedStagingFor` returns null (index.ts:393-399), so a take started then is staged in `.kaipu/tmp/` inside the synced folder. That is the case decision 15 keeps out of synced folders. The switcher also shows no provider until the final broadcast at line 759 corrects it.

Fix: detect the picked path before the transaction, as `addWorkspace` does, e.g. `await syncStates.refresh({ id, path: chosen })` after the picker and before `relocateWorkspace`. `SyncStates.of` only trusts a detection whose path matches the entry's current path (sync-state.ts:28), so a refused relocation leaves nothing wrong behind.

Independent evidence: relocateActive switch-transaction.ts:136 commits/broadcasts before index.ts:755 refresh; sync-state.ts:28-29 falls back to path rule, missing xattr-only Drive. Recording staging and media gate can be wrong in gap.

## 57. 483-0253fd7 / S-high / group R
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:755` (fix; bug)
Relocating the active workspace detects the new folder's provider after the commit, so the first re-list treats an xattr-only Drive folder as plain

`addWorkspace` (line 578) and `createWorkspace` (line 630) call `syncStates.refresh` before `runSwitch`, so the switch commits with the provider already known. `relocateFolder` calls it only at line 755, after `relocateWorkspace` has returned. For the active workspace, `relocateActive` (`switch-transaction.ts:135-136`) has already run `afterCommit` by then, which sends `library:changed` and `workspaces:changed`. Between `registry.relocate` (`registry.ts:884`) and the refresh, `SyncStates.of` (`sync-state.ts:26-29`) has no entry for the new path. It falls back to `syncProviderOfPath`, which only knows the `~/Library/CloudStorage/…` and iCloud paths. A Google Drive folder recognised only by its `com.google.drivefs.item-id#S` xattr, outside `~/Library/CloudStorage`, answers null.

The renderer's re-list reads `activeEvictionProbe()` and `activeScratch()` (`library/index.ts:74`, `library/index.ts:420-421`), and `media-protocol.ts:126` reads `activeEvictionProbe()` too. All of them return null for that folder. Evicted items are listed as ordinary files and get thumbnail URLs. `kaipu-media://` opens them without the 409 gate, which downloads them. That is the hazard decision 15 forbids. After the refresh, only `broadcastState` runs (line 759). Nothing sends `library:changed` again, so the already-built list stays without eviction marks until something else re-lists. The detection at line 755 can take up to 2 s per step, which is the window in which the renderer's re-list lands.

The registry stores the picked path unchanged (`registry.ts:882`), so the provider can be detected before the transaction. Call `await syncStates.refresh({ id, path: chosen })` right before `relocateWorkspace` at line 751. `of()` matches on id and path, so the commit already sees the right provider. Keep the refresh at line 755 for the `unchanged` case and for a path the registry normalised. If the relocate is refused, the pre-detected entry does not match the registered path and `of()` ignores it.

Independent evidence: relocateActive switch-transaction.ts:136 commits/broadcasts before index.ts:755 refresh; sync-state.ts:28-29 falls back to path rule, missing xattr-only Drive. Recording staging and media gate can be wrong in gap.

## 58. 483-0253fd7 / S-high-2 / group R
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:755` (fix; bug)
Relocating the active workspace commits and re-lists before the new folder's sync state is detected

For the active workspace, `relocateWorkspace` runs `relocateActive`, which commits the gate and calls `afterCommit` (`switch-transaction.ts:135-137`). `afterCommit` calls `broadcastLibraryChanged()` and `broadcastState()` (`workspaces/index.ts:524-529`), so the windows re-list the library from the new folder. `syncStates.refresh(current)` only runs afterwards, at line 755. Until it finishes, `SyncStates.of` sees that the path changed and falls back to the path rule (`sync-state.ts:26-29`). That rule only recognises `~/Library/CloudStorage` and similar locations. A Google Drive or iCloud folder that only the xattr check recognises (the case the earlier threads on `index.ts:770` describe) therefore counts as not synced for the whole re-list:
- `activeEvictionProbe()` returns null (line 369), so the re-list gets no eviction probe.
- `activeScratch()` and `syncedStagingFor()` return null (lines 375, 397), so a recording started in that window stages in `.kaipu/tmp/` inside the synced folder.
- `refresh` can take up to the 2 s detection timeout, which widens the window.

The add and create paths avoid this: they call `syncStates.refresh` before `runSwitch` (lines 578 and 630).

Fix: detect before the transaction commits. For example, call `syncStates.refresh({ id, path: chosen })` right before `relocateWorkspace` at line 751. If `outcome.ok` is false, re-run `syncStates.refresh(entry)` for the old entry, because the map would otherwise hold the chosen path under this id. Alternatively, do the refresh inside the `apply` callback so it runs before `gate.commit`.

Independent evidence: relocateActive switch-transaction.ts:136 commits/broadcasts before index.ts:755 refresh; sync-state.ts:28-29 falls back to path rule, missing xattr-only Drive. Recording staging and media gate can be wrong in gap.

## 59. 483-0253fd7 / S-medium / group T
**VALID** — `apps/kaipu-record/src/main/workspaces/index.ts:756` (fix; bug)
Relocating out of an unverified synced folder leaves the id in `unverified`, so moves stay refused

`availabilityOf` adds an id to `unverified` when a synced folder's probe times out (line 191). It removes it only when a synced probe answers (line 182). Line 179 returns early for a non-synced workspace without clearing it. After `relocateFolder` points such a workspace at a plain folder, `syncStates.refresh` makes `of()` return null. `availabilityOf` then takes the early return at line 179, and the stale id stays in the set. `resolveMoveSide` (line 206) returns null for it, so every move from or to that workspace is refused as "not connected" until a restart or until it is synced again. Nothing tells the user why. Fix: call `unverified.delete(id)` on the early-return path at line 179, or in `relocateFolder` after the refresh. I did not read the move caller that turns the null into the refusal reason.

Independent evidence: index.ts:179 plain-folder return never clears unverified; :206 refuses moves when stale set membership survives relocation.

## 60. 484-59f6d48 / C-S-high / group W
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile.test.tsx:374` (consider; tests)
Spy restore is not guaranteed if the assertion fails

`selection.mockRestore()` runs after `expect(box).toBeChecked()` at line 373. If that assertion throws, the `getSelection` mock stays installed for the rest of the file, and later tests would fail for an unrelated reason. Restore it in `afterEach` or in a `try/finally`. The `afterEach` in this file's `vitest` import is already available.

Independent evidence: reconcile.test.tsx:373 assertion precedes :374 restore; local afterEach :65 and global renderer test setup only clean state/DOM, not spies.

## 61. 484-59f6d48 / H-high / group U
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile-dialog.tsx:216` (consider; bug)
A double-click on a row's name now toggles it once instead of not at all

Before this change, a double-click on a row's text ran the row's `onClick` twice, and each click called `setFixing([finding.path], !fixing)` (line 217), so the two toggles cancelled out. With the new guard, the first click's mousedown collapses the selection, so the first click toggles. The second mousedown selects the word, and the second click then sees `window.getSelection()` non-empty and returns at line 216. Net effect: a double-click now flips the row once, which the PR does not mention. The guard was meant for a drag that selects a name. If the one-toggle result is not wanted, a double-click on the text could be handled as a no-op, or the guard could be limited to a selection that started in this press. The author should decide which result they want and say so in the PR.

Independent evidence: reconcile-dialog.tsx:216-217 first click toggles before word selection on second press; second click then skips toggle. Low severity is proportionate.

## 62. 484-59f6d48 / H-high / group V
**UNCERTAIN** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile-dialog.tsx:216` (consider; bug)
Any existing text selection in the window suppresses a row toggle

The guard reads the document-wide selection, not one created by the current press. If a mousedown on the row does not collapse an earlier selection, a selection made elsewhere (the intro paragraph, the group description, or another row's name) makes the next click on this row do nothing. The row does not change and no message says why, so the user has to click again. I could not confirm from the repository whether Chromium/Electron collapses the selection on mousedown for a press on a row's padding or text; `reconcile.module.css:277-279` sets no `user-select` rule. If the selection is always collapsed on mousedown, this is not a problem. Question for the author: has a click on the row been checked after selecting text in another part of the dialog?

Independent evidence: reconcile-dialog.tsx:216 uses document selection, but reachability needs native Electron/Chromium evidence that clicking row text/padding preserves a previous unrelated selection.

## 63. 484-59f6d48 / H-high / group W
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile.test.tsx:369` (consider; tests)
Selection case sits in a test whose name does not cover it, and the spy is restored only on success

The new block (lines 368-374) is added to the test named "a click anywhere on a selectable row toggles it, not only on the 16 px box". Nothing in that name says a click with selected text must not toggle, so a reader looking for coverage of the copy case will not find it. Give the selection case its own `it(...)`. Also, `selection.mockRestore()` at line 374 runs only if the assertion before it passes. If `expect(box).toBeChecked()` at line 373 fails, the `getSelection` mock stays in place for the rest of the file, and `afterEach` (line 65) does not restore it. Use `try/finally` or `afterEach(() => vi.restoreAllMocks())`. The mock also returns a fake selection object, so the test checks only the early return. It does not check that a real drag-select produces a click on the `li`.

Independent evidence: reconcile.test.tsx:373 assertion precedes :374 restore; local afterEach :65 and global renderer test setup only clean state/DOM, not spies.

## 64. 484-59f6d48 / H-high-2 / group U
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile-dialog.tsx:216` (consider; question)
Double-click on a row now toggles once, not twice

The new guard at line 216 returns early whenever `window.getSelection()` has text. A double-click on a row's name selects a word on the second mousedown, so the second click event now sees a non-empty selection and does nothing. Before this change, the two clicks toggled the row twice and left it unchanged. The net result is now one toggle. This looks like an improvement, but it is a behaviour change nobody asked for. Is a single toggle on double-click the intended result? If so, a comment here would make that explicit. If not, a double-click guard would need its own check.

Independent evidence: reconcile-dialog.tsx:216-217 first click toggles before word selection on second press; second click then skips toggle. Low severity is proportionate.

## 65. 484-59f6d48 / H-high-2 / group W
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile.test.tsx:368` (consider; tests)
New selection assertions sit under a test whose name does not cover them, and the spy is not restored on failure

The test is named "a click anywhere on a selectable row toggles it, not only on the 16 px box", but lines 368-374 now also assert that a click with a selection does not toggle. The name no longer describes the whole test. Splitting the selection case into its own `it(...)` would fix that. Also, `selection.mockRestore()` at line 374 is skipped if an earlier `expect` fails, so the spy would leak into later tests in the file. Wrapping it in try/finally or calling `vi.restoreAllMocks()` in `afterEach` avoids that. The test stubs `getSelection` with a fake object, so it confirms the guard but not a real drag in a browser. That is a limit of jsdom, not a defect.

Independent evidence: reconcile.test.tsx:373 assertion precedes :374 restore; local afterEach :65 and global renderer test setup only clean state/DOM, not spies.

## 66. 484-59f6d48 / S-high-2 / group W
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile.test.tsx:374` (consider; tests)
Selection spy is restored only if the assertions before it pass

`selection.mockRestore()` runs after `expect(box).toBeChecked()`. If that assertion fails, the `getSelection` spy stays active for the later tests in the file. The file's only `afterEach` (line 65) resets the reconcile store and does not restore mocks. Use `try/finally`, or add `vi.restoreAllMocks()` to the `afterEach`, so one failure doesn't cascade into unrelated failures.

Independent evidence: reconcile.test.tsx:373 assertion precedes :374 restore; local afterEach :65 and global renderer test setup only clean state/DOM, not spies.

## 67. 484-59f6d48 / S-high-2 / group U
**VALID** — `apps/kaipu-record/src/renderer/src/features/library/reconcile/reconcile-dialog.tsx:216` (consider; bug)
Double-clicking a name to select it still toggles the row once

A double-click on a word fires click #1 before the browser selects the word, so the selection is empty and the row toggles. Click #2 sees the new selection and is skipped. The user selects the word to copy it and the row ends up toggled once. The drag-select case is fixed, but this one is not. If you want to close it, ignore clicks with `event.detail > 1`. That alone would not stop the first toggle, so you would need to decide whether that residual toggle is acceptable.

Independent evidence: reconcile-dialog.tsx:216-217 first click toggles before word selection on second press; second click then skips toggle. Low severity is proportionate.
