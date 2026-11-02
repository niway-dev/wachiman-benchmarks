=== COMMENT 4437320104 apps/kaipu-record/src/main/recording/recording-ready-window.ts:18
16 DIP is far less room than the card's shadow needs. `.card` in `status-card.module.css` uses `box-shadow: 0 30px 80px -30px rgba(0, 0, 0, 0.8)`, which reaches about 80px below the card. Where the window ends, 16px below the card, the shadow is still around 0.25 alpha. So the floating card will end in a hard horizontal shadow line, easy to see over a light desktop or app. Inside the app the dark UI hid this; floating over other apps, it won't.

<details><summary>Technical details</summary>

````markdown
# Floating card's shadow is clipped by its window

## Affected sites
- apps/kaipu-record/src/main/recording/recording-ready-window.ts:18 — `READY_WINDOW_PADDING = 16`, documented as leaving room so the shadow is not clipped
- apps/kaipu-record/src/renderer/src/assets/main.css:87 — `padding: 16px` on `body[data-window="recording-ready"]`
- apps/kaipu-record/src/renderer/src/features/status-cards/status-card.module.css:11 — `box-shadow: 0 30px 80px -30px rgba(0, 0, 0, 0.8)`, which extends about 80px below and about 50px to the sides of the card

## Required outcome
- In the floating window, the card's shadow fades out inside the window bounds, with no visible cut at the window edge.

## Suggested approach (optional)
- Option 1: in `recording-ready-card.module.css`, give the card a tighter shadow that fits in the 16px padding (scoped to `.frame`).
- Option 2: make the bottom and side padding large enough for the existing shadow, and update `readyWindowBounds` and the CSS together.
- Option 1 keeps the transparent area that sits over other apps small.
````

</details>

