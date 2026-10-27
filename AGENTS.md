# AGENTS.md

## What this repo is

A **static PWA** — no application server, no database, no build step.

| Path | Role |
| :--- | :--- |
| `index.html` | The whole site (~200 KB single-file React artifact, self-contained) |
| `app.html` | Leaflet map page, loads `partners.json` and OSM tiles |
| `manifest.json`, `sw.js` | PWA manifest / service worker |
| `partners.json`, `robots.txt`, `sitemap.xml` | Static data & SEO files |
| `main.py`, `config.py`, `auto_organize.py`, `scripts/next_gen_engine.py` | Content-generation jobs, **not** part of serving the site |

## Run it (Base44 dev environment)

```bash
docker compose -f docker-compose.base44.yml up -d
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/   # 200
```

- `web` is `nginx:1.27-alpine` serving the bind-mounted checkout at
  `/usr/share/nginx/html`, exposed on host port **3000**.
- `docker/nginx.base44.conf` is a **full** `nginx.conf` (not a `conf.d` snippet):
  `user root;` so nginx can read a 700-permission checkout, caching disabled so
  edits appear on reload, and `*.py|*.md|*.yml` blocked with 404 so source files
  are never served to the browser.
- There is no reload watcher; a page refresh picks up any edit, because nothing
  is compiled or copied.

## Gotchas

- Do **not** run `main.py` / `scripts/next_gen_engine.py` to "check the app":
  they rewrite `index.html` and `latest_travel_news.html` with generated
  affiliate content. They need Blogger OAuth + Telegram credentials and only run
  in GitHub Actions (`.github/workflows/`).
- `index.html` asks for `/fonts/Optimistic*.woff2`, which the repo does not
  ship; the fallback to `system-ui` is expected and matches the GitHub Pages
  deployment.
- No credentials are required to serve the preview.

## Verification

- `curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/` returns `200`.
- `docker compose -f docker-compose.base44.yml ps` shows `web` as `healthy`.
- `/app.html` returns `200` and renders the Leaflet map with the Rome/Dhaka
  partner markers from `partners.json`.
