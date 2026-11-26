(function () {
  "use strict";

  var script = document.currentScript;
  var configUrl = script && script.src
    ? new URL("blog-control.json", script.src).href
    : "https://cocvghuj-trtt-news-bot-git-main-trtt6.vercel.app/blog-control.json";

  function createMenuItem(item) {
    if (!item || typeof item.label !== "string" || !item.label.trim() ||
        typeof item.href !== "string" || !item.href.trim()) {
      throw new Error("Invalid Blogger menu item.");
    }

    var url = new URL(item.href, window.location.origin);
    if (url.protocol !== "https:" || !url.hostname) {
      throw new Error("Only HTTPS Blogger menu links are allowed.");
    }

    var li = document.createElement("li");
    var link = document.createElement("a");
    link.href = url.href;
    link.textContent = item.label.trim();
    link.setAttribute("role", "menuitem");
    li.appendChild(link);
    return li;
  }

  function renderMenu(config) {
    if (!config || !Array.isArray(config.menu) ||
        config.menu.length < 1 || config.menu.length > 8) {
      throw new Error("Invalid Blogger menu configuration.");
    }

    var navs = document.querySelectorAll("#main-menu-nav");
    if (!navs || !navs.length) return;

    // Prepare every item before changing either menu. On failure, preserve the
    // current Blogger menu rather than leaving a partially rendered navigation.
    var preparedItems = config.menu.map(createMenuItem);

    Array.prototype.forEach.call(navs, function (nav) {
      while (nav.firstChild) nav.removeChild(nav.firstChild);
      preparedItems.forEach(function (item) {
        nav.appendChild(item.cloneNode(true));
      });
    });
  }

  function loadMenu() {
    fetch(configUrl, {
      method: "GET",
      mode: "cors",
      credentials: "omit",
      cache: "no-store"
    })
      .then(function (response) {
        if (!response.ok) throw new Error("Menu configuration request failed.");
        return response.json();
      })
      .then(renderMenu)
      .catch(function () {
        // Fail closed: keep the Blogger-provided navigation intact.
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadMenu, { once: true });
  } else {
    loadMenu();
  }
})();
