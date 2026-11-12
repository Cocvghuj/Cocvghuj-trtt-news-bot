// TRTT Vault Answer Engine API — Gemini + OpenRouter + Groq
// Server-side only: API keys are read from Vercel environment variables.
//
// Environment variables (Vercel -> Settings -> Environment Variables):
//   GEMINI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY      (keys, never put them in code)
//   GEMINI_MODEL      optional, default gemini-3.8-flash
//   OPENROUTER_MODEL  optional, default openai/gpt-5.2
//   GROQ_MODEL        optional, default openai/gpt-oss-120b
//   GROQ_WEB_SEARCH   optional, set to 1 to try Groq's built-in browser_search tool
//   ANSWER_PROVIDERS  optional, order of providers, default gemini,openrouter,groq
//   ANSWER_MODE       optional, "fallback" (default: ask one provider, next only if it fails)
//                     or "all" (ask every provider at once, costs more)
//   EXTRA_ORIGINS     optional, comma separated extra allowed websites
//   GLOBAL_MAX_PER_HOUR optional, safety cap per server instance, default 300

const ALLOWED_ORIGINS = new Set([
  "https://trttnews24bd.blogspot.com",
  "https://trttnews24bd.com",
  "https://www.trttnews24bd.com",
  ...String(process.env.EXTRA_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean)
]);

const WINDOW_MS = 10 * 60 * 1000;
const MAX_REQUESTS = 12;
const GLOBAL_MAX = Number(process.env.GLOBAL_MAX_PER_HOUR || 300);
const TOTAL_BUDGET_MS = 27000;
const requestCounts = new Map();
let globalWindow = { started: 0, count: 0 };

const SYSTEM_PROMPT =
  "You are the TRTT evidence-first answer assistant. Answer in the user's language. " +
  "Prefer primary and official sources. Separate verified facts from uncertainty. " +
  "Never invent citations, prices, schedules, laws, names, statistics, or live status. " +
  "If reliable evidence is unavailable or sources conflict, say so clearly and do not guess. " +
  "Do not claim that a fact is verified merely because you generated it. " +
  "Give a concise useful answer and state dates where relevant.";

function uniqueSources(items) {
  const seen = new Set();
  return (items || []).filter(Boolean).map((item) => {
    const url = String(item.url || item.uri || "").trim();
    if (!/^https:\/\/[^ ]+$/i.test(url) || seen.has(url)) return null;
    let host;
    try { host = new URL(url).hostname; } catch (_) { return null; }
    seen.add(url);
    return { title: String(item.title || item.name || host).slice(0, 180), url };
  }).filter(Boolean).slice(0, 8);
}

function linksFromText(text) {
  const found = [];
  const re = /\[([^\]]{1,160})\]\((https:\/\/[^)\s]+)\)/g;
  let match;
  while ((match = re.exec(text)) !== null) found.push({ title: match[1], url: match[2] });
  return found;
}

function providerErrorText(data, fallback) {
  const raw = data && data.error && data.error.message ? data.error.message : (data && data.message) || fallback;
  return String(raw).slice(0, 220);
}

function redact(message) {
  return String(message || "Request failed")
    .replace(/AIza[0-9A-Za-z_-]{20,}/g, "[redacted]")
    .replace(/sk-or-v1-[0-9a-f]{20,}/gi, "[redacted]")
    .replace(/gsk_[0-9A-Za-z]{20,}/g, "[redacted]")
    .replace(/Bearer\s+[^\s]+/gi, "Bearer [redacted]")
    .slice(0, 260);
}

