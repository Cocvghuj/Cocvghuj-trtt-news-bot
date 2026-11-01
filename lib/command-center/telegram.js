"use strict";
const { safeEqual } = require("./auth");

function verifyTelegramWebhook(req, env = process.env) {
  const expected = env.TELEGRAM_WEBHOOK_SECRET;
  const supplied = req.headers?.["x-telegram-bot-api-secret-token"] || "";
  return Boolean(expected && safeEqual(String(supplied), expected));
}

async function sendTelegramMessage(text, env = process.env, chatId = env.TELEGRAM_CHAT_ID) {
  if (!env.TELEGRAM_BOT_TOKEN || !chatId) throw new Error("Telegram bot token or owner chat ID is not configured.");
  const response = await fetch("https://api.telegram.org/bot" + env.TELEGRAM_BOT_TOKEN + "/sendMessage", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text: String(text || "").slice(0, 3900), disable_web_page_preview: true }),
    signal: AbortSignal.timeout(15000)
  });
  const data = await response.json();
  if (!response.ok || data.ok !== true) throw new Error("Telegram message delivery failed.");
  return { message_id: data.result?.message_id, chat_id: data.result?.chat?.id };
}

module.exports = { verifyTelegramWebhook, sendTelegramMessage };