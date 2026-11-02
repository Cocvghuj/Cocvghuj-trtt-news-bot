// TRTT GHOST LOADER - Single Source of Truth - No Public Folder - Loads Vault Only
(function(){
  const CFG = document.getElementById('trtt-master-key')?.dataset?.config || "https://raw.githubusercontent.com/Cocvghuj/Cocvghuj-trtt-news-bot/main/blog-control.json";
  const BASE = "https://cocvghuj-trtt-news-bot.vercel.app";
  async function getConfig(){try{const r=await fetch(CFG+"?t="+Date.now(),{cache:"no-store"});return r.ok?await r.json():{}}catch{return {};}}
  getConfig().then(cfg=>{
    // Hide old Blogger menus
    let s=document.createElement('style'); s.innerHTML=".LinkList,.PageList{display:none !important} #TRTT-MASTER{position:relative;z-index:9999}"; document.head.appendChild(s);
    let root=document.getElementById('TRTT-MASTER'); if(!root){root=document.createElement('div'); root.id='TRTT-MASTER'; document.body.prepend(root);}
    root.innerHTML="<div style='height:4px;background:linear-gradient(90deg,#ff2e63,#FFC300,#AF7AC5)'></div>";
    // Load Protected Brand Vault - No one can touch this file directly, only via loader
    let sc=document.createElement('script'); sc.src=BASE+"/roksana-vault.js?t="+Date.now(); sc.onload=function(){ if(window.RoksanaVault){ window.RoksanaVault.show(cfg.roksanaVault||{}); } }; document.head.appendChild(sc);
    // Load Menu from blog-control.json - Traveler Friendly
    if(cfg.menu){ console.log('TRTT: Menu loaded from GitHub', cfg.menu.length); }
    console.log('TRTT GHOST LOADER: Brand Protected - Marker 787950');
  });
})();
