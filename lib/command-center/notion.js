"use strict";

async function appendNotionNote(content, env = process.env) {
  if (!env.NOTION_API_KEY || !env.NOTION_PROJECT_PAGE_ID) {
    throw new Error("Notion integration token and project page are not configured.");
  }
  const text = String(content || "").trim().slice(0, 1800);
  if (!text) throw new Error("Notion note content is required.");
  const response = await fetch("https://api.notion.com/v1/blocks/" + encodeURIComponent(env.NOTION_PROJECT_PAGE_ID) + "/children", {
    method: "PATCH",
    headers: {
      "Authorization": "Bearer " + env.NOTION_API_KEY,
      "Notion-Version": "2026-03-11",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      children: [{
        object: "block",
        type: "paragraph",
        paragraph: { rich_text: [{ type: "text", text: { content: text } }] }
      }]
    }),
    signal: AbortSignal.timeout(15000)
  });
  if (!response.ok) throw new Error("Notion API request failed (HTTP " + response.status + ").");
  return response.json();
}

module.exports = { appendNotionNote };