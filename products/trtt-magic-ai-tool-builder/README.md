# TRTT MAGIC — AI Tool Builder MVP

**Branch:** `feature/trtt-magic-ai-tool-builder-mvp-v1`  
**Stage:** Release candidate hardening  
**Release file:** `products/trtt-magic-ai-tool-builder/trttmagic.html`  
**Product direction:** Free-first AI tool builder for TRTT Voyage.

## What this prototype does

- Responsive, mobile-first tool configuration for name, category, audience, task, boundaries, tone, and output format.
- Three starter templates: SEO brief, blog outline, and FAQ maker.
- Builds a reusable instruction prompt locally in the browser.
- Copies the prompt or exports a JSON tool definition.
- Invalidates the previous preview whenever the user edits or changes configuration, preventing stale copy/export data.
- Uses no external libraries, API keys, remote requests, or browser storage.

## Important boundary

This is a **front-end prompt-builder prototype**, not a connected AI service. “Generate tool prompt” assembles instructions; it does not call Gemini, OpenRouter, or another model and does not generate an AI answer. Backend AI execution, authentication, database, saved tools, billing, hosting, and production deployment are not implemented.

## Security and privacy

- No provider keys or OAuth tokens in browser code.
- No prompt transmission or local persistence in this prototype.
- No `eval()`, dynamic code execution, or third-party scripts.
- Export is an explicit user-initiated JSON download.
- No publishing, deployment, billing, or account connection.

## Validation status

- Previous V3 visual QA baseline: 12/12 Chromium checks passed on GitHub Actions.
- PASS — release-candidate source tests target `trttmagic.html`; GitHub Actions run 45758872204 passed 11/11 tests.
- Chromium E2E/visual QA now targets `trttmagic.html` and includes stale-preview regression coverage; latest run 45758872131 is still in progress, so RC browser validation remains PENDING.
- Physical Android Chrome test: NOT TESTED.
- AI provider integration, authentication, database, and production hosting: NOT IMPLEMENTED.
- Main merge, production deployment, and Blogger publication: NOT AUTHORIZED / NOT ATTEMPTED.

## Next development stages

1. Complete the release-candidate GitHub Actions run and inspect results.
2. Run a physical Android browser check when practical.
3. Define a server-side AI request contract and fail-closed audit behaviour before any provider integration.
4. Review privacy, authentication, storage, and retention requirements before adding accounts or persistence.
5. Merge, deploy, or publish only after separate explicit owner approval.
