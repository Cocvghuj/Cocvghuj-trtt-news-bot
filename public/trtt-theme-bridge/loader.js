/* TRTT Voyage JSDelivr Theme Bridge Loader
   Enables the scoped CSS layer. Does not call Blogger APIs or modify post data. */
(function () {
  "use strict";
  var root = document.documentElement;
  if (!root || root.getAttribute("data-trtt-theme") === "enabled") return;
  root.setAttribute("data-trtt-theme", "enabled");
  root.setAttribute("data-trtt-theme-bridge", "github-jsdelivr");
})();
