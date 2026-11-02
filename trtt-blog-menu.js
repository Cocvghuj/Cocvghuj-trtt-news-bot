(function () {
  "use strict";

  var MENU_ID = "trtt-final-menu";
  var STYLE_ID = "trtt-final-menu-styles";
  var scriptUrl = document.currentScript && document.currentScript.src
    ? document.currentScript.src
    : "https://cocvghuj-trtt-news-bot.vercel.app/trtt-blog-menu.js";
  var configUrl = new URL("trtt-blog-menu.json", scriptUrl).href;

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
    var links = Array.isArray(config.links) ? config.links : [];
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
      "#trtt-final-menu{position:sticky;top:0;z-index:99999;width:100%;background:var(--trtt-menu-bg,#ff2e63);font-family:Arial,sans-serif;box-sizing:border-box}",
      "#trtt-final-menu *{box-sizing:border-box}",
      "#trtt-final-menu .trtt-bar{min-height:50px;padding:0 15px;display:flex;align-items:center;justify-content:space-between;gap:12px;position:relative}",
      "#trtt-final-menu .trtt-logo-txt{color:var(--trtt-menu-text,#fff);font-weight:800;font-size:16px;letter-spacing:1px;white-space:nowrap;text-decoration:none}",
      "#trtt-final-menu .trtt-ham{display:none;border:0;background:transparent;color:var(--trtt-menu-text,#fff);font-size:25px;line-height:1;padding:8px;cursor:pointer}",
      "#trtt-final-menu .trtt-links{display:flex;align-items:center;list-style:none;margin:0;padding:0;gap:0}",
      "#trtt-final-menu .trtt-links a{display:block;padding:17px 12px;color:var(--trtt-menu-text,#fff)!important;text-decoration:none;font-weight:700;font-size:13px;white-space:nowrap}",
      "#trtt-final-menu .trtt-links a:hover,#trtt-final-menu .trtt-links a:focus-visible{background:rgba(0,0,0,.16);outline-offset:-3px}",
      "@media(max-width:768px){#trtt-final-menu .trtt-bar{padding:0 12px}#trtt-final-menu .trtt-ham{display:block}#trtt-final-menu .trtt-links{display:none;position:absolute;left:0;right:0;top:100%;width:100%;flex-direction:column;align-items:stretch;background:var(--trtt-menu-mobile-bg,#ff5a8a);box-shadow:0 10px 20px rgba(0,0,0,.2)}#trtt-final-menu.open .trtt-links{display:flex}#trtt-final-menu .trtt-links a{padding:13px 16px;border-top:1px solid rgba(255,255,255,.16)}}",
      "@media(min-width:769px) and (max-width:950px){#trtt-final-menu .trtt-links a{padding-left:8px;padding-right:8px;font-size:12px}}"
    ].join("\n");
    document.head.appendChild(style);

    var menu = document.createElement("nav");
    menu.id = MENU_ID;
    menu.setAttribute("aria-label", "Main navigation");
    menu.style.setProperty("--trtt-menu-bg", config.menuBackground || "#ff2e63");
    menu.style.setProperty("--trtt-menu-mobile-bg", config.mobileBackground || "#ff5a8a");
    menu.style.setProperty("--trtt-menu-text", config.textColor || "#ffffff");

    var bar = document.createElement("div");
    bar.className = "trtt-bar";
    var brand = document.createElement("a");
    brand.className = "trtt-logo-txt";
    brand.href = "/";
    brand.textContent = typeof config.brand === "string" ? config.brand : "TRTT VOYAGE";
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
