"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { appendAuditEvent } = require("../../lib/command-center/audit");
const { getRepositoryMetadata } = require("../../lib/command-center/github-app");

module.exports = async function handler(req, res) {
  if (req.method !== "GET") return res.status(405).json({ error: "Method not allowed." });
  const auth = authorize(req);
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  try {
    const url = new URL(req.url, "https://command-center.local");
    const repository = url.searchParams.get("repository") || "Cocvghuj/Cocvghuj-trtt-news-bot";
    await appendAuditEvent({ action: "github.read", resource: repository, status: "requested", summary: "Read-only GitHub repository metadata requested." });
    const data = await getRepositoryMetadata(repository);
    await appendAuditEvent({ action: "github.read", resource: repository, status: "completed", summary: "GitHub repository metadata retrieved." });
    return res.status(200).json(data);
  } catch (error) {
    return res.status(503).json({ error: String(error.message || "GitHub read unavailable") });
  }
};