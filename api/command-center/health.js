"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { getProviderStatus } = require("../../lib/command-center/providers");

module.exports = function handler(req, res) {
  if (req.method !== "GET") return res.status(405).json({ error: "Method not allowed." });
  const auth = authorize(req);
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  res.setHeader("Cache-Control", "no-store");
  return res.status(200).json({
    service: "TRTT AI Command Center",
    status: "scaffolded",
    providers: getProviderStatus(),
    note: "Configured means environment variables exist; it does not prove external OAuth consent or API access."
  });
};