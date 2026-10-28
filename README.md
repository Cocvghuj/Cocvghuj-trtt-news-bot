# TRTT News 24 BD

TRTT News 24 BD is a static travel and publishing website focused on Europe travel tips, smart trip planning, and AI-assisted content automation. The site is designed for GitHub Pages or static hosting and includes a travel guide, blog/news section, and affiliate comparison pages.

## Project overview

This repository contains:
- a marketing and travel landing page
- a blog/news section
- travel guide and disclosure pages
- eSIM / affiliate comparison pages
- automation scripts for content generation
- Docker preview configuration for local static serving

## Repository structure

- `index.html` — main landing page
- `app.html` — map/marker page
- `blog/index.html` — blog/news landing page
- `trtt-shop/esim/index.html` — eSIM comparison page
- `assets/css/site.css` — shared site styling
- `scripts/` — Python automation helpers
- `main.py` — content generation entry point
- `auto_organize.py` — content organization utility
- `docker-compose.base44.yml` — local preview via nginx

## Local preview

### Option 1: Docker preview

```bash
docker compose -f docker-compose.base44.yml up -d
```

Then visit:

```text
http://localhost:3000/
```

### Option 2: open static files directly

You can also open the HTML files locally in a browser, though some relative links work best when served from a static web host.

## Deployment

This project is suitable for:
- GitHub Pages
- static hosting providers
- any nginx or CDN static host

## Notes

- The site is static and does not require a backend server.
- Python scripts are automation content tools and are not required for serving the site.
- For content and automation workflows, review the Python scripts before running them in production.

## Recommended next improvements

- unify branding across all pages
- add article cards and categories to the news section
- create dedicated travel destination pages
- add SEO files such as `robots.txt` and `sitemap.xml`
- add a stronger README for automation and publishing workflows
