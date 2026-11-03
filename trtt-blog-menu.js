(function () {
  "use strict";

  var MENU_ID = "trtt-final-menu";
  var STYLE_ID = "trtt-final-menu-styles";
  var scriptUrl = document.currentScript && document.currentScript.src
    ? document.currentScript.src
    : "https://cocvghuj-trtt-news-bot.vercel.app/trtt-blog-menu.js";
  var configUrl = new URL("blog-control.json", scriptUrl).href;

  function hideLegacyLeftMenu() {
    var candidates = document.querySelectorAll("nav, [id*='menu' i], [class*='menu' i], [id*='nav' i], [class*='nav' i]");
    candidates.forEach(function (el) {
      if (!el || el.id === MENU_ID || el.closest("#" + MENU_ID)) return;
      var label = ((el.id || "") + " " + (typeof el.className === "string" ? el.className : "")).toLowerCase();
      if (!/(menu|nav)/.test(label) && el.tagName !== "NAV") return;
      var rect = el.getBoundingClientRect();
      if (rect.width > 0 && rect.width <= 380 && rect.height >= 70 &&
          rect.left <= 180 && el.querySelectorAll("a").length >= 2) {
        el.style.setProperty("display", "none", "important");
        el.style.setProperty("visibility", "hidden", "important");
      }
    });
  }

  function safeUrl(value) {
    if (typeof value !== "string") return null;
    if (value.charAt(0) === "/" || /^https:\/\//i.test(value)) return value;
    return null;
  }

  function installMenu(config) {
    if (!document.body || document.getElementById(MENU_ID)) return;
    config = config && typeof config === "object" ? config : {};
    var links = Array.isArray(config.menu)
      ? config.menu.map(function (item) {
          return item && {
            label: (item.icon ? item.icon + " " : "") + item.label,
            url: item.href
          };
        })
      : (Array.isArray(config.links) ? config.links : []);
    var theme = config.theme && typeof config.theme === "object" ? config.theme : {};
    var rootStyle = document.documentElement.style;
    rootStyle.setProperty("--trtt-brand-primary", theme.primary || "#052962");
    rootStyle.setProperty("--trtt-brand-accent", theme.accent || "#00A8E8");
    rootStyle.setProperty("--trtt-page-bg", theme.background || "#f8fafc");
    rootStyle.setProperty("--trtt-text", theme.text || "#1e293b");
    if (!links.length) {
      links = [
        { label: "Home", url: "/" },
        { label: "eSIM Guide", url: "/search/label/eSIM" },
        { label: "Flights", url: "/search/label/Flights" },
        { label: "Explore Life", url: "https://cocvghuj-trtt-news-bot.vercel.app/" },
        { label: "About Us", url: "/p/about-us.html" },
        { label: "Contact", url: "/p/contact.html" }
      ];
    }

    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = [
      "#trtt-final-menu{position:sticky;top:0;z-index:99999;width:100%;background:linear-gradient(110deg,#101b36 0%,#172b52 65%,#243b66 100%);border-bottom:3px solid #ef476f;box-shadow:0 8px 26px rgba(15,23,42,.18);font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;box-sizing:border-box}",
      "#trtt-final-menu *{box-sizing:border-box}",
      "#trtt-final-menu .trtt-bar{max-width:1280px;min-height:68px;margin:0 auto;padding:8px 24px;display:flex;align-items:center;justify-content:space-between;gap:18px;position:relative}",
      "#trtt-final-menu .trtt-logo-txt{color:#fff;font-weight:900;font-size:17px;letter-spacing:.08em;white-space:nowrap;text-decoration:none;display:inline-flex;align-items:center;gap:10px}",
      "#trtt-final-menu .trtt-logo-txt:before{content:'T';display:inline-grid;place-items:center;width:34px;height:34px;border-radius:11px;background:linear-gradient(135deg,#ef476f,#ffc857);color:#101b36;font-size:18px;letter-spacing:0;box-shadow:0 4px 12px rgba(239,71,111,.28)}",
      "#trtt-final-menu .trtt-ham{display:none;border:1px solid rgba(255,255,255,.22);border-radius:12px;background:rgba(255,255,255,.08);color:#fff;font-size:23px;line-height:1;padding:9px 12px;cursor:pointer}",
      "#trtt-final-menu .trtt-links{display:flex;align-items:center;justify-content:flex-end;flex-wrap:wrap;list-style:none;margin:0;padding:0;gap:4px}",
      "#trtt-final-menu .trtt-links a{display:block;padding:11px 13px;border-radius:10px;color:#edf2ff!important;text-decoration:none;font-weight:700;font-size:13px;white-space:nowrap;transition:background .18s ease,color .18s ease,transform .18s ease}",
      "#trtt-final-menu .trtt-links a:hover,#trtt-final-menu .trtt-links a:focus-visible{background:rgba(255,255,255,.13);color:#ffc857!important;outline:2px solid rgba(255,200,87,.45);outline-offset:1px}",
      "#trtt-final-menu .trtt-links li:last-child a{background:#ef476f;color:#fff!important;box-shadow:0 5px 14px rgba(239,71,111,.25)}",
      "#trtt-final-menu .trtt-links li:last-child a:hover{background:#d93660;color:#fff!important}",
      "@media(max-width:900px){#trtt-final-menu .trtt-bar{padding:8px 16px}#trtt-final-menu .trtt-ham{display:block}#trtt-final-menu .trtt-links{display:none;position:absolute;left:0;right:0;top:100%;width:100%;padding:10px 14px 16px;flex-direction:column;align-items:stretch;flex-wrap:nowrap;background:#172b52;box-shadow:0 14px 22px rgba(15,23,42,.2)}#trtt-final-menu.open .trtt-links{display:flex}#trtt-final-menu .trtt-links a{padding:13px 14px;border-radius:9px;border-top:1px solid rgba(255,255,255,.08)}}",
      "@media(prefers-reduced-motion:reduce){#trtt-final-menu *{transition:none!important}}"
    ].join("\n");
    document.head.appendChild(style);

    var menu = document.createElement("nav");
    menu.id = MENU_ID;
    menu.setAttribute("aria-label", "Main navigation");
    menu.style.setProperty("--trtt-menu-bg", theme.menuBackground || theme.primary || config.menuBackground || "#052962");
    menu.style.setProperty("--trtt-menu-mobile-bg", theme.mobileBackground || config.mobileBackground || "#093b7a");
    menu.style.setProperty("--trtt-menu-text", theme.menuText || config.textColor || "#ffffff");

    var bar = document.createElement("div");
    bar.className = "trtt-bar";
    var brand = document.createElement("a");
    brand.className = "trtt-logo-txt";
    brand.href = "/";
    brand.textContent = typeof config.brand === "string" ? config.brand : "TRTT NEWS 24 BD";
    bar.appendChild(brand);

    var toggle = document.createElement("button");
    toggle.className = "trtt-ham";
    toggle.type = "button";
    toggle.textContent = "☰";
    toggle.setAttribute("aria-label", "Open menu");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", "trtt-main-links");
    bar.appendChild(toggle);

    var list = document.createElement("ul");
    list.className = "trtt-links";
    list.id = "trtt-main-links";
    links.forEach(function (item) {
      if (!item || typeof item.label !== "string") return;
      var href = safeUrl(item.url);
      if (!href) return;
      var li = document.createElement("li");
      var anchor = document.createElement("a");
      anchor.href = href;
      anchor.textContent = item.label;
      li.appendChild(anchor);
      list.appendChild(li);
    });
    bar.appendChild(list);
    menu.appendChild(bar);
    document.body.insertBefore(menu, document.body.firstChild);
    loadRoksanaVault();
    hideLegacyLeftMenu();

    function closeMenu() {
      menu.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
    }
    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      toggle.setAttribute("aria-label", expanded ? "Open menu" : "Close menu");
      menu.classList.toggle("open", !expanded);
    });
    list.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeMenu();
    });
    document.addEventListener("click", function (event) {
      if (!menu.contains(event.target)) closeMenu();
    });
    if (window.MutationObserver) {
      var observer = new MutationObserver(hideLegacyLeftMenu);
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }

  function loadRoksanaVault() {
    if (document.getElementById("roksana-vault-loader")) return;
    var script = document.createElement("script");
    script.id = "roksana-vault-loader";
    script.async = true;
    script.src = new URL("roksana-vault.js", scriptUrl).href;
    script.onerror = function () {
      if (window.console && console.warn) console.warn("Roksana Vault could not be loaded; check public asset access.");
    };
    document.head.appendChild(script);
  }

  function start() {
    if (!document.body) return;
    fetch(configUrl, { cache: "no-store" })
      .then(function (response) {
        if (!response.ok) throw new Error("Menu config unavailable");
        return response.json();
      })
      .then(installMenu)
      .catch(function () { installMenu(null); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();
