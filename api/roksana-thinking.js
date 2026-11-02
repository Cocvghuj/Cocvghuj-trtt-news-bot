// ROKSANA NILLA LIVE AI - DUAL BACKUP - OpenRouter + Gemini + Local - Marker 787950
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET');
  res.setHeader('Cache-Control', 'no-cache');

  const fallback = [
    "Golapi means Love - #ff2e63",
    "Kathali means Gold - #FFC300",
    "Piaji means Dream - #AF7AC5",
    "Marker 787950 SECURED - Sanluri HQ LIVE",
    "Cagliari - Rome €29 Live - Best Deal!",
    "eSIM Italy €4.99 - Instant - TRTT",
    "Building Trillion Dollar Future Beyond Google"
  ];

  // 1st Try: OpenRouter
  const openRouterKey = process.env.OPENROUTER_API_KEY;
  if (openRouterKey) {
    try {
      const r = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${openRouterKey}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://trttnews24bd.blogspot.com',
          'X-Title': 'Roksana Nilla Vault'
        },
        body: JSON.stringify({
          model: 'openai/gpt-3.5-turbo',
          messages: [{ role: 'user', content: 'Generate 1 short live thinking for Roksana Nilla Vault - Golapi Kathali Piaji - Marker 787950 - Max 10 words - No quotes' }],
          max_tokens: 25
        })
      });
      const data = await r.json();
      const txt = data.choices?.[0]?.message?.content?.trim();
      if (txt) return res.status(200).json({ thinking: `Roksana Thinking: ${txt}`, source: 'openrouter-live' });
    } catch (e) { console.log('OpenRouter fail, trying Gemini', e.message); }
  }

  // 2nd Try: Gemini (Your Existing Key)
  const geminiKey = process.env.GEMINI_API_KEY;
  if (geminiKey) {
    try {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${geminiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contents: [{ parts: [{ text: "Generate 1 short live thinking for Roksana Nilla Vault - Golapi Kathali Piaji - Marker 787950 - Max 10 words" }] }] })
      });
      const d = await r.json();
      const live = d.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
      if (live) return res.status(200).json({ thinking: `Roksana Thinking: ${live}`, source: 'gemini-live' });
    } catch (e) { console.log('Gemini fail, fallback to local', e.message); }
  }

  // 3rd Fallback: Local - Always Works!
  const idx = Math.floor(Date.now() / 5000) % fallback.length;
  return res.status(200).json({ thinking: `Roksana Thinking: ${fallback[idx]}...`, source: 'local-backup' });
}
