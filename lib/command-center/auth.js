"use strict";
const crypto = require("node:crypto");

function safeEqual(left, right) {
  if (typeof left !== "string" || typeof right !== "string" || !left || !right) return false;
  const a = Buffer.from(left, "utf8");
  const b = Buffer.from(right, "utf8");
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

function authorize(req, envName = "COMMAND_CENTER_ACCESS_TOKEN") {
  const expected = process.env[envName];
  if (typeof expected !== "string" || !expected.trim()) {
    return { ok: false, status: 503, error: "Command Center access is not configured.", diagnostic: "TOKEN_NOT_CONFIGURED" };
  }
  const header = req.headers?.authorization || req.headers?.Authorization || "";
  if (typeof header !== "string" || !header.startsWith("Bearer ")) {
    return { ok: false, status: 401, error: "Unauthorized.", diagnostic: "BEARER_HEADER_MISSING_OR_INVALID" };
  }
  const supplied = header.slice(7).trim();
  if (!supplied) {
    return { ok: false, status: 401, error: "Unauthorized.", diagnostic: "BEARER_TOKEN_EMPTY" };
  }
  if (expected !== expected.trim()) {
    return { ok: false, status: 401, error: "Unauthorized.", diagnostic: "CONFIGURED_TOKEN_HAS_OUTER_WHITESPACE" };
  }
  if (!safeEqual(supplied, expected)) {
    return { ok: false, status: 401, error: "Unauthorized.", diagnostic: "TOKEN_MISMATCH" };
  }
  return { ok: true };
}

module.exports = { safeEqual, authorize };
