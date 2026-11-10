/* TRTT CONTROL — VERSION 103 COMPATIBILITY ENTRY
 * Canonical implementation: /trtt-control/trtt-app.js
 * This legacy entry point delegates to the single v103 app.
 * It never clears, replaces, or rewrites Blogger menu contents.
 */
(function () {
  "use strict";
  if (window.__TRTT_CONTROL_V103__ || document.getElementById("trtt-control-app")) return;
  var script = document.createElement("script");
  script.id = "trtt-control-app";
  script.src = "https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@trtt-control-v103/trtt-control/trtt-app.js?v=103";
  script.defer = true;
  script.crossOrigin = "anonymous";
  document.head.appendChild(script);
})();
