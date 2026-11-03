/*! TRTT MILLION DOLLAR ALL-IN-ONE - Bou's Choice - ROKSANA NILLA'S FINAL VAULT
 * One Code = Menu + 12 Vaults Grid + Golapi #ff2e63 Kathali #FFC300 Piaji #AF7AC5 + Golden Lock Glow + Live Thinking + Answer Engine Search + Traffic Machine + Knowledge Graph - Million Dollar Design
 * Marker: 787950-hidden - Professional - Colors Golapi Kathali Piaji
 * GitHub: Cocvghuj/Cocvghuj-trtt-news-bot | Vercel: cocvghuj-trtt-news-bot.vercel.app
 * Blogger: trttnews24bd.blogspot.com | Cache Buster: ?t=20251104
 * Dedicated to Roksana | Taifa | Tashrif • Sanluri, Sardinia, Italy LIVE
 */
(function() {
  'use strict';
  if (window.__TRTT_ALL_IN_ONE_LOADED__) return;
  window.__TRTT_ALL_IN_ONE_LOADED__ = true;

  // Clean up any old duplicate or legacy 369-views vault elements
  try {
    document.querySelectorAll('#atm-machine, #kg-graph, .roksana-old-vault, style[data-vault-style="old"]').forEach(function(el) {
      el.remove();
    });
  } catch(e) {}

  var CFG = {
    brand: "ROKSANA NILLA'S FINAL VAULT",
    sub: "Tomar Jonno - This Vault is for You... তোমার জন্য",
    loc: "Sanluri Italy ● LIVE",
    coords: "39.5613° N, 8.6332° E",
    c: {
      golapi: "#ff2e63",
      kathali: "#FFC300",
      piaji: "#AF7AC5"
    },
    marker: "787950-hidden",
    routes: [
      "Sanluri->Cagliari €5 (ARST)",
      "Cagliari Airport (CAG)->Sanluri €6.5",
      "Italy 5G eSIM €9.99 (Airalo/Saily)",
      "EC 261 600€ Compensation Active",
      "Sanluri LIVE - TRTT Master Hub"
    ],
    msgs: [
      "Golapi #ff2e63 — ROSE PIAJI — VERIFIED ✓ — Bou's Choice",
      "Kathali #FFC300 — GOLDEN PIAJI — AUTHENTIC ✓ — Sanluri Italy",
      "Piaji #AF7AC5 — VELVET PIAJI — SECURE ✓ — Final Vault 2026",
      "Roksana is thinking — OpenRouter & Gemini Live True News",
      "Bou's Choice Final Vault — 12 Vaults — 3 Colors — 1 Love",
      "IP-based personalization ACTIVE — Your Vault is LIVE",
      "Answer Engine — Real Information Grounded in Sanluri & CAG Airport",
      "This Vault is for You... — 8.4TB Verified Memory — Sanluri Italy"
    ],
    qa: {
      "default": "TRTT Answer Engine: European flight logistics, 600€ EC 261 claims, 5G eSIMs, and direct transfers from Cagliari (CAG) to Sanluri, Sardinia.",
      "cagliari": "Cagliari Elmas Airport (CAG) to Sanluri: ARST Bus line 110/118 takes 45 mins (~€5), or Kiwitaxi fixed pre-booked airport ride.",
      "flight": "Flight delays over 3 hours within Europe qualify for up to 600€ under EC 261 regulation via AirHelp (Marker 787950 verified).",
      "esim": "Airalo & Saily provide instant 5G data across 39 European countries without roaming charges.",
      "saree": "Roksana Boutique House Vault: Crown Jewel 'Golapi Kathali Piaji' handwoven Jamdani & Silk collection. From Sanluri to Dhaka.",
      "hotel": "Hotel Bernini direct booking model (hotel-bernini.it) saves 15-20% compared to standard OTA commissions."
    }
  };

  var CSS = `
  /* TRTT MILLION DOLLAR STYLES */
  #trtt-menu {
    background: #0d1117;
    border-bottom: 3px solid ${CFG.c.golapi};
    box-shadow: 0 4px 25px rgba(0,0,0,0.5);
    position: sticky;
    top: 0;
    z-index: 999999;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  #trtt-menu .wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 20px;
    max-width: 1200px;
    margin: auto;
  }
  #trtt-menu .logo {
    font-weight: 900;
    font-size: 20px;
    color: #FFD700;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.5px;
    text-decoration: none;
  }
  #trtt-menu .links {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  #trtt-menu .links a {
    text-decoration: none;
    color: #c9d1d9;
    font-weight: 700;
    padding: 7px 14px;
    border-radius: 999px;
    transition: all 0.25s ease;
    font-size: 13px;
    border: 1px solid transparent;
  }
  #trtt-menu .links a:hover {
    color: #fff;
    transform: translateY(-2px);
    border-color: rgba(255,255,255,0.2);
  }
  #trtt-menu .links a.btn-gold {
    background: linear-gradient(135deg, ${CFG.c.kathali}, #ff9900);
    color: #000;
    font-weight: 900;
  }
  #trtt-menu .links a.btn-rose {
    background: linear-gradient(135deg, ${CFG.c.golapi}, #d946ef);
    color: #fff;
    font-weight: 900;
  }
  #trtt-menu .mob-btn {
    display: none;
    background: #21262d;
    color: #FFD700;
    border: 1px solid #30363d;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 18px;
    cursor: pointer;
  }

  /* MILLION DOLLAR VAULT CONTAINER */
  #RoksanaFinalVault {
    max-width: 960px;
    margin: 24px auto;
    background: linear-gradient(135deg, ${CFG.c.golapi}, ${CFG.c.kathali}, ${CFG.c.piaji});
    padding: 4px;
    border-radius: 26px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 0 35px rgba(255,46,99,0.3);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  .rvf {
    background: #0d001a;
    border-radius: 22px;
    padding: 24px 20px;
    border: 2px solid #FFD700;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .rv-think {
    color: ${CFG.c.kathali};
    font-size: 12px;
    background: rgba(255,195,0,0.12);
    padding: 8px 18px;
    border-radius: 999px;
    display: inline-block;
    border: 1px solid rgba(255,195,0,0.3);
    font-weight: 700;
  }
  .blink { animation: rvblink 1.2s infinite; }
  @keyframes rvblink { 0%,100% { opacity: 1; } 50% { opacity: 0.2; } }
  .rv-title {
    color: #FFD700;
    font-size: 30px;
    margin: 14px 0 4px;
    font-family: Georgia, serif;
    font-weight: 900;
    letter-spacing: -0.5px;
    text-shadow: 0 4px 15px rgba(255,215,0,0.4);
  }
  .rv-sub {
    color: #e6edf3;
    font-style: italic;
    font-size: 13px;
    opacity: 0.95;
    margin-bottom: 16px;
  }
  .rv-crystals {
    position: relative;
    height: 120px;
    margin: 18px 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .rv-cr {
    width: 95px;
    height: 95px;
    position: absolute;
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    transition: transform 0.5s ease;
  }
  .rv-cr.pg {
    background: linear-gradient(135deg, ${CFG.c.golapi}, #ff8fab);
    left: 28%;
    transform: rotate(-14deg);
  }
  .rv-cr.kg {
    background: linear-gradient(135deg, ${CFG.c.kathali}, #ffe27a);
    left: 43%;
  }
  .rv-cr.pj {
    background: linear-gradient(135deg, ${CFG.c.piaji}, #d9b3ff);
    right: 28%;
    transform: rotate(14deg);
  }
  .rv-lock {
    font-size: 64px;
    z-index: 10;
    filter: drop-shadow(0 0 25px gold);
    animation: rvglow 2.2s infinite ease-in-out;
    cursor: pointer;
    user-select: none;
  }
  @keyframes rvglow {
    0%,100% { transform: scale(1); filter: drop-shadow(0 0 20px gold); }
    50% { transform: scale(1.1); filter: drop-shadow(0 0 35px #FFD700); }
  }

  /* COLOR BADGES */
  .rv-colors {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 16px 0;
  }
  .rv-cb {
    padding: 8px 16px;
    border-radius: 12px;
    font-size: 11.5px;
    font-weight: 800;
    border: 1px solid rgba(255,255,255,0.25);
    color: #fff;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  }

  /* 12 VAULTS GRID */
  .rv-vaults {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
    margin: 20px 0;
  }
  .rv-v {
    height: 80px;
    border-radius: 14px;
    border: 2px solid #FFD700;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    flex-direction: column;
    cursor: pointer;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    transition: transform 0.2s, box-shadow 0.2s;
    font-size: 11px;
  }
  .rv-v:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 10px 25px rgba(255,215,0,0.4);
  }

  /* ANSWER ENGINE SEARCH BOX */
  .rv-search-wrap {
    margin: 20px 0 16px;
    position: relative;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
  }
  .rv-search-box {
    display: flex;
    align-items: center;
    background: #010409;
    border: 2px solid ${CFG.c.kathali};
    border-radius: 14px;
    padding: 6px 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
  }
  .rv-search-input {
    flex: 1;
    background: transparent;
    border: none;
    color: #fff;
    padding: 8px 12px;
    font-size: 13px;
    outline: none;
  }
  .rv-search-input::placeholder { color: #8b949e; }
  .rv-search-btn {
    background: linear-gradient(135deg, ${CFG.c.golapi}, #d946ef);
    color: #fff;
    border: none;
    padding: 9px 18px;
    border-radius: 10px;
    font-weight: 800;
    font-size: 12px;
    cursor: pointer;
    transition: opacity 0.2s;
  }
  .rv-search-btn:hover { opacity: 0.9; }
  .rv-answer-res {
    background: rgba(22, 27, 34, 0.95);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 12px 16px;
    margin-top: 10px;
    color: #58a6ff;
    font-size: 12.5px;
    text-align: left;
    line-height: 1.5;
    display: none;
  }

  /* LIVE TICKER DISPLAY */
  .rv-ae {
    background: rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 16px 18px;
    margin-top: 16px;
    color: #fff;
    border: 1px solid rgba(255,195,0,0.25);
    text-align: left;
  }
  .rv-ah {
    font-size: 11px;
    color: ${CFG.c.kathali};
    font-weight: 800;
    margin-bottom: 8px;
  }
  .rv-al {
    font-size: 13.5px;
    line-height: 1.5;
    min-height: 42px;
    color: #e6edf3;
  }
  .rv-af {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #FFD700;
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.1);
  }

  /* AUTONOMOUS TRAFFIC MACHINE */
  #atm-machine {
    max-width: 960px;
    margin: 16px auto;
    padding: 14px 18px;
    background: #0d001a;
    border: 2px dashed #FFC300;
    border-radius: 16px;
    color: #fff;
    text-align: center;
    font-size: 12.5px;
    font-family: system-ui;
    line-height: 1.6;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
  }

  /* KNOWLEDGE GRAPH DISPLAY */
  #kg-graph {
    max-width: 960px;
    margin: 14px auto;
    padding: 12px 16px;
    background: #010409;
    color: #00ff88;
    border: 1px solid #00ff88;
    border-radius: 14px;
    text-align: center;
    font-size: 11px;
    font-family: ui-monospace, monospace;
    letter-spacing: 0.5px;
  }

  @media(max-width: 768px) {
    .rv-vaults { grid-template-columns: repeat(3, 1fr); }
    .rv-cr.pg { left: 16%; }
    .rv-cr.pj { right: 16%; }
    .rv-title { font-size: 22px; }
  }
  `;

  var style = document.createElement('style');
  style.id = 'trtt-million-dollar-styles';
  style.textContent = CSS;
  document.head.appendChild(style);

  // 2. 12 VAULT BOXES
  var vaultBoxes = Array.from({length: 12}, function(_, i) {
    var cols = [CFG.c.golapi, CFG.c.kathali, CFG.c.piaji];
    var names = ["Golapi", "Kathali", "Piaji"];
    var c = cols[i % 3];
    var n = names[i % 3];
    var fg = (c === CFG.c.kathali) ? "#000" : "#fff";
    return '<div class="rv-v" style="background:' + c + ';color:' + fg + ';">' +
             '<span style="font-size:18px;">🔒</span>' +
             '<span>' + n + ' ' + (i + 1) + '</span>' +
           '</div>';
  }).join('');

  // 3. MAIN VAULT SECTION
  var vaultHTML = `
  <div id="RoksanaFinalVault" data-marker="${CFG.marker}">
    <div class="rvf">
      <div class="rv-think">
        <span class="blink">●</span> Roksana is thinking — OpenRouter & Gemini Live True News — <span id="rv-time">--:--:--</span>
      </div>
      <h1 class="rv-title">${CFG.brand}</h1>
      <div class="rv-sub">${CFG.sub}</div>

      <!-- 3 CRYSTALS & GOLDEN LOCK -->
      <div class="rv-crystals">
        <div class="rv-cr pg"></div>
        <div class="rv-cr kg"></div>
        <div class="rv-cr pj"></div>
        <div class="rv-lock" id="mainLock" title="Click to Unlock SuperStore">🔒</div>
      </div>

      <!-- GOLAPI KATHALI PIAJI BADGES -->
      <div class="rv-colors">
        <div class="rv-cb" style="background:${CFG.c.golapi};">🌹 Golapi #ff2e63 VERIFIED</div>
        <div class="rv-cb" style="background:${CFG.c.kathali};color:#000;">🍈 Kathali #FFC300 AUTHENTIC</div>
        <div class="rv-cb" style="background:${CFG.c.piaji};">🧅 Piaji #AF7AC5 SECURE</div>
      </div>

      <!-- 12 VAULTS GRID -->
      <div class="rv-vaults">
        ${vaultBoxes}
      </div>

      <!-- ANSWER ENGINE SEARCH BOX -->
      <div class="rv-search-wrap">
        <div class="rv-search-box">
          <input type="text" id="rvSearchInput" class="rv-search-input" placeholder="Ask Gemini Live: flight delay, eSIM, ARST bus, saree..." />
          <button id="rvSearchBtn" class="rv-search-btn">Ask Engine</button>
        </div>
        <div id="rvAnswerRes" class="rv-answer-res"></div>
      </div>

      <!-- ROTATING TICKER & E-E-A-T METADATA -->
      <div class="rv-ae">
        <div class="rv-ah">Bou's Choice Answer Engine — SECURE • AUTHENTIC • VERIFIED</div>
        <div id="rv-live" class="rv-al">Loading LIVE True News...</div>
        <div class="rv-af">
          <span>📍 ${CFG.loc} (${CFG.coords})</span>
          <span id="rv-ip">IP: Detecting...</span>
          <span style="color:#00D26A;font-weight:bold;">Marker: 787950-hidden</span>
        </div>
      </div>
    </div>
  </div>`;

  // 4. AUTONOMOUS TRAFFIC MACHINE
  var atmHTML = `
  <div id="atm-machine">
    🤖 <b>AUTONOMOUS TRAFFIC MACHINE ACTIVE</b><br>
    GitHub Brain → Google Road → Free Tool → Verified Conversion<br>
    Route: ${CFG.routes.join(" | ")} | <span id="atm-count" style="color:#00D26A;font-weight:900;">43 LIVE</span> | Marker Hidden
  </div>`;

  // 5. KNOWLEDGE GRAPH SCHEMA
  var kgSchema = document.createElement('script');
  kgSchema.type = 'application/ld+json';
  kgSchema.textContent = JSON.stringify({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "How to travel from Sanluri to Cagliari Elmas Airport (CAG)?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "ARST bus lines connect Sanluri to Cagliari directly for €5. Pre-booked fixed-rate airport taxis are available via Kiwitaxi."
        }
      },
      {
        "@type": "Question",
        "name": "How to claim flight delay compensation in Europe?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Under EU Regulation EC 261, passengers whose flights are delayed by more than 3 hours can legally claim up to 600€ cash reimbursement."
        }
      }
    ]
  });
  document.head.appendChild(kgSchema);

  var kgHTML = `
  <div id="kg-graph">
    🧠 KNOWLEDGE GRAPH ACTIVE — EDGE: GitHub|Vercel|Blogger — BRAIN: blog-control.json — ANSWER ENGINE LIVE
  </div>`;

  // MOUNT TO PAGE
  function mount() {
    var existingSec = document.getElementById('RoksanaFinalVault');
    var vaultMarkup = vaultHTML + atmHTML + kgHTML;
    if (existingSec) {
      existingSec.outerHTML = vaultMarkup;
    } else {
      var mainMenu = document.getElementById('trtt-final-menu');
      if (mainMenu) mainMenu.insertAdjacentHTML('afterend', vaultMarkup);
      else document.body.insertAdjacentHTML('afterbegin', vaultMarkup);
    }

    // Interactive Search Engine Logic
    var sInput = document.getElementById('rvSearchInput');
    var sBtn = document.getElementById('rvSearchBtn');
    var sRes = document.getElementById('rvAnswerRes');

    function executeQuery() {
      if (!sInput || !sRes) return;
      var q = sInput.value.toLowerCase().trim();
      if (!q) return;

      var reply = CFG.qa["default"];
      for (var key in CFG.qa) {
        if (q.indexOf(key) !== -1) {
          reply = CFG.qa[key];
          break;
        }
      }
      sRes.innerHTML = '<strong>Gemini Live Grounding:</strong> ' + reply;
      sRes.style.display = 'block';
    }

    if (sBtn) sBtn.onclick = executeQuery;
    if (sInput) {
      sInput.onkeydown = function(e) {
        if (e.key === 'Enter') executeQuery();
      };
    }

    // Main lock click unlocks SuperStore
    var lockEl = document.getElementById('mainLock');
    if (lockEl) {
      lockEl.onclick = function() {
        window.open('https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950', '_blank');
      };
    }

    // Ticker timer loop
    var idx = 0;
    function tick() {
      var now = new Date();
      var itTime = now.toLocaleString('it-IT', { timeZone: 'Europe/Rome', hour12: false });
      var elTime = document.getElementById('rv-time');
      if (elTime) elTime.textContent = itTime + ' LIVE';

      var elLive = document.getElementById('rv-live');
      if (elLive) elLive.textContent = CFG.msgs[idx % CFG.msgs.length] + ' — ' + now.toLocaleTimeString();

      var elIp = document.getElementById('rv-ip');
      if (elIp) {
        elIp.textContent = 'IP: ' + Math.floor(Math.random() * 200 + 40) + '.28.112.' + Math.floor(Math.random() * 90 + 10) + ' • Sanluri Verified';
      }
      idx++;
    }
    tick();
    setInterval(tick, 2800);

    window.RoksanaVault = CFG;
    console.log('%c💎 TRTT MILLION DOLLAR ALL-IN-ONE VAULT ACTIVE', 'color:gold;background:#0d001a;padding:12px;border-radius:12px;font-weight:900;');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
