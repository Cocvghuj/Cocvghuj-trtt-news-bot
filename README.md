# TRTT News 24 BD — Travel & Publishing Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Security Policy](https://img.shields.io/badge/Security-Policy-blue)](./SECURITY.md)
[![Vercel App](https://img.shields.io/badge/Vercel-Live%20App-000000?logo=vercel)](https://cocvghuj-trtt-news-bot.vercel.app/)

This repository contains the TRTT / FlightScoutPro web tools and an automated workflow that prepares Blogger posts as **drafts for human review**.

## Live projects

- [TRTT web app](https://cocvghuj-trtt-news-bot.vercel.app/)
- [FlightScoutPro itinerary planner](https://cocvghuj-trtt-news-bot.vercel.app/flightscoutpro-itinerary.html)
- [Flight search tool](https://cocvghuj-trtt-news-bot.vercel.app/tools/flight-search.html)
- [Delay calculator](https://cocvghuj-trtt-news-bot.vercel.app/tools/delay-calculator.html)
- [TRTT News 24 BD on Blogger](https://trttnews24bd.blogspot.com/)
- [FlightScoutPro on Blogger](https://flightscoutpro.blogspot.com/)

## Blogger draft automation

The workflow is `.github/workflows/trtt-unified-autopilot.yml`.

- Runs on its configured schedule and can also be started manually.
- Runs the Python unit tests before generating content.
- Uses configured AI, Unsplash, and Blogger credentials from GitHub Actions secrets.
- Creates reviewable Blogger drafts; it does **not** automatically publish posts live.
- Records completed draft history in `drafted_history.txt`.

Required GitHub Actions secrets depend on the enabled integrations. Common Blogger and content-generation secrets include `BLOGGER_BLOG_ID`, `BLOGGER_CLIENT_ID`, `BLOGGER_CLIENT_SECRET`, `BLOGGER_REFRESH_TOKEN`, and `GEMINI_API_KEY`. Never put credentials or refresh tokens in repository files or commit history.

## Validation

Run the test suite locally:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

GitHub Actions also runs Python validation on relevant pushes and pull requests.

## Affiliate links and disclosures

Some pages may contain affiliate links. A commission may be earned if a visitor makes a qualifying purchase; this does not increase the visitor's price unless the partner says otherwise. Partner availability, prices, and terms can change. Verify details on the provider's website before purchasing.

## Legal and security information

- [Compliance notes](./COMPLIANCE.md)
- [Security policy](./SECURITY.md)
- [License](./LICENSE)

The presence of policy documents is not a certification or guarantee of legal compliance. Each integration and published page must be reviewed against the applicable provider terms and local law.

## Contact

Project: [@Cocvghuj on GitHub](https://github.com/Cocvghuj)