/* ---------- Provider 1: Gemini (Google Search grounding) ---------- */
async function callGemini(question, timeoutMs) {
  const key = process.env.GEMINI_API_KEY;
  if (!key) throw new Error("Gemini is not configured");
  const model = process.env.GEMINI_MODEL || "gemini-3.8-flash";
  const response = await fetch(
    "https://generativelanguage.googleapis.com/v1beta/models/" + encodeURIComponent(model) + ":generateContent",
    {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": key },
      signal: AbortSignal.timeout(timeoutMs),
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: SYSTEM_PROMPT + " Use Google Search grounding for current or factual claims." }] },
        contents: [{ role: "user", parts: [{ text: question }] }],
        tools: [{ google_search: {} }],
        generationConfig: { maxOutputTokens: 2048 }
      })
    }
  );
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error("HTTP " + response.status + ": " + providerErrorText(data, "Provider returned an error"));
  const candidate = data.candidates && data.candidates[0];
  const answer = candidate && candidate.content && candidate.content.parts
    ? candidate.content.parts.map((part) => part.text || "").join("").trim()
    : "";
  if (!answer) throw new Error("Gemini returned no answer");
  const grounding = candidate.groundingMetadata || {};
  const sources = uniqueSources((grounding.groundingChunks || []).map((chunk) => ({
    title: chunk.web && chunk.web.title,
    url: chunk.web && chunk.web.uri
  })));
  return {
    model: "Gemini (" + model + ")",
    answer: answer.slice(0, 6000),
    sources,
    searchQueries: (grounding.webSearchQueries || []).slice(0, 5),
    grounded: sources.length > 0
  };
}

/* ---------- Provider 2: OpenRouter (openrouter:web_search server tool) ---------- */
async function callOpenRouter(question, timeoutMs) {
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error("OpenRouter is not configured");
  const model = process.env.OPENROUTER_MODEL || "openai/gpt-5.2";
  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + key,
      "Content-Type": "application/json",
      "HTTP-Referer": "https://trttnews24bd.blogspot.com/",
      "X-OpenRouter-Title": "TRTT Vault Evidence Answer Engine"
    },
    signal: AbortSignal.timeout(timeoutMs),
    body: JSON.stringify({
      model,
      messages: [
        { role: "system", content: SYSTEM_PROMPT + " Use the web search tool for factual or current claims and cite source links in markdown." },
        { role: "user", content: question }
      ],
      tools: [{ type: "openrouter:web_search", parameters: { max_results: 5, max_uses: 3 } }],
      max_tool_calls: 3,
      max_completion_tokens: 1500
    })
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error("HTTP " + response.status + ": " + providerErrorText(data, "Provider returned an error"));
  const message = data.choices && data.choices[0] && data.choices[0].message;
  const answer = message && typeof message.content === "string" ? message.content.trim() : "";
  if (!answer) throw new Error("OpenRouter returned no answer");
  const annotated = (message.annotations || []).map((annotation) => ({
    title: annotation.url_citation && annotation.url_citation.title,
    url: annotation.url_citation && annotation.url_citation.url
  }));
  const sources = uniqueSources([...(data.citations || []).map((url) => ({ url })), ...annotated, ...linksFromText(answer)]);
  return {
    model: String(data.model || model),
    answer: answer.slice(0, 6000),
    sources,
    grounded: sources.length > 0
  };
}

/* ---------- Provider 3: Groq (very fast; web search only if enabled) ---------- */
async function callGroq(question, timeoutMs) {
  const key = process.env.GROQ_API_KEY;
  if (!key) throw new Error("Groq is not configured");
  const model = process.env.GROQ_MODEL || "openai/gpt-oss-120b";
  const useSearch = process.env.GROQ_WEB_SEARCH === "1";
  const system = useSearch
    ? SYSTEM_PROMPT + " Use the browser search tool for current or factual claims and cite source links in markdown."
    : SYSTEM_PROMPT + " You have NO live web access in this request. Do not present current prices, schedules, laws or live status as verified; say you cannot verify them and suggest checking the official provider.";
  const body = {
    model,
    messages: [{ role: "system", content: system }, { role: "user", content: question }],
    max_completion_tokens: 2000,
    temperature: 0.3
  };
  if (useSearch) body.tools = [{ type: "browser_search" }];
  const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
    method: "POST",
    headers: { "Authorization": "Bearer " + key, "Content-Type": "application/json" },
    signal: AbortSignal.timeout(timeoutMs),
    body: JSON.stringify(body)
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error("HTTP " + response.status + ": " + providerErrorText(data, "Provider returned an error"));
  const message = data.choices && data.choices[0] && data.choices[0].message;
  const answer = message && typeof message.content === "string" ? message.content.trim() : "";
  if (!answer) throw new Error("Groq returned no answer");
  const sources = uniqueSources(linksFromText(answer));
  return {
    model: "Groq (" + model + ")",
    answer: answer.slice(0, 6000),
    sources,
    grounded: sources.length > 0,
    webSearch: useSearch
  };
}

