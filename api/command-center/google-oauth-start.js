"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { createOAuthStart } = require("../../lib/command-center/google-oauth");

module.exports = function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed." });
  const auth = authorize(req);
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  try {
    const result = createOAuthStart();
    res.setHeader("Cache-Control", "no-store, max-age=0");
    res.setHeader("Pragma", "no-cache");
    res.setHeader("Set-Cookie", result.cookies);
    return res.status(200).json({ authorization_url: result.url, expires_in_seconds: 600, note: "Open this URL in the same browser to complete owner consent. The callback displays the refresh token once for manual storage in Vercel; never paste it into chat or GitHub." });
  } catch (error) {
    return res.status(503).json({ error: error.message });
  }
};
