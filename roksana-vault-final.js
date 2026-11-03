/* =========================================================
   ROKSANA NILLA — TRTT FINAL VAULT
   Strict 3-domain allowlist | 12-color rotation
   12 responsive cards | Live local clock | Duplicate protection
   ========================================================= */
(function () {
  "use strict";

  var ROOT_ID = "RoksanaFinalVault";
  var STYLE_ID = "roksana-final-vault-style";
  var ALLOWED = [
    "trttnews24bd.blogspot.com",
    "trttnews24bd.com",
    "www.trttnews24bd.com"
  ];
  var host = window.location.hostname.toLowerCase().trim();

  if (ALLOWED.indexOf(host) === -1) {
    var blocked = document.getElementById(ROOT_ID);
    if (blocked) blocked.remove();
    console.warn("[Roksana Vault] Domain not allowed:", host);
    return;
  }

  if (window.__ROKSANA_VAULT_INITIALIZED__) return;
  window.__ROKSANA_VAULT_INITIALIZED__ = true;

  var COLORS = [
    "#FF2E63", "#FFC300", "#AF7AC5", "#E8A0A8",
    "#967BB6", "#FF7F70", "#8E44AD", "#FFB38A",
    "#D946A6", "#F4D58D", "#6C3483", "#F7A8C4"
  ];

  var ITEMS = [
    ["TRTT Voyage", "Travel & Discovery", "TRTT Voyage"],
    ["Bangladesh", "দেশের খবর", "Bangladesh"],
    ["World News", "বিশ্ব সংবাদ", "World News"],
    ["Technology", "প্রযুক্তির খবর", "Technology"],
    ["Lifestyle", "জীবনযাপন", "Lifestyle"],
    ["Entertainment", "বিনোদন", "Entertainment"],
    ["Travel Stories", "ভ্রমণ কাহিনি", "Travel Stories"],
    ["Food & Culture", "খাবার ও সংস্কৃতি", "Food Culture"],
    ["Business", "ব্যবসা-বাণিজ্য", "Business"],
    ["Education", "শিক্ষা", "Education"],
    ["Health & Life", "স্বাস্থ্য ও জীবন", "Health Life"],
    ["All Articles", "সব প্রকাশনা", ""]
  ];

  var colorStep = 0;
  var clockTimer = null;
  var colorTimer = null;
  var observer = null;

  function searchUrl(term) {
    return term
      ? window.location.origin + "/search?q=" + encodeURIComponent(term)
      : window.location.origin + "/search";
  }

  function addStyles() {
    if (document.getElementById(STYLE_ID)) return;

    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = [
      "#" + ROOT_ID + "{box-sizing:border-box;width:min(1100px,calc(100% - 20px));margin:14px auto 20px;padding:3px;border-radius:19px;background:linear-gradient(115deg,#FF2E63,#FFC300,#AF7AC5,#E8A0A8,#967BB6,#FF7F70,#8E44AD,#FFB38A,#D946A6,#F4D58D,#6C3483,#F7A8C4);font-family:Arial,sans-serif;position:relative;z-index:20}",
      "#" + ROOT_ID + " *{box-sizing:border-box}",
      "#" + ROOT_ID + " .rv-inner{padding:19px;border-radius:16px;background:radial-gradient(circle at 10% 0%,#38213b 0,#171322 44%,#10111b 100%);color:#fff;overflow:hidden}",
      "#" + ROOT_ID + " .rv-head{text-align:center;margin:0 auto 16px}",
      "#" + ROOT_ID + " .rv-kicker{margin:0 0 7px;color:#f7c8d6;font-size:10px;letter-spacing:3px;text-transform:uppercase}",
      "#" + ROOT_ID + " .rv-title{margin:0;color:#ff8cad;font-size:clamp(21px,4vw,32px);line-height:1.2;font-weight:900;letter-spacing:.4px}",
      "#" + ROOT_ID + " .rv-sub{margin:8px 0 0;color:#f1dce8;font-size:13px;line-height:1.6}",
      "#" + ROOT_ID + " .rv-clock{display:inline-block;margin-top:11px;padding:6px 11px;border:1px solid rgba(255,255,255,.2);border-radius:99px;color:#fce7ef;font-size:11px;letter-spacing:.5px}",
      "#" + ROOT_ID + " .rv-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}",
      "#" + ROOT_ID + " .rv-card{display:flex;min-width:0;min-height:88px;flex-direction:column;justify-content:center;gap:6px;padding:12px 9px;border:1px solid var(--rv-color);border-radius:13px;background:linear-gradient(145deg,var(--rv-tint,#292033),#171522 78%);color:#fff;text-align:center;text-decoration:none;transition:transform .2s ease,box-shadow .2s ease}",
      "#" + ROOT_ID + " .rv-card:hover,#" + ROOT_ID + " .rv-card:focus-visible{transform:translateY(-3px);box-shadow:0 5px 16px rgba(255,46,99,.22);outline:2px solid var(--rv-color);outline-offset:2px}",
      "#" + ROOT_ID + " .rv-card strong{color:var(--rv-color);font-size:13px;line-height:1.3}",
      "#" + ROOT_ID + " .rv-card span{color:#eee6f0;font-size:10px;line-height:1.4}",
      "#" + ROOT_ID + " .rv-footer{margin:15px 0 0;color:#bdb3c7;font-size:10px;text-align:center}",
      "@media(max-width:700px){#" + ROOT_ID + " .rv-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}}",
      "@media(max-width:420px){#" + ROOT_ID + "{width:calc(100% - 14px)}#" + ROOT_ID + " .rv-inner{padding:14px 10px}#" + ROOT_ID + " .rv-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}#" + ROOT_ID + " .rv-card{min-height:78px}#" + ROOT_ID + " .rv-card strong{font-size:12px}}",
      "@media(prefers-reduced-motion:reduce){#" + ROOT_ID + " .rv-card{transition:none}#" + ROOT_ID + " .rv-card:hover{transform:none}}"
    ].join("\n");
    document.head.appendChild(style);
  }

  function createVault() {
    var root = document.getElementById(ROOT_ID);
    if (root) return root;

    root = document.createElement("section");
    root.id = ROOT_ID;
    root.setAttribute("aria-label", "Roksana Nilla Final Vault");

    var inner = document.createElement("div");
    inner.className = "rv-inner";

    var head = document.createElement("header");
    head.className = "rv-head";

    var kicker = document.createElement("p");
    kicker.className = "rv-kicker";
    kicker.textContent = "A Little World of Inspiration";

    var title = document.createElement("h2");
    title.className = "rv-title";
    title.textContent = "✨ ROKSANA NILLA'S FINAL VAULT ✨";

    var subtitle = document.createElement("p");
    subtitle.className = "rv-sub";
    subtitle.textContent = "Tomar Jonno — This Vault is for You | TRTT VOYAGE";

    var clock = document.createElement("div");
    clock.className = "rv-clock";
    clock.id = "rv-clock";
    clock.setAttribute("aria-live", "off");

    head.appendChild(kicker);
    head.appendChild(title);
    head.appendChild(subtitle);
    head.appendChild(clock);

    var grid = document.createElement("div");
    grid.className = "rv-grid";

    ITEMS.forEach(function (item, index) {
      var link = document.createElement("a");
      link.className = "rv-card";
      link.href = searchUrl(item[2]);
      link.style.setProperty("--rv-color", COLORS[index]);

      var name = document.createElement("strong");
      name.textContent = item[0];

      var description = document.createElement("span");
      description.textContent = item[1];

      link.appendChild(name);
      link.appendChild(description);
      grid.appendChild(link);
    });

    var footer = document.createElement("p");
    footer.className = "rv-footer";
    footer.textContent = "ROKSANA VAULT • 12-COLOR COLLECTION • TRTT VOYAGE";

    inner.appendChild(head);
    inner.appendChild(grid);
    inner.appendChild(footer);
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
    if (logo && !root.contains(logo)) {
      var container = logo.closest("header, .header-outer, .header-inner, #header") || logo;
      if (container.parentNode) {
        return { parent: container.parentNode, before: container.nextSibling };
      }
    }

    var feed = document.querySelector(
      "#Blog1, .blog-posts, .blog-posts-hfeed, .main-inner, #main, main, .post-outer-container"
    );
    if (feed && feed.parentNode && !root.contains(feed)) {
      return { parent: feed.parentNode, before: feed };
    }
    return null;
  }

  function placeVault() {
    var root = document.getElementById(ROOT_ID);
    if (!root || !document.body) return false;

    var target = findInsertionPoint(root);
    if (!target || !target.parent) return false;

    if (root.parentNode === target.parent && root.nextSibling === target.before) {
      return true;
    }
    target.parent.insertBefore(root, target.before || null);
    return true;
  }

  function updateClock() {
    var clock = document.getElementById("rv-clock");
    if (!clock) return;
    clock.textContent = "LOCAL TIME • " +
      new Intl.DateTimeFormat("en-GB", {
        dateStyle: "medium",
        timeStyle: "medium"
      }).format(new Date());
  }

  function rotateColors() {
    var elements = document.querySelectorAll("#" + ROOT_ID + " .rv-card");
    elements.forEach(function (element, index) {
      element.style.setProperty("--rv-color", COLORS[(index + colorStep) % COLORS.length]);
    });
    colorStep = (colorStep + 1) % COLORS.length;
  }

  function mount() {
    if (!document.body || !document.head) return;

    addStyles();
    var root = createVault();
    if (!root.parentNode) document.body.appendChild(root);

    placeVault();
    updateClock();
    rotateColors();

    if (clockTimer) window.clearInterval(clockTimer);
    clockTimer = window.setInterval(updateClock, 1000);

    if (colorTimer) window.clearInterval(colorTimer);
    colorTimer = window.setInterval(rotateColors, 2800);

    if (observer) observer.disconnect();
    if (window.MutationObserver) {
      var queued = false;
      observer = new MutationObserver(function () {
        if (queued) return;
        queued = true;
        window.requestAnimationFrame(function () {
          queued = false;
          placeVault();
        });
      });
      observer.observe(document.body, { childList: true, subtree: true });
    }

    window.RoksanaVault = {
      name: "ROKSANA NILLA'S FINAL VAULT",
      allowedDomains: ALLOWED.slice(),
      colors: COLORS.slice(),
      cards: ITEMS.length
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount, { once: true });
  } else {
    mount();
  }
})();
