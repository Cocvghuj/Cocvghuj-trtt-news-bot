/* Roksana Nila Future Vault — Golapi #ff2e63 / Kathali #FFC300 / Piaji #AF7AC5 */
(function(){
'use strict';
var RV_ALLOWED_HOSTS=Object.freeze({
  'trttnews24bd.blogspot.com':true,
  'trttnews24bd.com':true,
  'www.trttnews24bd.com':true
});
var RV_CURRENT_HOST=String(window.location.hostname||'').toLowerCase();
if(!Object.prototype.hasOwnProperty.call(RV_ALLOWED_HOSTS,RV_CURRENT_HOST)){
  var rvExisting=document.getElementById('rv-future-mounted')||document.getElementById('RoksanaFinalVault');
  if(rvExisting)rvExisting.remove();
  var rvExistingStyle=document.getElementById('rv-future-style');
  if(rvExistingStyle)rvExistingStyle.remove();
  var rvLockWarning=document.createElement('div');
  rvLockWarning.id='rv-domain-lock';
  rvLockWarning.textContent='🔒 Strict Locked — this Vault is unavailable on this domain.';
  rvLockWarning.setAttribute('role','alert');
  rvLockWarning.style.cssText='margin:16px auto;padding:14px 18px;max-width:680px;border:1px solid #AF7AC5;border-radius:12px;background:#15111e;color:#fff;font:600 13px system-ui,sans-serif;text-align:center';
  (document.body||document.documentElement).appendChild(rvLockWarning);
  return;
}
if(window.__ROKSANA_FUTURE_VAULT__)return;
window.__ROKSANA_FUTURE_VAULT__=true;
var C={g:'#ff2e63',k:'#FFC300',p:'#AF7AC5'};
var THEMES=[
{name:'Signature',g:'#ff2e63',k:'#FFC300',p:'#AF7AC5'},
{name:'Rose Glow',g:'#FF4F86',k:'#FFD166',p:'#B99AEF'},
{name:'Sunset Pop',g:'#F43F75',k:'#F6C453',p:'#C4A1FF'},
{name:'Orchid Light',g:'#E94B8B',k:'#E8B84A',p:'#A78BFA'},
{name:'Candy Bloom',g:'#FF6B9A',k:'#FFC857',p:'#C084FC'},
{name:'Royal Petal',g:'#F05291',k:'#F4D06F',p:'#B49AF5'}
];
var R=[
['✦','Welcome Studio','START HERE',C.k,'Your entry point to the Roksana Nila universe.'],
['🌹','Golapi Archive','COLLECTION',C.g,'Bold, warm and unmistakable. Golapi signature: #ff2e63.'],
['👑','Kathali Treasury','COLLECTION',C.k,'Radiant, confident and timeless. Kathali signature: #FFC300.'],
['💜','Piaji Gallery','COLLECTION',C.p,'Elegant, imaginative and distinctive. Piaji signature: #AF7AC5.'],
['💎','The Crown Room','FEATURED',C.k,'A curated home for featured pieces and favorite moments.'],
['📖','Roksana Journal','STORIES',C.p,'A quiet editorial space for notes, memories and stories.'],
['▧','Memory Gallery','GALLERY',C.g,'A visual gallery for photographs and keepsakes.'],
['✧','Signature Edit','CURATED',C.k,'A considered mix of the three signature colors.'],
['⌘','Secret Garden','COMING SOON',C.p,'Reserved for future private content. This is not password protection.'],
['✉','Notes & Letters','MESSAGES',C.g,'A space for letters and thoughtful messages.'],
['◈','Help & Guide','SUPPORT',C.k,'Explore rooms and discover the meaning behind the Vault.'],
['♡','About Roksana','THE STORY',C.p,'A personal identity built around Golapi, Kathali and Piaji.']
];
var css=[
'#rv-future-mounted .rv-lock-status{display:inline-block;margin-left:8px;padding:4px 7px;border:1px solid #AF7AC5;border-radius:999px;color:#fff;font-size:9px;font-weight:800;letter-spacing:.04em;vertical-align:middle}',
'#rv-future-mounted{--g:#ff2e63;--k:#FFC300;--p:#AF7AC5;width:min(1180px,calc(100% - 20px));margin:22px auto 36px;color:#f8f5fb;font-family:Inter,system-ui,sans-serif}',
'#rv-future-mounted *{box-sizing:border-box}',
'#rv-future-mounted .app{overflow:hidden;border:1px solid #af7ac744;border-radius:25px;background:radial-gradient(ellipse at 8% 0%,#ff2e632b,transparent 34%),radial-gradient(ellipse at 100% 10%,#af7ac72b,transparent 32%),linear-gradient(145deg,#0b0911,#15111e 55%,#090710);box-shadow:0 28px 90px #0009}',
'#rv-future-mounted .top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 21px;border-bottom:1px solid #ffffff14;background:#090710aa}',
'#rv-future-mounted .brand{font-size:11px;font-weight:900;letter-spacing:.17em;color:#fff}',
'#rv-future-mounted .gem{display:inline-grid;place-items:center;width:28px;height:28px;margin-right:9px;border-radius:9px;background:linear-gradient(135deg,var(--g),var(--k),var(--p));color:#160e19}',
'#rv-future-mounted .time{font-size:10px;color:#a99fb4}',
'#rv-future-mounted .layout{display:grid;grid-template-columns:205px 1fr;min-height:650px}',
'#rv-future-mounted .side{padding:23px 13px;border-right:1px solid #ffffff12;background:#08070d66}',
'#rv-future-mounted .side small{display:block;padding:0 10px 10px;color:#81778d;font-size:9px;font-weight:900;letter-spacing:.2em}',
'#rv-future-mounted .nav{display:grid;gap:5px}',
'#rv-future-mounted .nav button{padding:11px 10px;border:1px solid transparent;border-radius:10px;background:transparent;color:#bdb4c8;text-align:left;font-size:11px;cursor:pointer}',
'#rv-future-mounted .nav button:hover,#rv-future-mounted .nav button.active{border-color:#ffc30044;background:#af7ac71c;color:#fff}',
'#rv-future-mounted .side .note{margin:25px 4px;padding:13px;border:1px solid #af7ac744;border-radius:12px;color:#aaa1b4;font-size:10px;line-height:1.7}',
'#rv-future-mounted .main{min-width:0;padding:clamp(17px,3vw,34px)}',
'#rv-future-mounted .hero{display:flex;justify-content:space-between;gap:15px;margin:4px 0 25px}',
'#rv-future-mounted .eyebrow{color:var(--k);font-size:9px;font-weight:900;letter-spacing:.23em}',
'#rv-future-mounted h1{margin:10px 0;color:#fff;font:700 clamp(29px,4vw,45px)/1.05 Georgia,serif}',
'#rv-future-mounted .gradient{background:linear-gradient(95deg,#fff,var(--k),var(--p),#ffc1d1);-webkit-background-clip:text;background-clip:text;color:transparent}',
'#rv-future-mounted .intro{max-width:590px;color:#aaa1b4;font-size:12px;line-height:1.8}',
'#rv-future-mounted .crown{width:76px;height:76px;flex:none;display:grid;place-items:center;border:1px solid #ffc30055;border-radius:23px;background:linear-gradient(145deg,#ff2e6325,#ffc30020,#af7ac72b);color:var(--k);font-size:34px}',
'#rv-future-mounted .swatches{display:flex;gap:7px;flex-wrap:wrap;margin-top:15px}',
'#rv-future-mounted .swatch{padding:7px 10px;border:1px solid #ffffff1c;border-radius:99px;color:#d6cfdd;font-size:9px;font-weight:800;letter-spacing:.08em}',
'#rv-future-mounted .toolbar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:22px 0 13px}',
'#rv-future-mounted h2{margin:0;color:#f7f2fa;font:700 18px Georgia,serif}',
'#rv-future-mounted .hint{margin-top:4px;color:#82798e;font-size:10px}',
'#rv-future-mounted .search{width:min(260px,48%);padding:10px 12px;border:1px solid #ffffff20;border-radius:10px;background:#0005;color:#fff}',
'#rv-future-mounted .search input{width:90%;border:0;outline:0;background:transparent;color:#fff;font-size:11px}',
'#rv-future-mounted .filters{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:13px}',
'#rv-future-mounted .filter{padding:7px 11px;border:1px solid #ffffff1c;border-radius:99px;background:transparent;color:#aaa1b4;font-size:9px;cursor:pointer}',
'#rv-future-mounted .filter.active{border-color:#ffc30066;background:#ffc30016;color:var(--k)}',
'#rv-future-mounted .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}',
'#rv-future-mounted .room{min-height:125px;padding:14px;border:1px solid #ffffff1b;border-radius:14px;background:linear-gradient(145deg,#ffffff12,#ffffff04);color:#fff;text-align:left;cursor:pointer;transition:.2s}',
'#rv-future-mounted .room:hover{transform:translateY(-3px);border-color:var(--rc);background:#ffffff16}',
'#rv-future-mounted .room[hidden]{display:none}',
'#rv-future-mounted .ico{display:grid;place-items:center;width:31px;height:31px;margin-bottom:13px;border-radius:9px;background:color-mix(in srgb,var(--rc),transparent 84%);color:var(--rc);font-size:16px}',
'#rv-future-mounted .room b{display:block;font-size:11px}',
'#rv-future-mounted .room small{display:block;margin-top:6px;color:#82798e;font-size:8px;font-weight:900;letter-spacing:.15em}',
'#rv-future-mounted .detail{display:none;margin-top:15px;padding:18px;border:1px solid #ffc30055;border-radius:14px;background:linear-gradient(100deg,#ff2e6318,#af7ac71c,#ffc30012)}',
'#rv-future-mounted .detail.open{display:block}',
'#rv-future-mounted .detail h3{margin:0;color:var(--k);font:700 18px Georgia,serif}',
'#rv-future-mounted .detail p{color:#c9c0d1;font-size:11px;line-height:1.8}',
'#rv-future-mounted .close{float:right;border:1px solid #ffffff22;border-radius:8px;background:#ffffff0c;color:#fff;padding:6px 9px;cursor:pointer}',
'#rv-future-mounted .foot{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:25px;padding-top:14px;border-top:1px solid #ffffff14;color:#766d81;font-size:9px}',
'@media(max-width:780px){#rv-future-mounted .layout{grid-template-columns:1fr}#rv-future-mounted .side{display:none}#rv-future-mounted .grid{grid-template-columns:repeat(2,minmax(0,1fr))}}',
'@media(max-width:520px){#rv-future-mounted{width:calc(100% - 10px)}#rv-future-mounted .top{padding:13px}#rv-future-mounted .main{padding:16px 12px}#rv-future-mounted .crown{width:53px;height:53px;font-size:24px}#rv-future-mounted .toolbar{align-items:stretch;flex-direction:column}#rv-future-mounted .search{width:100%}#rv-future-mounted .room{min-height:116px;padding:11px}}',
'@media(prefers-reduced-motion:reduce){#rv-future-mounted *{transition:none!important}}'
].join('\n') + '\n' + [
'#rv-future-mounted .app{background:radial-gradient(ellipse at 8% 0%,color-mix(in srgb,var(--g),transparent 82%),transparent 34%),radial-gradient(ellipse at 100% 10%,color-mix(in srgb,var(--p),transparent 80%),transparent 32%),linear-gradient(145deg,#0b0911,#15111e 55%,#090710)}',
'#rv-future-mounted .gem{background:linear-gradient(135deg,var(--g),var(--k),var(--p))}',
'#rv-future-mounted .eyebrow{color:var(--k)}',
'#rv-future-mounted .gradient{background-image:linear-gradient(95deg,#fff,var(--k),var(--p),var(--g));-webkit-background-clip:text;background-clip:text;color:transparent}',
'#rv-future-mounted .crown{border-color:color-mix(in srgb,var(--k),transparent 45%);background:linear-gradient(145deg,color-mix(in srgb,var(--g),transparent 84%),color-mix(in srgb,var(--k),transparent 86%),color-mix(in srgb,var(--p),transparent 82%));color:var(--k)}',
'#rv-future-mounted .swatch:nth-child(1){color:var(--g)}#rv-future-mounted .swatch:nth-child(2){color:var(--k)}#rv-future-mounted .swatch:nth-child(3){color:var(--p)}',
'#rv-future-mounted .nav button:hover,#rv-future-mounted .nav button.active{border-color:color-mix(in srgb,var(--k),transparent 55%);background:color-mix(in srgb,var(--p),transparent 87%)}',
'#rv-future-mounted .side .note{border-color:color-mix(in srgb,var(--p),transparent 55%)}',
'#rv-future-mounted .filter.active{border-color:color-mix(in srgb,var(--k),transparent 35%);background:color-mix(in srgb,var(--k),transparent 88%);color:var(--k)}',
'#rv-future-mounted .room,.#rv-future-mounted .ico{transition:color .9s ease,border-color .9s ease,background-color .9s ease,background .9s ease,box-shadow .9s ease,transform .2s ease}',
'#rv-future-mounted .gem,#rv-future-mounted .eyebrow,#rv-future-mounted .gradient,#rv-future-mounted .crown,#rv-future-mounted .swatch,#rv-future-mounted .filter,#rv-future-mounted .detail,#rv-future-mounted .detail h3{transition:color .9s ease,border-color .9s ease,background .9s ease,background-color .9s ease}',
'#rv-future-mounted .detail{border-color:color-mix(in srgb,var(--k),transparent 48%);background:linear-gradient(100deg,color-mix(in srgb,var(--g),transparent 89%),color-mix(in srgb,var(--p),transparent 88%),color-mix(in srgb,var(--k),transparent 91%))}',
'#rv-future-mounted .detail h3{color:var(--k)}'
].join('\n');
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function markup(){
var cards=R.map(function(r,i){return '<button class="room" type="button" data-room="'+i+'" data-cat="'+r[2]+'" style="--rc:'+r[3]+'"><span class="ico">'+r[0]+'</span><b>'+esc(r[1])+'</b><small>'+esc(r[2])+'</small></button>';}).join('');
return '<section id="RoksanaFinalVault" aria-label="Roksana Nila Future Vault"><div class="app"><header class="top"><div class="brand"><span class="gem">✦</span>ROKSANA NILA / VAULT <span class="rv-lock-status">🔒 Strict Locked</span></div><div class="time">LIVE THEME · 10 SEC · <span id="rv-clock">--:--</span></div></header><div class="layout"><aside class="side"><small>WORKSPACE</small><nav class="nav"><button class="active" data-filter="ALL">⌂　Overview</button><button data-filter="COLLECTION">◈　Collections</button><button data-filter="STORIES">▤　Stories</button><button data-filter="GALLERY">▧　Gallery</button><button data-filter="FEATURED">✧　Featured</button></nav><small style="margin-top:25px">THE SIGNATURE</small><div class="note">GOLAPI · KATHALI · PIAJI<br>Three colors. One identity. A personal world designed to feel timeless.</div></aside><main class="main"><div class="hero"><div><div class="eyebrow">THE NEXT CHAPTER · YOUR COLLECTION</div><h1>Welcome to the<br><span class="gradient">Future Vault.</span></h1><div class="intro">A refined digital home for stories, memories and signature collections. Explore the rooms and discover the world of Roksana Nila.</div><div class="swatches"><span class="swatch">● GOLAPI</span><span class="swatch">● KATHALI</span><span class="swatch">● PIAJI</span></div></div><div class="crown">♛</div></div><div class="toolbar"><div><h2>Explore your space</h2><div class="hint">12 thoughtfully designed rooms · Choose one to open</div></div><label class="search">⌕ <input id="rv-search" type="search" placeholder="Search your vault…"></label></div><div class="filters"><button class="filter active" data-filter="ALL">All rooms</button><button class="filter" data-filter="COLLECTION">Collections</button><button class="filter" data-filter="STORIES">Stories</button><button class="filter" data-filter="GALLERY">Gallery</button><button class="filter" data-filter="FEATURED">Featured</button></div><div class="grid">'+cards+'</div><div class="detail" id="rv-detail" aria-live="polite"><button class="close" id="rv-close">CLOSE ×</button><h3 id="rv-title"></h3><p id="rv-desc"></p></div><footer class="foot"><span>CRAFTED FOR ROKSANA NILA</span><span>GOLAPI · KATHALI · PIAJI</span><span>YOUR SPACE, YOUR STORY.</span></footer></main></div></div></section>';
}
function mount(){
if(!document.body||document.getElementById('rv-future-mounted'))return;
if(!document.getElementById('rv-future-style')){var st=document.createElement('style');st.id='rv-future-style';st.textContent=css;document.head.appendChild(st);}
var old=document.getElementById('RoksanaFinalVault'),html=markup();
if(old)old.outerHTML=html;else{var menu=document.getElementById('trtt-final-menu');if(menu&&menu.parentNode)menu.insertAdjacentHTML('afterend',html);else document.body.insertAdjacentHTML('afterbegin',html);}
var root=document.getElementById('RoksanaFinalVault');if(!root)return;root.id='rv-future-mounted';
var search=root.querySelector('#rv-search'),detail=root.querySelector('#rv-detail'),active='ALL';
var themeIndex=0;
function applyTheme(){var t=THEMES[themeIndex];root.style.setProperty('--g',t.g);root.style.setProperty('--k',t.k);root.style.setProperty('--p',t.p);root.setAttribute('data-theme',t.name);root.querySelectorAll('.room').forEach(function(card,i){card.style.setProperty('--rc',[t.g,t.k,t.p][i%3]);});themeIndex=(themeIndex+1)%THEMES.length;}
applyTheme();window.setInterval(applyTheme,10000);
function filter(){var q=search.value.toLowerCase().trim(),n=0;root.querySelectorAll('.room').forEach(function(b){var r=R[+b.dataset.room],ok=(active==='ALL'||r[2]===active||(active==='COLLECTION'&&r[2]==='COLLECTION'))&&(!q||(r.join(' ').toLowerCase().indexOf(q)>-1));b.hidden=!ok;if(ok)n++;});}
root.addEventListener('click',function(e){var card=e.target.closest('[data-room]');if(card){var r=R[+card.dataset.room];root.querySelector('#rv-title').textContent=r[1];root.querySelector('#rv-title').style.color=r[3];root.querySelector('#rv-desc').textContent=r[4];detail.classList.add('open');return;}var f=e.target.closest('[data-filter]');if(f){active=f.dataset.filter;root.querySelectorAll('[data-filter]').forEach(function(x){x.classList.toggle('active',x.dataset.filter===active);});filter();return;}if(e.target.closest('#rv-close'))detail.classList.remove('open');});
search.addEventListener('input',filter);
var clock=root.querySelector('#rv-clock');function tick(){clock.textContent=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}tick();window.setInterval(tick,30000);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount,{once:true});else mount();
})();