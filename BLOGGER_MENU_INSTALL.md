# TRTT Blogger GitHub → Vercel → Gadget control

## One-time Blogger Gadget loader

Keep one HTML/JavaScript gadget on the Blogger layout. It loads the menu and theme from the Vercel production deployment:

```html
<link rel="stylesheet" href="https://cocvghuj-trtt-news-bot.vercel.app/trtt-theme.css">
<script defer src="https://cocvghuj-trtt-news-bot.vercel.app/trtt-blog-menu.js"></script>
```

Do not paste OAuth credentials or GitHub/Vercel tokens into Blogger. The gadget only loads public presentation assets.

## Edit the menu

Change `trtt-blog-menu.json` in GitHub:
- `brand`: menu brand text
- `links`: ordered label + URL entries
- `menuBackground`, `mobileBackground`, `textColor`: menu colors

## Edit the theme

Change `trtt-theme.css` in GitHub. The Vercel Git integration builds the repository and publishes the root browser assets from `dist/`. The existing gadget loader remains unchanged.

## Posts and Pages source of truth

- Add or edit a Markdown article in `posts/*.md`; the GitHub workflow publishes it as a live Blogger post.
- Add or edit a page in `pages/trttnews24bd/*.html`; the same workflow publishes it as a live Blogger Page.
- Remove a source file to remove only the corresponding Blogger item that was created and marked by this GitHub sync.
- `posts/news_guideline.md` is an editorial instruction file and is intentionally never published.
- The sync uses the existing `BLOGGER_BLOG_ID`, `BLOGGER_CLIENT_ID`, `BLOGGER_CLIENT_SECRET`, and `BLOGGER_REFRESH_TOKEN` GitHub Actions secrets. No credentials are sent to the browser.

The first content-sync run reconciles every supported source file. Later pushes update changed items and remove deleted GitHub-managed items. Blogger items without the TRTT source marker are never modified or deleted.

## Scope boundary

This controls Blogger Posts and Pages plus the Gadget-delivered menu/theme assets. Blogger Theme XML, Layout gadget placement, account settings, and Blogger-only settings are not exposed by the public Blogger API; the one-time Gadget loader must remain installed in Blogger.
