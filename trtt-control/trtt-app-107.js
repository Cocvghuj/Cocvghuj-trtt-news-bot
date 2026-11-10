/*! TRTT VOYAGE — THINKING ROOM / V107 */
(function () {
"use strict";
if (window.__TRTT_THINKING_ROOM_V107__) return;
window.__TRTT_THINKING_ROOM_V107__ = true;
var ROUTES=[
["Home","/","Start here"],["My Diary","/search/label/My%20Diary","Personal journal"],
["Flight","/search/label/Flight","Flight services"],["Ride","/search/label/Ride","Ride services"],
["eSIM","/search/label/eSIM","Stay connected"],["Tour","/search/label/Tour","Explore places"],
["Shop","/search/label/Shop","TRTT Shop"],["Night","/search/label/Night","Night services"]];
function el(tag,cls,txt){var n=document.createElement(tag);if(cls)n.className=cls;if(txt!=null)n.textContent=txt;return n;}
function link(route,cls){var a=el("a",cls);a.href=route[1];a.appendChild(el("strong","",route[0]));a.appendChild(el("span","",route[2]));return a;}
function mountTarget(){var slot=document.querySelector("#header-wrap .header-menu");if(slot)return{slot:slot,old:slot.querySelector("#main-menu")};var old=document.querySelector("#header-wrap #main-menu");return old?{slot:old.parentNode,old:old}:null;}
function buildRoom(){
var o=el("section","trtt-room-overlay");o.id="trtt-room-overlay";o.setAttribute("role","dialog");o.setAttribute("aria-modal","true");o.setAttribute("aria-labelledby","trtt-room-title");o.setAttribute("aria-hidden","true");
var p=el("div","trtt-room-panel"),top=el("header","trtt-room-top"),identity=el("div","trtt-room-identity");
identity.appendChild(el("span","trtt-room-kicker","TRTT VOYAGE • IDEA SPACE"));identity.appendChild(el("h2","","THINKING ROOM"));identity.appendChild(el("p","","Muse  ✦  ChatGPT  ✦  Gemini"));
var close=el("button","trtt-room-close","×");close.type="button";close.setAttribute("aria-label","Close Thinking Room");top.appendChild(identity);top.appendChild(close);p.appendChild(top);
var lock=el("div","trtt-room-lock","ROKSANA — LOCKED");p.appendChild(lock);
var main=el("main","trtt-room-main");main.appendChild(el("span","trtt-room-kicker","TODAY'S THINKING"));
var q=el("h3","","What idea should TRTT Voyage explore today?");q.id="trtt-room-title";main.appendChild(q);
main.appendChild(el("p","trtt-room-description","A shared space for ideas, planning and creative work. Choose a destination below to continue exploring TRTT Voyage."));
var links=el("nav","trtt-room-links");links.setAttribute("aria-label","TRTT Voyage destinations");ROUTES.forEach(function(r){links.appendChild(link(r,"trtt-room-link"));});main.appendChild(links);p.appendChild(main);
p.appendChild(el("footer","trtt-room-footer","Made by MAC — Muse, Abu, ChatGPT"));o.appendChild(p);
function shut(){o.classList.remove("is-open");o.setAttribute("aria-hidden","true");document.body.classList.remove("trtt-room-open");if(o.returnFocus&&o.returnFocus.focus)o.returnFocus.focus();}
close.addEventListener("click",shut);o.addEventListener("click",function(e){if(e.target===o)shut();});
document.addEventListener("keydown",function(e){if(!o.classList.contains("is-open"))return;if(e.key==="Escape"){e.preventDefault();shut();}if(e.key==="Tab"){var f=o.querySelectorAll("a[href],button:not([disabled])");if(!f.length)return;var first=f[0],last=f[f.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}});
o.openRoom=function(trigger){o.returnFocus=trigger;o.classList.add("is-open");o.setAttribute("aria-hidden","false");document.body.classList.add("trtt-room-open");close.focus();};return o;
}
function buildNav(room){var n=el("nav","trtt-control-nav");n.id="trtt-control-nav";n.setAttribute("aria-label","TRTT Voyage main menu");
var brand=el("a","trtt-control-brand","TRTT VOYAGE");brand.href="/";n.appendChild(brand);
var list=el("div","trtt-route-list");ROUTES.forEach(function(r){list.appendChild(link(r,"trtt-route-bubble"));});n.appendChild(list);
var door=el("button","trtt-thinking-room-trigger");door.type="button";door.appendChild(el("span","trtt-door-icon","✦"));
var copy=el("span","trtt-door-copy");copy.appendChild(el("strong","","THINKING ROOM"));copy.appendChild(el("small","","ENTER THE IDEA SPACE"));door.appendChild(copy);door.appendChild(el("span","trtt-door-arrow","↗"));
door.addEventListener("click",function(){room.openRoom(door);});n.appendChild(door);return n;
}
function mount(){var t=mountTarget();if(!t||!t.slot||!document.body)return false;
var oldNav=document.getElementById("trtt-control-nav");if(oldNav)oldNav.remove();var oldRoom=document.getElementById("trtt-room-overlay");if(oldRoom)oldRoom.remove();
var room=buildRoom(),nav=buildNav(room);if(t.old&&t.old.parentNode===t.slot)t.old.replaceWith(nav);else t.slot.appendChild(nav);document.body.appendChild(room);return true;}
function start(){if(mount())return;var obs=new MutationObserver(function(){if(mount())obs.disconnect();});obs.observe(document.documentElement,{childList:true,subtree:true});}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});else start();
})();