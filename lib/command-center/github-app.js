"use strict";
const crypto = require("node:crypto");

function b64url(value) {
  return Buffer.from(value).toString("base64url");
}

function createAppJwt(env = process.env, nowSeconds = Math.floor(Date.now() / 1000)) {
  if (!env.GITHUB_APP_ID || !env.GITHUB_APP_PRIVATE_KEY) throw new Error("GitHub App credentials are not configured.");
  const header = b64url(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const payload = b64url(JSON.stringify({ iat: nowSeconds - 60, exp: nowSeconds + 540, iss: env.GITHUB_APP_ID }));
  const unsigned = header + "." + payload;
  const privateKey = String(env.GITHUB_APP_PRIVATE_KEY).replace(/\\n/g, "\n");
  const signature = crypto.sign("RSA-SHA256", Buffer.from(unsigned), privateKey).toString("base64url");
  return unsigned + "." + signature;
}

async function getInstallationToken(env = process.env) {
  if (!env.GITHUB_APP_INSTALLATION_ID) throw new Error("GitHub App installation ID is not configured.");
  const jwt = createAppJwt(env);
  const response = await fetch("https://api.github.com/app/installations/" + encodeURIComponent(env.GITHUB_APP_INSTALLATION_ID) + "/access_tokens", {
    method: "POST",
    headers: { Authorization: "Bearer " + jwt, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" },
    signal: AbortSignal.timeout(15000)
  });
  if (!response.ok) throw new Error("GitHub App installation token request failed (HTTP " + response.status + ").");
  const data = await response.json();
  if (!data.token) throw new Error("GitHub App returned no installation token.");
  return data.token;
}

async function getRepositoryMetadata(repositoryFullName, env = process.env) {
  if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repositoryFullName || "")) throw new Error("Repository must use owner/name format.");
  const token = await getInstallationToken(env);
  const response = await fetch("https://api.github.com/repos/" + repositoryFullName, {
    headers: { Authorization: "Bearer " + token, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" },
    signal: AbortSignal.timeout(15000)
  });
  if (!response.ok) throw new Error("GitHub repository read failed (HTTP " + response.status + ").");
  const data = await response.json();
  return { full_name: data.full_name, default_branch: data.default_branch, private: data.private, html_url: data.html_url };
}

module.exports = { createAppJwt, getInstallationToken, getRepositoryMetadata };