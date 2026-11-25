# TRTT MAGIC — AI Tool Builder MVP

**Branch:** `feature/trtt-magic-ai-tool-builder-mvp-v1`  
**Stage:** Step 1 — first static MVP draft  
**Product direction:** Free-first AI tool builder for TRTT Voyage.

## What this first slice does

- Provides a responsive, mobile-first tool configuration screen.
- Lets a user define a tool name, category, audience, task, boundaries, tone, and output format.
- Includes three starter templates: SEO brief, blog outline, and FAQ maker.
- Generates a reusable instruction prompt locally in the browser.
- Copies the prompt or exports a JSON tool definition.
- Uses no external libraries, API keys, remote requests, or browser storage.

## Important boundary

This is a **front-end prototype**, not a connected AI service. “Generate tool prompt” assembles instructions; it does not call Gemini, OpenRouter, or another model and does not generate an AI answer. The existing TRTT AI Command Center has a separate authenticated server-side AI route, but integration is intentionally deferred until a dedicated API contract, authentication flow, audit requirements, and owner-approved provider configuration are reviewed.

## Security and privacy

- No provider keys or OAuth tokens in browser code.
- No prompt transmission or local persistence in this prototype.
- No `eval()`, dynamic code execution, or third-party scripts.
- Export is an explicit user-initiated JSON download.
- No publishing, deployment, billing, or account connection.

## Validation status

- Static source review: pending Step 2.
- Browser/device runtime test: not run.
- AI provider integration: not connected.
- Authentication and database: not implemented.
- Production deployment: not authorized or attempted.

## Next development stages

1. Review the diff and run static checks.
2. Fix any issues found.
3. Define the server-side AI request contract and fail-closed audit behaviour.
4. Integrate only an approved free-tier provider configuration.
5. Add secure Google OAuth only if required for user accounts; never ask users to paste passwords or OTPs.
6. Add storage only after data retention, deletion/export rights, and privacy notices are designed.
7. Deploy only after explicit owner approval and successful validation.
