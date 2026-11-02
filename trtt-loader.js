// TRTT FINAL MASTER LOADER - One Time Install - 1 Click Mind Reading
// Golapi #ff2e63, Kathali #FFC300, Piaji #AF7AC5 - Wife's Favorite Colors
(function(){
  const CFG_URL = document.getElementById('trtt-master-key')?.dataset?.config;
  const DEFAULT_CFG = {
    theme:{golapi:"#ff2e63",kathali:"#FFC300",piaji:"#AF7AC5",bodyBg:"#fffafb"},
    menu:[
      {id:"home",label:"Home",href:"/",icon:"🏠",color:"#ff2e63"},
      {id:"esim",label:"eSIM Guide",href:"/search/label/eSIM",icon:"📱",color:"#FFC300"},
      {id:"flights",label:"Flights",href:"/search/label/Flights",icon:"✈️",color:"#AF7AC5"},
      {id:"explore",label:"Explore Life",href:"https://cocvghuj-trtt-news-bot.vercel.app/",icon:"🌍",color:"#ff2e63"},
      {id:"about",label:"About Us",href:"/p/about-us.html",icon:"ℹ️",color:"#FFC300"},
      {id:"contact",label:"Contact",href:"/p/contact.html",icon:"✉️",color:"#AF7AC5"}
    ]
  };

  async function getConfig(){
    if(!CFG_URL) return DEFAULT_CFG;
    try{
      const r = await fetch(CFG_URL+'?t='+Date.now(), {cache:'no-store'});
      if(!r.ok) throw new Error('no config');
      return await r.json();
    }catch(e){ return DEFAULT_CFG; }
  }

  function getScores(){ try{return JSON.parse(localStorage.getItem('trtt_smart_1click')||'{}')}catch(e){return{}} }
  function saveScore(id){
    const s=getScores(); s[id]=(s[id]||0)+1;
    localStorage.setItem('trtt_smart_1click', JSON.stringify(s));
    return s;
  }

  async function init(){
    const cfg = await getConfig();
    // Hide old Blogger menus
    const hideCss = document.createElement('style');
    hideCss.innerHTML = `.LinkList,.PageList,#main-menu,.main-menu,.PopularPosts{display:none !important} #trtt-final-root{position:sticky;top:0;z-index:99999;width:100%}`;
    document.head.appendChild(hideCss);

    let root = document.getElementById('trtt-final-root');
    if(!root){
      root=document.createElement('div'); root.id='trtt-final-root';
      const h=document.querySelector('header,.header,#header,.logo');
      if(h && h.parentNode) h.parentNode.insertBefore(root, h.nextSibling);
      else document.body.insertBefore(root, document.body.firstChild);
    }

    const scores = getScores();
    const sorted = [...cfg.menu].sort((a,b)=>(scores[b.id]||0)-(scores[a.id]||0));
    const top = sorted[0] && scores[sorted[0].id]>0 ? sorted[0] : null;

    root.innerHTML = `
      <div style="background:linear-gradient(90deg, ${cfg.theme.golapi} 0%, ${cfg.theme.piaji} 50%, ${cfg.theme.kathali} 100%);box-shadow:0 4px 20px rgba(0,0,0,0.15)">
        <div style="display:flex;align-items:center;justify-content:space-between;padding:0 15px;height:54px;max-width:1300px;margin:0 auto">
          <div style="color:#fff;font-weight:900;letter-spacing:1px">TRTT VOYAGE</div>
          <ul id="trtt-ul" style="display:flex;list-style:none;margin:0;padding:0;gap:4px">
            ${sorted.map(m=>{
              const isTop = top && m.id===top.id;
              return `<li data-id="${m.id}"><a href="${m.href}" data-id="${m.id}" style="display:block;padding:10px 14px;color:${isTop?'#000':'#fff'};background:${isTop?m.color:'transparent'};border-radius:20px;text-decoration:none;font-weight:${isTop?'800':'600'};font-size:14px;transition:0.2s">${m.icon} ${m.label} ${isTop?'<span style="font-size:10px;background:#000;color:#fff;padding:2px 6px;border-radius:10px;margin-left:5px">Your Interest ♥</span>':''}</a></li>`;
            }).join('')}
          </ul>
          <div id="trtt-ham" style="display:none;color:#fff;font-size:24px;cursor:pointer">☰</div>
        </div>
      </div>
      <style>
        @media(max-width:900px){
          #trtt-ham{display:block !important}
          #trtt-ul{display:none !important;flex-direction:column;position:absolute;left:0;top:54px;width:100%;background:linear-gradient(180deg, ${cfg.theme.golapi}, ${cfg.theme.piaji});padding:10px}
          #trtt-final-root.open #trtt-ul{display:flex !important}
        }
      </style>
    `;

    // 1-CLICK LOGIC - একবার ক্লিক করলেই মেনু বদলাবে
    root.querySelectorAll('a[data-id]').forEach(a=>{
      a.addEventListener('click', ()=>{
        saveScore(a.dataset.id);
        // পরের বার রিফ্রেশে আগে আসবে - কেউ বুঝবে না, এটাই গোপন ট্রিকস
      });
    });
    const ham=document.getElementById('trtt-ham');
    if(ham) ham.onclick=()=>root.classList.toggle('open');

    console.log('TRTT Blog Control: GitHub Active - 1 Click Mode');
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
