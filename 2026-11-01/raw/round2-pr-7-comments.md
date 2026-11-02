=== COMMENT 4437281260 apps/kaipu-record/src/renderer/src/pages/library/library-page.test.tsx:225
👮 **Wachiman** · 🟡🧪 **Consider · tests: "…and forgets it" never checks that the copy was forgotten**

The test only checks `router.state.location.pathname`. Nothing checks that `markCopySeen` ran (`ready-copy-card` `onOpen` → `library-page.tsx:416`), for example that `getReadyCopies().copies` no longer has `asset-copy`. If the `markCopySeen` call were dropped, this test would still pass, because no Sidebar is mounted here to forget the copy on the detail route. You could add `expect(getReadyCopies().copies).toEqual([])`.

<!-- wachi:finding -->

=== COMMENT 4437281261 apps/kaipu-record/src/renderer/src/pages/library/library-page.tsx:409
👮 **Wachiman** · 🟡🐛 **Consider · bug: While its ready card shows, the copy loses its Edit, Prepare, Tags and Delete actions**

`leadingIds` takes the copy out of the regular `VideoCard` list (lines 422–424), and `ReadyCopyCard` only offers open, reveal, drag and dismiss. So from the grid, a copy that just finished cannot be deleted, tagged or prepared until the user closes the card or leaves the Library. The list view (line 447 onward) never shows the ready card, so there the copy keeps its row. If this is intended, it is worth saying so in the backlog doc. If not, the ready card could expose the same overflow actions.

<!-- wachi:finding -->

