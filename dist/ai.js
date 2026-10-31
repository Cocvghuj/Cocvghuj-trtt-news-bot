// ai.js - Full Auto OpenRouter - No need to touch index.html HTML
const OPENROUTER_KEY = "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";
const MODEL = "nvidia/nemotron-3.5-lightning:free";

(function() {
  // Auto create UI without touching HTML
  const style = document.createElement('style');
  style.innerHTML = `#ai-box{position:fixed;bottom:20px;right:20px;z-index:99999;display:flex;gap:5px}#ai-input{padding:12px;width:220px;border-radius:25px;border:1px solid #ccc;box-shadow:0 2px 10px rgba(0,0,0,0.1)}#ai-btn{padding:12px 18px;border-radius:25px;background:#000;color:#fff;border:none;cursor:pointer}#ai-output{position:fixed;bottom:80px;right:20px;width:300px;max-height:400px;overflow-y:auto;padding:15px;background:#fff;border-radius:15px;box-shadow:0 5px 20px rgba(0,0,0,0.2);display:none;z-index:99999;font-family:sans-serif;font-size:14px;line-height:1.5}`;
  document.head.appendChild(style);

  const box = document.createElement('div');
  box.id = 'ai-box';
  box.innerHTML = `<input id="ai-input" placeholder="কোথায় যাবে? লিখো..."><button id="ai-btn">Go</button>`;
  document.body.appendChild(box);

  const output = document.createElement('div');
  output.id = 'ai-output';
  document.body.appendChild(output);

  async function autoGenerate() {
    const input = document.getElementById('ai-input');
    const prompt = input.value.trim();
    if(!prompt) return;
    
    output.style.display = "block";
    output.innerHTML = "AI লিখছে... ✈️ একটু অপেক্ষা করো...";

    try {
      const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + OPENROUTER_KEY,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://cocvghuj.github.io",
          "X-Title": "Trtr Travel"
        },
        body: JSON.stringify({
          model: MODEL,
          messages: [
            { role: "system", content: "You are a Europe travel expert. Answer in simple Bengali+English mix, short, helpful, give flight/hotel tips." },
            { role: "user", content: prompt }
          ]
        })
      });
      const data = await res.json();
      if(data.error) throw new Error(data.error.message);
      output.innerHTML = data.choices[0].message.content.replace(/\n/g, "<br>");
    } catch(e) {
      output.innerHTML = "Error: " + e.message + "<br>Key টা ঠিক আছে কিনা দেখো।";
    }
  }

  document.getElementById('ai-btn').addEventListener('click', autoGenerate);
  document.getElementById('ai-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') autoGenerate(); });
})();
