/*! TRTT VOYAGE — INDEPENDENT THINKING ROOM DOOR / V106 */
(function () {
  "use strict";
  if (window.__TRTT_DOOR_V106__) return;
  window.__TRTT_DOOR_V106__ = true;

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

  function node(tag, className, value) {
    var el = document.createElement(tag);
    if (className) el.className = className;
    if (value !== undefined && value !== null) el.textContent = value;
    return el;
  }

  function makeRoute(item, className) {
    var a = node("a", className);
    a.href = item[2];
    a.appendChild(node("strong", "", item[0]));
    a.appendChild(node("span", "", item[1]));
    return a;
  }

  function findMount() {
    return document.querySelector("#header-wrap .header-menu") ||
      document.querySelector("#header-wrap #main-menu");
  }

  function buildNav() {
    var nav = node("nav", "trtt-control-nav");
    nav.id = "trtt-control-nav";
    nav.setAttribute("aria-label", "TRTT Voyage main menu");

    var brand = node("a", "trtt-control-brand", "TRTT VOYAGE");
    brand.href = "/";
    nav.appendChild(brand);

    var list = node("div", "trtt-route-list");
    ROUTES.forEach(function (item) {
      list.appendChild(makeRoute(item, "trtt-route-bubble"));
    });
    nav.appendChild(list);
    return nav;
  }

  function buildRoom() {
    var overlay = node("section", "trtt-room-overlay");
    overlay.id = "trtt-room-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-hidden", "true");
    overlay.setAttribute("aria-labelledby", "trtt-room-title");

    var panel = node("div", "trtt-room-panel");
    var header = node("header", "trtt-room-header");
    var identity = node("div", "trtt-room-identity");
    identity.appendChild(node("span", "trtt-room-kicker", "TRTT VOYAGE • SANLURI TO WORLD"));
    var title = node("h2", "", "THINKING ROOM");
    title.id = "trtt-room-title";
    identity.appendChild(title);
    identity.appendChild(node("p", "", "Muse  ✦  Abu  ✦  ChatGPT"));

    var close = node("button", "trtt-room-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close Thinking Room");
    header.appendChild(identity);
    header.appendChild(close);
    panel.appendChild(header);

    panel.appendChild(node("div", "trtt-room-lock", "ROKSANA — LOCKED"));

    var main = node("main", "trtt-room-main");
    main.appendChild(node("span", "trtt-room-kicker", "ONE TASK AT A TIME"));
    main.appendChild(node("h3", "", "Ideas become journeys when we work on them."));
    main.appendChild(node("p", "trtt-room-description",
      "A quiet workspace for planning, learning and building TRTT Voyage. Choose a destination to continue."));

    var destinations = node("nav", "trtt-room-links");
    destinations.setAttribute("aria-label", "TRTT Voyage destinations");
    ROUTES.forEach(function (item) {
      destinations.appendChild(makeRoute(item, "trtt-room-link"));
    });
    main.appendChild(destinations);
    panel.appendChild(main);

    panel.appendChild(node("footer", "trtt-room-footer",
      "TRTT MAC-787950 LOCKED • Made by MAC — Muse, Abu, ChatGPT"));
    overlay.appendChild(panel);

    function closeRoom() {
      overlay.classList.remove("is-open");
      overlay.setAttribute("aria-hidden", "true");
      document.documentElement.classList.remove("trtt-room-open");
      if (overlay.returnFocus && overlay.returnFocus.focus) {
        overlay.returnFocus.focus();
      }
    }

    close.addEventListener("click", closeRoom);
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeRoom();
    });

    document.addEventListener("keydown", function (event) {
      if (!overlay.classList.contains("is-open")) return;
      if (event.key === "Escape") {
        event.preventDefault();
        closeRoom();
        return;
      }
      if (event.key === "Tab") {
        var focusable = overlay.querySelectorAll("a[href],button:not([disabled])");
        if (!focusable.length) return;
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });

    overlay.openRoom = function (trigger) {
      overlay.returnFocus = trigger;
      overlay.classList.add("is-open");
      overlay.setAttribute("aria-hidden", "false");
      document.documentElement.classList.add("trtt-room-open");
      close.focus();
    };
    return overlay;
  }

  function ensureDoor() {
    var previousDoor = document.getElementById("trtt-thinking-room-trigger");
    if (previousDoor) previousDoor.remove();
    var previousRoom = document.getElementById("trtt-room-overlay");
    if (previousRoom) previousRoom.remove();

    var door = node("button", "trtt-thinking-room-trigger");
    door.type = "button";
    door.id = "trtt-thinking-room-trigger";
    door.setAttribute("aria-label", "Open Thinking Room");
    door.title = "Open Thinking Room";

    var icon = node("span", "trtt-door-icon", "✦");
    icon.setAttribute("aria-hidden", "true");
    door.appendChild(icon);

    var copy = node("span", "trtt-door-copy");
    copy.appendChild(node("strong", "", "THINKING ROOM"));
    copy.appendChild(node("small", "", "OPEN THE DOOR"));
    door.appendChild(copy);
    door.appendChild(node("span", "trtt-door-arrow", "↗"));

    var overlay = document.getElementById("trtt-room-overlay");
    if (!overlay) {
      overlay = buildRoom();
      document.body.appendChild(overlay);
    }

    door.addEventListener("click", function () {
      overlay.openRoom(door);
    });
    document.body.appendChild(door);
    return true;
  }

  function mount() {
    if (!document.body) return false;

    var nav = document.getElementById("trtt-control-nav");
    if (!nav) {
      var target = findMount();
      if (!target) return false;
      nav = buildNav();

      if (target.classList && target.classList.contains("header-menu")) {
        var oldMenu = target.querySelector("#main-menu") ||
          target.querySelector("#main-menu-nav");
        if (oldMenu && oldMenu.parentNode) {
          oldMenu.parentNode.replaceChild(nav, oldMenu);
        } else {
          target.insertBefore(nav, target.firstChild);
        }
      } else if (target.id === "main-menu" && target.parentNode) {
        target.parentNode.replaceChild(nav, target);
      } else {
        return false;
      }
    }

    ensureDoor();
    return true;
  }

  function start() {
    if (mount()) return;
    var observer = new MutationObserver(function () {
      if (mount()) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();