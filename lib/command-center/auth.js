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
  if (!expected) return { ok: false, status: 503, error: "Command Center access is not configured." };
  const header = req.headers?.authorization || req.headers?.Authorization || "";
  const supplied = typeof header === "string" && header.startsWith("Bearer ") ? header.slice(7).trim() : "";
  if (!safeEqual(supplied, expected)) return { ok: false, status: 401, error: "Unauthorized." };
  return { ok: true };
}

module.exports = { safeEqual, authorize };