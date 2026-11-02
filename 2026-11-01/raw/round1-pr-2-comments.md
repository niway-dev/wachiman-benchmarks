=== COMMENT 4437259043 apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:216
👮 **Wachiman** · 🟡🐛 **Consider · bug: Progressbar nested inside the pill's button is hidden from assistive tech**

The pill is a `<button aria-label={t("expand")}>` (line 199–203) that wraps a `<span role="progressbar" aria-valuenow=…>`. Buttons have presentational children in ARIA, and the button's `aria-label` overrides its content, so screen readers announce only "Show the export's progress". They never hear the percent or the progressbar role. If the minimized state should still report progress, move the progressbar out of the button so it is a sibling, or add the percent to the button's accessible name (for example, by including the `pill` text in the label).

<!-- wachi:finding -->

