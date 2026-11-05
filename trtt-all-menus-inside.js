/* TRTT VoyageHub — responsive all-menus panel */
(function () {
  "use strict";
  if (window.__TRTT_ALL_MENU_V2__) return;
  window.__TRTT_ALL_MENU_V2__ = true;

  var CFG = {
    telegram: "https://t.me/trttnews24bd",
    menus: [
      { name: "Home", icon: "⌂", href: "/" },
      { name: "Blog Stories", icon: "▤", href: "/blog/" },
      { name: "Flights", icon: "✈", href: "/tools/flight-search.html" },
      { name: "Travel Guides", icon: "⌖", href: "/travel-guide.html" },
      { name: "Destinations", icon: "◎", href: "/destinations/" },
      { name: "eSIM Guide", icon: "▣", href: "/tools/esim-compare.html" },
      { name: "News", icon: "✦", href: "/latest_travel_news.html" },
      { name: "About", icon: "i", href: "/about.html" }
    ],
    tools: [
      { name: "Flight Search", desc: "Explore routes and compare flight options", icon: "✈", href: "/tools/flight-search.html", tag: "FLIGHTS" },
      { name: "Baggage Checker", desc: "Check cabin-bag dimensions", icon: "▣", href: "/tools/baggage-size-checker.html", tag: "BAGGAGE" },
      { name: "Delay Calculator", desc: "Review possible EU delay compensation", icon: "◷", href: "/tools/delay-calculator.html", tag: "FLIGHT RIGHTS" },
      { name: "eSIM Comparison", desc: "Compare travel connectivity options", icon: "◉", href: "/tools/esim-compare.html", tag: "CONNECTIVITY" },
      { name: "Taxi Calculator", desc: "Estimate local transfer costs", icon: "⌁", href: "/tools/taxi-calculator.html", tag: "TRANSFERS" },
      { name: "Travel Map", desc: "Explore travel locations and references", icon: "◎", href: "/app.html", tag: "DISCOVER" }
    ]
  };

  function addStyles() {
    if (document.getElementById("trtt-all-menu-style-v2")) return;
    var style = document.createElement("style");
    style.id = "trtt-all-menu-style-v2";
    style.textContent = [
      "#trtt-all-overlay{position:fixed;inset:0;z-index:2147483645;display:none;overflow-y:auto;overscroll-behavior:contain;background:#f6f7fb;color:#17233d;font-family:Arial,sans-serif}",
      "#trtt-all-overlay.open{display:block;animation:trttMenuFade .18s ease-out}",
      "@keyframes trttMenuFade{from{opacity:0}to{opacity:1}}",
      "#trtt-all-overlay *{box-sizing:border-box}",
      "#trtt-all-overlay .trtt-top{position:sticky;top:0;z-index:3;display:flex;align-items:center;justify-content:space-between;gap:14px;padding:14px clamp(14px,3vw,30px);background:rgba(255,255,255,.94);border-bottom:1px solid #e7eaf1;backdrop-filter:blur(14px)}",
      "#trtt-all-overlay .trtt-brand{display:flex;align-items:center;gap:11px;min-width:0}",
      "#trtt-all-overlay .trtt-mark{width:42px;height:42px;flex:0 0 42px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,#ef476f,#ffc857);color:#14213d;font-size:21px;font-weight:900}",
      "#trtt-all-overlay .trtt-brand b{display:block;color:#14213d;font-size:15px;letter-spacing:.08em}",
      "#trtt-all-overlay .trtt-brand small{display:block;margin-top:4px;color:#8490a4;font-size:9px;letter-spacing:.12em}",
      "#trtt-all-overlay .trtt-close{width:42px;height:42px;flex:0 0 42px;border:1px solid #e7eaf1;border-radius:12px;background:#fff;color:#14213d;font-size:20px;cursor:pointer}",
      "#trtt-all-overlay .trtt-layout{display:grid;grid-template-columns:245px minmax(0,1fr);gap:20px;width:min(1240px,100%);margin:auto;padding:clamp(14px,3vw,30px)}",
      "#trtt-all-overlay .trtt-panel{min-width:0;padding:18px;border:1px solid #e7eaf1;border-radius:18px;background:#fff;box-shadow:0 10px 30px rgba(20,33,61,.05)}",
      "#trtt-all-overlay .trtt-kicker{margin:0 0 12px;color:#9aa3b3;font-size:10px;font-weight:800;letter-spacing:.16em}",
      "#trtt-all-overlay .trtt-nav{display:grid;gap:5px}",
      "#trtt-all-overlay .trtt-nav a{display:flex;align-items:center;gap:11px;padding:12px;border-radius:11px;color:#34415c;text-decoration:none;font-size:13px;font-weight:700}",
      "#trtt-all-overlay .trtt-nav a:hover,#trtt-all-overlay .trtt-nav a:focus-visible{outline:none;background:#fff0f3;color:#d93660}",
      "#trtt-all-overlay .trtt-nav-icon{width:28px;height:28px;display:grid;place-items:center;border-radius:9px;background:#f5f7fb;color:#d93660;font-size:15px}",
      "#trtt-all-overlay .trtt-main h2{margin:0 0 7px;color:#14213d;font-size:clamp(22px,3vw,30px);letter-spacing:-.03em}",
      "#trtt-all-overlay .trtt-intro{margin:0 0 20px;color:#69758b;font-size:13px;line-height:1.7}",
      "#trtt-all-overlay .trtt-tools{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}",
      "#trtt-all-overlay .trtt-tool{display:flex;align-items:flex-start;gap:12px;min-width:0;padding:16px;border:1px solid #e7eaf1;border-radius:15px;background:#fff;text-decoration:none;transition:transform .18s,border-color .18s,box-shadow .18s}",
      "#trtt-all-overlay .trtt-tool:hover{transform:translateY(-2px);border-color:#ef9db1;box-shadow:0 10px 24px rgba(20,33,61,.07)}",
      "#trtt-all-overlay .trtt-tool-icon{width:42px;height:42px;flex:0 0 42px;display:grid;place-items:center;border-radius:12px;background:#fff0f3;color:#d93660;font-size:20px}",
      "#trtt-all-overlay .trtt-tool b{display:block;color:#14213d;font-size:14px}",
      "#trtt-all-overlay .trtt-tool small{display:block;margin-top:5px;color:#69758b;font-size:11px;line-height:1.5}",
      "#trtt-all-overlay .trtt-tool em{display:block;margin-top:9px;color:#d93660;font-size:9px;font-style:normal;font-weight:800;letter-spacing:.12em}",
      "#trtt-all-overlay .trtt-bottom{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-top:18px;padding:16px;border-radius:15px;background:#14213d;color:#fff}",
      "#trtt-all-overlay .trtt-bottom p{margin:0;color:#d4dced;font-size:12px;line-height:1.6}",
      "#trtt-all-overlay .trtt-bottom a{flex:0 0 auto;padding:10px 14px;border-radius:10px;background:#ffc857;color:#14213d;text-decoration:none;font-size:11px;font-weight:900}",
      "#trtt-all-fab{position:fixed;left:16px;bottom:16px;z-index:2147483644;width:54px;height:54px;display:grid;place-items:center;border:2px solid rgba(255,255,255,.9);border-radius:17px;background:linear-gradient(135deg,#ef476f,#ffc857);box-shadow:0 8px 24px rgba(20,33,61,.22);color:#14213d;font-size:25px;font-weight:900;cursor:pointer}",
      "@media(max-width:760px){#trtt-all-overlay .trtt-top{padding:10px 13px}#trtt-all-overlay .trtt-layout{grid-template-columns:minmax(0,1fr);gap:12px;padding:12px}#trtt-all-overlay .trtt-panel{padding:14px;border-radius:15px}#trtt-all-overlay .trtt-nav{grid-template-columns:repeat(2,minmax(0,1fr));gap:5px}#trtt-all-overlay .trtt-nav a{padding:10px 8px;font-size:12px}#trtt-all-overlay .trtt-tools{grid-template-columns:minmax(0,1fr);gap:9px}#trtt-all-overlay .trtt-tool{padding:13px}#trtt-all-overlay .trtt-bottom{align-items:flex-start;flex-direction:column}#trtt-all-overlay .trtt-bottom a{width:100%;text-align:center}#trtt-all-fab{left:12px;bottom:12px;width:50px;height:50px;border-radius:15px}}",
      "@media(min-width:761px) and (max-width:980px){#trtt-all-overlay .trtt-layout{grid-template-columns:205px minmax(0,1fr);gap:12px}#trtt-all-overlay .trtt-tools{grid-template-columns:minmax(0,1fr)}}",
      "@media(prefers-reduced-motion:reduce){#trtt-all-overlay *{animation:none!important;transition:none!important}}"
    ].join("");
    document.head.appendChild(style);
  }

  function build() {
    if (document.getElementById("trtt-all-overlay")) return;
    var overlay = document.createElement("section");
    overlay.id = "trtt-all-overlay";
    overlay.setAttribute("aria-label", "TRTT VoyageHub menu");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("role", "dialog");

    var nav = CFG.menus.map(function (item) {
      return '<a href="' + item.href + '"><span class="trtt-nav-icon" aria-hidden="true">' + item.icon + '</span>' + item.name + '</a>';
    }).join("");
    var tools = CFG.tools.map(function (item) {
      return '<a class="trtt-tool" href="' + item.href + '">' +
        '<span class="trtt-tool-icon" aria-hidden="true">' + item.icon + '</span>' +
        '<span><b>' + item.name + '</b><small>' + item.desc + '</small><em>' + item.tag + ' · OPEN ↗</em></span></a>';
    }).join("");

    overlay.innerHTML =
      '<header class="trtt-top"><div class="trtt-brand"><span class="trtt-mark">T</span><span><b>TRTT VOYAGEHUB</b><small>NEWS · GUIDES · TRAVEL TOOLS</small></span></div>' +
      '<button class="trtt-close" type="button" aria-label="Close menu">×</button></header>' +
      '<div class="trtt-layout"><aside class="trtt-panel"><p class="trtt-kicker">EXPLORE TRTT</p><nav class="trtt-nav" aria-label="All TRTT sections">' + nav + '</nav></aside>' +
      '<main class="trtt-main"><section class="trtt-panel"><p class="trtt-kicker">THE TRAVEL TOOLKIT</p><h2>Plan your next journey.</h2><p class="trtt-intro">Useful tools and clear travel information, designed to make every step easier.</p><div class="trtt-tools">' + tools + '</div></section>' +
      '<div class="trtt-bottom"><p>Travel updates, useful guides and new tools from TRTT VoyageHub.</p><a href="' + CFG.telegram + '" target="_blank" rel="noopener noreferrer">Join TRTT on Telegram ↗</a></div></main></div>';

    document.body.appendChild(overlay);
    var close = overlay.querySelector(".trtt-close");
    close.addEventListener("click", closePanel);
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closePanel();
    });
    overlay.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closePanel();
    });
  }

  function closePanel() {
    var overlay = document.getElementById("trtt-all-overlay");
    if (overlay) overlay.classList.remove("open");
    var fab = document.getElementById("trtt-all-fab");
    if (fab) fab.setAttribute("aria-expanded", "false");
  }

  function addFab() {
    if (document.getElementById("trtt-all-fab")) return;
    var fab = document.createElement("button");
    fab.id = "trtt-all-fab";
    fab.type = "button";
    fab.textContent = "☰";
    fab.setAttribute("aria-label", "Open TRTT menu");
    fab.setAttribute("aria-controls", "trtt-all-overlay");
    fab.setAttribute("aria-expanded", "false");
    fab.addEventListener("click", function () {
      var overlay = document.getElementById("trtt-all-overlay");
      if (!overlay) return;
      overlay.classList.add("open");
      fab.setAttribute("aria-expanded", "true");
      var close = overlay.querySelector(".trtt-close");
      if (close) close.focus();
    });
    document.body.appendChild(fab);
  }

  function init() {
    addStyles();
    build();
    addFab();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true });
  else init();
})();
