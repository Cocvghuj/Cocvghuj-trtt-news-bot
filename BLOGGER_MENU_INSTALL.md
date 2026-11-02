# TRTT Blogger — GitHub-controlled menu and theme assets

This setup makes GitHub the source of truth for the public navigation and CSS styling served to the Blogger site.

## One-time Blogger action (required)

In Blogger Dashboard → Layout, keep one HTML/JavaScript gadget and add:

```html
<link rel="stylesheet" href="https://cocvghuj-trtt-news-bot.vercel.app/trtt-theme.css">
<script defer src="https://cocvghuj-trtt-news-bot.vercel.app/trtt-blog-menu.js"></script>
```

Save the gadget. This one-time Blogger action cannot currently be automated through the public Blogger API. Do not paste OAuth credentials, GitHub tokens, or Vercel tokens into Blogger.

## Ongoing GitHub control

- Edit `trtt-blog-menu.json` to change brand, links, and menu colors.
- Edit `trtt-theme.css` to change the visual styling.
- Push to `main`; the connected Vercel project builds and serves the assets.
- The gadget loads the public assets. It does not receive any secrets.

## Posts and Pages

- `posts/*.md` is the source for GitHub-managed Blogger posts.
- `pages/trttnews24bd/*.html` is the source for GitHub-managed Blogger pages.
- The GitHub Actions content-sync workflow publishes new files and updates changed files.
- Removing a source file removes the corresponding managed Blogger item on the next sync. Review deletions carefully.
- Blogger items without the repository's source marker are not managed by this sync.

## Comments and audit

Use GitHub Actions → **Blogger Admin and Comments** for read-only audit/listing and explicit comment moderation. See [BLOGGER_COMMENTS_ADMIN.md](./BLOGGER_COMMENTS_ADMIN.md).

## Honest control boundary

GitHub controls the posts, pages, menu configuration, delivered CSS, and supported comment operations. It does **not** control Blogger Theme XML, Layout gadget placement, every Blogger setting, or Google account-level settings. The Blogger API does not provide general write endpoints for those areas. A complete takeover is therefore not possible with the current Blogger API; the one-time gadget installation and unsupported dashboard settings remain manual.
