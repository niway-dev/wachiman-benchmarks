## apps/kaipu-record/src/main/index.ts:902 by pullfrog[bot]

`showMainWindow()` only calls `show()` and `focus()`. The card is a non-activating panel, so clicking a chip leaves Kaipu inactive, and the repo has already found that this is not enough: `recording-hub.test.ts:728` says *"Showing the window alone leaves it unfocused behind the other app"* and expects `app.focus({ steal: true })`. When the user is in another app (the case this window is for), step 5 of the test plan ("Kaipu comes to the front") will probably fail. Prepare or the editor would open behind the other app. `bringAppToFront()` in this file already does `showMainWindow()`, `applyDockPolicy()` and `app.focus({ steal: true })`.

```suggestion
    openInMain: (handOff) => {
      bringAppToFront();
      sendToRenderer(IPC_CHANNELS.recordingReadyOpen, handOff);
    },
```

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:49 by pullfrog[bot]

Nit: this doc comment still says the card stays until the user *"leaves the page"*. That is now true only of the in-app fallback, because the floating window outlives navigation. Line 47 also runs well past the wrap width of the lines around it.

```suggestion
 * "Your video is ready" (NIW2-584): the card shown right after a recording, floating on the
 * desktop in its own window (`RecordingReadyCard`), or on the recording page's status stack
 * when that window could not open. It asks where the video is going, with chips into
 * Prepare, and stays until the user picks something or closes it (the in-app card also
 * when the user leaves the page) — there is no timer, since the question
```

## apps/kaipu-record/src/renderer/src/features/status-cards/post-recording-card.tsx:49 by pullfrog[bot]

Correction: the suggestion above drops the last line, `is the point. Settings → Export quality turns it off.`. Please keep that line after it if you apply the suggestion.

<!-- PULLFROG_DIVIDER_DO_NOT_REMOVE_PLZ -->
<sup><a href="https://pullfrog.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pullfrog.com/logos/frog-white-full-18px.png"><img src="https://pullfrog.com/logos/frog-green-full-18px.png" width="9px" height="9px" style="vertical-align: middle; " alt="Pullfrog"></picture></a>&nbsp;&nbsp;｜ [View workflow run](https://github.com/niway-dev/kaipu-bench-pullfrog-v2/actions/runs/41362567509/job/125015871110) ｜ via [Pullfrog](https://pullfrog.com) ｜ Using `claude-opus-5-5` ｜ [𝕏](https://x.com/pullfrogai)</sup>

