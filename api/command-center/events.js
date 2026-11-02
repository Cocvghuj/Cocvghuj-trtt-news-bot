"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { appendAuditEvent } = require("../../lib/command-center/audit");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed." });
  const auth = authorize(req);
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  const body = typeof req.body === "string" ? (() => { try { return JSON.parse(req.body); } catch { return {}; } })() : (req.body || {});
  if (JSON.stringify(body).length > 4096) return res.status(413).json({ error: "Request too large." });
  try {
    const event = await appendAuditEvent(body);
    return res.status(201).json({ saved: true, event_id: event.event_id, occurred_at: event.occurred_at });
  } catch (error) {
    return res.status(503).json({ saved: false, error: String(error.message || "Audit storage unavailable") });
  }
};