# TRTT Voyage — SEO Health, Public Index Visibility & Blog Growth Audit
Date: 2026-11-26
Repository: Cocvghuj/Cocvghuj-trtt-news-bot
Branch: feature/trtt-seo-meta-descriptions
Scope: Public live-site inspection and repository review. No Search Console account data, Blogger dashboard changes, live publication, DNS, Cloudflare, Main merge, or deployment.

## Executive summary

- Public website and sampled article URLs are reachable (HTTP 200).
- Live canonical brand identity is `https://www.trttvoyage.com/` based on homepage Open Graph metadata and the live Blogger sitemap URLs.
- Live `www` sitemap is an Atom feed, HTTP 200, with 131 observed URL occurrences and 131 timestamps; all observed post URLs use `www.trttvoyage.com`.
- Live `www` robots.txt includes a sitemap declaration and allows Googlebot / Googlebot-News; the apex robots endpoint is separately served by Cloudflare-managed policy and does not include a Sitemap line.
- Public search query `site:trttvoyage.com` returned only the homepage, with the message “No information is available for this page.” This is weak public-index evidence only; it does NOT establish that posts are not indexed.
- Google Search Console coverage, impressions, clicks, sitemap processing status, and URL Inspection remain NOT VERIFIED because no eligible direct Search Console connector/account data was available. Do not infer GSC state from public search snippets.
- Repository SEO setup documentation contains older Blogspot-domain assumptions that conflict with the current live custom-domain evidence. This addendum records the discrepancy; the historical file is not overwritten.

## Public live checks

| Check | Evidence | Status |
|---|---|---|
| Homepage | `https://www.trttvoyage.com/` returned HTTP 200; title “TRTT Voyage | Global News, Travel, Technology & AI”; description and Open Graph metadata present | PASS |
| Homepage canonical identity | `og:url=https://www.trttvoyage.com/` on both apex and www homepage fetches | PASS |
| www robots | HTTP 200 text/plain; `Allow: /`, `Disallow: /search`, Googlebot and Googlebot-News Allow rules, sitemap line | PASS |
| apex robots | HTTP 200 text/plain; Cloudflare-managed content-signal/crawler policy; no sitemap line in response | Improvement candidate |
| www sitemap | HTTP 200 `application/atom+xml`; 131 URL occurrences, 131 lastmod values; all observed URLs use www host | PASS |
| sitemap timestamps | Range observed: 2026-10-15T10:22:19Z to 2026-11-25T18:21:40Z | Observed; not independently verified against post edits |
| newest sampled posts | Three newest feed URLs returned HTTP 200 | PASS |
| Public search | `site:trttvoyage.com` query returned homepage only; no post result surfaced | Limited signal; indexing NOT VERIFIED |
| Search Console | No direct GSC property, performance, indexing or URL inspection report retrieved | NOT VERIFIED |

## Important interpretation

1. The Blogger sitemap is an Atom feed, not a conventional XML sitemap index. Google supports RSS/Atom feeds as sitemap formats.
2. Robots rules apply to the exact protocol, host, and port. Apex and www robots files are independent.
3. The apex robots file appears Cloudflare-managed; do not edit repository `robots.txt` expecting it to change live Blogger or Cloudflare responses.
4. Firecrawl's processed HTML for post pages included an embedded Blogger comment-frame canonical element (`https://www.blogger.com/comment/frame/...`). This is an iframe artifact, not reliable evidence of the article's own canonical tag. The post canonical tag therefore remains NOT VERIFIED in this audit. A browser/raw source inspection or Search Console URL Inspection is required.
5. A public `site:` search is approximate and cannot replace Search Console's indexed/not-indexed reports.

## Repository discrepancy

The existing `BLOGGER_SEO_SETUP.md` in this feature branch describes the earlier Blogspot-hosted domain, including an older homepage title/description and a Blogspot sitemap submission instruction. Those details conflict with the currently observed custom-domain homepage metadata and sitemap host. The historical guide was not changed; this new audit addendum supersedes its old live-domain assumptions for the evidence date above. Before applying any manual settings, reconcile the Blogger property and custom-domain configuration using the current Blogger dashboard and Search Console.

## Prioritized SEO action plan

### P0 — Verify Search Console truth (owner/account access required)
- Inspect the Domain property for `trttvoyage.com` (or the exact verified URL-prefix property).
- Check Sitemaps report for `https://www.trttvoyage.com/sitemap.xml`: submitted/read status, last read, discovered URLs, errors.
- Inspect homepage plus 3 representative article URLs with URL Inspection: Google-selected canonical, user-declared canonical, crawl allowed, indexing allowed, last crawl, referring sitemap.
- Export 28-day and 3-month Performance reports (clicks, impressions, CTR, average position; queries and pages).
- Do not request indexing in bulk. Use URL Inspection only for a small set of important updated/new URLs after technical verification.

### P1 — Confirm canonical and crawler directives
- Inspect raw rendered HTML (not embedded comment iframe) for each article's canonical, meta robots, title, description and structured data.
- Confirm apex ordinary page URLs redirect to the preferred www HTTPS host. The robots endpoint fetch alone does not prove page redirect behavior.
- Consider adding the canonical www sitemap line to apex robots only through the Cloudflare-managed robots configuration, preserving all existing rules. No change made.
- Do not inject duplicate canonical or Article schema without verifying Blogger's current output.

### P2 — Improve content discoverability
- Prioritize useful, original travel utility pages that answer one concrete traveller question.
- Build tightly connected topic clusters: Sardinia/Cagliari travel, EU passenger rights, airport transfers, eSIM connectivity, baggage/flight planning.
- Each article: descriptive title, one clear H1, unique accurate search description, useful first-hand/original information, named sources for claims, descriptive image alt text, and 2–4 contextual internal links to genuinely related pages.
- Add a visible “Last updated” note only when substantive review/update occurred; do not manipulate dates.
- Add an author/editorial policy and transparent affiliate disclosure where relevant.
- Avoid thin AI-generated pages, keyword stuffing, duplicate location pages, unsupported prices/claims, and mass-produced FAQs.

## Next content brief — draft only, not published

Working title: **Cagliari Airport to the City Centre: Transport Options, Costs to Check and Planning Tips**

Search intent: Practical trip planning for travellers arriving at Cagliari Elmas Airport (CAG).

Proposed outline:
1. Quick answer: airport location and the main transport choices (verify current services before publication).
2. Train: station access, journey planning, timetable source.
3. Taxi: official rank, fare basis and how to verify current fare.
4. Rental car: pickup, insurance, parking and ZTL cautions.
5. Bus / alternative transfers: current operator and service verification.
6. Which option fits late arrivals, families, luggage and onward Sardinia trips.
7. FAQ based only on verified operator/airport information.
8. Sources and last-checked date.

Publication gate: do not state live fares, schedules, service frequency, terminal access or operating hours until verified from official airport/operator sources. Add a clear update date and affiliate disclosure if monetized links are used. This is a content brief only, not a Blogger draft or live post.

## Evidence links

- Homepage: https://www.trttvoyage.com/
- Robots (www): https://www.trttvoyage.com/robots.txt
- Robots (apex): https://trttvoyage.com/robots.txt
- Sitemap: https://www.trttvoyage.com/sitemap.xml
- Google sitemap guidance: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google robots specification: https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec

## Change log

- Added this audit as a new file only.
- No existing file overwritten or deleted.
- No Blogger settings, live posts, Cloudflare settings, DNS, GitHub Main, or deployment changed.
