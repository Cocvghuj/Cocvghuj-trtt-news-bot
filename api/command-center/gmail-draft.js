"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { appendAuditEvent } = require("../../lib/command-center/audit");
const { createGmailDraft } = require("../../lib/command-center/google-services");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed." });
  const auth = authorize(req);
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  const body = typeof req.body === "string" ? (() => { try { return JSON.parse(req.body); } catch { return {}; } })() : (req.body || {});
  let draft = null;
  try {
    await appendAuditEvent({ action: "gmail.draft_requested", resource: "Gmail", status: "requested", summary: "Owner requested a draft; message content is not logged." });
    draft = await createGmailDraft(body);
    try {
      await appendAuditEvent({ action: "gmail.draft_created", resource: draft.id || "Gmail draft", status: "completed", summary: "Gmail draft created; not sent." });
      return res.status(201).json({ created: true, sent: false, audit_recorded: true, draft_id: draft.id });
    } catch {
      return res.status(202).json({ created: true, sent: false, audit_recorded: false, audit_status: "pending", draft_id: draft.id });
    }
  } catch (error) {
    return res.status(503).json({ created: Boolean(draft), sent: false, draft_id: draft?.id, error: String(error.message || "Gmail draft operation failed") });
  }
};
