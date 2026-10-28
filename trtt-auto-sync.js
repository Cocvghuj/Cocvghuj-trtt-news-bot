// TRTT Auto-Sync Ecosystem Activated - One Source - AI Store App = Outside Blog/Website - Auto Update No Code
(function(){
  const CONFIG = {
    BLOG_JSON: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/blog.json',
    MARKER: '787950',
    BLOG_NAME: 'trttnews24bd'
  };
  async function autoSync(){
    try{
      const r = await fetch(CONFIG.BLOG_JSON + '?t=' + Date.now());
      if(!r.ok) throw new Error('blog.json not yet deployed');
      const data = await r.json();
      const container = document.getElementById('trtt-auto-posts');
      if(container && data.posts && data.posts.length){
        let html = '<div style="background:white; padding:15px; border-radius:12px; margin:10px 0; border:2px solid #00A8E8;"><h3 style="margin:0 0 10px;">🔄 Auto Synced from AI Store - Marker 787950</h3>';
        data.posts.slice(0,5).forEach(p=>{
          html += `<div style="border-bottom:1px solid #eee; padding:10px 0;"><h4 style="margin:5px 0;">${p.title}</h4><div>${p.html||''}</div><small style="color:#888;">${p.date||''} - Marker ${p.marker||CONFIG.MARKER}</small></div>`;
        });
        html += '</div>';
        container.innerHTML = html;
      }
      document.querySelectorAll('a[href*="tp.st"], a[href*="tpo.lv"]').forEach(a=>{
        try{ let href = a.href.replace('tpo.lv','tp.st'); const u = new URL(href); if(!u.searchParams.has('marker')) u.searchParams.set('marker', CONFIG.MARKER); a.href = u.toString().replace(/tlZcbMOB/g,'tIZcbMOB'); }catch(e){}
      });
      console.log('✅ TRTT Auto Sync - Blog ' + CONFIG.BLOG_NAME + ' - Marker ' + CONFIG.MARKER);
    }catch(e){ console.log('Auto Sync waiting - ' + e.message); }
  }
  autoSync(); setInterval(autoSync, 60000);
})();
