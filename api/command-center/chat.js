"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { generateAnswer } = require("../../lib/command-center/ai-router");
const { appendAuditEvent } = require("../../lib/command-center/audit");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed." });
  const auth = authorize(req);
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  const body = typeof req.body === "string" ? (() => { try { return JSON.parse(req.body); } catch { return {}; } })() : (req.body || {});
  if (JSON.stringify(body).length > 8192) return res.status(413).json({ error: "Request too large." });
  try {
    const result = await generateAnswer(body.prompt);
    // The chat endpoint never reports a durable success unless the audit ledger is configured.
    await appendAuditEvent({
      action: "ai.request",
      resource: result.provider + "/" + result.model,
      status: "completed",
      summary: "AI request completed; prompt content is intentionally not stored."
    });
    res.setHeader("Cache-Control", "no-store");
    return res.status(200).json(result);
  } catch (error) {
    const message = String(error.message || "Request failed");
    const status = message.includes("not configured") || message.includes("not configured.") || message.includes("audit spreadsheet") ? 503 : 502;
    return res.status(status).json({ error: message });
  }
};