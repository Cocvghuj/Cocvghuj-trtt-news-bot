"use strict";
const { cookie, takeOAuthCallback, exchangeAuthorizationCode } = require("../../lib/command-center/google-oauth");

module.exports = async function handler(req, res) {
  if (req.method !== "GET") return res.status(405).send("Method not allowed.");
  res.setHeader("Cache-Control", "no-store, max-age=0");
  res.setHeader("Pragma", "no-cache");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'");
  const clear = [
    cookie("trtt_google_oauth_state", "", 0),
    cookie("trtt_google_oauth_verifier", "", 0)
  ];
  try {
    const pending = takeOAuthCallback(req);
    const result = await exchangeAuthorizationCode(pending);
    res.setHeader("Set-Cookie", clear);
    return res.status(200).json({
      connected: true,
      refresh_token: result.refreshToken,
      granted_scopes: result.scope,
      next_step: "Copy refresh_token directly into the Vercel Preview environment variable GOOGLE_REFRESH_TOKEN, then remove this response from browser history. Do not send it to ChatGPT, email, or GitHub."
    });
  } catch (error) {
    res.setHeader("Set-Cookie", clear);
    return res.status(400).json({ connected: false, error: error.message });
  }
};
