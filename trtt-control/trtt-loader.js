(function () {
  "use strict";

  var BASE = "https://raw.githubusercontent.com/Cocvghuj/Cocvghuj-trtt-news-bot/main/trtt-control/";
  var VERSION = "20261109-2";

  function loadCss() {
    if (document.getElementById("trtt-control-css")) return;
    var css = document.createElement("link");
    css.id = "trtt-control-css";
    css.rel = "stylesheet";
    css.href = BASE + "trtt-app.css?v=" + VERSION;
    css.onerror = function () {
      console.error("[TRTT] Could not load trtt-app.css from GitHub.");
    };
    document.head.appendChild(css);
  }

  function loadApp() {
    if (document.getElementById("trtt-control-app")) return;
    var app = document.createElement("script");
    app.id = "trtt-control-app";
    app.src = BASE + "trtt-app.js?v=" + VERSION;
    app.async = true;
    app.onerror = function () {
      console.error("[TRTT] Could not load trtt-app.js from GitHub.");
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
