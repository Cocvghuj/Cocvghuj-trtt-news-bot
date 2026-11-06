(function () {
  "use strict";
  var CONFIG = "https://cocvghuj-trtt-news-bot.vercel.app/blog-control.json";
  var ROOT = "trtt-world-menu";
  var CSS = "trtt-world-menu-css";
  var ICONS = ["⌂","▤","✈","↗","◉","▱","✦","⌘","ⓘ","✉"];
  var DESCRIPTIONS = [
    "The latest stories and updates",
    "News, reports and useful updates",
    "Discover Europe with confidence",
    "Plan routes and compare flights",
    "Stay connected wherever you go",
    "Find a better place to stay",
    "A private corner of the TRTT world",
    "Smart tools for your next journey",
    "The people and purpose behind TRTT",
    "Talk to the TRTT team"
  ];
  function safeUrl(value) {
    return typeof value === "string" && (value.charAt(0) === "/" || /^https:\/\//i.test(value)) ? value : null;
  }
  function addStyles() {
    if (document.getElementById(CSS)) return;
    var style = document.createElement("style");
    style.id = CSS;
    style.textContent = [
      "#"+ROOT+"{position:fixed;inset:0;z-index:2147483000;display:none;overflow-y:auto;overscroll-behavior:contain;background:radial-gradient(ellipse at 85% 5%,rgba(239,71,111,.22),transparent 32%),radial-gradient(ellipse at 0% 80%,rgba(65,126,190,.25),transparent 38%),linear-gradient(145deg,#071326 0%,#10284a 52%,#17213d 100%);color:#f7f9ff;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;opacity:0;transition:opacity .22s ease}",
      "body.trtt-world-open #"+ROOT+"{display:block;opacity:1}",
      "body.trtt-world-open{overflow:hidden!important}",
      "#"+ROOT+" *{box-sizing:border-box}",
      "#"+ROOT+" .tw-shell{width:min(100%,1040px);min-height:100%;margin:auto;padding:22px clamp(18px,5vw,48px) 36px}",
      "#"+ROOT+" .tw-top{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:8px 0 28px;border-bottom:1px solid rgba(255,255,255,.13)}",
      "#"+ROOT+" .tw-brand{font-size:13px;font-weight:900;letter-spacing:.18em;color:#fff;text-transform:uppercase}",
      "#"+ROOT+" .tw-brand span{display:block;margin-top:5px;color:#a9bad4;font-size:10px;font-weight:600;letter-spacing:.22em}",
      "#"+ROOT+" .tw-close{width:46px;height:46px;border:1px solid rgba(255,255,255,.24);border-radius:15px;background:rgba(255,255,255,.08);color:#fff;font-size:27px;line-height:1;cursor:pointer}",
      "#"+ROOT+" .tw-intro{padding:32px 0 22px}",
      "#"+ROOT+" .tw-kicker{color:#ff7798;font-size:11px;font-weight:800;letter-spacing:.2em;text-transform:uppercase}",
      "#"+ROOT+" .tw-title{margin:10px 0 8px;color:#fff;font-size:clamp(32px,7vw,58px);font-weight:900;letter-spacing:-.055em;line-height:1.02}",
      "#"+ROOT+" .tw-copy{max-width:580px;margin:0;color:#b9c7dc;font-size:14px;line-height:1.7}",
      "#"+ROOT+" .tw-search{display:flex;align-items:center;gap:10px;margin:22px 0 20px;padding:0 16px;height:52px;border:1px solid rgba(255,255,255,.17);border-radius:15px;background:rgba(255,255,255,.08)}",
      "#"+ROOT+" .tw-search span{color:#9fb1ca;font-size:19px}",
      "#"+ROOT+" .tw-search input{width:100%;border:0;outline:0;background:transparent;color:#fff;font-size:14px}",
      "#"+ROOT+" .tw-search input::placeholder{color:#9fb1ca}",
      "#"+ROOT+" .tw-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}",
      "#"+ROOT+" .tw-card{position:relative;display:flex;min-height:122px;flex-direction:column;justify-content:space-between;gap:12px;padding:17px;border:1px solid rgba(255,255,255,.13);border-radius:19px;background:linear-gradient(145deg,rgba(255,255,255,.105),rgba(255,255,255,.045));color:#fff;text-decoration:none;box-shadow:0 10px 26px rgba(0,0,0,.12);transition:transform .18s ease,border-color .18s ease,background .18s ease}",
      "#"+ROOT+" .tw-card:active{transform:scale(.985)}",
      "#"+ROOT+" .tw-card:hover{border-color:rgba(255,119,152,.7);background:linear-gradient(145deg,rgba(255,255,255,.16),rgba(255,255,255,.07))}",
      "#"+ROOT+" .tw-icon{display:grid;place-items:center;width:36px;height:36px;border-radius:12px;background:rgba(255,119,152,.15);color:#ff8aa7;font-size:19px;font-weight:800}",
      "#"+ROOT+" .tw-card strong{display:block;font-size:14px;font-weight:800;letter-spacing:-.01em}",
      "#"+ROOT+" .tw-card small{display:block;margin-top:4px;color:#aebed4;font-size:11px;line-height:1.45}",
      "#"+ROOT+" .tw-arrow{position:absolute;right:15px;top:17px;color:#91a5c2;font-size:17px}",
      "#"+ROOT+" .tw-footer{display:flex;justify-content:space-between;gap:12px;margin-top:24px;padding-top:18px;border-top:1px solid rgba(255,255,255,.12);color:#91a5c2;font-size:10px;letter-spacing:.08em}",
      "@media(min-width:700px){#"+ROOT+" .tw-grid{grid-template-columns:repeat(3,minmax(0,1fr))}#"+ROOT+" .tw-card{min-height:145px;padding:20px}}",
      "@media(max-width:360px){#"+ROOT+" .tw-grid{gap:9px}#"+ROOT+" .tw-card{min-height:116px;padding:13px}#"+ROOT+" .tw-card strong{font-size:13px}}",
      "@media(prefers-reduced-motion:reduce){#"+ROOT+"{transition:none}#"+ROOT+" .tw-card{transition:none}}"
    ].join("\n");
    document.head.appendChild(style);
  }
  function build(config) {
    if (document.getElementById(ROOT)) return;
    var items = Array.isArray(config.menu) ? config.menu : [];
    var overlay = document.createElement("section");
    overlay.id = ROOT;
    overlay.setAttribute("role","dialog");
    overlay.setAttribute("aria-modal","true");
    overlay.setAttribute("aria-label","TRTT NEWS 24 BD full screen menu");
    var shell = document.createElement("div");
    shell.className = "tw-shell";
    var top = document.createElement("div");
    top.className = "tw-top";
    var brand = document.createElement("div");
    brand.className = "tw-brand";
    brand.textContent = "TRTT NEWS 24 BD";
    var sub = document.createElement("span");
    sub.textContent = "TRAVEL • NEWS • DISCOVERY";
    brand.appendChild(sub);
    var close = document.createElement("button");
    close.className = "tw-close";
    close.type = "button";
    close.setAttribute("aria-label","Close menu");
    close.textContent = "×";
    top.appendChild(brand); top.appendChild(close);
    var intro = document.createElement("div");
    intro.className = "tw-intro";
    var kicker = document.createElement("div");
    kicker.className = "tw-kicker";
    kicker.textContent = "YOUR WORLD, OPENED";
    var title = document.createElement("h2");
    title.className = "tw-title";
    title.textContent = "Explore more.";
    var copy = document.createElement("p");
    copy.className = "tw-copy";
    copy.textContent = "Everything from TRTT in one place. Choose a world and start exploring.";
    intro.appendChild(kicker); intro.appendChild(title); intro.appendChild(copy);
    var search = document.createElement("label");
    search.className = "tw-search";
    var searchIcon = document.createElement("span"); searchIcon.textContent = "⌕";
    var input = document.createElement("input");
    input.type = "search"; input.placeholder = "Find a section…"; input.setAttribute("aria-label","Find a section");
    search.appendChild(searchIcon); search.appendChild(input);
    var grid = document.createElement("div"); grid.className = "tw-grid";
    items.forEach(function(item,index){
      if (!item || typeof item.label !== "string") return;
      var href = safeUrl(item.href); if (!href) return;
      var card = document.createElement("a");
      card.className = "tw-card"; card.href = href;
      var icon = document.createElement("span"); icon.className = "tw-icon"; icon.textContent = ICONS[index] || "✦";
      var arrow = document.createElement("span"); arrow.className = "tw-arrow"; arrow.textContent = "↗";
      var words = document.createElement("span");
      var heading = document.createElement("strong"); heading.textContent = item.label;
      var desc = document.createElement("small"); desc.textContent = DESCRIPTIONS[index] || "Explore this section";
      words.appendChild(heading); words.appendChild(desc);
      card.appendChild(icon); card.appendChild(arrow); card.appendChild(words);
      card.addEventListener("click", closeWorld);
      grid.appendChild(card);
    });
    var footer = document.createElement("div"); footer.className = "tw-footer";
    var footLeft = document.createElement("span"); footLeft.textContent = "TRTT VOYAGE";
    var footRight = document.createElement("span"); footRight.textContent = "DISCOVER • PLAN • GO";
    footer.appendChild(footLeft); footer.appendChild(footRight);
    shell.appendChild(top); shell.appendChild(intro); shell.appendChild(search); shell.appendChild(grid); shell.appendChild(footer);
    overlay.appendChild(shell); document.body.appendChild(overlay);
    close.addEventListener("click",closeWorld);
    overlay.addEventListener("click",function(e){if(e.target===overlay)closeWorld();});
    input.addEventListener("input",function(){
      var q=input.value.trim().toLowerCase();
      Array.prototype.forEach.call(grid.children,function(card){card.style.display=card.textContent.toLowerCase().indexOf(q)>=0?"flex":"none";});
    });
    function openWorld(){document.body.classList.add("trtt-world-open","nav-active");overlay.style.display="block";window.setTimeout(function(){input.focus();},80);}
    function closeWorld(){document.body.classList.remove("trtt-world-open","nav-active");overlay.style.display="none";}
    window.addEventListener("keydown",function(e){if(e.key==="Escape" && document.body.classList.contains("trtt-world-open"))closeWorld();});
    var legacyToggle=document.querySelector(".mobile-menu-toggle");
    if(legacyToggle && !legacyToggle.dataset.trttWorldBound){
      legacyToggle.dataset.trttWorldBound="1";
      legacyToggle.addEventListener("click",function(e){
        e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();
        if(document.body.classList.contains("trtt-world-open"))closeWorld();else openWorld();
      },true);
      legacyToggle.setAttribute("aria-label","Open TRTT full screen menu");
      legacyToggle.setAttribute("role","button");
      legacyToggle.setAttribute("tabindex","0");
    }
    var oldNav=document.getElementById("trtt-final-menu");
    if(oldNav)oldNav.remove();
    var oldBarStyle=document.getElementById("trtt-final-menu-styles");
    if(oldBarStyle)oldBarStyle.remove();
  }
  function start(){
    if(!document.body)return;
    addStyles();
    fetch(CONFIG,{cache:"no-store"}).then(function(r){if(!r.ok)throw new Error("config");return r.json();})
      .then(build).catch(function(){build({menu:[
        {label:"Home",href:"/"},{label:"Latest News",href:"/search/label/TRTT%20News"},
        {label:"Europe Travel",href:"/search/label/Europe%20Travel"},{label:"Flights",href:"/search/label/Flights"},
        {label:"eSIM",href:"/search/label/eSIM"},{label:"Hotels",href:"/search/label/Hotels"},
        {label:"Roksana Vault",href:"/p/roksana-vault.html"},{label:"Travel Tools",href:"https://cocvghuj-trtt-news-bot.vercel.app/"},
        {label:"About",href:"/p/about-us.html"},{label:"Contact",href:"/p/contact.html"}
      ]});});
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});else start();
})();