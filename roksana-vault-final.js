// TRTT News Bot - Roksana Vault FINAL - Marker 787950 LOCKED
// Browser-safe classic script shared by the website and Blogger publication.
(function (global) {
  'use strict';
  var ROKSANA_VAULT_FINAL = {
    marker: "787950 LOCKED",
    version: "FINAL",
    blog1: "trttnews24bd.blogspot.com",
    blog2: "flightscoutpro.blogspot.com",
    showroom: "cocvghuj-trtt-news-bot.vercel.app",
    allowedDomains: ["trttnews24bd.blogspot.com", "trttnews24bd.com", "www.trttnews24bd.com", "cocvghuj-trtt-news-bot.vercel.app"],
    affiliate: {
      marker: 787950,
      aviasales: "https://aviasales.tp.st/xxxxx?marker=787950",
      klook: "https://klook.tp.st/xxxxx?marker=787950",
      airalo: "https://airalo.tp.st/xxxxx?marker=787950",
      gettransfer: "https://gettransfer.tp.st/xxxxx?marker=787950",
      amazon: "https://amzn.to/4shg6Hn"
    },
    signature: { name:'Signature',g:'#ff2e63',k:'#FFC300',p:'#AF7AC5' },
    status: "ACTIVE",
    validated: true,
    answerApi: "https://cocvghuj-trtt-news-bot.vercel.app/api/answer"
  };
  global.ROKSANA_VAULT_FINAL = ROKSANA_VAULT_FINAL;
  global.ROKSANA_VAULT = ROKSANA_VAULT_FINAL;

  function mountVault() {
    if (!global.document || document.getElementById('roksana-vault-ui')) return;
    var host = (global.location && global.location.hostname || '').toLowerCase();
    if (ROKSANA_VAULT_FINAL.allowedDomains.indexOf(host) === -1) return;
    var style = document.createElement('style');
    style.textContent = '#roksana-vault-ui{font:15px/1.5 system-ui,sans-serif;max-width:760px;margin:24px auto;padding:20px;border:1px solid #d9deea;border-radius:16px;background:#fff;color:#172033;box-sizing:border-box}#roksana-vault-ui *{box-sizing:border-box}#roksana-vault-ui h2{margin:0 0 8px;font-size:22px}#roksana-vault-ui .rv-signature{display:flex;gap:8px;margin:12px 0}#roksana-vault-ui .rv-signature span{height:5px;flex:1;border-radius:8px}#roksana-vault-ui textarea{width:100%;min-height:100px;padding:12px;border:1px solid #cbd2e1;border-radius:10px;font:inherit}#roksana-vault-ui button{margin-top:10px;padding:11px 18px;border:0;border-radius:9px;background:#172b4d;color:white;font-weight:700;cursor:pointer}#roksana-vault-ui button:disabled{opacity:.6;cursor:wait}#roksana-vault-ui .rv-answer{margin-top:14px;padding:12px;background:#f4f6fa;border-radius:10px;white-space:pre-wrap;min-height:44px}';
    document.head.appendChild(style);
    var section = document.createElement('section');
    section.id = 'roksana-vault-ui';
    section.innerHTML = '<h2>Roksana Nila · TRTT Answer Desk</h2><div class="rv-signature" aria-hidden="true"><span style="background:#ff2e63"></span><span style="background:#FFC300"></span><span style="background:#AF7AC5"></span></div><label for="rv-ai-question"><strong>Ask your travel question</strong></label><textarea id="rv-ai-question" placeholder="Type your question here…" maxlength="4000"></textarea><button id="rv-ai-ask" type="button">Ask AI</button><div class="rv-answer" id="rv-ai-answer" aria-live="polite">Your answer will appear here.</div><div class="rv-status">Marker 787950 LOCKED · Dual-AI Answer Engine</div>';
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
        var response = await fetch(ROKSANA_VAULT_FINAL.answerApi, {
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
  console.log("Roksana Vault FINAL Loaded - Marker 787950 LOCKED");
})(typeof window !== 'undefined' ? window : globalThis);
