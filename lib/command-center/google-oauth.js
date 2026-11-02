"use strict";

const crypto = require("node:crypto");
const CALLBACK_PATH = "/api/command-center/google-oauth-callback";
const COOKIE_MAX_AGE = 600;
const DEFAULT_SCOPES = ["openid", "email", "profile", "https://www.googleapis.com/auth/gmail.compose"];
const ALLOWED_SCOPES = new Set([...DEFAULT_SCOPES]);

function parseCookies(header = "") {
  return Object.fromEntries(String(header).split(";").map((part) => {
    const i = part.indexOf("=");
    if (i < 0) return ["", ""];
    return [part.slice(0, i).trim(), decodeURIComponent(part.slice(i + 1).trim())];
  }).filter(([key]) => key));
}

function cookie(name, value, maxAge) {
  return name + "=" + encodeURIComponent(value) + "; Path=" + CALLBACK_PATH +
    "; Max-Age=" + maxAge + "; HttpOnly; Secure; SameSite=Lax";
}

function getScopes(env = process.env) {
  const raw = env.GOOGLE_OAUTH_SCOPES || DEFAULT_SCOPES.join(" ");
  const scopes = raw.split(/[\s,]+/).filter(Boolean);
  if (!scopes.length || scopes.some((scope) => !/^https:\/\/www\.googleapis\.com\/auth\/[a-zA-Z0-9._-]+$/.test(scope) && !["openid", "email", "profile"].includes(scope))) {
    throw new Error("GOOGLE_OAUTH_SCOPES contains an unsupported scope.");
  }
  return [...new Set(scopes)];
}

function buildAuthorizationUrl({ clientId, redirectUri, state, codeChallenge, scopes }) {
  const url = new URL("https://accounts.google.com/o/oauth2/v2/auth");
  url.search = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: "code",
    scope: scopes.join(" "),
    access_type: "offline",
    prompt: "consent",
    include_granted_scopes: "false",
    state,
    code_challenge: codeChallenge,
    code_challenge_method: "S256"
  }).toString();
  return url.toString();
}

function createOAuthStart(env = process.env) {
  if (!env.GOOGLE_OAUTH_CLIENT_ID) throw new Error("GOOGLE_OAUTH_CLIENT_ID is not configured.");
  if (!env.GOOGLE_OAUTH_REDIRECT_URI) throw new Error("GOOGLE_OAUTH_REDIRECT_URI is not configured.");
  const redirect = new URL(env.GOOGLE_OAUTH_REDIRECT_URI);
  if (redirect.protocol !== "https:" || redirect.pathname !== CALLBACK_PATH || redirect.search || redirect.hash) {
    throw new Error("GOOGLE_OAUTH_REDIRECT_URI must be the exact HTTPS callback URL.");
  }
  const state = crypto.randomBytes(32).toString("base64url");
  const verifier = crypto.randomBytes(48).toString("base64url");
  const challenge = crypto.createHash("sha256").update(verifier).digest("base64url");
  return {
    url: buildAuthorizationUrl({
      clientId: env.GOOGLE_OAUTH_CLIENT_ID,
      redirectUri: redirect.toString(),
      state,
      codeChallenge: challenge,
      scopes: getScopes(env)
    }),
    cookies: [
      cookie("trtt_google_oauth_state", state, COOKIE_MAX_AGE),
      cookie("trtt_google_oauth_verifier", verifier, COOKIE_MAX_AGE)
    ]
  };
}

function takeOAuthCallback(req, env = process.env) {
  const params = new URL(req.url, "https://placeholder.invalid").searchParams;
  const state = params.get("state") || "";
  const code = params.get("code") || "";
  const cookies = parseCookies(req.headers?.cookie || "");
  const expectedState = cookies.trtt_google_oauth_state || "";
  const verifier = cookies.trtt_google_oauth_verifier || "";
  if (!state || !expectedState || !verifier || state.length !== expectedState.length ||
      !crypto.timingSafeEqual(Buffer.from(state), Buffer.from(expectedState))) {
    throw new Error("OAuth state validation failed. Restart the Google connection.");
  }
  if (params.has("error")) throw new Error("Google OAuth consent was not completed.");
  if (!code) throw new Error("Google OAuth callback did not include an authorization code.");
  if (!env.GOOGLE_OAUTH_CLIENT_ID || !env.GOOGLE_OAUTH_CLIENT_SECRET || !env.GOOGLE_OAUTH_REDIRECT_URI) {
    throw new Error("Google OAuth client configuration is incomplete.");
  }
  return { code, verifier, redirectUri: env.GOOGLE_OAUTH_REDIRECT_URI };
}

async function exchangeAuthorizationCode({ code, verifier, redirectUri }, env = process.env) {
  const response = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      code,
      client_id: env.GOOGLE_OAUTH_CLIENT_ID,
      client_secret: env.GOOGLE_OAUTH_CLIENT_SECRET,
      redirect_uri: redirectUri,
      grant_type: "authorization_code",
      code_verifier: verifier
    }),
    signal: AbortSignal.timeout(15000)
  });
  if (!response.ok) throw new Error("Google authorization-code exchange failed (HTTP " + response.status + ").");
  const data = await response.json();
  if (!data.refresh_token) throw new Error("Google returned no refresh token. Revoke the app grant and retry consent with offline access.");
  return { refreshToken: data.refresh_token, scope: data.scope || "", tokenType: data.token_type || "Bearer" };
}

module.exports = { CALLBACK_PATH, cookie, createOAuthStart, takeOAuthCallback, exchangeAuthorizationCode, getScopes };
