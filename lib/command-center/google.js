"use strict";

async function getGoogleAccessToken(env = process.env) {
  const required = ["GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"];
  const missing = required.filter((name) => !env[name]);
  if (missing.length) throw new Error("Google OAuth is not configured: " + missing.join(", "));
  const response = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_OAUTH_CLIENT_ID,
      client_secret: env.GOOGLE_OAUTH_CLIENT_SECRET,
      refresh_token: env.GOOGLE_REFRESH_TOKEN,
      grant_type: "refresh_token"
    }),
    signal: AbortSignal.timeout(15000)
  });
  if (!response.ok) throw new Error("Google OAuth token refresh failed (HTTP " + response.status + ").");
  const data = await response.json();
  if (!data.access_token) throw new Error("Google OAuth returned no access token.");
  return data.access_token;
}

async function googleApi(url, options = {}, env = process.env) {
  const token = await getGoogleAccessToken(env);
  const response = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: "Bearer " + token
    },
    signal: options.signal || AbortSignal.timeout(20000)
  });
  if (!response.ok) throw new Error("Google API request failed (HTTP " + response.status + ").");
  if (response.status === 204) return null;
  return response.json();
}

module.exports = { getGoogleAccessToken, googleApi };