# TRTT AI Command Center

## Goal
A secure orchestration layer for TRTT projects and approved Google, Notion, GitHub, Vercel, AI-provider, and Telegram integrations.

## Source-of-truth design
- GitHub: source code, reviewed changes, CI evidence.
- Google Sheets: operational audit ledger (requires Google OAuth and a dedicated spreadsheet with an `Audit` tab).
- Google Drive: timestamped JSON backups of the audit ledger.
- Notion: project decisions, architecture, runbooks, and human-readable knowledge.
- Vercel: hosting, server-side functions, deployment and runtime evidence.
- Telegram: owner-only command channel and notifications.
- Gmail and Calendar: scoped workflows; drafts first, sending or event creation requires owner approval.

Do not copy every record into every service. Keep one canonical record and store references/status for secondary mirrors. A failed mirror remains pending; never report it as completed.

## AI routing
1. Gemini is primary when configured.
2. OpenRouter is fallback; model IDs must end in `:free` unless `ALLOW_PAID_AI=true`.
3. OpenAI API is skipped unless `ALLOW_PAID_AI=true`.
4. Paid service provisioning and paid API use are disabled by default. Provider free quotas are not unlimited and must be checked in the provider console.

## Current server routes
- `GET /api/command-center/health`: authenticated provider readiness (presence only; never returns secrets).
- `POST /api/command-center/chat`: authenticated Gemini → free OpenRouter fallback; requires a durable Google Sheets audit write before reporting success.
- `POST /api/command-center/events`: append a normalized event to Google Sheets.
- `POST /api/command-center/backup`: create a JSON backup in Google Drive using a separate backup token.

## Required Vercel environment variables
- `COMMAND_CENTER_ACCESS_TOKEN`: long random owner-only access token.
- `COMMAND_CENTER_BACKUP_TOKEN`: separate long random backup token.
- `GEMINI_API_KEY`, optional `GEMINI_MODEL` (default `gemini-2.5-flash`).
- `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` (must end in `:free` while paid use is disabled).
- `ALLOW_PAID_AI`: leave unset or `false`; never enable without explicit budget approval.
- `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`.
- `GOOGLE_AUDIT_SHEET_ID`: spreadsheet containing an `Audit` tab with columns A:H.
- `GOOGLE_DRIVE_BACKUP_FOLDER_ID`: private Drive folder for backups.
- Later phases: `NOTION_API_KEY`, `NOTION_AUDIT_PAGE_ID`, GitHub App credentials, Telegram bot token/chat/webhook secret.

## OAuth scopes to request only when the owner is ready
Start with the minimum scopes required for the approved features:
- Sheets audit: `https://www.googleapis.com/auth/spreadsheets`.
- Drive backup: `https://www.googleapis.com/auth/drive.file`.
- Gmail draft workflow: `https://www.googleapis.com/auth/gmail.compose`.
- Calendar: `https://www.googleapis.com/auth/calendar.events`.
Add Docs, Slides, Tasks, Forms, Search Console, Analytics, Maps, Photos, or other Google services only after a concrete use case and scope review. A free consumer product does not guarantee free API access.

## Security boundaries
- All server routes require bearer authentication; backup uses a separate token.
- Provider keys never belong in browser JavaScript or Git.
- AI prompts are not written to the audit log; only provider/model/action metadata is stored.
- Audit writes fail closed. No successful response is returned when the primary audit ledger cannot be written.
- Gmail sending, calendar writes, deployment, GitHub writes, Notion writes, public publishing, paid usage, and destructive actions require explicit owner approval.
- Blogger publishing, Blogger workflow execution, and `main.py` execution remain blocked.
- OAuth consent, account linking, paid quotas, and provider dashboard steps are owner-completed checkpoints.

## Consent and activation checklist
1. Revoke any API key previously exposed in public source and create a replacement.
2. Create the private Google audit spreadsheet and Drive backup folder.
3. Configure Google OAuth consent with only the scopes above; add refresh token to Vercel environment variables, never GitHub.
4. Set the owner access and backup tokens in Vercel.
5. Add Gemini key and a free OpenRouter model key/model if desired.
6. Add Notion integration and share only the project knowledge page.
7. Install a repository-scoped GitHub App; connect the Vercel project through OIDC/Connect.
8. Create a Telegram bot and allowlist only the owner's chat ID.
9. Run integration smoke tests and verify each provider's read/write permissions before enabling actions.

## Not yet connected
The code scaffold does not mean OAuth or account access is complete. External account consent and environment setup are intentionally pending. No paid services are provisioned by this project.
