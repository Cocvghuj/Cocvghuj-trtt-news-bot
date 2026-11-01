"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const { createOAuthStart, takeOAuthCallback, getScopes, CALLBACK_PATH } = require("../lib/command-center/google-oauth");

const env = {
  GOOGLE_OAUTH_CLIENT_ID: "client-id.apps.googleusercontent.com",
  GOOGLE_OAUTH_CLIENT_SECRET: "test-client-secret",
  GOOGLE_OAUTH_REDIRECT_URI: "https://preview.example.com" + CALLBACK_PATH,
  GOOGLE_OAUTH_SCOPES: "openid email https://www.googleapis.com/auth/gmail.compose"
};

test("Google OAuth start uses offline access, explicit consent and PKCE S256", () => {
  const result = createOAuthStart(env);
  const url = new URL(result.url);
  assert.equal(url.origin, "https://accounts.google.com");
  assert.equal(url.searchParams.get("access_type"), "offline");
  assert.equal(url.searchParams.get("prompt"), "consent");
  assert.equal(url.searchParams.get("code_challenge_method"), "S256");
  assert.equal(url.searchParams.get("redirect_uri"), env.GOOGLE_OAUTH_REDIRECT_URI);
  assert.equal(result.cookies.length, 2);
  assert.match(result.cookies[0], /HttpOnly; Secure; SameSite=Lax/);
});

test("Google OAuth callback rejects missing or mismatched state", () => {
  const state = "a".repeat(40);
  const verifier = crypto.randomBytes(48).toString("base64url");
  const req = { url: "/api/command-center/google-oauth-callback?code=abc&state=" + state, headers: { cookie: "trtt_google_oauth_state=wrong; trtt_google_oauth_verifier=" + verifier } };
  assert.throws(() => takeOAuthCallback(req, env), /state validation failed/);
});

test("Google OAuth callback accepts matching state cookie and returns PKCE verifier", () => {
  const state = crypto.randomBytes(32).toString("base64url");
  const verifier = crypto.randomBytes(48).toString("base64url");
  const req = { url: "/api/command-center/google-oauth-callback?code=auth-code&state=" + state, headers: { cookie: "trtt_google_oauth_state=" + state + "; trtt_google_oauth_verifier=" + verifier } };
  const pending = takeOAuthCallback(req, env);
  assert.equal(pending.code, "auth-code");
  assert.equal(pending.verifier, verifier);
  assert.equal(pending.redirectUri, env.GOOGLE_OAUTH_REDIRECT_URI);
});

test("Google OAuth scopes reject non-Google scope URLs", () => {
  assert.throws(() => getScopes({ GOOGLE_OAUTH_SCOPES: "https://evil.example/scope" }), /unsupported scope/);
});
