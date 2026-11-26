# TRTT Voyage — GitHub-controlled Blogger styling and menu

GitHub is the source of truth for the managed public CSS, menu configuration and menu loader. Blogger remains the authority for Theme XML, Layout gadget placement and account settings.

## Existing Blogger gadget

The public TRTT Voyage homepage already has a Blogger menu. **Do not add a duplicate HTML/JavaScript gadget.** Preserve the existing Header, LinkList, Blog, page, post and other widgets.

After the owner-reviewed menu-loader PR is merged and the production assets are verified, the existing HTML/JavaScript gadget should reference these production assets:

```html
<link rel="stylesheet" href="https://cocvghuj-trtt-news-bot-git-main-trtt6.vercel.app/trtt-theme.css">
<script defer src="https://cocvghuj-trtt-news-bot-git-main-trtt6.vercel.app/trtt-blog-menu.js"></script>
```

Do not install a feature-branch Preview URL as a permanent Blogger asset. If the existing gadget already contains the verified URLs, do not duplicate or re-add it.

## Menu behavior

- The loader reads the public `blog-control.json` file from the same Vercel production deployment.
- It updates the existing desktop and mobile `#main-menu-nav` lists only after the configuration is fetched and validated.
- If the configuration cannot be fetched or validated, the existing Blogger menu is left unchanged.
- It does not delete Blogger widgets, posts, pages, comments, Theme XML or settings.
- The menu configuration is limited to Home, News, Travel, AI, Tools and About.

## GitHub-controlled assets

- `blog-control.json`: public brand palette and menu links.
- `trtt-theme.css`: Blogger page styling and responsive rules.
- `trtt-blog-menu.js`: safe menu loader.
- `build.js`: verifies that all three public assets are present in the Vercel output.

The public config endpoint permits anonymous GET access only. No Blogger credentials or private data are exposed.

## Control boundaries

GitHub manages the public menu data and delivered assets. Blogger Theme XML, Layout gadget placement, all Blogger settings, posts and Google account settings remain controlled in Blogger. This repository does not claim that a GitHub commit can directly change the Blogger Layout.
