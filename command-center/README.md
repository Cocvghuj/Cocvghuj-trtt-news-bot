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
5. Google Search grounding is not enabled in the app yet: Gemini Search grounding has usage-based billing beyond its current free allowance, so it requires an explicit quota/billing decision first.

## Current server routes
- `GET /api/command-center/health`: authenticated provider readiness (presence only; never returns secrets).
- `POST /api/command-center/chat`: authenticated Gemini → free OpenRouter fallback; requires a durable Google Sheets audit write before reporting success.
- `POST /api/command-center/events`: append a normalized event to Google Sheets.
- `POST /api/command-center/backup`: create a JSON backup in Google Drive using a separate backup token.
- `POST /api/command-center/gmail-draft`: create a Gmail draft only; never sends.
- `GET /api/command-center/calendar-events`: read primary Calendar events.
- `POST /api/command-center/calendar-events`: create an event only with explicit owner approval.
- `GET /api/command-center/github-repo`: read repository metadata through a repository-scoped GitHub App.
- `POST /api/command-center/notion-note`: append a Notion note only with explicit owner approval.
- `POST /api/command-center/telegram-webhook`: owner-chat-only Telegram AI replies with webhook secret validation.

## Required Vercel environment variables
- `COMMAND_CENTER_ACCESS_TOKEN`: long random owner-only access token.
- `COMMAND_CENTER_BACKUP_TOKEN`: separate long random backup token.
- `GEMINI_API_KEY`, `GEMINI_FREE_TIER_CONFIRMED=true` only after checking the Google AI Studio project is on the free tier, optional `GEMINI_MODEL` (default `gemini-2.5-flash`).
- `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` (must end in `:free` while paid use is disabled).
- `ALLOW_PAID_AI`: leave unset or `false`; never enable without explicit budget approval.
- `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`.
- `GOOGLE_AUDIT_SHEET_ID`: spreadsheet containing an `Audit` tab with columns A:H.
- `GOOGLE_DRIVE_BACKUP_FOLDER_ID`: private Drive folder for backups.
- `NOTION_API_KEY`, `NOTION_PROJECT_PAGE_ID`.
- `GITHUB_APP_ID`, `GITHUB_APP_PRIVATE_KEY`, `GITHUB_APP_INSTALLATION_ID`.
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_WEBHOOK_SECRET`.
- Optional OpenAI: `OPENAI_API_KEY`, `OPENAI_MODEL`; never used unless `ALLOW_PAID_AI=true`.

## OAuth scopes to request only when the owner is ready
Start with the minimum scopes required for the approved features:
- Sheets audit: `https://www.googleapis.com/auth/spreadsheets`.
- Drive backup: `https://www.googleapis.com/auth/drive.file`.
- Gmail draft workflow: `https://www.googleapis.com/auth/gmail.compose`.
- Calendar read/write: `https://www.googleapis.com/auth/calendar.events.readonly` for read-only, or `https://www.googleapis.com/auth/calendar.events` only if event creation is enabled.
- Docs: `https://www.googleapis.com/auth/documents`.
- Slides: `https://www.googleapis.com/auth/presentations`.
- Tasks: `https://www.googleapis.com/auth/tasks`.
- Forms: `https://www.googleapis.com/auth/forms.body`.
Add Search Console, Analytics, Maps, Photos, or other Google services only after a concrete use case and scope review. A free consumer product does not guarantee free API access.

## Security boundaries
- All server routes require bearer authentication; backup uses a separate token; Telegram uses its webhook secret and owner chat allowlist.
- Provider keys never belong in browser JavaScript or Git.
- AI prompts and email contents are not written to the audit log; only provider/model/action metadata is stored.
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
6. Create a Notion integration and share only the project knowledge page.
7. Install a repository-scoped GitHub App; connect the Vercel project through OIDC/Connect.
8. Create a Telegram bot and allowlist only the owner's chat ID.
9. Run integration smoke tests and verify each provider's read/write permissions before enabling actions.

## Not yet connected
The code scaffold does not mean OAuth or account access is complete. External account consent and environment setup are intentionally pending. No paid services are provisioned by this project.


## Google OAuth authorization-code setup (Preview only)

The OAuth helper is deliberately a manual, owner-consent flow; it does not connect an account merely because the code is deployed.

1. In Google Cloud project `trtt-news-24`, enable only the Google APIs required for the chosen workflows and configure the OAuth consent screen / test users.
2. Create a **Web application** OAuth client. Add the exact Preview callback URL shown below to Authorized redirect URIs:
   `https://<your-preview-host>/api/command-center/google-oauth-callback`
3. Add these Vercel **Preview** variables (never Production for this task): `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REDIRECT_URI` (exact URL above), and `GOOGLE_OAUTH_SCOPES` (space-separated scopes selected by the owner; default is only `openid email profile`). Keep `COMMAND_CENTER_ACCESS_TOKEN` configured for Preview as well.
4. Call `POST /api/command-center/google-oauth-start` with `Authorization: Bearer <COMMAND_CENTER_ACCESS_TOKEN>` from a secure local terminal. Open the returned `authorization_url` in the same browser. Complete consent yourself.
5. The callback exchanges the code with PKCE and validates the one-time state cookie. It returns the refresh token **once** in a no-store response because this project has no approved token vault/database. Copy it directly into Vercel Preview as `GOOGLE_REFRESH_TOKEN`; never paste it into chat, GitHub, logs, or email. Clear browser history after copying.
6. Redeploy the Preview after adding the variables and run a read-only smoke test. The app does not store the refresh token in its database or repository.

The callback uses HTTPS-only, HttpOnly, SameSite=Lax, 10-minute state/verifier cookies, PKCE S256, exact redirect URI matching, and no-store/no-referrer response headers. A refresh token is sensitive: only perform the callback on a trusted device/browser. If no refresh token is returned, revoke the app grant in your Google Account and repeat consent with offline access. Do not add broader scopes without reviewing the need first.
