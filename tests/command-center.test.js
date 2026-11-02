"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { safeEqual, authorize } = require("../lib/command-center/auth");
const { decisionFor } = require("../lib/command-center/policy");
const { getProviderStatus } = require("../lib/command-center/providers");
const { normalizeEvent, clean } = require("../lib/command-center/audit");
const { generateAnswer } = require("../lib/command-center/ai-router");

test("access token comparison rejects missing and unequal tokens", () => {
  assert.equal(safeEqual("", "secret"), false);
  assert.equal(safeEqual("secret", "other"), false);
  assert.equal(safeEqual("secret", "secret"), true);
});

test("API authorization fails closed when access token is not configured", () => {
  const result = authorize({ headers: {} }, "TRTT_TEST_TOKEN_NOT_CONFIGURED_2026");
  assert.equal(result.ok, false);
  assert.equal(result.status, 503);
});

test("API authorization trims configured token boundary whitespace", () => {
  const name = "TRTT_TEST_COMMAND_CENTER_TOKEN";
  const previous = process.env[name];
  process.env[name] = "  owner-token\n";
  try {
    const result = authorize({ headers: { authorization: "Bearer owner-token" } }, name);
    assert.equal(result.ok, true);
    assert.equal(authorize({ headers: { authorization: "Bearer wrong" } }, name).ok, false);
  } finally {
    if (previous === undefined) delete process.env[name];
    else process.env[name] = previous;
  }
});

test("blocked publishing and paid usage cannot be approved through the generic policy", () => {
  assert.equal(decisionFor("blogger_draft_publish", true).allowed, false);
  assert.equal(decisionFor("blogger_workflow", true).allowed, false);
  assert.equal(decisionFor("execute_main_py", true).allowed, false);
  assert.equal(decisionFor("paid_api_usage", true).allowed, false);
});

test("external writes require owner approval", () => {
  assert.equal(decisionFor("send_email", false).allowed, false);
  assert.equal(decisionFor("send_email", true).allowed, true);
  assert.equal(decisionFor("create_calendar_event", false).allowed, false);
});

test("provider readiness reports presence only and never returns secret values", () => {
  const status = getProviderStatus({ GEMINI_API_KEY: "test-secret", GEMINI_FREE_TIER_CONFIRMED: "true", OPENROUTER_API_KEY: "another-secret", OPENROUTER_MODEL: "model:free" });
  assert.equal(status.find((p) => p.id === "gemini").configured, true);
  assert.equal(status.find((p) => p.id === "openrouter").configured, true);
  assert.equal(JSON.stringify(status).includes("test-secret"), false);
  assert.equal(JSON.stringify(status).includes("another-secret"), false);
});

test("audit events accept only known actions and redact secret-like strings", () => {
  const event = normalizeEvent({ action: "ai.request", resource: "model", summary: "key sk-or-v1-12345678901234567890 must be hidden" });
  assert.ok(event.event_id);
  assert.equal(event.actor, "owner");
  assert.match(event.summary, /REDACTED/);
  assert.throws(() => normalizeEvent({ action: "unknown.action" }), /Unsupported/);
  assert.equal(clean("Bearer super-secret"), "Bearer [REDACTED]");
});

test("paid OpenRouter models are rejected unless paid usage is explicitly enabled", async () => {
  await assert.rejects(
    () => generateAnswer("hello", { OPENROUTER_API_KEY: "test", OPENROUTER_MODEL: "provider/paid-model" }),
    /No permitted AI provider succeeded/
  );
});

test("OpenAI API is not called when paid usage is disabled", async () => {
  await assert.rejects(
    () => generateAnswer("hello", { OPENAI_API_KEY: "test", ALLOW_PAID_AI: "false" }),
    /No permitted AI provider succeeded/
  );
});

test("AI router validates prompt size before contacting providers", async () => {
  await assert.rejects(() => generateAnswer("x".repeat(4001), {}), /1–4000/);
});

test("public browser AI client contains no provider API key or direct provider endpoint", () => {
  const fs = require("node:fs");
  const path = require("node:path");
  const source = fs.readFileSync(path.join(__dirname, "..", "ai.js"), "utf8");
  assert.doesNotMatch(source, /sk-or-v1-[A-Za-z0-9]+/);
  assert.doesNotMatch(source, /api\.openrouter\.ai/);
  assert.match(source, /\/api\/command-center\/chat/);
});
