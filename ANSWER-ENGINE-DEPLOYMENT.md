# TRTT Answer Engine — Deployment and Blogger connection

This repository is the source of truth for the Answer Engine.

## Architecture

- Blogger displays the Answer Engine UI from `trtt-all-in-one.js`.
- The browser sends questions to `https://cocvghuj-trtt-news-bot.vercel.app/api/answer`.
- Vercel runs the server-only function in `api/answer.js`.
- Gemini, OpenRouter, and Groq credentials must remain in Vercel Environment Variables. Never put keys in Blogger HTML, browser JavaScript, GitHub source, or this document.

## Required Vercel environment variables

Set these for the Vercel project and the Production environment (and Preview too, only if testing previews):

- `GEMINI_API_KEY`
- `OPENROUTER_API_KEY`
- `GROQ_API_KEY`

Do not paste secret values into GitHub issues, commits, chat, Blogger, or browser code.

## Vercel project configuration

- Repository: `Cocvghuj/Cocvghuj-trtt-news-bot`
- Branch: `main`
- Root Directory: repository root
- Build Command: `npm run build`
- Output Directory: `dist`
- Keep `api/answer.js` at the repository root. Vercel discovers supported functions from the root `api` directory.
- `build.js` intentionally excludes `api` from static browser assets; do not remove that exclusion.
- `vercel.json` sets the Answer Engine function duration to 30 seconds.

## Allowed Blogger origins (strict three-domain allowlist)

The API allows only these browser origins:

- `https://trttnews24bd.blogspot.com`
- `https://trttnews24bd.com`
- `https://www.trttnews24bd.com`

If the Blogger site uses a different origin, do not broaden this list without the owner's explicit approval.

## Files that must stay synchronized

- `trtt-all-in-one.js`
- `public/trtt-all-in-one.js`

These two browser files must contain identical code. Keep the Golapi `#ff2e63`, Kathali `#FFC300`, and Piaji `#AF7AC5` colors unchanged.

## Safe verification after the owner deploys

1. Confirm the deployment completed successfully.
2. Confirm `https://cocvghuj-trtt-news-bot.vercel.app/api/answer` responds with HTTP 405 to a normal GET request (the endpoint accepts POST only; a GET check does not call either AI provider).
3. From each allowed Blogger origin, submit one simple test question and confirm Gemini, OpenRouter, and Groq results and source links render.
4. If the test fails, inspect Vercel Function Logs and fix the API/configuration before changing Blogger.
5. Do not repeatedly submit questions while debugging: every successful question can call both providers and incur usage charges.

## Important limitations

- AI answers are not guaranteed to be correct; users must inspect the source links, especially for high-impact topics.
- The in-memory rate limit is best-effort and can reset when serverless instances restart.
- The OpenRouter web-search tool is capped at 3 tool calls per question to help control usage. Groq uses the documented `compound-beta` model with built-in web search and citations enabled.
- Do not claim the Blogger integration is live until the owner has deployed the GitHub commit and completed the one-question smoke test.
