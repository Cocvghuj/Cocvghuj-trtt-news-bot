# TRTT Blogger SEO setup

This guide separates repository-side improvements from Blogger dashboard settings. A GitHub commit does not change the live Blogger theme or blog settings by itself.

## Live audit findings (6 November 2026)

The public homepage and a representative post were checked directly.

- Canonical URLs are present and point to the expected Blogspot URLs.
- The homepage title is `TRTTVoyage - Official All-in-One Travel Hub`.
- The homepage meta description is only `TRTT News 24bd`, which is too generic to explain the site's subject.
- A representative flight-guide post has a route-specific title, but its meta description is also only `TRTT News 24bd`.
- The Open Graph and Twitter descriptions inherit that same generic text.

## Recommended global blog identity

Use one consistent brand name and a natural description that accurately reflects the site's actual coverage.

**Suggested blog title**

`TRTT VoyageHub | Europe Travel Guides & Flight Planning`

**Suggested blog description**

`Independent travel-planning guides from Sardinia: Cagliari flights, Europe airport transfers, baggage costs, eSIM connectivity and EU passenger rights.`

Do not add keyword lists, repeated city names, unsupported claims, or promotional guarantees.

## Blogger dashboard steps (manual)

1. Open Blogger Dashboard → Settings → Basic.
2. Set the blog title to the suggested title above, or keep the existing title if the owner prefers it.
3. Open Settings → Meta tags. Enable the search description and enter the suggested global blog description.
4. Save, then re-fetch the homepage and one post to verify the actual `description`, Open Graph description, and Twitter description.
5. In Google Search Console, select the Blogspot property and submit `https://trttnews24bd.blogspot.com/sitemap.xml`. Do not submit the Vercel app sitemap as the Blogger sitemap.
6. Inspect the homepage and a representative post URL in Search Console after Google has had time to recrawl them.

## Per-post search descriptions

The Blogger draft pipeline now builds a unique description from the queued route, IATA airport codes, and travel date, then sends it as Blogger's `customMetaData` field. It deliberately does not use unverified queue prices or airline names as SEO claims.

New drafts still require human review before publication. Existing live posts are not modified by this repository change; update their Search description field in Blogger only after reviewing each article.

## Technical safeguards

- Keep Blogger's canonical URLs; do not inject a second canonical tag.
- Do not add duplicate Article/BlogPosting structured data until the live page's existing structured data has been inspected.
- Do not create keyword-stuffed hidden text or doorway pages.
- Keep affiliate disclosures visible and mark affiliate links with appropriate sponsored attributes.
- Check that every important article has a descriptive title, a unique search description, a clear main heading, useful internal links, and meaningful image alt text.
- Repository changes do not publish to Blogger. The owner must review and apply the manual dashboard steps separately.
