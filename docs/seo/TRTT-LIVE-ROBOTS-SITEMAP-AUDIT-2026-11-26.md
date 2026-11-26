# TRTT Voyage — Live Robots & Sitemap Audit
Date: 2026-11-26
Scope: Public live domain checks only; no Blogger, Cloudflare, DNS, production, or Main settings changed.

## Executive result

- Canonical brand host indicated by homepage Open Graph URL and sitemap entries: `https://www.trttvoyage.com/`.
- Both HTTPS robots endpoints returned HTTP 200 and `text/plain`.
- Both HTTP robots endpoints returned HTTP 200 and `text/plain`; no redirect was observed by the live fetch.
- Both sitemap endpoints returned HTTP 200 and `application/atom+xml; charset=UTF-8`.
- The sitemap feed exposed 131 canonical `www.trttvoyage.com` URL occurrences and 131 timestamps, with no non-canonical host occurrence detected in the feed text.
- Three newest sampled sitemap articles returned HTTP 200.

## Live evidence

| URL | Result |
|---|---|
| `https://trttvoyage.com/robots.txt` | HTTP 200, text/plain; Cloudflare-managed content-signal/crawler policy; no Sitemap directive in returned body |
| `https://www.trttvoyage.com/robots.txt` | HTTP 200, text/plain; Cloudflare-managed policy followed by Blogger-style rules; contains `Disallow: /search`, `Allow: /`, explicit Googlebot and Googlebot-News Allow rules, and `Sitemap: https://www.trttvoyage.com/sitemap.xml` |
| `http://trttvoyage.com/robots.txt` | HTTP 200, text/plain |
| `http://www.trttvoyage.com/robots.txt` | HTTP 200, text/plain |
| `https://trttvoyage.com/sitemap.xml` | HTTP 200, Atom feed; returned feed entries use the www host |
| `https://www.trttvoyage.com/sitemap.xml` | HTTP 200, Atom feed; 131 URL occurrences and 131 timestamps |
| Homepage metadata | Both host homepage fetches expose `og:url=https://www.trttvoyage.com/` |
| Sample articles | Three newest feed articles returned HTTP 200 |

Sitemap timestamp range observed: `2026-10-15T10:22:19Z` through `2026-11-25T18:21:40Z`. Timestamp truthfulness against each post's actual significant modification was not independently audited.

## Findings

1. **PASS — Live sitemap available.** Blogger's Atom feed is a supported sitemap format for Google. Google accepts Atom 1.0 feeds; CMS feeds may contain only recent URLs.
2. **PASS — Canonical host consistency in sitemap.** The 131 observed URL occurrences use `www.trttvoyage.com`; no alternate host occurrence was found.
3. **PASS — Sample post availability.** The three newest sampled URLs returned HTTP 200.
4. **PASS — www robots declares sitemap.** The www robots file points to the live www sitemap.
5. **LOW-RISK IMPROVEMENT — apex robots lacks Sitemap line.** The apex robots response is Cloudflare-managed and contains no Sitemap directive, while the www robots file does. Since robots rules apply per host, the apex robots file is independent. Add `Sitemap: https://www.trttvoyage.com/sitemap.xml` to the apex robots response only if the Cloudflare robots configuration can preserve the current managed policy.
6. **NOT VERIFIED — Full sitemap coverage.** The live feed returned 131 URL/timestamp pairs, but this audit did not compare every Blogger post against the feed or Search Console indexing.
7. **NOT VERIFIED — HTTP canonical redirects.** The HTTP robots endpoints returned 200 in the fetch; redirect behavior for ordinary HTTP page URLs was not conclusively tested.
8. **NOT VERIFIED — Search Console processing.** No Search Console sitemap report or URL Inspection data was available in this audit.

## Safe fix decision

No live changes were made. The apex robots response is generated/managed by Cloudflare, while the www response contains Blogger's rules. Editing the repository's static `robots.txt` would not safely change either live Blogger/Cloudflare response. The correct next change, if approved, is a narrowly scoped Cloudflare robots configuration addition for the apex host:

```text
Sitemap: https://www.trttvoyage.com/sitemap.xml
```

Do not replace the Cloudflare-managed file or remove its existing crawler/content-signal policies. Do not add a second Blogger sitemap or manually replace the Blogger-generated Atom feed.

## Repository context

- The previously referenced branch `feature/trtt-voyage-diamond-theme-v1` was not found in the repository branch search.
- Existing repository root `robots.txt` and `sitemap.xml` on `feature/trtt-seo-meta-descriptions` describe the separate Vercel app host `cocvghuj-trtt-news-bot.vercel.app`; they are not the live Blogger domain's source of truth and were left unchanged.
- This audit report is an additive evidence record only. No existing file was overwritten or deleted.

## References

- Google: RSS/Atom 1.0 feeds are accepted as sitemap formats: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google: robots.txt applies to the specific protocol, host, and port: https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec
- Live endpoints: https://www.trttvoyage.com/robots.txt ; https://www.trttvoyage.com/sitemap.xml
