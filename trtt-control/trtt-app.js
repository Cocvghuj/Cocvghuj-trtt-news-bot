/* TRTT VOYAGE — THINKING ROOM | MENU ONLY | VERSION 102 */
(function () {
  "use strict";

  var MENU = [
    { name: "Home", detail: "TRTT Voyage", href: "/" },
    { name: "My Diary", detail: "Personal journal", href: "/search/label/My%20Diary" },
    { name: "Flight", detail: "Flight services", href: "/search/label/Flight" },
    { name: "Ride", detail: "Ride services", href: "/search/label/Ride" },
    { name: "eSIM", detail: "Connectivity", href: "/search/label/eSIM" },
    { name: "Tour", detail: "Explore the world", href: "/search/label/Tour" },
    { name: "Shop", detail: "TRTT Shop", href: "/search/label/Shop" },
    { name: "Night", detail: "Night services", href: "/search/label/Night" },
    { name: "Thinking Room", detail: "Ideas and direction", current: true },
    { name: "ROKSANA LOCKED", detail: "Locked", locked: true },
    { name: "About MAC", detail: "Muse • Abu • ChatGPT", href: "/p/about-mac.html" }
  ];

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = text;
    return node;
  }

  function isHidden(node) {
    for (var current = node; current && current.nodeType === 1; current = current.parentElement) {
      var style = window.getComputedStyle ? window.getComputedStyle(current) : null;
      if (style && (style.display === "none" || style.visibility === "hidden")) return true;
      if (current.hidden || current.getAttribute("aria-hidden") === "true") return true;
    }
    return false;
  }

  // Only mount inside a visible Blogger header navigation/menu. Never use a floating/body fallback.
  function findHeaderMenu() {
    var selectors = [
      "#trtt-thinking-room-anchor",
      "#main-menu",
      "#header-wrap .header-menu",
      "#header-wrapper .header-menu",
      "#header .header-menu",
      ".header-menu",
      "#header-wrap nav",
      "#header-wrapper nav",
      "header nav",
      "nav[aria-label*='menu' i]",
      ".main-menu",
      "#menu"
    ];
    for (var i = 0; i < selectors.length; i++) {
      var node = document.querySelector(selectors[i]);
      if (node && !isHidden(node)) {
        if (node.id === "trtt-thinking-room-anchor") return node;
        if (node.matches("nav, #main-menu, .header-menu, .main-menu, #menu")) return node;
      }
    }
    return null;
  }

  function build() {
    if (document.getElementById("trtt-thinking-room")) return true;

    var mount = findHeaderMenu();
    if (!mount) return false;

    var launcher = mount.querySelector(".trtt-launcher");
    if (!launcher) {
      launcher = el("button", "trtt-launcher", "✦ THINKING ROOM");
      launcher.type = "button";
      launcher.setAttribute("aria-haspopup", "dialog");
      launcher.setAttribute("aria-expanded", "false");
      launcher.setAttribute("aria-controls", "trtt-thinking-room");
      mount.appendChild(launcher);
    }

    var overlay = el("div", "trtt-overlay");
    overlay.id = "trtt-thinking-room";
    overlay.setAttribute("aria-hidden", "true");

    var room = el("section", "trtt-room");
    room.setAttribute("role", "dialog");
    room.setAttribute("aria-modal", "true");
    room.setAttribute("aria-label", "TRTT Voyage menu");

    var header = el("header", "trtt-header");
    var title = el("div", "trtt-title");
    title.appendChild(el("small", "", "TRTT VOYAGE • SANLURI TO WORLD"));
    title.appendChild(el("h1", "", "Thinking Room"));
    title.appendChild(el("p", "", "Choose a destination."));
    var close = el("button", "trtt-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close menu");
    header.appendChild(title);
    header.appendChild(close);

    var core = el("div", "trtt-core");
    core.appendChild(el("span", "trtt-core-orbit", "✦"));
    core.appendChild(el("strong", "", "TRTT VOYAGE"));
    core.appendChild(el("small", "", "SANLURI TO WORLD"));

    var bubbles = el("div", "trtt-bubbles");
    MENU.forEach(function (item) {
      var node;
      if (item.href) {
        node = el("a", "trtt-bubble");
        node.href = item.href;
      } else {
        node = el("div", "trtt-bubble" + (item.locked ? " trtt-locked-item" : " trtt-current-item"));
        node.setAttribute("aria-disabled", "true");
        if (item.current) node.setAttribute("aria-current", "page");
      }
      node.appendChild(el("strong", "", item.name));
      node.appendChild(el("span", "", item.detail));
      bubbles.appendChild(node);
    });

    var footer = el("footer", "trtt-footer", "TRTT MAC-787950 LOCKED");
    var universe = el("div", "trtt-universe");
    universe.appendChild(core);
    universe.appendChild(bubbles);

    room.appendChild(header);
    room.appendChild(universe);
    room.appendChild(footer);
    overlay.appendChild(room);
    document.body.appendChild(overlay);

    function openMenu() {
      overlay.classList.add("active");
      overlay.setAttribute("aria-hidden", "false");
      launcher.setAttribute("aria-expanded", "true");
      document.documentElement.classList.add("trtt-locked");
      close.focus();
    }

    function closeMenu() {
      if (!overlay.classList.contains("active")) return;
      overlay.classList.remove("active");
      overlay.setAttribute("aria-hidden", "true");
      launcher.setAttribute("aria-expanded", "false");
      document.documentElement.classList.remove("trtt-locked");
      launcher.focus();
    }

    launcher.addEventListener("click", openMenu);
    close.addEventListener("click", closeMenu);
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeMenu();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && overlay.classList.contains("active")) closeMenu();
    });

    console.info("[TRTT] Version 102 menu mounted inside header menu:", mount.id || mount.className || mount.tagName);
    return true;
  }

  function start() {
    if (build()) return;
    var observer = new MutationObserver(function () {
      if (build()) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    console.warn("[TRTT] Version 102 waiting for a visible Blogger header menu.");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();