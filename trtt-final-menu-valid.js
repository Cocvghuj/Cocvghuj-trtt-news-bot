(function(){
"use strict";
var ROOT="trtt-future-world",STYLE="trtt-future-world-ui",CSS_URL="https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@be48117f5e1ac14732cf8fcce6dc72655903ac06/trtt-future-blog.css";
var HUB="https://cocvghuj-trtt-news-bot.vercel.app/";
var LINKS=[
 {title:"About Us",desc:"Who we are, what we believe and why we travel",href:"/p/about-us.html"},
 {title:"TRTT Voyage Hub",desc:"Your gateway to tools, routes and the wider TRTT world",href:HUB,external:true}
];
function sharpenHeaderLogo(){
 var img=document.querySelector("#header .header-image-wrapper img,.header-widget .header-image-wrapper img");
 if(!img||img.dataset.trttHiRes)return;
 var src=img.getAttribute("src")||"";
 if(/=s\d+(-c)?$/.test(src))img.setAttribute("src",src.replace(/=s\d+(-c)?$/,"=s480"));
 img.dataset.trttHiRes="1";
}
function addCSS(){
 if(!document.getElementById(STYLE)){
  var l=document.createElement("link");l.id=STYLE;l.rel="stylesheet";l.href=CSS_URL;document.head.appendChild(l);
 }
}
function safe(h){return typeof h==="string"&&(h.charAt(0)==="/"||/^https:\/\//i.test(h));}
function close(){document.body.classList.remove("trtt-future-open");var x=document.getElementById(ROOT);if(x)x.setAttribute("aria-hidden","true");}
function build(){
 if(document.getElementById(ROOT))return;
 var root=document.createElement("section");root.id=ROOT;root.setAttribute("aria-hidden","true");root.setAttribute("role","dialog");root.setAttribute("aria-modal","true");root.setAttribute("aria-label","TRTT Voyage navigation");
 var wrap=document.createElement("div");wrap.className="tf-wrap";
 var top=document.createElement("header");top.className="tf-top";
 var brand=document.createElement("a");brand.className="tf-brand";brand.href="/";brand.innerHTML="<span class='tf-monogram'>T.</span><span>TRTT <i>VOYAGE</i><small>INDEPENDENT TRAVEL & CULTURE</small></span>";
 var closeBtn=document.createElement("button");closeBtn.className="tf-close";closeBtn.type="button";closeBtn.setAttribute("aria-label","Close navigation");closeBtn.textContent="×";
 top.appendChild(brand);top.appendChild(closeBtn);
 var intro=document.createElement("div");intro.className="tf-intro";
 var eyebrow=document.createElement("div");eyebrow.className="tf-eyebrow";eyebrow.textContent="A DIFFERENT WAY TO EXPLORE";
 var h=document.createElement("h2");h.textContent="The world is\nnot a checklist."; 
 var p=document.createElement("p");p.textContent="Thoughtful travel stories, useful details and a little inspiration for the road ahead.";
 intro.appendChild(eyebrow);intro.appendChild(h);intro.appendChild(p);
 var body=document.createElement("div");body.className="tf-body";
 var list=document.createElement("nav");list.className="tf-list";list.setAttribute("aria-label","Explore TRTT");
 LINKS.forEach(function(item,i){if(!safe(item.href))return;var a=document.createElement("a");a.className="tf-link";a.href=item.href;if(item.external)a.target="_blank",a.rel="noopener";var n=document.createElement("span");n.className="tf-num";n.textContent=String(i+1).padStart(2,"0");var t=document.createElement("span");t.className="tf-text";var b=document.createElement("b");b.textContent=item.title;var s=document.createElement("small");s.textContent=item.desc;t.appendChild(b);t.appendChild(s);var ar=document.createElement("span");ar.className="tf-arrow";ar.textContent="↗";a.appendChild(n);a.appendChild(t);a.appendChild(ar);a.addEventListener("click",close);list.appendChild(a);});
 var aside=document.createElement("aside");aside.className="tf-aside";
 var art=document.createElement("div");art.className="tf-art";art.innerHTML="<span class='tf-art-orbit'></span><span class='tf-art-label'>FIELD NOTES<br/>FOR THE CURIOUS</span><span class='tf-art-mark'>T</span>";
 var note=document.createElement("p");note.className="tf-note";note.textContent="Go further. Look closer. Travel better.";
 aside.appendChild(art);aside.appendChild(note);body.appendChild(list);body.appendChild(aside);
 var foot=document.createElement("footer");foot.className="tf-foot";foot.innerHTML="<span>TRTT VOYAGE · EST. FOR THE CURIOUS</span><span>OPEN THE WORLD ↗</span>";
 wrap.appendChild(top);wrap.appendChild(intro);wrap.appendChild(body);wrap.appendChild(foot);root.appendChild(wrap);document.body.appendChild(root);
 function open(){document.body.classList.add("trtt-future-open");root.setAttribute("aria-hidden","false");closeBtn.focus();}
 closeBtn.addEventListener("click",close);root.addEventListener("click",function(e){if(e.target===root)close();});
 document.addEventListener("keydown",function(e){if(e.key==="Escape")close();});
 var toggle=document.querySelector(".mobile-menu-toggle");
 if(toggle&&!toggle.dataset.trttFuture){
  toggle.dataset.trttFuture="1";toggle.setAttribute("aria-label","Open TRTT Voyage navigation");toggle.setAttribute("role","button");toggle.setAttribute("tabindex","0");
  toggle.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();open();},true);
  toggle.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();open();}},true);
 }
 var nav=document.getElementById("trtt-final-menu");if(nav)nav.remove();
 var old=document.getElementById("trtt-final-menu-styles");if(old)old.remove();
 var ribbon=document.createElement("div");ribbon.id="trtt-future-ribbon";
 var left=document.createElement("div");var k=document.createElement("div");k.className="tf-kicker";k.textContent="TRTT VOYAGE / THE DAILY EDITION";var title=document.createElement("div");title.className="tf-head";title.textContent="A wider view of the world.";left.appendChild(k);left.appendChild(title);
 var date=document.createElement("div");date.className="tf-date";date.textContent="Stories • Guides • Journeys";
 ribbon.appendChild(left);ribbon.appendChild(date);
 var main=document.querySelector("#main-wrapper,.main");
 if(main&&main.parentNode)main.parentNode.insertBefore(ribbon,main);
}
function styles(){
 if(document.getElementById("trtt-future-world-css"))return;
 var s=document.createElement("style");s.id="trtt-future-world-css";
 s.textContent=[
 "#"+ROOT+"{position:fixed;inset:0;z-index:2147483000;display:none;overflow-y:auto;background:#f6f4ef;color:#101b2d;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}",
 "body.trtt-future-open{overflow:hidden!important}body.trtt-future-open #"+ROOT+"{display:block}",
 "#"+ROOT+" *{box-sizing:border-box}#"+ROOT+" .tf-wrap{max-width:1200px;min-height:100%;margin:auto;padding:24px clamp(20px,5vw,64px) 30px}",
 "#"+ROOT+" .tf-top{display:flex;align-items:center;justify-content:space-between;padding:5px 0 22px;border-bottom:1px solid #dedbd3}",
 "#"+ROOT+" .tf-brand{display:flex;align-items:center;gap:12px;color:#101b2d;text-decoration:none;font-size:13px;font-weight:900;letter-spacing:.14em}",
 "#"+ROOT+" .tf-brand i{font-style:normal;color:#d95b42}#"+ROOT+" .tf-brand small{display:block;margin-top:4px;color:#737b87;font-size:9px;letter-spacing:.2em}",
 "#"+ROOT+" .tf-monogram{display:grid;place-items:center;width:42px;height:42px;border-radius:50%;background:#d95b42;color:white;font-family:Georgia,serif;font-size:22px;letter-spacing:-.1em}",
 "#"+ROOT+" .tf-close{width:44px;height:44px;border:1px solid #dedbd3;border-radius:50%;background:transparent;color:#101b2d;font-size:27px;cursor:pointer}",
 "#"+ROOT+" .tf-intro{padding:clamp(35px,7vw,78px) 0 32px;max-width:780px}#"+ROOT+" .tf-eyebrow{color:#d95b42;font-size:10px;font-weight:900;letter-spacing:.22em}",
 "#"+ROOT+" .tf-intro h2{white-space:pre-line;margin:14px 0;font-family:Georgia,serif;font-size:clamp(43px,8vw,92px);line-height:.94;letter-spacing:-.065em;font-weight:500}",
 "#"+ROOT+" .tf-intro p{max-width:500px;color:#687386;font-size:15px;line-height:1.7}",
 "#"+ROOT+" .tf-body{display:grid;grid-template-columns:1.2fr .8fr;gap:clamp(30px,7vw,100px);align-items:stretch;border-top:1px solid #dedbd3;padding-top:18px}",
 "#"+ROOT+" .tf-link{display:grid;grid-template-columns:42px 1fr 24px;align-items:center;gap:14px;padding:16px 4px;border-bottom:1px solid #dedbd3;color:#101b2d;text-decoration:none;transition:padding .2s ease,color .2s ease}",
 "#"+ROOT+" .tf-link:hover{padding-left:12px;color:#d95b42}#"+ROOT+" .tf-num{font-size:10px;color:#d95b42;font-weight:800;letter-spacing:.12em}",
 "#"+ROOT+" .tf-text b{display:block;font-family:Georgia,serif;font-size:clamp(19px,2.4vw,25px);font-weight:500;letter-spacing:-.025em}",
 "#"+ROOT+" .tf-text small{display:block;margin-top:3px;color:#77808c;font-size:11px}#"+ROOT+" .tf-arrow{font-size:18px;color:#d95b42}",
 "#"+ROOT+" .tf-aside{display:flex;flex-direction:column;justify-content:center}#"+ROOT+" .tf-art{position:relative;display:grid;place-items:center;min-height:320px;overflow:hidden;background:#172b42;color:#f6f4ef}",
 "#"+ROOT+" .tf-art:before,#"+ROOT+" .tf-art:after{content:'';position:absolute;border:1px solid rgba(255,255,255,.22);border-radius:50%;width:240px;height:240px}",
 "#"+ROOT+" .tf-art:after{width:330px;height:330px;border-color:rgba(217,91,66,.6)}#"+ROOT+" .tf-art-orbit{position:absolute;width:420px;height:110px;border:1px solid rgba(255,255,255,.28);border-radius:50%;transform:rotate(-35deg)}",
 "#"+ROOT+" .tf-art-label{position:absolute;top:22px;left:22px;font-size:9px;line-height:1.6;letter-spacing:.22em;color:#e5a18e}",
 "#"+ROOT+" .tf-art-mark{font-family:Georgia,serif;font-size:150px;line-height:1;color:#f6f4ef;opacity:.95;z-index:1}",
 "#"+ROOT+" .tf-note{font-family:Georgia,serif;font-size:20px;font-style:italic;color:#687386}",
 "#"+ROOT+" .tf-foot{display:flex;justify-content:space-between;gap:12px;margin-top:45px;padding-top:18px;border-top:1px solid #dedbd3;color:#7c8490;font-size:9px;letter-spacing:.16em}",
 "@media(max-width:760px){#"+ROOT+" .tf-body{grid-template-columns:1fr}#"+ROOT+" .tf-aside{display:none}#"+ROOT+" .tf-intro{padding:38px 0 24px}#"+ROOT+" .tf-foot{margin-top:28px;flex-direction:column}#"+ROOT+" .tf-link{padding:14px 2px}}"
 ].join("\n");document.head.appendChild(s);
}

