(function () {
  "use strict";

  const BASE =
    "https://raw.githubusercontent.com/Cocvghuj/Cocvghuj-trtt-news-bot/main/trtt-control/";

  function loadFile(id, tag, url) {
    if (document.getElementById(id)) return;

    const element = document.createElement(tag);
    element.id = id;

    if (tag === "link") {
      element.rel = "stylesheet";
      element.href = url;
    } else {
      element.src = url;
      element.defer = true;
    }

    document.head.appendChild(element);
  }

  function start() {
    loadFile("trtt-control-css", "link", BASE + "trtt-app.css");
    loadFile("trtt-control-app", "script", BASE + "trtt-app.js");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
