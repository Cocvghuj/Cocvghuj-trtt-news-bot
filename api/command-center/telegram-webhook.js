"use strict";
const { verifyTelegramWebhook, sendTelegramMessage } = require("../../lib/command-center/telegram");
const { generateAnswer } = require("../../lib/command-center/ai-router");
const { appendAuditEvent } = require("../../lib/command-center/audit");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed." });
  if (!verifyTelegramWebhook(req)) return res.status(401).json({ error: "Invalid Telegram webhook secret." });
  const update = typeof req.body === "string" ? (() => { try { return JSON.parse(req.body); } catch { return {}; } })() : (req.body || {});
  const message = update.message || update.edited_message;
  const chatId = String(message?.chat?.id || "");
  if (!message?.text || !process.env.TELEGRAM_CHAT_ID || chatId !== String(process.env.TELEGRAM_CHAT_ID)) {
    return res.status(200).json({ ignored: true });
  }
  try {
    const result = await generateAnswer(message.text);
    await appendAuditEvent({ action: "telegram.ai_reply", resource: result.provider + "/" + result.model, status: "completed", summary: "Owner-only Telegram AI reply; message text is not stored." });
    await sendTelegramMessage(result.text, process.env, chatId);
    return res.status(200).json({ replied: true });
  } catch (error) {
    return res.status(503).json({ replied: false, error: String(error.message || "Telegram request not completed") });
  }
};
