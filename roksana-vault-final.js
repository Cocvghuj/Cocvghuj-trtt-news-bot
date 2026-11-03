(function () {
  "use strict";

  var ROOT_ID = "RoksanaFinalVault";
  var STYLE_ID = "roksana-vault-styles";
  var TIMER_KEY = "__roksanaVaultTimer";
  var COLOR_TIMER_KEY = "__roksanaVaultColorTimer";
  var colorStep = 0;
  var OBSERVER_KEY = "__roksanaVaultObserver";
  var COLORS = [
    "#FF2E63", "#FFC300", "#AF7AC5", "#E8A0A8",
    "#967BB6", "#FF7F70", "#8E44AD", "#FFB38A",
    "#D946A6", "#F4D58D", "#6C3483", "#F7A8C4"
  ];
  var ITEMS = [
    ["Flight Finder", "Flights and fare searches", "flight"],
    ["eSIM Corner", "Mobile data and eSIM guides", "esim"],
    ["Hotel Finder", "Hotel ideas and travel stays", "hotel"],
    ["Italy Stories", "Italy travel information", "Italy"],
    ["Europe Guide", "Explore European destinations", "Europe"],
    ["Travel News", "Latest travel updates", "travel news"],
    ["Budget Trips", "Affordable travel ideas", "budget travel"],
    ["City Guides", "Practical city guides", "city guide"],
    ["Airport Help", "Airport and journey tips", "airport"],
    ["Travel Tools", "Useful travel planning tools", "travel tools"],
    ["Destinations", "Places to discover", "destinations"],
    ["TRTT Journal", "Read the travel blog", "travel"]
  ];

  function searchUrl(term) {
    return "/search?q=" + encodeURIComponent(term);
  }

  function addStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = [
      "#" + ROOT_ID + "{--rv-pink:#FF2E63;--rv-gold:#FFC300;box-sizing:border-box;width:min(1100px,calc(100% - 24px));margin:18px auto 22px;padding:2px;border-radius:20px;background:linear-gradient(115deg,#FF2E63,#FFC300,#AF7AC5,#E8A0A8,#967BB6,#FF7F70,#8E44AD,#FFB38A,#D946A6,#F4D58D,#6C3483,#F7A8C4);font-family:Arial,sans-serif;position:relative;z-index:20;}",
      "#" + ROOT_ID + " *{box-sizing:border-box}",
      "#" + ROOT_ID + " .rv-inner{border-radius:18px;padding:18px;background:radial-gradient(circle at 10% 0%,#38213b 0,#171322 42%,#10111b 100%);color:#fff;overflow:hidden}",
      "#" + ROOT_ID + " .rv-head{text-align:center;margin:0 auto 15px}",
      "#" + ROOT_ID + " .rv-kicker{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#f7c8d6;margin:0 0 6px}",
      "#" + ROOT_ID + " .rv-title{font-size:clamp(21px,4vw,32px);line-height:1.15;font-weight:900;letter-spacing:.5px;margin:0;background:linear-gradient(90deg,#fff,#FFC300,#ff8cad);background-clip:text;-webkit-background-clip:text;color:transparent}",
      "#" + ROOT_ID + " .rv-sub{font-size:13px;line-height:1.5;color:#f1dce8;margin:8px 0 0}",
      "#" + ROOT_ID + " .rv-live{display:inline-flex;align-items:center;gap:7px;margin-top:10px;padding:5px 10px;border:1px solid rgba(255,255,255,.18);border-radius:99px;color:#fce7ef;font-size:10px;letter-spacing:1px}",
      "#" + ROOT_ID + " .rv-dot{width:7px;height:7px;border-radius:50%;background:#69e6a5;box-shadow:0 0 10px #69e6a5}",
      "#" + ROOT_ID + " .rv-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}",
      "#" + ROOT_ID + " .rv-card{min-height:90px;padding:13px 10px;border:1px solid color-mix(in srgb,var(--rv-color) 65%,transparent);border-radius:13px;background:linear-gradient(145deg,color-mix(in srgb,var(--rv-color) 18%,#191725),#171522 72%);color:#fff;text-decoration:none;display:flex;flex-direction:column;justify-content:center;gap:6px;transition:transform .2s ease,border-color .2s ease,background .2s ease}",
      "#" + ROOT_ID + " .rv-card:hover,#" + ROOT_ID + " .rv-card:focus-visible{transform:translateY(-3px);border-color:var(--rv-color);background:linear-gradient(145deg,color-mix(in srgb,var(--rv-color) 30%,#191725),#171522 75%);outline:2px solid var(--rv-color);outline-offset:2px}",
      "#" + ROOT_ID + " .rv-card strong{font-size:13px;line-height:1.2;color:var(--rv-color)}",
      "#" + ROOT_ID + " .rv-card span{font-size:10px;line-height:1.35;color:#e8e2ec}",
      "#" + ROOT_ID + " .rv-foot{text-align:center;color:#bdb3c7;font-size:10px;margin:13px 0 0}",
      "@media(max-width:640px){#" + ROOT_ID + "{width:calc(100% - 16px);margin:12px auto 17px}#" + ROOT_ID + " .rv-inner{padding:14px 11px}#" + ROOT_ID + " .rv-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}#" + ROOT_ID + " .rv-card{min-height:82px;padding:10px 7px}#" + ROOT_ID + " .rv-card strong{font-size:11px}#" + ROOT_ID + " .rv-card span{font-size:9px}}",
      "@media(max-width:360px){#" + ROOT_ID + " .rv-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}",
      "@media(prefers-reduced-motion:reduce){#" + ROOT_ID + " .rv-card{transition:none}#" + ROOT_ID + " .rv-card:hover{transform:none}}"
    ].join("\n");
    document.head.appendChild(style);
  }

  function makeRoot() {
    var root = document.getElementById(ROOT_ID);
    if (root) return root;
    root = document.createElement("section");
    root.id = ROOT_ID;
    root.setAttribute("aria-label", "Roksana Nilla's travel vault");
    var inner = document.createElement("div");
    inner.className = "rv-inner";

    var head = document.createElement("header");
    head.className = "rv-head";
    var kicker = document.createElement("p");
    kicker.className = "rv-kicker";
    kicker.textContent = "A little world of travel inspiration";
    var title = document.createElement("h2");
    title.className = "rv-title";
    title.textContent = "ROKSANA NILLA'S FINAL VAULT";
    var sub = document.createElement("p");
    sub.className = "rv-sub";
    sub.textContent = "Tomar Jonno — This Vault is for You… তোমার জন্য";
    var live = document.createElement("span");
    live.className = "rv-live";
    var dot = document.createElement("i");
    dot.className = "rv-dot";
    dot.setAttribute("aria-hidden", "true");
    var liveText = document.createElement("span");
    liveText.id = "rv-clock";
    live.appendChild(dot);
    live.appendChild(liveText);
    head.appendChild(kicker);
    head.appendChild(title);
    head.appendChild(sub);
    head.appendChild(live);

    var grid = document.createElement("div");
    grid.className = "rv-grid";
    ITEMS.forEach(function (item, index) {
      var card = document.createElement("a");
      card.className = "rv-card";
      card.href = searchUrl(item[2]);
      card.style.setProperty("--rv-color", COLORS[index]);
      var name = document.createElement("strong");
      name.textContent = item[0];
      var desc = document.createElement("span");
      desc.textContent = item[1];
      card.appendChild(name);
      card.appendChild(desc);
      grid.appendChild(card);
    });

    var foot = document.createElement("p");
    foot.className = "rv-foot";
    foot.textContent = "ROKSANA NILLA'S VAULT  •  12 COLOR COLLECTION";
    inner.appendChild(head);
    inner.appendChild(grid);
    inner.appendChild(foot);
    root.appendChild(inner);
    return root;
  }

  function findInsertionPoint(root) {
    var header = document.querySelector(
      "#header, .header-outer, .header-inner, header#header, .blog-header, [role='banner']"
    );
    if (header && header !== root && !root.contains(header)) {
      return { parent: header.parentNode, before: header.nextSibling };
    }

    var logo = document.querySelector(
      ".header-widget a, .header-logo, #Header1, [class*='header-title'], [id*='Header']"
    );
    if (logo && logo.parentNode && !root.contains(logo)) {
      var headerContainer = logo.closest("header, .header-outer, .header-inner, #header") || logo;
      return { parent: headerContainer.parentNode, before: headerContainer.nextSibling };
    }

    var feed = document.querySelector(
      "#Blog1, .blog-posts, .blog-posts-hfeed, .main-inner, #main, main, .post-outer-container"
    );
    if (feed && feed.parentNode && !root.contains(feed)) {
      return { parent: feed.parentNode, before: feed };
    }
    return null;
  }

  function placeRoot() {
    var root = document.getElementById(ROOT_ID);
    if (!root || !document.body) return false;
    var target = findInsertionPoint(root);
    if (!target || !target.parent) return false;
    if (root.parentNode === target.parent && root.nextSibling === target.before) return true;
    target.parent.insertBefore(root, target.before || null);
    return true;
  }

  function cycleColors() {
    var cards = document.querySelectorAll("#" + ROOT_ID + " .rv-card");
    cards.forEach(function (card, index) {
      card.style.setProperty("--rv-color", COLORS[(index + colorStep) % COLORS.length]);
    });
    colorStep = (colorStep + 1) % COLORS.length;
  }

  function updateClock() {
    var clock = document.getElementById("rv-clock");
    if (!clock) return;
    clock.textContent = "LOCAL TIME " + new Date().toLocaleTimeString();
  }

  function mount() {
    if (!document.body || !document.head) return;
    addStyles();
    var root = makeRoot();
    if (!root.parentNode) document.body.appendChild(root);
    placeRoot();

    if (window[TIMER_KEY]) window.clearInterval(window[TIMER_KEY]);
    updateClock();
    window[TIMER_KEY] = window.setInterval(updateClock, 1000);
    if (window[COLOR_TIMER_KEY]) window.clearInterval(window[COLOR_TIMER_KEY]);
    cycleColors();
    window[COLOR_TIMER_KEY] = window.setInterval(cycleColors, 2800);

    if (window[OBSERVER_KEY]) window[OBSERVER_KEY].disconnect();
    if (window.MutationObserver) {
      var queued = false;
      window[OBSERVER_KEY] = new MutationObserver(function () {
        if (queued) return;
        queued = true;
        window.requestAnimationFrame(function () {
          queued = false;
          placeRoot();
        });
      });
      window[OBSERVER_KEY].observe(document.body, { childList: true, subtree: true });
    }
    window.RoksanaVault = { name: "ROKSANA NILLA'S FINAL VAULT", colors: COLORS.slice(), cards: ITEMS.length };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount, { once: true });
  } else {
    mount();
  }
})();

// Source entry for roksana-final-no-secret.yml; deploy output is generated from this file.
