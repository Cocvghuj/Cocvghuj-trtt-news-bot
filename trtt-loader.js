/*! TRTT CONTROL LOADER — VERSION 106
 * Single Blogger entry point.
 * Cache-busted, uniquely named V106 assets from the reviewed control branch.
 */
(function () {
  "use strict";

  var base = "https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@ab12821c5b78c4e044a3bfb35d664c26f0b603a8/";
  var version = "106-universe-room-pinned-20261112";

  if (!document.getElementById("trtt-control-css")) {
    var css = document.createElement("link");
    css.id = "trtt-control-css";
    css.rel = "stylesheet";
    css.href = base + "trtt-control/trtt-app-106.css?v=" + version;
    document.head.appendChild(css);
  }

  if (!document.getElementById("trtt-control-app")) {
    var app = document.createElement("script");
    app.id = "trtt-control-app";
    app.src = base + "trtt-control/trtt-app-106.js?v=" + version;
    app.defer = true;
    app.crossOrigin = "anonymous";
    document.head.appendChild(app);
  }
})();
