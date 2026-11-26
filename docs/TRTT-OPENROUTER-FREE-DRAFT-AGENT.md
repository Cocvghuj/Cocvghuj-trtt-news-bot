# TRTT Voyage — OpenRouter Free Draft Agent

## Purpose
Generate one original, Blogger-ready HTML travel article draft each day using OpenRouter's `openrouter/free` model router. The workflow creates or updates a **draft pull request**; it does not publish to Blogger and does not send Telegram messages.

## Required GitHub Actions Secret
- `OPENROUTER_API_KEY` — OpenRouter API key. Store it in the repository's Actions Secrets. Never paste it into chat, code, commits, or workflow logs.

The workflow also uses GitHub's built-in `GITHUB_TOKEN` for the pull-request action. It does not need Blogger OAuth secrets or Telegram credentials because this workflow does not publish or forward content.

## Free-only configuration
- Model: `openrouter/free`
- Endpoint: `https://openrouter.ai/api/v1/chat/completions`
- No paid model fallback is configured.
- Free-model availability and rate limits can change. A failed/free-capacity request fails the run; it must not silently switch to a paid model.

## Workflow
- Scheduled daily at 04:20 UTC; can also be started manually.
- Generates a new timestamped file under `blog/drafts/`.
- Opens or updates the draft PR on `automation/trtt-openrouter-daily-drafts`.
- No direct commit to `main`, Blogger publish, or Telegram send.

## Editorial safety
- The prompt prohibits fabricated statistics, prices, citations, external URLs, and image URLs.
- The script rejects external URLs and AI-generated image elements.
- It checks for the TRTT marker, website link, five main sections plus FAQ heading, and disclosure text.
- These checks are structural only. They do not prove factual accuracy or publication readiness.
- An editor must verify facts and add a real, licensed image URL before Blogger publication.

## Secret audit limitation
GitHub's connected read interface does not expose the Actions Secrets inventory. Therefore whether `OPENROUTER_API_KEY` is already configured is **NOT VERIFIED**. The secret value is never read by this workflow or exposed in repository files.
