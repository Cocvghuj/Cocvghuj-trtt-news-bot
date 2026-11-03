/*!
 * ROKSANA NILA / FUTURE VAULT
 * Signature palette preserved: Golapi #ff2e63 · Kathali #FFC300 · Piaji #AF7AC5
 * Interactive front-end experience. No false claims of authentication, AI, or visitor verification.
 */
(function () {
  'use strict';
  if (window.__ROKSANA_FUTURE_VAULT__) return;
  window.__ROKSANA_FUTURE_VAULT__ = true;

  var palette = { golapi: '#ff2e63', kathali: '#FFC300', piaji: '#AF7AC5' };
  var rooms = [
    {icon:'✦',name:'Welcome Studio',category:'START HERE',color:palette.kathali,desc:'Your entry point to the Roksana Nila universe. A calm, personal space shaped by three signature colors.'},
    {icon:'🌹',name:'Golapi Archive',category:'COLLECTION',color:palette.golapi,desc:'The Golapi collection — expressive, warm and unmistakable. The signature rose tone is #ff2e63.'},
    {icon:'👑',name:'Kathali Treasury',category:'COLLECTION',color:palette.kathali,desc:'The Kathali collection — radiant, confident and timeless. The signature golden tone is #FFC300.'},
    {icon:'💜',name:'Piaji Gallery',category:'COLLECTION',color:palette.piaji,desc:'The Piaji collection — imaginative, elegant and distinctive. The signature violet tone is #AF7AC5.'},
    {icon:'💎',name:'The Crown Room',category:'FEATURED',color:palette.kathali,desc:'A curated home for featured pieces, favorite moments and special highlights.'},
    {icon:'📖',name:'Roksana Journal',category:'STORIES',color:palette.piaji,desc:'A quiet editorial space for notes, memories, creative ideas and stories.'},
    {icon:'▧',name:'Memory Gallery',category:'GALLERY',color:palette.golapi,desc:'A visual gallery for photographs, keepsakes and moments worth revisiting.'},
    {icon:'✧',name:'Signature Edit',category:'CURATED',color:palette.kathali,desc:'A considered mix of the three signature colors, selected stories and favorite details.'},
    {icon:'⌘',name:'Secret Garden',category:'COMING SOON',color:palette.piaji,desc:'A reserved doorway for future private content. This visual room is not password protection; private access needs secure authentication.'},
    {icon:'✉',name:'Notes & Letters',category:'MESSAGES',color:palette.golapi,desc:'A space for letters and thoughtful messages. Connect a real contact form to receive submissions.'},
    {icon:'◈',name:'Help & Guide',category:'SUPPORT',color:palette.kathali,desc:'Explore the rooms, search collections and discover the meaning behind the Vault.'},
    {icon:'♡',name:'About Roksana',category:'THE STORY',color:palette.piaji,desc:'The heart of the Vault: a personal identity built around Golapi, Kathali and Piaji.'}
  ];

  var css = [
    '#RoksanaFinalVault{--rv-g:#ff2e63;--rv-k:#FFC300;--rv-p:#AF7AC5;color:#f8f5fb;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;width:min(1180px,calc(100% - 24px));margin:24px auto 40px;isolation:isolate}',
    '#RoksanaFinalVault *{box-sizing:border-box}',
    '#RoksanaFinalVault .rv-app{position:relative;overflow:hidden;border:1px solid rgba(175,122,197,.28);border-radius:26px;background:radial-gradient(ellipse at 8% 0%,rgba(255,46,99,.16),transparent 32%),radial-gradient(ellipse at 100% 12%,rgba(175,122,197,.16),transparent 30%),linear-gradient(145deg,#0b0911,#12101a 55%,#0a0810);box-shadow:0 30px 100px rgba(0,0,0,.48)}',
    '#RoksanaFinalVault .rv-app:before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.22;background-image:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:34px 34px;mask-image:linear-gradient(to bottom,black,transparent 78%)}',
    '#RoksanaFinalVault .rv-top{position:relative;z-index:2;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:17px 22px;border-bottom:1px solid rgba(255,255,255,.08);background:rgba(9,7,14,.64);backdrop-filter:blur(18px)}',
    '#RoksanaFinalVault .rv-brand{display:flex;align-items:center;gap:11px;min-width:0;font-size:11px;font-weight:900;letter-spacing:.17em;color:#fff}',
    '#RoksanaFinalVault .rv-mark{width:29px;height:29px;display:grid;place-items:center;flex:none;border-radius:10px;color:#1a1019;font-size:16px;background:linear-gradient(135deg,var(--rv-g),var(--rv-k) 52%,var(--rv-p));box-shadow:0 0 22px rgba(255,195,0,.2)}',
    '#RoksanaFinalVault .rv-topright{display:flex;align-items:center;gap:12px;color:#aaa1b4;font-size:10px}',
    '#RoksanaFinalVault .rv-live-dot{width:7px;height:7px;display:inline-block;border-radius:50%;background:var(--rv-p);box-shadow:0 0 12px var(--rv-p);margin-right:6px}',
    '#RoksanaFinalVault .rv-layout{position:relative;z-index:1;display:grid;grid-template-columns:218px minmax(0,1fr);min-height:700px}',
    '#RoksanaFinalVault .rv-side{padding:23px 14px;border-right:1px solid rgba(255,255,255,.075);background:rgba(8,7,13,.27)}',
    '#RoksanaFinalVault .rv-side-label{padding:0 10px;margin:8px 0 10px;color:#82798e;font-size:9px;font-weight:900;letter-spacing:.18em}',
    '#RoksanaFinalVault .rv-nav{display:grid;gap:5px}',
    '#RoksanaFinalVault .rv-nav button{display:flex;align-items:center;gap:11px;width:100%;padding:11px 10px;border:1px solid transparent;border-radius:11px;background:transparent;color:#bcb4c7;text-align:left;font:600 11px inherit;cursor:pointer;transition:.2s}',
    '#RoksanaFinalVault .rv-nav button:hover,#RoksanaFinalVault .rv-nav button.is-active{color:#fff;border-color:rgba(255,195,0,.19);background:linear-gradient(90deg,rgba(255,46,99,.13),rgba(175,122,197,.1))}',
    '#RoksanaFinalVault .rv-nav-ico{width:22px;text-align:center;font-size:15px;color:var(--rv-k)}',
    '#RoksanaFinalVault .rv-side-note{margin:28px 5px 0;padding:13px;border:1px solid rgba(175,122,197,.2);border-radius:13px;background:rgba(175,122,197,.07);color:#aaa1b4;font-size:10px;line-height:1.7}',
    '#RoksanaFinalVault .rv-side-note strong{display:block;margin-bottom:4px;color:#e8d8f2;font-size:10px}',
    '#RoksanaFinalVault .rv-main{min-width:0;padding:clamp(18px,3vw,34px)}',
    '#RoksanaFinalVault .rv-welcome{display:flex;align-items:flex-start;justify-content:space-between;gap:18px;margin:4px 0 25px}',
    '#RoksanaFinalVault .rv-kicker{color:var(--rv-k);font-size:9px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}',
    '#RoksanaFinalVault .rv-h1{margin:9px 0 8px;color:#fff;font:700 clamp(28px,4vw,43px)/1.05 Georgia,"Times New Roman",serif;letter-spacing:-.025em}',
    '#RoksanaFinalVault .rv-gradient{background:linear-gradient(95deg,#fff,var(--rv-k) 38%,var(--rv-p) 72%,#ffc1d1);-webkit-background-clip:text;background-clip:text;color:transparent}',
    '#RoksanaFinalVault .rv-intro{max-width:590px;margin:0;color:#aaa1b4;font-size:12px;line-height:1.8}',
    '#RoksanaFinalVault .rv-crown{width:78px;height:78px;display:grid;place-items:center;flex:none;border:1px solid rgba(255,195,0,.32);border-radius:24px;background:linear-gradient(145deg,rgba(255,46,99,.15),rgba(255,195,0,.1),rgba(175,122,197,.17));color:var(--rv-k);font-size:35px;box-shadow:inset 0 0 25px rgba(255,255,255,.035),0 0 40px rgba(255,195,0,.07)}',
    '#RoksanaFinalVault .rv-palette{display:flex;gap:7px;flex-wrap:wrap;margin-top:15px}',
    '#RoksanaFinalVault .rv-swatch{display:inline-flex;align-items:center;gap:7px;padding:7px 10px;border:1px solid rgba(255,255,255,.1);border-radius:999px;background:rgba(255,255,255,.035);color:#d6cfdd;font-size:9px;font-weight:800;letter-spacing:.08em}',
    '#RoksanaFinalVault .rv-swatch i{width:8px;height:8px;border-radius:50%;box-shadow:0 0 10px currentColor}',
    '#RoksanaFinalVault .rv-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:24px 0 15px}',
    '#RoksanaFinalVault .rv-toolbar h2{margin:0;color:#f7f2fa;font:700 18px Georgia,serif}',
    '#RoksanaFinalVault .rv-toolbar p{margin:4px 0 0;color:#82798e;font-size:10px}',
    '#RoksanaFinalVault .rv-search{width:min(270px,48%);display:flex;align-items:center;gap:8px;padding:9px 11px;border:1px solid rgba(255,255,255,.12);border-radius:11px;background:rgba(0,0,0,.22);color:#92899d}',
    '#RoksanaFinalVault .rv-search input{width:100%;min-width:0;border:0;outline:0;background:transparent;color:#fff;font:11px inherit}',
    '#RoksanaFinalVault .rv-search input::placeholder{color:#71697d}',
    '#RoksanaFinalVault .rv-filters{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px}',
    '#RoksanaFinalVault .rv-filter{padding:7px 11px;border:1px solid rgba(255,255,255,.1);border-radius:999px;background:transparent;color:#a69daf;font-size:9px;font-weight:800;cursor:pointer}',
    '#RoksanaFinalVault .rv-filter.is-active{border-color:rgba(255,195,0,.42);background:rgba(255,195,0,.09);color:var(--rv-k)}',
    '#RoksanaFinalVault .rv-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:11px}',
    '#RoksanaFinalVault .rv-card{position:relative;min-height:132px;padding:15px 14px;border:1px solid rgba(255,255,255,.105);border-radius:15px;background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.018));color:#fff;text-align:left;cursor:pointer;overflow:hidden;transition:transform .2s,border-color .2s,background .2s}',
    '#RoksanaFinalVault .rv-card:after{content:"";position:absolute;right:-27px;bottom:-39px;width:92px;height:92px;border-radius:50%;background:var(--room-color);opacity:.09;filter:blur(19px);transition:opacity .2s}',
    '#RoksanaFinalVault .rv-card:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--room-color),transparent 35%);background:linear-gradient(145deg,rgba(255,255,255,.105),rgba(255,255,255,.025))}',
    '#RoksanaFinalVault .rv-card:hover:after{opacity:.22}',
    '#RoksanaFinalVault .rv-card[hidden]{display:none}',
    '#RoksanaFinalVault .rv-cardtop{display:flex;align-items:center;justify-content:space-between;margin-bottom:15px}',
    '#RoksanaFinalVault .rv-icon{width:31px;height:31px;display:grid;place-items:center;border-radius:10px;background:color-mix(in srgb,var(--room-color),transparent 87%);color:var(--room-color);font-size:16px}',
    '#RoksanaFinalVault .rv-arrow{color:#655d70;font-size:13px}',
    '#RoksanaFinalVault .rv-cardname{display:block;color:#f5f0f8;font-size:11px;font-weight:800;line-height:1.35}',
    '#RoksanaFinalVault .rv-cardcat{display:block;margin-top:5px;color:#81788d;font-size:8px;font-weight:900;letter-spacing:.15em}',
    '#RoksanaFinalVault .rv-empty{display:none;padding:24px;text-align:center;color:#aaa1b4;font-size:11px}',
    '#RoksanaFinalVault .rv-detail{display:none;margin-top:15px;padding:18px;border:1px solid rgba(255,195,0,.25);border-radius:15px;background:linear-gradient(110deg,rgba(255,46,99,.09),rgba(175,122,197,.1),rgba(255,195,0,.06))}',
    '#RoksanaFinalVault .rv-detail.is-open{display:block}',
    '#RoksanaFinalVault .rv-detailhead{display:flex;align-items:center;justify-content:space-between;gap:12px}',
    '#RoksanaFinalVault .rv-detail h3{margin:0;color:var(--rv-k);font:700 18px Georgia,serif}',
    '#RoksanaFinalVault .rv-detail p{margin:10px 0 0;color:#c9c0d1;font-size:11px;line-height:1.8}',
    '#RoksanaFinalVault .rv-close{padding:7px 10px;border:1px solid rgba(255,255,255,.13);border-radius:9px;background:rgba(255,255,255,.05);color:#ddd5e5;font-size:9px;cursor:pointer}',
    '#RoksanaFinalVault .rv-bottom{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:27px;padding-top:15px;border-top:1px solid rgba(255,255,255,.08);color:#766d81;font-size:9px}',
    '#RoksanaFinalVault .rv-bottom b{color:var(--rv-k);font-weight:800}',
    '#RoksanaFinalVault button:focus-visible,#RoksanaFinalVault input:focus-visible{outline:2px solid #fff;outline-offset:3px}',
    '@media(max-width:820px){#RoksanaFinalVault .rv-layout{grid-template-columns:1fr}#RoksanaFinalVault .rv-side{display:none}#RoksanaFinalVault .rv-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}',
    '@media(max-width:520px){#RoksanaFinalVault{width:calc(100% - 12px);margin:12px auto 24px}#RoksanaFinalVault .rv-app{border-radius:19px}#RoksanaFinalVault .rv-top{padding:13px 14px}#RoksanaFinalVault .rv-topright{font-size:9px}#RoksanaFinalVault .rv-main{padding:17px 13px}#RoksanaFinalVault .rv-crown{width:54px;height:54px;border-radius:17px;font-size:25px}#RoksanaFinalVault .rv-welcome{gap:8px}#RoksanaFinalVault .rv-toolbar{align-items:flex-start;flex-direction:column}#RoksanaFinalVault .rv-search{width:100%}#RoksanaFinalVault .rv-grid{gap:8px}#RoksanaFinalVault .rv-card{min-height:119px;padding:12px 10px}#RoksanaFinalVault .rv-cardtop{margin-bottom:12px}}',
    '@media(prefers-reduced-motion:reduce){#RoksanaFinalVault *{scroll-behavior:auto!important;transition:none!important}}'
  ].join('\n');

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function render() {
    var cards = rooms.map(function (r, i) {
      return '<button type="button" class="rv-card" data-room="' + i + '" data-category="' + esc(r.category) + '" style="--room-color:' + r.color + '">' +
        '<span class="rv-cardtop"><span class="rv-icon">' + r.icon + '</span><span class="rv-arrow">↗</span></span>' +
        '<span class="rv-cardname">' + esc(r.name) + '</span><span class="rv-cardcat">' + esc(r.category) + '</span></button>';
    }).join('');
    return '<section id="RoksanaFinalVault" aria-label="Roksana Nila Future Vault">' +
      '<div class="rv-app"><header class="rv-top"><div class="rv-brand"><span class="rv-mark">✦</span><span>ROKSANA NILA <span style="color:#AF7AC5">/</span> VAULT</span></div><div class="rv-topright"><span><i class="rv-live-dot"></i>YOUR PERSONAL SPACE</span><span id="rv-time">--:--</span></div></header>' +
      '<div class="rv-layout"><aside class="rv-side"><div class="rv-side-label">WORKSPACE</div><nav class="rv-nav"><button type="button" class="is-active" data-filter="ALL"><span class="rv-nav-ico">⌂</span>Overview</button><button type="button" data-filter="COLLECTION"><span class="rv-nav-ico">◈</span>Collections</button><button type="button" data-filter="STORIES"><span class="rv-nav-ico">▤</span>Stories</button><button type="button" data-filter="GALLERY"><span class="rv-nav-ico">▧</span>Gallery</button><button type="button" data-filter="FEATURED"><span class="rv-nav-ico">✧</span>Featured</button></nav><div class="rv-side-label" style="margin-top:27px">SIGNATURE PALETTE</div><div class="rv-nav"><button type="button" data-palette="GOLAPI"><span class="rv-nav-ico" style="color:#ff2e63">●</span>Golapi</button><button type="button" data-palette="KATHALI"><span class="rv-nav-ico" style="color:#FFC300">●</span>Kathali</button><button type="button" data-palette="PIAJI"><span class="rv-nav-ico" style="color:#AF7AC5">●</span>Piaji</button></div><div class="rv-side-note"><strong>✦ THE ROksana SIGNATURE</strong>Three colors. One identity. A personal world designed to feel timeless.</div></aside>' +
      '<main class="rv-main"><section class="rv-welcome"><div><div class="rv-kicker">THE NEXT CHAPTER · YOUR COLLECTION</div><h1 class="rv-h1">Welcome to the<br><span class="rv-gradient">Future Vault.</span></h1><p class="rv-intro">A refined digital home for stories, memories and signature collections. Explore the rooms and discover the world of Roksana Nila.</p><div class="rv-palette"><span class="rv-swatch"><i style="background:#ff2e63;color:#ff2e63"></i>GOLAPI</span><span class="rv-swatch"><i style="background:#FFC300;color:#FFC300"></i>KATHALI</span><span class="rv-swatch"><i style="background:#AF7AC5;color:#AF7AC5"></i>PIAJI</span></div></div><div class="rv-crown" aria-hidden="true">♛</div></section>' +
      '<div class="rv-toolbar"><div><h2>Explore your space</h2><p>12 thoughtfully designed rooms · Choose one to open</p></div><label class="rv-search"><span>⌕</span><input id="rv-search" type="search" placeholder="Search your vault…" aria-label="Search vault rooms"></label></div>' +
      '<div class="rv-filters"><button type="button" class="rv-filter is-active" data-filter="ALL">All rooms</button><button type="button" class="rv-filter" data-filter="COLLECTION">Collections</button><button type="button" class="rv-filter" data-filter="STORIES">Stories</button><button type="button" class="rv-filter" data-filter="GALLERY">Gallery</button><button type="button" class="rv-filter" data-filter="FEATURED">Featured</button></div>' +
      '<div class="rv-grid" id="rv-grid">' + cards + '</div><div class="rv-empty" id="rv-empty">No rooms match your search. Try another word.</div>' +
      '<section class="rv-detail" id="rv-detail" aria-live="polite"><div class="rv-detailhead"><h3 id="rv-detail-title"></h3><button class="rv-close" id="rv-close" type="button">CLOSE ×</button></div><p id="rv-detail-text"></p></section>' +
      '<footer class="rv-bottom"><span>CRAFTED FOR <b>ROKSANA NILA</b></span><span>GOLAPI · KATHALI · PIAJI</span><span>YOUR SPACE, YOUR STORY.</span></footer></main></div></div></section>';
  }

  function mount() {
    if (!document.body || document.getElementById('rv-future-vault-mounted')) return;
    if (!document.getElementById('rv-future-vault-style')) {
      var style = document.createElement('style');
      style.id = 'rv-future-vault-style';
      style.textContent = css;
      document.head.appendChild(style);
    }
    var existing = document.getElementById('RoksanaFinalVault');
    var html = render();
    if (existing) existing.outerHTML = html;
    else {
      var menu = document.getElementById('trtt-final-menu');
      if (menu && menu.parentNode) menu.insertAdjacentHTML('afterend', html);
      else document.body.insertAdjacentHTML('afterbegin', html);
    }
    var root = document.getElementById('RoksanaFinalVault');
    if (!root) return;
    root.id = 'rv-future-vault-mounted';
    var search = root.querySelector('#rv-search');
    var empty = root.querySelector('#rv-empty');
    var detail = root.querySelector('#rv-detail');
    var activeFilter = 'ALL';

    function filterRooms() {
      var q = search.value.toLowerCase().trim();
      var count = 0;
      root.querySelectorAll('.rv-card').forEach(function (card) {
        var r = rooms[Number(card.getAttribute('data-room'))];
        var categoryMatch = activeFilter === 'ALL' || r.category === activeFilter ||
          (activeFilter === 'COLLECTION' && r.category === 'COLLECTION');
        var searchMatch = !q || (r.name + ' ' + r.category + ' ' + r.desc).toLowerCase().indexOf(q) !== -1;
        card.hidden = !(categoryMatch && searchMatch);
        if (!card.hidden) count++;
      });
      empty.style.display = count ? 'none' : 'block';
    }

    function setFilter(value) {
      activeFilter = value;
      root.querySelectorAll('[data-filter]').forEach(function (b) {
        b.classList.toggle('is-active', b.getAttribute('data-filter') === value);
      });
      filterRooms();
    }

    root.addEventListener('click', function (event) {
      var card = event.target.closest('[data-room]');
      if (card && root.contains(card)) {
        var room = rooms[Number(card.getAttribute('data-room'))];
        if (!room) return;
        root.querySelector('#rv-detail-title').textContent = room.name;
        root.querySelector('#rv-detail-title').style.color = room.color;
        root.querySelector('#rv-detail-text').textContent = room.desc;
        detail.classList.add('is-open');
        detail.scrollIntoView({behavior:'smooth',block:'nearest'});
        return;
      }
      var filter = event.target.closest('[data-filter]');
      if (filter && root.contains(filter)) { setFilter(filter.getAttribute('data-filter')); return; }
      var paletteButton = event.target.closest('[data-palette]');
      if (paletteButton && root.contains(paletteButton)) {
        var key = paletteButton.getAttribute('data-palette');
        search.value = key.toLowerCase();
        setFilter('ALL');
        filterRooms();
        return;
      }
      if (event.target.closest('#rv-close')) detail.classList.remove('is-open');
    });
    search.addEventListener('input', filterRooms);
    function updateClock() {
      var node = root.querySelector('#rv-time');
      if (node) node.textContent = new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
    }
    updateClock();
    window.setInterval(updateClock, 30000);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once:true});
  else mount();
})();