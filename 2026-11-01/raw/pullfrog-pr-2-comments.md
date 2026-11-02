=== COMMENT 4437315710 apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:224
Screen readers never get the percent from the minimized pill. ARIA treats a `<button>`'s children as presentational, so the nested `role="progressbar"` is dropped. The button's `aria-label` ("Show the export's progress") also replaces its visible text, so assistive tech announces neither "YouTube copy" nor "38%".

<details><summary>Technical details</summary>

````markdown
# Pill progress is invisible to assistive tech

## Affected sites
- apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:202 — `aria-label={t("expand")}` on the `<button>` overrides the content-derived name
- apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:216-224 — `role="progressbar"` nested inside a button (children presentational per WAI-ARIA)

## Required outcome
- The pill's accessible name/description includes the destination and percent (e.g. "YouTube copy · 38%") while still saying it expands the widget.

## Suggested approach
- Drop the nested `role="progressbar"`/aria-value* attributes and either let the visible text name the button (with the expand hint via `aria-describedby` or `title`), or build the `aria-label` from both `expand` and `pill` strings. Update the test that queries `{ name: "Show the export's progress" }` accordingly.
````

</details>

