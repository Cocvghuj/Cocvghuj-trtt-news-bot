/* Roksana Nila Future Vault — Golapi #ff2e63 / Kathali #FFC300 / Piaji #AF7AC5 */
(function(){
'use strict';
if(window.__ROKSANA_FUTURE_VAULT__)return;
window.__ROKSANA_FUTURE_VAULT__=true;
var C={g:'#ff2e63',k:'#FFC300',p:'#AF7AC5'};
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
'#RoksanaFinalVault{--g:#ff2e63;--k:#FFC300;--p:#AF7AC5;width:min(1180px,calc(100% - 20px));margin:22px auto 36px;color:#f8f5fb;font-family:Inter,system-ui,sans-serif}',
'#RoksanaFinalVault *{box-sizing:border-box}',
'#RoksanaFinalVault .app{overflow:hidden;border:1px solid #af7ac744;border-radius:25px;background:radial-gradient(ellipse at 8% 0%,#ff2e632b,transparent 34%),radial-gradient(ellipse at 100% 10%,#af7ac72b,transparent 32%),linear-gradient(145deg,#0b0911,#15111e 55%,#090710);box-shadow:0 28px 90px #0009}',
'#RoksanaFinalVault .top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 21px;border-bottom:1px solid #ffffff14;background:#090710aa}',
'#RoksanaFinalVault .brand{font-size:11px;font-weight:900;letter-spacing:.17em;color:#fff}',
'#RoksanaFinalVault .gem{display:inline-grid;place-items:center;width:28px;height:28px;margin-right:9px;border-radius:9px;background:linear-gradient(135deg,var(--g),var(--k),var(--p));color:#160e19}',
'#RoksanaFinalVault .time{font-size:10px;color:#a99fb4}',
'#RoksanaFinalVault .layout{display:grid;grid-template-columns:205px 1fr;min-height:650px}',
'#RoksanaFinalVault .side{padding:23px 13px;border-right:1px solid #ffffff12;background:#08070d66}',
'#RoksanaFinalVault .side small{display:block;padding:0 10px 10px;color:#81778d;font-size:9px;font-weight:900;letter-spacing:.2em}',
'#RoksanaFinalVault .nav{display:grid;gap:5px}',
'#RoksanaFinalVault .nav button{padding:11px 10px;border:1px solid transparent;border-radius:10px;background:transparent;color:#bdb4c8;text-align:left;font-size:11px;cursor:pointer}',
'#RoksanaFinalVault .nav button:hover,#RoksanaFinalVault .nav button.active{border-color:#ffc30044;background:#af7ac71c;color:#fff}',
'#RoksanaFinalVault .side .note{margin:25px 4px;padding:13px;border:1px solid #af7ac744;border-radius:12px;color:#aaa1b4;font-size:10px;line-height:1.7}',
'#RoksanaFinalVault .main{min-width:0;padding:clamp(17px,3vw,34px)}',
'#RoksanaFinalVault .hero{display:flex;justify-content:space-between;gap:15px;margin:4px 0 25px}',
'#RoksanaFinalVault .eyebrow{color:var(--k);font-size:9px;font-weight:900;letter-spacing:.23em}',
'#RoksanaFinalVault h1{margin:10px 0;color:#fff;font:700 clamp(29px,4vw,45px)/1.05 Georgia,serif}',
'#RoksanaFinalVault .gradient{background:linear-gradient(95deg,#fff,var(--k),var(--p),#ffc1d1);-webkit-background-clip:text;background-clip:text;color:transparent}',
'#RoksanaFinalVault .intro{max-width:590px;color:#aaa1b4;font-size:12px;line-height:1.8}',
'#RoksanaFinalVault .crown{width:76px;height:76px;flex:none;display:grid;place-items:center;border:1px solid #ffc30055;border-radius:23px;background:linear-gradient(145deg,#ff2e6325,#ffc30020,#af7ac72b);color:var(--k);font-size:34px}',
'#RoksanaFinalVault .swatches{display:flex;gap:7px;flex-wrap:wrap;margin-top:15px}',
'#RoksanaFinalVault .swatch{padding:7px 10px;border:1px solid #ffffff1c;border-radius:99px;color:#d6cfdd;font-size:9px;font-weight:800;letter-spacing:.08em}',
'#RoksanaFinalVault .toolbar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:22px 0 13px}',
'#RoksanaFinalVault h2{margin:0;color:#f7f2fa;font:700 18px Georgia,serif}',
'#RoksanaFinalVault .hint{margin-top:4px;color:#82798e;font-size:10px}',
'#RoksanaFinalVault .search{width:min(260px,48%);padding:10px 12px;border:1px solid #ffffff20;border-radius:10px;background:#0005;color:#fff}',
'#RoksanaFinalVault .search input{width:90%;border:0;outline:0;background:transparent;color:#fff;font-size:11px}',
'#RoksanaFinalVault .filters{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:13px}',
'#RoksanaFinalVault .filter{padding:7px 11px;border:1px solid #ffffff1c;border-radius:99px;background:transparent;color:#aaa1b4;font-size:9px;cursor:pointer}',
'#RoksanaFinalVault .filter.active{border-color:#ffc30066;background:#ffc30016;color:var(--k)}',
'#RoksanaFinalVault .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}',
'#RoksanaFinalVault .room{min-height:125px;padding:14px;border:1px solid #ffffff1b;border-radius:14px;background:linear-gradient(145deg,#ffffff12,#ffffff04);color:#fff;text-align:left;cursor:pointer;transition:.2s}',
'#RoksanaFinalVault .room:hover{transform:translateY(-3px);border-color:var(--rc);background:#ffffff16}',
'#RoksanaFinalVault .room[hidden]{display:none}',
'#RoksanaFinalVault .ico{display:grid;place-items:center;width:31px;height:31px;margin-bottom:13px;border-radius:9px;background:color-mix(in srgb,var(--rc),transparent 84%);color:var(--rc);font-size:16px}',
'#RoksanaFinalVault .room b{display:block;font-size:11px}',
'#RoksanaFinalVault .room small{display:block;margin-top:6px;color:#82798e;font-size:8px;font-weight:900;letter-spacing:.15em}',
'#RoksanaFinalVault .detail{display:none;margin-top:15px;padding:18px;border:1px solid #ffc30055;border-radius:14px;background:linear-gradient(100deg,#ff2e6318,#af7ac71c,#ffc30012)}',
'#RoksanaFinalVault .detail.open{display:block}',
'#RoksanaFinalVault .detail h3{margin:0;color:var(--k);font:700 18px Georgia,serif}',
'#RoksanaFinalVault .detail p{color:#c9c0d1;font-size:11px;line-height:1.8}',
'#RoksanaFinalVault .close{float:right;border:1px solid #ffffff22;border-radius:8px;background:#ffffff0c;color:#fff;padding:6px 9px;cursor:pointer}',
'#RoksanaFinalVault .foot{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:25px;padding-top:14px;border-top:1px solid #ffffff14;color:#766d81;font-size:9px}',
'@media(max-width:780px){#RoksanaFinalVault .layout{grid-template-columns:1fr}#RoksanaFinalVault .side{display:none}#RoksanaFinalVault .grid{grid-template-columns:repeat(2,minmax(0,1fr))}}',
'@media(max-width:520px){#RoksanaFinalVault{width:calc(100% - 10px)}#RoksanaFinalVault .top{padding:13px}#RoksanaFinalVault .main{padding:16px 12px}#RoksanaFinalVault .crown{width:53px;height:53px;font-size:24px}#RoksanaFinalVault .toolbar{align-items:stretch;flex-direction:column}#RoksanaFinalVault .search{width:100%}#RoksanaFinalVault .room{min-height:116px;padding:11px}}',
'@media(prefers-reduced-motion:reduce){#RoksanaFinalVault *{transition:none!important}}'
].join('\n');
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function markup(){
var cards=R.map(function(r,i){return '<button class="room" type="button" data-room="'+i+'" data-cat="'+r[2]+'" style="--rc:'+r[3]+'"><span class="ico">'+r[0]+'</span><b>'+esc(r[1])+'</b><small>'+esc(r[2])+'</small></button>';}).join('');
return '<section id="RoksanaFinalVault" aria-label="Roksana Nila Future Vault"><div class="app"><header class="top"><div class="brand"><span class="gem">✦</span>ROKSANA NILA / VAULT</div><div class="time">YOUR SPACE · <span id="rv-clock">--:--</span></div></header><div class="layout"><aside class="side"><small>WORKSPACE</small><nav class="nav"><button class="active" data-filter="ALL">⌂　Overview</button><button data-filter="COLLECTION">◈　Collections</button><button data-filter="STORIES">▤　Stories</button><button data-filter="GALLERY">▧　Gallery</button><button data-filter="FEATURED">✧　Featured</button></nav><small style="margin-top:25px">THE SIGNATURE</small><div class="note">GOLAPI · KATHALI · PIAJI<br>Three colors. One identity. A personal world designed to feel timeless.</div></aside><main class="main"><div class="hero"><div><div class="eyebrow">THE NEXT CHAPTER · YOUR COLLECTION</div><h1>Welcome to the<br><span class="gradient">Future Vault.</span></h1><div class="intro">A refined digital home for stories, memories and signature collections. Explore the rooms and discover the world of Roksana Nila.</div><div class="swatches"><span class="swatch">● GOLAPI</span><span class="swatch">● KATHALI</span><span class="swatch">● PIAJI</span></div></div><div class="crown">♛</div></div><div class="toolbar"><div><h2>Explore your space</h2><div class="hint">12 thoughtfully designed rooms · Choose one to open</div></div><label class="search">⌕ <input id="rv-search" type="search" placeholder="Search your vault…"></label></div><div class="filters"><button class="filter active" data-filter="ALL">All rooms</button><button class="filter" data-filter="COLLECTION">Collections</button><button class="filter" data-filter="STORIES">Stories</button><button class="filter" data-filter="GALLERY">Gallery</button><button class="filter" data-filter="FEATURED">Featured</button></div><div class="grid">'+cards+'</div><div class="detail" id="rv-detail" aria-live="polite"><button class="close" id="rv-close">CLOSE ×</button><h3 id="rv-title"></h3><p id="rv-desc"></p></div><footer class="foot"><span>CRAFTED FOR ROKSANA NILA</span><span>GOLAPI · KATHALI · PIAJI</span><span>YOUR SPACE, YOUR STORY.</span></footer></main></div></div></section>';
}
function mount(){
if(!document.body||document.getElementById('rv-future-mounted'))return;
if(!document.getElementById('rv-future-style')){var st=document.createElement('style');st.id='rv-future-style';st.textContent=css;document.head.appendChild(st);}
var old=document.getElementById('RoksanaFinalVault'),html=markup();
if(old)old.outerHTML=html;else{var menu=document.getElementById('trtt-final-menu');if(menu&&menu.parentNode)menu.insertAdjacentHTML('afterend',html);else document.body.insertAdjacentHTML('afterbegin',html);}
var root=document.getElementById('RoksanaFinalVault');if(!root)return;root.id='rv-future-mounted';
var search=root.querySelector('#rv-search'),detail=root.querySelector('#rv-detail'),active='ALL';
function filter(){var q=search.value.toLowerCase().trim(),n=0;root.querySelectorAll('.room').forEach(function(b){var r=R[+b.dataset.room],ok=(active==='ALL'||r[2]===active||(active==='COLLECTION'&&r[2]==='COLLECTION'))&&(!q||(r.join(' ').toLowerCase().indexOf(q)>-1));b.hidden=!ok;if(ok)n++;});}
root.addEventListener('click',function(e){var card=e.target.closest('[data-room]');if(card){var r=R[+card.dataset.room];root.querySelector('#rv-title').textContent=r[1];root.querySelector('#rv-title').style.color=r[3];root.querySelector('#rv-desc').textContent=r[4];detail.classList.add('open');return;}var f=e.target.closest('[data-filter]');if(f){active=f.dataset.filter;root.querySelectorAll('[data-filter]').forEach(function(x){x.classList.toggle('active',x.dataset.filter===active);});filter();return;}if(e.target.closest('#rv-close'))detail.classList.remove('open');});
search.addEventListener('input',filter);
var clock=root.querySelector('#rv-clock');function tick(){clock.textContent=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}tick();window.setInterval(tick,30000);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount,{once:true});else mount();
})();