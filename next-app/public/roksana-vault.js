/* Roksana Nila Vault — compact, private-feeling personal collection UI.
   The signature palette is expressed visually; color values are never printed in the interface. */
(function(){
"use strict";
var allowed={"trttnews24bd.blogspot.com":1,"trttnews24bd.com":1,"www.trttnews24bd.com":1};
if(!allowed[String(location.hostname||"").toLowerCase()])return;
if(window.__ROKSANA_COMPACT_VAULT__)return;
window.__ROKSANA_COMPACT_VAULT__=true;
var rooms=[
{icon:"✦",name:"Welcome Studio",type:"START HERE",color:"var(--rv-gold)",desc:"A calm entry point to the Roksana Nila collection."},
{icon:"🌹",name:"Golapi Archive",type:"COLLECTION",color:"var(--rv-rose)",desc:"A bold, warm collection of signature moments."},
{icon:"👑",name:"Kathali Treasury",type:"COLLECTION",color:"var(--rv-gold)",desc:"Radiant keepsakes and timeless favorites."},
{icon:"💜",name:"Piaji Gallery",type:"COLLECTION",color:"var(--rv-lilac)",desc:"An elegant gallery for creative memories."},
{icon:"💎",name:"The Crown Room",type:"FEATURED",color:"var(--rv-gold)",desc:"A curated home for featured pieces."},
{icon:"📖",name:"Roksana Journal",type:"STORIES",color:"var(--rv-lilac)",desc:"Notes, memories and stories."},
{icon:"▧",name:"Memory Gallery",type:"GALLERY",color:"var(--rv-rose)",desc:"A visual home for photographs and keepsakes."},
{icon:"✧",name:"Signature Edit",type:"FEATURED",color:"var(--rv-gold)",desc:"A considered mix of the three signature colors."},
{icon:"⌘",name:"Secret Garden",type:"COMING SOON",color:"var(--rv-lilac)",desc:"Reserved for future private content. This is not password protection."},
{icon:"✉",name:"Notes & Letters",type:"MESSAGES",color:"var(--rv-rose)",desc:"A space for thoughtful messages."},
{icon:"◈",name:"Help & Guide",type:"SUPPORT",color:"var(--rv-gold)",desc:"A short guide to the rooms in this Vault."},
{icon:"♡",name:"About Roksana",type:"THE STORY",color:"var(--rv-lilac)",desc:"The story behind this personal collection."}
];
var style=document.createElement("style");
style.id="rv-compact-style";
style.textContent=`
:root{--rv-rose:#ff4778;--rv-gold:#f5c95b;--rv-lilac:#b58bd0}
#rv-launcher{position:fixed;right:18px;bottom:18px;z-index:99990;border:1px solid #ffffff40;border-radius:999px;padding:11px 16px;background:linear-gradient(115deg,#24152e,#493057);color:#fff;box-shadow:0 10px 32px #100b1d55;font:800 12px Inter,system-ui,sans-serif;cursor:pointer}
#rv-launcher span{color:var(--rv-gold);margin-right:7px}
#rv-overlay{position:fixed;inset:0;z-index:99999;display:none;align-items:center;justify-content:center;padding:16px;background:#090711c9;backdrop-filter:blur(8px)}
#rv-overlay.open{display:flex}
#rv-dialog{width:min(920px,100%);max-height:min(88vh,820px);overflow:auto;border:1px solid #b58bd055;border-radius:22px;background:radial-gradient(ellipse at 0 0,#ff47781e,transparent 34%),radial-gradient(ellipse at 100% 0,#b58bd022,transparent 35%),#120e1a;color:#f7f2fa;box-shadow:0 30px 100px #000a;font-family:Inter,system-ui,sans-serif}
#rv-dialog *{box-sizing:border-box}
#rv-dialog .rv-head{position:sticky;top:0;z-index:2;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 20px;background:#120e1af2;border-bottom:1px solid #ffffff17}
#rv-dialog .rv-brand{font-size:11px;font-weight:950;letter-spacing:.14em}
#rv-dialog .rv-brand i{display:inline-grid;place-items:center;width:30px;height:30px;margin-right:9px;border-radius:10px;background:linear-gradient(135deg,var(--rv-rose),var(--rv-gold),var(--rv-lilac));color:#201429;font-style:normal}
#rv-dialog .rv-close{border:1px solid #ffffff30;border-radius:10px;padding:8px 11px;background:#ffffff0c;color:#fff;font-weight:800;cursor:pointer}
#rv-dialog .rv-content{padding:clamp(17px,3vw,28px)}
#rv-dialog .rv-kicker{font-size:9px;font-weight:900;letter-spacing:.2em;color:var(--rv-gold)}
#rv-dialog h2{margin:9px 0 10px;color:#fff;font:700 clamp(25px,4vw,38px)/1.1 Georgia,serif}
#rv-dialog .rv-lede{max-width:680px;color:#bdb2c7;font-size:12px;line-height:1.8;margin:0}
#rv-dialog .rv-swatches{display:flex;gap:7px;margin:14px 0 20px;flex-wrap:wrap}
#rv-dialog .rv-swatches span{padding:6px 10px;border:1px solid #ffffff20;border-radius:30px;color:#e7ddeb;font-size:9px;font-weight:800;letter-spacing:.1em}
#rv-dialog .rv-toolbar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:22px 0 12px}
#rv-dialog .rv-toolbar strong{font:700 17px Georgia,serif}
#rv-dialog .rv-search{width:min(250px,50%);padding:10px 12px;border:1px solid #ffffff25;border-radius:10px;background:#08070d;color:#fff;font:12px Inter,system-ui,sans-serif}
#rv-dialog .rv-filters{display:flex;gap:7px;overflow:auto;padding:2px 0 12px}
#rv-dialog .rv-filter{flex:none;padding:7px 11px;border:1px solid #ffffff22;border-radius:30px;background:transparent;color:#bdb2c7;font-size:9px;font-weight:800;cursor:pointer}
#rv-dialog .rv-filter.active{background:#b58bd026;border-color:#b58bd0;color:#fff}
#rv-dialog .rv-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
#rv-dialog .rv-room{min-height:112px;padding:13px;border:1px solid #ffffff20;border-radius:13px;background:#ffffff08;color:#fff;text-align:left;cursor:pointer;transition:transform .18s,border-color .18s,background .18s}
#rv-dialog .rv-room:hover{transform:translateY(-2px);border-color:#f5c95b88;background:#ffffff12}
#rv-dialog .rv-room[hidden]{display:none}
#rv-dialog .rv-icon{display:block;margin-bottom:10px;font-size:19px}
#rv-dialog .rv-room b{display:block;font-size:11px}
#rv-dialog .rv-room small{display:block;margin-top:5px;color:#978ba3;font-size:8px;font-weight:900;letter-spacing:.13em}
#rv-dialog .rv-detail{display:none;margin-top:12px;padding:15px;border:1px solid #f5c95b55;border-radius:13px;background:#f5c95b0c}
#rv-dialog .rv-detail.open{display:block}
#rv-dialog .rv-detail h3{margin:0 0 6px;color:var(--rv-gold);font:700 17px Georgia,serif}
#rv-dialog .rv-detail p{margin:0;color:#c9bfd1;font-size:11px;line-height:1.8}
#rv-dialog .rv-letter{margin:20px 0;padding:17px;border:1px solid #b58bd044;border-radius:14px;background:linear-gradient(110deg,#ff477810,#b58bd010,#f5c95b0a)}
#rv-dialog .rv-letter p{margin:7px 0;color:#d5ccdc;font-size:11px;line-height:1.8}
#rv-dialog .rv-ai{margin-top:20px;padding:17px;border:1px solid #b58bd055;border-radius:14px;background:#ffffff06}
#rv-dialog .rv-ai h3{margin:0 0 6px;color:var(--rv-gold);font:700 17px Georgia,serif}
#rv-dialog .rv-ai p{margin:0 0 12px;color:#a99eb3;font-size:10px;line-height:1.7}
#rv-dialog .rv-ai-form{display:flex;gap:8px}
#rv-dialog .rv-ai-input{flex:1;min-width:0;padding:11px 12px;border:1px solid #ffffff2c;border-radius:10px;background:#08070d;color:#fff;font:12px Inter,system-ui,sans-serif}
#rv-dialog .rv-ai-button{padding:0 15px;border:0;border-radius:10px;background:linear-gradient(120deg,var(--rv-rose),var(--rv-lilac));color:#fff;font-size:10px;font-weight:950;cursor:pointer}
#rv-dialog .rv-ai-button:disabled{opacity:.55;cursor:wait}
#rv-dialog .rv-ai-status{min-height:16px;margin:9px 0;color:var(--rv-gold);font-size:10px}
#rv-dialog .rv-ai-result{margin-top:9px;padding:12px;border:1px solid #ffffff20;border-radius:11px;background:#08070d}
#rv-dialog .rv-ai-result b{display:block;margin-bottom:7px;color:var(--rv-gold);font-size:11px}
#rv-dialog .rv-ai-result p{margin:0;color:#e4dce9;font-size:11px;white-space:pre-wrap;overflow-wrap:anywhere}
#rv-dialog .rv-ai-result a{color:#ff9bb6;font-size:10px;overflow-wrap:anywhere}
#rv-dialog .rv-footer{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:18px;padding-top:13px;border-top:1px solid #ffffff18;color:#8e8398;font-size:9px;letter-spacing:.08em}
@media(max-width:700px){#rv-dialog .rv-grid{grid-template-columns:repeat(2,minmax(0,1fr))}#rv-dialog .rv-content{padding:16px}}
@media(max-width:460px){#rv-launcher{right:12px;bottom:12px;padding:10px 13px}#rv-dialog .rv-head{padding:12px 14px}#rv-dialog .rv-toolbar{align-items:stretch;flex-direction:column}#rv-dialog .rv-search{width:100%}#rv-dialog .rv-ai-form{flex-direction:column}#rv-dialog .rv-ai-button{min-height:40px}}
@media(prefers-reduced-motion:reduce){#rv-dialog *{transition:none!important}}
`;
document.head.appendChild(style);
var launcher=document.createElement("button");launcher.id="rv-launcher";launcher.type="button";launcher.innerHTML="<span>✦</span> Roksana Vault";launcher.setAttribute("aria-haspopup","dialog");
var overlay=document.createElement("div");overlay.id="rv-overlay";overlay.innerHTML='<section id="rv-dialog" role="dialog" aria-modal="true" aria-labelledby="rv-title"><header class="rv-head"><div class="rv-brand"><i>R</i>ROKSANA NILA · PERSONAL VAULT</div><button class="rv-close" type="button" aria-label="Close vault">Close ×</button></header><div class="rv-content"><div class="rv-kicker">A SMALL DIGITAL HOME · MADE WITH LOVE</div><h2 id="rv-title">A world of memories,<br>wrapped in three colors.</h2><p class="rv-lede">A personal collection for stories, keepsakes and the little details that make a family feel close, wherever life takes us.</p><div class="rv-swatches"><span>● GOLAPI</span><span>● KATHALI</span><span>● PIAJI</span></div><div class="rv-toolbar"><strong>Explore the Vault</strong><input class="rv-search" type="search" placeholder="Search rooms…" aria-label="Search Vault rooms"></div><div class="rv-filters"><button class="rv-filter active" data-filter="ALL">All rooms</button><button class="rv-filter" data-filter="COLLECTION">Collections</button><button class="rv-filter" data-filter="STORIES">Stories</button><button class="rv-filter" data-filter="GALLERY">Gallery</button><button class="rv-filter" data-filter="FEATURED">Featured</button></div><div class="rv-grid"></div><div class="rv-detail" aria-live="polite"><h3></h3><p></p></div><section class="rv-letter"><div class="rv-kicker">A LETTER ACROSS DISTANCE</div><p>রোকসানা, দূরত্ব আমাদের আলাদা জায়গায় রাখলেও তুমি আমার হৃদয়ের খুব কাছে। এই ছোট্ট Vault তোমার জন্য—আমার ভালোবাসা, স্মৃতি আর পরিবারের প্রতি টান ভাগ করে নেওয়ার একটি ঠিকানা।</p><p>With love, from Italy.</p></section><section class="rv-ai"><h3>Evidence Answer Engine</h3><p>Ask a question. Gemini and OpenRouter can return independent answers with source links when their services are configured and available.</p><div class="rv-ai-form"><input class="rv-ai-input" type="text" maxlength="2000" placeholder="Ask in any language…" aria-label="Ask the Answer Engine"><button class="rv-ai-button" type="button">ASK AI</button></div><div class="rv-ai-status" role="status" aria-live="polite">Ready. Provider keys stay on the server.</div><div class="rv-ai-results"></div></section><footer class="rv-footer"><span>ROKSANA NILA</span><span>GOLAPI · KATHALI · PIAJI</span><span>YOUR SPACE, YOUR STORY.</span></footer></div></section>';
document.body.appendChild(launcher);document.body.appendChild(overlay);
var dialog=overlay.querySelector("#rv-dialog"),grid=dialog.querySelector(".rv-grid"),search=dialog.querySelector(".rv-search"),detail=dialog.querySelector(".rv-detail"),active="ALL";
rooms.forEach(function(room,index){var b=document.createElement("button");b.type="button";b.className="rv-room";b.dataset.index=String(index);b.dataset.type=room.type;b.innerHTML='<span class="rv-icon">'+room.icon+'</span><b></b><small></small>';b.querySelector("b").textContent=room.name;b.querySelector("small").textContent=room.type;grid.appendChild(b);});
function filter(){var q=search.value.trim().toLowerCase();grid.querySelectorAll(".rv-room").forEach(function(b){var r=rooms[Number(b.dataset.index)];b.hidden=!(active==="ALL"||(active==="COLLECTION"&&r.type==="COLLECTION")||r.type===active)&&!(q&&((r.name+" "+r.type+" "+r.desc).toLowerCase().includes(q)));if(q)b.hidden=!(r.name+" "+r.type+" "+r.desc).toLowerCase().includes(q);});}
dialog.addEventListener("click",function(e){var b=e.target.closest(".rv-room");if(b){var r=rooms[Number(b.dataset.index)];detail.querySelector("h3").textContent=r.name;detail.querySelector("h3").style.color=r.color;detail.querySelector("p").textContent=r.desc;detail.classList.add("open");return;}var f=e.target.closest("[data-filter]");if(f){active=f.dataset.filter;dialog.querySelectorAll(".rv-filter").forEach(function(x){x.classList.toggle("active",x===f);});filter();return;}if(e.target.closest(".rv-close"))close();});
search.addEventListener("input",filter);
function open(){overlay.classList.add("open");document.body.style.overflow="hidden";launcher.setAttribute("aria-expanded","true");dialog.querySelector(".rv-close").focus();}
function close(){overlay.classList.remove("open");document.body.style.overflow="";launcher.setAttribute("aria-expanded","false");launcher.focus();}
launcher.addEventListener("click",open);overlay.addEventListener("click",function(e){if(e.target===overlay)close();});document.addEventListener("keydown",function(e){if(e.key==="Escape"&&overlay.classList.contains("open"))close();});
var input=dialog.querySelector(".rv-ai-input"),button=dialog.querySelector(".rv-ai-button"),status=dialog.querySelector(".rv-ai-status"),results=dialog.querySelector(".rv-ai-results");
function addResult(name,result,error){var box=document.createElement("div");box.className="rv-ai-result";var title=document.createElement("b");title.textContent=name+(result&&result.model?" · "+result.model:"");box.appendChild(title);var p=document.createElement("p");p.textContent=result&&result.answer?result.answer:(error||"No answer returned.");box.appendChild(p);if(result&&Array.isArray(result.sources)){result.sources.forEach(function(s){try{var u=new URL(s.url);if(u.protocol!=="https:")return;var a=document.createElement("a");a.href=u.href;a.target="_blank";a.rel="noopener noreferrer";a.textContent=s.title||u.hostname;box.appendChild(a);}catch(_){}});}results.appendChild(box);}
async function ask(){var question=input.value.trim();if(!question){status.textContent="Please enter a question.";input.focus();return;}button.disabled=true;results.replaceChildren();status.textContent="Sending question to the available AI providers…";try{var response=await fetch("https://cocvghuj-trtt-news-bot.vercel.app/api/answer",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:question})});var data=await response.json().catch(function(){return {};});if(!response.ok||!data.ok){if(data.errors){addResult("Gemini",data.results&&data.results.gemini,data.errors.gemini);addResult("OpenRouter",data.results&&data.results.openrouter,data.errors.openrouter);status.textContent=data.error||"Provider error; details shown below.";return;}throw new Error(data.error||("HTTP "+response.status));}addResult("Gemini",data.results&&data.results.gemini,data.errors&&data.errors.gemini);addResult("OpenRouter",data.results&&data.results.openrouter,data.errors&&data.errors.openrouter);status.textContent="Completed. Check source links before relying on the answers.";}catch(e){status.textContent="Answer Engine unavailable: "+(e&&e.message?e.message:"request failed");}finally{button.disabled=false;}}
button.addEventListener("click",ask);input.addEventListener("keydown",function(e){if(e.key==="Enter"){e.preventDefault();ask();}});
})();
