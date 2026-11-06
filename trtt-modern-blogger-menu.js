/* TRTT Modern Blogger Navigation
 * Standalone replacement navigation. Does not edit, hide, clone, or cover the Blogger logo/header.
 * Load this file after the existing Blogger header markup.
 */
(function () {
  "use strict";
  if (window.__TRTT_MODERN_NAV__) return;
  window.__TRTT_MODERN_NAV__ = true;

  var LINKS = [
    ["Home", "/"],
    ["Latest News", "/search/label/TRTT%20News"],
    ["Europe Travel", "/search/label/Europe%20Travel"],
    ["Flights", "/search/label/Flights"],
    ["eSIM", "/search/label/eSIM"],
    ["Hotels", "/search/label/Hotels"],
    ["Roksana Vault", "/p/roksana-vault.html"],
    ["Travel Tools", "https://cocvghuj-trtt-news-bot.vercel.app/"],
    ["About", "/p/about-us.html"],
    ["Contact", "/p/contact.html"]
  ];

  var CSS = [
    "#trtt-modern-nav{--tmn-ink:#14213d;--tmn-accent:#ef476f;--tmn-line:#e7ebf2;position:relative;z-index:40;width:100%;box-sizing:border-box;background:#fff;border-top:1px solid var(--tmn-line);border-bottom:1px solid var(--tmn-line);box-shadow:0 5px 18px rgba(20,33,61,.07);font:600 14px/1.4 Inter,system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--tmn-ink)}",
    "#trtt-modern-nav *{box-sizing:border-box}",
    "#trtt-modern-nav .tmn-inner{max-width:1240px;margin:0 auto;padding:0 20px;min-height:62px;display:flex;align-items:center;gap:16px}",
    "#trtt-modern-nav .tmn-links{display:flex;align-items:center;justify-content:center;gap:4px;flex:1;flex-wrap:wrap;min-width:0}",
    "#trtt-modern-nav a{color:var(--tmn-ink);text-decoration:none}",
    "#trtt-modern-nav .tmn-link{display:inline-flex;align-items:center;min-height:40px;padding:9px 11px;border-radius:9px;white-space:nowrap;transition:background .18s,color .18s}",
    "#trtt-modern-nav .tmn-link:hover,#trtt-modern-nav .tmn-link:focus-visible{background:#fff0f3;color:#c82f56;outline:none}",
    "#trtt-modern-nav .tmn-link[aria-current='page']{color:#c82f56;background:#fff0f3}",
    "#trtt-modern-nav .tmn-search{display:flex;align-items:center;gap:6px;flex:0 0 auto}",
    "#trtt-modern-nav .tmn-search input{width:145px;min-width:0;height:38px;border:1px solid #d9dfeb;border-radius:9px;padding:0 11px;font:500 13px inherit;color:var(--tmn-ink);background:#fff}",
    "#trtt-modern-nav .tmn-search button,#trtt-modern-nav .tmn-toggle{height:38px;border:0;border-radius:9px;padding:0 12px;background:var(--tmn-ink);color:#fff;font:700 13px inherit;cursor:pointer}",
    "#trtt-modern-nav .tmn-toggle{display:none;align-items:center;justify-content:center;gap:8px;min-width:94px}",
    "#trtt-modern-nav button:focus-visible,#trtt-modern-nav input:focus-visible{outline:3px solid rgba(239,71,111,.35);outline-offset:2px}",
    "@media(max-width:980px){#trtt-modern-nav .tmn-inner{min-height:58px;justify-content:space-between;padding:0 16px}#trtt-modern-nav .tmn-toggle{display:inline-flex}#trtt-modern-nav .tmn-links{display:none;position:absolute;top:100%;left:0;right:0;max-height:calc(100vh - 120px);overflow:auto;padding:12px 16px 18px;background:#fff;border-bottom:1px solid var(--tmn-line);box-shadow:0 16px 28px rgba(20,33,61,.14);align-items:stretch;flex-direction:column;gap:3px}#trtt-modern-nav.is-open .tmn-links{display:flex}#trtt-modern-nav .tmn-link{width:100%;min-height:46px;padding:11px 13px}#trtt-modern-nav .tmn-search{margin-left:auto}#trtt-modern-nav .tmn-search input{width:min(30vw,150px)}}",
    "@media(max-width:480px){#trtt-modern-nav .tmn-inner{gap:8px;padding:0 12px}#trtt-modern-nav .tmn-search input{width:100px}#trtt-modern-nav .tmn-search button{padding:0 10px}#trtt-modern-nav .tmn-toggle{min-width:82px;padding:0 9px}}",
    "@media(prefers-reduced-motion:reduce){#trtt-modern-nav *{transition:none!important;scroll-behavior:auto!important}}"
  ].join("\n");

  function make(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function mount() {
    if (document.getElementById("trtt-modern-nav")) return;

    // Insert after the existing brand/header area; never place controls over the logo.
    var header = document.querySelector("header#header, #header.header-widget, header.header-widget, .header-widget");
    if (!header || !header.parentNode) return;

    if (!document.getElementById("trtt-modern-nav-style")) {
      var style = make("style");
      style.id = "trtt-modern-nav-style";
      style.textContent = CSS;
      document.head.appendChild(style);
    }

    var nav = make("nav");
    nav.id = "trtt-modern-nav";
    nav.setAttribute("aria-label", "Main navigation");

    var inner = make("div", "tmn-inner");
    var toggle = make("button", "tmn-toggle", "☰  Menu");
    toggle.type = "button";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", "trtt-modern-nav-links");

    var links = make("div", "tmn-links");
    links.id = "trtt-modern-nav-links";

    LINKS.forEach(function (item) {
      var a = make("a", "tmn-link", item[0]);
      a.href = item[1];
      if (item[1].indexOf("https://") === 0) {
        a.target = "_blank";
        a.rel = "noopener noreferrer";
      }
      try {
        var target = new URL(a.href, location.href);
        var current = new URL(location.href);
        if (target.origin === current.origin && target.pathname.replace(/\/$/, "") === current.pathname.replace(/\/$/, "")) {
          a.setAttribute("aria-current", "page");
        }
      } catch (_) {}
      a.addEventListener("click", closeMenu);
      links.appendChild(a);
    });

    var search = make("form", "tmn-search");
    search.action = "/";
    search.method = "get";
    var input = make("input");
    input.type = "search";
    input.name = "q";
    input.placeholder = "Search…";
    input.setAttribute("aria-label", "Search this blog");
    var submit = make("button", "", "Search");
    submit.type = "submit";
    search.appendChild(input);
    search.appendChild(submit);

    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "✕  Close" : "☰  Menu";
    });

    function closeMenu() {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.textContent = "☰  Menu";
    }

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeMenu();
    });
    document.addEventListener("click", function (event) {
      if (!nav.contains(event.target)) closeMenu();
    });

    inner.appendChild(toggle);
    inner.appendChild(links);
    inner.appendChild(search);
    nav.appendChild(inner);

    if (header.nextSibling) header.parentNode.insertBefore(nav, header.nextSibling);
    else header.parentNode.appendChild(nav);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount, { once: true });
  } else {
    mount();
  }
})();