const PROVIDERS = {
  gemini: { label: "Gemini", call: callGemini },
  openrouter: { label: "OpenRouter", call: callOpenRouter },
  groq: { label: "Groq", call: callGroq }
};

function allowRequest(ip, weight) {
  const now = Date.now();
  if (now - globalWindow.started >= 3600000) globalWindow = { started: now, count: 0 };
  if (globalWindow.count + weight > GLOBAL_MAX) return false;
  const previous = requestCounts.get(ip);
  if (previous && now - previous.started < WINDOW_MS) {
    if (previous.count + weight > MAX_REQUESTS) return false;
    previous.count += weight;
  } else {
    requestCounts.set(ip, { started: now, count: weight });
  }
  globalWindow.count += weight;
  if (requestCounts.size > 500) {
    for (const [key, value] of requestCounts) if (now - value.started >= WINDOW_MS) requestCounts.delete(key);
  }
  return true;
}

module.exports = async function handler(req, res) {
  const origin = String(req.headers.origin || "");
  res.setHeader("Vary", "Origin");
  if (!ALLOWED_ORIGINS.has(origin)) {
    return res.status(403).json({ ok: false, error: "This origin is not allowed." });
  }
  res.setHeader("Access-Control-Allow-Origin", origin);
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", "no-store");

  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ ok: false, error: "Use POST." });

  const order = String(process.env.ANSWER_PROVIDERS || "gemini,openrouter,groq")
    .split(",").map((s) => s.trim()).filter((name) => PROVIDERS[name]);
  const mode = process.env.ANSWER_MODE === "all" ? "all" : "fallback";

  const ip = String(req.headers["x-real-ip"] || req.headers["x-forwarded-for"] || "unknown").split(",")[0].trim();
  if (!allowRequest(ip, mode === "all" ? Math.max(order.length, 1) : 1)) {
    return res.status(429).json({ ok: false, error: "Too many questions. Please wait a few minutes." });
  }

  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch (_) { body = {}; }
  }
  const question = String((body && body.question) || "").trim();
  if (!question) return res.status(400).json({ ok: false, error: "Please enter a question." });
  if (question.length > 2000) return res.status(413).json({ ok: false, error: "Question is too long (maximum 2,000 characters)." });

  const started = Date.now();
  const timeLeft = () => TOTAL_BUDGET_MS - (Date.now() - started);
  const results = { gemini: null, openrouter: null, groq: null };
  const errors = { gemini: null, openrouter: null, groq: null };

  async function run(name) {
    try {
      results[name] = await PROVIDERS[name].call(question, Math.min(20000, Math.max(3000, timeLeft())));
    } catch (reason) {
      console.error("Answer Engine " + name + " failed:", redact(reason && reason.message));
      errors[name] = PROVIDERS[name].label + ": temporarily unavailable";
    }
  }

  if (mode === "all") {
    await Promise.all(order.map(run));
  } else {
    for (const name of order) {
      if (timeLeft() < 4000) break;
      await run(name);
      if (results[name]) break;
    }
  }

  if (!order.some((name) => results[name])) {
    return res.status(502).json({ ok: false, error: "The AI providers are unavailable right now. Please try again later.", errors });
  }
  return res.status(200).json({
    ok: true,
    mode,
    results,
    errors,
    note: "AI output can still be wrong. Check the linked sources, especially for legal, medical, financial, travel and other high-impact decisions. Do not enter passport, booking or other personal details."
  });
};

module.exports.config = { maxDuration: 30 };
