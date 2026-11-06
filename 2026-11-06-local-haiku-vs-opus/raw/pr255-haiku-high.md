# Wachiman review of branch `bench/pr-255` of pr-255 against origin/replay/pr-255/base (merge-base 400c80e), at 78e20a2

All 5 files reviewed.

Profile: default — your own signed-in `claude`; its plugins are untested and could reach the review

4 finding(s): 1 to fix, 3 to consider

## Findings

### 🟠❓ **Fix · question: Re-assert after hide/show is now a no-op in the regular state; the docstring and the hub's comments say it is needed (confidence medium)**

`apps/kaipu-record/src/main/infrastructure/settings-store.ts:95`

`applyDockPolicy()` used to call `app.dock.show()` on every invocation. With the new `setActivationPolicy` cache (lines 78-86), it does nothing when the policy is already `regular`. With the default `showInDock: true` (apps/kaipu-record/src/shared/types/ipc.ts:214), that is the normal state during a recording.

The repo's own comments say this call is the re-assert that keeps the app in Dock/Cmd+Tab after windows are hidden or shown:
- settings-store.ts:88-93 says the function is "exported so the recording hub can re-assert it after hiding/showing the main window".
- recording-hub.ts:263-267: on recording start the main window is hidden, then `forceRegularPolicy()` runs so the app is not lost from the switcher. With `showInDock` on, that call is now skipped entirely.
- recording-hub.ts:281-284: on stop, "re-assert the policy ... so it's back in the switcher". `applyDockPolicy()` is now skipped here too.

The PR's diagnosis says `dock.show()` is what churns the windows. The comments say it is what restores switcher presence. Both cannot be fully right, and the PR does not show that the regular-to-regular re-assert was unnecessary. If the comments' premise holds, the app can drop out of Cmd+Tab after a recording or a rescue, with no error. The rescue path `bringAppToFront` (apps/kaipu-record/src/main/index.ts:234-238) has the same dependency on `applyDockPolicy()` re-issuing `dock.show()`. Please confirm on a packaged build that the app stays in Cmd+Tab after recording start and stop with `showInDock` on. If it does not, keep a `dock.show()`-only re-assert for the hide/show call sites. The docstring at lines 88-93 also needs updating, because "re-assert" is now a no-op in the case it describes.

### 🟡📝 **Consider · docs: Doc states the mechanism and the fix as established, but its own confirming experiment is not recorded (confidence high)**

`apps/documentation/src/content/docs/backlog/bug-main-window-hides-on-blur.md:20`

The doc says "Why that is the whole fix" and "exactly as measured below", and at line 100 "hypothesis 1 held". Nothing in the doc records the result of the "Next experiment" it describes (log each policy call with its caller, then reproduce). The measurements shown in the doc (lines 46-63) log only the camera path and the window events. They have no policy-call logs, so they do not show a policy call before each `blur → hide`. The doc's own finding 1 (line 68) says the first cycle happens before the camera is touched.

The regression tests mock AppKit, so they show that re-asserting an unchanged policy makes no AppKit call. They do not show that the blur → hide cycle is gone. The status "🟢 Ready to validate" is the right one; the body should say the fix is unverified on a real build, not that hypothesis 1 held. Either record the experiment's result or reword lines 20-26 and 100 as the expected effect to validate.

### 🟡📝 **Consider · docs: Code comments state the causal mechanism as fact, and one contradicts the doc's finding that the camera is not the cause (confidence high)**

`apps/kaipu-record/src/main/infrastructure/settings-store.ts:73`

The block comment at settings-store.ts:70-76 says AppKit "orders every window out and back in" during `dock.show()`, and that "the camera-on path re-asserts the policy, and each re-assertion was a blur → hide → show cycle." The backlog doc (bug-main-window-hides-on-blur.md:68-70) says the camera is not the cause and that the first cycle happens before the camera is touched. The same overstatement appears in recording-hub.test.ts:69-72 ("every re-assertion used to run `app.dock.show()`, which on macOS orders the main window out and back in") and settings-store.test.ts:73-75. Reword these as the diagnosed mechanism or cross-reference the doc, so the code does not state as established something the doc still lists as a hypothesis.

### 🟡🧪 **Consider · tests: Tests cover only the camera toggle; the start/stop re-assert paths that this change alters are untested (confidence high)**

`apps/kaipu-record/src/main/recording/recording-hub.test.ts:74`

The new tests cover one path: toggling the camera on (directly and over IPC). The change also alters the recording-start path (recording-hub.ts:262-268, `forceRegularPolicy()` after `hide()`) and the stop path (recording-hub.ts:275-287, `applyDockPolicy()` after `show()`). Those are where a skipped `dock.show()` would matter if the re-assert was needed (see the finding on settings-store.ts:95). No test runs `recordingStart` or `recordingStop` and checks the policy and dock calls, and none covers `bringAppToFront`. A test pinning the intended switcher behaviour for these paths would show whether the skipped call is harmless.

