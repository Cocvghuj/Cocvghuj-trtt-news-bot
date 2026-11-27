# TRTT Voyage — Website, Publishing & Digital Tools

<div align="center">

**[TRTT Voyage — From Vision to Global Brand!](https://trttvoyage.com)**  
**Explore Beyond. Discover Everything.**

[![Official Website](https://img.shields.io/badge/Official%20Website-TRTT%20Voyage-E98BAF?style=for-the-badge)](https://trttvoyage.com)
[![GitHub](https://img.shields.io/badge/GitHub-Cocvghuj-11152D?style=for-the-badge&logo=github)](https://github.com/Cocvghuj)
[![Organization](https://img.shields.io/badge/Organization-Trttvoyage-B77991?style=for-the-badge)](https://github.com/Trttvoyage)

**ONE TEAM. ONE VISION. ONE JOURNEY.**

</div>

## About TRTT Voyage

TRTT Voyage is an independent digital publishing and product-building project founded by **Engr. Abu Taher**. Its focus is practical travel information, verified news, AI-assisted workflows, free web tools, and useful software experiments.

The project is built around four public areas:

- **News** — sourced, dated, transparent editorial content.
- **Travel** — guides, trip-planning resources, and clearly disclosed partner links.
- **AI** — explainers and human-reviewed AI-assisted workflows.
- **Tools** — practical utilities and software experiments with honest feature and privacy notes.

Not every idea or prototype is a finished or publicly deployed product. Each feature must be tested and described according to its actual status.

## Official TRTT Voyage links

- [Official website](https://trttvoyage.com)
- [GitHub profile — Engr. Abu Taher](https://github.com/Cocvghuj)
- [GitHub organization — Trttvoyage](https://github.com/Trttvoyage)
- [WhatsApp Channel](https://whatsapp.com/channel/0029Vb8co9VDeONEz0B5e51M)
- [Telegram Channel](https://t.me/trttnews24bd)
- [Facebook](https://www.facebook.com/profile.php?id=61595319351601)
- [CodePen](https://codepen.io/Abu-Taher-the-styleful)
- [Buy Me a Coffee](https://buymeacoffee.com/engrtaher20)

## Application and repository links

- **GitHub source:** this repository.
- **Vercel project domain:** [cocvghuj-trtt-news-bot.vercel.app](https://cocvghuj-trtt-news-bot.vercel.app/) — a READY production deployment exists in the connected Vercel project, but the project live-alias flag and public access have not been independently confirmed.
- **FlightScoutPro:** a separate project with separate ownership and workflows. It is not part of TRTT Voyage publishing or credential scope.

The canonical TRTT Voyage website link is shown first. The older GitHub repository name, Blogger source folder identifiers, and Vercel project slug are technical identifiers; they are not the public brand name.

## What this repository contains

This repository contains multiple components. Read [AGENTS.md](./AGENTS.md) before making code changes.

| Area | Main files | Purpose |
|---|---|---|
| Static web/PWA | `index.html`, `app.html`, `manifest.json`, `sw.js` | Public site and supporting browser experience |
| Blogger menu and styling | `blog-control.json`, `trtt-theme.css`, menu assets | Blogger-facing navigation and presentation |
| Content and pages | `posts/`, `pages/`, `blog/` | Source material and page templates |
| Blogger draft workflows | `post_news_draft.py`, `post_diary_draft.py`, related scripts | Controlled draft creation and validation |
| Answer Engine | `api/answer.js`, `trtt-all-in-one.js`, `public/trtt-all-in-one.js` | Server-side answer service and browser UI |
| Tests and build | `tests/`, `scripts/`, `build.js` | Offline validation and static build |

## Blogger and publishing boundaries

- GitHub source files do not automatically prove that a Blogger page, theme, menu, or setting has changed.
- The Blogger content-sync workflow is currently disabled.
- The repository may contain draft-generation workflows. A draft is not a live post.
- Live Blogger publishing, theme replacement, and Blogger Layout changes require separate owner approval.
- Existing Blogger posts, pages, widgets, and historical content must be preserved.
- The directory `pages/trttnews24bd/` is retained as a legacy integration/source identifier for compatibility. Its presence does not define the public brand. Do not rename it without auditing every workflow and Blogger mapping.

## Vercel and deployment

The repository is linked to the TRTT Vercel team. The latest production deployment reported by Vercel is READY, but the project-level live flag is false and the custom domain `trttvoyage.com` is not attached to this Vercel team. Do not infer that a production alias, Blogger custom domain, or public route works from a successful build alone.

No deployment is performed by this documentation change. Production deployment, domain attachment, DNS, and security settings remain owner-approved operations.

## Development and validation

Run only the checks appropriate to the component being changed. The repository includes:

```bash
python -m unittest discover -s tests -v
npm test
npm run build
```

Do not run content-generation or publishing scripts as a substitute for tests. Follow [AGENTS.md](./AGENTS.md) and the workflow-specific documentation.

## Security and privacy

- Never commit OAuth refresh tokens, API keys, passwords, Telegram bot tokens, or deployment credentials.
- Keep TRTT Voyage and FlightScoutPro workflows, blog IDs, and secrets isolated.
- Store credentials only in the exact approved GitHub Actions or Vercel secret store required by the relevant workflow.
- Do not publish private email addresses, personal phone numbers, or account recovery details in public pages.
- Public contact is through the official social/community links above.

## Disclaimer and transparency

TRTT Voyage is an independent information and software project. It is not an airline, travel agency, law firm, or government authority. Travel information, fares, schedules, availability, regulations, and partner terms can change; verify important details with official providers before acting.

Some content may contain affiliate links. Where applicable, the relationship must be disclosed clearly near the link. Affiliate links do not guarantee a booking, saving, or result.

AI tools may assist with research, writing, translation, coding, and review. Human review remains necessary. AI assistance is not a substitute for professional legal, financial, medical, travel, or security advice.

Third-party projects and services retain their own ownership, licenses, trademarks, terms, and privacy policies. A fork or integration does not imply endorsement or ownership.

---

**Owner:** Engr. Abu Taher  
**Brand:** [TRTT Voyage](https://trttvoyage.com)  
**Project motto:** ONE TEAM. ONE VISION. ONE JOURNEY.
