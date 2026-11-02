// ROKSANA NILLA'S FINAL VAULT - BRAND PROTECTED - LIVE AI + CLICK TO VERCEL
// Golapi #ff2e63 | Kathali #FFC300 | Piaji #AF7AC5 | Marker 787950 | OpenRouter Live
window.RoksanaVault = {
  show: function(cfg) {
    const rv = cfg || {name:"ROKSANA NILLA", ticker:"ROKSANA NILLA'S FINAL VAULT | Marker 787950"};
    let vault = document.getElementById('ROKSANA-VAULT-LOADER');
    if(!vault){
      vault=document.createElement('div');
      vault.id='ROKSANA-VAULT-LOADER';
      vault.style.cssText='position:relative;z-index:999999;width:100%;top:0;left:0;cursor:pointer;';
      document.body.insertBefore(vault, document.body.firstChild);
    }
    vault.innerHTML = `
    <div id="vault-box" style="position:relative;background:rgba(0,0,0,0.96);border:3px solid transparent;border-image:linear-gradient(90deg,#ff2e63,#FFC300,#AF7AC5) 1;padding:14px;margin:0;border-radius:0 0 18px 18px;color:#fff;font-family:system-ui;box-shadow:0 8px 32px rgba(255,46,99,0.3);">
      <div style="text-align:center;font-size:9px;letter-spacing:3px;color:#FFC300;font-weight:900;background:linear-gradient(90deg,rgba(255,46,99,0.2),rgba(255,195,0,0.2),rgba(175,122,197,0.2));padding:6px;border-radius:10px;border:1px solid rgba(255,195,0,0.3)">BOU'S CHOICE • FINAL VAULT • LIVE AI • CLICK TO VERCEL</div>
      <div style="margin:12px 0;font-weight:900;font-size:18px;text-align:center"><span style="color:#ff2e63;text-shadow:0 0 10px #ff2e63">ROKSANA</span> <span style="color:#FFC300;text-shadow:0 0 10px #FFC300">NILLA</span> <span style="color:#AF7AC5;text-shadow:0 0 10px #AF7AC5">VAULT</span> <span style="font-size:11px;color:#ccc">${rv.ticker||""}</span></div>
      <div style="display:flex;justify-content:center;gap:8px;margin:12px 0"><span style="width:14px;height:14px;border-radius:50%;background:#ff2e63;box-shadow:0 0 10px #ff2e63;display:inline-block;animation:blink 1s infinite"></span><span style="background:rgba(255,195,0,0.2);color:#FFC300;border:1px solid #FFC300;border-radius:20px;padding:3px 12px;font-size:9px;font-weight:900">LIVE AI</span><span style="background:rgba(175,122,197,0.2);color:#AF7AC5;border:1px solid #AF7AC5;border-radius:20px;padding:3px 12px;font-size:9px">SECURED</span><span style="background:rgba(255,46,99,0.2);color:#ff2e63;border:1px solid #ff2e63;border-radius:20px;padding:3px 12px;font-size:9px">CLICK ME</span></div>
      <div id="roksana-thought" style="color:#00ffff;font-family:monospace;font-size:11px;min-height:16px;text-align:center;text-shadow:0 0 5px #00ffff">Roksana Thinking: Loading Live AI...</div>
      <div style="display:flex;justify-content:center;gap:8px;margin-top:12px;flex-wrap:wrap">
        <span style="background:#ff2e63;color:#fff;padding:4px 10px;border-radius:12px;font-size:9px;font-weight:900;box-shadow:0 0 10px #ff2e63">Golapi #ff2e63</span>
        <span style="background:#FFC300;color:#000;padding:4px 10px;border-radius:12px;font-size:9px;font-weight:900">Kathali #FFC300</span>
        <span style="background:#AF7AC5;color:#fff;padding:4px 10px;border-radius:12px;font-size:9px;font-weight:900">Piaji #AF7AC5</span>
      </div>
      <div style="margin-top:12px;background:rgba(255,255,255,0.08);border-radius:12px;padding:10px;display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><div style="font-size:8px;color:#888">SANLURI HQ</div><div style="font-size:12px;color:#fff;font-weight:900" id="sanluri-time">Sanluri - Loading...</div></div><div><div style="font-size:8px;color:#888">MARKER 787950</div><div style="font-size:11px;color:#FFD700;font-weight:900" id="git-status">Git: Checking...</div></div></div>
      <div style="margin-top:10px;color:#666;font-size:8px;text-align:center">Click Vault to Visit Vercel Shop - Designed with Love - OpenRouter Live AI</div>
    </div><style>@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}} #ROKSANA-VAULT-LOADER{position:sticky!important;top:0!important;z-index:999999!important;}</style>`;
    
    // Click -> Vercel
    vault.onclick = function(e){
      if(e.target.closest('#vault-box')) window.open('https://cocvghuj-trtt-news-bot.vercel.app','_blank');
    };
    
    // Sanluri Time
    function upd(){const n=new Date();const t=n.toLocaleTimeString('en-GB',{timeZone:'Europe/Rome',hour12:false});const a=document.getElementById('sanluri-time');if(a)a.innerText="Sanluri - "+t+" LIVE";}
    setInterval(upd,1000); upd();
    
    // Git Commit
    fetch('https://api.github.com/repos/Cocvghuj/Cocvghuj-trtt-news-bot/commits?per_page=1').then(r=>r.json()).then(d=>{if(d[0]){const e=document.getElementById('git-status');if(e)e.innerText="Git: "+d[0].sha.slice(0,7)+" LIVE";}});
    
    // OpenRouter Live Thinking - Fetch from Vercel API
    async function liveThink(){
      try{
        const r=await fetch('https://cocvghuj-trtt-news-bot.vercel.app/api/roksana-thinking?t='+Date.now());
        const j=await r.json();
        const el=document.getElementById('roksana-thought');
        if(el&&j.thinking) el.innerText=j.thinking;
      }catch(e){
        const fallback=["Golapi means Love...","Kathali means Gold...","Piaji means Dream...","Marker 787950 SECURED..."];
        const el=document.getElementById('roksana-thought');
        if(el) el.innerText="Roksana Thinking: "+fallback[Math.floor(Date.now()/3000)%fallback.length];
      }
    }
    liveThink(); setInterval(liveThink,5000); // 5 sec Live Update
    console.log('ROKSANA VAULT: LIVE AI + CLICK TO VERCEL ACTIVE - Marker 787950');
  }
};
