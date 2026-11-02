=== COMMENT 4437322403 apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:155
Seeded gap segments get a random `crypto.randomUUID()` id, so seeding the same take twice gives two different scenes. `wholeFingerprint` (Share) and `editFingerprint` (an untouched editor scene that was never saved) both hash `scene.webcam` with these ids. For any take with gaps, the fingerprint is new on every mount, and "already exported → reuse" never finds the earlier export. That contradicts the PR note that the fingerprint covers seeded segments automatically.

<details><summary>Technical details</summary>

````markdown
# Seeded webcam gap segments make export fingerprints unstable

## Affected sites
- apps/kaipu-record/src/renderer/src/features/video-editor/webcam/webcam-model.ts:155 — `id: crypto.randomUUID()` in `gapSegments`
- apps/kaipu-record/src/renderer/src/features/library/components/share-recording.tsx:127-130 — `initialScene(...)` in a `useMemo`, then `wholeFingerprint(scene.webcam)`; a new hash on every mount for a take with gaps
- apps/kaipu-record/src/renderer/src/features/video-editor/export/export-reuse.ts:63-85 — `stableStringify` includes segment `id`s

## Required outcome
- Seeding the same `WebcamTrackMeta` (same gaps, same duration) twice gives an identical `WebcamScene`, so `wholeFingerprint` / `editFingerprint` are stable across mounts.
- Add a test next to the existing `export-reuse.test.ts` "same webcam → same fingerprint" case, using a meta that has `gaps`.

## Suggested approach
- Derive the id from the gap, e.g. `` `gap-${segments.length}` `` or `` `gap-${gap.startMs}` ``. `validateWebcamSegment` accepts any string id, so a session round-trip still works.
````

</details>

=== COMMENT 4437322410 apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:943
This closes the gap too early when the camera goes on, off and on again while the first re-open is still pending. The off is not queued: it calls `turnWebcamOff()` straight away, which supersedes the request. The superseded `turnWebcamOn` then resolves `"ok"`, and by that time `webcamOn` is `true` again from the second on. So the gap closes when the cancelled camera finished opening, not when the second camera's first frame arrives. During that warm-up the editor shows the frozen frame from the start of the gap, and if the second re-open fails it shows it until the file ends.

The comment above the `queue` line ("an off that follows waits for this camera to open") also does not match the code, since off never goes through the queue.

<details><summary>Technical details</summary>

````markdown
# Gap closed by a superseded re-open

## Affected sites
- apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:938-944 — `if (webcamOn) gaps.close(...)` after a superseded `turnWebcamOn` that returned "ok"
- apps/kaipu-record/src/renderer/src/features/recording/recorder-engine.ts:787-793,810 — a superseded request returns "ok", which cannot be told apart from a real feed

## Sequence
off (gap opens) → on (turnWebcamOn#1 pending) → off (turnWebcamOff supersedes #1, gap stays open) → on (#2 queued behind #1, webcamOn = true) → #1 resolves "ok" → gap closes now → #2 opens the camera and feeds frames later.

## Required outcome
- A gap closes only when the request that actually fed a frame resolves (or when the file ends).

## Suggested approach
- Keep a local toggle generation in `forwardLiveSettings` and close only when the resolving call is the latest on request. Alternatively, let `turnWebcamOn` return a distinct "superseded" result that the store ignores.
- Fix the queue comment so it describes what actually happens.
````

</details>

