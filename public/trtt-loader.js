/* TRTT GITHUB CONTROL LOADER */
(function () {
  "use strict";

  const BASE =
    "https://raw.githubusercontent.com/Cocvghuj/Cocvghuj-trtt-news-bot/main/trtt-control/";

  function start() {
    if (!document.getElementById("trtt-control-css")) {
      const css = document.createElement("link");
      css.id = "trtt-control-css";
      css.rel = "stylesheet";
      css.href = BASE + "trtt-app.css";
      document.head.appendChild(css);
    }

    if (!document.getElementById("trtt-control-app")) {
      const js = document.createElement("script");
      js.id = "trtt-control-app";
      js.src = BASE + "trtt-app.js";
      js.defer = true;
      document.body.appendChild(js);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
