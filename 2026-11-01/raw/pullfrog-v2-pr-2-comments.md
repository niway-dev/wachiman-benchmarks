## apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:943 by pullfrog[bot]

This can close the gap too early if the camera is toggled off → on → off → on quickly. The first `turnWebcamOn` (A) is superseded by the second off, and the engine returns `"ok"` for a superseded call. But `webcamOn` is already `true` again from the second on (B, still queued), so `gaps.close()` runs when A resolves. B's camera hasn't sent a frame yet at that point. The held frame then shows in the editor and export for B's whole warm-up, which can be up to about 6 s. If B fails to reopen, it shows until the file ends.

<details><summary>Technical details</summary>


````markdown
# Superseded reopen closes the camera-off gap before frames are back

## Affected sites
- apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:939-944 — the `queue` callback treats any `"ok"` as "frames are back" whenever `webcamOn` is true, even when a later off/on pair superseded this request
- apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:790-792, 810 — a superseded `turnWebcamOn` returns `"ok"`, the same result as a real reopen

## Sequence
off(t1) → on(t2, A queued) → off(t3: `turnWebcamOff` bumps `cameraRequest`; `gaps.open` is a no-op because the t1 gap is still open) → on(t4: `webcamOn = true`, B queued after A) → A resolves `"ok"` (superseded) → `webcamOn` is true → `gaps.close(tA)`. B then opens the camera, and its own `gaps.close` is a no-op.

## Required outcome
- A gap closes only when the request that actually fed the relay delivers its first frame (or when the file ends), never when a superseded request resolves.

## Suggested approach
Keep a toggle generation in `forwardLiveSettings` that is bumped on every camera off and on. Capture it when the on is queued, and call `gaps.close()` only if it is unchanged after `await handle.turnWebcamOn()`. Another option: have the engine return a distinct result for a superseded call. A store test for off/on/off/on with A resolving before B would pin the fix down.
````

</details>