function enableInfiniteScroll(){
 var pager=document.getElementById("blog-pager");
 var grid=document.querySelector("#main-wrapper .grid-posts");
 if(!pager||!grid||pager.dataset.trttInfinite==="1")return;
 var link=pager.querySelector("#load-more-link");
 if(!link||!link.getAttribute("data-load"))return;
 pager.dataset.trttInfinite="1";
 var loading=false,before=0,failTimer=null,observer=null;
 function visible(el){return !!el&&window.getComputedStyle(el).display!=="none"&&el.offsetParent!==null;}
 function nearEnd(){
  var r=pager.getBoundingClientRect();
  return r.top < window.innerHeight+950 && r.bottom > -150;
 }
 function stopIfDone(){
  var done=pager.querySelector(".no-more.show");
  return !!done;
 }
 function requestNext(){
  link=pager.querySelector("#load-more-link");
  if(loading||!link||!link.getAttribute("data-load")||!visible(link)||stopIfDone())return;
  loading=true;
  before=grid.querySelectorAll(".index-post").length;
  link.click();
  failTimer=setTimeout(function(){
   if(!loading)return;
   var now=grid.querySelectorAll(".index-post").length;
   if(now===before&&!stopIfDone()){
    loading=false;
    if(link){link.style.display="inline-block";link.setAttribute("aria-label","Load more posts manually");}
   }
  },20000);
 }
 var mo=new MutationObserver(function(){
  var now=grid.querySelectorAll(".index-post").length;
  if(loading&&now>before){
   clearTimeout(failTimer);
   loading=false;
   if(!stopIfDone()&&nearEnd())setTimeout(requestNext,450);
  }
 });
 mo.observe(grid,{childList:true});
 if("IntersectionObserver" in window){
  observer=new IntersectionObserver(function(entries){
   if(entries.some(function(e){return e.isIntersecting;}))requestNext();
  },{root:null,rootMargin:"950px 0px",threshold:0});
  observer.observe(pager);
 }else{
  var ticking=false;
  window.addEventListener("scroll",function(){
   if(ticking)return;ticking=true;
   window.requestAnimationFrame(function(){ticking=false;if(nearEnd())requestNext();});
  },{passive:true});
 }
 pager.addEventListener("click",function(e){
  if(e.target.closest("#load-more-link")){loading=true;before=grid.querySelectorAll(".index-post").length;}
 });
}

function start(){
 addCSS();styles();sharpenHeaderLogo();enableInfiniteScroll();
 var wait=0;var timer=setInterval(function(){if(document.body&&document.querySelector(".mobile-menu-toggle")){clearInterval(timer);build();}else if(++wait>30){clearInterval(timer);if(document.body)build();}},250);
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});else start();
})();