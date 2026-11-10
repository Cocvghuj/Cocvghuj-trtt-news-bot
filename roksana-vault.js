// TRTT News Bot - 787950 Vault FINAL - Marker 787950 LOCKED
// Browser-safe classic script shared by the website and Blogger publication.
(function (global) {
  'use strict';
  var MARKER_BYTES = Object.freeze([0x37, 0x38, 0x37, 0x39, 0x35, 0x30]);
  var MARKER_NUMBER = MARKER_BYTES.map(function (byte) {
    return String.fromCharCode(byte);
  }).join('');
  var MARKER = MARKER_NUMBER + ' LOCKED';

  var MENU_TOOLS = Object.freeze([
    Object.freeze({id:"main-hub",label:"Main Hub",url:"https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950"}),
    Object.freeze({id:"flightscoutpro",label:"FlightScoutPro",url:"https://www.aviasales.com/?marker=787950"}),
    Object.freeze({id:"ghost-esim",label:"Ghost-SIM",url:"https://www.airalo.com/?marker=787950"}),
    Object.freeze({id:"ride-stay",label:"Ride & Stay",url:"https://gettransfer.com/?marker=787950"}),
    Object.freeze({id:"experience-vault",label:"Experience Vault",url:"https://www.klook.com/?marker=787950"}),
    Object.freeze({id:"amazon-gear",label:"Amazon Gear",url:"https://amzn.to/4shg6Hn?marker=787950"})
  ]);
  var MARKER_LOCK = Object.freeze({value:"787950",hex:"373837393530"});
  function mountBottomMenu(){
    if(!global.document||document.getElementById("trtt-787950-bottom-menu"))return;
    var css=document.createElement("style");
    css.textContent="#trtt-787950-bottom-menu{position:fixed;left:50%;bottom:90px;transform:translateX(-50%);z-index:2147483646;display:flex;gap:5px;padding:8px;border:1px solid #ff6b8b88;border-radius:16px;background:#17131de8;backdrop-filter:blur(16px);box-shadow:0 0 20px #ff6b8b44;color:white;font:11px system-ui;max-width:calc(100vw - 20px)}#trtt-787950-bottom-menu a{position:relative;min-width:66px;padding:7px 5px;color:white;text-decoration:none;text-align:center;border-radius:9px}#trtt-787950-bottom-menu a:hover{background:#ff6b8b33;box-shadow:0 0 14px #ff6b8b}#trtt-787950-bottom-menu a:after{content:attr(data-tip);position:absolute;bottom:110%;left:50%;transform:translateX(-50%);padding:5px 7px;border-radius:5px;background:#111;white-space:nowrap;opacity:0;pointer-events:none}#trtt-787950-bottom-menu a:hover:after{opacity:1}#trtt-787950-bottom-menu .pulse{animation:trttPulse 2s infinite}@keyframes trttPulse{50%{box-shadow:0 0 15px #ff6b8b}}#trtt-787950-menu-toggle{position:fixed;right:12px;bottom:90px;z-index:2147483647;background:#17131d;color:white;border:1px solid #a55eea;border-radius:20px;padding:6px 9px;font-size:10px}@media(max-width:700px){#trtt-787950-bottom-menu{left:10px;right:10px;bottom:20px;transform:none;justify-content:space-around;gap:1px;padding:6px 3px}#trtt-787950-bottom-menu a{min-width:0;flex:1;font-size:9px;padding:6px 1px}#trtt-787950-menu-toggle{bottom:88px}}#trtt-787950-bottom-menu.eco{box-shadow:none;animation:none}";
    document.head.appendChild(css);
    var nav=document.createElement("nav");nav.id="trtt-787950-bottom-menu";nav.setAttribute("aria-label","787950 travel tools");
    MENU_TOOLS.forEach(function(t){var a=document.createElement("a");a.href=t.url;a.target="_blank";a.rel="sponsored nofollow noopener noreferrer";a.id=t.id==="ghost-esim"?"ghost-esim":"trtt-"+t.id;a.textContent=t.label;a.setAttribute("data-tip",t.label+" · 787950 LOCKED");if(t.id==="main-hub"){a.className="pulse";var badge=document.createElement("span");badge.textContent="787950 LOCKED";badge.style.cssText="display:block;margin-top:2px;color:#ff6b8b;font-size:8px;font-weight:800";a.appendChild(badge);}nav.appendChild(a);});
    var toggle=document.createElement("button");toggle.id="trtt-787950-menu-toggle";toggle.type="button";toggle.textContent="⇄ Menu side";var side="right";try{side=localStorage.getItem("trtt-menu-side")||"right";}catch(e){}
    function place(){nav.style.left=side==="left"?"10px":"auto";nav.style.right=side==="right"?"10px":"auto";nav.style.transform="none";}
    toggle.addEventListener("click",function(){side=side==="right"?"left":"right";try{localStorage.setItem("trtt-menu-side",side);}catch(e){}place();});
    document.body.appendChild(nav);document.body.appendChild(toggle);place();
    if(navigator.getBattery)navigator.getBattery().then(function(battery){function eco(){if(battery&&battery.level<=0.20&&!battery.charging){nav.classList.add("eco");}else{nav.classList.remove("eco");}}eco();battery.addEventListener("levelchange",eco);battery.addEventListener("chargingchange",eco);}).catch(function(){});
  }

  var TRTT_787950_VAULT_FINAL = Object.freeze({
    marker: MARKER,
    menuTools: MENU_TOOLS,
    markerHex: "373837393530",
    protocol: "Revenue Protection Protocol",
    version: "FINAL",
    blog1: "trttnews24bd.blogspot.com",
    blog2: "flightscoutpro.blogspot.com",
    showroom: "cocvghuj-trtt-news-bot.vercel.app",
    allowedDomains: Object.freeze(["trttnews24bd.blogspot.com", "trttnews24bd.com", "www.trttnews24bd.com", "cocvghuj-trtt-news-bot.vercel.app"]),
    affiliate: Object.freeze({
      marker: Number(MARKER_NUMBER),
      aviasales: "https://aviasales.tpo.lv/Fb8U9yav?marker=787950",
      klook: "https://klook.tpo.lv/TWKnemhz?marker=787950",
      airalo: "https://airalo.tpo.lv/ZZoQC7Mz?marker=787950",
      gettransfer: "https://gettransfer.tpo.lv/1u8zRU5s?marker=787950",
      amazon: "https://amzn.to/4shg6Hn?marker=787950"
    }),
    signature: Object.freeze({ name:'Signature',g:'#ff2e63',k:'#FFC300',p:'#AF7AC5' }),
    status: "ACTIVE",
    validated: true,
    answerApi: "https://cocvghuj-trtt-news-bot.vercel.app/api/answer"
  });
  global.TRTT_787950_VAULT_FINAL = TRTT_787950_VAULT_FINAL;
  global.TRTT_787950_VAULT = TRTT_787950_VAULT_FINAL;

  function mountVault() {
    if (!global.document || document.getElementById('trtt-787950-vault-ui')) return;
    var host = (global.location && global.location.hostname || '').toLowerCase();
    if (TRTT_787950_VAULT_FINAL.allowedDomains.indexOf(host) === -1) return;
    mountBottomMenu();
    var style = document.createElement('style');
    style.textContent = '#trtt-787950-vault-ui{font:15px/1.5 system-ui,sans-serif;max-width:760px;margin:24px auto;padding:20px;border:1px solid #d9deea;border-radius:16px;background:#fff;color:#172033;box-sizing:border-box}#trtt-787950-vault-ui *{box-sizing:border-box}#trtt-787950-vault-ui h2{margin:0 0 8px;font-size:22px}#trtt-787950-vault-ui .rv-signature{display:flex;gap:8px;margin:12px 0}#trtt-787950-vault-ui .rv-signature span{height:5px;flex:1;border-radius:8px}#trtt-787950-vault-ui textarea{width:100%;min-height:100px;padding:12px;border:1px solid #cbd2e1;border-radius:10px;font:inherit}#trtt-787950-vault-ui button{margin-top:10px;padding:11px 18px;border:0;border-radius:9px;background:#172b4d;color:white;font-weight:700;cursor:pointer}#trtt-787950-vault-ui button:disabled{opacity:.6;cursor:wait}#trtt-787950-vault-ui .rv-answer{margin-top:14px;padding:12px;background:#f4f6fa;border-radius:10px;white-space:pre-wrap;min-height:44px}';
    document.head.appendChild(style);
    var section = document.createElement('section');
    section.id = 'trtt-787950-vault-ui';
    section.innerHTML = '<h2>787950 LOCKED · TRTT Answer Desk</h2><div class="rv-signature" aria-hidden="true"><span style="background:#ff2e63"></span><span style="background:#FFC300"></span><span style="background:#AF7AC5"></span></div><label for="rv-ai-question"><strong>Ask your travel question</strong></label><textarea id="rv-ai-question" placeholder="Type your question here…" maxlength="4000"></textarea><button id="rv-ai-ask" type="button">Ask AI</button><div class="rv-answer" id="rv-ai-answer" aria-live="polite">Your answer will appear here.</div><div class="rv-status">Marker 787950 LOCKED · Dual-AI Answer Engine</div>';
    (document.querySelector('main') || document.body).appendChild(section);
    var ask = section.querySelector('#rv-ai-ask');
    var question = section.querySelector('#rv-ai-question');
    var answer = section.querySelector('#rv-ai-answer');
    ask.addEventListener('click', async function () {
      var prompt = question.value.trim();
      if (!prompt) { answer.textContent = 'Please enter a question first.'; return; }
      ask.disabled = true;
      answer.textContent = 'Checking your question…';
      try {
        var response = await fetch(TRTT_787950_VAULT_FINAL.answerApi, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: prompt })
        });
        var data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Answer service unavailable.');
        answer.textContent = data.answer || data.output_text || data.text || JSON.stringify(data, null, 2);
      } catch (error) {
        answer.textContent = 'Unable to get an answer right now: ' + error.message;
      } finally { ask.disabled = false; }
    });
  }
  if (global.document) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mountVault, { once: true });
    else mountVault();
  }
  console.log("787950 Vault FINAL Loaded - Marker 787950 LOCKED");
})(typeof window !== 'undefined' ? window : globalThis);
