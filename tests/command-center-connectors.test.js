"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { validateGmailDraft, validateCalendarEvent } = require("../lib/command-center/google-services");
const { appendNotionNote } = require("../lib/command-center/notion");
const { createAppJwt } = require("../lib/command-center/github-app");
const { verifyTelegramWebhook } = require("../lib/command-center/telegram");
const { getGoogleAccessToken } = require("../lib/command-center/google");

test("Gmail draft validation accepts a safe draft and rejects invalid addresses", () => {
  assert.equal(validateGmailDraft({ to: "owner@example.com", subject: "Test", body: "Draft only" }).to, "owner@example.com");
  assert.throws(() => validateGmailDraft({ to: "not-an-email", subject: "Test", body: "Draft only" }), /valid recipient/);
});

test("Calendar event validation requires a valid increasing time range", () => {
  assert.equal(validateCalendarEvent({ summary: "Review", start: { dateTime: "2026-11-02T10:00:00Z" }, end: { dateTime: "2026-11-02T11:00:00Z" } }).summary, "Review");
  assert.throws(() => validateCalendarEvent({ summary: "Bad", start: { dateTime: "2026-11-02T11:00:00Z" }, end: { dateTime: "2026-11-02T10:00:00Z" } }), /after start/);
});

test("Notion writes fail closed when no integration consent is configured", async () => {
  await assert.rejects(() => appendNotionNote("test", {}), /Notion integration token/);
});

test("GitHub App JWT creation fails closed without an installed app", () => {
  assert.throws(() => createAppJwt({}), /GitHub App credentials/);
});

test("Telegram webhook verification requires the configured secret", () => {
  assert.equal(verifyTelegramWebhook({ headers: { "x-telegram-bot-api-secret-token": "wrong" } }, { TELEGRAM_WEBHOOK_SECRET: "right" }), false);
  assert.equal(verifyTelegramWebhook({ headers: { "x-telegram-bot-api-secret-token": "right" } }, { TELEGRAM_WEBHOOK_SECRET: "right" }), true);
});

test("Google OAuth token refresh fails closed before any network call without consent", async () => {
  await assert.rejects(() => getGoogleAccessToken({}), /Google OAuth is not configured/);
});
