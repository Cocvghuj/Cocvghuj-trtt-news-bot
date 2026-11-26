# TRTT Central Hub Architecture

## Single automation home

`Cocvghuj/Cocvghuj-trtt-news-bot` is the central home for shared TRTT publishing automation, Blogger/Telegram integrations, reusable validation, delivery records, and operating documentation. Other repositories remain source workspaces; their own Blogger/Telegram credentials are not required.

## Public source intake

The scheduled workflow `.github/workflows/trtt-central-draft-ingest.yml` scans only the public repositories in `config/trtt-source-repositories.json`. It reads only direct HTML files under `blogger-drafts/` or `blog/drafts/`.

A source article is ignored unless it contains this exact opt-in comment:

```html
<!-- TRTT_BLOGGER_DRAFT: true -->
```

One previously owner-approved Rise From Ashes article is grandfathered by an exact repository, path, and Git blob SHA pin in the central registry. If that source file changes, the pin no longer matches and the intake rejects it until the central approval is reviewed and updated.

The central workflow downloads eligible files read-only, stages them temporarily under `blog/drafts/`, and calls the central Blogger safety bridge. Temporary copies are removed after processing. Source repositories are never modified.

## Credentials and boundaries

- Blogger OAuth secrets and `BLOGGER_BLOG_ID` are read only from this central repository's GitHub Actions secrets.
- Child repositories need no Blogger or Telegram secrets.
- Private vaults, personal profile repositories, and non-allowlisted repositories are excluded.
- The source allowlist contains public TRTT project repositories only.
- The bridge must validate HTML and read back the Blogger post ID, title, exact content, and `DRAFT` status.
- A matching identical draft may be reused; conflicting or LIVE posts must fail closed.
- No workflow in this intake publishes a Blogger post or sends Telegram.
- Telegram remains a separate published-post-only workflow.
- A dry-run can validate the intake without Blogger credentials or Blogger writes.

## Adding an article

1. Add an HTML article directly under `blogger-drafts/` or `blog/drafts/` in an allowlisted public TRTT source repository.
2. Add the explicit opt-in comment inside the article.
3. Ensure the article meets the central bridge's editorial and HTML validation rules.
4. Merge the source article through the normal review process.
5. The central hourly scan will validate it and create/reuse a Blogger DRAFT only.

A repository being on the allowlist does not make all its content eligible. No marker means no import.

## Current exclusions and limitations

- `trtt-diamond-king-private-vault` is deliberately excluded; no private repository token or cross-repository write access is introduced.
- Public source reading uses GitHub's unauthenticated read API, so the schedule is intentionally limited to once per hour to stay within free rate limits.
- The actual presence and validity of central Blogger secrets, OAuth access, Blogger API success, and Telegram delivery are verified only by real workflow runs.
- This automation does not make a repository open event trigger a workflow. It polls for explicit, merged source content.
