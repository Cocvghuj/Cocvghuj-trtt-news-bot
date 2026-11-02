# TRTT News 24 BD — GitHub-controlled Blogger setup

GitHub is the source of truth for the managed blog content, menu configuration, and delivered CSS.

## One-time Blogger setup

In Blogger Dashboard → Layout, add one HTML/JavaScript gadget containing:

```html
<link rel="stylesheet" href="https://cocvghuj-trtt-news-bot.vercel.app/trtt-theme.css">
<script defer src="https://cocvghuj-trtt-news-bot.vercel.app/trtt-blog-menu.js"></script>
```

Save the gadget. This one-time installation must be done in Blogger; the public Blogger API does not let GitHub place Layout gadgets.

## Control from GitHub

- Edit `blog-control.json` for the site brand, colors, and menu links.
- Edit `trtt-theme.css` for Blogger page styling.
- Edit `posts/*.md` for managed posts.
- Edit `pages/trttnews24bd/*.html` for managed pages.
- Push to `main`; Vercel serves the updated assets and GitHub Actions syncs supported posts/pages to Blogger.

The menu loader reads `blog-control.json` directly. The build allowlist publishes this public configuration file; credentials and private files are excluded.

## Control boundaries

GitHub manages supported posts, pages, menu data, CSS, and supported comment operations. Blogger Theme XML, Layout gadget placement, all Blogger settings, and Google account settings remain controlled in Blogger. The gadget above is the only required one-time Blogger-side installation.
