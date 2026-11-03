// TRTT Vault Answer Engine API
// Server-side only: API keys are read from Vercel environment variables.
const ALLOWED_ORIGINS = new Set([
  "https://trttnews24bd.blogspot.com",
  "https://trttnews24bd.com",
  "https://www.trttnews24bd.com"
]);
const WINDOW_MS = 10 * 60 * 1000;
const MAX_REQUESTS = 12;
const requestCounts = new Map();

function uniqueSources(items) {
  const seen = new Set();
  return (items || []).filter(Boolean).map((item) => {
    const url = String(item.url || item.uri || "").trim();
    if (!/^https:\/\/[^ ]+$/i.test(url) || seen.has(url)) return null;
    seen.add(url);
    return { title: String(item.title || item.name || new URL(url).hostname).slice(0, 180), url };
  }).filter(Boolean).slice(0, 8);
}

function linksFromText(text) {
  const found = [];
  const re = /\[([^\]]{1,160})\]\((https:\/\/[^)\s]+)\)/g;
  let match;
  while ((match = re.exec(text)) !== null) found.push({ title: match[1], url: match[2] });
  return found;
}

async function callGemini(question) {
  const key = process.env.GEMINI_API_KEY;
  if (!key) throw new Error("Gemini is not configured");
  const response = await fetch(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + encodeURIComponent(key),
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: AbortSignal.timeout(25000),
      body: JSON.stringify({
        systemInstruction: { parts: [{ text:
          "You are the TRTT evidence-first answer assistant. Answer in the user's language. Use Google Search grounding for current or factual claims. Prefer primary and official sources. Separate verified facts from uncertainty. Never invent citations, prices, schedules, laws, names, statistics, or live status. If reliable evidence is unavailable or sources conflict, say so clearly and do not guess. Do not claim that a fact is verified merely because you generated it. Give a concise useful answer and state dates where relevant."
        }] },
        contents: [{ role: "user", parts: [{ text: question }] }],
        tools: [{ google_search: {} }],
        generationConfig: { temperature: 0.2, maxOutputTokens: 900 }
      })
    }
  );
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error("Gemini request failed (" + response.status + ")");
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
    model: "Gemini 2.5 Flash",
    answer,
    sources,
    searchQueries: (grounding.webSearchQueries || []).slice(0, 5),
    grounded: sources.length > 0
  };
}

async function callOpenRouter(question) {
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error("OpenRouter is not configured");
  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + key,
      "Content-Type": "application/json",
      "HTTP-Referer": "https://trttnews24bd.blogspot.com/",
      "X-OpenRouter-Title": "TRTT Vault Evidence Answer Engine"
    },
    signal: AbortSignal.timeout(25000),
    body: JSON.stringify({
      model: "openai/gpt-5.2",
      messages: [
        {
          role: "system",
          content: "You are an evidence-first assistant. Answer in the user's language. Use the web search tool for factual or current claims. Prefer official/primary sources, cite source links in markdown, distinguish facts from uncertainty, and never invent citations, prices, schedules, laws, names, statistics or live status. If sources are missing or conflict, say that the answer is not confirmed. Do not claim certainty without evidence."
        },
        { role: "user", content: question }
      ],
      tools: [{ type: "openrouter:web_search", parameters: { max_results: 5 } }],
      temperature: 0.2,
      max_tokens: 900
    })
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error("OpenRouter request failed (" + response.status + ")");
  const message = data.choices && data.choices[0] && data.choices[0].message;
  const answer = message && typeof message.content === "string" ? message.content.trim() : "";
  if (!answer) throw new Error("OpenRouter returned no answer");
  const annotated = (message.annotations || []).map((annotation) => ({
    title: annotation.url_citation && annotation.url_citation.title,
    url: annotation.url_citation && annotation.url_citation.url
  }));
  const sources = uniqueSources([...(data.citations || []).map((url) => ({ url })), ...annotated, ...linksFromText(answer)]);
  return {
    model: String(data.model || "OpenRouter"),
    answer,
    sources,
    grounded: sources.length > 0
  };
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

  const ip = String(req.headers["x-forwarded-for"] || "unknown").split(",")[0].trim();
  const now = Date.now();
  const previous = requestCounts.get(ip);
  if (previous && now - previous.started < WINDOW_MS && previous.count >= MAX_REQUESTS) {
    return res.status(429).json({ ok: false, error: "Too many questions. Please wait a few minutes." });
  }
  if (!previous || now - previous.started >= WINDOW_MS) requestCounts.set(ip, { started: now, count: 1 });
  else requestCounts.set(ip, { started: previous.started, count: previous.count + 1 });
  if (requestCounts.size > 500) {
    for (const [key, value] of requestCounts) if (now - value.started >= WINDOW_MS) requestCounts.delete(key);
  }

  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch (_) { body = {}; }
  }
  const question = String((body && body.question) || "").trim();
  if (!question) return res.status(400).json({ ok: false, error: "Please enter a question." });
  if (question.length > 2000) return res.status(413).json({ ok: false, error: "Question is too long (maximum 2,000 characters)." });

  const results = await Promise.allSettled([callGemini(question), callOpenRouter(question)]);
  const gemini = results[0].status === "fulfilled" ? results[0].value : null;
  const openrouter = results[1].status === "fulfilled" ? results[1].value : null;
  const errors = {
    gemini: gemini ? null : "Gemini could not complete this request.",
    openrouter: openrouter ? null : "OpenRouter could not complete this request."
  };
  if (!gemini && !openrouter) {
    return res.status(502).json({ ok: false, error: "Both AI services are temporarily unavailable. Please try again later.", errors });
  }
  return res.status(200).json({
    ok: true,
    results: { gemini, openrouter },
    errors,
    note: "AI output can still be wrong. Check the linked sources, especially for legal, medical, financial, travel and other high-impact decisions."
  });
};

module.exports.config = { maxDuration: 30 };
