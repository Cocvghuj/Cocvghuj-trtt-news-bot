"use strict";

async function readJson(response, provider) {
  let data;
  try { data = await response.json(); } catch { throw new Error(provider + " returned invalid JSON."); }
  if (!response.ok) throw new Error(provider + " request failed (HTTP " + response.status + ").");
  return data;
}

async function callGemini(prompt, env) {
  if (!env.GEMINI_API_KEY) throw new Error("Gemini is not configured.");
  const model = env.GEMINI_MODEL || "gemini-2.5-flash";
  const response = await fetch("https://generativelanguage.googleapis.com/v1beta/models/" + encodeURIComponent(model) + ":generateContent", {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": env.GEMINI_API_KEY },
    body: JSON.stringify({ contents: [{ role: "user", parts: [{ text: prompt }] }] }),
    signal: AbortSignal.timeout(25000)
  });
  const data = await readJson(response, "Gemini");
  const text = (data.candidates?.[0]?.content?.parts || []).map((part) => part.text || "").join("\n").trim();
  if (!text) throw new Error("Gemini returned no text.");
  return { provider: "gemini", model, text };
}

async function callOpenRouter(prompt, env) {
  if (!env.OPENROUTER_API_KEY || !env.OPENROUTER_MODEL) throw new Error("OpenRouter is not configured.");
  const model = env.OPENROUTER_MODEL;
  if (!model.endsWith(":free") && env.ALLOW_PAID_AI !== "true") {
    throw new Error("OpenRouter paid models are disabled by default.");
  }
  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: { "Authorization": "Bearer " + env.OPENROUTER_API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({ model, messages: [{ role: "user", content: prompt }], max_tokens: 1200 }),
    signal: AbortSignal.timeout(25000)
  });
  const data = await readJson(response, "OpenRouter");
  const text = data.choices?.[0]?.message?.content;
  if (typeof text !== "string" || !text.trim()) throw new Error("OpenRouter returned no text.");
  return { provider: "openrouter", model, text: text.trim() };
}

async function callOpenAI(prompt, env) {
  if (env.ALLOW_PAID_AI !== "true") throw new Error("Paid AI usage is disabled.");
  if (!env.OPENAI_API_KEY) throw new Error("OpenAI API is not configured.");
  const model = env.OPENAI_MODEL || "gpt-4.1-mini";
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: { "Authorization": "Bearer " + env.OPENAI_API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({ model, messages: [{ role: "user", content: prompt }], max_tokens: 1200 }),
    signal: AbortSignal.timeout(25000)
  });
  const data = await readJson(response, "OpenAI");
  const text = data.choices?.[0]?.message?.content;
  if (typeof text !== "string" || !text.trim()) throw new Error("OpenAI returned no text.");
  return { provider: "openai", model, text: text.trim() };
}

async function generateAnswer(prompt, env = process.env) {
  if (typeof prompt !== "string" || !prompt.trim() || prompt.length > 4000) {
    throw new Error("Prompt must contain 1–4000 characters.");
  }
  const attempts = [() => callGemini(prompt, env), () => callOpenRouter(prompt, env)];
  if (env.ALLOW_PAID_AI === "true") attempts.push(() => callOpenAI(prompt, env));
  const failures = [];
  for (const attempt of attempts) {
    try { return await attempt(); }
    catch (error) { failures.push(String(error.message || "Provider error")); }
  }
  throw new Error("No permitted AI provider succeeded: " + failures.join("; "));
}

module.exports = { generateAnswer, callGemini, callOpenRouter, callOpenAI };