"use strict";
const crypto = require("node:crypto");
const { googleApi } = require("./google");

function clean(value, max = 240) {
  return String(value || "")
    .replace(/(?:sk-or-v1-|sk-|AIza)[A-Za-z0-9_\-]{12,}/g, "[REDACTED]")
    .replace(/Bearer\s+\S+/gi, "Bearer [REDACTED]")
    .replace(/[\r\n\t]+/g, " ")
    .slice(0, max);
}

function normalizeEvent(input = {}) {
  const allowedActions = new Set(["ai.request", "integration.check", "backup.created", "gmail.draft_created", "calendar.event_created", "github.change", "vercel.deployment"]);
  if (!allowedActions.has(input.action)) throw new Error("Unsupported audit action.");
  return {
    event_id: crypto.randomUUID(),
    occurred_at: new Date().toISOString(),
    actor: "owner",
    action: input.action,
    resource: clean(input.resource, 160),
    status: clean(input.status || "completed", 40),
    summary: clean(input.summary, 500),
    correlation_id: clean(input.correlation_id || "", 100)
  };
}

async function appendAuditEvent(input, env = process.env) {
  if (!env.GOOGLE_AUDIT_SHEET_ID) throw new Error("Google audit spreadsheet is not configured.");
  const event = normalizeEvent(input);
  const spreadsheetId = encodeURIComponent(env.GOOGLE_AUDIT_SHEET_ID);
  const url = "https://sheets.googleapis.com/v4/spreadsheets/" + spreadsheetId +
    "/values/Audit%21A:H:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS";
  await googleApi(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ values: [[event.event_id, event.occurred_at, event.actor, event.action, event.resource, event.status, event.summary, event.correlation_id]] })
  }, env);
  return event;
}

async function createDriveBackup(env = process.env) {
  if (!env.GOOGLE_AUDIT_SHEET_ID || !env.GOOGLE_DRIVE_BACKUP_FOLDER_ID) {
    throw new Error("Google Sheets audit and Drive backup must both be configured.");
  }
  const sheetId = encodeURIComponent(env.GOOGLE_AUDIT_SHEET_ID);
  const data = await googleApi("https://sheets.googleapis.com/v4/spreadsheets/" + sheetId + "/values/Audit%21A:H", {}, env);
  const boundary = "trtt_" + crypto.randomUUID().replace(/-/g, "");
  const filename = "trtt-command-center-audit-" + new Date().toISOString().replace(/[:.]/g, "-") + ".json";
  const metadata = { name: filename, mimeType: "application/json", parents: [env.GOOGLE_DRIVE_BACKUP_FOLDER_ID] };
  const body = [
    "--" + boundary,
    "Content-Type: application/json; charset=UTF-8",
    "",
    JSON.stringify(metadata),
    "--" + boundary,
    "Content-Type: application/json",
    "",
    JSON.stringify({ exported_at: new Date().toISOString(), spreadsheet_id: env.GOOGLE_AUDIT_SHEET_ID, rows: data.values || [] }),
    "--" + boundary + "--",
    ""
  ].join("\r\n");
  return googleApi("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name", {
    method: "POST",
    headers: { "Content-Type": "multipart/related; boundary=" + boundary },
    body
  }, env);
}

module.exports = { clean, normalizeEvent, appendAuditEvent, createDriveBackup };