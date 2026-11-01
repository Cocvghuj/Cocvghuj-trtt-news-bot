"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { appendAuditEvent } = require("../../lib/command-center/audit");
const { appendNotionNote } = require("../../lib/command-center/notion");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed." });
  const auth = authorize(req);
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  const body = typeof req.body === "string" ? (() => { try { return JSON.parse(req.body); } catch { return {}; } })() : (req.body || {});
  if (body.owner_approved !== true) return res.status(403).json({ error: "Explicit owner approval is required to write a Notion note." });
  let result = null;
  try {
    await appendAuditEvent({ action: "notion.note_requested", resource: "TRTT project page", status: "approved", summary: "Owner approved a Notion note; content is not copied into the audit ledger." });
    result = await appendNotionNote(body.content);
    try {
      await appendAuditEvent({ action: "notion.note_created", resource: "TRTT project page", status: "completed", summary: "Approved note appended to the Notion project page." });
      return res.status(201).json({ saved: true, audit_recorded: true, blocks: result.results?.length || 0 });
    } catch {
      return res.status(202).json({ saved: true, audit_recorded: false, audit_status: "pending", blocks: result.results?.length || 0 });
    }
  } catch (error) {
    return res.status(503).json({ saved: Boolean(result), error: String(error.message || "Notion write unavailable") });
  }
};
