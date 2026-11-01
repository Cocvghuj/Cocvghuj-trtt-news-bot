(function () {
  // This legacy public widget is retained only as a safe authenticated client.
  // The access token is held in memory for this page session only; provider keys
  // are never sent to or stored in the browser.
  if (document.getElementById("trtt-ai-panel")) return;
  const style = document.createElement("style");
  style.textContent = "#trtt-ai-panel{position:fixed;right:16px;bottom:16px;z-index:99990;width:min(360px,calc(100vw - 32px));font:14px system-ui;background:#fff;color:#111827;border:1px solid #d1d5db;border-radius:16px;padding:14px;box-shadow:0 8px 32px #0002}#trtt-ai-panel input,#trtt-ai-panel textarea{box-sizing:border-box;width:100%;padding:10px;border:1px solid #d1d5db;border-radius:9px;margin:5px 0}#trtt-ai-panel button{padding:9px 13px;border:0;border-radius:9px;background:#111827;color:white;cursor:pointer}#trtt-ai-output{white-space:pre-wrap;max-height:220px;overflow:auto;margin-top:10px}#trtt-ai-panel small{color:#6b7280}";
  document.head.appendChild(style);
  const panel = document.createElement("section");
  panel.id = "trtt-ai-panel";
  const title = document.createElement("strong");
  title.textContent = "TRTT AI Assistant";
  const note = document.createElement("small");
  note.textContent = "Secure server-side AI. Enter your owner access token; it is not saved.";
  const token = document.createElement("input");
  token.type = "password";
  token.autocomplete = "off";
  token.placeholder = "Command Center access token";
  token.setAttribute("aria-label", "Command Center access token");
  const prompt = document.createElement("textarea");
  prompt.rows = 2;
  prompt.placeholder = "তোমার প্রশ্ন লিখো...";
  prompt.setAttribute("aria-label", "তোমার প্রশ্ন");
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = "Send";
  const output = document.createElement("div");
  output.id = "trtt-ai-output";
  output.setAttribute("role", "status");
  panel.append(title, document.createElement("br"), note, token, prompt, button, output);
  document.body.appendChild(panel);
  button.addEventListener("click", async function () {
    const accessToken = token.value.trim();
    const message = prompt.value.trim();
    if (!accessToken || !message) {
      output.textContent = "Access token ও প্রশ্ন—দুটিই দিতে হবে।";
      return;
    }
    button.disabled = true;
    output.textContent = "AI উত্তর তৈরি করছে...";
    try {
      const response = await fetch("/api/command-center/chat", {
        method: "POST",
        headers: { "Authorization": "Bearer " + accessToken, "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: message })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Request failed");
      output.textContent = data.text || "কোনো উত্তর পাওয়া যায়নি।";
    } catch (error) {
      output.textContent = "সেবা এখন প্রস্তুত নয়: " + String(error.message || "Unknown error");
    } finally {
      button.disabled = false;
      token.value = "";
    }
  });
})();