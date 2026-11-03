/* TRTT legacy compatibility loader.
   The canonical navigation and single Roksana Nila Vault are maintained in
   trtt-blog-menu.js and roksana-vault.js. Keep this filename for older gadgets. */
(function () {
  "use strict";
  var host = String(window.location.hostname || "").toLowerCase();
  if (host !== "trttnews24bd.blogspot.com" &&
      host !== "trttnews24bd.com" &&
      host !== "www.trttnews24bd.com") return;
  if (window.__TRTT_CANONICAL_LOADER__) return;
  window.__TRTT_CANONICAL_LOADER__ = true;
  if (document.getElementById("trtt-menu-loader")) return;
  var script = document.createElement("script");
  script.id = "trtt-menu-loader";
  script.src = "https://cocvghuj-trtt-news-bot.vercel.app/trtt-blog-menu.js";
  script.async = true;
  script.onerror = function () {
    if (window.console && console.warn) console.warn("TRTT navigation could not be loaded.");
  };
  (document.head || document.documentElement).appendChild(script);
}());
