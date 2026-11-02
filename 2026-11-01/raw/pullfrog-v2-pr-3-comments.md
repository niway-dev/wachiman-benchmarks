## packages/i18n/messages/en.json:1431 by pullfrog[bot]

`destinationTag` has no `archive` branch. Archive copies get their label from `other`, so any destination missing from this `select` will be tagged "Archive copy" on the poster. The email destination the description mentions (#467) would hit exactly that. The same applies to `es.json:1431`. Name `archive` explicitly and make `other` neutral (or have the TS side enforce that every `DestinationId` is covered), so a new destination can't quietly get the wrong label.

```suggestion
    "destinationTag": "{destination, select, youtube {For YouTube} vertical {For Reels} square {For LinkedIn} github {For GitHub} chat {For chat} archive {Archive copy} other {Copy}}",
```

## apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:202 by pullfrog[bot]

The button's `aria-label` ("Show the export's progress") replaces its visible text, so screen readers never hear "YouTube copy · 38%". The nested `role="progressbar"` doesn't make up for it, because ARIA treats a button's children as presentational and the progressbar gets flattened. Drop the `aria-label` so the visible text names the button (maybe move "Show the export's progress" to `title`), or put the percent into the label.

## apps/documentation/src/content/docs/backlog/ready-copy-in-library.md:78 by pullfrog[bot]

This validation step makes a GitHub copy and then a chat copy, then expects the cards "newest first, FOR GITHUB / FOR CHAT". Newest first means chat leads, and that is what the PR description's step 7 and the `shows one card per finished copy, newest first` test say. QA following this doc would flag correct behaviour as a bug.

```suggestion
7. Make a GitHub copy and a chat copy back to back, then open the Library: two cards, newest
   first, FOR CHAT / FOR GITHUB, Drag to Slack / Drag to GitHub. ✕ on one: its regular card returns.
```

