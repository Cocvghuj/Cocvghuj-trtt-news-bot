// IDEA 13 - PRO LOCK - 7 POINT EXPERT SIGNAL - Marker 787950 LOCKED
(function(){
  if(window.TRTT_PRO_LOCKED) return; window.TRTT_PRO_LOCKED=true;
  const MARKER="787950";
  // 1. tp.st + FIXED tIZcbMOB (tlZcbMOB না)
  const LINKS={
    Aviasales:`https://aviasales.tp.st/Fb8U9yav?marker=${MARKER}`,
    AirHelp:`https://airhelp.tp.st/3ItXS0E4?marker=${MARKER}`,
    Airalo:`https://airalo.tp.st/ZZoQC7Mz?marker=${MARKER}`,
    Saily:`https://saily.tp.st/ssekmS4X?marker=${MARKER}`,
    Yesim:`https://yesim.tp.st/krzFKLpg?marker=${MARKER}`,
    Drimsim:`https://drimsim.tp.st/Ly7ywIY8?marker=${MARKER}`,
    Kiwitaxi:`https://kiwitaxi.tp.st/tIZcbMOB?marker=${MARKER}`, // FIXED tl -> tI
    Trip:`https://trip.tp.st/h3LrTZcS?marker=${MARKER}`,
    Tiqets:`https://tiqets.tp.st/bnx8pnF6?marker=${MARKER}`,
    Amazon:`https://amazon.tp.st/4shg6Hn?marker=${MARKER}`
  };

  // 2. SubID + UTM + country_code Auto
  async function getCountry(){ try{ let r=await fetch("https://ipapi.co/json/"); let d=await r.json(); return d.country_code.toLowerCase(); }catch(e){ return "it"; } }
  
  async function buildUrl(base, type){
    let c=await getCountry();
    let url=new URL(base);
    url.searchParams.set('subid',`trtt_lock_${c}`);
    url.searchParams.set('utm_source',`${type}_${c}`);
    url.searchParams.set('utm_medium','autonomous_network');
    return url.toString();
  }

  // 4. Real .it Domains Only
  const REAL_IT=["https://www.hotel-bernini.it","https://www.hotel-roma.it"];

  // 5. GDPR + Cookie + Popup + Privacy
  function addGDPR(){
    if(localStorage.getItem('trtt_cookie_consent_esim')) return;
    var b=document.createElement('div');
    b.innerHTML=`<div style='position:fixed;bottom:0;left:0;right:0;background:#000;color:#fff;padding:10px;text-align:center;z-index:99999;font-family:Arial;font-size:11px'>🍪 We use cookies + Affiliate Disclosure - <a href="/p/privacy.html" style="color:#FFC300">Privacy</a> <a href="/p/terms.html" style="color:#FFC300">Terms</a> <button id="trtt-ok" style="background:#FFC300;color:#000;border:none;padding:4px 10px;border-radius:10px;margin-left:8px'>OK</button></div>`;
    document.body.appendChild(b);
    document.getElementById('trtt-ok').onclick=()=>{ localStorage.setItem('trtt_cookie_consent_esim','yes'); b.remove(); };
  }

  // 6. GitHub Open Source Transparency Badge
  function addBadge(){
    var d=document.createElement('div');
    d.innerHTML=`<div style='max-width:900px;margin:10px auto;padding:8px;background:#0d001a;color:#00ff88;border:1px solid #00ff88;border-radius:8px;text-align:center;font-family:monospace;font-size:10px'>✅ PRO LOCKED: tp.st ONLY | Marker ${MARKER} | 10 Programs Full Stack | Real .it Only | GDPR OK | Open Source: github.com/Cocvghuj/Cocvghuj-trtt-news-bot | Live: cocvghuj.github.io/?marker=${MARKER} | TRTTVoyageHub ONE - 100 Features Vision - 3-5% vs Booking 20% | IP Auto EN/IT ACTIVE</div>`;
    var v=document.getElementById('RoksanaFinalVault'); if(v) v.after(d);
  }

  // 7. Vision Text
  window.TRTT_LINKS=LINKS;
  window.TRTT_buildUrl=buildUrl;

  addGDPR(); addBadge();
  console.log("%cTRTT PRO LOCK ACTIVE - Marker 787950 - 10 Programs","background:#000;color:gold;padding:6px");
})();
