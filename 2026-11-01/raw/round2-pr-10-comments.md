=== COMMENT 4437287390 apps/kaipu-record/src/renderer/src/pages/export/recent-exports.tsx:65
👮 **Wachiman** · 🟡🐛 **Consider · bug: An email export changes to the chat label in Recent exports once it finishes**

While a copy is exporting, its row uses `running.destination` (`export-runner.ts:59`, which is set for every destination, including email). After it finishes, the row is built from `destinationOfPreset(copy.export!.preset)`. Email uses the same preset as chat, and `destinations.ts:11-13` says `destinationOfPreset("balanced")` answers "chat". The sidecar only stores `{ preset, fingerprint }` (`shared/types/library-storage.ts:49`). So a copy the user exported "For email" shows the email logo while it runs, then turns into the Slack/Discord logo and name once it's done. The fix is either to save the destination in the sidecar's `export` record or to show a group-neutral label when a preset belongs to more than one destination.

<!-- wachi:finding -->

=== COMMENT 4437287394 apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:80
👮 **Wachiman** · 🟠🧪 **Fix · tests: "does not take a video dropped on the window" would pass even if Library still imported drops**

This test never stubs `pathForFile`, so it uses the global mock in `src/renderer/src/test/setup.ts:156`, `pathForFile: () => ""`. In `use-import-videos.ts:102-111`, `importDropped` treats an empty path as a skipped file and returns before it calls `importVideoFiles`. So if LibraryPage still had a window drop handler, the `.mp4` would be skipped and `expect(importVideoFiles).not.toHaveBeenCalled()` would still pass. The old version of this test stubbed `pathForFile` for exactly this reason.

Fix: stub it like `export-page.test.tsx:421` does (`window.electronAPI.pathForFile = vi.fn((f: File) => `/Users/me/Movies/${f.name}`)`). Optionally also assert that `fireEvent.drop` returns true, meaning nothing called preventDefault, or that no toast was shown. Then the test fails if a drop handler comes back.

<!-- wachi:finding -->

=== COMMENT 4437287396 apps/kaipu-record/src/renderer/src/shell/sidebar.test.tsx:39
👮 **Wachiman** · 🟡🧪 **Consider · tests: "with and without a video" only checks the URL with a video**

The test's name says the Export link is active on Export both with and without a video, but it only renders `/export/asset-1`. The no-video route (`ROUTES.exportNew`, `/export`) is never checked for `aria-current="page"`. The two cases go through different paths: `sidebar.tsx:69` uses `matchPath` with `end: false`, and NavLink has its own matching. Consider adding `renderAt(ROUTES.exportNew)` and the same assertion so the test covers what its name says.

<!-- wachi:finding -->

=== COMMENT 4437287400 apps/kaipu-record/src/renderer/src/pages/library/library-page.module.css:108
👮 **Wachiman** · 🟠📝 **Fix · docs: Orphaned comment about the removed drop strip**

The `.importZone` rule was removed, but its comment `/* NIW2-579: the "Drop a video here" strip, between the header and the toolbar. */` is still there. It now sits right above the `.stickyBar` comment, so it reads as if it describes the sticky toolbar. Delete line 108.

<!-- wachi:finding -->

