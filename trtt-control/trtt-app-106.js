/*! TRTT VOYAGE — THINKING ROOM / V106 CLEAN REBUILD */
(function () {
  "use strict";
  if (window.__TRTT_DOOR_V106_CLEAN__) return;
  window.__TRTT_DOOR_V106_CLEAN__ = true;

  var ROUTES = [
    ["Home", "Start here", "/"],
    ["My Diary", "Personal journal", "/search/label/My%20Diary"],
    ["Flight", "Flight services", "/search/label/Flight"],
    ["Ride", "Ride services", "/search/label/Ride"],
    ["eSIM", "Stay connected", "/search/label/eSIM"],
    ["Tour", "Explore places", "/search/label/Tour"],
    ["Shop", "TRTT Shop", "/search/label/Shop"],
    ["Night", "Night services", "/search/label/Night"]
  ];

  function el(tag, className, text) {
    var item = document.createElement(tag);
    if (className) item.className = className;
    if (text != null) item.textContent = text;
    return item;
  }

  function routeLink(route, className) {
    var link = el("a", className);
    link.href = route[2];
    link.appendChild(el("strong", "", route[0]));
    link.appendChild(el("span", "", route[1]));
    return link;
  }

  function buildMenu() {
    if (document.getElementById("trtt-control-nav")) return;
    var target = document.querySelector("#header-wrap .header-menu") ||
      document.querySelector("#header-wrap #main-menu");
    if (!target) return;

    var nav = el("nav", "trtt-control-nav");
    nav.id = "trtt-control-nav";
    nav.setAttribute("aria-label", "TRTT Voyage main menu");
    var brand = el("a", "trtt-control-brand", "TRTT VOYAGE");
    brand.href = "/";
    nav.appendChild(brand);

    var list = el("div", "trtt-route-list");
    ROUTES.forEach(function (route) {
      list.appendChild(routeLink(route, "trtt-route-bubble"));
    });
    nav.appendChild(list);

    var old = target.querySelector("#main-menu") ||
      target.querySelector("#main-menu-nav");
    if (target.classList.contains("header-menu") && old && old.parentNode) {
      old.parentNode.replaceChild(nav, old);
    } else if (target.classList.contains("header-menu")) {
      target.insertBefore(nav, target.firstChild);
    } else if (target.id === "main-menu" && target.parentNode) {
      target.parentNode.replaceChild(nav, target);
    }
  }

  function openRoom(overlay, door) {
    overlay.classList.add("is-open");
    overlay.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("trtt-room-open");
    door.setAttribute("aria-expanded", "true");
    overlay.querySelector(".trtt-room-close").focus();
  }

  function closeRoom(overlay, door) {
    overlay.classList.remove("is-open");
    overlay.setAttribute("aria-hidden", "true");
    document.documentElement.classList.remove("trtt-room-open");
    door.setAttribute("aria-expanded", "false");
    door.focus();
  }

  function buildDoor() {
    if (document.getElementById("trtt-thinking-room-trigger")) return;

    var door = el("button", "trtt-thinking-room-trigger");
    door.id = "trtt-thinking-room-trigger";
    door.type = "button";
    door.setAttribute("aria-label", "Open Thinking Room");
    door.setAttribute("aria-controls", "trtt-room-overlay");
    door.setAttribute("aria-expanded", "false");
    door.appendChild(el("span", "trtt-door-symbol", "✦"));
    var label = el("span", "trtt-door-label");
    label.appendChild(el("strong", "", "THINKING ROOM"));
    label.appendChild(el("small", "", "ENTER THE ROOM"));
    door.appendChild(label);
    door.appendChild(el("span", "trtt-door-arrow", "↗"));

    var overlay = el("section", "trtt-room-overlay");
    overlay.id = "trtt-room-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-hidden", "true");
    overlay.setAttribute("aria-labelledby", "trtt-room-title");

    var panel = el("div", "trtt-room-panel");
    var header = el("header", "trtt-room-header");
    var identity = el("div", "trtt-room-identity");
    identity.appendChild(el("span", "trtt-room-eyebrow", "TRTT VOYAGE • SANLURI TO WORLD"));
    var title = el("h2", "", "THINKING ROOM");
    title.id = "trtt-room-title";
    identity.appendChild(title);
    identity.appendChild(el("p", "", "Muse  ✦  Abu  ✦  ChatGPT"));
    var close = el("button", "trtt-room-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close Thinking Room");
    header.appendChild(identity);
    header.appendChild(close);
    panel.appendChild(header);

    panel.appendChild(el("div", "trtt-room-lock", "ROKSANA — LOCKED"));
    var main = el("main", "trtt-room-main");
    main.appendChild(el("span", "trtt-room-eyebrow", "ONE TASK AT A TIME"));
    main.appendChild(el("h3", "", "A quiet place to think. A clear place to build."));
    main.appendChild(el("p", "trtt-room-description",
      "Plan the next journey, work on an idea, and build TRTT Voyage one task at a time."));
    var links = el("nav", "trtt-room-links");
    links.setAttribute("aria-label", "Thinking Room destinations");
    ROUTES.forEach(function (route) {
      links.appendChild(routeLink(route, "trtt-room-link"));
    });
    main.appendChild(links);
    panel.appendChild(main);
    panel.appendChild(el("footer", "trtt-room-footer",
      "TRTT MAC-787950 LOCKED • Made by MAC — Muse, Abu, ChatGPT"));
    overlay.appendChild(panel);

    door.addEventListener("click", function () { openRoom(overlay, door); });
    close.addEventListener("click", function () { closeRoom(overlay, door); });
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeRoom(overlay, door);
    });
    document.addEventListener("keydown", function (event) {
      if (!overlay.classList.contains("is-open")) return;
      if (event.key === "Escape") {
        event.preventDefault();
        closeRoom(overlay, door);
      }
    });

    document.body.appendChild(overlay);
    document.body.appendChild(door);
  }

  function start() {
    if (!document.body) return;
    buildMenu();
    buildDoor();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();