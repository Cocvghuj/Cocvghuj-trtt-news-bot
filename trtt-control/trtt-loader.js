(function () {
  "use strict";

  var BASE = "https://raw.githubusercontent.com/Cocvghuj/Cocvghuj-trtt-news-bot/main/trtt-control/";
  var VERSION = "20261109-7";

  function loadCss() {
    if (document.getElementById("trtt-control-css")) return;
    var css = document.createElement("link");
    css.id = "trtt-control-css";
    css.rel = "stylesheet";
    css.href = BASE + "trtt-app.css?v=" + VERSION;
    css.onerror = function () {
      if (css.getAttribute("data-trtt-fallback")) {
        console.error("[TRTT] Could not load trtt-app.css from either CDN.");
        return;
      }
      css.setAttribute("data-trtt-fallback", "1");
      css.href = "https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@main/trtt-control/trtt-app.css?v=" + VERSION;
    };
    (document.head || document.documentElement).appendChild(css);
  }

  function loadApp() {
    if (document.getElementById("trtt-control-app")) return;
    var app = document.createElement("script");
    app.id = "trtt-control-app";
    app.src = BASE + "trtt-app.js?v=" + VERSION;
    app.async = true;
    app.onerror = function () {
      if (app.getAttribute("data-trtt-fallback")) {
        console.error("[TRTT] Could not load trtt-app.js from either CDN.");
        return;
      }
      app.setAttribute("data-trtt-fallback", "1");
      app.src = "https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@main/trtt-control/trtt-app.js?v=" + VERSION;
    };
    (document.head || document.documentElement).appendChild(app);
  }

  function start() {
    loadCss();
    loadApp();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();
