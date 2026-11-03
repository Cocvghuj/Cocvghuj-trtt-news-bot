/* FlightScout Pro Blogger navigation loader.
   Add this script once using Blogger Layout > Add a Gadget > HTML/JavaScript. */
(function () {
  "use strict";
  var host = String(window.location.hostname || "").toLowerCase();
  if (host !== "flightscoutpro.blogspot.com" && host !== "www.flightscoutpro.blogspot.com") return;
  if (window.__FLIGHTSCOUT_PRO_MENU__) return;
  window.__FLIGHTSCOUT_PRO_MENU__ = true;

  var scriptUrl = document.currentScript && document.currentScript.src
    ? document.currentScript.src
    : "https://cocvghuj-trtt-news-bot.vercel.app/flightscoutpro-menu.js";
  var base = new URL(".", scriptUrl);
  var configUrl = new URL("flightscoutpro-control.json", base).href;
  var cssUrl = new URL("assets/css/flightscoutpro-theme.css", base).href;

  function safeHref(value) {
    if (typeof value !== "string") return null;
    if (value.charAt(0) === "/") return value;
    try { var u = new URL(value); return u.protocol === "https:" ? u.href : null; }
    catch (_) { return null; }
  }

  function addStyles() {
    if (document.getElementById("fsp-theme-css")) return;
    var link = document.createElement("link");
    link.id = "fsp-theme-css";
    link.rel = "stylesheet";
    link.href = cssUrl;
    document.head.appendChild(link);
  }

  function render(config) {
    if (!document.body || document.getElementById("fsp-main-menu")) return;
    config = config && typeof config === "object" ? config : {};
    var theme = config.theme || {};
    document.documentElement.style.setProperty("--fsp-brand", theme.primary || "#122b45");
    document.documentElement.style.setProperty("--fsp-accent", theme.accent || "#f28c28");
    addStyles();

    var nav = document.createElement("nav");
    nav.id = "fsp-main-menu";
    nav.setAttribute("aria-label", "Main navigation");
    nav.style.cssText = "position:sticky;top:0;z-index:99990;background:linear-gradient(110deg,#122b45,#174b73 72%,#167c91);border-bottom:3px solid #f28c28;box-shadow:0 8px 24px rgba(16,42,67,.15);font-family:Inter,system-ui,sans-serif";
    var wrap = document.createElement("div");
    wrap.style.cssText = "max-width:1280px;min-height:66px;margin:auto;padding:8px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px;position:relative";
    var brand = document.createElement("a");
    brand.href = "/";
    brand.textContent = config.brand || "FLIGHTSCOUT PRO";
    brand.style.cssText = "color:#fff;text-decoration:none;font-size:15px;font-weight:900;letter-spacing:.09em;white-space:nowrap";
    wrap.appendChild(brand);

    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.textContent = "☰";
    toggle.setAttribute("aria-label", "Open menu");
    toggle.setAttribute("aria-expanded", "false");
    toggle.style.cssText = "display:none;border:1px solid #ffffff55;border-radius:9px;background:#ffffff12;color:#fff;padding:9px 12px;font-size:20px;cursor:pointer";
    wrap.appendChild(toggle);

    var list = document.createElement("ul");
    list.style.cssText = "display:flex;align-items:center;justify-content:flex-end;gap:4px;flex-wrap:wrap;list-style:none;margin:0;padding:0";
    (Array.isArray(config.menu) ? config.menu : []).forEach(function (item) {
      if (!item || typeof item.label !== "string") return;
      var href = safeHref(item.href);
      if (!href) return;
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = href;
      a.textContent = item.label;
      a.style.cssText = "display:block;padding:9px 10px;border-radius:8px;color:#edf6fc;text-decoration:none;font-size:12px;font-weight:750";
      a.addEventListener("mouseenter", function () { a.style.background = "#ffffff20"; a.style.color = "#f5c451"; });
      a.addEventListener("mouseleave", function () { a.style.background = "transparent"; a.style.color = "#edf6fc"; });
      li.appendChild(a);
      list.appendChild(li);
    });
    wrap.appendChild(list);
    nav.appendChild(wrap);
    document.body.insertBefore(nav, document.body.firstChild);

    var style = document.createElement("style");
    style.textContent = "@media(max-width:980px){#fsp-main-menu>div{padding:8px 14px!important}#fsp-main-menu button{display:block!important}#fsp-main-menu ul{display:none!important;position:absolute;left:0;right:0;top:100%;padding:10px 14px 15px!important;background:#122b45;box-shadow:0 14px 24px #102a4333;flex-direction:column;align-items:stretch!important;flex-wrap:nowrap!important}#fsp-main-menu.is-open ul{display:flex!important}#fsp-main-menu li a{padding:12px 13px!important;border-top:1px solid #ffffff18}}";
    document.head.appendChild(style);

    function close() { nav.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); toggle.setAttribute("aria-label", "Open menu"); }
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.setAttribute("aria-label", open ? "Open menu" : "Close menu");
      nav.classList.toggle("is-open", !open);
    });
    list.addEventListener("click", function (event) { if (event.target.closest("a")) close(); });
    document.addEventListener("keydown", function (event) { if (event.key === "Escape") close(); });
    document.addEventListener("click", function (event) { if (!nav.contains(event.target)) close(); });
  }

  fetch(configUrl, { cache: "no-cache" })
    .then(function (response) { if (!response.ok) throw new Error("Config unavailable"); return response.json(); })
    .then(render)
    .catch(function () { render(null); });
}());
