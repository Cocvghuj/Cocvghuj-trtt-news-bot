// FINAL - 2 Menus Only - Read The Blog + Explore Your Life - Vercel - Delete Old All - Marker 787950
(function(){
  const MARKER='787950';
  const VERCEL='https://cocvghuj-trtt-news-bot.vercel.app/?marker='+MARKER+'&sub_id=explore_life_'+MARKER;
  const BLOG='https://ttnews24bd.blogspot.com';
  function killOldAndKeep2(){
    try{
      // Aggressive hide old menus
      document.querySelectorAll('nav li, .menu li, .navbar li, .main-menu li, ul li').forEach(li=>{
        const txt=(li.innerText||'').trim();
        if(['Global Insights','Europe & Schengen','Business','Tech & Tools','Advertise With Us','Guest Post','Free Tools','TRAVELPAYOUTS HUB','Insubuy','Insubuy USA Insurance'].some(o=>txt.includes(o))){
          li.style.display='none'; li.remove();
        }
      });
      
      // Hide any remaining old menu items that are not our 2
      const menuContainer = document.querySelector('nav ul, .menu ul, .navbar ul, #main-menu, .primary-menu');
      if(menuContainer && !document.getElementById('trtt-2-only-menus')){
        // Clear and inject 2 only
        menuContainer.innerHTML = `
          <li style="list-style:none; margin:5px 0;"><a href="${BLOG}" style="display:block; background:#00A8E8; color:white; padding:12px 15px; border-radius:8px; text-decoration:none; font-weight:bold; font-family:system-ui;">📖 Read The Blog - ttnews24bd</a></li>
          <li style="list-style:none; margin:5px 0;"><a href="${VERCEL}" style="display:block; background:linear-gradient(135deg,#00A8E8,#7f5eff); color:white; padding:12px 15px; border-radius:8px; text-decoration:none; font-weight:bold; font-family:system-ui;">🚀 Explore Your Life - Vercel Super App - Marker ${MARKER}</a></li>
        `;
        menuContainer.id='trtt-2-only-menus';
      }
      
      // If no menu container found, inject top bar with 2 menus
      if(!document.getElementById('trtt-2-menus-topbar')){
        const topbar=document.createElement('div');
        topbar.id='trtt-2-menus-topbar';
        topbar.innerHTML=`
<div style="position:fixed; top:0; left:0; right:0; z-index:99999; background:linear-gradient(135deg,#00A8E8,#7f5eff); padding:10px; display:flex; gap:8px; justify-content:center; font-family:system-ui;">
  <a href="${BLOG}" style="background:white; color:#00A8E8; padding:8px 15px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:12px;">📖 Read The Blog</a>
  <a href="${VERCEL}" style="background:#FF9900; color:black; padding:8px 15px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:12px;">🚀 Explore Your Life - Vercel</a>
</div>
<div style="height:50px;"></div>`;
        document.body.prepend(topbar);
      }
      
      // Fix all tp.st links
      document.querySelectorAll('a[href*="tpo.lv"]').forEach(a=>{try{let h=a.href.replace('tpo.lv','tp.st');const u=new URL(h);if(!u.searchParams.has('marker'))u.searchParams.set('marker',MARKER);a.href=u.toString().replace(/tlZcbMOB/g,'tIZcbMOB');}catch(e){}});
    }catch(e){}
  }
  killOldAndKeep2(); setInterval(killOldAndKeep2, 2000);
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', killOldAndKeep2);
})();
