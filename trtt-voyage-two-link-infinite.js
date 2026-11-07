(function () {
"use strict";
var HUB="https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950";
var STYLE="trtt-voyage-gadget-style", MENU="trtt-voyage-gadget-menu", CARD="trtt-voyage-sidebar-card";

function removeLegacy() {
 ["trtt-future-world","trtt-final-menu","trtt-final-menu-styles","trtt-future-ribbon","trtt-voyage-sidebar-card"]
 .forEach(function(id){var el=document.getElementById(id);if(el)el.remove();});
 document.querySelectorAll(".trtt-final-menu,.trtt-old-menu,[data-trtt-old-menu]").forEach(function(el){el.remove();});
}
function styles() {
 if(document.getElementById(STYLE))return;
 var css = [
 "#content-wrapper>.container,.content-wrapper>.container{display:grid!important;grid-template-columns:minmax(0,1fr) 290px!important;gap:30px!important;align-items:start!important}",
 "#main-wrapper{grid-column:1!important;grid-row:1!important;float:none!important;width:100%!important;max-width:100%!important;min-width:0!important}",
 "#sidebar-wrapper{display:block!important;grid-column:2!important;grid-row:1!important;float:none!important;width:290px!important;max-width:290px!important;min-width:0!important;margin:0!important;visibility:visible!important}",
 "#sidebar1{display:block!important;width:100%!important}",
 "#"+CARD+"{display:block!important;width:100%!important;margin:0 0 22px!important;padding:22px!important;box-sizing:border-box!important;border:1px solid rgba(255,255,255,.8)!important;border-radius:18px!important;background:linear-gradient(145deg,#fffefa,#eaf1f6)!important;box-shadow:0 14px 38px rgba(20,43,67,.1)!important;backdrop-filter:blur(18px)!important;-webkit-backdrop-filter:blur(18px)!important}",
 "#"+CARD+" .tv-eyebrow{margin:0 0 10px!important;color:#c65b43!important;font:800 9px/1.4 Arial,sans-serif!important;letter-spacing:.2em!important}",
 "#"+CARD+" .tv-heading{margin:0 0 10px!important;color:#142b43!important;font:500 30px/1.04 Georgia,serif!important;letter-spacing:-.045em!important}",
 "#"+CARD+" .tv-copy{margin:0 0 18px!important;color:#687586!important;font:13px/1.7 Arial,sans-serif!important}",
 "#"+CARD+" .tv-open{display:flex!important;align-items:center!important;justify-content:space-between!important;width:100%!important;min-height:46px!important;padding:0 15px!important;border:0!important;border-radius:9px!important;background:#142b43!important;color:#fff!important;font:700 12px/1.2 Arial,sans-serif!important;cursor:pointer!important}",
 "#"+CARD+" .tv-open span{color:#f0a18d!important;font-size:18px!important}",
 "#"+MENU+"{position:fixed!important;inset:0!important;z-index:2147483000!important;display:none!important;overflow-y:auto!important;padding:24px!important;background:rgba(12,27,43,.76)!important;backdrop-filter:blur(16px)!important;-webkit-backdrop-filter:blur(16px)!important}",
 "#"+MENU+".tv-visible{display:grid!important;place-items:center!important}",
 "#"+MENU+" .tv-panel{position:relative!important;width:min(760px,100%)!important;padding:clamp(25px,5vw,52px)!important;border:1px solid rgba(255,255,255,.8)!important;border-radius:22px!important;background:#f7f6f1!important;box-shadow:0 28px 90px rgba(0,0,0,.25)!important;box-sizing:border-box!important}",
 "#"+MENU+" .tv-close{position:absolute!important;top:18px!important;right:18px!important;width:42px!important;height:42px!important;border:1px solid #dedbd3!important;border-radius:50%!important;background:transparent!important;color:#142b43!important;font-size:25px!important;cursor:pointer!important}",
 "#"+MENU+" .tv-brand{margin:0 50px 12px 0!important;color:#142b43!important;font:800 12px/1.4 Arial,sans-serif!important;letter-spacing:.2em!important;text-transform:uppercase!important}",
 "#"+MENU+" .tv-title{max-width:570px!important;margin:25px 0 12px!important;color:#142b43!important;font:500 clamp(40px,8vw,76px)/.98 Georgia,serif!important;letter-spacing:-.06em!important}",
 "#"+MENU+" .tv-intro{max-width:510px!important;margin:0 0 25px!important;color:#687586!important;font:14px/1.75 Arial,sans-serif!important}",
 "#"+MENU+" .tv-link{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:16px!important;padding:19px 2px!important;border-top:1px solid #dedbd3!important;color:#142b43!important;text-decoration:none!important;font:500 clamp(20px,3vw,27px)/1.2 Georgia,serif!important}",
 "#"+MENU+" .tv-link:last-child{border-bottom:1px solid #dedbd3!important}",
 "#"+MENU+" .tv-link span{color:#c65b43!important;font:700 18px/1 Arial,sans-serif!important}",
 "body.tv-menu-open{overflow:hidden!important}",
 "@media(max-width:1000px){#content-wrapper>.container,.content-wrapper>.container{display:flex!important;flex-direction:column!important;gap:24px!important}#main-wrapper{order:1!important;width:100%!important;max-width:100%!important}#sidebar-wrapper{display:block!important;order:2!important;width:100%!important;max-width:100%!important;margin-top:8px!important}}",
 "@media(max-width:600px){#"+MENU+"{padding:12px!important}#"+MENU+" .tv-panel{padding:28px 22px!important;border-radius:17px!important}#"+MENU+" .tv-title{margin-top:32px!important}}"
 ].join("\n");
 var s=document.createElement("style");s.id=STYLE;s.textContent=css;document.head.appendChild(s);
}
function closeMenu(menu){menu.classList.remove("tv-visible");document.body.classList.remove("tv-menu-open");menu.setAttribute("aria-hidden","true");}
function openMenu(menu){menu.classList.add("tv-visible");document.body.classList.add("tv-menu-open");menu.setAttribute("aria-hidden","false");}
function makeMenu(){
 var menu=document.createElement("div");menu.id=MENU;menu.setAttribute("aria-hidden","true");
 var panel=document.createElement("div");panel.className="tv-panel";panel.setAttribute("role","dialog");panel.setAttribute("aria-modal","true");panel.setAttribute("aria-label","TRTT Voyage menu");
 var brand=document.createElement("div");brand.className="tv-brand";brand.textContent="TRTT Voyage";
 var close=document.createElement("button");close.className="tv-close";close.type="button";close.setAttribute("aria-label","Close menu");close.textContent="×";
 var title=document.createElement("h2");title.className="tv-title";title.textContent="Go further. Travel better.";
 var intro=document.createElement("p");intro.className="tv-intro";intro.textContent="Explore practical travel information, useful tools and stories from around the world.";
 var about=document.createElement("a");about.className="tv-link";about.href="/p/about-us.html";about.appendChild(document.createTextNode("About Us"));
 var aa=document.createElement("span");aa.textContent="↗";about.appendChild(aa);
 var tools=document.createElement("a");tools.className="tv-link";tools.href=HUB;tools.target="_blank";tools.rel="noopener noreferrer";tools.appendChild(document.createTextNode("Travel Tools"));
 var ta=document.createElement("span");ta.textContent="↗";tools.appendChild(ta);
 [brand,close,title,intro,about,tools].forEach(function(el){panel.appendChild(el);});
 menu.appendChild(panel);document.body.appendChild(menu);
 close.addEventListener("click",function(){closeMenu(menu);});
 menu.addEventListener("click",function(e){if(e.target===menu)closeMenu(menu);});
 document.addEventListener("keydown",function(e){if(e.key==="Escape"&&menu.classList.contains("tv-visible"))closeMenu(menu);});
 return menu;
}
function addSidebar(menu){
 var sidebar=document.getElementById("sidebar1");if(!sidebar)return false;
 var card=document.createElement("section");card.id=CARD;card.setAttribute("aria-label","TRTT Voyage navigation");
 var eyebrow=document.createElement("p");eyebrow.className="tv-eyebrow";eyebrow.textContent="TRAVEL • DISCOVER • EXPLORE";
 var heading=document.createElement("h2");heading.className="tv-heading";heading.textContent="Your next journey starts here.";
 var copy=document.createElement("p");copy.className="tv-copy";copy.textContent="Discover useful travel tools, smarter routes and stories from around the world.";
 var button=document.createElement("button");button.className="tv-open";button.type="button";button.appendChild(document.createTextNode("Explore TRTT Voyage"));
 var arrow=document.createElement("span");arrow.textContent="↗";button.appendChild(arrow);
 button.addEventListener("click",function(){openMenu(menu);});
 [eyebrow,heading,copy,button].forEach(function(el){card.appendChild(el);});
 sidebar.insertBefore(card,sidebar.firstChild);return true;
}
function infiniteScroll(){
 var pager=document.getElementById("blog-pager"),grid=document.querySelector("#main-wrapper .grid-posts");
 if(!pager||!grid||pager.dataset.tvInfinite==="1")return;
 var link=pager.querySelector("#load-more-link");if(!link||!link.getAttribute("data-load"))return;
 pager.dataset.tvInfinite="1";var busy=false,count=grid.querySelectorAll(".index-post").length,timer;
 function load(){
  link=pager.querySelector("#load-more-link");
  if(busy||!link||!link.getAttribute("data-load"))return;
  busy=true;count=grid.querySelectorAll(".index-post").length;link.click();
  clearTimeout(timer);timer=setTimeout(function(){busy=false;},18000);
 }
 var io=new IntersectionObserver(function(entries){if(entries.some(function(e){return e.isIntersecting;}))load();},{rootMargin:"850px 0px",threshold:0});
 io.observe(pager);
 var mo=new MutationObserver(function(){
  if(busy&&grid.querySelectorAll(".index-post").length>count){busy=false;clearTimeout(timer);}
 });
 mo.observe(grid,{childList:true,subtree:true});
 pager.addEventListener("click",function(e){if(e.target.closest("#load-more-link")){busy=true;count=grid.querySelectorAll(".index-post").length;}});
}
function watchLegacy(){
 var observer=new MutationObserver(function(){
  ["trtt-future-world","trtt-final-menu","trtt-final-menu-styles","trtt-future-ribbon"].forEach(function(id){var el=document.getElementById(id);if(el)el.remove();});
 });
 observer.observe(document.body,{childList:true,subtree:true});
}
function start(){
 if(!document.body||!document.head)return;
 removeLegacy();styles();watchLegacy();
 var menu=makeMenu(),attempt=0;
 function mount(){
  ["trtt-future-world","trtt-final-menu","trtt-final-menu-styles","trtt-future-ribbon"].forEach(function(id){var el=document.getElementById(id);if(el)el.remove();});
  if(addSidebar(menu)){infiniteScroll();return;}
  if(++attempt<40)setTimeout(mount,250);
 }
 mount();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});else start();
})();