/*! TRTT CONTROL LOADER — VERSION 107 */
(function () {
  "use strict";
  if (window.__TRTT_LOADER_V107__) return;
  window.__TRTT_LOADER_V107__ = true;

  var base = "https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@trtt-control-v107/";
  var version = "107";

  if (!document.getElementById("trtt-control-css")) {
    var css = document.createElement("link");
    css.id = "trtt-control-css";
    css.rel = "stylesheet";
    css.href = base + "trtt-control/trtt-app-107.css?v=" + version;
    document.head.appendChild(css);
  }

  if (!document.getElementById("trtt-control-app")) {
    var app = document.createElement("script");
    app.id = "trtt-control-app";
    app.src = base + "trtt-control/trtt-app-107.js?v=" + version;
    app.defer = true;
    app.crossOrigin = "anonymous";
    document.head.appendChild(app);
  }
})();
