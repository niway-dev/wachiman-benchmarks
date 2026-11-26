# kaipu-bench-wachi-v3#119 [replay r3] feat(desktop): recording detail — title on top, destinations strip, copies from this original - bot inline comments

## apps/kaipu-record/src/renderer/src/features/prepare/components/destinations-panel.tsx:91 · github-actions[bot] · 2026-11-26T20:08:25Z

| 👮 **Wachiman** | Cards show "…" forever when the file cannot be read |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`probe` is null both while the file is being read and after `useSourceProbe` ends in `status: "error"` (it returns `probe: null` for an unusable read, use-prepare-copy.ts:51-58, 29-31). `estimate()` returns null in both cases (line 43), so five of the six cards keep a loading-style "…" for the rest of the page's life when the probe fails. The cards still work, but nothing says the size is unavailable. The caller could pass the probe state, or the card could omit the size line once the read has failed.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:190 · github-actions[bot] · 2026-11-26T20:08:25Z

| 👮 **Wachiman** | Does "Where is it going?" flash back when an export finishes? |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ❓ question |
| **Confidence** | 🟥⬜⬜ Low |
| **Track record** | no record yet · seed |

`showDestinations` depends on `!hasCopies`, where `hasCopies = exports.length > 0 || running !== null` (lines 189-191). When the runner finishes it sets `ready` and clears the job (export-runner.ts:462), so `running` becomes null. The new copy is only in `exports` once the library list has refreshed. That refresh is the `readyId` effect at lines 146-148, or a library-changed broadcast. If the list lags the runner state by a render or more, the page briefly shows the destinations panel and hides "Export a copy", then swaps to the copies panel. Is the new copy guaranteed to be in `videos` before `running` goes null? If not, keeping the destinations panel hidden until the refresh settles would avoid the flash.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/pages/library-detail/library-detail-page.tsx:142 · github-actions[bot] · 2026-11-26T20:08:25Z

| 👮 **Wachiman** | The file is now probed on every preparable recording page, not only when needed |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | ⚡ perf |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

The old code read the file only when `heavy || showCard` ("Read the file up front only when the banner or the card needs its numbers"). Now `useSourceProbe(preparable?.id ?? null)` runs on every recording and copy page, to fill the resolution in the metadata line, the card sizes and the copy dimensions. That is a mediabunny read of container metadata and packets each time a page opens, including for pages that show none of these. This is probably acceptable, but it is a deliberate change from the earlier behaviour and the PR does not say so.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.tsx:109 · github-actions[bot] · 2026-11-26T20:08:25Z

| 👮 **Wachiman** | A copy's picture size is recomputed from the master's probe, not read from the copy |
|:--|:--|
| **Priority** | **Could** · worth a look; change on the merits |
| **Severity** | 🟡 Consider |
| **Area** | 🐛 bug |
| **Confidence** | 🟥🟥⬜ Medium |
| **Track record** | no record yet · seed |

`factsOf` shows `resolveExportTarget(preset, probe, probe.durationSec)` as the copy's "W × H" next to its real file size. This is what today's rules would produce, not what the stored file has. The runner stamps copies with `ENCODE_REVISION` precisely because encode rules change between versions (export-runner.ts:450-453). If the tier or canvas rules change later, older copies will show dimensions they do not have, and nothing marks them as inferred. The prop doc says "follows from it and its preset", so this is acknowledged, but a copy whose real size can be read (or stored on the sidecar) would not drift.

<!-- wachi:finding -->

## apps/kaipu-record/src/renderer/src/features/prepare/components/master-copies-panel.test.tsx:140 · github-actions[bot] · 2026-11-26T20:08:25Z

| 👮 **Wachiman** | Test title claims the button is omitted without an export screen, but only the click is tested |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 🧪 tests |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

"Open in Export → shows only where there is an export screen to open" renders with `onOpenExport` set and clicks it. It never renders without the prop to assert the button is absent. That is the half the title and the `onOpenExport?` contract promise (the page passes `undefined` for a non-preparable video, library-detail-page.tsx:513). Add a `queryByRole("button", { name: "Open in Export →" })` null assertion without the prop.

<!-- wachi:finding -->

## apps/documentation/src/content/docs/backlog/prepare-screen.md:183 · github-actions[bot] · 2026-11-26T20:08:25Z

| 👮 **Wachiman** | Validation steps say to drag the copy's row, but only the Drag handle starts a drag |
|:--|:--|
| **Priority** | **Should** · a change is expected; answer if you disagree |
| **Severity** | 🟡 Consider |
| **Area** | 📝 docs |
| **Confidence** | 🟥🟥🟥 High |
| **Track record** | no record yet · seed |

The checklist says "Drag the copy's row out of the page into Finder". In `master-copies-panel.tsx` the row is a link plus a separate `Drag` button, and only that button is `draggable` and calls `startFileDrag` (lines 164-179). A tester who drags the row, or its link, gets nothing. Say "Drag the copy's Drag handle" so the manual check matches the UI.

<!-- wachi:finding -->
