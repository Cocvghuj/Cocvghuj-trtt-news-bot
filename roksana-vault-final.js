/*!
 * ROKSANA NILA — MULTI-TRILLION VAULT
 * Signature colors preserved: Golapi #ff2e63 | Kathali #FFC300 | Piaji #AF7AC5
 * Interactive client-side rooms. No fabricated IP/API/verification claims.
 */
(function () {
  'use strict';
  if (window.__ROKSANA_MULTI_TRILLION_VAULT__) return;
  window.__ROKSANA_MULTI_TRILLION_VAULT__ = true;
  var C = {g:'#ff2e63',k:'#FFC300',p:'#AF7AC5'};
  var rooms = [
    ['✦','The Welcome Hall','WELCOME',C.k,'Welcome to Roksana Nila’s Vault — a personal, carefully curated space built around Golapi, Kathali and Piaji.'],
    ['🌹','Golapi Archive','ROSE COLLECTION',C.g,'Golapi is the expressive heart of the Vault: bold, warm and unforgettable. Signature color: #ff2e63.'],
    ['👑','Kathali Treasury','GOLD COLLECTION',C.k,'Kathali brings the golden signature: radiant, confident and timeless. Signature color: #FFC300.'],
    ['💜','Piaji Gallery','VELVET COLLECTION',C.p,'Piaji adds the final note: elegant, imaginative and distinctive. Signature color: #AF7AC5.'],
    ['💎','The Crown Room','HIGHLIGHTS',C.k,'A dedicated space for featured pieces, favorite moments and special highlights. Add your chosen photographs and stories here.'],
    ['📖','Roksana’s Journal','STORIES',C.p,'A quiet corner for notes, memories, creative ideas and stories. New entries can be added to the blog whenever you choose.'],
    ['🖼️','Memory Gallery','PHOTO COLLECTION',C.g,'A gallery concept for photographs and keepsakes. Connect real gallery links or images when ready.'],
    ['✨','The Signature Edit','CURATED PICKS',C.k,'A curated collection where the three signature colors meet. Use it for featured designs, favorite posts or selected recommendations.'],
    ['🗝️','The Secret Garden','PRIVATE SPACE',C.p,'A visual doorway reserved for future private content. This panel is not password protection; real private access requires secure authentication.'],
    ['📝','Notes & Letters','MESSAGES',C.g,'A place for letters, notes and meaningful messages. Connect a real contact form or post link to receive messages.'],
    ['❔','The Help Desk','GUIDE',C.k,'Choose any of the twelve rooms to explore. Use the search field to find a room by name, collection or keyword.'],
    ['♡','The Heart of the Vault','ABOUT',C.p,'Made with care for the Roksana Nila identity. The three signature colors remain the foundation of the entire experience.']
  ];
  var css = \`
  #RoksanaFinalVault,#RoksanaFinalVault *{box-sizing:border-box}
  #RoksanaFinalVault{--g:\${C.g};--k:\${C.k};--p:\${C.p};width:min(1080px,calc(100% - 24px));margin:28px auto 36px;color:#fff;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;isolation:isolate}
  #RoksanaFinalVault .rv-shell{position:relative;overflow:hidden;border-radius:30px;padding:clamp(18px,4vw,42px);background:radial-gradient(ellipse at 12% 5%,rgba(255,46,99,.18),transparent 34%),radial-gradient(ellipse at 90% 12%,rgba(175,122,197,.2),transparent 35%),radial-gradient(ellipse at 50% 100%,rgba(255,195,0,.11),transparent 42%),linear-gradient(145deg,#0b0812,#15101e 52%,#090711);border:1px solid rgba(255,195,0,.55);box-shadow:0 28px 90px #0009,0 0 0 5px #af7ac514,0 0 55px #ff2e631f}
  #RoksanaFinalVault .rv-shell:before{content:"";position:absolute;inset:9px;border:1px solid #ffffff14;border-radius:23px;pointer-events:none}
  #RoksanaFinalVault .rv-topline{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;position:relative;z-index:1}
  #RoksanaFinalVault .rv-brand{display:flex;align-items:center;gap:10px;color:#fff;font-size:11px;font-weight:900;letter-spacing:.22em}
  #RoksanaFinalVault .rv-gem{width:12px;height:12px;transform:rotate(45deg);background:linear-gradient(135deg,var(--g),var(--k),var(--p));box-shadow:0 0 18px #ffc300a6}
  #RoksanaFinalVault .rv-clock{font-size:11px;color:#c9c2d2;letter-spacing:.08em}
  #RoksanaFinalVault .rv-hero{text-align:center;position:relative;z-index:1;padding:24px 0 10px}
  #RoksanaFinalVault .rv-eyebrow{font-size:10px;letter-spacing:.34em;color:var(--k);font-weight:900;text-transform:uppercase}
  #RoksanaFinalVault .rv-title{margin:12px 0 9px;font-family:Georgia,serif;font-size:clamp(28px,6vw,54px);line-height:1.04;background:linear-gradient(100deg,#fff2c0 5%,var(--k) 34%,#fff 52%,var(--p) 75%,#ffd3df);-webkit-background-clip:text;background-clip:text;color:transparent}
  #RoksanaFinalVault .rv-sub{max-width:610px;margin:0 auto;color:#d5ccdc;font-size:13px;line-height:1.75}
  #RoksanaFinalVault .rv-emblem{width:158px;height:158px;margin:24px auto 18px;display:grid;place-items:center;position:relative}
  #RoksanaFinalVault .rv-orbit{position:absolute;inset:5px;border-radius:50%;border:1px solid #ffc3008c;box-shadow:0 0 28px #ffc3001f,inset 0 0 25px #af7ac71f}
  #RoksanaFinalVault .rv-orbit:before,#RoksanaFinalVault .rv-orbit:after{content:"";position:absolute;inset:10px;border-radius:50%;border:1px dashed #af7ac78c}
  #RoksanaFinalVault .rv-orbit:after{inset:19px;border-color:#ff2e6380;transform:rotate(35deg)}
  #RoksanaFinalVault .rv-lock{width:92px;height:92px;border:1px solid #ffc300cc;border-radius:27px;background:linear-gradient(145deg,#ff2e633d,#ffc30029,#af7ac74d);box-shadow:0 0 35px #ffc3002e,inset 0 0 25px #ffffff0f;color:#ffe7a0;font-size:43px;cursor:pointer;display:grid;place-items:center;position:relative;z-index:2;transition:transform .25s,box-shadow .25s}
  #RoksanaFinalVault .rv-lock:hover{transform:translateY(-3px) scale(1.04);box-shadow:0 0 48px #ffc3004d}
  #RoksanaFinalVault button:focus-visible,#RoksanaFinalVault input:focus-visible{outline:3px solid #fff;outline-offset:3px}
  #RoksanaFinalVault .rv-triad{display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin:18px 0 28px}
  #RoksanaFinalVault .rv-chip{display:inline-flex;align-items:center;gap:8px;padding:9px 14px;border-radius:999px;background:#ffffff0b;border:1px solid #ffffff21;font-size:11px;font-weight:800;color:#f8f4fb}
  #RoksanaFinalVault .rv-dot{width:9px;height:9px;border-radius:50%;box-shadow:0 0 12px currentColor}
  #RoksanaFinalVault .rv-head{display:flex;align-items:end;justify-content:space-between;gap:12px;margin:22px 0 14px}
  #RoksanaFinalVault .rv-head h2{margin:0;color:#fff;font:700 20px Georgia,serif}
  #RoksanaFinalVault .rv-head p{margin:4px 0 0;color:#a99fb4;font-size:11px}
  #RoksanaFinalVault .rv-count{color:var(--k);font-size:10px;font-weight:900;letter-spacing:.16em}
  #RoksanaFinalVault .rv-search{display:flex;gap:8px;max-width:520px;margin:0 auto 20px;padding:6px;border-radius:15px;background:#0006;border:1px solid #ffc30059}
  #RoksanaFinalVault .rv-search input{min-width:0;flex:1;background:transparent;border:0;color:#fff;padding:9px 11px;font-size:13px}
  #RoksanaFinalVault .rv-search input::placeholder{color:#8f859b}
  #RoksanaFinalVault .rv-search button{border:0;border-radius:10px;padding:0 17px;background:linear-gradient(110deg,var(--g),#b84c9c);color:#fff;font-weight:900;font-size:11px;cursor:pointer}
  #RoksanaFinalVault .rv-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
  #RoksanaFinalVault .rv-room{min-height:130px;text-align:left;padding:16px 14px;border-radius:17px;position:relative;overflow:hidden;border:1px solid #ffffff21;background:linear-gradient(145deg,#ffffff13,#ffffff05);color:#fff;cursor:pointer;transition:transform .22s,border-color .22s,background .22s}
  #RoksanaFinalVault .rv-room:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--room-color)}
  #RoksanaFinalVault .rv-room:hover{transform:translateY(-4px);border-color:var(--room-color);background:linear-gradient(145deg,#ffffff1f,#ffffff09)}
  #RoksanaFinalVault .rv-roomicon{display:block;font-size:23px;margin-bottom:13px}
  #RoksanaFinalVault .rv-roomname{display:block;font-size:12px;font-weight:850;line-height:1.35}
  #RoksanaFinalVault .rv-roomtag{display:block;margin-top:6px;color:#a99fb4;font-size:9px;letter-spacing:.13em;font-weight:800}
  #RoksanaFinalVault .rv-room[hidden]{display:none}
  #RoksanaFinalVault .rv-empty{display:none;text-align:center;padding:20px;color:#c9c2d2;font-size:12px}
  #RoksanaFinalVault .rv-detail{display:none;margin:18px 0 0;padding:20px;border-radius:18px;background:linear-gradient(135deg,#ff2e631a,#af7ac71f,#ffc30014);border:1px solid #ffc30059;text-align:left}
  #RoksanaFinalVault .rv-detail.is-open{display:block}
  #RoksanaFinalVault .rv-detailtop{display:flex;justify-content:space-between;gap:12px;align-items:center}
  #RoksanaFinalVault .rv-detail h3{margin:0;color:var(--k);font:700 19px Georgia,serif}
  #RoksanaFinalVault .rv-detail p{margin:12px 0 0;color:#e6deeb;font-size:13px;line-height:1.75}
  #RoksanaFinalVault .rv-close{background:#ffffff14;border:1px solid #ffffff2e;color:#fff;border-radius:9px;padding:7px 11px;cursor:pointer}
  #RoksanaFinalVault .rv-footer{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:26px;padding-top:16px;border-top:1px solid #ffffff1a;color:#968ba2;font-size:10px}
  #RoksanaFinalVault .rv-footer strong{color:var(--k)}
  @media(max-width:720px){#RoksanaFinalVault{width:calc(100% - 14px);margin:14px auto 24px}#RoksanaFinalVault .rv-shell{padding:17px 13px;border-radius:22px}#RoksanaFinalVault .rv-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}#RoksanaFinalVault .rv-room{min-height:116px;padding:13px 11px}#RoksanaFinalVault .rv-roomicon{font-size:21px;margin-bottom:10px}#RoksanaFinalVault .rv-clock{font-size:9px}#RoksanaFinalVault .rv-emblem{width:138px;height:138px}#RoksanaFinalVault .rv-head h2{font-size:18px}#RoksanaFinalVault .rv-search button{padding:0 12px}}
  @media(prefers-reduced-motion:reduce){#RoksanaFinalVault *{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
  \`;
  function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
  function markup(){
    var cards=rooms.map(function(r,i){return '<button type="button" class="rv-room" data-room="'+i+'" style="--room-color:'+r[3]+'"><span class="rv-roomicon" aria-hidden="true">'+r[0]+'</span><span class="rv-roomname">'+esc(r[1])+'</span><span class="rv-roomtag">'+esc(r[2])+'</span></button>';}).join('');
    return '<section id="RoksanaFinalVault" aria-label="Roksana Nila Multi-Trillion Vault"><div class="rv-shell"><div class="rv-topline"><div class="rv-brand"><span class="rv-gem"></span> ROKSANA NILA ✦ PRIVATE COLLECTION</div><div class="rv-clock">YOUR LOCAL TIME · <span id="rv-time">--:--</span></div></div><header class="rv-hero"><div class="rv-eyebrow">A signature world of three colors</div><h1 class="rv-title">THE MULTI-TRILLION VAULT</h1><p class="rv-sub">A royal little universe of beauty, stories and treasured moments.<br>Tomar Jonno — This Vault is for You… তোমার জন্য</p><div class="rv-emblem"><div class="rv-orbit"></div><button class="rv-lock" id="rv-main-lock" type="button" aria-label="Open welcome room">♛</button></div><div class="rv-triad"><span class="rv-chip"><i class="rv-dot" style="background:'+C.g+';color:'+C.g+'"></i> GOLAPI</span><span class="rv-chip"><i class="rv-dot" style="background:'+C.k+';color:'+C.k+'"></i> KATHALI</span><span class="rv-chip"><i class="rv-dot" style="background:'+C.p+';color:'+C.p+'"></i> PIAJI</span></div></header><div class="rv-head"><div><h2>Explore the Twelve Rooms</h2><p>Choose a room to reveal its story</p></div><span class="rv-count">12 ROOMS · 3 COLORS</span></div><div class="rv-search"><input id="rv-search-input" type="search" placeholder="Find a room or collection…" aria-label="Search vault rooms"><button id="rv-search-clear" type="button">CLEAR</button></div><div class="rv-grid" id="rv-room-grid">'+cards+'</div><div class="rv-empty" id="rv-empty">No matching room. Try another word.</div><section class="rv-detail" id="rv-detail" aria-live="polite"><div class="rv-detailtop"><h3 id="rv-detail-title">Welcome</h3><button class="rv-close" id="rv-detail-close" type="button">CLOSE ×</button></div><p id="rv-detail-body"></p></section><footer class="rv-footer"><span><strong>GOLAPI</strong> · <strong>KATHALI</strong> · <strong>PIAJI</strong></span><span>Crafted with care for Roksana Nila</span></footer></div></section>';
  }
  function mount(){
    if(!document.body||document.getElementById('RoksanaFinalVault'))return;
    if(!document.getElementById('rv-multitrillion-style')){var st=document.createElement('style');st.id='rv-multitrillion-style';st.textContent=css;document.head.appendChild(st);}
    var old=document.getElementById('RoksanaFinalVault'),html=markup();
    if(old)old.outerHTML=html;
    else{var menu=document.getElementById('trtt-final-menu');if(menu&&menu.parentNode)menu.insertAdjacentHTML('afterend',html);else document.body.insertAdjacentHTML('afterbegin',html);}
    var root=document.getElementById('RoksanaFinalVault');if(!root)return;
    var detail=root.querySelector('#rv-detail'),heading=root.querySelector('#rv-detail-title'),body=root.querySelector('#rv-detail-body'),search=root.querySelector('#rv-search-input'),empty=root.querySelector('#rv-empty');
    function openRoom(i){var r=rooms[i];if(!r)return;heading.textContent=r[1];heading.style.color=r[3];body.textContent=r[4];detail.classList.add('is-open');detail.scrollIntoView({behavior:'smooth',block:'nearest'});}
    function filter(q){q=q.toLowerCase().trim();var n=0;root.querySelectorAll('.rv-room').forEach(function(b){var r=rooms[Number(b.getAttribute('data-room'))],ok=!q||(r.join(' ').toLowerCase().indexOf(q)!==-1);b.hidden=!ok;if(ok)n++;});empty.style.display=n?'none':'block';}
    root.addEventListener('click',function(e){var b=e.target.closest('[data-room]');if(b&&root.contains(b)){openRoom(Number(b.getAttribute('data-room')));return;}if(e.target.closest('#rv-main-lock')){openRoom(0);return;}if(e.target.closest('#rv-detail-close')){detail.classList.remove('is-open');return;}if(e.target.closest('#rv-search-clear')){search.value='';filter('');}});
    search.addEventListener('input',function(){filter(search.value);});
    function clock(){var el=root.querySelector('#rv-time');if(el)el.textContent=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}
    clock();window.setInterval(clock,30000);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount,{once:true});else mount();
})();