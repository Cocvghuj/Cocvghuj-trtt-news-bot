// TRTT ONE MASTER CONTROL - Menu + Design + Color + Theme - 100% GitHub Controlled
(function(){
  const CFG = document.getElementById('trtt-master-key')?.dataset?.config;
  const DEF = {
    theme:{golapi:"#ff2e63", kathali:"#FFC300", piaji:"#AF7AC5", bg:"#fffafb", text:"#222", font:"Hind Siliguri, sans-serif"},
    menu:[
      {id:"home", label:"Home", href:"/", icon:"🏠"},
      {id:"esim", label:"eSIM", href:"/search/label/eSIM", icon:"📱"},
      {id:"flights", label:"Flights", href:"/search/label/Flights", icon:"✈️"}
    ],
    customCSS:""
  };
  async function load(){
    try{
      if(!CFG) return DEF;
      const r = await fetch(CFG+"?t="+Date.now(),{cache:"no-store"});
      return r.ok ? await r.json() : DEF;
    }catch{ return DEF; }
  }
  load().then(cfg=>{
    // 1. পুরোনো মেনু লুকাও
    let s=document.createElement('style');
    s.innerHTML=`.LinkList,.PageList,#main-menu{display:none !important} #TRTT-MASTER{position:sticky;top:0;z-index:99999} body{background:${cfg.theme.bg} !important; color:${cfg.theme.text}; font-family:${cfg.theme.font}} ${cfg.customCSS||''}`;
    document.head.appendChild(s);
    
    // 2. নতুন মেনু বানাও
    let root=document.getElementById('TRTT-MASTER');
    if(!root){ root=document.createElement('div'); root.id='TRTT-MASTER'; document.body.prepend(root); }
    
    root.innerHTML=`
      <div style="background:linear-gradient(90deg,${cfg.theme.golapi},${cfg.theme.piaji},${cfg.theme.kathali}); padding:0 15px">
        <div style="max-width:1300px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; height:56px">
          <b style="color:#fff">TRTT VOYAGE</b>
          <div style="display:flex; gap:6px; flex-wrap:wrap">
            ${cfg.menu.map(m=>`<a href="${m.href}" style="background:#fff; color:${cfg.theme.golapi}; padding:8px 14px; border-radius:20px; text-decoration:none; font-weight:700; font-size:13px">${m.icon||''} ${m.label}</a>`).join('')}
          </div>
        </div>
      </div>`;
    console.log('TRTT: GitHub Control Active');
  });
})();
