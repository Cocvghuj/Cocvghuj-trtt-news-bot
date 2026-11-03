# Copilot instructions — TRTT News 24 BD

## Mission
Maintain the GitHub-managed Blogger assets and the Roksana Nila Answer Engine in this repository. Treat the checked-in code as the source of truth. Before editing, inspect the current files and the relevant workflow history; do not assume old documentation is accurate if it conflicts with current source.

## Answer Engine architecture
- Blogger-facing browser UI: `trtt-all-in-one.js`.
- Public mirror: `public/trtt-all-in-one.js`; it must be byte-identical to the root file.
- Server-only API: `api/answer.js`; it calls Gemini and OpenRouter from the server.
- Static build: `build.js`; it must exclude `api/` from browser-facing `dist/` assets.
- Vercel config: `vercel.json`; static output is `dist`, and `api/answer.js` has a 30-second max duration.
- Browser API endpoint currently configured in the vault: `https://cocvghuj-trtt-news-bot.vercel.app/api/answer`. Do not silently change the hostname.

## Secrets and cost protection
- The API reads only `GEMINI_API_KEY` and `OPENROUTER_API_KEY` from server-side Vercel Environment Variables.
- Never put API keys, OAuth tokens, refresh tokens, access tokens, or other secrets in browser JS, Blogger HTML, repository files, logs, commits, or pull-request text.
- Do not print or request secret values. Verify only whether required secret names are configured, using safe metadata if available.
- Do not confuse Blogger credentials (`BLOGGER_BLOG_ID`, `BLOGGER_API_KEY`, `BLOGGER_ACCESS_TOKEN`, or the OAuth client/refresh-token variables used by existing workflows) with Gemini/OpenRouter credentials.
- Do not make live AI API calls during tests or validation. They can consume paid quota. Use mocked/fake responses for tests.
- Preserve request limits, input-size limits, server-side timeout, and source-link validation. Never remove rate limiting or web-search tool-call limits without documenting the reason.

## Brand and domain locks
Preserve these colors exactly:
- Golapi: `#ff2e63`
- Kathali: `#FFC300`
- Piaji: `#AF7AC5`

Preserve the strict three-origin allowlist in `api/answer.js`:
- `https://trttnews24bd.blogspot.com`
- `https://trttnews24bd.com`
- `https://www.trttnews24bd.com`

Do not add wildcard CORS, extra domains, or broad origin matching. Do not infer that a deployment or Blogger publication happened just because source code changed.

## Blogger boundaries
- The Blogger API cannot generally edit Blogger Theme XML or install/reposition Layout gadgets. The one-time loader/gadget setup is a Blogger-dashboard task and must be documented honestly.
- Existing Blogger publishing/sync workflows can change live content. Do not run, dispatch, enable, or broaden any publishing workflow unless the repository owner explicitly asks for Blogger publishing in the current task.
- In particular, do not trigger `.github/workflows/blogger-direct-publish.yml` or `.github/workflows/blogger-content-sync.yml` as part of Answer Engine work.
- Do not create an automatic push-to-Blogger trigger for the Answer Engine unless explicitly authorized.

## Deployment boundary
- Do not deploy to Vercel, change Vercel project settings, modify Vercel environment variables, or publish to Blogger.
- Prepare and validate repository changes only. The owner will perform deployment separately.
- Do not claim that Blogger is updated or the Answer Engine is live until an authorized deployment and live smoke test have actually succeeded.

## Required checks before committing
Run:
1. `npm test`
2. `npm run build`
3. `node --check api/answer.js`
4. `node --check trtt-all-in-one.js`

If Python workflows are changed, also run the relevant Python unit tests. Do not run content-generation scripts that rewrite live assets as a validation shortcut.

## Change discipline
- Make the smallest safe change that satisfies the task.
- Keep root/public browser copies synchronized.
- Review `git diff` for accidental secrets, unrelated files, changed colors, widened CORS, or changes to live-publishing workflows.
- Preserve existing Blogger posts/pages and unrelated project files.
- If a check fails, fix it before saying the work is ready. If a live integration cannot be tested without secrets/deployment, say exactly that.
