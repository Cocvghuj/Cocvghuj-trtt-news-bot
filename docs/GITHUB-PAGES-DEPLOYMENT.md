# TRTT Voyage — GitHub Pages launch plan

## Scope

This pipeline publishes a static, privacy-filtered version of the TRTT Voyage website from this repository. It does not publish to Blogger, change DNS, attach `trttvoyage.com`, or deploy the Vercel Answer Engine.

Expected project-site URL after GitHub confirms the first deployment:

`https://trtt-voyage.github.io/Cocvghuj-trtt-news-bot/`

The URL is a project-site URL, not a custom-domain migration. The existing Blogger-managed `trttvoyage.com` domain remains untouched.

## Deployment gates

- Pull requests run the existing project tests, existing production-build validation, and the Pages-specific static build/link checks.
- Pull requests upload a validation artifact but do not deploy.
- Only a push to `main` (normally after Owner merges the reviewed PR) deploys the artifact.
- A manual workflow dispatch deploys only when selected on `main`.
- No Blogger workflow is invoked.

## Public artifact allowlist

The Pages build copies only the public website entry points, travel tools, destination pages, selected blog/news HTML, selected CSS and logo assets. It does not copy arbitrary root-level HTML or the entire repository.

Excluded by design: Diamond King admin/command-center HTML, `trttmagic.html`, Blogger vault embeds, diary/health routine pages, backups, raw data/queues, credentials, Python scripts, GitHub workflow source, Blogger theme XML, and private configuration.

The build rewrites root-relative asset links for the GitHub project-site path, updates the PWA manifest scope/start URL, and generates a Pages-specific `robots.txt` and sitemap. It checks every local HTML `href`/`src`/`action`/`poster` target before artifact upload.

## Owner launch steps

1. Review and merge this PR only after its Pages build and existing tests pass.
2. Open **Actions → TRTT Voyage GitHub Pages — Safe Build & Deploy** and verify the main-branch deployment completed successfully.
3. Open the exact `page_url` reported by the deployment job and check the home page, navigation, tools, destination pages, mobile layout, manifest and sitemap.
4. Only after the Pages site is confirmed, begin the separate Blogger stage. Blogger live theme/page/post changes remain separately gated.

## Limitations

GitHub Pages is static hosting. Server-side routes such as `/api/answer` are not included. External provider links remain subject to each provider's terms, availability and tracking behavior. Google indexing is not guaranteed by deployment; Search Console verification and sitemap submission are separate tasks.
