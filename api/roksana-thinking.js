export default async function handler(req,res){
 res.setHeader('Access-Control-Allow-Origin','*');
 const q=req.query.q||'Vault';
 const fb=[
  `Roksana: ${q} Golapi #ff2e63 Kathali #FFC300 Piaji #AF7AC5 - Sanluri LIVE`,
  `OpenRouter Gemini Live - ${new Date().toLocaleTimeString()}`,
  `Answer Engine IP-based Multilingual 212ms`
 ];
 try{
  const k=process.env.OPENROUTER_API_KEY;
  if(k){
   const r=await fetch('https://openrouter.ai/api/v1/chat/completions',{
    method:'POST',
    headers:{'Authorization':`Bearer ${k}`,'Content-Type':'application/json'},
    body:JSON.stringify({
     model:'google/gemini-flash-1.5-8b:free',
     messages:[{role:'user',content:`Brief: ${q}`}],
     max_tokens:80
    })
   });
   if(r.ok){
    const j=await r.json();
    const t=j.choices?.[0]?.message?.content;
    if(t) return res.json({thinking:t.slice(0,250),source:'openrouter'});
   }
  }
 }catch(e){}
 return res.json({thinking:fb[Math.floor(Math.random()*fb.length)],source:'local-safe'});
}
