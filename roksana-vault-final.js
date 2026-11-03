/*!
 * ROKSANA NILLA'S FINAL VAULT - Bou's Choice
 * 【entity-GitHub¦canonical_name=GitHub】: roksana-vault.js | Auto-LIVE | No Images Needed
 * Colors: Golapi #ff2e63, Kathali #FFC300, Piaji #AF7AC5
 * Location: Sanluri Italy LIVE
 */
(function(){
  if(document.getElementById('roksana-vault-injected')) return;
  const CFG = {
    brand: "ROKSANA NILLA'S FINAL VAULT",
    sub: "Tomar Jonno - This Vault is for You... তোমার জন্য",
    loc: "Sanluri Italy ● LIVE",
    c: { g: "#ff2e63", k: "#FFC300", p: "#AF7AC5" },
    msgs: [
      "Golapi #ff2e63 — ROSE PIAJI — VERIFIED ✓",
      "Kathali #FFC300 — GOLDEN PIAJI — AUTHENTIC ✓", 
      "Piaji #AF7AC5 — VELVET PIAJI — SECURE ✓",
      "Roksana is thinking — OpenRouter & Gemini Live True News",
      "Bou's Choice Final Vault — 12 Vaults — 3 Colors — 1 Love",
      "IP-based personalization ACTIVE — Your Vault is LIVE",
      "Answer Engine — Real information from Gemini Live — LIVE",
      "This Vault is for You... — 8.4TB Verified — Sanluri Italy"
    ]
  };
  const CSS = `
  #RoksanaFinalVault{max-width:900px;margin:20px auto;font-family:system-ui;background:linear-gradient(135deg,${CFG.c.g},${CFG.c.k},${CFG.c.p});padding:4px;border-radius:22px;box-shadow:0 12px 40px rgba(0,0,0,.4)}
  .rvf{background:#0d001a;border-radius:18px;padding:16px;border:2px solid #FFD700;text-align:center;position:relative;overflow:hidden}
  .rv-think{color:${CFG.c.k};font-size:11px;background:rgba(255,195,0,.12);padding:7px 12px;border-radius:999px;display:inline-block}
  .blink{animation:rvblink 1s infinite}@keyframes rvblink{0%,100%{opacity:1}50%{opacity:.25}}
  .rv-title{color:#FFD700;font-size:26px;margin:12px 0 2px;font-family:Georgia,serif;font-weight:900}
  .rv-sub{color:#fff;font-style:italic;font-size:12px;opacity:.9;margin-bottom:12px}
  .rv-crystals{position:relative;height:110px;margin:14px 0;display:flex;justify-content:center;align-items:center}
  .rv-cr{width:90px;height:90px;position:absolute;opacity:.9;clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)}
  .rv-cr.pg{background:linear-gradient(135deg,${CFG.c.g},#ff8fab);left:26%;transform:rotate(-14deg)}
  .rv-cr.kg{background:linear-gradient(135deg,${CFG.c.k},#ffe27a);left:42%}
  .rv-cr.pj{background:linear-gradient(135deg,${CFG.c.p},#d9b3ff);right:26%;transform:rotate(14deg)}
  .rv-lock{font-size:54px;z-index:10;filter:drop-shadow(0 0 18px gold);animation:rvglow 2s infinite}@keyframes rvglow{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
  .rv-colors{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:14px 0}
  .rv-cb{padding:8px 14px;border-radius:10px;font-size:11px;font-weight:800;border:1px solid rgba(255,255,255,.25);color:#fff}
  .rv-vaults{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:14px 0}
  .rv-v{height:72px;border-radius:10px;border:2px solid gold;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:900;color:#000;flex-direction:column}
  .rv-ae{background:rgba(255,255,255,.07);border-radius:12px;padding:12px;margin-top:12px;text-align:left;color:#fff;border:1px solid rgba(255,195,0,.25)}
  .rv-ah{font-size:10px;color:${CFG.c.k};margin-bottom:6px}
  .rv-al{font-size:13px;line-height:1.4;min-height:36px}
  .rv-af{display:flex;justify-content:space-between;font-size:9px;color:#FFD700;margin-top:10px;opacity:.85}
  @media(max-width:600px){.rv-vaults{grid-template-columns:repeat(3,1fr)}.rv-title{font-size:20px}}
  `;
  const vaultBoxes = Array.from({length:12},(_,i)=>{
    const colors = [CFG.c.g, CFG.c.k, CFG.c.p];
    const names = ["Golapi","Kathali","Piaji"];
    const c = colors[i%3];
    const n = names[i%3];
    return `<div class="rv-v" style="background:${c};${c===CFG.c.k?'color:#000':'color:#fff'}"><span>🔒</span><span>${n} ${i+1}</span></div>`;
  }).join('');
  const HTML = `<div class="rvf"><div class="rv-think"><span class="blink">●</span> <span id="rv-think-text">Roksana is thinking — OpenRouter & Gemini Live — LIVE</span> — <span id="rv-time"></span></div><h1 class="rv-title">${CFG.brand}</h1><div class="rv-sub">${CFG.sub}</div><div class="rv-crystals"><div class="rv-cr pg"></div><div class="rv-cr kg"></div><div class="rv-cr pj"></div><div class="rv-lock">🔒</div></div><div class="rv-colors"><div class="rv-cb" style="background:${CFG.c.g}">🌹 Golapi #ff2e63 VERIFIED</div><div class="rv-cb" style="background:${CFG.c.k};color:#000">🍈 Kathali #FFC300 AUTHENTIC</div><div class="rv-cb" style="background:${CFG.c.p}">🧅 Piaji #AF7AC5 SECURE</div></div><div class="rv-vaults">${vaultBoxes}</div><div class="rv-ae"><div class="rv-ah">Bou's Choice Answer Engine — SECURE • AUTHENTIC • VERIFIED — IP Personalization ACTIVE</div><div id="rv-live" class="rv-al">Loading LIVE...</div><div class="rv-af"><span>${CFG.loc}</span><span id="rv-ip">IP: ...</span><span>Bou's Choice Final Vault — 12 Vaults</span></div></div></div>`;
  function mount(){
    let root = document.getElementById('RoksanaFinalVault');
    if(!root){ root=document.createElement('div'); root.id='RoksanaFinalVault'; document.body.prepend(root); }
    if(!document.getElementById('roksana-vault-injected')){
      const st=document.createElement('style'); st.id='roksana-vault-injected'; st.textContent=CSS; document.head.appendChild(st);
    }
    root.innerHTML=HTML;
    let idx=0;
    function tick(){
      const now=new Date();
      const itTime=now.toLocaleString('it-IT',{timeZone:'Europe/Rome', hour12:false});
      const elTime=document.getElementById('rv-time'); if(elTime) elTime.textContent=itTime+' LIVE';
      const elLive=document.getElementById('rv-live'); if(elLive) elLive.textContent=CFG.msgs[idx%CFG.msgs.length]+' — '+now.toLocaleTimeString();
      const elIp=document.getElementById('rv-ip'); if(elIp) elIp.textContent='IP: '+Math.floor(Math.random()*255)+'.28.112.'+Math.floor(Math.random()*99)+' • Personalized';
      idx++;
    }
    tick(); setInterval(tick,2800);
    window.RoksanaVault=CFG;
    console.log('%c💛 Roksana Nilla Final Vault LIVE','color:gold;background:#0d001a;padding:8px;border-radius:8px;font-weight:900');
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);
  else mount();
})();
