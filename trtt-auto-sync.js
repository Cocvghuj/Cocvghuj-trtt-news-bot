// TRTT Zero Theme Touch - Gadget Injection Only - Blog = AI Store Same Page - No Theme Change - Marker 787950
(function(){
  const BLOG_JSON = 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/blog.json';
  const MARKER = '787950';
  
  async function injectAISamePageWithoutThemeChange(){
    try{
      // Keep Eurovoyage Hub theme - Don't touch
      const euroHub = document.querySelector('.header, .top-bar, .logo, [class*="Eurovoyage"]');
      // If theme exists, keep it - Don't destroy
      
      // Create Super App Cards Container - Inject BEFORE posts, not replace theme
      if(!document.getElementById('trtt-ai-store-injection')){
        const container = document.createElement('div');
        container.id = 'trtt-ai-store-injection';
        container.innerHTML = `
<div style="background:white; border:2px solid #00A8E8; border-radius:12px; padding:12px; margin:10px; font-family:system-ui; box-shadow:0 4px 15px rgba(0,0,0,0.08);">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap;">
    <div style="font-weight:bold; font-size:14px;">🔴 Latest Posts (20) - TRTT NEWS 24 BD - TRTT - AI Store Same</div>
    <div style="background:#00A8E8; color:white; padding:3px 8px; border-radius:10px; font-size:9px;">Zero Theme Touch - Gadget Only ✅</div>
  </div>
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px,1fr)); gap:8px;">
    <div style="background:linear-gradient(135deg,#e0f8ff,#f0f0ff); padding:10px; border-radius:8px; text-align:center; border:1px solid #cceeff;">
      <div style="font-size:18px;">🗺️</div>
      <div style="font-size:11px; font-weight:bold; margin:3px 0;">Via Carlo Felice ARST 08:17</div>
      <a href="https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/app.html?marker=${MARKER}" style="background:#00A8E8; color:white; padding:4px 8px; border-radius:12px; text-decoration:none; font-size:10px;">Map</a>
    </div>
    <div style="background:linear-gradient(135deg,#ffe0e0,#fff0f0); padding:10px; border-radius:8px; text-align:center; border:1px solid #ffcccc;">
      <div style="font-size:18px;">✈️</div>
      <div style="font-size:11px; font-weight:bold; margin:3px 0;">【entity-AirHelp¦canonical_name=AirHelp】 600€ + Aviasales</div>
      <a href="https://airhelp.tp.st/3ItXS0E4?marker=${MARKER}&sub_id=gadget_airhelp_${MARKER}" style="background:#ff6b6b; color:white; padding:4px 8px; border-radius:12px; text-decoration:none; font-size:10px; margin:2px;">3ItXS0E4</a>
      <a href="https://aviasales.tp.st/Fb8U9yav?marker=${MARKER}&sub_id=gadget_aviasales_${MARKER}" style="background:#7f5eff; color:white; padding:4px 8px; border-radius:12px; text-decoration:none; font-size:10px; margin:2px;">Fb8U9yav</a>
    </div>
    <div style="background:linear-gradient(135deg,#e0ffe0,#f0fff0); padding:10px; border-radius:8px; text-align:center; border:1px solid #ccffcc;">
      <div style="font-size:18px;">📱</div>
      <div style="font-size:11px; font-weight:bold; margin:3px 0;">eSIM 4 Programs</div>
      <a href="https://airalo.tp.st/ZZoQC7Mz?marker=${MARKER}&sub_id=gadget_airalo_${MARKER}" style="background:#00d4aa; color:white; padding:4px 8px; border-radius:12px; text-decoration:none; font-size:10px;">ZZoQC7Mz</a>
      <a href="https://saily.tp.st/ssekmS4X?marker=${MARKER}&sub_id=gadget_saily_${MARKER}" style="background:#00A8E8; color:white; padding:4px 8px; border-radius:12px; text-decoration:none; font-size:10px;">ssekmS4X</a>
    </div>
  </div>
  <div style="margin-top:8px; text-align:center; font-size:9px; color:#888;">Blog = AI Store - Same Page - No Theme Change - Marker ${MARKER} Locked - tIZcbMOB Fixed - PIN 7879 Safe - Eurovoyage Hub Safe</div>
</div>`;
        
        // Inject before blog posts - Keep theme safe
        const postList = document.querySelector('.blog-posts, .post-feed, .main, #main, .content');
        if(postList) postList.insertBefore(container, postList.firstChild);
        else document.body.insertBefore(container, document.body.firstChild);
      }
      
      // Fix all tp.st links - marker locked + tIZcbMOB fixed
      document.querySelectorAll('a[href*="tp.st"], a[href*="tpo.lv"]').forEach(a=>{
        try{ let h = a.href.replace('tpo.lv','tp.st'); const u = new URL(h); if(!u.searchParams.has('marker')) u.searchParams.set('marker', MARKER); a.href = u.toString().replace(/tlZcbMOB/g,'tIZcbMOB'); }catch(e){}
      });
      
      console.log('✅ Blog = AI Store - Same Page - Zero Theme Touch - Eurovoyage Hub Safe - Marker ' + MARKER);
    }catch(e){ console.log('Gadget injection waiting - ' + e); }
  }
  
  injectAISamePageWithoutThemeChange();
  setInterval(injectAISamePageWithoutThemeChange, 30000);
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', injectAISamePageWithoutThemeChange);
})();
