# Blogger Comments and Admin workflow

GitHub Actions → **Blogger Admin and Comments** provides:

- `audit`: read-only totals for the blog, posts, pages, and comments grouped by status.
- `list_comments`: lists comment IDs, post IDs, status, and date. Comment text and author details are deliberately not logged.
- `approve`: marks a selected comment as not spam.
- `mark_spam`: marks a selected comment as spam.
- `delete`: permanently deletes a selected comment and requires the exact confirmation `DELETE:<comment_id>`.

## Run it

Open the repository's Actions tab → Blogger Admin and Comments → Run workflow.
Choose the operation. For a moderation action, provide both the Blogger post ID and comment ID. For deletion, type the exact confirmation string.

Pushing changes to this script or workflow automatically runs only the read-only audit. No comment is changed by a push.

The workflow uses the existing four Blogger GitHub Actions secrets. Credentials are never exposed to the browser or committed to GitHub.

## Blogger API limits

The official Blogger API supports blog metadata, posts, pages, comments, and page-view statistics. It does not provide a general endpoint for editing Blogger Theme XML, rearranging Layout gadgets, or changing all Blogger account/settings options. Those controls remain in Blogger itself.
