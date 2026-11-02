# TRTT News 24 BD — GitHub-managed Blogger publishing and site assets

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Security Policy](https://img.shields.io/badge/Security-Policy-blue)](./SECURITY.md)
[![Vercel App](https://img.shields.io/badge/Vercel-Live%20App-000000?logo=vercel)](https://cocvghuj-trtt-news-bot.vercel.app/)

This repository is the source of truth for the GitHub-managed parts of TRTT News 24 BD. GitHub Actions synchronizes supported content to Blogger; Vercel serves the public menu and theme assets.

## Live projects

- [TRTT News 24 BD on Blogger](https://trttnews24bd.blogspot.com/)
- [TRTT web app](https://cocvghuj-trtt-news-bot.vercel.app/)
- [FlightScoutPro itinerary planner](https://cocvghuj-trtt-news-bot.vercel.app/flightscoutpro-itinerary.html)
- [Flight search tool](https://cocvghuj-trtt-news-bot.vercel.app/tools/flight-search.html)
- [Delay calculator](https://cocvghuj-trtt-news-bot.vercel.app/tools/delay-calculator.html)

## What GitHub controls

| Blog area | Source of truth / control | Current boundary |
| --- | --- | --- |
| Posts | `posts/*.md` → Blogger Posts via GitHub Actions | Supported files are published live; edits sync; deleting a managed source file deletes its managed Blogger post |
| Pages | `pages/trttnews24bd/*.html` → Blogger Pages via GitHub Actions | Same managed-source behavior as posts |
| Menu | `trtt-blog-menu.json` → Vercel → Blogger HTML/JavaScript gadget | The gadget must be installed once in Blogger Layout |
| Theme styling | `trtt-theme.css` → Vercel → Blogger gadget stylesheet | CSS styling is controlled; Blogger Theme XML is not |
| Comments | GitHub Actions workflow **Blogger Admin and Comments** | Read/list/approve/mark-spam/delete selected comments; moderation is manual |
| Blog audit | GitHub Actions workflow **Blogger Admin and Comments** | Read-only blog, post, page, comment and page-view report |

## Publish and edit content

- Add or edit a Markdown article in `posts/*.md`.
- Add or edit an HTML page in `pages/trttnews24bd/*.html`.
- Push to `main`; the content-sync workflow updates the matching GitHub-managed Blogger items.
- `posts/news_guideline.md` is intentionally excluded.
- Removing a managed source file is destructive: the next sync deletes the corresponding GitHub-managed Blogger item. Review deletions before pushing.

The sync uses stable source markers and does not intentionally modify Blogger posts/pages that do not carry a TRTT GitHub source marker.

## Menu and styling

Edit `trtt-blog-menu.json` for the brand, ordered links, and colors. Edit `trtt-theme.css` for presentation. The Vercel build copies public browser assets from the repository into `dist/`.

One-time Blogger setup is required: keep a single HTML/JavaScript gadget in Blogger Layout containing the loader shown in [BLOGGER_MENU_INSTALL.md](./BLOGGER_MENU_INSTALL.md). Do not place OAuth credentials or deployment tokens in that gadget.

## Comments and audit

Open GitHub → Actions → **Blogger Admin and Comments**. The default audit is read-only. Comment moderation requires an explicit manual workflow run and the target post/comment IDs. Permanent deletion additionally requires the exact confirmation string described in [BLOGGER_COMMENTS_ADMIN.md](./BLOGGER_COMMENTS_ADMIN.md).

## What cannot be fully controlled by GitHub

The public Blogger API does not expose general write operations for Blogger Theme XML, Layout gadget placement, all Blogger Settings, or Google account-level settings. Therefore this repository does not claim complete control of the Blogger account. The Blogger-side loader installation and unsupported settings remain manual Blogger-dashboard actions. Do not assume a GitHub push changed those areas.

## Validation

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
npm run build
```

## Security

Blogger OAuth credentials belong only in GitHub Actions secrets. Never commit refresh tokens, client secrets, access tokens, or deployment credentials. Public Vercel assets must contain presentation code only.

See [Security Policy](./SECURITY.md), [Compliance notes](./COMPLIANCE.md), and [MIT License](./LICENSE).
