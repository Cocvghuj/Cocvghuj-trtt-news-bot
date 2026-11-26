# TRTT Voyage — Diamond Horizon Mobile & Deployment Repair

**Project:** DR-TRTT-OPS-001  
**Date:** 2026-11-26  
**Branch:** feature/trtt-diamond-horizon-mobile-vercel-fix-20261126

## Scope
- Preserve all existing Blogger posts, pages, menu destinations, and public URLs.
- Add responsive refinements to the existing VoyageHub landing page stylesheet.
- Improve Blogger article readability on narrow screens (tables, code, embeds, images, and tap targets).
- Correct the Vercel Python function configuration so the platform can auto-detect its built-in Python runtime.

## Production deployment finding
The latest Vercel Production deployment for the merged Diamond Horizon commit failed with:
- Error code: `invalid_function_runtime`
- Message: `Function Runtimes must have a valid version`
- Faulty config: `runtime: "@vercel/python"` under `api/trtt_787950_master.py`.

The repair removes the obsolete custom runtime string and keeps `maxDuration: 30`, allowing Vercel's built-in Python function detection to select the runtime. No secrets or environment variables are changed.

## Blogger installation boundary
The repository documents a one-time Blogger Dashboard → Layout → HTML/JavaScript gadget installation:
```html
<link rel="stylesheet" href="https://cocvghuj-trtt-news-bot.vercel.app/trtt-theme.css">
<script defer src="https://cocvghuj-trtt-news-bot.vercel.app/trtt-blog-menu.js"></script>
```
GitHub/Vercel can serve the CSS and menu assets, but the Blogger public API cannot place this gadget or edit Theme XML/Layout. The live blog styling changes only if this gadget is already installed and references the active asset URLs. This PR does not claim to install it.

## Mobile verification matrix
Static targets covered by the stylesheet:
- 320px / 360px / 390px narrow phone widths: single-column cards, wrapping headings and news titles, no forced wide grid.
- 700px breakpoint: touch-sized menu and navigation links, full-width primary actions.
- 768px Blogger breakpoint: responsive post containers, horizontally scrollable tables, wrapping code, bounded images/embeds, larger pager/comment targets.
- Reduced-motion preference remains supported by existing rules.

## Verification boundary
- Source readback and JSON/CSS structural checks: to be recorded after commit.
- Vercel preview build: pending PR automation.
- Actual browser screenshot/device rendering at 320/360/390/768px: NOT TESTED in this chat.
- Live Blogger gadget installation and appearance: NOT TESTED.
- Production deployment: not performed by this PR; owner review/merge remains the release gate.
