## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 by pullfrog[bot]

If the file can't be read, five of the six cards show `…` forever. `useSourceProbe` returns `{ status: "error", probe: null }` for an unusable probe (for example `durationSec === 0`, which the page already guards against with `durationUnreadable`). The page passes only `.probe`, so this panel can't tell "still reading" apart from "failed". Pass the probe status (or a `probeFailed` flag) through and drop the size line, or show a neutral fallback, once reading has failed.

<details><summary>Technical details</summary>

````markdown
# Destination cards stay on "…" when the probe fails

## Affected sites
- apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 — `useSourceProbe(...).probe` discards `status`
- apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:43 — `if (!probe) return null` is the same for loading and error
- apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 — `size ?? "…"` renders a loading indicator forever

## Required outcome
- When `useSourceProbe` reports `status: "error"`, the non-archive cards no longer show a loading ellipsis; they show nothing or a neutral fallback.
- The archive card, which uses `sizeBytes` directly, is unaffected.
````

</details>

