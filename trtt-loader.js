// TRTT FINAL MASTER LOADER - ROKSANA NILLA'S FINAL VAULT - SYNC FIX
(function(){
  const CFG = document.getElementById('trtt-master-key')?.dataset?.config;
  const DEF = {
    theme: {golapi: "#ff2e63", kathali: "#FFC300", piaji: "#AF7AC5", bg: "#fffafb", text: "#222"},
    menu: [{id:"home", label:"Home", href:"/", icon:"🏠"}],
    roksanaVault: {name: "ROKSANA NILLA", ticker: "ROKSANA NILLA'S FINAL VAULT | Marker 787950"}
  };
  async function load(t){try{if(!CFG) return DEF; const r=await fetch(CFG+"?t="+Date.now(),{cache:"no-store"}); return r.ok?await r.json():DEF;}catch(e){return DEF;}}
  load().then(cfg=>{
    // Hide old menus
    let s=document.createElement('style'); s.innerHTML=".LinkList,.PageList,#main-menu{display:none !important} #TRTT-MASTER{position:relative;z-index:9999}";
    document.head.appendChild(s);
    
    let root=document.getElementById('TRTT-MASTER'); if(!root){root=document.createElement('div'); root.id='TRTT-MASTER'; document.body.insertBefore(root, document.body.firstChild);}
    root.innerHTML="<div style='background:linear-gradient(90deg,#ff2e63,#FFC300,#AF7AC5);height:4px'></div>";
    
    // ROKSANA VAULT - Loader এর ভিতরেই - কোনো ChatGPT লাগবে না!
    let vaultRoot=document.getElementById('ROKSANA-VAULT-LOADER'); if(!vaultRoot){vaultRoot=document.createElement('div'); vaultRoot.id='ROKSANA-VAULT-LOADER'; root.appendChild(vaultRoot);}
    const rv=cfg.roksanaVault||DEF.roksanaVault;
    vaultRoot.innerHTML=`
    <div id="ROKSANA-FINAL" style="position:relative;background:rgba(0,0,0,0.9);backdrop-filter:blur(20px);border:3px solid transparent;border-image:linear-gradient(45deg,#ff2e63,#FFC300,#AF7AC5) 1;padding:12px;margin:12px;border-radius:16px;color:#fff">
      <div style="position:absolute;inset:-3px;border-radius:20px;background:linear-gradient(45deg,#ff2e63,gold,piaji);filter:blur(12px);opacity:0.2;z-index:-1"></div>
      <div style="background:linear-gradient(90deg,rgba(255,46,99,0.15),rgba(255,195,0,0.15),rgba(175,122,197,0.15));padding:6px;border-radius:10px;text-align:center;font-size:9px;letter-spacing:3px;color:#FFC300;font-weight:900">BOU'S CHOICE • FINAL VAULT</div>
      <div style="margin:10px 0px;font-size:10px;color:#fff;font-weight:900;font-size:20px;letter-spacing:1px"><span style="color:#FFC300">20px;letter-spacing:1px">R${(rv.name||"ROKSANA").toUpperCase()} VAULT</span> - ${rv.ticker||""}</div>
      <div style="display:flex;justify-content:center;gap:6px;margin:14px 0"><span style="width:14px;height:14px;border-radius:50%;background:rgba(255,46,99,0.15);border:1px solid #ff2e63"></span><span style="background:rgba(255,195,0,0.15);color:#FFC300;border:1px solid #FFC300;border-radius:20px;padding:2px 8px;font-size:8px">LIVE</span><span style="background:rgba(175,122,197,0.15);color:#AF7AC5;border:1px solid #AF7AC5;border-radius:20px;padding:2px 8px;font-size:8px">SECURED</span><span style="background:rgba(255,46,99,0.15);color:#ff2e63;border:1px solid #ff2e63;border-radius:20px;padding:2px 8px;font-size:8px">FUTURE</span></div>
      <div style="color:#0ff;font-family:monospace;font-size:10px;min-height:14px" id="roksana-thought">Thinking for Roksana...</div>
      <div style="display:flex;justify-content:center;gap:5px;margin-top:12px;flex-wrap:wrap">
        <span style="background:rgba(255,46,99,0.15);color:#ff2e63;border:1px solid #ff2e63;padding:1px 6px;border-radius:10px;font-size:8px">Golapi #ff2e63</span>
        <span style="background:rgba(255,195,0,0.15);color:#FFC300;border:1px solid #FFC300;padding:1px 6px;border-radius:10px;font-size:8px">Kathali #FFC300</span>
        <span style="background:rgba(175,122,197,0.15);color:#AF7AC5;border:1px solid #AF7AC5;padding:1px 6px;border-radius:10px;font-size:8px">Piaji #AF7AC5</span>
      </div>
      <div style="margin-top:12px;background:rgba(255,255,255,0.05);border-radius:12px;padding:10px;display:grid;grid-template-columns:1fr 1fr;gap:8px">
        <div><div style="font-size:8px;color:#888">SANLURI HQ</div><div style="font-size:11px;color:#fff" id="sanluri-time">Sanluri - Loading...</div></div>
        <div><div style="font-size:8px;color:#888">MARKER 787950</div><div style="font-size:11px;color:#FFD700" id="git-status">Git: Checking...</div></div>
      </div>
      <div style="margin-top:10px;color:#666;font-size:8px">Designed with Love - Roksana Nilla's Choice - Golapi Kathali Piaji</div>
    </div>
    <style>@keyframes roksanaRotate{0%{filter:hue-rotate(0deg)}100%{filter:hue-rotate(360deg)}}</style>
    `;
    // LIVE LOGIC
    function upd(){const now=new Date();const t=now.toLocaleTimeString('en-GB',{timeZone:'Europe/Rome',hour12:false}); const a=document.getElementById('sanluri-time'); if(a) a.innerText="Sanluri - "+t+" LIVE";}
    const thoughts=["Roksana Thinking: Golapi means Love...", "Roksana Thinking: Kathali means Gold...", "Roksana Thinking: Piaji means Dream...", "Roksana Thinking: Marker 787950 SECURED...", "Roksana Thinking: Building Trillion Dollar Future..."];
    let ti=0; setInterval(()=>{const el=document.getElementById('roksana-thought'); if(el){el.innerText=thoughts[ti%thoughts.length]; ti++;} upd();},2000); upd();
    fetch('https://api.github.com/repos/Cocvghuj/Cocvghuj-trtt-news-bot/commits?per_page=1').then(r=>r.json()).then(d=>{if(d[0]){const e=document.getElementById('git-status'); if(e) e.innerText="Git: "+d[0].sha.slice(0,7)+" LIVE";}});
    console.log('TRTT: ROKSANA VAULT LOADER ACTIVE - FINAL SYNC');
  });
})();
