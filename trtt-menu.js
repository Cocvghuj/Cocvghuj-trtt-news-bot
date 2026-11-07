
(function(){
"use strict";

/* Version-aware singleton: safely replaces the older 320px menu. */
const VERSION="TRTT-THINKING-ROOM-2026-11-07-03";
if(window.__TRTT_VOYAGE_MENU_VERSION__===VERSION)return;
try{
  var previousRoot=document.getElementById("trtt-voyage-menu");
  if(previousRoot)previousRoot.remove();
  document.getElementById("trtt-voyage-filter-title")?.remove();
  if(document.body)document.body.classList.remove("tv-filtering");
  [
    "#trtt-old-menu","#trtt-side-menu","#trtt-menu",
    "#trtt-voyage-sidebar","#trtt-voyage-side-menu",
    ".trtt-old-menu",".trtt-side-menu",".trtt-menu-panel",
    ".trtt-voyage-sidebar"
  ].forEach(function(selector){
    document.querySelectorAll(selector).forEach(function(node){node.remove();});
  });
}catch(_){}
if(document.getElementById("trtt-voyage-menu"))return;
window.__TRTT_VOYAGE_MENU__=true;
window.__TRTT_VOYAGE_MENU_VERSION__=VERSION;

const LOCK=Object.freeze({marker:"787950"});
const VOYAGE_PHOTOS=Object.freeze(["https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1518837695005-2083093ee35b?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1494783367193-149034c05e8f?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&w=1800&q=82","https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1800&q=82"]);

const CFG=Object.freeze({
home:"https://trttnews24bd.blogspot.com/",
ai:"https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950",
storage:"trtt-voyage:last-category",
photo:"https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1800&q=85",
cats:Object.freeze([
{name:"Flights & Partner Platform",icon:"✈",desc:"Discover flights, smart fares and travel partners."},
{name:"Passenger Support & Luggage",icon:"🧳",desc:"Practical help for smoother journeys."},
{name:"eSIM & Connectivity",icon:"📶",desc:"Stay connected wherever the journey takes you."},
{name:"Cars & Transfers",icon:"🚘",desc:"Move freely with rides and airport transfers."},
{name:"Tours & Experiences",icon:"🗺",desc:"Find memorable places and experiences."},
{name:"Travel Gear",icon:"🎒",desc:"Useful gear for every kind of traveller."}
])
});

function esc(s){
return String(s).replace(/[&<>"']/g,c=>({
"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
}[c]));
}

function marked(s){
try{
let u=new URL(s,CFG.home);
u.searchParams.set("marker",LOCK.marker);
return u.href;
}catch(_){
return CFG.home+"?marker="+LOCK.marker;
}
}

function mount(){
if(!document.body||document.getElementById("trtt-voyage-menu"))return;

const css=[
"#trtt-voyage-menu,#trtt-voyage-menu *{box-sizing:border-box}#trtt-voyage-menu{font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;color:#202437}",

"#trtt-voyage-menu .tv-trigger{position:fixed;z-index:2147483000;left:16px;top:16px;width:49px;height:49px;border:1px solid #f1e8ec;border-radius:16px;background:#ffffffed;box-shadow:0 7px 25px #27304720;display:grid;place-items:center;cursor:pointer;backdrop-filter:blur(14px)}#trtt-voyage-menu .tv-trigger svg{width:22px;height:22px;stroke:#25283a;stroke-width:2;fill:none;stroke-linecap:round}",

"#trtt-voyage-menu .tv-screen{position:fixed;inset:0;z-index:2147483001;width:100%;max-width:100vw;height:100vh;height:100dvh;overflow-x:hidden;overflow-y:auto;overscroll-behavior:contain;background:#fff;opacity:0;visibility:hidden;transform:scale(.985);transition:opacity .2s,transform .25s,visibility .2s}#trtt-voyage-menu.tv-open .tv-screen{opacity:1;visibility:visible;transform:scale(1)}",

"#trtt-voyage-menu .tv-bar{position:sticky;top:0;z-index:5;min-height:78px;padding:12px clamp(14px,4vw,54px);display:flex;align-items:center;gap:16px;background:#ffffffed;border-bottom:1px solid #f2edf0;backdrop-filter:blur(18px)}#trtt-voyage-menu .tv-brand{display:flex;align-items:center;gap:9px;min-width:max-content;color:#202437;text-decoration:none;font-size:18px;font-weight:900;letter-spacing:-.6px}#trtt-voyage-menu .tv-logo{width:40px;height:40px;border-radius:14px;background:linear-gradient(145deg,#ff6487,#ffa0b1);display:grid;place-items:center;color:#fff;font-size:23px;font-weight:900}#trtt-voyage-menu .tv-lock{padding:6px 8px;border-radius:8px;background:#fff0f3;color:#d94c70;font-size:10px;font-weight:900}",

"#trtt-voyage-menu .tv-search{height:47px;max-width:620px;flex:1;margin-left:auto;display:flex;align-items:center;gap:10px;padding:0 15px;border:1px solid #eee8ec;border-radius:15px;background:#f9f8fa}#trtt-voyage-menu .tv-search svg{width:20px;height:20px;stroke:#85818a;fill:none;stroke-width:2}#trtt-voyage-menu .tv-search input{width:100%;min-width:0;border:0;outline:0;background:transparent;font:500 14px system-ui;color:#25283a}#trtt-voyage-menu .tv-theme{width:38px;height:38px;flex:0 0 38px;border:1px solid #eee8ec;border-radius:12px;background:#fff;color:#343342;font-size:17px;cursor:pointer;display:grid;place-items:center}#trtt-voyage-menu .tv-close{width:40px;height:40px;flex:0 0 40px;border:0;border-radius:14px;background:#f5f3f5;color:#343342;font-size:27px;cursor:pointer}",

" #trtt-voyage-menu .tv-main{width:min(1160px,100%);margin:auto;padding:clamp(13px,2.2vw,25px) clamp(13px,3vw,34px) 24px}#trtt-voyage-menu .tv-hero{min-height:clamp(210px,27vw,310px);position:relative;display:flex;align-items:flex-end;overflow:hidden;border-radius:clamp(20px,3vw,32px);background:#d8e4ec url('"+CFG.photo+"') center/cover no-repeat;box-shadow:0 18px 50px #29364b1b}#trtt-voyage-menu .tv-hero:before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,#10192bc9,#15243b65 58%,#17243a05),linear-gradient(0deg,#121a2b65,transparent 70%)}#trtt-voyage-menu .tv-hero-copy{position:relative;padding:clamp(24px,5vw,58px);color:#fff;max-width:780px}#trtt-voyage-menu .tv-eyebrow{display:inline-block;margin-bottom:13px;padding:7px 11px;border:1px solid #ffffff66;border-radius:999px;background:#ffffff20;font-size:10px;font-weight:850;letter-spacing:1.4px}#trtt-voyage-menu .tv-hero h1{margin:0;font-size:clamp(29px,5.2vw,58px);line-height:1.05;letter-spacing:-1.8px;font-weight:900}#trtt-voyage-menu .tv-hero p{margin:14px 0 0;max-width:590px;color:#ffffffed;font-size:clamp(13px,1.5vw,17px);line-height:1.65}",

"#trtt-voyage-menu .tv-heading{margin:25px 2px 14px}#trtt-voyage-menu .tv-heading h2{margin:0;font-size:clamp(22px,3vw,30px);letter-spacing:-.8px}#trtt-voyage-menu .tv-heading p{margin:6px 0 0;color:#85818c;font-size:13px}#trtt-voyage-menu .tv-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px}#trtt-voyage-menu .tv-card{position:relative;overflow:hidden;min-height:145px;padding:17px;display:flex;flex-direction:column;align-items:flex-start;border:1px solid #f0e9ed;border-radius:21px;background:linear-gradient(145deg,#fff,#fffafb);text-align:left;cursor:pointer;box-shadow:0 7px 22px #29243a08;transition:transform .18s,border-color .18s,box-shadow .18s}#trtt-voyage-menu .tv-card:after{content:'';position:absolute;inset:-40% auto -40% -65%;width:42%;pointer-events:none;transform:skewX(-20deg);background:linear-gradient(90deg,transparent,#ffffffc9 48%,transparent);animation:tv-glass-sweep 3s ease-in-out infinite}#trtt-voyage-menu .tv-card:hover{transform:translateY(-4px);border-color:#ffc1ce;box-shadow:0 15px 30px #29243a12}#trtt-voyage-menu .tv-ico{width:45px;height:45px;display:grid;place-items:center;border-radius:15px;background:#fff0f3;font-size:23px}#trtt-voyage-menu .tv-title{margin:15px 0 5px;font-size:15px;line-height:1.3;font-weight:850}#trtt-voyage-menu .tv-desc{margin:0;color:#85818c;font-size:12px;line-height:1.55}#trtt-voyage-menu .tv-arrow{margin-top:auto;padding-top:13px;color:#e35b7b;font-size:13px;font-weight:800}",

"#trtt-voyage-menu .tv-ai{min-height:66px;margin:29px 0 0;padding:14px 22px;display:flex;align-items:center;justify-content:center;gap:12px;border-radius:19px;background:linear-gradient(100deg,#f65f83,#ff8da4);color:#fff;text-decoration:none;text-align:center;font-size:17px;font-weight:900;box-shadow:0 12px 28px #ff6b8b3d}",

"#trtt-voyage-menu .tv-detail[hidden],#trtt-voyage-menu .tv-home[hidden]{display:none!important}#trtt-voyage-menu .tv-detail-head{display:flex;align-items:center;gap:14px;margin:4px 0 23px}#trtt-voyage-menu .tv-back{min-height:42px;padding:0 15px;border:1px solid #eee8ec;border-radius:12px;background:#fff;color:#343342;font-size:13px;font-weight:750;cursor:pointer}#trtt-voyage-menu .tv-detail h2{margin:0;font-size:clamp(22px,3vw,31px);letter-spacing:-.8px}#trtt-voyage-menu .tv-detail p{margin:5px 0 0;color:#89838c;font-size:13px}#trtt-voyage-menu .tv-posts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}#trtt-voyage-menu .tv-post{overflow:hidden;border:1px solid #f0eaf0;border-radius:18px;background:#fff;box-shadow:0 7px 22px #29243a09}#trtt-voyage-menu .tv-post img{display:block;width:100%;height:165px;object-fit:cover;background:#f8e8ed}#trtt-voyage-menu .tv-post h3{margin:13px 15px 17px;font-size:15px;line-height:1.45}#trtt-voyage-menu .tv-post a{color:#292b3d;text-decoration:none}#trtt-voyage-menu .tv-status{grid-column:1/-1;padding:28px;border:1px dashed #eadfe5;border-radius:16px;color:#827c85;text-align:center;font-size:14px}",

"#trtt-voyage-menu .tv-live-stage{min-height:clamp(230px,26vw,320px);position:relative;isolation:isolate;overflow:hidden;border:1px solid #ffffffa8;border-radius:clamp(20px,3vw,32px);background:radial-gradient(ellipse at 12% 8%,#ff9f4380,transparent 42%),radial-gradient(ellipse at 88% 20%,#a55eea70,transparent 42%),radial-gradient(ellipse at 68% 88%,#ff6b8b65,transparent 45%),linear-gradient(135deg,#eaf8f1 0%,#f9f6ff 46%,#fff4ed 100%);box-shadow:0 18px 50px #29364b12}#trtt-voyage-menu .tv-live-photo{position:absolute;inset:-5%;z-index:-3;background:url('"+CFG.photo+"') center/cover no-repeat;opacity:.30;filter:saturate(1.15) contrast(1.03);transform-origin:center;animation:tv-photo-kenburns 10s ease-in-out infinite alternate}#trtt-voyage-menu .tv-live-sky{position:absolute;inset:-25%;z-index:-2;background:conic-gradient(from 0deg at 50% 50%,#ff9f4320,#ff6b8b35,#a55eea35,#42c99a30,#ff9f4320);filter:blur(28px);animation:tv-sky-drift 9s ease-in-out infinite alternate}#trtt-voyage-menu .tv-live-wave{position:absolute;z-index:-1;left:-12%;width:125%;height:48%;bottom:-21%;border-radius:48% 52% 0 0/30% 36% 0 0;filter:blur(1px);transform:rotate(-5deg);animation:tv-wave-flow 5s ease-in-out infinite alternate}#trtt-voyage-menu .tv-wave-one{background:linear-gradient(110deg,#42c99a70,#a55eea45 48%,#ff6b8b65 78%,#ff9f4360)}#trtt-voyage-menu .tv-wave-two{bottom:-29%;left:-18%;height:42%;opacity:.7;background:linear-gradient(100deg,#a55eea55,#ff6b8b55,#ff9f4370,#42c99a55);animation-duration:5s;animation-direction:alternate-reverse}#trtt-voyage-menu .tv-live-road{position:absolute;z-index:-1;width:46%;height:74%;right:-4%;bottom:-38%;border:2px solid #ffffff85;border-radius:50% 50% 0 0;transform:rotate(-22deg);box-shadow:0 0 0 15px #ffffff17,0 0 0 34px #ffffff12;opacity:.8;animation:tv-road-glide 6s ease-in-out infinite alternate}#trtt-voyage-menu .tv-live-copy{position:relative;z-index:1;padding:clamp(24px,5vw,58px);max-width:820px;color:#283044}#trtt-voyage-menu .tv-live-wordmark{display:flex;align-items:center;gap:13px;margin:0 0 18px;width:max-content}#trtt-voyage-menu .tv-live-wordmark>span{font-size:clamp(42px,7vw,76px);line-height:.95;font-weight:950;letter-spacing:-5px;background:linear-gradient(105deg,#ff9f43 0%,#ff6b8b 28%,#ffffff 43%,#a55eea 58%,#42c99a 78%,#ff9f43 100%);background-size:300% 100%;background-clip:text;-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 9px #ff6b8b65);animation:tv-trtt-shimmer 2s linear infinite,tv-trtt-glow 2.6s ease-in-out infinite alternate}#trtt-voyage-menu .tv-live-wordmark i{display:flex;align-items:center;gap:6px;padding:7px 10px;border:1px solid #ffffffd9;border-radius:999px;background:#ffffffa8;box-shadow:0 5px 18px #35405512;color:#344054;font-size:10px;font-style:normal;font-weight:900;letter-spacing:1.2px;backdrop-filter:blur(12px)}#trtt-voyage-menu .tv-live-wordmark i b{width:7px;height:7px;border-radius:50%;background:#24b77b;box-shadow:0 0 0 4px #24b77b20;animation:tv-live-pulse 2.3s ease-in-out infinite}#trtt-voyage-menu .tv-live-copy .tv-eyebrow{color:#51475f;border-color:#ffffffb8;background:#ffffff80}#trtt-voyage-menu .tv-live-copy h1{margin:0;font-size:clamp(27px,4.7vw,54px);line-height:1.07;letter-spacing:-1.7px;font-weight:900;color:#263047}#trtt-voyage-menu .tv-live-copy p{max-width:590px;margin:13px 0 0;color:#596174;font-size:clamp(13px,1.5vw,17px);line-height:1.65}#trtt-voyage-menu .tv-typing{display:flex;align-items:center;gap:5px;margin:12px 0 0 2px;color:#596174;font-size:11px;font-weight:750;letter-spacing:.5px}#trtt-voyage-menu .tv-typing span{width:5px;height:5px;border-radius:50%;background:#a55eea;animation:tv-typing-blink 1s ease-in-out infinite}#trtt-voyage-menu .tv-typing span:nth-child(2){animation-delay:.18s}#trtt-voyage-menu .tv-typing span:nth-child(3){animation-delay:.36s}#trtt-voyage-menu .tv-live-caption{position:absolute;right:22px;bottom:19px;color:#5562749c;font-size:9px;font-weight:900;letter-spacing:1.5px}#trtt-voyage-menu .tv-credit{margin:17px 0 0;text-align:center;color:#89838e;font-size:11px;letter-spacing:.15px}#trtt-voyage-menu .tv-disclosure{max-width:900px;margin:7px auto 0;padding:0 12px;text-align:center;color:#77727c;font-size:10px;line-height:1.5}#trtt-voyage-menu .tv-credit strong{color:#51475f;font-weight:800}#trtt-voyage-menu .tv-credit a{color:#8c58c6;text-decoration:none;font-weight:800}#trtt-voyage-menu .tv-credit a:hover{text-decoration:underline}@keyframes tv-glass-sweep{0%{left:-65%;opacity:0}12%{opacity:.95}72%{opacity:.85}100%{left:130%;opacity:0}}@keyframes tv-photo-kenburns{0%{transform:scale(1) translate3d(-1%,0,0)}100%{transform:scale(1.16) translate3d(1%,-1%,0)}}@keyframes tv-road-glide{0%{transform:translate3d(-9px,0,0) rotate(-25deg);opacity:.48}100%{transform:translate3d(12px,-7px,0) rotate(-19deg);opacity:.95}}@keyframes tv-trtt-shimmer{0%{background-position:100% 50%}100%{background-position:-100% 50%}}@keyframes tv-trtt-glow{0%{filter:drop-shadow(0 0 4px #ff9f4380) brightness(1)}100%{filter:drop-shadow(0 0 17px #a55eea9c) brightness(1.22)}}@keyframes tv-typing-blink{0%,60%,100%{opacity:.25;transform:translateY(0) scale(.8)}30%{opacity:1;transform:translateY(-3px) scale(1.2)}}@keyframes tv-live-pulse{0%,100%{opacity:.72;box-shadow:0 0 0 3px #24b77b16}50%{opacity:1;box-shadow:0 0 0 6px #24b77b24}}@keyframes tv-sky-drift{0%{transform:translate3d(-2%,1%,0) rotate(0deg) scale(1)}100%{transform:translate3d(2%,-1%,0) rotate(8deg) scale(1.06)}}@keyframes tv-wave-flow{0%{transform:translate3d(-2%,0,0) rotate(-5deg)}100%{transform:translate3d(3%,-7px,0) rotate(-1deg)}}@keyframes tv-color-breathe{0%{background-position:0% 50%;filter:drop-shadow(0 3px 8px #ff9f4320)}100%{background-position:100% 50%;filter:drop-shadow(0 4px 12px #a55eea28)}}#trtt-voyage-menu.tv-open .tv-live-photo,#trtt-voyage-menu.tv-open .tv-live-sky,#trtt-voyage-menu.tv-open .tv-live-wave,#trtt-voyage-menu.tv-open .tv-live-road,#trtt-voyage-menu.tv-open .tv-live-wordmark>span,#trtt-voyage-menu.tv-open .tv-live-wordmark i b,#trtt-voyage-menu.tv-open .tv-typing span,#trtt-voyage-menu.tv-open .tv-card:after{animation-play-state:running}#trtt-voyage-menu:not(.tv-open) .tv-live-photo,#trtt-voyage-menu:not(.tv-open) .tv-live-sky,#trtt-voyage-menu:not(.tv-open) .tv-live-wave,#trtt-voyage-menu:not(.tv-open) .tv-live-road,#trtt-voyage-menu:not(.tv-open) .tv-live-wordmark>span,#trtt-voyage-menu:not(.tv-open) .tv-live-wordmark i b,#trtt-voyage-menu:not(.tv-open) .tv-typing span,#trtt-voyage-menu:not(.tv-open) .tv-card:after{animation-play-state:paused}@media(max-width:560px){#trtt-voyage-menu .tv-live-stage{min-height:250px}#trtt-voyage-menu .tv-live-copy{padding:22px}#trtt-voyage-menu .tv-live-wordmark>span{font-size:54px;letter-spacing:-3px}#trtt-voyage-menu .tv-live-copy h1{font-size:29px;letter-spacing:-.9px}#trtt-voyage-menu .tv-live-caption{right:14px;bottom:12px;font-size:7px}}/* Keep the requested live brand motion visible in every browser preference mode. */",

"@media(max-width:800px){#trtt-voyage-menu .tv-grid{grid-template-columns:repeat(2,minmax(0,1fr))}#trtt-voyage-menu .tv-posts{grid-template-columns:repeat(2,minmax(0,1fr))}#trtt-voyage-menu .tv-bar{gap:9px}}",

"@media(max-width:560px){#trtt-voyage-menu .tv-trigger{left:12px;top:12px;width:46px;height:46px}#trtt-voyage-menu .tv-bar{min-height:68px;padding:9px 12px;gap:8px;flex-wrap:wrap}#trtt-voyage-menu .tv-brand{gap:7px;font-size:14px}#trtt-voyage-menu .tv-logo{width:34px;height:34px;font-size:20px}#trtt-voyage-menu .tv-lock{padding:5px 6px;font-size:8px}#trtt-voyage-menu .tv-close{width:38px;height:38px;flex-basis:38px;margin-left:auto}#trtt-voyage-menu .tv-search{order:3;flex-basis:100%;max-width:none;height:43px;margin:0}#trtt-voyage-menu .tv-main{padding:14px 13px 30px}#trtt-voyage-menu .tv-hero{min-height:250px;border-radius:21px;background-position:55% center}#trtt-voyage-menu .tv-hero h1{font-size:31px;letter-spacing:-1px}#trtt-voyage-menu .tv-hero-copy{padding:23px}#trtt-voyage-menu .tv-grid{gap:10px}#trtt-voyage-menu .tv-card{min-height:157px;padding:15px;border-radius:17px}#trtt-voyage-menu .tv-title{font-size:13px}#trtt-voyage-menu .tv-desc{font-size:11px}#trtt-voyage-menu .tv-posts{grid-template-columns:1fr}#trtt-voyage-menu .tv-post img{height:190px}#trtt-voyage-menu .tv-ai{min-height:59px;font-size:15px}}",

"@media(prefers-reduced-motion:reduce){#trtt-voyage-menu *{transition:none!important;scroll-behavior:auto!important}}"
].join("\n");

const st=document.createElement("style");
st.textContent=css;
st.textContent += "#trtt-voyage-menu .tv-live-photo{transition:opacity 1.2s ease}#trtt-voyage-menu .tv-live-photo-next{position:absolute;inset:-5%;z-index:-2;background:center/cover no-repeat;opacity:0;filter:saturate(1.15) contrast(1.03);animation:tv-photo-kenburns 10s ease-in-out infinite alternate;transition:opacity 1.2s ease}#trtt-voyage-menu .tv-live-photo-next.tv-photo-active{opacity:.34}#trtt-voyage-menu .tv-live-photo.tv-photo-fade{opacity:0}#trtt-voyage-menu .tv-voyage-footer{position:relative;isolation:isolate;overflow:hidden;min-height:86px;margin:17px 0 0;padding:16px 18px;border:1px solid #eee7f0;border-radius:18px;background:linear-gradient(110deg,#fff8ef,#fff1f5 48%,#f4efff);text-align:center}#trtt-voyage-menu .tv-voyage-track{position:absolute;inset:0;z-index:-1;overflow:hidden;opacity:.75}#trtt-voyage-menu .tv-footer-cloud{position:absolute;top:7px;left:-18%;font-size:23px;opacity:.55;animation:tv-cloud-pass 18s linear infinite}#trtt-voyage-menu .tv-footer-plane{position:absolute;top:13px;left:-8%;font-size:19px;animation:tv-plane-pass 8s linear infinite}#trtt-voyage-menu .tv-footer-road{position:absolute;left:0;right:0;bottom:0;height:16px;background:repeating-linear-gradient(90deg,#a55eea55 0 24px,transparent 24px 43px),linear-gradient(#30313d,#30313d);background-size:43px 2px,100% 100%;background-position:0 7px,0 0;background-repeat:repeat-x;animation:tv-footer-road 1.2s linear infinite}#trtt-voyage-menu .tv-footer-wave{position:absolute;bottom:12px;left:-10%;width:120%;height:20px;border-radius:50%;border-top:3px solid #42c99a9c;animation:tv-footer-wave 4s ease-in-out infinite alternate}#trtt-voyage-menu .tv-voyage-caption{font-size:11px;font-weight:850;letter-spacing:.7px;color:#484458}@keyframes tv-plane-pass{0%{transform:translateX(-10vw) translateY(9px)}100%{transform:translateX(115vw) translateY(-4px)}}@keyframes tv-cloud-pass{0%{transform:translateX(-10vw)}100%{transform:translateX(120vw)}}@keyframes tv-footer-road{to{background-position:43px 7px,0 0}}@keyframes tv-footer-wave{0%{transform:translateX(-2%)}100%{transform:translateX(3%)}}#trtt-voyage-menu.tv-dark .tv-screen{background:#0f0f12;color:#f2f0f5}#trtt-voyage-menu.tv-dark .tv-bar{background:#121216ed;border-color:#29262f}#trtt-voyage-menu.tv-dark .tv-brand{color:#f5f2f7}#trtt-voyage-menu.tv-dark .tv-theme{background:#201e25;border-color:#39333f;color:#ffcf80}#trtt-voyage-menu.tv-dark .tv-close{background:#242229;color:#fff}#trtt-voyage-menu.tv-dark .tv-search{background:#1b1a20;border-color:#34303a}#trtt-voyage-menu.tv-dark .tv-search input{color:#f4f0f6}#trtt-voyage-menu.tv-dark .tv-heading h2,#trtt-voyage-menu.tv-dark .tv-detail h2{color:#f5f2f7}#trtt-voyage-menu.tv-dark .tv-heading p,#trtt-voyage-menu.tv-dark .tv-detail p{color:#aaa4b2}#trtt-voyage-menu.tv-dark .tv-card{background:linear-gradient(145deg,#1b1a20,#141318);border-color:#38313e;box-shadow:0 8px 25px #0008}#trtt-voyage-menu.tv-dark .tv-title{color:#f5f1f8}#trtt-voyage-menu.tv-dark .tv-desc{color:#aaa4b2}#trtt-voyage-menu.tv-dark .tv-ico{background:#30202a}#trtt-voyage-menu.tv-dark .tv-ai{box-shadow:0 0 25px #ff6b8b40,0 0 40px #a55eea20}#trtt-voyage-menu.tv-dark .tv-live-stage{background:linear-gradient(135deg,#17151c,#111116 55%,#17131a);border-color:#39313e;box-shadow:0 0 34px #a55eea18}#trtt-voyage-menu.tv-dark .tv-live-wordmark>span{filter:drop-shadow(0 0 9px #ff9f43a0) drop-shadow(0 0 17px #a55eea90) brightness(1.2)}#trtt-voyage-menu.tv-dark .tv-live-wordmark i{background:#19171dcc;border-color:#ffffff26;color:#f5eaf7}#trtt-voyage-menu.tv-dark .tv-live-copy .tv-eyebrow{color:#e5d9ed;border-color:#ffffff26;background:#ffffff0c}#trtt-voyage-menu.tv-dark .tv-live-copy h1{color:#f8f3fb}#trtt-voyage-menu.tv-dark .tv-live-copy p,#trtt-voyage-menu.tv-dark .tv-typing{color:#c2b9cb}#trtt-voyage-menu.tv-dark .tv-voyage-footer{background:linear-gradient(110deg,#211b18,#24181f 48%,#1e1928);border-color:#403344}#trtt-voyage-menu.tv-dark .tv-voyage-caption,#trtt-voyage-menu.tv-dark .tv-credit,#trtt-voyage-menu.tv-dark .tv-disclosure{color:#eee2f5}#trtt-voyage-menu.tv-dark .tv-post{background:#19181e;border-color:#39313e}#trtt-voyage-menu.tv-dark .tv-post a{color:#f5f1f8}#trtt-voyage-menu.tv-dark .tv-status{border-color:#51465a;color:#c1b6ca}#trtt-voyage-menu.tv-dark .tv-back{background:#211f26;border-color:#403944;color:#f3edf7}";
document.head.appendChild(st);

const cards=CFG.cats.map(c=>
'<button class="tv-card" type="button" data-category="'+esc(c.name)+'"><span class="tv-ico" aria-hidden="true">'+c.icon+'</span><span class="tv-title">'+esc(c.name)+'</span><span class="tv-desc">'+esc(c.desc)+'</span><span class="tv-arrow">Explore →</span></button>'
).join("");

const root=document.createElement("div");
root.id="trtt-voyage-menu";

root.innerHTML=
'<button class="tv-trigger" type="button" aria-label="Open TRTT Voyage" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>'+
'<div class="tv-screen" role="dialog" aria-modal="true" aria-label="TRTT Voyage full-screen menu"><header class="tv-bar"><a class="tv-brand" href="'+marked(CFG.home)+'"><span class="tv-logo">T</span><span>TRTT Voyage</span><span class="tv-lock">787950 LOCKED</span></a><button class="tv-theme" type="button" aria-label="Switch to dark mode" title="Switch theme">🌙</button><label class="tv-search"><svg viewBox="0 0 24 24"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 5 5"/></svg><input type="search" placeholder="Search trips, support, gear..." aria-label="Search TRTT Voyage" autocomplete="off"></label><button class="tv-close" type="button" aria-label="Close full-screen menu">×</button></header><main class="tv-main"><section class="tv-home"><section class="tv-live-stage" aria-label="TRTT Voyage live animated welcome"><div class="tv-live-photo" aria-hidden="true"></div><div class="tv-live-photo-next" aria-hidden="true"></div><div class="tv-live-sky"></div><div class="tv-live-wave tv-wave-one"></div><div class="tv-live-wave tv-wave-two"></div><div class="tv-live-road"></div><div class="tv-live-copy"><div class="tv-live-wordmark"><span>TRTT</span><i><b></b> LIVE</i></div><div class="tv-eyebrow">✦ TRAVEL MEETS TECHNOLOGY</div><h1>Welcome to TRTT Voyage<br>A World of Technology</h1><p>Travel smarter, stay connected and discover a world of possibilities — all in one place.</p><div class="tv-typing" aria-label="Live typing animation"><span></span><span></span><span></span><small>Voyage is live</small></div></div><div class="tv-live-caption">A JOURNEY THAT NEVER STANDS STILL</div></section><div class="tv-heading"><h2>Explore your world</h2><p>Everything you need for a smarter journey.</p></div><div class="tv-grid">'+cards+'</div><a class="tv-ai" href="'+CFG.ai+'" target="_blank" rel="noopener noreferrer">✦ &nbsp; AI Playground Only &nbsp; ↗</a><div class="tv-credit">Built by <strong>Cocvghuj</strong> on <a href="https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot" target="_blank" rel="noopener noreferrer">GitHub</a></div><div class="tv-disclosure">Disclosure: As an Amazon Associate and Travelpayouts partner, TRTT Voyage earns from qualifying purchases.</div><div class="tv-voyage-footer"><div class="tv-voyage-track"><span class="tv-footer-cloud">☁️</span><span class="tv-footer-plane">✈️</span><span class="tv-footer-wave"></span><span class="tv-footer-road"></span></div><div class="tv-voyage-caption">A Journey That Never Stands Still - TRTT Voyage - Sanluri to World</div></div></section><section class="tv-detail" hidden><div class="tv-detail-head"><button class="tv-back" type="button">← All categories</button><div><h2></h2><p>Explore the latest from TRTT Voyage.</p></div></div><div class="tv-posts" aria-live="polite"></div></section></main></div>';

document.body.appendChild(root);

const themeButton=root.querySelector(".tv-theme");
const trigger=root.querySelector(".tv-trigger"),
screen=root.querySelector(".tv-screen"),
close=root.querySelector(".tv-close"),
search=root.querySelector("input"),
home=root.querySelector(".tv-home"),
detail=root.querySelector(".tv-detail"),
posts=root.querySelector(".tv-posts"),
detailTitle=detail.querySelector("h2");

let req=0,focusBefore=null,photoTimer=null,photoIndex=0,activePhoto=root.querySelector(".tv-live-photo"),nextPhoto=root.querySelector(".tv-live-photo-next");
const THEME_KEY="trtt-voyage:theme";
function applyTheme(dark){root.classList.toggle("tv-dark",dark);themeButton.textContent=dark?"☀️":"🌙";themeButton.setAttribute("aria-label",dark?"Switch to light mode":"Switch to dark mode");try{localStorage.setItem(THEME_KEY,dark?"dark":"light");}catch(_){}}
try{applyTheme(localStorage.getItem(THEME_KEY)==="dark");}catch(_){applyTheme(false);}
themeButton.addEventListener("click",()=>applyTheme(!root.classList.contains("tv-dark")));
function startPhotos(){if(photoTimer)return;photoTimer=setInterval(()=>{photoIndex=(photoIndex+1)%VOYAGE_PHOTOS.length;const url=VOYAGE_PHOTOS[photoIndex],probe=new Image();probe.onload=()=>{nextPhoto.style.backgroundImage="url('"+url+"')";nextPhoto.classList.add("tv-photo-active");activePhoto.classList.add("tv-photo-fade");const old=activePhoto;activePhoto=nextPhoto;nextPhoto=old;setTimeout(()=>{nextPhoto.classList.remove("tv-photo-active","tv-photo-fade");},1300);};probe.src=url;},6000);}
function stopPhotos(){if(photoTimer){clearInterval(photoTimer);photoTimer=null;}}

function toggle(open){
root.classList.toggle("tv-open",open);
trigger.setAttribute("aria-expanded",String(open));
document.body.style.overflow=open?"hidden":"";
if(open){
focusBefore=document.activeElement;
startPhotos();
close.focus();
}else{
stopPhotos();
if(focusBefore&&focusBefore.focus){focusBefore.focus();}else{trigger.focus();}
}
}

function status(msg){
posts.replaceChildren();
const p=document.createElement("div");
p.className="tv-status";
p.textContent=msg;
posts.appendChild(p);
}

function render(items){
posts.replaceChildren();
if(!items.length){
status("No posts found in this category yet.");
return;
}
items.forEach(entry=>{
const name=entry.title&&entry.title.$t?entry.title.$t:"Travel story",
alt=(entry.link||[]).find(l=>l.rel==="alternate"&&l.type==="text/html"),
url=alt?marked(alt.href):marked(CFG.home),
imgUrl=entry.media$thumbnail&&entry.media$thumbnail.url
?entry.media$thumbnail.url.replace(/\/s\d+(-c)?\//,"/s640/")
:CFG.photo,
card=document.createElement("article"),
img=document.createElement("img"),
h=document.createElement("h3"),
a=document.createElement("a");

card.className="tv-post";
img.src=imgUrl;
img.alt="";
img.loading="lazy";
img.decoding="async";
a.href=url;
a.textContent=name;
h.appendChild(a);
card.append(img,h);
posts.appendChild(card);
});
}

async function load(url,label){
const id=++req;
status("Loading "+label+"…");
try{
const response=await fetch(url,{
credentials:"omit",
cache:"default",
headers:{Accept:"application/json"}
});
if(!response.ok)throw Error();
const data=await response.json();
if(id!==req)return;
render(data&&data.feed&&data.feed.entry?data.feed.entry:[]);
}catch(_){
if(id===req)status("Posts could not be loaded. Please check your connection and try again.");
}
}

function choose(name){
const cat=CFG.cats.find(c=>c.name===name);
if(!cat)return;
home.hidden=true;
detail.hidden=false;
detailTitle.textContent=name;
screen.scrollTo({top:0,behavior:"auto"});
try{localStorage.setItem(CFG.storage,name);}catch(_){}
const u=new URL("/feeds/posts/default/-/"+encodeURIComponent(name),CFG.home);
u.searchParams.set("alt","json");
u.searchParams.set("max-results","30");
u.searchParams.set("marker",LOCK.marker);
load(u.href,name);
}

function searchPosts(q){
const u=new URL("/feeds/posts/default",CFG.home);
u.searchParams.set("alt","json");
u.searchParams.set("max-results","30");
u.searchParams.set("q",q);
u.searchParams.set("marker",LOCK.marker);
home.hidden=true;
detail.hidden=false;
detailTitle.textContent="Search results";
screen.scrollTo({top:0,behavior:"auto"});
load(u.href,"search results");
}

function back(){
req++;
detail.hidden=true;
home.hidden=false;
search.value="";
root.querySelectorAll(".tv-card").forEach(c=>c.hidden=false);
screen.scrollTo({top:0,behavior:"auto"});
search.focus();
}

trigger.addEventListener("click",()=>toggle(!root.classList.contains("tv-open")));
close.addEventListener("click",()=>toggle(false));
root.querySelector(".tv-back").addEventListener("click",back);

root.querySelectorAll(".tv-card").forEach(b=>
b.addEventListener("click",()=>choose(b.dataset.category))
);

search.addEventListener("input",()=>{
if(!home.hidden){
const q=search.value.trim().toLocaleLowerCase();
root.querySelectorAll(".tv-card").forEach(b=>
b.hidden=!!q&&
!b.dataset.category.toLocaleLowerCase().includes(q)&&
!b.querySelector(".tv-desc").textContent.toLocaleLowerCase().includes(q)
);
}
});

search.addEventListener("keydown",e=>{
if(e.key==="Enter"&&search.value.trim())searchPosts(search.value.trim());
});

document.addEventListener("keydown",e=>{
if(e.key==="Escape"&&root.classList.contains("tv-open"))toggle(false);
if(e.key==="Tab"&&root.classList.contains("tv-open")){
const f=Array.from(screen.querySelectorAll("a[href],button:not([disabled]),input:not([disabled])"))
.filter(x=>!x.closest("[hidden]"));
if(!f.length)return;
if(e.shiftKey&&document.activeElement===f[0]){
e.preventDefault();
f[f.length-1].focus();
}else if(!e.shiftKey&&document.activeElement===f[f.length-1]){
e.preventDefault();
f[0].focus();
}
}
});
}

if(document.readyState==="loading"){
document.addEventListener("DOMContentLoaded",mount,{once:true});
}else{
mount();
}
})();
