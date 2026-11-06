# Copilot one-shot task — prepare TRTT Answer Engine for Blogger

Copy the prompt below into GitHub Copilot Chat in Agent mode while this repository is open.

---

You are working in `Cocvghuj/Cocvghuj-trtt-news-bot`, branch `main`. Complete the TRTT News 24 BD / Roksana Nila Answer Engine repository preparation as one focused task.

## Read first
1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `README.md`
4. `ANSWER-ENGINE-DEPLOYMENT.md`
5. `api/answer.js`
6. `trtt-all-in-one.js` and `public/trtt-all-in-one.js`
7. `build.js`, `package.json`, and `vercel.json`
8. `trtt-loader.js`, `public/trtt-loader.js`, and `BLOGGER_MENU_INSTALL.md` if present.

## Goal
Leave one coherent, tested, documented implementation in GitHub so the owner can deploy it later and connect it to Blogger without having to redesign or reconstruct the project.

## Work to do
1. Audit the current Answer Engine end-to-end. Fix actual defects only; do not rewrite unrelated site features.
2. Confirm the browser UI posts to the existing Vercel API endpoint and handles loading, empty input, network errors, HTTP errors, partial Gemini/OpenRouter/Groq failures, answers, and source links safely.
3. Confirm the server API reads `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, and `GROQ_API_KEY` only from server environment variables. Keep all credentials out of browser files and Blogger HTML.
4. Verify Gemini Google Search grounding, OpenRouter web search, and Groq Compound web-search request/response handling against the currently supported provider API contracts. If a provider schema/model is uncertain, document the uncertainty and implement a conservative supported request; do not invent successful responses.
5. Keep strict CORS limited to exactly:
   - `https://trttnews24bd.blogspot.com`
   - `https://trttnews24bd.com`
   - `https://www.trttnews24bd.com`
6. Keep question length/rate limits, server timeouts, safe DOM rendering, HTTPS-only source links, and a bounded web-search tool-call count. Do not add client-side API keys.
7. Preserve the exact brand colors: `#ff2e63`, `#FFC300`, `#AF7AC5`.
8. Keep `trtt-all-in-one.js` and `public/trtt-all-in-one.js` byte-identical.
9. Keep `api/answer.js` server-only and excluded from `dist/` by `build.js`. Keep `vercel.json` configured for `dist` plus the Answer API function.
10. Ensure the Blogger installation guide explains the one-time Layout HTML/JavaScript gadget setup. Do not claim GitHub can install Blogger gadgets or edit Blogger Theme XML through the public Blogger API.
11. Add/update automated local checks. They must not call Gemini, OpenRouter, Blogger, or Vercel and must not consume API quota.
12. Update README and deployment docs with exact steps, required environment-variable NAMES only, expected smoke-test behavior, rollback guidance, and honest limits.
13. Review `git diff` for unrelated changes, secret leakage, extra CORS origins, color changes, or publishing workflows being altered.

## Absolute safety rules
- DO NOT deploy to Vercel.
- DO NOT publish or update anything on Blogger.
- DO NOT dispatch or change `.github/workflows/blogger-direct-publish.yml` or `.github/workflows/blogger-content-sync.yml`.
- DO NOT change Vercel settings or secrets.
- DO NOT print, request, commit, or expose secret values.
- Do not use `BLOGGER_API_KEY` or `BLOGGER_ACCESS_TOKEN` as Gemini/OpenRouter credentials. The Answer Engine requires separate server-side `GEMINI_API_KEY` and `OPENROUTER_API_KEY`.
- Do not claim the live blog is updated. This task prepares repository code only.
- Do not delete or overwrite unrelated Blogger pages, posts, themes, vault features, or existing project files.

## Validation
Run all of:
- `npm test`
- `npm run build`
- `node --check api/answer.js`
- `node --check trtt-all-in-one.js`

If any check fails, fix it and rerun. Inspect the final diff. If any live integration remains untestable without deployment/secrets, list it as a pending owner-side smoke test, not as a pass.

## Completion report
Return:
- files changed;
- fixes made;
- exact commands and pass/fail results;
- any remaining manual Blogger Layout step;
- required Vercel environment-variable names (names only): `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `GROQ_API_KEY`;
- explicit confirmation that no Vercel deployment, Blogger publishing, or paid AI API call was performed.

If repository write/commit capability is available, commit the finished changes to the current working branch and report the commit SHA. Do not force-push or rewrite history.
