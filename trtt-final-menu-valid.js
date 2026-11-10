/*! TRTT CONTROL LOADER — VERSION 103
 * This is the single script referenced by the Blogger Theme.
 * It loads one canonical CSS file and one canonical application file.
 */
(function () {
  "use strict";
  var base = "https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@main/";
  var version = "103";
  if (!document.getElementById("trtt-control-css")) {
    var css = document.createElement("link");
    css.id = "trtt-control-css";
    css.rel = "stylesheet";
    css.href = base + "trtt-control/trtt-app.css?v=" + version;
    document.head.appendChild(css);
  }
  if (!document.getElementById("trtt-control-app")) {
    var app = document.createElement("script");
    app.id = "trtt-control-app";
    app.src = base + "trtt-control/trtt-app.js?v=" + version;
    app.defer = true;
    app.crossOrigin = "anonymous";
    document.head.appendChild(app);
  }
})();