## Summary

The change correctly stops the no-op camera-on re-assert, and the tests check what they say: transitions still happen, re-asserts make no AppKit call, and non-darwin is untouched. The main risk is that the cache also suppresses the regular-to-regular `dock.show()` that the start, stop and rescue paths rely on (per their own comments), so the app may fall out of Cmd+Tab with no error. That needs a packaged-build check before merge. The doc and code comments also state the unverified mechanism as established. I did not build or run the code; the findings come from reading it.

<details><summary>What the change connects to (3 closed, 3 open)</summary>

Questions the reviewer answered about what this change does to the running product. The engine checked that the cited lines exist, not that the answers are true.

**Open: the reviewer could not close these**
- Recording start: getMainWindow()?.hide() then forceRegularPolicy() (`apps/kaipu-record/src/main/recording/recording-hub.ts:262-268`) — Does a regular-to-regular re-assert (app.dock.show() on an app already in regular) change whether the app stays in Dock/Cmd+Tab after the main window is hidden? The code comments say it does; the PR's diagnosis says dock.show() is the source of the window churn. Checking this ne… Files that would answer it: `apps/kaipu-record/src/main/recording/recording-hub.ts:263-268`, `apps/kaipu-record/src/main/infrastructure/settings-store.ts:88-93`, `apps/kaipu-record/src/main/index.ts:234-238`.
- Recording stop: applyStopWindowState runs main.show(), main.focus(), applyDockPolicy(), app.focus({ steal: true }) (`apps/kaipu-record/src/main/recording/recording-hub.ts:275-287`) — Same as the start path: does the skipped dock.show() on stop matter for Cmd+Tab presence once the main window is shown again? Files that would answer it: `apps/kaipu-record/src/main/recording/recording-hub.ts:281-285`, `apps/kaipu-record/src/main/infrastructure/settings-store.ts:88-93`.
- Rescue shortcut bringAppToFront(): showMainWindow(), applyDockPolicy(), app.focus({ steal: true }) (`apps/kaipu-record/src/main/index.ts:234-238`) — Does the rescue still recover a lost Dock/switcher state when the cached policy is regular and the OS state is not? The same check as the start/stop question is needed on a packaged build. Files that would answer it: `apps/kaipu-record/src/main/index.ts:234-238`, `apps/kaipu-record/src/main/infrastructure/settings-store.ts:84-85`.

**Closed, with the lines they rest on**
- Toggling Camera on (directly or via IPC) calls applyDockPolicy() after cameraBubble.show() (`apps/kaipu-record/src/main/recording/recording-hub.ts:152-158`) — No Dock or policy change when Camera is toggled and the policy is already correct. The main window is not hidden by this path (recording-hub.test.ts:96-112 asserts this with mocks). Evidence: `apps/kaipu-record/src/main/recording/recording-hub.ts:152-158`, `apps/kaipu-record/src/main/infrastructure/settings-store.ts:78-86`, `apps/kaipu-record/src/main/infrastructure/settings-store.ts:94-96`, `apps/kaipu-record/src/shared/types/ipc.ts:214`.
- Settings update over IPC: settings = mergeSettings(...); persist(); applySideEffects(); broadcast (`apps/kaipu-record/src/main/infrastructure/settings-store.ts:141-148`) — Changing an unrelated setting no longer touches the Dock. Changing showInDock still transitions (settings-store.test.ts:90-104 asserts this). Evidence: `apps/kaipu-record/src/main/infrastructure/settings-store.ts:125-130`, `apps/kaipu-record/src/main/infrastructure/settings-store.ts:141-148`, `apps/kaipu-record/src/main/infrastructure/settings-store.ts:82`.
- Module-level appliedPolicy cache in the main process (`apps/kaipu-record/src/main/infrastructure/settings-store.ts:78`) — None on its own. If it fails: The cache is process state. A renderer reload or window recreation does not reset it, and this is correct because the Dock policy belongs to the process. Only the AppKit-side changes noted in the res… Evidence: `apps/kaipu-record/src/main/infrastructure/settings-store.ts:15`, `apps/kaipu-record/src/main/infrastructure/settings-store.ts:78-86`.

</details>

## Coverage by batch

| Batch | Files | Lines | Highest risk | Status | Turns | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| Batch 1 of 1 | 5 | 332 | 5 | reviewed | 16 | $0.04 |

Cost: $0.04, an API-equivalent estimate (what these calls would cost at API prices), not a bill. 1 call(s), 16 turn(s), 2 min 35 s.

stop: complete

Claude Haiku 5.5 via Claude Code 2.1.311 · effort high · profile default · Wachiman 1.8.0

