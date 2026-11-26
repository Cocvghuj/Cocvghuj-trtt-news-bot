# TRTT HTML → Blogger Draft Automation

## Purpose
When an HTML article is merged into `main` under `blog/drafts/*.html`, this workflow creates a Blogger **DRAFT** on the TRTT Voyage blog and reads it back to verify the post ID, title, content, and `DRAFT` status.

It never publishes a post and never sends a Telegram message. Telegram forwarding remains a separate workflow that handles published feed items only.

## Required GitHub Actions Secrets
- `BLOGGER_BLOG_ID` — TRTT Voyage Blogger blog ID only.
- `BLOGGER_CLIENT_ID`
- `BLOGGER_CLIENT_SECRET`
- `BLOGGER_REFRESH_TOKEN`

The workflow intentionally does not use `FLIGHTSCOUTPRO_BLOG_ID`, Telegram credentials, or OpenRouter credentials.

## Trigger
- Automatic: push to `main` affecting `blog/drafts/*.html`. This includes an Owner-merged PR that adds a draft HTML file.
- Manual retry: Actions → “TRTT HTML to Blogger Draft (never publish)” → Run workflow, supplying an existing `blog/drafts/FILE.html` path.

## Safety
- Accepts only HTML files directly under `blog/drafts/`.
- Requires one H1 title, at least six H2 headings (five sections plus FAQ), the TRTT marker `787950`, the TRTT website link, and an affiliate disclosure.
- Rejects unsafe HTML tags, event-handler attributes, and non-HTTPS image/link URLs.
- Checks existing Blogger posts with the same title. A LIVE match or a different-content DRAFT match stops safely; it never overwrites an existing post.
- Creates with Blogger API `isDraft=True`.
- Reads the created/existing post back and verifies ID, title, exact HTML content, and status `DRAFT`.
- No Blogger live publish, no Telegram send, no FlightScoutPro write.

## Limitations
- The structural checks do not independently fact-check the article. Editorial source verification and image rights review remain required before Owner publication approval.
- Actual Secret configuration, OAuth access, Blogger API success, and Telegram delivery must be verified by a real workflow run. Source-code references alone do not prove a Secret exists.
