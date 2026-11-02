=== COMMENT 4437315416 apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189
When a master's first copy finishes, `runningCopyOf` returns `null` as soon as the runner leaves `"exporting"`. But `exports` only grows after the async `refresh()` that the `readyId` effect starts. In that window `hasCopies` is false, so "Copies from this original" unmounts, "Where is it going?" comes back (unless dismissed) and "Export a copy" disappears. Then everything flips back once the list arrives. The old `showCopies = master || …` kept the panel mounted through this gap.

<details><summary>Technical details</summary>

````markdown
# Bottom section flickers between panels when the first copy completes

## Affected sites
- apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:189: `hasCopies` reads only `exports` and `running`
- apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:146-148: `refresh()` runs only after `runner.ready` is set, so `exports` lags the end of `running`
- apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:35: `runningCopyOf` returns null once `status !== "exporting"`

## Required outcome
- Between the runner reporting the copy ready and the re-list landing, the page keeps showing the copies panel (with the finished copy or its last running state) instead of falling back to the destinations panel

## Suggested approach (optional)
- Treat a `runner.ready` whose source asset is this recording as "has copies" until `exports` contains it, e.g. fold it into `hasCopies`
````

</details>