## Prompt for your agent

```text
Read the review of 78e20a2 below. For each finding, open the cited file at the cited line, decide whether it is valid against the current code, and fix the ones that are. Report the ones you reject with the reason. Run the repository's checks after the fixes.

1. apps/kaipu-record/src/main/infrastructure/settings-store.ts:95 · 🟠❓ Fix · question: Re-assert after hide/show is now a no-op in the regular state; the docstring and the hub's comments say it is needed (confidence medium)
   `applyDockPolicy()` used to call `app.dock.show()` on every invocation. With the new `setActivationPolicy` cache (lines 78-86), it does nothing when the policy is already `regular`. With the default `showInDock: true` (apps/kaipu-record/src/shared/types/ipc.ts:214), that is the normal state during a recording.

   The repo's own comments say this call is the re-assert that keeps the app in Dock/Cmd+Tab after windows are hidden or shown:
   - settings-store.ts:88-93 says the function is "exported so the recording hub can re-assert it after hiding/showing the main window".
   - recording-hub.ts:263-267: on recording start the main window is hidden, then `forceRegularPolicy()` runs so the app is not lost from the switcher. With `showInDock` on, that call is now skipped entirely.
   - recording-hub.ts:281-284: on stop, "re-assert the policy ... so it's back in the switcher". `applyDockPolicy()` is now skipped here too.

   The PR's diagnosis says `dock.show()` is what churns the windows. The comments say it is what restores switcher presence. Both cannot be fully right, and the PR does not show that the regular-to-regular re-assert was unnecessary. If the comments' premise holds, the app can drop out of Cmd+Tab after a recording or a rescue, with no error. The rescue path `bringAppToFront` (apps/kaipu-record/src/main/index.ts:234-238) has the same dependency on `applyDockPolicy()` re-issuing `dock.show()`. Please confirm on a packaged build that the app stays in Cmd+Tab after recording start and stop with `showInDock` on. If it does not, keep a `dock.show()`-only re-assert for the hide/show call sites. The docstring at lines 88-93 also needs updating, because "re-assert" is now a no-op in the case it describes.
2. apps/documentation/src/content/docs/backlog/bug-main-window-hides-on-blur.md:20 · 🟡📝 Consider · docs: Doc states the mechanism and the fix as established, but its own confirming experiment is not recorded (confidence high)
   The doc says "Why that is the whole fix" and "exactly as measured below", and at line 100 "hypothesis 1 held". Nothing in the doc records the result of the "Next experiment" it describes (log each policy call with its caller, then reproduce). The measurements shown in the doc (lines 46-63) log only the camera path and the window events. They have no policy-call logs, so they do not show a policy call before each `blur → hide`. The doc's own finding 1 (line 68) says the first cycle happens before the camera is touched.

   The regression tests mock AppKit, so they show that re-asserting an unchanged policy makes no AppKit call. They do not show that the blur → hide cycle is gone. The status "🟢 Ready to validate" is the right one; the body should say the fix is unverified on a real build, not that hypothesis 1 held. Either record the experiment's result or reword lines 20-26 and 100 as the expected effect to validate.
3. apps/kaipu-record/src/main/infrastructure/settings-store.ts:73 · 🟡📝 Consider · docs: Code comments state the causal mechanism as fact, and one contradicts the doc's finding that the camera is not the cause (confidence high)
   The block comment at settings-store.ts:70-76 says AppKit "orders every window out and back in" during `dock.show()`, and that "the camera-on path re-asserts the policy, and each re-assertion was a blur → hide → show cycle." The backlog doc (bug-main-window-hides-on-blur.md:68-70) says the camera is not the cause and that the first cycle happens before the camera is touched. The same overstatement appears in recording-hub.test.ts:69-72 ("every re-assertion used to run `app.dock.show()`, which on macOS orders the main window out and back in") and settings-store.test.ts:73-75. Reword these as the diagnosed mechanism or cross-reference the doc, so the code does not state as established something the doc still lists as a hypothesis.
4. apps/kaipu-record/src/main/recording/recording-hub.test.ts:74 · 🟡🧪 Consider · tests: Tests cover only the camera toggle; the start/stop re-assert paths that this change alters are untested (confidence high)
   The new tests cover one path: toggling the camera on (directly and over IPC). The change also alters the recording-start path (recording-hub.ts:262-268, `forceRegularPolicy()` after `hide()`) and the stop path (recording-hub.ts:275-287, `applyDockPolicy()` after `show()`). Those are where a skipped `dock.show()` would matter if the re-assert was needed (see the finding on settings-store.ts:95). No test runs `recordingStart` or `recordingStop` and checks the policy and dock calls, and none covers `bringAppToFront`. A test pinning the intended switcher behaviour for these paths would show whether the skipped call is harmless.
```
