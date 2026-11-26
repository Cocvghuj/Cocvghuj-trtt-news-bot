# TRTT Voyage — Project-Wide Safety Audit (2026-11-26)

Project: `DR-TRTT-OPS-001`  
Audit scope: GitHub primary repository, workflow inventory, Blogger public surface, Vercel production asset paths, and owner approval gates.

## Executive result

This is a **partial evidence-based audit**, not a 100% completion certificate. The primary repository tree contains 389 entries and 32 GitHub Actions workflow files. The live Blogger homepage and production CSS were reachable. Several workflow-policy defects were found and corrected on this feature branch only. No PR was merged by the agent.

## Confirmed findings

| Area | Finding | Status |
|---|---|---|
| GitHub repository | Default branch is `main`; current main commit is `a66e2005d5af4575b9d22e6eb75bc28ce49578d8` | PASS |
| Vercel production | Main deployment is READY; production CSS endpoint responds HTTP 200 | PASS |
| Blogger menu loader | `BLOGGER_MENU_INSTALL.md` references `/trtt-blog-menu.js`, but that file is absent from the main tree and the production endpoint returns HTTP 404 | FAIL |
| Blogger menu | `blog-control.json` contains 10 entries; public homepage currently renders 8 entries | MISMATCH |
| Blogger public page | Homepage responds HTTP 200 and has an existing Blogger theme/menu; public HTML does not reveal the exact saved Layout gadget contents | PASS / exact gadget NOT VERIFIED |
| Mobile | CSS includes responsive rules, but physical device viewport testing has not been performed | NOT TESTED |
| News queue | `news/queue/30days.json` was generated 2026-11-06; only 2026-11-06 to 2026-11-08 are marked ready; 2026-11-26 is pending. The daily draft engine refuses to invent a route when today's entry is pending | BLOCKED pending verified queue data |
| News fact-check | `scripts/create_blogger_html_draft.py` validates HTML structure, marker, links and duplicate status; it does not fact-check factual claims | NOT SUFFICIENT alone |
| Central draft intake | Hourly scheduled intake scans allowlisted public repositories for explicit opt-in HTML; structural checks do not prove factual accuracy | Editorial verification required |
| Blogger API | No successful current draft creation/read-back evidence was available in this audit | NOT TESTED |
| Analytics | Current GA4 and Search Console reports were not inspected in this audit | NOT TESTED |

## Blogger menu repair proposed on this branch\n\n- Added `trtt-blog-menu.js` to update the existing desktop/mobile `#main-menu-nav` nodes from the public configuration. It validates HTTPS links and leaves the current Blogger menu unchanged if fetch/config validation fails.\n- Simplified `blog-control.json` to the six approved destinations: Home, News, Travel, AI, Tools and About. No post/page was deleted; only navigation entries are changed after the owner-reviewed release.\n- Added a focused Node test for six-link rendering, unsafe-link rejection and network-failure fallback.\n- Added a build-time check that the CSS, loader and config are included in `dist`, and that the six-link menu is in the approved order.\n- Added public GET CORS for the non-secret `blog-control.json` so the Blogger page can fetch it cross-origin.\n- Updated the install guide to the verified main-branch Vercel alias and explicitly says not to add a duplicate gadget. This is still a proposed asset change: production will remain 404 until the owner merges and Vercel deploys.\n\n## Workflow safety defects found and addressed on this branch

1. `.github/workflows/trtt-safe-auto.yml` previously ran `gh pr merge --auto --squash` for PRs carrying the `auto` label. The merge command is removed; the workflow now validates only and preserves owner-only merging.
2. `.github/workflows/trtt-blogger-telegram.yml` previously ran every 15 minutes and forwarded new Blogger feed items without an explicit per-run owner confirmation. The schedule is removed; manual dispatch now requires `live_done_confirmed=true`.
3. `scripts/telegram_blogger_feed.py` now independently blocks sending unless `TRTT_LIVE_DONE_CONFIRMED=true`, protecting against accidental invocation from another workflow.
4. `.github/workflows/auto-blog.yml` was a scheduled placeholder that wrote a dated Markdown file and attempted to send a hard-coded placeholder Telegram request; it did not create a verified Blogger article. It is now disabled.
5. `.github/workflows/daily-tool.yml` was a scheduled placeholder with no real tool build and an attempted direct push to the default branch. It is now disabled; future tools must use a feature branch and reviewed PR.\n6. `.github/workflows/claude.yml` invoked a paid external Claude API with broad repository write permissions, conflicting with the free-only policy. It is now disabled.\n7. `.github/workflows/trtt-auto-cleaner.yml` could use a personal token to disable other repository workflows. It is now disabled to prevent broad unintended automation changes.

