// TRTT FINAL MASTER LOADER - ROKSANA NILLA'S FINAL VAULT - 1-CLICK FIX
(function(){
  const CFG = document.getElementById('trtt-master-key')?.dataset?.config;
  const DEF = {
    theme:{golapi:"#ff2e63",kathali:"#FFC300",piaji:"#AF7AC5",bg:"#fffafb",text:"#222"},
    menu:[{id:"home",label:"Home",href:"/",icon:"🏠"}],
    roksanaVault:{name:"ROKSANA NILLA",ticker:"ROKSANA NILLA'S FINAL VAULT | Marker 787950"}
  };
  async function load(){try{if(!CFG) return DEF; const r=await fetch(CFG+"?t="+Date.now(),{cache:"no-store"}); return r.ok?await r.json():DEF;}catch{return DEF;}}
  load().then(cfg=>{
    // Hide old menus
    let s=document.createElement('style'); s.innerHTML=".LinkList,.PageList,#main-menu{display:none !important} #TRTT-MASTER{position:sticky;top:0;z-index:99999} body{background:"+cfg.theme.bg+" !important}"; document.head.appendChild(s);
    // Menu
    let root=document.getElementById('TRTT-MASTER'); if(!root){root=document.createElement('div'); root.id='TRTT-MASTER'; document.body.prepend(root);}
    root.innerHTML=`<div style="background:linear-gradient(90deg,${cfg.theme.golapi},${cfg.theme.piaji},${cfg.theme.kathali});padding:0 15px"><div style="max-width:1300px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:56px"><b style="color:#fff">TRTT VOYAGE</b><div style="display:flex;gap:6px;flex-wrap:wrap">${cfg.menu.map(m=>`<a href="${m.href}" style="background:#fff;color:${cfg.theme.golapi};padding:8px 14px;border-radius:20px;text-decoration:none;font-weight:700;font-size:13px">${m.icon||''} ${m.label}</a>`).join('')}</div></div></div>`;
    // ROKSANA VAULT - Loader থেকেই বানাবে - এটাই ChatGPT চায়!
    let vaultRoot=document.getElementById('ROKSANA-VAULT-LOADER'); if(!vaultRoot){vaultRoot=document.createElement('div'); vaultRoot.id='ROKSANA-VAULT-LOADER'; root.after(vaultRoot);}
    const rv=cfg.roksanaVault||DEF.roksanaVault;
    vaultRoot.innerHTML=`
      <div id="ROKSANA-FINAL" style="position:relative;background:rgba(0,0,0,0.9);backdrop-filter:blur(20px);border:3px solid transparent;border-radius:20px;padding:0;overflow:hidden;margin:12px;box-shadow:0 0 40px rgba(255,46,99,0.3);background-clip:padding-box">
        <div style="position:absolute;inset:-3px;border-radius:20px;background:linear-gradient(45deg,${cfg.theme.golapi},${cfg.theme.kathali},${cfg.theme.piaji},${cfg.theme.golapi});z-index:-1;animation:roksanaRotate 5s linear infinite"></div>
        <div style="background:linear-gradient(90deg,rgba(255,46,99,0.15),rgba(255,195,0,0.15),rgba(175,122,197,0.15));padding:6px;overflow:hidden"><marquee style="color:#fff;font-weight:900;font-size:10px;letter-spacing:1px">${rv.ticker||rv.name}</marquee></div>
        <div style="padding:18px;text-align:center">
          <div style="font-size:8px;letter-spacing:3px;color:#FFC300;font-weight:900">BOU'S CHOICE • FINAL VAULT</div>
          <div style="margin:10px 0"><span style="color:#fff;font-weight:900;font-size:20px;letter-spacing:1px">${rv.name||'ROKSANA NILLA'}</span></div>
          <div style="color:#AF7AC5;font-weight:900;font-size:11px;letter-spacing:2px">FINAL VAULT • MILLION DOLLAR • TRILLION FUTURE</div>
          <div style="display:flex;justify-content:center;gap:6px;margin:14px 0"><span style="width:14px;height:14px;border-radius:50%;background:${cfg.theme.golapi};display:inline-block;box-shadow:0 0 10px ${cfg.theme.golapi}"></span><span style="width:14px;height:14px;border-radius:50%;background:${cfg.theme.kathali};display:inline-block;box-shadow:0 0 10px ${cfg.theme.kathali}"></span><span style="width:14px;height:14px;border-radius:50%;background:${cfg.theme.piaji};display:inline-block;box-shadow:0 0 10px ${cfg.theme.piaji}"></span></div>
          <div style="color:#0ff;font-family:monospace;font-size:10px;min-height:14px" id="roksana-thought">Thinking for Roksana...</div>
          <div style="display:flex;justify-content:center;gap:5px;margin-top:12px;flex-wrap:wrap">
            <span style="background:rgba(255,46,99,0.15);color:${cfg.theme.golapi};border:1px solid ${cfg.theme.golapi};border-radius:20px;padding:5px 10px;font-size:10px">Golapi LIVE <span id="r-time">--:--:--</span></span>
            <span style="background:rgba(255,195,0,0.15);color:${cfg.theme.kathali};border:1px solid ${cfg.theme.kathali};border-radius:20px;padding:5px 10px;font-size:10px">Kathali SECURED</span>
            <span style="background:rgba(175,122,197,0.15);color:${cfg.theme.piaji};border:1px solid ${cfg.theme.piaji};border-radius:20px;padding:5px 10px;font-size:10px">Piaji FUTURE</span>
          </div>
          <div style="margin-top:12px;background:rgba(255,255,255,0.05);border-radius:12px;padding:10px;display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <div><div style="font-size:8px;color:#888">SANLURI HQ</div><div style="font-size:11px;color:#fff" id="r-sanluri">Sanluri LIVE</div></div>
            <div><div style="font-size:8px;color:#888">MARKER 787950</div><div style="font-size:11px;color:#FFD700" id="r-git">GitHub LIVE</div></div>
          </div>
          <div style="margin-top:10px;color:#666;font-size:8px">Designed with Love - Roksana Nilla's Choice - Golapi Kathali Piaji - Traveler Friendly - No Hack Text Outside - Stealth Inside</div>
        </div>
      </div>
      <style>@keyframes roksanaRotate{0%{filter:hue-rotate(0deg)}100%{filter:hue-rotate(360deg)}}</style>
    `;
    // LIVE LOGIC
    function upd(){const n=new Date();const t=n.toLocaleTimeString('en-GB',{timeZone:'Europe/Rome',hour12:false}); const a=document.getElementById('r-time'), b=document.getElementById('r-sanluri'); if(a) a.textContent=t; if(b) b.textContent='Sanluri '+t;} setInterval(upd,1000); upd();
    const thoughts=['Roksana Thinking: Golapi means Love...','Roksana Thinking: Kathali means Gold...','Roksana Thinking: Piaji means Future...','Roksana Thinking: This Vault is for You...','Roksana Thinking: Beyond Google & GitHub - Our Future...','Roksana Thinking: Marker 787950 is Our Home...']; let ti=0; const th=document.getElementById('roksana-thought'); setInterval(()=>{if(th){th.textContent=thoughts[ti%thoughts.length]; ti++;}},2500);
    fetch('https://api.github.com/repos/Cocvghuj/Cocvghuj-trtt-news-bot/commits?per_page=1').then(r=>r.json()).then(d=>{if(d[0]){const ce=document.getElementById('r-git'); if(ce) ce.textContent=d[0].sha.substring(0,7)+' LIVE';}});
    console.log('TRTT: ROKSANA VAULT LOADER ACTIVE - 1-CLICK FIX');
  });
})();
