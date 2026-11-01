"use strict";

const PROVIDERS = Object.freeze({
  gemini: { env: ["GEMINI_API_KEY"], role: "primary_ai", free_tier_only: "verify_in_provider_console" },
  openrouter: { env: ["OPENROUTER_API_KEY", "OPENROUTER_MODEL"], role: "fallback_ai", free_model_required: true },
  openai: { env: ["OPENAI_API_KEY"], role: "optional_ai", paid_disabled_by_default: true },
  google_workspace: { env: ["GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"], services: ["gmail", "drive", "sheets", "docs", "slides", "calendar", "tasks", "forms"] },
  google_audit: { env: ["GOOGLE_AUDIT_SHEET_ID"], role: "primary_audit_store" },
  google_drive_backup: { env: ["GOOGLE_DRIVE_BACKUP_FOLDER_ID", "COMMAND_CENTER_BACKUP_TOKEN"], role: "backup_store" },
  notion: { env: ["NOTION_API_KEY", "NOTION_PROJECT_PAGE_ID"], role: "project_knowledge" },
  github: { env: ["GITHUB_APP_ID", "GITHUB_APP_PRIVATE_KEY", "GITHUB_APP_INSTALLATION_ID"], role: "source_control_read_only" },
  vercel: { env: ["VERCEL_OIDC_TOKEN"], role: "hosting_and_deployments" },
  telegram: { env: ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "TELEGRAM_WEBHOOK_SECRET"], role: "command_and_notifications" },
  web_research: { env: [], role: "web_search_and_research", note: "Research provider remains disabled until free quota and billing behavior are verified." }
});

function getProviderStatus(env = process.env) {
  return Object.entries(PROVIDERS).map(([id, config]) => ({
    id,
    role: config.role,
    configured: config.env.length > 0 && config.env.every((name) => Boolean(env[name])),
    required_variables: config.env,
    ...(config.free_tier_only ? { free_tier_only: config.free_tier_only } : {}),
    ...(config.free_model_required ? { free_model_required: true } : {}),
    ...(config.paid_disabled_by_default ? { paid_disabled_by_default: true } : {}),
    ...(config.services ? { services: config.services } : {}),
    ...(config.note ? { note: config.note } : {})
  }));
}

module.exports = { PROVIDERS, getProviderStatus };
