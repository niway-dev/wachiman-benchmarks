=== COMMENT 4437283524 apps/kaipu-record/src/renderer/src/features/status-cards/export-status-cards.tsx:202
👮 **Wachiman** · 🟡🐛 **Consider · bug: Pill's aria-label hides its progress from screen readers**

The pill `<button>` has `aria-label={t("expand")}`. That label replaces the button's accessible name, so screen readers announce "Show the export's progress" and never read the visible "YouTube copy · 38%". The `role="progressbar"` span inside it (lines 216–224) is also likely ignored, because a button's children are presentational. While the widget is minimized, a screen-reader user has no way to hear how far the export has got. One option is to drop the button's aria-label and let the visible text name it, adding the expand hint with `aria-describedby` or `title`. Another is to put the progressbar next to the button instead of inside it.

<!-- wachi:finding -->

