// Vercel Serverless - ROKSANA NILLA LIVE THINKING - OpenRouter Proxy - Brand Protected
// API Key Vercel Environment Variable এ থাকবে - OPENROUTER_API_KEY - Safe!
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET');
  
  const thoughts = [
    "Golapi means Love - Roksana's Choice #ff2e63",
    "Kathali means Gold - Sonar Moto Hasi #FFC300",
    "Piaji means Dream - Amader Vobissot #AF7AC5",
    "Marker 787950 SECURED - Sanluri HQ LIVE",
    "Cagliari - Rome €29 Live - Best Deal Today!",
    "eSIM Italy €4.99 - Instant Activation - TRTT",
    "Building Trillion Dollar Future Beyond Google & GitHub"
  ];

  // Try OpenRouter if Key exists, else fallback to local thoughts
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (apiKey) {
    try {
      const r = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://trttnews24bd.blogspot.com',
          'X-Title': 'Roksana Nilla Final Vault'
        },
        body: JSON.stringify({
          model: 'openai/gpt-3.5-turbo',
          messages: [{role:'user', content:'Generate 1 short live thinking for Roksana Nilla Final Vault - Golapi Kathali Piaji - Marker 787950 - Sanluri Italy - Max 12 words - Example: Roksana Thinking: Cagliari Rome €29 Live'}],
          max_tokens: 30
        })
      });
      const data = await r.json();
      const liveText = data.choices?.[0]?.message?.content?.trim();
      if (liveText) {
        return res.status(200).json({ thinking: `Roksana Thinking: ${liveText}`, source: 'openrouter' });
      }
    } catch(e){ console.log('OpenRouter error, fallback', e); }
  }

  // Fallback - No API Key or Error - Local Live
  const idx = Math.floor(Date.now()/5000) % thoughts.length;
  return res.status(200).json({ thinking: `Roksana Thinking: ${thoughts[idx]}...`, source: 'local' });
}
