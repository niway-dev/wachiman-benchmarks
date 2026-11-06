# Wachiman review of branch `bench/pr-255` of pr-255 against origin/replay/pr-255/base (merge-base 400c80e), at 78e20a2

All 5 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

2 finding(s): 1 blocker(s), 1 to consider

## Findings

### 🔴❓ **Blocker · question: Does the cached policy go stale once Electron changes the policy natively? If so, Dock/Cmd+Tab re-assertion stops working (confidence medium)**

`apps/kaipu-record/src/main/infrastructure/settings-store.ts:82`

`appliedPolicy` only tracks calls made through this module. The callers re-assert the policy because something *outside* this module changes it: see `recording-hub.ts:155-156` and `281-283`, and `backlog/shortcuts.mdx:74-79` (Bug 1: "`applyDockPolicy()` is re-asserted after showing the camera bubble or the control bar, so opening a floating panel can't orphan the app"). Both panels call `setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true })` (`camera-bubble-window.ts:47`, `control-bar-window.ts:62`) without `skipTransformProcessType`. Electron documents that this call switches the process to a UIElement application by default (in effect an internal `dock.hide()`), and I believe that is what makes the app fall out of the Dock. Camera-off destroys the bubble (`recording-hub.ts:162`), so every camera-on builds a new window and runs that call again.

If that is right, then with `showInDock: true` the cache still says `"regular"` after the native switch, so `applyDockPolicy()` at `recording-hub.ts:157` does nothing and the app stays out of the Dock and Cmd+Tab. The same thing happens at recording stop (`recording-hub.ts:284`, after `forceRegularPolicy()` already cached `"regular"` and `bar.show()` ran the native transform) and in the `⌘⌃O` rescue (`index.ts:236`), which `shortcuts.mdx:79` calls "the guaranteed backstop". So the fix would trade the window flicker for the Bug 1 regression, with no error. The new tests mock `CameraBubbleWindow` and `ControlBarWindow`, so they cannot show this.

Can you confirm on a packaged build: with Show in Dock on, switch Camera ON and check whether the Dock icon and the Cmd+Tab entry are still there? If they disappear, possible fixes are passing `skipTransformProcessType: true` on both panels (check the full-screen-Space behaviour that option exists for), or keeping the cache but invalidating it wherever a panel is created.

### 🟡📝 **Consider · docs: "hypothesis 1 held" with no record of the experiment that confirmed it (confidence medium)**

`apps/documentation/src/content/docs/backlog/bug-main-window-hides-on-blur.md:100`

The heading says hypothesis 1 held, but the doc records no result from the experiment it describes (logging each policy call with its caller), and hypothesis 3 (a dev-only artefact, line 97-98) is still listed as not ruled out. The measured log (lines 47-52) shows a full `blur → hide → show` cycle before the camera is touched. The Fix section does not say which policy call caused that first cycle. Add the confirming log, or soften the heading until the packaged-build validation is done.

## Summary

The PR caches the last activation policy so applyDockPolicy and forceRegularPolicy return early when nothing changed. The callers' own comments and the Bug 1 reachability doc show that re-assertion exists to undo policy changes made outside this module. Both floating panels call setVisibleOnAllWorkspaces with visibleOnFullScreen, which Electron documents as transforming the process type. The cache would not see that change, so camera-on, recording stop and the ⌘⌃O rescue might stop putting the app back in the Dock and Cmd+Tab. The new tests mock the panel windows and cannot catch this. It should be checked on a packaged build before merging. Minor: the doc says hypothesis 1 held but records no confirming experiment.

<details><summary>What the change connects to (0 closed, 2 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Camera ON re-asserts the Dock policy through the now-cached setter (`apps/kaipu-record/src/main/recording/recording-hub.ts:157`) — Does setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true }) without skipTransformProcessType change the activation policy natively in the Electron version used here? Files that would answer it: `node_modules/electron/electron.d.ts`, `apps/kaipu-record/src/main/recording/control-bar-window.ts`.
- Recording start forces regular, then stop restores the preference (`apps/kaipu-record/src/main/recording/recording-hub.ts:267`) — Same open question as the camera-on entry, about Electron's native process transform. Files that would answer it: `apps/kaipu-record/src/main/recording/control-bar-window.ts`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 1 | 5 | 332 | 5 | reviewed | 13 | $0.61 |

Cost: $0.61, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 1 call(s), 13 turn(s), 1 min 30 s.

stop: complete

Claude Opus 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of 78e20a2 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/main/infrastructure/settings-store.ts:82 · 🔴❓ Blocker · question: Does the cached policy go stale once Electron changes the policy natively? If so, Dock/Cmd+Tab re-assertion stops working (confidence medium)
   `appliedPolicy` only tracks calls made through this module. The callers re-assert the policy because something *outside* this module changes it: see `recording-hub.ts:155-156` and `281-283`, and `backlog/shortcuts.mdx:74-79` (Bug 1: "`applyDockPolicy()` is re-asserted after showing the camera bubble or the control bar, so opening a floating panel can't orphan the app"). Both panels call `setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true })` (`camera-bubble-window.ts:47`, `control-bar-window.ts:62`) without `skipTransformProcessType`. Electron documents that this call switches the process to a UIElement application by default (in effect an internal `dock.hide()`), and I believe that is what makes the app fall out of the Dock. Camera-off destroys the bubble (`recording-hub.ts:162`), so every camera-on builds a new window and runs that call again.

   If that is right, then with `showInDock: true` the cache still says `"regular"` after the native switch, so `applyDockPolicy()` at `recording-hub.ts:157` does nothing and the app stays out of the Dock and Cmd+Tab. The same thing happens at recording stop (`recording-hub.ts:284`, after `forceRegularPolicy()` already cached `"regular"` and `bar.show()` ran the native transform) and in the `⌘⌃O` rescue (`index.ts:236`), which `shortcuts.mdx:79` calls "the guaranteed backstop". So the fix would trade the window flicker for the Bug 1 regression, with no error. The new tests mock `CameraBubbleWindow` and `ControlBarWindow`, so they cannot show this.

   Can you confirm on a packaged build: with Show in Dock on, switch Camera ON and check whether the Dock icon and the Cmd+Tab entry are still there? If they disappear, possible fixes are passing `skipTransformProcessType: true` on both panels (check the full-screen-Space behaviour that option exists for), or keeping the cache but invalidating it wherever a panel is created.
2. apps/documentation/src/content/docs/backlog/bug-main-window-hides-on-blur.md:100 · 🟡📝 Consider · docs: "hypothesis 1 held" with no record of the experiment that confirmed it (confidence medium)
   The heading says hypothesis 1 held, but the doc records no result from the experiment it describes (logging each policy call with its caller), and hypothesis 3 (a dev-only artefact, line 97-98) is still listed as not ruled out. The measured log (lines 47-52) shows a full `blur → hide → show` cycle before the camera is touched. The Fix section does not say which policy call caused that first cycle. Add the confirming log, or soften the heading until the packaged-build validation is done.
```
