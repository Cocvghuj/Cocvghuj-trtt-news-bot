# Security Policy — TRTT European Family Travel — Marker 787950

## TRTT Super App Security

This project powers European Family Travel automation for:
- GitHub Pages Fast Load: https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/
- Blogger Auto Post + Telegram Channel
- Affiliate Network: Aviasales Marker 787950 + Amazon amzn.to/4shg6Hn

We take security seriously — Affiliate links and customer emails are protected via GitHub Secrets.

## Supported Versions

We actively support security updates for the main travel bot pipeline.

| Version | Supported | Notes |
|---------|-----------|-------|
| 5.1.x   | ✅ | Current Main Branch — Marker 787950 Active |
| 5.0.x   | ✅ | Stable Travel Bot |
| 4.0.x   | ✅ | Legacy with Fast GitHub Mirror |
| < 4.0   | ❌ | No longer supported |

## Reporting a Vulnerability

If you discover a security vulnerability, especially related to:

- `config.py` secrets (BLOGGER_BLOG_ID, TELEGRAM_BOT_TOKEN, TRAVEL_PAYOUT_MARKER)
- Affiliate link injection (Aviasales, Kiwitaxi, Airalo, Amazon)
- GitHub Pages exposure

**Please do NOT open a public issue.**

Instead:

1. Email: Contact via GitHub Profile — Cocvghuj
2. Go to: Security Tab → Report a vulnerability (Private)
3. Expected response: Within 48 hours
4. If accepted: Fix will be deployed via `latest_travel_news.html` pipeline + new release
5. If declined: We will explain why

## Token Safety

- All API keys stored in GitHub Secrets — never hardcoded
- MARKER 787950 is public tracking, not a secret — safe to expose
- Amazon Link amzn.to/4shg6Hn is public — safe
- GMAIL_APP_PASSWORD and BLOGGER_REFRESH_TOKEN must remain secret

Thank you for keeping TRTT Safe!