These changes are proposed in a feature branch and are **not live until the owner reviews and merges the PR**.\n\n### Additional workflow review\n- Inspected the Blogger admin, content-sync and read-only diagnostic workflows: all were already disabled.\n- Inspected the TRTT leadership news draft workflow and its Python script: it created both English and Bengali Blogger drafts. The workflow has now been disabled on this branch to comply with TRTT's English-only public-content policy; the source script is preserved.\n- Inspected FlightScoutPro's single-draft workflow and its Python script: it targets the separate FlightScoutPro blog ID, uses a separate secret name, creates a DRAFT and reads it back to confirm DRAFT status; no publish call was found. This is kept isolated from TRTT.\n- Inspected the TRTT diary workflow: it is manual-only, requires the explicit `allow_draft=true` input, and the script creates/reads back DRAFTs.\n- Inspected the location-news workflow: dispatch is restricted to an owner-authored tagged issue, and the script checks Blogger status after creation. Source accuracy still requires editorial verification; a workflow gate alone is not proof of truth.

### Feature-branch verification
- GitHub Actions PR validation run `45894683585`: PASS. Both `npm test` and `npm run build` completed successfully.
- Vercel preview deployment `dpl_6QS3PQ2fg72ipi6TbLGYwgJd7Xoz`: READY, target preview (no production alias).
- Preview `/trtt-blog-menu.js`: HTTP 200.
- Preview `/blog-control.json`: HTTP 200; `Access-Control-Allow-Origin: *` confirmed.
- Preview `/trtt-theme.css`: HTTP 200.
- Preview homepage: HTTP 200.
- Preview URL is temporary and must not be installed as a permanent Blogger asset. Production main still remains unchanged until owner merge.

## News integrity rules

- No fabricated breaking news, route availability, fares, airline claims, quotes, statistics, official announcements or source attributions.
- A URL existing in an article is not proof that the linked source supports the claim.
- Every factual news draft needs a traceable primary source, publication/update date, claim-to-source correspondence, corroboration where appropriate, jurisdiction/context, and an explicit uncertainty check.
- If the evidence is incomplete, stop the news draft or label it as an unverified lead for internal review; do not send it to Blogger automatically.
- Blogger content remains DRAFT-only. Live publication requires owner approval.
- Telegram distribution requires a published URL and explicit owner `LIVE DONE` confirmation.

## Remaining blockers before any “100%” claim

1. Restore and verify the missing Blogger menu loader; confirm it renders from the actual Blogger Layout without removing existing widgets or links.
2. Reconcile the live 8-item menu with the approved 10-item configuration and the current MASTER-004 navigation.
3. Static review of all 32 workflow YAML files is complete. Runtime behavior, actual secret presence (not accessed), external action behavior, and scheduled-job outcomes remain NOT TESTED.
4. Add a meaningful editorial source-verification gate to news generation and Blogger draft ingestion; structural HTML validation is not fact-checking.
5. Replace stale route queue entries only with current, independently verified route/fare evidence.\n6. Keep the legacy bilingual TRTT leadership-draft workflow disabled: it generated both English and Bengali public drafts, conflicting with the English-only policy. Its Python script is preserved but is not callable through this disabled workflow.
6. Run the repository's `npm test` and `npm run build` on the proposed branch and inspect all GitHub Actions results.
7. Verify Blogger draft creation/read-back through an authorized workflow without publishing.
8. Verify Telegram only after the explicit LIVE DONE gate; no test message to the public channel.
9. Test real mobile/desktop rendering and inspect GA4/Search Console/PageSpeed evidence.
10. Reconcile GitLab backup for all relevant branches and verify exact file blob IDs.

## Change boundary

- No Blogger Theme XML, Layout gadget, posts, pages, settings, DNS, or account configuration was changed.
- No production deployment was triggered by this audit.
- No secrets were read, printed, or modified.
- No Telegram message was sent.
- No PR was merged.
- No files were deleted.

## Proposed change branch

`feature/trtt-owner-approval-and-workflow-safety-20261126`

Owner review PR: to be linked after creation.

## Additional editorial / account-isolation risks identified (not yet repaired)

1. `.github/workflows/trtt-news-draft.yml` was manual-only but invoked `post_news_draft_v2.py`, which created drafts on both TRTT and FlightScoutPro in the same workflow. This conflicted with the explicit project isolation rule. The workflow is now disabled on this feature branch; the Python source remains preserved. Separate single-blog workflows must be used.
2. `post_news_draft_v2.py` contains fixed articles dated 2026-11-09 and 2026-11-10. These may be used only as dated historical explainers after source re-verification; they are not a current-news feed. No Blogger draft was created.
3. Legacy `scripts/draft_news.py` is not referenced by the current active workflow inventory. Its entry point supplied default news topic/source and injected unsupported first-person Sanluri/Cagliari experience, named-author and affiliate claims. The entry point is now fail-closed on this feature branch, and the reference helper was reduced to a neutral TRTT link with a current-prices/terms verification reminder. Existing validation helpers are retained; focused tests now assert the unsupported claims are absent.
4. The daily route queue has no `source_url`, source publication timestamp, retrieval timestamp, fare verification timestamp or source attribution fields. The daily engine refuses to draft when today's queue item is pending, which is the current safe outcome. Do not mark a route ready until primary-source evidence and a current fare check are attached.
5. The existing HTML validator checks structure, URLs and disclosure wording; it does not confirm that source pages support individual claims. A claim-to-source editorial manifest and review gate remain outstanding.

These items are additional blockers. They are intentionally not represented as completed fixes.
